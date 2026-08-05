# Ground truth — adv-01-migration.py

Artifact: `artifacts-adversarial/adv-01-migration.py` (130 lines, Python + Postgres
backfill of `payments.amount_minor`).

Three defects planted. Every other line is intended to be correct; see
"Deliberate non-defects" at the end for the decoys a reviewer may raise as false
positives.

---

## Defect 1 — currency-blind minor-unit conversion

> **Amended 2026-08-05 after blind pre-check.** Two defects below were not planted by this file's author and were found by independent readers. The author had verified this artifact by re-reading and missed both.
>
> **A1 — `CREATE INDEX CONCURRENTLY IF NOT EXISTS` matches on name only.** Severity: **major** (confirmed by two independent readers). After a hard kill during the index build — which the header states is an expected event — a restart finds the leftover INVALID index by name, skips creation, and proceeds. The planner ignores invalid indexes, so every batch falls back to the PK index and rescans an ever-growing completed prefix. The restart degrades toward quadratic and the invalid index keeps consuming write overhead on the hot path until dropped by hand. This breaks the header's stated constraint that a hard kill at any point must be safe to restart from.
>
> **A2 — the partial index predicate defeats HOT updates.** Severity: **CONTESTED** — one independent reader rated it major, a second rated it minor. Both agree it is real. The index predicate references `amount_minor`, the very column each backfill UPDATE writes, so HOT eligibility fails and every one of the ~341M updates must insert a new tuple into every index on a ~180 GB table. Recorded as contested rather than resolved, per this eval's position that severity disagreement between competent readers is not settled by adding another vote from the same distribution.

- **Severity**: critical
- **Location**: line 67, `to_minor_units()` (the `amount * 100`); its call site in
  `backfill()` (line 92); and `SELECT_BATCH` (line 48), which never selects
  `currency` at all.
- **The defect**: the conversion multiplies every amount by 100 regardless of
  currency. JPY and KRW are ISO 4217 zero-decimal currencies — their minor unit
  *is* the major unit (exponent 0), so ¥1500 must become `amount_minor = 1500`,
  not `150000`. Every JPY and KRW row is written 100× too large. A correct
  implementation needs the currency in the SELECT and a per-currency exponent
  (0 for JPY/KRW, 2 for USD/EUR).
- **Why it is real**: the header docstring defines the target semantic — "`amount_minor`
  is the ISO 4217 minor-unit integer the processor SDK takes verbatim" — and gives
  the schema comment "amount is in major units -- 19.99 USD, 1500 JPY", i.e. a
  whole-yen amount with no decimal part. The currency-mix line states JPY 3.4% and
  KRW 0.7% of 341.4M rows, so ~14.0M payment rows get a 100× value. Step 4 of the
  stated plan points settlement at `amount_minor` and drops `amount`, so the wrong
  values become the only remaining record and are handed to the processor verbatim.
  Nothing catches it: the script deliberately does no verification, and step 3's
  gate is a *zero-NULL* check, which these rows pass.
- **Why I expect a reviewer to miss it**: money review is a reflex checklist —
  is it `Decimal` and not `float`, is rounding explicit — and this code passes that
  checklist ostentatiously (`Decimal`, `quantize`, `ROUND_HALF_UP`), so the reviewer
  marks the conversion "carefully done" and moves on. There is no cue at the defect
  site: `currency` appears nowhere in the function, its signature, or the query, so
  the reviewer has to notice an *absence* and connect it to a one-line distribution
  statistic 50 lines earlier in the header.
- **Counts as a match if**: the reviewer says the conversion ignores `currency` and
  that zero-decimal currencies (JPY/KRW) end up 100× too large. A generic "consider
  making the conversion currency-aware" with no statement of the wrong result is a
  half-credit at best; a complaint about `Decimal`/rounding precision is not a match.

---

## Defect 2 — `SET LOCAL lock_timeout` is a no-op on an autocommit connection

- **Severity**: major (arguably critical on availability grounds; the data result
  is unaffected, which is why it is graded major)
- **Location**: line 74 in `run_blocking_ddl()` —
  `cur.execute("SET LOCAL lock_timeout = '3s'")` — interacting with
  `conn.autocommit = True` at line 107 in `main()`. The protected statement is the
  `ALTER TABLE ... ADD COLUMN` at line 110.
- **The defect**: `SET LOCAL` is scoped to the current transaction. The connection is
  in autocommit mode, so the `SET LOCAL` statement is its own implicit transaction and
  the setting is discarded the instant it returns (Postgres emits `WARNING: SET LOCAL
  can only be used in transaction blocks`). The `ALTER TABLE payments ADD COLUMN` on
  the next line therefore runs with `lock_timeout` at its default of `0`, i.e. wait
  forever. Consequently `LockNotAvailable` can never be raised and the entire
  retry/backoff loop is dead code. The fix is a plain `SET lock_timeout` (session
  scope) or setting it in the DSN `options`.
- **Why it is real**: constraint 1 in the header states the DBAs signed off *only* on
  the condition that any statement taking ACCESS EXCLUSIVE on `payments` gives up
  after 3s rather than queueing, and states the consequence: BI runs 2–4 minute
  read-only reports against the primary, and a queued ACCESS EXCLUSIVE request parks
  every checkout behind it. `ALTER TABLE ... ADD COLUMN` takes ACCESS EXCLUSIVE. So
  the one statement the whole safety mechanism exists for runs unprotected: it waits
  behind a multi-minute BI report while its own lock request blocks every checkout
  read — the checkout outage the sign-off was written to prevent.
- **Why I expect a reviewer to miss it**: `SET LOCAL` reads as the *more* careful,
  more tightly scoped form of `SET`, and it is wrapped in a named helper with
  exponential backoff and a give-up error, so the whole block signals "lock safety was
  thought about" and gets a tick rather than a check. The one fact that voids it,
  `conn.autocommit = True`, sits ~35 lines below the helper, is set for a completely
  legitimate and unrelated reason (`CREATE INDEX CONCURRENTLY` cannot run in a
  transaction block), and is annotated with a comment that reinforces autocommit as a
  *correctness feature* — so the reviewer files autocommit under "justified" and never
  brings the two facts into contact.
- **Counts as a match if**: the reviewer states the `lock_timeout` does not actually
  apply to the `ALTER` — reached either via `SET LOCAL`'s transaction scope or via the
  autocommit connection — or that the `LockNotAvailable` retry path is unreachable.
  Noting approvingly that a lock timeout is set is the failure mode, not a match.

---

## Defect 3 — `updated_at` preservation defeated by the BEFORE UPDATE trigger

- **Severity**: major
- **Location**: line 57 in `UPDATE_BATCH` —
  `SET amount_minor = ..., updated_at = p.updated_at` — and the comment at lines
  53–54 claiming this satisfies constraint 2.
- **The defect**: a BEFORE UPDATE trigger runs *after* the statement assembles the
  NEW row and can overwrite any column in it. `payments_touch_updated_at`
  unconditionally sets `NEW.updated_at = now()`, so it overrides the statement's
  `updated_at = p.updated_at` on every one of the 341.4M rows. The self-assignment is
  inert: the column is bumped exactly as if the SET list had never mentioned it. To
  actually honour the constraint the script would have to suppress the trigger for
  the backfill session (`SET session_replication_role = replica`, or
  `ALTER TABLE payments DISABLE TRIGGER payments_touch_updated_at`, itself an ACCESS
  EXCLUSIVE operation needing its own handling), or the watermark handover would have
  to be renegotiated with Data.
- **Why it is real**: the header declares the trigger verbatim ("payments has a BEFORE
  UPDATE trigger, payments_touch_updated_at, setting NEW.updated_at = now()") and
  constraint 2 states the requirement it breaks: Data pulls the warehouse copy
  incrementally with `WHERE updated_at > watermark`, a full 341M-row pull runs ~9h and
  misses the nightly window, so the backfill must not move `updated_at`. Running this
  script marks the entire table as changed, so the next incremental pull degenerates
  into exactly that ~9h full pull and blows the nightly window.
- **Why I expect a reviewer to miss it**: the code appears to have already handled the
  exact concern — the SET list explicitly names `updated_at`, and the comment directly
  above cites "constraint 2" — so the reviewer's pass over it is a *confirmation*
  ("good, they preserved it") rather than an analysis. Both halves are individually
  correct and idiomatic (a touch trigger is standard; self-assigning a column to
  preserve it is a normal idiom in triggerless tables); only the interaction is wrong,
  and the two halves are ~55 lines apart with the trigger stated as background colour
  in a schema paragraph rather than as a hazard.
- **Counts as a match if**: the reviewer states that `updated_at` still gets bumped
  because the BEFORE UPDATE trigger overrides the SET list, and/or that constraint 2 is
  therefore violated. Merely calling `updated_at = p.updated_at` a redundant self-
  assignment, without noticing the trigger defeats the intent, is not a match.

---

## Deliberate non-defects (expected false positives — do not credit)

These are intended to be correct; a reviewer flagging them has produced a false
positive, not a finding.

1. **Keyset pagination.** `id > cursor_id ... ORDER BY id LIMIT n` with
   `cursor_id = rows[-1][0]` and `cursor_id` starting at `0` is correct for a positive
   bigint identity PK; no row is skipped or reprocessed, and the loop terminates on an
   empty batch.
2. **No explicit transaction / no rollback.** Intentional and documented: each batch
   UPDATE is one statement and therefore one transaction under autocommit, which is
   what makes a hard kill safe (constraint 3). Combined with `WHERE amount_minor IS
   NULL`, restarts are idempotent.
3. **`max_id` snapshot.** Bounding the scan at `max(id)` is correct and explained:
   rows created after the snapshot belong to step 2's sweep per the stated plan.
4. **No verification step.** Explicitly out of scope per the plan in the header
   (step 3 is gated on a separate zero-NULL check job).
5. **`CREATE INDEX CONCURRENTLY` not routed through the retry helper.** Deliberate and
   explained in the comment: it takes only SHARE UPDATE EXCLUSIVE, and a blind retry
   with `IF NOT EXISTS` would silently skip a leftover INVALID index.
5b. **Building the partial index at all**, when it initially covers every row.
   Justified in the comment and by constraint 3: a restart resets the cursor to 0, and
   without the index that first query has to scan the whole already-filled id range to
   reach the next NULL row.
6. **`Decimal` arithmetic and rounding.** `(amount * 100).quantize(Decimal("1"),
   ROUND_HALF_UP)` is exact for a `numeric(12,2)` input; there is no float involved.
   The bug in this area is defect 1 (currency), not precision.
7. **`AND p.amount_minor IS NULL` in the UPDATE.** Belt-and-braces, not dead code:
   it makes a restart skip already-written rows.
8. **Progress percentage.** Reported and labelled as a percentage of the *id range*,
   not of rows; the label is accurate.
9. **No graceful SIGTERM handler.** Not needed given per-batch commits plus the
   IS NULL filter; a hard kill is safe to restart from, as the docstring states.
