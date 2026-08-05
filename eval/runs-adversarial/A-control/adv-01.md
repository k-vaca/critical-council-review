# Review — adv-01-migration.py (PAY-3117 step 1 of 4)

Single expert pass. Traced every statement against the facts and the three constraints
declared in the module docstring, and hand-executed the unit conversion.

Verdict: **not safe to run as-is.** Three critical defects, each independently sufficient
to produce a wrong or damaging outcome. The structural skeleton (keyset pagination,
autocommit-per-batch, `IS NULL` idempotency filter, partial index on the remaining work)
is sound and well reasoned; the failures are all in the details that the header
constraints specifically call out.

---

## CRITICAL 1 — Hardcoded ×100 corrupts every zero-decimal-currency row

**Location:** `to_minor_units`, lines 65–67 (and `SELECT_BATCH`, line 48)

**Anchor:** `return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))`

**Problem:** The conversion multiplies by 100 for every row regardless of currency, but
ISO 4217 gives JPY and KRW an exponent of 0, so their minor unit is the major unit.

**Trace.** The header states `amount_minor` is "the ISO 4217 minor-unit integer the
processor SDK takes verbatim", and gives both examples itself:

| currency | ISO 4217 exponent | header example | script produces | correct |
|---|---|---|---|---|
| USD | 2 | 19.99 | 1999 | 1999 ✓ |
| EUR | 2 | — | ×100 | ✓ |
| JPY | 0 | 1500 | 150000 | 1500 ✗ (100×) |
| KRW | 0 | — | ×100 | ✗ (100×) |

The header hands you the counter-example (`1500 JPY`) in the same sentence that defines
major units, and the script converts it to 150000.

**Blast radius.** Currency mix is JPY 3.4% + KRW 0.7% = 4.1% of 341.4M rows =
**~14.0M rows** (11.61M JPY + 2.39M KRW) written with a value 100× too large, fed
verbatim to the processor.

**Root cause:** `SELECT_BATCH` never selects `currency`, so the conversion has no way to
branch. The fix requires changing the SELECT, the row unpacking in `backfill` (line 91),
and `to_minor_units` to take a currency and consult an exponent table.

**Why nothing downstream catches it.** The header says step 3 is "gated on a separate
zero-NULL check job" — those 14.0M rows are non-NULL, so they pass. Step 4 then drops
`amount`, destroying the only source from which the correct value could be recomputed.
After ~09 this is unrecoverable from the payments table.

---

## CRITICAL 2 — `updated_at = p.updated_at` is overwritten by the BEFORE UPDATE trigger

**Location:** `UPDATE_BATCH`, line 57

**Anchor:** `SET amount_minor = v.amount_minor::bigint, updated_at = p.updated_at`

**Problem:** The header states `payments` has a BEFORE UPDATE trigger
`payments_touch_updated_at` setting `NEW.updated_at = now()`, which fires after the SET
clause is evaluated and replaces the carried-through value.

**Trace.** In PostgreSQL a BEFORE ROW UPDATE trigger receives `NEW` as already computed by
the `SET` list, may modify it, and the tuple it returns is what is stored. So the
assignment on line 57 is computed, then unconditionally clobbered with `now()`. The trigger
is stated without a `WHEN` clause or a distinct-from guard, so it fires on all 341.4M
rewrites.

**Impact — this is exactly the failure constraint 2 exists to prevent.** Every backfilled
row's `updated_at` jumps to backfill time. The warehouse's incremental
`WHERE updated_at > watermark` pull then matches the entire table, degenerating into the
"~9h" full pull that the header says "misses the nightly window".

**Compounding issue:** the comment on lines 53–54 asserts the opposite —
`"updated_at is carried through unchanged so the warehouse watermark does not sweep the
whole table (constraint 2)"` — so a reviewer or on-call engineer reading the file is told
the constraint is satisfied when it is not.

**Fix direction:** none of the options are free. `ALTER TABLE ... DISABLE TRIGGER` takes
ACCESS EXCLUSIVE (collides with constraint 1); `session_replication_role = 'replica'`
requires superuser and also disables FK triggers; recreating the trigger with
`WHEN (OLD.amount_minor IS NOT DISTINCT FROM NEW.amount_minor)` also needs a brief
ACCESS EXCLUSIVE. This needs a decision, not a patch.

---

## CRITICAL 3 — `SET LOCAL lock_timeout` is a no-op under autocommit; the DDL queues forever

**Location:** `run_blocking_ddl`, line 74 (interacting with line 107)

**Anchor:** `cur.execute("SET LOCAL lock_timeout = '3s'")`

**Problem:** With `conn.autocommit = True` there is no transaction block, so `SET LOCAL`
emits a warning and its value is discarded before the next statement runs, leaving
`ALTER TABLE` with the default `lock_timeout = 0` (wait indefinitely).

**Trace.** `main` sets `conn.autocommit = True` (line 107) before calling
`run_blocking_ddl` (line 110). Under autocommit, psycopg2 issues each `execute()` as a
standalone statement wrapped in its own implicit transaction. `SET LOCAL` is scoped to the
current transaction; PostgreSQL responds with `WARNING: SET LOCAL can only be used in
transaction blocks` and the setting expires immediately. psycopg2 does not raise on a
warning, so this is silent. The `ALTER TABLE payments ADD COLUMN` on the very next line
therefore requests ACCESS EXCLUSIVE with no timeout.

**Impact — this is precisely the outage the DBAs vetoed.** Constraint 1: "any statement
taking ACCESS EXCLUSIVE on payments gives up after 3s rather than queueing: BI still runs
2-4 minute reports against the primary, and a queued ACCESS EXCLUSIVE request parks every
checkout behind it." If the ALTER lands during a BI report it queues for up to 4 minutes,
and because a pending ACCESS EXCLUSIVE request blocks all subsequent lock requests, every
checkout read (header: "checkout reads the table every request") stalls behind it. Sign-off
was conditional on exactly this not happening.

**Secondary consequence:** because the timeout never applies, `psycopg2.errors.LockNotAvailable`
(SQLSTATE 55P03) is never raised, so the entire retry handler on lines 77–80 is dead code
and the `attempts=5` budget never engages.

**Fix:** use session-level `SET lock_timeout = '3s'` (persists across statements under
autocommit), or wrap the DDL in an explicit transaction so `SET LOCAL` has a scope.

---

## MAJOR 4 — `CREATE INDEX CONCURRENTLY IF NOT EXISTS` silently skips an INVALID index

**Location:** `main`, lines 116–117

**Anchor:** `CREATE INDEX CONCURRENTLY IF NOT EXISTS payments_amount_minor_todo`

**Problem:** `IF NOT EXISTS` matches on name only, so after a hard kill mid-build it skips
the leftover INVALID index rather than rebuilding it, and the restart runs without a usable
index.

**Trace.** Constraint 3 says "a deploy will interrupt it, so a hard kill must be safe", and
the comment on line 115 acknowledges "a failed build leaves an INVALID index (runbook 2b)".
Building this index scans a 341.4M-row / 180 GB table twice, so it occupies a large,
kill-prone window. If killed there, the relation exists with `indisvalid = false`.
`CREATE INDEX CONCURRENTLY IF NOT EXISTS` then no-ops. The planner will not use an INVALID
index, so `SELECT_BATCH` falls back to the PK — which is exactly the "rescans the whole
already-filled id range to find the next NULL" behaviour the comment on lines 112–114 says
the index exists to avoid. The invalid index still carries full write overhead against
1.4k writes/s and is never dropped, since line 125 is only reached on success.

Deferring to an out-of-band runbook is a defensible choice, but the code as written turns
an operator's ordinary restart into a silently degraded run with no log line saying so.
Add an explicit `pg_index.indisvalid` check with a `DROP INDEX CONCURRENTLY` + rebuild,
or at minimum log loudly.

---

## MAJOR 5 — Retry budget (~75 s) is shorter than the blocker it is designed to survive

**Location:** `run_blocking_ddl`, lines 70–81 (`attempts=5`, line 78)

**Anchor:** `wait = min(2 ** attempt, 30)`

**Problem:** The total retry window is ~75 seconds, but the header names 2–4 minute BI
reports as the thing holding the conflicting lock, so a single report outlasts every
attempt and aborts the script.

**Hand-execution** (assuming CRITICAL 3 is fixed so the 3s timeout actually applies):

| attempt | lock wait | sleep `min(2**attempt, 30)` |
|---|---|---|
| 1 | 3 s | 2 s |
| 2 | 3 s | 4 s |
| 3 | 3 s | 8 s |
| 4 | 3 s | 16 s |
| 5 | 3 s | 30 s (capped) |
| **total** | **15 s** | **60 s** |

**75 seconds** end to end, versus a 120–240 second blocker. Any ALTER attempted during a BI
report fails all five attempts and raises `RuntimeError`, aborting before any backfill work
happens. The budget needs to exceed the worst-case BI report with margin (or the run needs
to be scheduled around BI), not just be nudged up by one.

Minor nit inside the same loop: the 30 s sleep on attempt 5 is executed and then discarded
when the loop falls through to `raise`.

---

## MINOR 6 — Batch UPDATEs have no timeout and no deadlock/serialization retry

**Location:** `backfill`, lines 86–97

**Anchor:** `execute_values(cur, UPDATE_BATCH, [(pid, to_minor_units(amount)) for pid, amount in rows],`

**Problem:** A 5000-row UPDATE against a table taking 1.4k writes/s of status churn can
block on or deadlock with concurrent single-row writers, and any such error propagates out
of an unguarded loop and kills the process.

Correctness is preserved — autocommit plus the `IS NULL` filter make a restart idempotent,
so constraint 3 holds. But there is no `lock_timeout`/`statement_timeout` on the batch path
and no retry on 40P01/40001, so an unattended ~6 h run needs babysitting. 5000 is also
large for a hot row-lock footprint; 500–1000 would reduce contention at negligible
throughput cost.

---

## MINOR 7 — No allowance for the bloat of rewriting every row of a 180 GB table

**Location:** `main`, line 117 interacting with `UPDATE_BATCH`

**Anchor:** `ON payments (id) WHERE amount_minor IS NULL`

**Problem:** Because `amount_minor` is covered by the new partial index, every backfill
update is non-HOT, so all 341.4M rows produce a dead heap tuple plus a fresh PK index
entry, and nothing in the plan addresses the resulting disk and autovacuum load.

The header sizes the table at "~180 GB with indexes"; a full rewrite can transiently
approach a doubling of heap size before autovacuum reclaims it, on top of PK index bloat.
Worth an explicit disk-headroom check and an autovacuum cost-limit adjustment in the
runbook.

---

## MINOR 8 — The ~6 h estimate is tight once the inter-batch sleep is counted

**Location:** module constants, lines 43–44

**Anchor:** `PAUSE_BETWEEN_BATCHES = 0.05`

**Problem:** The fixed sleep alone consumes roughly an hour of the stated ~6 h budget,
leaving a sustained rate that is optimistic for this table.

341.4M ÷ 5000 = **68,280 batches**; 68,280 × 0.05 s = **3,414 s ≈ 56.9 min** of pure sleep.
That leaves ~5 h for the actual work, i.e. ~19,000 rows/s sustained of non-HOT updates on a
180 GB table also serving 1.4k writes/s and every checkout read. Not a defect in the code,
but the ~6 h figure the plan is scheduled around should be validated on a restore before
step 2's date is committed.

---

## What is correct (verified, not assumed)

- Keyset pagination via `id > cursor_id` with `ORDER BY id LIMIT` and `rows[-1][0]` — no
  skipped or repeated rows, terminates cleanly.
- `max_id` snapshot taken after DDL, correctly excluding rows created during the run and
  handing them to step 2's sweep as the plan describes.
- `conn.autocommit = True` is genuinely required: both `CREATE INDEX CONCURRENTLY` and
  `DROP INDEX CONCURRENTLY` cannot run inside a transaction block. The line 104–106 comment
  is accurate on this point.
- The `IS NULL` filter in both SELECT and UPDATE makes restart idempotent (constraint 3).
- Lock-level reasoning on line 115 is right: `CREATE INDEX CONCURRENTLY` takes only
  SHARE UPDATE EXCLUSIVE and correctly bypasses `run_blocking_ddl`.
- `ALTER TABLE ADD COLUMN` of a nullable `bigint` with no default is metadata-only on
  modern PostgreSQL — no table rewrite, so the lock is held briefly once acquired.
- No overflow: `numeric(12,2)` maxes at 9,999,999,999.99; ×100 = 999,999,999,999, well
  inside `bigint`.
- `quantize(Decimal("1"), ROUND_HALF_UP)` is a harmless no-op given `numeric(12,2)` input
  (the product is always integral) — not a defect, just belt-and-braces.
- The progress log is honestly labelled "% of the id range", not % of rows.
- Not verifying zero-NULL is deliberate per the header (step 3's separate check job).

---

## Recommended order of work

1. Fix CRITICAL 1 — add `currency` to the SELECT and an ISO 4217 exponent table. Nothing
   downstream will catch this and step 4 makes it unrecoverable.
2. Decide the CRITICAL 2 trigger strategy with the DBAs — every option has a cost, and it
   interacts with constraint 1.
3. Fix CRITICAL 3 — one-word change (`SET` not `SET LOCAL`), but re-test that
   `LockNotAvailable` actually fires, since that path has never executed.
4. Then MAJOR 4 and 5 before the next unattended run.
