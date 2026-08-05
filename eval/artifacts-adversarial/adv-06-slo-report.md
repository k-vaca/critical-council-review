# Q2 2026 Reliability Review — Checkout API

**To:** Payments Platform leadership; Checkout EM/PM
**From:** P. Raman, Staff SRE, Checkout
**Date:** 2 July 2026
**Re:** Q2 SLO performance, error budget position, and Q3 investment recommendation

## 1. SLO and error budget policy

Per SLO doc v4.2, the Checkout API carries a request-ratio availability objective: **99.9% of valid checkout requests succeed.** The stated intent (§1 of that doc) is to measure the share of customer checkout attempts that the platform completes successfully.

- **Valid requests** — all checkout requests arriving at the edge, excluding (a) synthetic probes, (b) traffic carrying `X-LoadTest`, and (c) requests rejected at the edge with HTTP 429 and never dispatched to the service. Exclusion (c) is the platform SLI template's standard rate-limit carve-out.
- **Good requests** — valid requests answered 2xx, or 4xx other than 429, inside the 5s edge timeout.
- **Bad requests** — valid requests answered 5xx, or timed out.
- **Error budget** — 0.1% of valid requests in the window, computed on the same denominator as the SLI. Budget does not carry across windows.
- **Windows** — SLO compliance is reported per calendar quarter. The error budget policy is evaluated on a trailing 30-day window: releases to checkout pause while that window is more than 100% consumed, and resume when it falls back under. At this quarter's close the trailing 30-day window is 1–30 June.

## 2. Measurement method

The SLI comes from edge load-balancer request logs in 1-minute buckets. Quarterly availability is pooled — total good over total valid across all 131,040 minutes of the 91-day quarter — not an average of per-minute or per-month ratios. This matters: the unweighted mean of the three monthly figures below reads 99.9394%, 0.0019pp higher, because June carried more traffic. One 22-minute logging gap (3 May, 04:10–04:32 UTC, no incident in progress) was backfilled from CDN counters.

Client-side RUM puts quarterly checkout success at 99.86%, below the server-side SLI. That gap is expected — RUM also captures client network failures, app crashes, and session abandonment — and RUM remains a monitoring signal, not the SLO of record.

## 3. Results

| Month | Valid requests | Bad requests | Availability |
|---|---|---|---|
| April | 396.0M | 78,000 | 99.9803% |
| May | 410.0M | 117,000 | 99.9715% |
| June | 434.0M | 580,000 | 99.8664% |
| **Q2** | **1,240.0M** | **775,000** | **99.9375%** |

Impact window is first to last 1-minute bucket above a 1% checkout error ratio; impact minutes are the length of that window, not time-to-resolve. Postmortem clocks (detection to all-clear) run longer and are not used here.

| ID | Date | Impact window (UTC) | Impact (min) | Failed requests | Trigger |
|---|---|---|---|---|---|
| INC-4471 | 18 Apr | 09:12–09:58 | 46 | 60,000 | Bad config push, pricing sidecar |
| INC-4519 | 6 May | 22:40–23:31 | 51 | 45,000 | Primary DB failover |
| INC-4562 | 27 May | 03:15–04:02 | 47 | 53,400 | Expired mTLS cert, fraud service; risk-threshold requests failed closed |
| INC-4610 | 11 Jun | 14:05–15:47 | 82 | 447,000 | Write-path saturation |
| INC-4633 | 24 Jun | 18:30–19:12 | 42 | 115,000 | Cache stampede after region drain |
| **Total** | | | **268** | **720,400** | |

The remaining 54,600 bad requests are non-incident background errors, steady at roughly 600/day across the quarter.

INC-4610 dominates. A connection-pool sizing change shipped that morning saturated the checkout write path. 447,000 requests that reached the service failed; the edge's adaptive shedder engaged at 14:11 and turned away a further 612,000 checkout requests with HTTP 429 until the write path recovered. The change was reverted the same day and a capacity guardrail added to the pre-merge suite.

## 4. Error budget position

The quarterly error budget is 1,240,000 bad requests (0.1% of 1,240.0M valid). We consumed 775,000 of it — 62.5% — leaving 465,000, or 37.5%, unused. June carried 74.8% of the quarter's burn and 46.8% of the quarterly allowance, nearly all of it INC-4610. **We are not in a release freeze under the error budget policy: 37.5% of the budget remains.**

Two cross-checks. MSA Schedule C caps checkout unavailability at 280 impact-minutes per quarter before service credits are owed; at 268 minutes we closed 12 minutes inside the cap. For orientation only, 268 minutes against the quarter's 131,040 is 99.80% time-based availability — we do not use a time-based SLI here, because checkout traffic swings roughly 6x between trough and peak, so a minute is not a constant unit of customer harm.

## 5. Recommendation

**Ship.** Hold the Q3 roadmap as planned, move the release train from weekly to twice-weekly starting 13 July, and defer the two open reliability epics — write-path capacity headroom and shed-aware client retries — into Q4.

The quarter finished above objective with over a third of the budget unspent. The one incident that mattered has a root cause already reverted and guarded in CI; the other four were unrelated to release velocity — a config push, a planned failover, a cert expiry, and a region-drain stampede. As a counterfactual, Q2 without INC-4610 would have closed at 99.9735%.

This changes if a second saturation-class incident lands in July, or if the Q3 traffic forecast is revised above +15%; either would make twice-weekly cadence hard to defend before the capacity work.
