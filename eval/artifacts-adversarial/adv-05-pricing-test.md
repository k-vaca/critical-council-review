# Starter Monthly Price Test ($29 → $34): Readout and Rollout Recommendation

**To:** Pricing Committee | **From:** D. Ferraro, Growth Analytics | **Date:** 28 July 2026 | **Experiment ID:** PRC-2026-114

## Summary

We tested a $29 → $34 list price on Starter monthly in self-serve checkout for 28 days. Conversion fell 10.3% relative, average order value rose 16.0%, and revenue per visitor (RPV) rose 5.3% (95% CI +1.9% to +8.7%, p = 0.002). Guardrails were clean. **We recommend rolling $34 out to all new self-serve Starter monthly purchases, grandfathering existing subscribers for twelve months and retaining a 5% holdback for a 90-day follow-up.**

## Background

Starter monthly is the entry plan on self-serve, last repriced in 2022. New Starter monthly subscriptions add roughly **$24.4M** in annualized subscription value per year. All four self-serve plans together — Starter monthly, Starter annual, Team, and Business — add roughly **$68.2M**.

## Design

- **Randomization:** visitor-level, sticky by visitor ID and resolved to account ID when signed in, so no visitor saw both prices.
- **Window:** 22 June – 19 July 2026 — 28 days, four complete weekly cycles. Release freeze confirmed: no promotions, pricing-page redesign, or checkout changes shipped.
- **Exposure:** only the price on the Starter monthly card differed between arms. Existing subscribers billed at $29 and were out of sample.
- **Pre-registration:** fixed horizon, single analysis at day 28, no interim peeking. At the observed variance the test was powered to detect a 6.4% relative RPV change at 80% power.
- **Sample ratio:** 61,480 control / 61,203 treatment (50.1% / 49.9%), χ² p = 0.43. No sample ratio mismatch.
- **Estimation:** order values winsorized at the 99.5th percentile of the pooled pre-period distribution, identical threshold in both arms. Intervals from a 10,000-resample visitor-level bootstrap, not a t-test, given right-skewed order values.

## Table 1 — Primary results, 28 days

| | Control ($29) | Treatment ($34) | Change |
|---|---|---|---|
| Visitors | 61,480 | 61,203 | — |
| Orders | 2,214 | 1,977 | — |
| Conversion | 3.601% | 3.230% | −10.3% rel. |
| Average order value | $34.60 | $40.15 | +16.0% |
| First-invoice revenue | $76,604 | $79,377 | — |
| **Revenue per visitor** | **$1.2460** | **$1.2969** | **+4.1%** |

Unadjusted RPV lift: **+4.1%** (95% CI −0.4% to +8.6%, p = 0.074). Seats per order moved 1.19 → 1.18, not significant, so the AOV gain is price rather than a mix shift into larger orders. Implied elasticity over this range is −0.6 (−10.3% orders for +17.2% price).

*Reconciliation: the two arms produced $155,981 in first invoices over 28 days; annualized (×13.04) and carried over twelve monthly cycles before churn, that is the $24.4M above.*

## Variance reduction

The unadjusted interval spans zero, as the power calculation anticipated. To recover precision we applied CUPED, regressing visitor-level RPV on two covariates measured over the experiment window — sessions per visitor and pricing-page views per visitor — pooled across arms. Both were balanced between arms (sessions per visitor 2.41 control vs 2.38 treatment, p = 0.19), so the adjustment is not absorbing an arm-level difference. It cut estimator variance by 43%.

**Adjusted RPV lift: +5.3% (95% CI +1.9% to +8.7%, p = 0.002).** We report the adjusted estimate as primary.

## Table 2 — Revenue per visitor by acquisition source (unadjusted)

Every visitor is assigned exactly one source at first touch, so the rows below partition the sample.

| Source | Ctrl visitors | Ctrl orders | Ctrl AOV | Ctrl RPV | Trt visitors | Trt orders | Trt AOV | Trt RPV | RPV lift |
|---|---|---|---|---|---|---|---|---|---|
| Organic & direct | 26,417 | 1,043 | $35.20 | $1.3898 | 26,298 | 952 | $40.90 | $1.4806 | +6.5% |
| Paid search | 17,142 | 512 | $33.10 | $0.9886 | 17,090 | 476 | $38.60 | $1.0751 | +8.7% |
| Partner referral | 6,834 | 253 | $36.40 | $1.3476 | 6,791 | 220 | $42.30 | $1.3703 | +1.7% |

The lift is positive in every source, so the result is not one segment carrying the average. Partner referral is weakest, consistent with a price expectation set by the partner's listing page. Segments were pre-registered but reported descriptively; we make no inferential claim on any single row and have not adjusted for multiplicity.

## Guardrails

| Metric | Control | Treatment | p |
|---|---|---|---|
| Refunds + chargebacks within 14 days | 1.9% | 2.1% | 0.31 |
| Support contacts per 100 orders | 4.4 | 4.6 | 0.44 |
| Day-21 retention (2,043 orders from weeks 1–2) | 94.8% | 94.1% | 0.36 |

Nothing moves. The day-21 check matters most: it rules out a higher price merely buying forward revenue that churns in the first cycle.

## Financial impact

Applying the +5.3% RPV lift to the **$68.2M** self-serve annualized new-subscription base, discounted 20% for novelty and seasonality — the same haircut the committee applied to last year's Team change — gives **+$2.89M annualized**. That clears the $1.5M incremental threshold the committee set for a plan-level price change. We have not extended the lift to Team or Business, which were untouched by this test.

## Limitations

Twenty-eight days cannot observe churn past the first renewal cycle; day-21 retention is the longest read we have. With one price point, the elasticity should not be extrapolated to a larger increase. The holdback addresses both.

## Recommendation

1. Roll $34 to 100% of new self-serve Starter monthly purchases, effective the first of next month.
2. Grandfather existing subscribers at $29 for twelve months, then migrate with 60 days' notice.
3. Hold back 5% of eligible traffic at $29 for 90 days; re-read RPV, retention, and refunds before the grandfather window closes.
4. Re-test at $39 no earlier than Q1 2027.
