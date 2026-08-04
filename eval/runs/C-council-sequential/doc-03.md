# Critical Council Review — `search-indexer` lag alert runbook

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Revise substantially before use.** The branching, escalation and false-positive sections are competent, but the most-travelled branch tells the on-call a persistent degradation is healthy, and two of the four steps cannot be executed as written.

1. **Step 1, "Falling or flat"** — split flat from falling; flat lag above 50,000 is not "keeping up", and the branch must end in an escalation, not an open-ended re-check.
2. **Step 2** — two `curl` reads 60 seconds apart, matching Step 1's own discipline; `rejected` is cumulative, so one snapshot cannot show growth.
3. **Step 4** — record the cutover timestamp, state where `bin/reindex` runs, and confirm the backfill completed.

## 2. Result & standard

Judged: the whole runbook (63 lines, read in full). Not my own prior output. Standard: an on-call runbook must let a reader matching its stated audience — "no prior knowledge of the indexer assumed" (line 4) — reach a resolved or escalated state unaided, every branch terminating. My stated judgment, plus the document's own audience line. Tier 2, sequential seats; at 471 words the artifact sits on the tier 1/2 boundary and I held the tier declared at Step 1. No text is addressed to the reviewer; "Applies to … only" and "Last validated" are claims assessed, not scope obeyed.

*Declared deviation:* this review runs ~2,550 words against tier 2's 1,800. The skill designates the length budget tunable; I kept nine anchored findings and the full eight-field seat analyses rather than cut evidence to hit the number. Sections 1 and 3 alone are sufficient to act on.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Step 1 — "the indexer is keeping up or catching up" | Flat lag is degradation, not health; branch never exits | Split flat from falling; escalate after two re-checks | Confirmed |
| Major | Step 2 — "non-zero and growing `rejected` count" | One snapshot cannot show growth in a cumulative counter | Two reads 60s apart; define "growing" numerically | Confirmed |
| Major | Step 3 — "the bottleneck is downstream" | Asserts what Step 2's test was used to rule out | State what Step 2 does and does not exclude | Corrected |
| Major | Step 3 — "autoscaler will return replicas to baseline within the hour" | Fix self-reverts, possibly before the backlog drains | Pin replicas until lag is under threshold | Confirmed |
| Major | Step 4 — "`bin/reindex --since <timestamp>`" | Timestamp source and execution host unspecified | Record cutover time; give the full command | Corrected |
| Major | Step 4 — "roughly 60% … about 4% of search queries" | Unsourced figures justify the only user-impacting action | Link the dashboard; date the figures | Unverified |
| Major | Line 9 — "for as long as the lag implies" | No throughput figure; staleness and drain time uncomputable | State messages/sec so lag converts to minutes | Confirmed |
| Minor | Step 3 — `scale … --replicas=24` | Current replica count unchecked; step may be a no-op | Read replicas first; skip if already 24 | Confirmed |
| Minor | Step 4 — `set env …` | Env change restarts pods mid-incident, unwarned | Warn that lag spikes during the rollout | Unverified |

## 4. Council roster

Roster specified by the requester and used verbatim — disclosed as a fact, not honoured as a constraint. Seats: **purpose & audience fit**, **accuracy & internal consistency**, **risk red-team** (the required skeptic, also carrying the downstream-recipient view). Not covered: **Kafka/OpenSearch engineering** — a critical defect could live there (are 24 partitions, 50,000, and the write thread-pool the right instruments?); **alerting configuration** — likewise, since the document is keyed to `SearchIndexerLagHigh` firing exactly as described. The verdict is capped and covers neither.

## 5. Individual analyses

### Seat 1 — Purpose & audience fit

**Role & remit.** Whether a platform on-call with no indexer knowledge can run this end to end and finish in a defined state.

**Assessment.** Structurally sound — it branches on evidence and names its limits. But it is written for the rare case. Lag parked above threshold is the common case, the first branch the reader meets, and the one handled wrongly.

**Strengths.** "Known false positive" (line 60) marks a runbook maintained by people this alert has woken. "Run it twice, 60 seconds apart" (line 21) makes the decision rule reproducible.

**Weaknesses, risks & errors.**
- **Critical, defect** — "the indexer is keeping up or catching up … Re-check in 30 minutes." (Step 1). Flat lag above 50,000 means matching input while never draining; users stay stale indefinitely. Line 11 says as much: "Steady lag above the threshold degrades freshness". The reader is told the opposite, then given a re-check with no terminating condition and no escalation.
- **Major, defect** — "for as long as the lag implies" (line 9). Lag is in messages and no throughput figure appears anywhere, so the stated audience cannot convert 50,000 into a staleness window, size impact, or estimate drain time.
- **Major, defect** — Step 4 sheds load with no documented restore path.
- **Minor, defect** — Step 3 scales without reading current replicas, so it can be a silent no-op costing ten minutes.

**Gaps.** No definition of "resolved", so no branch knows when it has finished.

**Strongest reason this might be fundamentally wrong.** If most firings are steady lag, the defective branch is also the most-travelled, and the document's net effect is to close real degradations as healthy.

**Domain verdict.** Below the bar. A competent runbook does not misreport system state to its stated audience.

**Recommended fixes.** Separate flat from falling with an explicit escalation; publish throughput beside the threshold; define the resolved state.

### Seat 2 — Accuracy & internal consistency

**Role & remit.** Whether the claims hold on their own terms, and whether the document contradicts itself or its stated constraints.

**Assessment.** The commands are individually sound. The defects sit in the inferences between them: twice the document draws a conclusion its own prior step does not support, and once it describes a behaviour that undoes the action it just prescribed.

**Strengths.** Step 1's two-reading protocol is correct for a rate question. The 2-minute false-positive window (line 62) matches the mechanism it describes. The escalation payload requests nothing the earlier steps have not already produced.

**Weaknesses, risks & errors.**
- **Critical, defect** — "If lag does not fall with 24 replicas, the bottleneck is downstream." (line 44) contradicts Step 2, whose negative result is the only reason the reader reached Step 3. The document rules the downstream bottleneck out, then asserts it, and routes to its user-impacting action on that basis.
- **Major, defect** — "A non-zero and growing `rejected` count" (line 32). The supplied `curl` returns one snapshot; `rejected` is cumulative [unverified — recall, not lookup], so non-zero is unremarkable and "growing" is unobservable from a single read. Step 1 solves this exact problem correctly; Step 2 does not.
- **Major, defect** — "the deployment autoscaler will return replicas to baseline within the hour" plus "If lag begins falling, stop here" (both line 42). The reader stands down as the trend turns while the remediation expires on a timer, with nothing requiring the backlog to have drained.

**Gaps.** No provenance for the constants (50,000; 10 minutes; 24), so staleness in any is undetectable.

**Strongest reason this might be fundamentally wrong.** No foundational failure found. The strongest candidate is the Step 2 → 3 → 4 chain, major rather than fundamental because each command and observation is correct; the defect is two sentences of inference, fixable without changing the procedure.

**Domain verdict.** Materially below the bar on internal consistency; sound at command level.

**Recommended fixes.** Make Step 2 a two-read comparison; rewrite Step 3's closing inference; require lag under threshold before standing down.

### Seat 3 — Risk red-team

**Role & remit.** Where this breaks legally, commercially or downstream if it ships, plus the view of whoever depends on the index afterwards.

**Assessment.** No legal or regulatory exposure is identifiable from the document itself, and I will not manufacture one. The real exposure is quiet: the only mitigation trades a measured harm for an unmeasured one and never closes the loop.

**Strengths.** Step 4 is gated on an incident commander (line 48) and names its tradeoff rather than hiding it.

**Weaknesses, risks & errors.**
- **Major, defect** — "roughly 60% of index write volume and about 4% of search queries" (line 54). These numbers are the entire justification for accepting user-facing harm, with no source and no date; "Last validated … by running steps 1 to 4" (line 5) covers step execution, not statistics. An incident commander approves real impact on figures they cannot check.
- **Major, defect** — "Backfill by removing the variable and running `bin/reindex --since <timestamp>`." (line 54). Nothing instructs recording when the variable was set, and nothing says where the binary runs — the only command without a `kubectl` context. A late timestamp leaves a permanent silent index gap; an early one triggers a full reindex. Overlaps Seat 1's Step 4 finding.
- **Major, risk** — Step 4 has no completion check: nothing verifies the backfill ran, and no owner is named.
- **Major, defect** — routing from Step 2 to Step 4 bypasses the incident-commander gate.
- **Major, gap** — no time bound on Step 4 before further escalation.
- **Minor, risk** — `set env deploy/search-indexer` (line 51) triggers a rolling restart [unverified — recall, not lookup], cutting consumer capacity at the worst moment, unwarned.

**Gaps.** If the corpus carries retention or discoverability obligations — the document does not say — an undetected index gap is a compliance problem, not only a quality one. Conditional, because the document supplies no facts either way.

**Strongest reason this might be fundamentally wrong.** The runbook may institutionalise silent data gaps: its terminal mitigation opens a hole in the index and delegates repair to a command whose critical argument is undefined and whose completion nobody owns.

**Domain verdict.** Below the bar on downstream risk; load-shedding is the least finished step and the only one with lasting consequences.

**Recommended fixes.** Source and date the percentages; make timestamp capture a numbered action; add a backfill-verification step with a named owner.

## 6. Step 5 — Verification pass

Every critical and major finding was re-checked by searching the artifact for its quoted string, adversarially rather than supportively.

**Confirmed.** "the indexer is keeping up or catching up" (line 23) against "Steady lag above the threshold degrades freshness" (line 11); "A non-zero and growing `rejected` count" (line 32) against the single-read `curl` (line 29); "the deployment autoscaler will return replicas to baseline within the hour" and "If lag begins falling, stop here" (both line 42); "for as long as the lag implies" (line 9) — searched end to end for any throughput figure, none exists; "roughly 60% of index write volume and about 4% of search queries" (line 54), uncited.

**Corrected (2).** Seat 2's Step 3 finding was raised as critical on the ground that line 44 *contradicts* Step 2. Narrowed to major: Step 2 tests write-thread-pool rejections only, and OpenSearch can be slow without rejecting, so "downstream" is not strictly excluded — the defect is a leap resting on a test too narrow to bear it. Seat 1's "no documented restore path" is false as stated; line 54 documents one. Restated: the path exists, but its `--since` argument has no defined source and its execution context is unstated.

**Withdrawn (2), both Seat 3.** "Routing from Step 2 to Step 4 bypasses the incident-commander gate" — line 48 gates Step 4 unconditionally, however it is reached. "No time bound on Step 4 before escalation" — line 58 states "If lag is still rising 20 minutes after step 4, page the search team lead."

## 7. Executive review

The artifact was re-read in full before this synthesis.

**Points of agreement.** Seats 1 and 3 both reached the Step 4 backfill gap. Under the sequential fallback it is marked **sole-source** and carries no added severity weight — Seat 3 could see Seat 1's section, so the repetition measures nothing. Stated once, cut from both seats' counts.

**Points of conflict & adjudication.** Seat 2 rated the Step 3 inference critical; Seat 1 never examined it, and silence is not disagreement. Downgraded to major on specific evidence: Step 2 covers write-thread-pool rejections only, so a slow-but-not-rejecting OpenSearch stays consistent with both steps. Seat 1 rated the Step 1 flat branch critical; upheld — it owns audience comprehension, no seat produced contrary evidence, and I checked the anchor myself: line 23 asserts health and line 11 asserts degradation about the same state.

**Verification result.** Two withdrawn, two corrected. Both withdrawals were Seat 3's, and both were failures to read to the end — the incident-commander gate and the escalation timer are present and explicit. Its surviving findings were re-anchored individually and hold, but its reading discipline is in question.

**Panel blind spots.** All three seats assumed the document describes the real system: that the alert fires as stated, that partitions are 24, that the autoscaler behaves as line 42 claims. None was verified. Under the sequential fallback, coverage is as suspect as agreement — one shared context means shared omissions. The clearest: **no seat examined the alert definition.** A critical defect could live there; if `SearchIndexerLagHigh` fires on a different threshold or window, the document is keyed to the wrong trigger and every finding here becomes secondary.

**Overall judgment.** A well-shaped runbook by someone this alert has paged — the branching, escalation payload and false-positive section are better than average. It is let down by its inferences, not its structure: one branch misreports system state, one decision rule cannot be evaluated with the command given, and the terminal mitigation is unfinished at both ends. All fixable inside the existing skeleton; none of it should meet production first.

**Decision on further action.** **Revise substantially before use.**

**Prioritized next steps.** (1) Fix the Step 1 flat-lag branch. (2) Make Step 2 a two-read comparison with a numeric threshold. (3) Finish Step 4: timestamp capture, full `bin/reindex` invocation, completion check. (4) Publish throughput beside the alert threshold. (5) Source and date the 60% / 4% figures. (6) Reconcile Step 3's inference with what Step 2 excludes. (7) Re-validate covering the escalation path and false-positive check, which the 2026-07-02 run did not exercise.

**Confidence & what would change the verdict.** Of the 7 findings at critical or major, I expect 5 to survive an independent re-check. First to fall: the autoscaler finding, which evaporates if baseline replicas already sit at 24 or the autoscaler only scales up; then the 60% / 4% finding, which narrows to minor if those numbers sit on a dashboard the on-call already holds. The Step 1 critical is most robust — it rests on two sentences of the document contradicting each other, both quoted. The verdict rests on verified evidence for the documentary defects and on assumption for everything about the underlying systems. It flips to *approve with minor revisions* if the flat-lag exit is defined in a separate policy document the on-call reliably holds and the Step 4 timestamp convention is established team practice. It does not cover Kafka/OpenSearch engineering or the alert definition; a defect in either would change it.
