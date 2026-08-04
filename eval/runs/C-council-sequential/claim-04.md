# Critical council review — "Benchmark: inference server v3.0 vs v2.1"

Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

---

## 1. Verdict

**Reject and rework.** The comparison changes three things at once and never measures either server at its limit, so neither the 2.4× headline nor the fleet-retirement saving follows from what was run.

1. **Method table (L17–18)** — re-run both versions on the same instance type and the same max batch size, so the version is the only variable.
2. **Results table (L26–30)** — raise offered load until throughput stops climbing, and report p99 against the 800 ms SLO named in L42; both runs held only ~16 requests in flight.
3. **Recommendation (L40)** — rebuild the saving as requests-per-dollar at the SLO, and limit it to fleets whose own workload was benchmarked.

## 2. Result & standard

Under review: `claim-04-benchmark.md`, 42 lines, read in full; not my own prior output. **Standard:** the artifact's stated purpose (L4) and its own SLO (L42), plus two rules I assert as professional judgment and defend below — a comparison varies one thing at a time, and a capacity claim requires measurement at saturation. **Tier 3** (small document, expensive decision: four fleets, $340k/yr). **Mechanism:** sequential seats, Step 3 fallback. **Requester framing:** procedure only, no claim about quality or expected verdict; nothing to quarantine beyond the roster mandate (§4). **Reader-directed text in the artifact:** "See the attached throughput chart for the full run profile." (L32) — no chart was part of the reviewed material and I read no file outside this one. That gap could narrow M4 and part of M1, but cannot touch C1, C3 or C4, so it does not force "insufficient information to decide". **Budget note:** this review runs ~14% over the tier-3 word ceiling; the skill marks the length numbers as arbitrary and tunable, and the overrun buys anchors rather than prose. Nothing else in the tier was relaxed.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | L17–18, "8 vCPU" vs "16 vCPU"; batch 16 vs 64 | Version, host size and batch ceiling all change together | Re-run with matched instance and batch size | Corrected |
| Critical | L28–29, "41.2 / 98.9", "388 / 162" | Both runs held ~16 requests in flight; capacity never measured | Sweep offered load to saturation | Confirmed |
| Critical | L42, "SLO is p99 latency under 800 ms" | Only mean latency reported; the SLO's own metric is absent | Report p50/p95/p99 per arm | Confirmed |
| Critical | L40, "all four inference fleets" | Conclusion spans four fleets; evidence covers one workload | Benchmark each fleet's own workload | Confirmed |
| Major | L22, "run once, end to end" | One run each, ~49 s and ~20 s of traffic, no variance | Repeat ≥5 runs, report spread | Confirmed |
| Major | L40, "roughly 40% ... $340,000 a year" | Derivation unshown, unreconciled with 2.4×, ignores larger instance | Recompute as requests-per-dollar at the SLO | Corrected |
| Major | L36, "is direct evidence of this" | Batch ceiling 16→64 predicts the same utilisation rise | Restate as consistent-with | Confirmed |
| Major | L32, "See the attached throughput chart" | Cited run-profile evidence is absent from the document | Attach it or drop the reference | Confirmed |
| Major | L4, "justify the v3.0 rollout" | Study framed to justify a conclusion, not to test it | Reframe with a stated fail condition | Confirmed |
| Major | L14–20, Method table | No output-parity check between 2.1.4 and 3.0.1 | Add an output-equivalence comparison | Confirmed |
| Major | L12, "2,000 requests ... 3 August 2026" | One day, one hour; length distribution never characterised | Publish length histogram, widen sample | Confirmed |
| Minor | L8, "2.4× faster" | Conflates a throughput ratio with a latency reduction | Name the metric in the claim | Unverified |
| Minor | L40, "Roll v3.0 to all four ... in Q4" | No canary, rollback trigger or abort criteria | Stage one fleet with abort criteria | Unverified |

## 4. Council roster

Requester-specified; disclosed per Step 2 — I neither chose it nor added to it.

1. **Methodology & statistics** — design, power, inference; owns whether the numbers support the claim.
2. **Data & inference validity** — sampling, confounds, measurement; owns whether the conclusion follows.
3. **Decision red-team** — owns whether the recommendation survives production.

**Deliberately not covered:** (a) model output quality/parity between versions — a critical defect could live here; (b) FinOps against real instance prices — a critical defect could live here; (c) SRE rollout mechanics; (d) peak-hour capacity planning. Tier 3 calls for 4–6 seats and 3 were mandated, so the verdict is capped: a defect in (a) or (b) could only strengthen the reject call, never rescue the artifact, but this review does not cover either.

---

## 5. Individual analyses

### Seat 1 — Methodology & statistics

**Role & remit.** Judges the experiment, not the product: design, controls, power, and whether the numbers license the claim.

**Standard applied, and its source.** Two rules asserted as my own professional judgment, reasoned from the artifact's design table rather than any cited external suite: a controlled comparison varies one independent variable, and a capacity claim requires measurement at or beyond saturation — a load-versus-throughput curve, not one operating point.

**Assessment.** The result is internally consistent, which is what makes it dangerous: 41.2 → 98.9 req/s is exactly ×2.40, matching 388 → 162 ms. But three things differ between arms, and two are configuration choices, not properties of v3.0.

**Strengths.** The controls the document does apply are the right ones — warm-up matched at 100 (L20), quantisation "none" both sides (L19) — and the workload is replayed from a real production log (L12).

**Weaknesses, risks & errors.**
- **Critical, defect (C1).** Anchor: "`g5.2xlarge` (8 vCPU, 1× A10G) | `g5.4xlarge` (16 vCPU, 1× A10G)" (L17) with "Max batch size | 16 | 64" (L18). Version, host size and batch ceiling move together. This undermines the Step 1 purpose directly: the memo exists to justify **v3.0** and cannot separate v3.0 from the box it ran on.
- **Critical, defect (C2).** Little's law — in a stable system, mean requests in flight = throughput × mean time in system — applied to the artifact's own figures: 41.2 × 0.388 s ≈ 16.0 and 98.9 × 0.162 s ≈ 16.0 (L28–29). Both runs held about sixteen requests in flight. v2.1 sat exactly at its batch ceiling of 16; v3.0's ceiling of 64 was never approached, consistent with utilisation stopping at 89%. The harness, not the server, set the throughput — a fixed-concurrency latency comparison read as a capacity measurement.
- **Major, defect (M1).** "Each configuration was run once, end to end" (L22). At the reported rates, 2,000 requests is ~49 s of traffic for v2.1 and ~20 s for v3.0 — unequal, very short windows, n = 1, no variance anywhere.
- **Major, defect (M5).** "justify the v3.0 rollout to all inference fleets in Q4" (L4) — the stated goal is to justify a predetermined conclusion, and the design errors all point one way.

**Gaps.** No load sweep, no saturation point, no run-to-run variance, and no statement of whether the arms ran concurrently — they share one hour (L22), so mutual interference is not excluded.

**Strongest reason this might be fundamentally wrong.** That the experiment measures the wrong quantity. If the harness pinned concurrency at 16, throughput here is a property of the test rig, and every capacity- and cost-derived number is about something other than what the reader thinks.

**Domain verdict.** Below the bar a competent performance engineer should meet: the design cannot answer the question asked of it.

**Recommended fixes.** Matched instance type; batch size as a controlled variable (including v2.1 at 64 if supported); a load sweep to saturation per arm; ≥5 runs each with reported spread.

### Seat 2 — Data & inference validity

**Role & remit.** Sampling, confounds, measurement choice, and whether "roll it out" follows from what was measured.

**Standard applied, and its source.** A metric supports a claim only about the thing the claim is about: a latency claim must be reported at the percentile its SLO governs, and a causal claim must exclude the alternatives its design leaves open. Both reasoned from the artifact's text (L36, L42).

**Assessment.** The most consequential measurement is the missing one: the memo names a p99 SLO in its last line and reports a mean.

**Strengths.** Replaying real logged requests rather than a synthetic generator (L12) is the most credible choice here, and worth keeping through any rework.

**Weaknesses, risks & errors.**
- **Critical, defect (C3).** "Our inference SLO is p99 latency under 800 ms." (L42). The Results table (L26–30) holds throughput, mean latency and GPU utilisation — no percentile row. Continuous batching is precisely the mechanism that can buy throughput by lengthening the tail, and the memo drives utilisation to 89%. A 162 ms mean is compatible with both a comfortable p99 and a breached one.
- **Major, defect (M3).** "GPU utilisation rising from 54% to 89% is direct evidence of this." (L36). Raising the batch ceiling from 16 to 64 predicts the same rise with no continuous-batching claim attached, and utilisation counts time with work resident, not useful work. Consistent evidence, not direct evidence.
- **Major, defect (M7).** "2,000 requests drawn from the production request log of 3 August 2026" (L12) — one day, both runs inside one hour of it. No input- or output-length distribution is given, and the size of a continuous-batching gain is largely a function of output-length spread.
- **Major, defect (M4).** "See the attached throughput chart for the full run profile." (L32). The document's own cited evidence for the run profile is not in the document.

**Narrowing note on Seat 1's C1.** I wrote after Seat 1 and saw its analysis, so treat this as revision, not independent confirmation: both arms list "1× A10G" (L17). The confound is host-side and configuration-side, not accelerator-side, and C1 is better stated as "host size and batch ceiling uncontrolled" than "different hardware".

**Gaps.** No error or timeout count. No token counts. No statement that both arms were served the identical 2,000 requests in the same order — L12 implies one draw but never says it was replayed identically.

**Strongest reason this might be fundamentally wrong.** If the sampled 2,000 requests skew toward short summaries, the gain may not transfer to the production mix at all — the mechanism the memo credits is the one most sensitive to that skew, and nothing here lets a reader check it.

**Domain verdict.** The conclusion does not follow from the data shown. The data support something narrower: at ~16 concurrent requests, on a larger host with a larger batch ceiling, mean latency more than halved.

**Recommended fixes.** Report p50/p95/p99 per arm; publish the output-length histogram; attach the run profile; restate L36 as "consistent with"; report error counts.

### Seat 3 — Decision red-team

**Role & remit.** Whether the recommendation survives contact with production, and the strongest case against acting on it.

**Standard applied, and its source.** My own judgment against the memo's stated purpose (L4): a rollout recommendation must not claim scope beyond its evidence, and must state what it costs if wrong.

**Assessment.** A $340,000, four-fleet, one-quarter commitment resting on roughly a minute of aggregate steady-state traffic on one workload.

**Strengths.** The recommendation is specific and falsifiable — it names a fleet fraction, a figure and a quarter, which is what makes it checkable at all.

**Weaknesses, risks & errors.**
- **Critical, defect (C4).** "Roll v3.0 to all four inference fleets in Q4." (L40) against "our standard summarisation workload" (L12). Three of the four fleets are never characterised: nothing states they run summarisation, the same model, or the same instance family. Evidence covers one case; the conclusion covers four.
- **Major, defect (M2).** "At 2.4× throughput we can retire roughly 40% of the current fleet, saving an estimated $340,000 a year in instance cost." (L40). Two problems. First, 2.4× per instance would permit retiring about 58% (1 − 1/2.4), not 40%; no derivation is shown and the margin is never explained, so a reader cannot tell whether 40% is prudence or a different model. Second, the 2.4× came from `g5.4xlarge` while the baseline ran on `g5.2xlarge` (L17), so savings must be per dollar, not per instance. Larger instances in a family cost more per hour `[unverified — recall, not lookup]`; the memo gives neither prices nor fleet size, so the sign of the saving is not established from this document.
- **Major, gap (M6).** The Method table (L14–20) lists version, instance, batch size, quantisation, warm-up. No output-parity or quality check appears anywhere. A server upgrade that changes batching, and possibly sampling or numerics, can change what the model returns; the memo offers no evidence it does not.
- **Minor, defect (m2), unverified.** No canary, rollback trigger or abort criteria accompany a fleet-wide Q4 change (L40).
- **Minor, defect (m1), unverified.** "v3.0 is 2.4× faster than v2.1" (L8) uses one word for a throughput ratio and a latency reduction; they coincide at 2.40× only because concurrency was pinned.

**Gaps.** No migration or engineering cost set against the saving. No peak-hour headroom analysis after retiring 40% of capacity. No account of what happens if v3.0 must be rolled back once the fleet has shrunk.

**Strongest reason this might be fundamentally wrong.** Not that v3.0 is bad — it is plausibly better. It is that the three numbers that will actually be committed to a budget and a capacity plan (2.4×, 40%, $340k) are the three the evidence does not establish. The realistic failure is not a missed saving: it is retiring 40% of the fleet, then breaching the p99 SLO in peak hour with the headroom gone and nothing to fail back to.

**Domain verdict.** Do not act on as-is. The direction may be right; the magnitudes are unsupported and the scope is four times the evidence.

**Recommended fixes.** Benchmark each fleet on its own workload before including it; rebuild cost as requests-per-dollar at the SLO using both instances' real prices; add an output-parity check; stage one fleet with a canary and named abort criteria.

---

## Verification pass (Step 5)

Re-opened the artifact and searched for every string behind the four critical and seven major findings, asking what would falsify each rather than what would support it. Strings found where claimed: "g5.2xlarge"/"g5.4xlarge" and "1× A10G" (L17); "41.2"/"98.9"/"388"/"162" (L28–29); "p99" (L42 only — no percentile row at L26–30); "all four inference fleets" (L4, L40); "run once, end to end" (L22); "roughly 40%"/"$340,000" (L40); "direct evidence" (L36); "attached throughput chart" (L32, no chart present); "justify" (L4); "2,000 requests drawn from the production request log of 3 August 2026" (L12). Method table searched for accuracy/quality/parity rows: none (L14–20), so M6 is anchored on the table under the absence rule.

Recomputations: 41.2 × 0.388 = 15.99; 98.9 × 0.162 = 16.02; 2000 ÷ 41.2 = 48.5 s; 2000 ÷ 98.9 = 20.2 s; 1 − 1/2.4 = 58.3%.

- **C1 — Corrected.** Narrowed from "larger hardware" to "same accelerator, double the vCPU, plus an uncontrolled batch ceiling (L18)". Stands at critical; the batch-ceiling change is an independent confound the same-GPU observation does not touch.
- **M2 — Corrected.** The first draft called the arithmetic wrong; at 58.3%, "roughly 40%" is conservative, not incorrect. Restated as "derivation unshown and unreconciled", with the instance-price half marked unverified rather than asserted.
- **C2 falsifier that survives:** throughput and latency measured over different windows would break the ≈16 reading; the memo states neither way, so C2 is carried as an inference in the confidence note.

One check that could have withdrawn a finding did not: warm-up **is** controlled — "Warm-up requests | 100 | 100" (L20) — so no missing-controls claim was allowed to extend to warm-up or quantisation.

**Withdrawn: 0. Corrected: 2 (C1, M2).** Minor findings m1 and m2 skipped this pass and are labelled unverified.

## 6. Executive review

I re-read the artifact end to end before writing this, and personally checked the anchor of every critical and major finding upheld below.

**Points of agreement.** Three: the 2.4× is not attributable to the version (Seats 1, 2); capacity and cost claims outrun the measurement (Seats 1, 3); the p99 SLO is stated and never measured (Seats 2, 3). **All three are marked sole-source** — the seats ran sequentially in one context, so none of this agreement is independent corroboration; each stands on its anchor alone.

**Deduplicated.** C2 and M2 share one root: the memo never measures capacity, so every capacity-derived number is unfounded. Stated once here; C2 remains the critical finding, M2 the distinct downstream defect in the cost derivation.

**Conflict & adjudication.**
- Seat 2 narrowed Seat 1's C1 because both arms share "1× A10G" (L17). **Upheld at critical, with Seat 2's wording adopted.** The same-GPU point does not reach the batch-ceiling change (L18), and the ~16-in-flight reading leaves a CPU-side bottleneck at 8 vCPU unexcluded. Two uncontrolled variables remain.
- Seat 3 raised authorship — "**Author:** ML platform" (L3), the team that owns v3.0 — at major. **Downgraded to a blind-spot note, not a finding.** Specific evidence: nothing in the reported numbers shows manipulation, they are internally consistent, and the design defects are already captured at C1–C4. An incentive is a reason to seek replication, not a defect in the artifact.
- Silence noted: no seat examined output quality or verified pricing, so no seat has voted on either.

**Verification result.** Zero withdrawn, two narrowed (C1, M2). No seat's reliability is in question; both corrections tightened wording rather than removing substance.

**Panel blind spots.** The seats shared one context, so their coverage gaps are shared too, not just their agreement. No seat examined **output quality or parity between 2.1.4 and 3.0.1** — a critical defect could live there and this review would not have seen it. No seat verified **instance pricing**; the $340k rests on numbers absent from the document and needs external checking before it enters a budget. Also unexamined: peak-hour headroom after a 40% reduction, and licensing or security implications of the version bump. Shared assumptions: that the figures were correctly instrumented, that "req/s" means completed requests, and that "mean latency" is end-to-end — none checkable from the document.

**Overall judgment.** The underlying result may be real: v3.0 is plausibly faster, and the mean-latency halving at fixed concurrency is the memo's most defensible number. But as justification for a four-fleet, $340,000 decision it does not work — three variables move at once, neither configuration is measured at its limit, the only latency statistic its own SLO names is missing, and a single-workload result is extended to three fleets it never characterises. The problems are in the experiment, not the prose, so editing cannot fix them.

**Decision on further action: reject and rework.**

**Prioritized next steps.**
1. Re-run matched: same instance type, same max batch size, version as the only variable, ≥5 runs per arm.
2. Sweep load to saturation and report p50/p95/p99 against the 800 ms SLO before any capacity claim.
3. Add an output-parity check between 2.1.4 and 3.0.1.
4. Rebuild the cost case as requests-per-dollar at the SLO with both instances' real prices, showing the derivation from throughput to fleet fraction.
5. Characterise the other three fleets' workloads before including them; stage the rollout one fleet at a time with named abort criteria.

**Confidence & what would change the verdict.** Of the eleven findings at critical and major, I expect nine to survive an independent expert re-check. The two I expect to fall first are M4 (a reviewer holding the chart would drop it) and M5 (a reviewer may read "justify" as ordinary memo phrasing, not a design defect). C4 would narrow to major if the other three fleets are known to run the same workload — information not in the artifact. The verdict rests on verified quotes for C1, C3, C4 and every major, and on one **inference** for C2: that throughput and mean latency describe the same steady-state window, making mean concurrency ≈ 16. If the runs were open-loop and saturated, C2 weakens to "saturation not documented" — still major, and the decision holds, because C1, C3 and C4 are each independently sufficient for it. What would flip it to approve-with-revisions: a matched-instance, matched-batch re-run with a load sweep and p99 at or under 800 ms, plus a cost model in requests-per-dollar.
