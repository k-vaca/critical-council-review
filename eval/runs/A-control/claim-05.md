# Review — claim-05-capacity-forecast.md

**Reviewer pass:** single expert review, capacity planning / quantitative forecasting.
**Artifact:** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/claim-05-capacity-forecast.md`

## Verdict

This is a competent decision memo. It is scenario-based rather than a false point estimate, it names its assumptions, it states its own weaknesses honestly, and — importantly — the three headline numbers reproduce exactly from the stated inputs.

Checked and confirmed sound:

- **Horizon.** 31 Jul 2026 → 31 Oct 2027 is 15 months. The "15-month forecast" self-description in Known weaknesses is correct.
- **Low.** 1.31 × 1.22^1.25 = 1.680 → 1.68 PB. Correct.
- **Base.** 1.31 × 1.31^1.25 = 1.836 → 1.84 PB. Correct.
- **High.** 1.31 × 1.38^1.25 = 1.959, + 0.21 PB migrations = 2.169 → 2.17 PB. Correct.
- **Threshold fraction.** 2.17 / 2.5 = 86.8% → "87%". Correct.
- **Endpoint-only test is the right test.** Under monotone growth the endpoint is the maximum, so "high case ends at 2.17 PB" does establish "never crosses 2.5 PB during the term." The method is not under-specified here.
- **Data source choice.** Forecasting the billing export rather than the metrics API, because the billing export is what is charged, is the correct choice for a cost decision, and the memo says why.
- **Direction of the unmodelled risks.** Assumptions 1 and 2 (retention shortening, large-customer departure) both push storage *down*, so they can only strengthen the "do not commit" recommendation. Correctly noted rather than scenario'd.

The headline recommendation — do not commit to the larger tier — survives every defect below. The defects are in the sensitivity analysis and in two quantitative side-claims, not in the primary conclusion. No critical findings.

---

## Findings

### 1. MAJOR — "What would change this", line 46

> "Monthly deletion rate falling below 1%, which would push the base case to roughly 1.95 PB."

The 1.95 PB figure is inconsistent with the memo's own definition of the deletion rate by roughly a factor of six.

Assumption 4 (line 34) defines deletion as "2–4% of monthly writes." The base case is 31%/yr net = 2.28%/month net. If deletion is 3% of writes, gross writes are 2.28/0.97 = 2.35%/month of total. Dropping deletion from 3% to 1% of writes raises net growth by 0.047 pp/month, giving 1.31 × 1.02327^15 = **1.85 PB**, not 1.95 PB. Even the most generous variant (4% → 0%) only reaches 1.86 PB.

Reaching 1.95 PB would require net monthly growth to rise from 2.28% to 2.69% — an extra 0.41 pp/month, which is more than the entire gross write rate attributable to the deletion swing. The figure is not recoverable under the stated definition. (It is not recoverable under the alternative reading either: if deletion were 2–4% *of total stored bytes* per month, the same change would give ~2.46 PB, not 1.95 PB.)

This matters because this bullet is one of four triggers a recipient would use to set monitoring thresholds and gauge headroom. The sensitivity needs redoing.

### 2. MAJOR — Conclusion, line 38

> "which is 87% of the threshold — close enough that a third large migration would cross it."

Not supported by the memo's own migration sizing. Crossing requires 2.5 − 2.17 = **330 TB**. The two pending migrations are 210 TB *combined* (line 27), i.e. ~105 TB each. A third migration would therefore have to be roughly 3.1× the size of the contracted ones to cross the threshold.

As written, the sentence reads as "we are one ordinary enterprise migration away from the threshold," which is the line an executive is most likely to key on. On the document's own numbers the true headroom is about three migrations' worth. The error is conservative relative to the recommendation, but it could still push a reader to commit to the tier the memo is advising against. Either quantify ("a third migration above ~330 TB, three times the size of the pending two") or drop the claim.

### 3. MINOR — Method, line 25 and line 27

> "Growth returns to 38%/yr and the two pending enterprise migrations land in Q1"

The 210 TB is added as a flat quantity at the horizon and is not itself grown, so the stated Q1 landing date does no work in the model — the same 2.17 PB results whether the migration lands in month 1 or month 15. If 210 TB lands in Q1 and then participates in 38%/yr growth for the remaining ~10 months, the high case is ~2.23 PB (89% of threshold), not 2.17 PB (87%).

Not decision-changing, but the treatment is internally inconsistent: everything else compounds and this does not. Either compound it or state explicitly that the migration volume is held flat as a deliberate conservatism.

### 4. MINOR — Recommendation, line 40

> "Re-run this forecast in April 2027, when both pending migrations will have either landed or lapsed."

Contradicts line 27, "Neither has a confirmed date." Nothing in the memo establishes a contractual expiry or drop-dead date that would force resolution by April 2027. If no such date exists, the April re-run may be no better informed than today's, and the reader is left ~6 months from the next 1 November decision point with the same uncertainty. State the contractual basis for the April date, or pick the re-run trigger off something observable.

### 5. MINOR — line 9

> "the 2.5 PB threshold at which the next reserved tier becomes cheaper than on-demand"

This is the single decision rule for the entire memo and it is asserted with no source, no tier terms, no unit prices, and no break-even derivation. The memo contains no dollar figures anywhere. The asymmetry is conspicuous given how carefully the byte data is sourced two sections later (billing export vs metrics API, with a stated reason for the choice). A reviewer cannot check whether 2.5 PB is the right break-even, or whether the break-even is even a single volume rather than a function of commit term and discount depth.

### 6. MINOR — "What would change this", line 44

> "Either pending migration landing at more than 350 TB rather than the contracted 210 TB combined."

Scope mismatch: a per-migration figure (350 TB) is compared against a combined figure (210 TB). It is ambiguous whether the trigger fires when one migration exceeds 350 TB, or when the pair does. The two readings imply very different monitoring. Restate both sides on the same basis.

### 7. MINOR — "What would change this", line 47

> "diverging by more than 5%, which would mean one of them is wrong and the baseline is unreliable"

Two slips. First, line 13 already establishes the two disagree by 1–3% every month, so one of them is *already* wrong — divergence is evidence of magnitude, not of a newly appearing error. Second, the memo's own justification for using the billing export is that it "is the figure we are charged on." If that is true, the billing export is definitionally the correct baseline for a cost decision, and metrics-API drift does not make it unreliable. As drafted this bullet undercuts the data-selection rationale it is meant to protect.

### 8. MINOR — line 23, line 25, line 40, and title

Mixed fiscal and calendar references, none of them defined. The title says "FY27"; the deadline is "the 1 November deadline" with no year; the high scenario says "Q1" with no year or basis; the low scenario and the recommendation use calendar months ("since March", "April 2027"). If FY27 runs 1 Nov 2026 – 31 Oct 2027, fiscal Q1 is Nov–Jan, whereas calendar Q1 2027 is Jan–Mar. In a memo whose every other date is explicit, this is worth fixing — particularly since migration timing is one of the few dated inputs.

### 9. MINOR — line 23 and line 51

The underlying 24-month series is not included, so two stated figures cannot be checked by the recipient:

> "Growth decays to 22%/yr, matching the slowdown in new-account creation since March"

The 22% is the only scenario rate not tied to a computed figure — Base uses the stated trailing-6-month rate and High uses the stated trailing-12-month rate, but 22% is asserted. "Matching the slowdown in new-account creation" is not quantified, and new-account creation is not a bytes metric; the linkage between the two is not shown. Similarly, the 1.71 PB linear fit in Known weaknesses (line 51) cannot be reproduced without the monthly points. Attach the series or the fit parameters.

---

## Not defects (checked, deliberately not raised)

- Stacking two independent upside events in the high scenario is standard scenario construction, not double-counting.
- Absence of probability weights on the three scenarios is conventional practice for a scenario memo and is compatible with the stated "moderate" confidence.
- "Invalidate all three scenarios" for a retention change (line 31) is strong wording, but the underlying point — a 340 TB step change off a 1.31 PB base is 26% of stock and breaks the growth-only model — is correct.
- The Known-weaknesses framing of the migration assumption as resting on "a single prior observation" is consistent with the contracted 210 TB: the contract fixes the size, the n=1 history is what informs whether contracted TB become stored TB.
