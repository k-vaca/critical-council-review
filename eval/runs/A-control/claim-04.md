# Review — claim-04-benchmark.md

Artifact: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/claim-04-benchmark.md`
Scope: one expert review pass. Reviewed as a benchmark report intended to justify a fleet-wide production rollout and a capacity/cost decision.

## Verdict

The arithmetic in the document is internally consistent (98.9/41.2 = 2.40×; +140% throughput; −58% mean latency; 89−54 = 35pp). The problem is not the numbers, it is the experiment. Two variables were changed alongside the software version, so the headline 2.4× cannot be attributed to v3.0; and the decision the document recommends (retire 40% of fleet, save $340k) rests on a latency metric that is not the one in the SLO and a cost model that ignores the instance upgrade. As written, a recipient acting on this can both overstate savings and breach the stated SLO.

---

## Critical

### C1 — Method table, line 17: instance type is not held constant
**Anchor:** "`g5.2xlarge` (8 vCPU, 1× A10G) | `g5.4xlarge` (16 vCPU, 1× A10G)"
**Problem:** v3.0 was measured on an instance with twice the vCPU (and roughly twice the memory and network) as v2.1, so the 2.4× cannot be attributed to the software version at all.

Note: this cuts especially deep for an inference server, where host CPU drives tokenisation, detokenisation, request scheduling and HTTP handling — exactly the work that determines whether the GPU stays fed. The missing arm is v3.0 on `g5.2xlarge` (and ideally v2.1 on `g5.4xlarge`).

### C2 — Method table, line 18: max batch size is not held constant
**Anchor:** "Max batch size | 16 | 64"
**Problem:** A second uncontrolled variable was changed at the same time, so any portion of the gain attributable to a 4× larger batch window — some of which v2.1 might also capture — is silently credited to v3.0.

### C3 — Recommendation, line 40: cost model ignores the more expensive instance
**Anchor:** "we can retire roughly 40% of the current fleet, saving an estimated $340,000 a year in instance cost"
**Problem:** The throughput was achieved on a `g5.4xlarge`, which costs materially more per hour than the `g5.2xlarge` baseline (on-demand, roughly 1.3–1.4×), so a fleet that migrates to the tested configuration pays more per remaining node and the $340k figure is overstated by an unknown and possibly decisive margin.

Worked illustration with the document's own numbers: retiring 40% leaves 0.6N nodes; at ~1.34× unit price the new fleet costs ~0.80× the old, i.e. a ~20% saving, not the ~40% the framing implies. If instead the fleet stays on `g5.2xlarge`, the 2.4× was never measured on that hardware (see C1) and the savings basis disappears entirely.

### C4 — Line 42 against line 29: the SLO metric was never measured
**Anchor:** "Our inference SLO is p99 latency under 800 ms."
**Problem:** Only mean latency is reported, and mean latency cannot certify a p99 SLO — continuous batching characteristically trades tail latency for throughput, so the one number that governs whether this rollout is safe is absent.

This compounds with the capacity recommendation: the tested v3.0 configuration already sits at 89% GPU utilisation, and retiring 40% of the fleet pushes the survivors further toward saturation, the regime where p99 degrades non-linearly. The document recommends the action most likely to break the constraint it states one line later. Required before rollout: p50/p95/p99 at the target post-consolidation load.

---

## Major

### M1 — Method, line 22: single unreplicated run, and each run lasts under a minute
**Anchor:** "Each configuration was run once, end to end, on 3 August between 14:00 and 15:00 UTC."
**Problem:** With n=1 per arm there is no variance estimate, no confidence interval and no control for ordering, thermal or noisy-neighbour effects; worse, 2,000 requests at the reported rates means only ~49 s of measurement for v2.1 and ~20 s for v3.0, far too short to reach steady state (KV-cache pressure, memory fragmentation, scheduler warm-up) and enough for only ~20 samples in the p99 tail.

### M2 — Interpretation, line 36: GPU utilisation is misused as causal evidence
**Anchor:** "GPU utilisation rising from 54% to 89% is direct evidence of this."
**Problem:** Standard GPU utilisation reports the fraction of time any kernel is resident, not useful work or occupancy, and the doubled host CPU (C1) is an equally good explanation for better GPU feeding — so this is consistent with the continuous-batching story but is not evidence for it over the alternatives.

### M3 — Method line 12 against Recommendation line 40: one workload generalised to four fleets
**Anchor:** "Roll v3.0 to all four inference fleets in Q4."
**Problem:** The evidence is a single summarisation workload from a single log; fleets running chat, embedding, long-context or heavily variable-output workloads have different batching dynamics and prefill/decode ratios, so the result does not transfer without per-fleet measurement.

### M4 — Results section: no error rate and no output-equivalence check
**Anchor:** "| Throughput (req/s) | 41.2 | 98.9 | +140% |"
**Problem:** The report never states that all 2,000 requests succeeded in both arms or that v3.0 produced equivalent outputs, and throughput gains that come from dropped, truncated or numerically divergent responses would be indistinguishable from real gains in this table.

### M5 — Method: load model and concurrency are unspecified, and the numbers imply batch-64 was never exercised
**Anchor:** "2,000 requests drawn from the production request log of 3 August 2026"
**Problem:** Neither the offered concurrency nor whether the harness is open- or closed-loop is stated, yet throughput × mean latency gives an in-flight concurrency of ~16.0 in *both* arms (41.2 × 0.388 and 98.9 × 0.162), which indicates a fixed concurrency of 16 — below the v3.0 batch ceiling of 64, so neither arm measured saturation throughput and the configuration change in C2 was likely never actually engaged.

If that reading is right, the benchmark measured latency-at-fixed-concurrency and relabelled it capacity; a capacity claim needs a load sweep to the knee of the throughput/latency curve.

### M6 — Recommendation, line 40: the capacity and savings figures are not derived
**Anchor:** "At 2.4× throughput we can retire roughly 40% of the current fleet"
**Problem:** 2.4× throughput implies needing 1/2.4 = 41.7% of nodes, i.e. retiring ~58%, not 40%, and the document gives no fleet size, instance count, hourly price, utilisation headroom or pricing model (on-demand vs reserved vs spot), so neither the 40% nor the $340,000 can be checked or reproduced by the reader.

### M7 — Method section: the run is not reproducible
**Anchor:** "We ran our standard summarisation workload"
**Problem:** Model identity and size, input/output token length distribution, sampling parameters, load-generator identity, and server flags beyond batch size and quantisation are all omitted, so no one can rerun this benchmark or audit the claim.

---

## Minor

### Mi1 — Line 32: referenced evidence is absent
**Anchor:** "See the attached throughput chart for the full run profile."
**Problem:** Nothing is attached or linked, so the only offered view of run-profile behaviour over time — where warm-up artefacts and instability would show — is unavailable to the reader.

### Mi2 — Line 12 against line 22: the request log cannot cover the day it was drawn from
**Anchor:** "the production request log of 3 August 2026"
**Problem:** The run happened on 3 August between 14:00 and 15:00 UTC, so at most a partial day of that log existed, and the sample cannot be claimed to represent the full diurnal traffic mix including peak.

### Mi3 — Line 20: warm-up and request-set handling are ambiguous
**Anchor:** "Warm-up requests | 100 | 100"
**Problem:** It is not stated whether the 100 warm-up requests are inside or outside the 2,000 measured, nor whether both arms replayed the identical request set in identical order, either of which shifts the comparison.

---

## What would make this decision-grade

1. Re-run with one variable changed at a time: v2.1 and v3.0 on the same instance type, same max batch size; then a separate arm for the batch-size change.
2. Report p50/p95/p99 and error rate, and run a load sweep to saturation rather than a single fixed-concurrency point.
3. At least 3–5 repetitions per arm over a longer window, with variance reported.
4. Validate output equivalence between versions before treating this as a speed-only change.
5. Rebuild the cost case on measured throughput-per-dollar at the target instance type, showing fleet size, unit price and headroom assumptions.
6. Scope the rollout recommendation to the fleet actually measured; treat the other three as untested.
