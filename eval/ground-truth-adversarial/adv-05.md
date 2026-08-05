# Ground truth — adv-05-pricing-test.md

Artifact: `artifacts-adversarial/adv-05-pricing-test.md`
Planted defects: 3 (1 critical, 2 major). Everything else in the memo is deliberately sound and internally consistent; any other "finding" is a false positive.

---

## Defect 1 — Financial projection applied to the wrong revenue base

- **Severity**: critical

- **Location**: "Financial impact" section, first sentence. Governing figures are in "Background" (paragraph 1) and in the reconciliation italic line under Table 1.

- **The defect**: The +5.3% RPV lift is multiplied by **$68.2M**, which the Background paragraph explicitly defines as the base for **all four self-serve plans** (Starter monthly, Starter annual, Team, Business). The price test touched **only Starter monthly**, whose base the same paragraph gives as **$24.4M**. The lift is applied to a base ~2.8× larger than the population that was actually repriced. The projected +$2.89M should be ≈ +$1.03M, which falls **below** the $1.5M committee threshold the memo claims the result clears. A reviewer should say: the impact number uses the all-plans base instead of the Starter-monthly base, and the recommendation's stated justification collapses when corrected.

- **Why it is real**:
  - Memo's arithmetic, internally correct: $68.2M × 5.3% = $3.6146M; × 0.8 (novelty haircut) = **$2.892M** → "+$2.89M" as printed.
  - Correct base: $24.4M × 5.3% = $1.2932M; × 0.8 = **$1.0346M** → **+$1.03M**.
  - Overstatement factor: 68.2 / 24.4 = **2.795×**.
  - The threshold is stated in the same sentence: $1.5M. $2.89M clears it; $1.03M does not. So a recipient approving the rollout on the stated business case is acting on a number that is wrong by 2.8× and that inverts the go/no-go test.
  - The $24.4M base is independently confirmed by the memo's own reconciliation line: $155,981 × (365/28) = $2.0333M annualized first invoices; × 12 = $24.40M. That line ties the test's own dollars to the Starter-monthly base and nothing else.
  - The Design section additionally confirms scope: "only the price on the Starter monthly card differed between arms."
  - The same sentence contains a direct self-contradiction: "We have not extended the lift to Team or Business, which were untouched" — but Team and Business are inside the $68.2M base by the Background definition.

- **Why I expect a reviewer to miss it**: The multiplication itself is arithmetically correct and the haircut is conservative, so a reviewer verifying the math ticks the line off and moves on; the trailing sentence disclaiming Team and Business reads as scope discipline already exercised, which actively suppresses the check it fails. The two base figures sit ~500 words upstream in a Background paragraph that reads as throat-clearing, and the word "self-serve" appears in both the test description and the base label, so the shorthand "self-serve test → self-serve base" feels right.

---

## Defect 2 — CUPED adjustment uses covariates measured during the experiment

- **Severity**: major

- **Location**: "Variance reduction" section.

- **The defect**: CUPED is applied using "sessions per visitor and pricing-page views per visitor" explicitly described as **measured over the experiment window**. CUPED requires covariates measured **pre-experiment** and unaffected by treatment. Both covariates here are post-randomization outcomes that a price change plausibly moves (a higher price changes how much people shop and re-visit the pricing page). Conditioning on them biases the treatment effect estimate rather than merely reducing its variance. The memo then designates this biased estimate as primary and it is the estimate carried into the recommendation and the financial projection.

- **Why it is real**:
  - Post-treatment variables are colliders/mediators on the causal path from price to purchase; adjusting for them is textbook post-treatment bias. This is not a judgment call — CUPED's validity condition is that the covariate is independent of assignment by construction, which only pre-period data guarantees.
  - The adjustment is consequential, not cosmetic: it moves the estimate from **+4.1% (95% CI −0.4% to +8.6%, p = 0.074)** to **+5.3% (95% CI +1.9% to +8.7%, p = 0.002)** — both printed in the artifact. A valid CUPED adjustment shrinks the interval around roughly the same point estimate; here the point estimate itself moves by 1.2pp, which is the fingerprint of the covariate carrying treatment effect. Statistical significance exists only after the invalid adjustment.
  - The memo's own defense is the tell: it reports the covariates are "balanced between arms (sessions per visitor 2.41 control vs 2.38 treatment, p = 0.19)." A balance test on a post-treatment variable establishes nothing about its validity as a CUPED covariate, and the −1.2% direction is exactly what treatment-affected browsing would look like at this sample size.
  - Correctly analyzed (unadjusted, or CUPED on genuine pre-period spend), the headline is +4.1% with p = 0.074 — the memo's own numbers show the result is not statistically established at the pre-registered horizon.

- **Why I expect a reviewer to miss it**: Naming CUPED reads as sophistication and reviewers pattern-match "variance reduction = good practice, they went beyond the basics"; the accompanying balance check looks like the author already stress-tested the choice, so the reviewer credits rigor instead of reading the covariate definition. The critical words — "measured over the experiment window" — are a subordinate clause in a sentence whose payload appears to be the 43% variance reduction.

---

## Defect 3 — Segment table omits ~18% of the sample and hides a losing group

- **Severity**: major

- **Location**: Table 2 and the sentence immediately above it ("the rows below partition the sample"), read against Table 1.

- **The defect**: Table 2 claims to partition the sample across three first-touch acquisition sources. It does not. The three rows account for only **82%** of visitors, orders, and revenue. The residual ~18% of traffic — never named, never shown — has a **negative** RPV effect of about **−6.6%**, which falsifies the memo's claim that "the lift is positive in every source, so the result is not one segment carrying the average," and means a 100% rollout knowingly loses money on roughly one visitor in five.

- **Why it is real** (all figures printed in Tables 1 and 2):
  - **Visitors.** Control: 26,417 + 17,142 + 6,834 = 50,393 vs Table 1 total 61,480 → **11,087 missing (18.0%)**. Treatment: 26,298 + 17,090 + 6,791 = 50,179 vs 61,203 → **11,024 missing (18.0%)**.
  - **Orders.** Control: 1,043 + 512 + 253 = 1,808 vs 2,214 → **406 missing**. Treatment: 952 + 476 + 220 = 1,648 vs 1,977 → **329 missing**.
  - **Revenue** (orders × AOV). Control: $36,713.60 + $16,947.20 + $9,209.20 = $62,870.00 vs $76,604 → **$13,734 missing**. Treatment: $38,936.80 + $18,373.60 + $9,306.00 = $66,616.40 vs $79,377 → **$12,760 missing**.
  - **Omitted group's RPV.** Control $13,734.40 / 11,087 = **$1.2388**. Treatment $12,760.15 / 11,024 = **$1.1575**. Lift = **−6.6%**. Its conversion falls 3.662% → 2.984%, a 18.5% relative drop, roughly double the drop in any shown segment.
  - **Cross-check.** The three shown rows aggregate to a +6.4% RPV lift, versus +4.1% overall in Table 1. A partition's weighted average must equal the total; it does not, which is itself proof the table is not a partition.
  - The exhaustiveness claim is stated flatly in the memo ("Every visitor is assigned exactly one source at first touch, so the rows below partition the sample"), so this cannot be defended as a disclosed subset.

- **Why I expect a reviewer to miss it**: Reviewers read segment tables for *pattern* ("all positive, no Simpson's paradox, good") rather than for *closure*, and the row-level arithmetic is all correct, so spot-checking any single row passes. The shown lifts (+1.7%, +6.5%, +8.7%) deliberately straddle the +4.1% headline, so the "weighted average must lie inside the range of its parts" shortcut does not fire — catching this requires actually summing three visitor columns and differencing them against Table 1, which few reviewers do when the rows are labeled as a partition and the segment counts are non-round.

---

## Deliberately sound — do not credit as findings

Verified correct and internally consistent; flagging these is a false positive:

- Table 1 arithmetic: 2,214 × $34.60 = $76,604.40; 1,977 × $40.15 = $79,376.55; RPV $1.2460 and $1.2969; lift +4.088% → +4.1%.
- Conversion 3.601% → 3.230% = −10.30% relative; AOV +16.04%; (1 − 0.1030)(1 + 0.1604) = 1.0409, ties to the RPV lift.
- Seats per order: $34.60/$29 = 1.193; $40.15/$34 = 1.181 → "1.19 → 1.18" as stated.
- Elasticity: −10.30% / +17.24% = −0.597 → −0.6 as stated, with the derivation shown on the page.
- SRM: 61,480 / 61,203 = 50.11% / 49.89%; χ² = 0.625, p = 0.43. Genuinely no mismatch.
- Interval/p-value coherence: +4.1% ± 4.5pp → SE 2.296, p = 0.074. +5.3% ± 3.4pp → SE 1.735, p = 0.002. Variance reduction 1 − (1.735/2.296)² = 43%, exactly as claimed. MDE at 80% power = 2.8 × 2.296 = 6.4%, as claimed.
- Reconciliation line: $155,981 × 365/28 = $2.0333M; × 12 = $24.40M.
- Every Table 2 row is internally correct (orders × AOV / visitors = printed RPV; printed lift matches).
- Run length (4 full weekly cycles), release freeze, sticky randomization preventing price-switching, winsorization at a pooled pre-period threshold applied identically to both arms, bootstrap rather than t-test on skewed revenue, fixed horizon with no peeking, no multiplicity claim on segments, grandfathering, and the 5% 90-day holdback are all correct practice and are pre-empted on purpose.
- The 28-day churn limitation and the single-price-point elasticity caveat are disclosed by the author in "Limitations"; raising them as defects is a false positive.
