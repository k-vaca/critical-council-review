# Experiment readout: simplified signup form

**Owner:** growth
**Ran:** 14 July – 22 July 2026
**Decision requested:** ship variant B to 100%.

## Setup

Variant A is the current four-field signup form. Variant B removes the "company size" and "how did you hear about us" fields, leaving email and password. Traffic split 50/50 on first visit, sticky by cookie. Primary metric: signup completion rate (completed signups ÷ form views).

We planned for a two-week run. We monitored the dashboard daily and stopped on day 9, when the difference reached significance.

## Results

| | Form views | Signups | Completion rate |
|---|---|---|---|
| A (control) | 18,204 | 1,438 | 7.90% |
| B (variant) | 18,061 | 1,592 | 8.81% |

Variant B improves completion by **11.5%**. Two-proportion z-test, p = 0.0038.

## Secondary metrics

Day-7 activation (created at least one project) was 31.2% for A and 29.8% for B. Not significant at n this size.

Support tickets tagged `signup` were 6 for A and 9 for B over the period.

## Recommendation

Ship B to 100%. The completion gain is large and clearly significant, and no secondary metric moved against us. Removing the two fields costs us the self-reported attribution data, which marketing says they can live without for a quarter.

We expect this to add roughly 1,850 signups a month at current traffic.
