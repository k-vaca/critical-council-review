# Review — doc-05-migration-plan.md

Artifact: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/doc-05-migration-plan.md`
Reviewer pass: single expert pass, judged against what a competent platform/DBA lead should produce for a 1.4 TB production cutover.

## Overall assessment

The document has the right skeleton for a cutover plan — explicit goal, window, constraints, a task table with dependencies, a run sheet, and success criteria — and the stated constraints are the right ones to have surfaced. It is let down by the fact that its own numbers do not survive arithmetic. The dependency graph contains a cycle, so the plan cannot be executed as written; the run sheet contradicts the dependency table in order to work around that cycle; and three of the plan's own stated constraints (5-minute downtime, the 03:00 finance export, the 90-minute data movement time) are each violated by the schedule that is supposed to satisfy them. The rollback section is one sentence and does not constitute a revert path.

This is a draft that needs a rework of the sequence and the verification/rollback design before it is safe to run, not a polish pass.

13 findings: 4 critical, 5 major, 4 minor.

---

## Critical

### C1 — Circular dependency between C and E makes the plan unexecutable

- **Location:** Tasks table, rows C and E (lines 19 and 21)
- **Anchor:** `| C | Cut over the checkout service to write to Postgres | E | 10 min |`
- **Problem:** C is listed as depending on E while E is listed as depending on C, so the dependency graph has a cycle and no valid execution order exists; the run sheet silently resolves it by running C first, meaning the table and the run sheet disagree about which task gates which.

Whichever direction was intended has real consequences and must be stated explicitly. If verification genuinely gates the write cutover, downtime absorbs E's 40 minutes. If the cutover comes first, then E is a post-hoc check and the rollback trigger hangs off a gate that fires after the irreversible step — see C2 and M3.

### C2 — The schedule produces roughly 15 minutes of write downtime against a 5-minute goal

- **Location:** Sequence on the night, steps 2–3 (lines 28–29); goal (line 3); success criteria (line 41)
- **Anchor:** `2. 02:15 — pause checkout writes.` / `3. 02:20 — run C.`
- **Problem:** Writes pause at 02:15, C does not start until 02:20 and is estimated at 10 minutes, so the earliest writes can resume is 02:30 — three times the 5-minute budget stated as the plan's primary goal and repeated as a success criterion.

Under the dependency table's own ordering (C after E, 40 min) the downtime is closer to 55 minutes. There is no reading of this document under which the 5-minute target is met. Either the target or the method has to change: a 5-minute write pause on a 1.4 TB cutover normally requires the write path to be switched at the application or proxy layer with replication already drained, not a 10-minute service cutover performed inside the pause.

### C3 — The 03:00 finance export runs against a MySQL database that is no longer receiving writes

- **Location:** Sequence on the night, step 5 (line 31), against constraint at line 11
- **Anchor:** `5. 03:15 — run F.`
- **Problem:** The finance export is repointed to Postgres at 03:15, but it fires at 03:00 daily, so on the cutover night it reads MySQL — which stopped receiving checkout writes at 02:15 — and produces an export missing every order written after cutover.

The constraints section explicitly states this outcome costs finance two days of manual reconciliation, so the plan breaches the one constraint it identified as most expensive. This is a scheduling error, not a design limitation: F must be moved ahead of 03:00, or the export must be suppressed and re-run after F, or the window must be shifted. The plan should also say which of those three it is doing and who confirms with finance.

### C4 — No wait for replication to catch up; the schedule allows ~30 minutes for a data movement the document itself sizes at 90

- **Location:** Sequence on the night, steps 1–2 (lines 27–28), against constraint at line 9
- **Anchor:** `1. 01:00 — run A and B.`
- **Problem:** Replication starts at 01:00 at the earliest (in practice ~01:45, since B depends on A's 45 minutes) and writes are paused at 02:15, leaving roughly 30 minutes for an initial load the constraints section says takes about 90 minutes, and no step anywhere gates the cutover on replication lag reaching zero.

Task B's 20-minute estimate plausibly covers *starting* replication, not completing the snapshot, but nothing in the plan covers the snapshot. As written, checkout is cut over to a Postgres instance holding a fraction of the 1.4 TB. A correct plan either seeds Postgres and starts replication days in advance (leaving only lag drain for the window) or budgets the full snapshot inside the window — which does not fit alongside the rest of the work in a 4-hour window. There must be an explicit "replication lag = 0, sustained for N minutes" gate immediately before the write pause.

---

## Major

### M1 — The rollback section is a paging instruction, not a rollback procedure

- **Location:** Rollback (lines 35–37)
- **Anchor:** `If checksums do not match at E, stop and page the payments lead.`
- **Problem:** It defines one trigger and one notification, but no revert path, no procedure for the writes Postgres has already accepted that MySQL does not have, no rollback trigger for failures at A, B, D or F, no point of no return, and no abort deadline relative to the 05:00 window close.

By the time E can fail, checkout has been writing to Postgres for up to 40 minutes. Reverting therefore requires reverse-replicating or replaying those writes back into MySQL, which needs to be designed and rehearsed before the night, not improvised at 03:10. The plan also needs a stated latest-abort time (e.g. "if not verified by 04:00, roll back") so the decision is not made under time pressure.

### M2 — Row-count and checksum equality is not a valid check once only one database is taking writes

- **Location:** Task E (line 21) and success criteria (line 42)
- **Anchor:** `Row counts identical across both databases at cutover.`
- **Problem:** E runs from 02:30 to 03:10 while checkout is writing to Postgres only, so Postgres legitimately diverges from MySQL during the check and row counts will differ by design, making both the verification and the corresponding success criterion unachievable as specified.

The comparison has to be pinned to a consistent point — a common LSN/GTID or a frozen cutover timestamp with the comparison bounded to rows created at or before it — and the criterion should be reworded to match ("row counts and checksums match as of the cutover watermark").

### M3 — Production reads are repointed before verification completes

- **Location:** Sequence on the night, step 4 (line 30); Tasks table row D (line 20)
- **Anchor:** `4. 02:30 — run D and E.`
- **Problem:** D moves fulfilment and support tooling onto Postgres between 02:30 and 02:45, while E — the only verification step and the only rollback trigger in the document — does not finish until 03:10, so live read traffic is committed to an unvalidated database for 25 minutes.

The dependency table reinforces this: D depends on C, not on E. Reads should be gated on verification passing, which also makes the rollback decision cheaper because fewer consumers have moved.

### M4 — Postgres sequences are never reseeded past the MySQL maximum IDs

- **Location:** Task A (line 17)
- **Anchor:** `| A | Provision the Postgres cluster and apply the schema | — | 45 min |`
- **Problem:** "Apply the schema" creates sequences at their default start value, and nothing in the plan advances them past the highest replicated `orders` id, so the first checkout writes after cutover will collide with existing primary keys.

This is the single most common failure mode in MySQL→Postgres cutovers and it fails loudly at the worst possible moment — immediately after the write pause ends, with the rollback path undefined. It needs to be an explicit step between replication drain and cutover, plus a check in E.

### M5 — The replication mechanism and the type mapping are never specified

- **Location:** Task B (line 18)
- **Anchor:** `| B | Start logical replication from MySQL into Postgres | A | 20 min |`
- **Problem:** MySQL-to-Postgres logical replication is not a native capability of either engine, so the task is not actionable without naming the tool (Debezium, DMS, pgloader-plus-CDC, etc.), and the plan contains no step for validating the MySQL-to-Postgres type, charset and collation mapping.

Whoever executes B has to make this decision themselves, and the choice materially changes the estimates in the table. The known-sharp edges for an `orders` table — unsigned integers, `ENUM`, `DATETIME` vs `timestamptz`, zero dates, `utf8mb4` collation ordering affecting any sorted output — belong in the plan or in a linked schema-mapping doc, and should be validated during a rehearsal rather than on the night.

---

## Minor

### m1 — No step resumes checkout writes

- **Location:** Sequence on the night, step 6 (line 32)
- **Anchor:** `6. 03:30 — declare the cutover complete and resume normal monitoring.`
- **Problem:** The run sheet pauses writes at 02:15 but never contains a corresponding "resume writes" step, so the end of the downtime window — the thing being measured against the 5-minute goal — is left implicit.

### m2 — Success criteria skip the finance export that is actually at risk

- **Location:** Success criteria (line 43)
- **Anchor:** `The finance export completes on Sunday 13 September without manual intervention.`
- **Problem:** The export at risk is the 03:00 UTC run on Saturday 12 September, inside the migration window; checking only Sunday's run means the plan declares success without covering the failure mode described in C3.

### m3 — No backup or retention requirement before MySQL is decommissioned

- **Location:** Task G (line 23)
- **Anchor:** `| G | Decommission the MySQL cluster | F | 30 min |`
- **Problem:** Deferring G by a week is sensible, but the plan never requires a final snapshot or states a retention period, so the last copy of the pre-migration data can be destroyed with no stated recovery option.

### m4 — Step 1 reads as parallel execution of two dependent tasks

- **Location:** Sequence on the night, step 1 (line 27)
- **Anchor:** `1. 01:00 — run A and B.`
- **Problem:** "Run A and B" at a single timestamp implies concurrency, but B depends on A in the task table, and the same phrasing in step 4 ("run D and E") genuinely is concurrent — so the notation is ambiguous exactly where it matters.

---

## What holds up

Worth stating plainly, so the findings above are read in proportion:

- The constraints section identifies the right three risks (data size, consumer fan-out, the finance export SLA) and quantifies each. Most plans at this stage omit the downstream-consumer inventory entirely.
- Separating the read consumers into two repointing tasks (D for fulfilment/support, F for finance) is a sound decision, since it lets the finance export be moved on its own schedule. Only the timing is wrong.
- Deferring decommissioning by a week rather than doing it in the window is correct.
- The dates check out: 12 September 2026 is a Saturday and 13 September is the following Sunday, so the window and the success criterion are internally consistent on that point.
- The overall arc — provision, replicate, verify, cut writes, move readers, decommission — is the right shape. The rework needed is in sequencing, gating and rollback, not in the strategy.
