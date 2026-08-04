# Storage capacity forecast — object store, FY27

**Author:** infrastructure
**Purpose:** decide whether to commit to a larger reserved-capacity tier before the 1 November deadline.
**Confidence:** moderate. See "What would change this" before acting.

## What we are forecasting

Total bytes stored in the primary object store on 31 October 2027, and whether that figure crosses the 2.5 PB threshold at which the next reserved tier becomes cheaper than on-demand.

## Data

Monthly totals for the 24 months to 31 July 2026, taken from the billing export rather than from the store's own metrics API. The two disagree by 1–3% in every month; the billing export is the figure we are charged on, so it is the one we forecast.

Current total: 1.31 PB. Trailing-12-month growth: 38%. Trailing-6-month growth, annualised: 31%.

## Method

Three scenarios, not a point estimate.

| Scenario | Assumption | 31 Oct 2027 total |
|---|---|---|
| Low | Growth decays to 22%/yr, matching the slowdown in new-account creation since March | 1.68 PB |
| Base | Growth continues at the trailing-6-month rate of 31%/yr | 1.84 PB |
| High | Growth returns to 38%/yr and the two pending enterprise migrations land in Q1 | 2.17 PB |

The two pending migrations are modelled at 210 TB combined, which is the figure in their signed contracts. Neither has a confirmed date.

## Assumptions we are making

1. The retention policy does not change. A shortening of the 7-year retention on archived exports would remove an estimated 340 TB and invalidate all three scenarios.
2. No large customer departs. Our three largest accounts hold 41% of stored bytes between them.
3. Compression ratios stay where they are. We have no plans to change the encoder.
4. Growth is modelled as compounding monthly on total stored bytes, which assumes deletion stays at its historical 2–4% of monthly writes. It has not exceeded 5% in 24 months.

## Conclusion

Under all three scenarios we stay below 2.5 PB on 31 October 2027. The high scenario reaches 2.17 PB, which is 87% of the threshold — close enough that a third large migration would cross it.

**Recommendation:** do not commit to the larger tier this year. Re-run this forecast in April 2027, when both pending migrations will have either landed or lapsed.

## What would change this

- Either pending migration landing at more than 350 TB rather than the contracted 210 TB combined.
- A third enterprise migration entering the pipeline before April.
- Monthly deletion rate falling below 1%, which would push the base case to roughly 1.95 PB.
- The billing export and metrics API diverging by more than 5%, which would mean one of them is wrong and the baseline is unreliable.

## Known weaknesses

24 months is a short series for a 15-month forecast, and it covers only one enterprise migration, so the high scenario's migration assumption rests on a single prior observation. We have not modelled the possibility that growth is not exponential at all; a linear fit to the last 12 months gives 1.71 PB, inside our range but for different reasons.
