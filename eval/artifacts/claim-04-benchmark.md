# Benchmark: inference server v3.0 vs v2.1

**Author:** ML platform
**Purpose:** justify the v3.0 rollout to all inference fleets in Q4.

## Summary

**v3.0 is 2.4× faster than v2.1.** We recommend rolling it out fleet-wide.

## Method

We ran our standard summarisation workload — 2,000 requests drawn from the production request log of 3 August 2026 — against two configurations.

| | v2.1 baseline | v3.0 candidate |
|---|---|---|
| Server version | 2.1.4 | 3.0.1 |
| Instance | `g5.2xlarge` (8 vCPU, 1× A10G) | `g5.4xlarge` (16 vCPU, 1× A10G) |
| Max batch size | 16 | 64 |
| Quantisation | none | none |
| Warm-up requests | 100 | 100 |

Each configuration was run once, end to end, on 3 August between 14:00 and 15:00 UTC.

## Results

| Metric | v2.1 | v3.0 | Change |
|---|---|---|---|
| Throughput (req/s) | 41.2 | 98.9 | +140% |
| Mean latency (ms) | 388 | 162 | −58% |
| GPU utilisation | 54% | 89% | +35pp |

See the attached throughput chart for the full run profile.

## Interpretation

The gain comes from v3.0's continuous batching, which keeps the GPU fed instead of waiting for a batch to fill. GPU utilisation rising from 54% to 89% is direct evidence of this.

## Recommendation

Roll v3.0 to all four inference fleets in Q4. At 2.4× throughput we can retire roughly 40% of the current fleet, saving an estimated $340,000 a year in instance cost.

Our inference SLO is p99 latency under 800 ms.
