# Expert review — PRC-2026-114, "Starter Monthly Price Test ($29 → $34)"

Reviewer pass: one careful expert read. Every figure on the page was re-derived independently
before being accepted. Findings are ordered by severity.

## What checks out (so the findings below are read in proportion)

These were verified and are correct — they are not defects:

- Table 1 internal arithmetic. Conversion 2,214/61,480 = 3.6011%; 1,977/61,203 = 3.2302%;
  relative change −10.30%. AOV change 5.55/34.60 = +16.04%. First-invoice revenue
  2,214 × 34.60 = $76,604 and 1,977 × 40.15 = $79,377. RPV $1.24600 and $1.29694,
  unadjusted lift +4.09%. The multiplicative identity holds: 0.8970 × 1.1604 = 1.0409.
- Sample-ratio check. 61,480/122,683 = 50.11%, 61,203/122,683 = 49.89%; χ²(1) = 0.625,
  p = 0.43. Stated correctly.
- Power statement. Unadjusted half-width 4.5pp ⇒ SE = 2.296pp; MDE at 80% power
  = 2.8016 × 2.296 = 6.43%. Matches the stated 6.4%.
- Both p-values. z = 4.1/2.296 = 1.786 ⇒ p = 0.074. z = 5.3/1.735 = 3.055 ⇒ p = 0.002.
- The claimed 43% variance cut. (3.4/4.5)² = 0.571, i.e. a 42.9% reduction. Consistent
  with the two reported intervals, both of which are symmetric about their point estimates.
- Elasticity. Price +17.24%; −10.30/17.24 = −0.60.
- Window. 22 June – 19 July 2026 inclusive is 28 days, Monday to Sunday, four whole weeks.
- Every RPV cell and every lift in Table 2 recomputes exactly from its own row.
- Financial-impact arithmetic *as written*: 68.2 × 0.053 × 0.80 = $2.892M.
- Winsorizing at a **pre-period** percentile with an identical threshold in both arms is
  correct practice — which makes finding C2 below the more conspicuous.

The document is numerically careful at the cell level. Its failures are at the level of what
each number is entitled to be multiplied by, and what the estimator is entitled to claim.

---

## Critical

### C1 — The headline dollar impact is applied to a base ~2.8× larger than the test earns

**Location:** Financial impact, line 67 (interacts with Background, line 11).

**Anchor:** "Applying the +5.3% RPV lift to the **$68.2M** self-serve annualized new-subscription
base ... gives **+$2.89M annualized**."

**Problem:** The $68.2M base is all four self-serve plans, but the experiment changed only
Starter monthly, whose base the memo itself states as $24.4M — so the projection is applied
to a base it is not entitled to.

**Re-derivation.** The tested RPV is Starter-monthly first-invoice revenue per visitor:
control AOV $34.60 ≈ 1.19 seats × $29, treatment $40.15 ≈ 1.18 × $34. Nothing in the metric
touches Starter annual, Team, or Business. The lift is therefore entitled to the $24.4M base
only:

| Base used | Calculation | Result | Clears $1.5M? |
|---|---|---|---|
| $68.2M (as written) | 68.2 × 0.053 × 0.80 | **$2.89M** | yes |
| $24.4M (correct) | 24.4 × 0.053 × 0.80 | **$1.03M** | **no** |
| $24.4M, unadjusted +4.1% | 24.4 × 0.041 × 0.80 | $0.80M | no |
| $24.4M, no 20% haircut | 24.4 × 0.053 | $1.29M | no |

The impact is overstated by a factor of 2.79. **Under every variant on the correct base —
including the most generous one, adjusted lift with no haircut at all — the test fails the
committee's $1.5M threshold.** The sentence "That clears the $1.5M incremental threshold" is
false, and it is the sentence the recommendation rests on.

A bottom-up check confirms the magnitude. Incremental RPV is $1.29694 − $1.24600 = $0.05093
per visitor. Across all 122,683 visitors that is $6,249 per 28 days, ×13.04 = $81,490 of
incremental first invoices per year, ×12 monthly cycles = $0.98M — the same ~$1M order of
magnitude, not $2.89M.

The memo also contradicts itself here within two sentences: "We have not extended the lift to
Team or Business, which were untouched by this test" — while the $68.2M base it just multiplied
by 5.3% *is* Starter monthly plus Starter annual plus Team plus Business (line 11). The
disclaimer describes an analysis the arithmetic did not perform.

**Fix:** recompute against $24.4M, restate the verdict against the $1.5M threshold, and take
the rollout recommendation back to the committee as a below-threshold change.

### C2 — CUPED covariates were measured inside the experiment window, so the primary estimate is not trustworthy

**Location:** Variance reduction, line 39.

**Anchor:** "we applied CUPED, regressing visitor-level RPV on two covariates measured over the
experiment window — sessions per visitor and pricing-page views per visitor"

**Problem:** CUPED requires covariates that cannot be affected by treatment — normally
pre-experiment data — and both covariates here are measured post-assignment and are plainly
downstream of the price the visitor was shown.

"Pricing-page views per visitor" is the most direct case: the price under test is *on the
pricing page*, so the number of times a visitor returns to it is a behavioural response to the
treatment. Sessions per visitor is the same problem one step removed — a visitor who hesitates
at $34 returns in a later session. Adjusting the outcome on a post-treatment variable
conditions away part of the treatment effect and introduces bias of unknown sign; it is not
variance reduction.

The memo's own defence does not hold: "Both were balanced between arms (sessions per visitor
2.41 control vs 2.38 treatment, p = 0.19), so the adjustment is not absorbing an arm-level
difference." A non-significant balance test is not evidence of no effect. At n ≈ 61,000 per arm
this is a 1.2% relative gap in the covariate, in the direction one would predict if a higher
price suppresses engagement, and p = 0.19 simply means the covariate check is underpowered
relative to the bias it needs to exclude. Note also that the same document winsorized against a
**pre-period** distribution (line 20) — the correct instinct, not carried over to the covariates.

Why this is critical rather than methodological hygiene: the pre-registered, unadjusted result
is **null** (+4.1%, 95% CI −0.4% to +8.6%, p = 0.074). Every significance claim in the memo —
the summary's "p = 0.002", the entire basis for rolling out — comes from the adjusted estimator
alone. If the adjustment is invalid, the experiment did not detect an effect. The adjustment
also moved the *point* estimate by 1.2pp (+4.1% → +5.3%, a 29% increase in effect size); valid
CUPED reduces variance and should leave the point estimate near-unchanged, so the shift is at
minimum worth explaining.

**Fix:** re-run CUPED on genuinely pre-period covariates (pre-assignment sessions, prior
visits, prior spend). If the pre-period-adjusted interval still spans zero, report the test as
null and do not roll out on it.

---

## Major

### M1 — Table 2 does not partition the sample; ~18% of visitors are unreported, and that block is negative

**Location:** Table 2, lines 45–53.

**Anchor:** "Every visitor is assigned exactly one source at first touch, so the rows below
partition the sample."

**Problem:** The three rows sum to 82% of each arm, not 100%, and the unreported residual has a
**−6.6%** RPV lift, which falsifies the claim that the lift is positive in every source.

**Re-derivation.**

| | Control | Treatment |
|---|---|---|
| Table 1 visitors | 61,480 | 61,203 |
| Table 2 rows summed | 26,417 + 17,142 + 6,834 = 50,393 | 26,298 + 17,090 + 6,791 = 50,179 |
| **Unreported visitors** | **11,087 (18.0%)** | **11,024 (18.0%)** |
| Table 1 orders | 2,214 | 1,977 |
| Table 2 orders summed | 1,043 + 512 + 253 = 1,808 | 952 + 476 + 220 = 1,648 |
| **Unreported orders** | **406** | **329** |
| Table 1 revenue | $76,604.40 | $79,376.55 |
| Table 2 revenue summed | $62,870.00 | $66,616.40 |
| **Unreported revenue** | **$13,734.40** | **$12,760.15** |

The implied residual segment:

| Residual segment | Control | Treatment | Change |
|---|---|---|---|
| Conversion | 406/11,087 = 3.662% | 329/11,024 = 2.984% | **−18.5% rel.** |
| AOV | $33.83 | $38.78 | +14.6% |
| **RPV** | **$1.2388** | **$1.1575** | **−6.6%** |

So the single largest block in the breakdown — larger than partner referral by a factor of
1.6 — lost 6.6% of revenue per visitor, and its conversion fell nearly twice as steeply as the
overall −10.3%. Two statements in the memo are therefore wrong as written: the partition claim,
and "The lift is positive in every source, so the result is not one segment carrying the
average." The correct reading is closer to the opposite: organic & direct (43% of the sample,
+6.5%) plus paid search are carrying an 18% block that is negative.

The disclaimer two lines down ("we make no inferential claim on any single row") does not cover
this. The sentence being disclaimed is a *robustness* claim about all rows, and it is
contradicted by the sample's own totals, not by a significance test.

**Fix:** name and report the missing source (email, app-store, unattributed, or whatever it is),
and withdraw the "positive in every source" claim.

### M2 — The day-21 guardrail cannot do the job the memo assigns it

**Location:** Guardrails, line 63 (and Limitations, line 71).

**Anchor:** "The day-21 check matters most: it rules out a higher price merely buying forward
revenue that churns in the first cycle."

**Problem:** For a monthly plan the first renewal decision occurs at ~day 30, so a day-21 read
stops short of the event it claims to rule out — and no order in the experiment reached its
first renewal before the analysis date.

The earliest orders were placed on day 1 (22 June) and renew ~22 July; the pre-registered
analysis point is day 28 (19 July). Not one subscription in the test was observed making a
renewal payment at $34. Day-21 retention on a monthly plan measures pre-first-bill cancellation
and refund behaviour — useful, but categorically not the renewal decision. The 94.8% vs 94.1%
comparison is therefore silent on the exact risk a price increase creates.

Limitations understates this too: "Twenty-eight days cannot observe churn past the first
renewal cycle" — it cannot observe the first renewal cycle *at all*.

**Fix:** restate the guardrail as "no elevated pre-renewal cancellation or refund signal," and
move first-renewal retention from a claimed result to an open risk that the holdback must
resolve.

### M3 — RPV measures Starter monthly revenue only, so plan substitution is unmeasured

**Location:** Design (Exposure, line 17) with Table 1 and Financial impact.

**Anchor:** "only the price on the Starter monthly card differed between arms"

**Problem:** Starter monthly sat on a pricing page alongside three unchanged plans, so some of
the 237 lost orders plausibly moved to Starter annual, Team, or Business — revenue the primary
metric does not count and the memo never checks.

Both control and treatment AOVs reconcile to Starter monthly seats × list price ($29 × 1.19 =
$34.51 vs $34.60; $34 × 1.18 = $40.12 vs $40.15), confirming the metric is plan-scoped. Raising
one plan's price by 17.2% changes its position relative to the plans beside it; substitution is
the expected first-order response, and it can cut either way — a visitor pushed to Starter
annual is revenue gained, a visitor pushed to nothing is revenue lost. Neither is visible here.

This compounds C1: total self-serve revenue per visitor is the only measurement that would
license an all-plan base, and it is exactly the measurement that was not taken.

**Fix:** re-cut the experiment data on total self-serve first-invoice revenue per visitor
across all four plans. That number already exists in the logs and settles both M3 and the
correct scope for C1.

### M4 — Both bases assume twelve monthly cycles with zero churn, and the haircut does not cover it

**Location:** Reconciliation, line 35; Financial impact, line 67.

**Anchor:** "annualized (×13.04) and carried over twelve monthly cycles before churn, that is
the $24.4M above"

**Problem:** The base counts twelve full payments from every new monthly subscriber with no
attrition, an assumption the memo elsewhere concedes it cannot support, and the 20% haircut is
explicitly attributed to novelty and seasonality rather than churn.

The chain reconciles arithmetically ($155,981 × 13.04 = $2.034M; × 12 = $24.41M), so the flaw
is the assumption, not the multiplication. For a self-serve monthly entry plan, twelve
consecutive renewals from 100% of a cohort is not a realistic expectation — at even 5% monthly
churn the expected cycles are ~9.2, not 12, cutting the base by roughly 23%. Since the impact
figure is this base × a percentage, the error passes straight through to the threshold test
that C1 already fails.

**Fix:** substitute an observed retention curve for the zero-churn assumption, or state the
implied 12-month survival explicitly so the committee can price the assumption itself.

### M5 — The primary estimator was adopted after the pre-registered one returned null

**Location:** Variance reduction, lines 39–41, against Design (Pre-registration and Estimation,
lines 18 and 20).

**Anchor:** "The unadjusted interval spans zero, as the power calculation anticipated. To
recover precision we applied CUPED"

**Problem:** The pre-registered estimation plan lists winsorization and a bootstrap but no
variance reduction, and CUPED is introduced narratively *in response to* the null unadjusted
result, which is estimator selection after seeing the outcome.

The Estimation bullet is specific about method — winsorization threshold, 10,000-resample
visitor-level bootstrap, rationale for not using a t-test — and CUPED appears nowhere in it.
The Pre-registration bullet covers horizon and peeking only. The document then says "We report
the adjusted estimate as primary," promoting an estimator that is not in the registered plan
and that is the only one producing significance. Whether or not CUPED was privately intended,
as written this reads as a post-hoc switch and inflates the false-positive rate beyond the
nominal 5%.

**Fix:** produce the pre-registration record. If CUPED was pre-specified, say so explicitly and
reorder the section so it does not read as a reaction to the null. If it was not, the
pre-registered result is +4.1%, p = 0.074, and that is the result.

### M6 — The 5% / 90-day holdback is underpowered for the re-read it is asked to perform

**Location:** Recommendation, item 3.

**Anchor:** "Hold back 5% of eligible traffic at $29 for 90 days; re-read RPV, retention, and
refunds"

**Problem:** A 95/5 split cannot detect the effect it is meant to confirm — its MDE is larger
than the effect — and for retention it is short by more than an order of magnitude.

**Re-derivation.** The 28-day test drew 122,683 visitors, so 90 days ≈ 394,300; a 5% holdback
is ~19,720 against ~374,600 treated. Precision scales with 1/n₁ + 1/n₂:

- Original test: 1/61,480 + 1/61,203 = 3.260 × 10⁻⁵
- Holdback design: 1/19,720 + 1/374,600 = 5.339 × 10⁻⁵
- Ratio 1.637 ⇒ SE inflated 1.28× ⇒ **MDE ≈ 6.4% × 1.28 = 8.2% relative RPV**

The effect to be confirmed is 5.3%. The holdback would fail to detect it at 80% power even if
it is entirely real, and a null re-read would be uninformative rather than reassuring.

Retention is worse. At ~3.2% conversion the holdback yields ~640 orders over 90 days; detecting
the observed 0.7pp difference on a ~94.5% base needs roughly 16,700 per arm — about 26× short.

**Fix:** size the holdback to the question. Roughly 20–25% held back for 90 days brings the RPV
MDE back near 5%; first-renewal retention needs either a longer window or acceptance that it
will only detect large degradations, stated as such.

---

## Minor

### m1 — The $24.4M base is computed from blended two-arm revenue, half of it at the test price

**Location:** Reconciliation, line 35.

**Anchor:** "the two arms produced $155,981 in first invoices over 28 days"

**Problem:** A base representing status-quo new-subscription value should not include the
treatment arm's $34 revenue; on control economics the figure is $153,208 × 13.04 × 12 = $23.97M,
so $24.4M overstates the $29 baseline by about 1.8%. Small, but it is the denominator of a
threshold test.

### m2 — The summary mixes an adjusted estimate with unadjusted ones without labelling it

**Location:** Summary, line 7.

**Anchor:** "Conversion fell 10.3% relative, average order value rose 16.0%, and revenue per
visitor (RPV) rose 5.3%"

**Problem:** Conversion and AOV are unadjusted while RPV is CUPED-adjusted, so the summary's own
three numbers do not reconcile — 0.897 × 1.1604 = 1.041, i.e. +4.1%, which is also what Table 1
shows. A reader who never reaches the Variance reduction section will not learn that the
pre-registered result was not significant. The section itself is transparent; the summary is not.

### m3 — The day-21 read on weeks 1–2 orders extends past the pre-registered analysis cut

**Location:** Guardrails, line 61, against Design line 18.

**Anchor:** "Day-21 retention (2,043 orders from weeks 1–2)"

**Problem:** Orders placed through 5 July reach day 21 on 26 July, seven days after the day-28
cut of 19 July that the design pins as a "single analysis ... no interim peeking." The memo
date of 28 July makes a later pull plausible, but the document never reconciles the two, so the
reader cannot tell whether the cohort is fully observed or truncated. State the pull date.

### m4 — Recommendation item 1 contradicts item 3

**Location:** Recommendation, items 1 and 3 (repeated in Summary, line 7).

**Anchor:** "Roll $34 to 100% of new self-serve Starter monthly purchases"

**Problem:** You cannot ship to 100% of new purchases and simultaneously hold 5% of eligible
traffic at $29; an implementer following item 1 literally destroys the holdback. Intent is
recoverable from reading both, but the actionable instruction should say 95%.

---

## Bottom line

The cell-level arithmetic in this memo is sound — conversions, AOVs, RPVs, both confidence
intervals, both p-values, the χ², the MDE and the 43% variance figure all reconcile. The
failures are structural and they run in one direction, toward the recommendation.

Two of them are decisive. The only statistically significant result in the document comes from
a CUPED adjustment built on covariates measured after assignment and downstream of the treatment
(C2); strip it and the pre-registered result is null at p = 0.074. And the financial case
multiplies a Starter-monthly-only lift by an all-plan base (C1); on the correct $24.4M base the
impact is ~$1.03M and **fails** the committee's $1.5M threshold under every assumption variant,
including the most generous. The memo's own disclaimer about not extending the lift to Team and
Business describes an analysis its arithmetic did not perform.

The supporting evidence is weaker than presented: 18% of the sample is absent from the segment
table and that block is −6.6% (M1), the guardrail that "matters most" stops nine days before the
first renewal it claims to rule out (M2), the revenue base assumes twelve renewals from
everyone (M4), and the holdback meant to catch all of this cannot detect the effect it is
checking (M6).

Recommended disposition: do not approve rollout on this readout. Return it for (a) CUPED on
pre-period covariates or a null finding, (b) total self-serve RPV across all four plans, (c) the
financial case against $24.4M with a real retention curve, (d) the complete segment table, and
(e) a holdback sized to its own question.
