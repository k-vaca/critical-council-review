# Critical Council Review — `doc-05-migration-plan.md`

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Revise substantially before use.**

The plan's task graph is circular (C waits on E, E waits on C), so there is no single executable ordering; on its own timings it misses its headline downtime goal by 3x, and it has no rollback for an irreversible cutover.

1. **Resolve the C↔E circular dependency** (Tasks table, rows C and E) — decide explicitly whether verification gates the cutover or follows it, and rewrite the Sequence to match.
2. **Replace the Rollback section** (line 37) with a real one: reverse replication or a replayable write log established *before* C, a named point of no return, and abort criteria per step.
3. **Restate or re-engineer the downtime commitment** (Goal line 3 against Sequence steps 2–4) — the current sequence pauses writes for at least 15 minutes.

## 2. Result & standard

**Under review:** `artifacts/doc-05-migration-plan.md`, 44 lines, read in full. Not my own prior output; authored by a third party and held to the third-party bar.

**Standard:** the document's own stated goal, window and success criteria, plus the competent-practitioner standard for a production database cutover runbook — a plan at minute granularity must be executable by the on-call engineer in the window without further interpretation, must be reversible until a stated point of no return, and must respect every constraint it itself declares.

**Success criteria treated as a claim, not a rule** (Step 1). The three criteria on lines 41–43 are narrower than the artifact's actual use: criterion 2 is unsatisfiable as written, and criterion 3 covers only the Sunday finance export while the at-risk run is the Saturday 03:00 one inside the window. Both verdicts are reported: against its own criteria the plan is unverifiable; against the practitioner standard it is not yet executable.

**Text addressed to the reviewer:** none present. The artifact does not attempt to set its own review scope.

**Tier:** 2 (a single deliverable). **Independence mechanism:** Step 3 sequential fallback — no subagent tooling available for this run. **Length budget:** tuned upward from the tier ceiling, which the skill's application-strength note marks as freely tunable; all non-negotiables and Steps 3–6 held as written.

**Date check (passed):** 12 September 2026 is a Saturday and 13 September a Sunday. No finding here.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Tasks table rows C and E: "Cut over the checkout service … \| E" and "Verify row counts and checksums … \| C" | Circular dependency — neither task can start, and the Sequence silently executes the opposite order to the table | Choose one ordering; if verification gates cutover, add a pre-cutover checkpoint task E′ that does not depend on C | Confirmed |
| Critical | Goal (line 3) vs Sequence 2–4: "02:15 — pause checkout writes" / "02:20 — run C" | Writes pause at 02:15 and cannot resume before 02:30 — at least 15 minutes against a 5-minute goal | Either re-engineer C to a sub-5-minute traffic switch or restate the goal at the achievable figure | Confirmed |
| Critical | Rollback (line 37): "If checksums do not match at E, stop and page the payments lead." | No rollback exists — replication is one-way, so after C there is no non-lossy path back; the sole trigger fires past the point of no return | Establish reverse replication or a replayable write log before C; define abort criteria for A, B, D, F, G | Confirmed |
| Major | Task B (line 18) vs Constraints (line 9): "1.4 TB and takes roughly 90 minutes to dump and restore" | B's 20-minute estimate covers only starting replication; no time is allocated anywhere for the initial 1.4 TB copy | State the seeding method and duration; pre-seed from a snapshot before the window if the copy exceeds the available time | Corrected |
| Major | Task E (line 21) and Success criteria (line 42): "Row counts identical across both databases at cutover." | Once Postgres takes writes and MySQL does not, counts diverge by construction — the check cannot pass and no comparison watermark is defined | Compare at a named LSN/binlog position captured at the write pause, not at wall-clock time | Confirmed |
| Major | Constraints (line 11) vs Sequence 5: "03:15 — run F" | The Saturday 03:00 export runs 15 minutes before it is repointed, against a MySQL frozen since 02:15; the plan never mentions it | State the export's coverage window; either repoint before 03:00 or suspend and re-run the Saturday export explicitly | Corrected |
| Major | Task G (line 23) and Sequence 7: "Following Saturday — run G." | Irreversible destruction of the source with no preconditions, soak criteria, final backup, or record-retention check | Gate G on a named soak period, a reconciliation sign-off, and a retained cold backup of MySQL | Confirmed |
| Major | Sequence 6: "declare the cutover complete and resume normal monitoring" | Completion rests on tasks having been run, not on fulfilment, support tooling or the finance export actually working | Add application-level smoke tests for each of the three named consumers as a precondition to declaring complete | Confirmed |
| Major | Sequence 2: "02:15 — pause checkout writes." | The plan never says what inbound checkout traffic does during the pause (rejected, queued, retried) nor the expected order volume | State the pause mechanism and the customer-facing behaviour; attach the expected order count for 01:00–05:00 UTC | Confirmed |
| Major | Header (line 5): "**Owner:** payments platform." | No named accountable individual, no go/no-go checkpoint, and no notification to the three downstream consumers named in Constraints | Name the on-call engineer and decision-maker; add a go/no-go gate before the 02:15 pause and a comms step | Confirmed |
| Minor | "## Constraints" (line 7) — absence | No data-protection controls stated for the new cluster or the replication stream for a 1.4 TB payments dataset | Reference the provisioning and encryption standard task A inherits, or add it | Unverified |
| Minor | Sequence 1: "01:00 — run A and B." | Runs B concurrently with A though the table states B depends on A — same "run X and Y" form used for genuinely parallel D and E | Write "01:00 — run A, then B" | Unverified |
| Minor | Sequence 2–3: "02:15 — pause checkout writes" / "02:20 — run C" | Unexplained 5-minute gap consumes the entire downtime budget before any cutover work begins | Close the gap or state what happens in it | Unverified |
| Minor | Task D (line 20) and Sequence 4 | Fulfilment and support read a stale MySQL from roughly 02:30 until D completes at 02:45 | Repoint reads in the same change as C, or accept and state the 15-minute stale-read window | Unverified |

Withdrawn at Step 5: 1. See Verification result.

## 4. Council roster

Three seats, **specified by the requester** — disclosed per Step 2 as a fact, not honoured as a constraint on findings.

1. **Purpose & audience fit** — does the document do the job it exists to do, for the engineer executing it at 01:00? Owns the failure mode "correct in the abstract, unusable on the night."
2. **Accuracy & internal consistency** — are the claims correct, and does the document contradict itself or its own constraints? Owns the failure mode "the plan disagrees with itself," which this artifact's dual ordering (table vs sequence) makes the dominant risk.
3. **Risk red-team** — legal, compliance, commercial and downstream exposure if this ships as written. Owns irreversibility, data handling, and the four named consumers.

**Deliberately not covered — and a critical defect could live in each:**

- **MySQL→Postgres schema and dialect fidelity.** Collation and case-sensitivity defaults, unsigned integers, zero dates, `AUTO_INCREMENT` vs sequences, and MySQL-specific SQL in the checkout and export code. **A critical defect could plausibly live here**, and no seat examined it.
- **Capacity and performance of the new cluster** under production load — connection limits, pooling, index parity. **A critical defect could plausibly live here.**

The artifact required a database-migration engineering seat that the specified roster omits. Because the roster is fixed for this run, **the verdict is capped accordingly**: this judgment does not cover schema/dialect fidelity or cluster capacity, and a defect in either would change it.

## 5. Individual analyses

### Seat 1 — Purpose & audience fit

**Role & remit.** Judges whether this document does its job for its actual reader: the on-call engineer running it at 01:00 UTC on a Saturday, and the payments lead who must decide whether to proceed or abort. Standard applied: a plan written at minute granularity has declared itself an execution document and must be actionable at that grain without interpretation.

**Assessment.** The document is well-organised and its framing sections are genuinely strong, but it does not survive contact with its own timetable. Its single most prominent commitment — the 5-minute downtime figure in the first line — is contradicted by the sequence three sections later.

**Strengths.** The Constraints section is above the standard for this document type: it names all four consumers of the table, gives a concrete data-size and duration figure, and quantifies the cost of the finance failure mode in days of downstream work. Success criteria are numeric and dated rather than aspirational. Deferring G by a week rather than doing it on the night is a sound instinct. The schedule also leaves roughly 90 minutes of unused slack inside the stated window — real headroom for the contingency the plan otherwise lacks.

**Weaknesses, risks & errors.** **Critical, defect** — the plan cannot meet its headline goal. Anchor: "**Goal:** cut over the orders service to Postgres with no more than 5 minutes of write downtime" (line 3) against "2. 02:15 — pause checkout writes" and "3. 02:20 — run C" (Sequence), with C estimated at 10 minutes: writes cannot resume before 02:30, giving at least 15 minutes. Even the most favourable reading — writes resuming the instant C's switch flips — still spends the full 5-minute budget on the unexplained 02:15→02:20 gap alone. **Major, defect** — completion is declared without evidence. Anchor: "6. 03:30 — declare the cutover complete and resume normal monitoring" (Sequence); nothing in the plan validates that fulfilment, support tooling or the finance export actually function after being repointed. **Major, defect** — no human is accountable at the grain the plan operates at. Anchor: "**Owner:** payments platform." (line 5); a team is not a decision-maker at 02:15, there is no go/no-go gate before the irreversible pause, and none of the three consumers named in Constraints is notified anywhere in the sequence.

**Gaps.** No contingency branch for any task overrunning, despite 90 minutes of slack available to spend. No definition of the pause mechanism. No statement of who may call an abort.

**Strongest reason this might be fundamentally wrong.** The plan may be organised around the wrong objective. It optimises visibly for a 5-minute write-downtime target that its own sequence cannot deliver, while the binding constraint the document itself identifies — the 03:00 finance export whose failure costs two days — never appears in the timetable at all. If the export is the real constraint, the entire sequence is shaped around the wrong number and tightening the cutover would not help.

**Domain verdict.** Below the bar as an execution document; adequate as a design sketch. A competent engineer handed this at 01:00 would have to stop and ask which ordering to follow before starting.

**Recommended fixes.** Name the on-call engineer and the abort decision-maker. Add a go/no-go gate immediately before the 02:15 pause. Add smoke tests for fulfilment, support and finance as preconditions to step 6. Reconcile the goal line with the sequence.

### Seat 2 — Accuracy & internal consistency

**Role & remit.** Judges whether the document's claims are correct and whether it contradicts itself or the constraints it declares. Standard applied: a plan containing a dependency table and a timetable must have the two agree, and every stated constraint must be discharged somewhere in the plan.

**Assessment.** The document contains two mutually exclusive orderings and never says which is authoritative. This is not a typo — the two orderings describe different migrations with different risk profiles, so there is no single artifact here to check.

**Strengths.** The task estimates, taken individually, sum to fit the window: 01:00 + A(45) + B(20) reaches 02:05 before the 02:15 pause, and the night's work finishes at 03:30 against a 05:00 close. The arithmetic of the timetable, considered on its own terms, is internally consistent.

**Weaknesses, risks & errors.** **Critical, defect** — circular dependency. Anchors: "| C | Cut over the checkout service to write to Postgres | E | 10 min |" (line 19) and "| E | Verify row counts and checksums match between the two databases | C | 40 min |" (line 21). Neither task can start. The Sequence resolves this silently by running C at 02:20 and E at 02:30, i.e. the opposite of what the table states — so a reader following the table and a reader following the sequence execute different plans, one verifying before an irreversible step and one after. **Major, defect** — task E cannot pass as specified. Anchors: "Row counts identical across both databases at cutover" (line 42) and E's 02:30–03:10 slot; during that window Postgres receives new writes and MySQL receives none, so the counts diverge by construction. No comparison watermark or freeze point is defined. **Major, defect** — no time is allocated for the initial data copy. Anchors: "| B | Start logical replication from MySQL into Postgres | A | 20 min |" (line 18) against "The orders table is 1.4 TB and takes roughly 90 minutes to dump and restore at current sizes" (line 9); B's estimate covers starting replication, and the document offers no figure at all for seeding 1.4 TB into an empty target. **Major, defect** — a declared constraint is never discharged. Anchors: "The finance export runs at 03:00 UTC daily and must not be skipped" (line 11) and "5. 03:15 — run F" (Sequence); the Saturday 03:00 run falls inside the stated window and appears nowhere in the timetable. **Minor** — "1. 01:00 — run A and B" (Sequence) runs B concurrently with A despite B's stated dependency; the document uses the same "run X and Y" form for D and E, which genuinely are parallel. **Minor** — the 02:15→02:20 gap is unexplained and unbudgeted.

*Overlap noted, not restated:* the downtime arithmetic is owned by the Purpose seat.

**Gaps.** No statement of which of the two orderings is authoritative. No seeding estimate. No definition of "checksums" — what is being checksummed, at what granularity, and against what tolerance.

**Strongest reason this might be fundamentally wrong.** The table and the sequence are not two views of one plan; they are two plans. Verify-then-cut and cut-then-verify differ in whether the team ever gets a safe abort. Because the document never states which it means, there is no coherent artifact to check for correctness — every downstream finding is conditional on a choice the author has not made.

**Domain verdict.** Fails on internal consistency. Three of the document's five sections contradict at least one other section.

**Recommended fixes.** Declare one authoritative ordering and regenerate the other view from it. Add a seeding task with its own estimate. Define the checksum comparison against a captured replication position. Add the Saturday 03:00 export to the timetable as a named step.

### Seat 3 — Risk red-team

**Role & remit.** Finds where this breaks and who pays: legal, compliance, commercial, and the four downstream consumers. Standard applied: an irreversible change to a payments-adjacent system must have a stated point of no return, a rollback that works up to it, and a named owner for each downstream consequence.

**Assessment.** Every safety control in this document sits on the wrong side of the point of no return. The plan reads as though it is reversible until E, but it is irreversible from the moment C completes.

**Strengths.** Quantifying the finance failure at two days of manual reconciliation is genuinely useful risk work — it converts a vague dependency into a costed one, which is what makes the missing mitigation visible at all.

**Weaknesses, risks & errors.** **Critical, defect** — there is no rollback. Anchor: "If checksums do not match at E, stop and page the payments lead" (line 37). This is an escalation, not a rollback. Replication runs MySQL→Postgres only (task B), so from the moment checkout writes to Postgres, those orders have no path back; the single defined trigger fires at a point where returning to MySQL means losing accepted orders. No abort criteria exist for A, B, D, F or G at all. **Major, defect** — irreversible destruction with no gate. Anchors: "| G | Decommission the MySQL cluster | F | 30 min |" (line 23) and "7. Following Saturday — run G" (Sequence). No soak criteria, no reconciliation sign-off, no final backup, and no reference to retention obligations for order and financial records — which for a payments platform are typically multi-year `[unverified — recall, not lookup]`. Once G runs, both the fallback and the historical source are gone. **Major, defect** — the customer-facing cost of the pause is unstated and unhandled. Anchor: "2. 02:15 — pause checkout writes" (Sequence). The document never says whether inbound checkouts are rejected, queued or retried, and never states expected order volume; 01:00–05:00 UTC is also business hours across Asia-Pacific, an assumption of quietness the document does not make explicit. **Minor** — no data-protection controls are stated. Anchor: absence in "## Constraints" (line 7), which lists three operational constraints and none on data handling; no encryption, access-control, residency or review reference for a 1.4 TB order dataset, and the document does not state whether `orders` carries cardholder data, which would change the migration's compliance scope. **Minor** — fulfilment and support read a stale MySQL from roughly 02:30 until D completes at 02:45.

**Gaps.** No point of no return named. No customer or SLA notification. No statement of what an incomplete finance export costs commercially beyond the two finance-days already quantified.

**Strongest reason this might be fundamentally wrong.** The plan's entire risk posture treats the checksum gate as a safety net, when it is positioned after the only irreversible step. If that is the intended design rather than an ordering slip, the team believes it has a rollback it does not have — and will discover this at 02:30 on a Saturday with checkout already writing to a database that may be incomplete.

**Domain verdict.** Reject and rework in my domain. An irreversible change to the order-of-record for a payments platform, with no rollback and an ungated decommission, should not enter a change window in this state.

**Recommended fixes.** Establish reverse replication or a replayable write log before C. Name the point of no return explicitly in the document. Gate G on a soak period, a reconciliation sign-off, and a retained cold backup. State the pause behaviour and the expected order volume for the window.

## 6. Executive review

The executive re-read the artifact in full before synthesis.

**Points of agreement.** The seats converge on three readings: the C/E ordering is broken; the checksum gate is mis-positioned relative to irreversibility; and the plan's stated success criteria do not measure what actually has to go right. **Under the Step 3 sequential fallback this convergence is not evidence.** All three points are marked **sole-source**, and each was upheld only on its own anchor, re-checked directly against the text.

**Deduplicated.** The downtime miss was reached by both the Purpose seat (as a goal failure) and the Accuracy seat (as timeline arithmetic). Stated once, at critical, in the findings table; the Accuracy seat notes the overlap without restating it.

**Points of conflict & adjudication.**

- *Risk seat says reject and rework; Purpose and Accuracy imply revise.* **Adjudicated: revise substantially.** The evidence for downgrading is specific — the approach the document chooses (logical replication, brief write pause, cut over, verify, repoint consumers, decommission after a soak) is the standard and correct approach for this migration, and the Constraints section, task inventory and window are all reusable. What is broken is the specification of that approach, not the approach. Reject-and-rework would discard sound material. The Risk seat's domain verdict stands *within its domain* and is the reason the decision is not "approve with revisions."
- *Risk seat rated the data-protection silence major.* **Downgraded to minor.** Named evidence: task A is "Provision the Postgres cluster and apply the schema" — provisioning at a payments platform will inherit an existing standard, so the document's silence is most likely a documentation gap rather than a control gap. This reverts to major if this document *is* the change-approval record, which cannot be determined from the text.
- *Accuracy seat rated the finance-export omission at critical.* **Downgraded to major at Step 5** — see below.

**Verification result.** Every critical and major finding was re-checked by searching the artifact for its quoted string. **1 withdrawn, 2 corrected.**

- **Withdrawn (Accuracy seat):** "E's 40-minute estimate is unsupported, since the document's own figure for a full pass over 1.4 TB is 90 minutes." This transferred the 90-minute figure from "dump and restore" (line 9) to a checksum scan, which is a different operation — two full data movements versus one partitionable read. The document gives no checksum figure at all. The finding rested on reading a passage outside the context that governs it. Dropped.
- **Corrected (finance export, critical→major):** searched "The finance export runs at 03:00 UTC daily and must not be skipped" (found, line 11) and "03:15 — run F" (found, line 31). The adversarial question — what would make this false? — has an answer: if the export covers the prior calendar day rather than a trailing window to run time, the Saturday 03:00 run against a MySQL frozen at 02:15 is complete and unaffected. The document never states the coverage window. Restated as narrowly as the evidence supports: the plan cannot be shown to be safe here, and it omits a constraint it declared binding, but incompleteness is not established.
- **Corrected (replication seeding):** searched "Start logical replication from MySQL into Postgres" (found, line 18) and "1.4 TB and takes roughly 90 minutes to dump and restore" (found, line 9). Narrowed: the defect is that no seeding time is allocated or estimated anywhere, not that 90 minutes is the correct figure — logical-replication seeding is a closer analogue to dump-and-restore than a checksum scan is, but it is still not the same operation. Held at major on the omission.
- **Confirmed with strings located:** C/E circularity (lines 19, 21); "no more than 5 minutes of write downtime" (line 3) with "02:15 — pause checkout writes" (line 28); "If checksums do not match at E, stop and page the payments lead" (line 37); "Row counts identical across both databases at cutover" (line 42); "Decommission the MySQL cluster" (line 23) with "Following Saturday — run G" (line 33); "declare the cutover complete" (line 32); "**Owner:** payments platform." (line 5).
- **Seat reliability:** the Accuracy seat produced the withdrawn finding and one of the two corrections. Both errors are the same error — over-extending a single numeric constraint the document states once. Its purely structural findings (the circularity, the table/sequence conflict) required no such inference and are unaffected.

**Panel blind spots.** The strongest case the council is wrong: all three seats assumed the **Sequence** is the authoritative ordering. If the **Tasks table** is authoritative instead, the downtime finding gets substantially worse rather than better — verification would have to complete before C, pushing the write pause past 40 minutes — but several process findings would soften, since a verify-first plan does have a genuine abort point. No seat tested that branch.

Per the sequential caveat, coverage is suspect as well as agreement. In a single context these three seats are one reader wearing three hats; the discipline constrains write order, not what the reader thought to look for. Two domains no seat examined, in both of which a **critical defect could plausibly live**: (1) MySQL→Postgres schema and dialect fidelity — collation and case-sensitivity defaults, unsigned integers, zero dates, `AUTO_INCREMENT` versus sequences, and MySQL-specific SQL in checkout and the export; (2) capacity and performance of the new cluster under production load. The requester-specified roster omitted the database-engineering seat the artifact required, and the verdict is capped accordingly.

Load-bearing claims that should be verified externally before acting: the 90-minute dump-and-restore figure (line 9), the 40-minute checksum estimate (task E), and the finance export's coverage window — none can be checked from the document alone.

**Overall judgment.** A well-framed plan with a broken core. The framing sections do real work — the Constraints section is better than most migration plans produce, and the window has genuine slack. But the executable content contradicts itself in three places, misses its headline commitment by 3x on its own numbers, and provides no way back from an irreversible change to the order-of-record for a payments platform. Against its own success criteria the plan is unverifiable, because criterion 2 cannot be satisfied as written. Against the competent-practitioner standard it is not yet safe to run.

**Decision on further action.** Revise substantially before use.

**Prioritized next steps.**
1. Choose one authoritative ordering and resolve C↔E; regenerate the timetable from the dependency graph rather than maintaining both by hand.
2. Design a real rollback: reverse replication or a replayable write log established before C, a named point of no return, and abort criteria per task.
3. Fix the verification gate — compare at a replication position captured at the write pause, not at wall-clock time, and drop or restate success criterion 2.
4. Add the Saturday 03:00 finance export to the timetable as a named step, after stating its coverage window.
5. Reconcile the downtime goal with the sequence: either re-engineer C to a sub-5-minute switch or restate the target honestly.
6. Add a seeding task and estimate; gate G on a soak period, sign-off and retained backup; name the on-call engineer and the go/no-go point.
7. Commission the database-engineering review this roster could not provide, covering schema and dialect fidelity and cluster capacity.

**Confidence & what would change the verdict.** Of the 10 findings reported at critical or major, I expect **8 to survive** an independent expert re-check. The two I expect to fall first: the **finance-export omission**, which depends entirely on the export's coverage window — a reviewer with access to the export definition could show the Saturday run is unaffected, reducing it to a documentation gap; and the **replication-seeding** finding, which collapses to "the plan doesn't say so" if the team intends to pre-seed from a snapshot taken before the window. The three criticals rest on **verified evidence**, not inference: each is a contradiction internal to the text, checkable by any reader without outside knowledge, which is why I expect all three to survive. The process findings (no named owner, no completion validation, no stated pause behaviour) rest on the **inference** that this document is the execution artifact rather than a summary of one.

What would flip the verdict: the existence of a companion runbook that resolves the C/E ordering, defines rollback, and schedules the Saturday export. If one exists, this document is a summary and the decision moves to *approve with minor revisions* — the summary would still need its goal line and success criteria corrected. Absent that, the decision stands.
