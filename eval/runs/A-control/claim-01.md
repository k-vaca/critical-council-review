# Review: "Experiment readout: simplified signup form"

Artifact: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/claim-01-ab-test.md`
Reviewer pass: single expert pass, experimentation / applied statistics.

## Verdict

The readout requests a ship-to-100% decision. As written it does not support that decision.
The headline direction (B beats A on form completion) is probably real — the effect is large
relative to sampling noise even after correction — but three load-bearing claims in the
document are unsound: the p-value is invalid because of the stopping rule, the "no secondary
metric moved against us" statement is contradicted by the document's own numbers, and the
day-7 activation figure cannot have been measured for most of the cohort in a 9-day window.
The forecast is also materially overstated.

**What is sound** (stated so the findings below are read in proportion):
- Table arithmetic is correct: 1438/18204 = 7.90%, 1592/18061 = 8.81%.
- The split is balanced. 18,204 vs 18,061 against an expected 18,132.5 each is z ≈ 0.75,
  p ≈ 0.45 — no sample-ratio mismatch. The doc doesn't report this check, but it passes.
- The primary metric is explicitly defined, the decision requested is explicit, and the
  attribution trade-off is at least surfaced with a named stakeholder.

---

## Critical

### C1 — Stopped early on a peeked metric; the p-value is not interpretable as stated
**Location:** line 11, "Setup"
**Anchor:** "We monitored the dashboard daily and stopped on day 9, when the difference reached significance."
**Problem:** Testing repeatedly and stopping at the first crossing of α = 0.05 inflates the
false-positive rate well beyond 5% (roughly 15–20% for daily looks over this many days), so
the reported nominal p-value overstates the evidence and the reported effect size is
upward-biased by the stopping rule (you stop on a high draw — the winner's-curse effect).

Two consequences, and they matter differently:
- *For the ship decision:* the naive z here is ~3.15 (see M1), which would still clear a
  Pocock-style boundary for ~9 looks at α = 0.05. So the direction likely survives correction.
  The document has not earned the claim, but the claim is probably true.
- *For the forecast:* the point estimate of the lift is biased high, which propagates directly
  into the 1,850/month number (see M3). This is the part that does real damage.

**Fix:** state the sequential design actually used (alpha-spending / group-sequential boundary,
or an always-valid / mSPRT approach), report the boundary-adjusted p and a de-biased effect
estimate. If none was pre-specified, say so and treat the readout as directional.

### C2 — Day-7 activation cannot be measured for most of the cohort in a 9-day test
**Location:** line 24, "Secondary metrics"
**Anchor:** "Day-7 activation (created at least one project) was 31.2% for A and 29.8% for B. Not significant at n this size."
**Problem:** The test ran 14–22 July and stopped on day 9. Only users who signed up on or
before 15 July have had seven days to activate by the readout's cutoff — roughly the first
2 of 9 days, i.e. about 22% of the cohort. So the figure is either computed on ~320 and ~354
users per arm, or computed over the full cohort with most users not yet eligible to activate,
which censors both rates downward and makes them meaningless. The document never states the
denominators, so a reader cannot tell which.

This is decision-critical because of what the experiment therefore cannot rule out. On the
full-cohort denominators the 95% CI on the activation difference is about ±3.3pp; on the
~320/354 denominators it is about ±7pp. Converting to activated users per form view:

| | completion | day-7 activation | activated per view |
|---|---|---|---|
| A | 7.90% | 31.2% | 0.02465 |
| B | 8.81% | 29.8% | 0.02627 (+6.6%) |
| B at CI low end (~24%) | 8.81% | 24% | 0.02115 (−14%) |

The point estimate favours B even on activated users. But the experiment as run cannot
distinguish "B is +7% on activated users" from "B is −14%" — and −14% is exactly the failure
mode you would predict from removing qualifying fields (more signups, lower intent). That
analysis is the one the readout needed to do and did not.

**Fix:** wait for the full cohort to reach day 7, re-report activation with stated denominators,
and report activated-users-per-form-view (the business metric) with a CI, not just the
per-signup rate.

### C3 — The recommendation misstates the document's own data
**Location:** line 30, "Recommendation"
**Anchor:** "no secondary metric moved against us"
**Problem:** Both reported secondary metrics moved against B. Activation fell 31.2% → 29.8%
(−1.4pp, −4.5% relative) and `signup`-tagged support tickets rose 6 → 9 (0.42% → 0.57% per
signup, +35% relative). Neither is statistically distinguishable from noise, but "not
significant" is not "did not move against us," and with an underpowered secondary the
distinction is the whole point. A reader who skims to the Recommendation is told the opposite
of what the Results section shows.

**Fix:** state the observed direction and the width of the interval: "both secondaries moved
slightly against B; the test is not powered to detect a change of the size that would matter."

---

## Major

### M1 — Reported p-value does not match the reported test
**Location:** line 20, "Results"
**Anchor:** "Two-proportion z-test, p = 0.0038."
**Problem:** A two-proportion z-test on these counts gives p ≈ 0.0017, not 0.0038.

    pooled p = 3030/36265 = 0.083552
    SE       = sqrt(0.083552 × 0.916448 × (1/18204 + 1/18061)) = 0.0029062
    diff     = 0.088146 − 0.078994 = 0.0091521
    z        = 3.149   →  two-sided p ≈ 0.0016

Cross-check by chi-square on the 2×2 (1438/16766 vs 1592/16469): χ² = 9.87, 1 df, p ≈ 0.0017.
Continuity correction gives z = 3.13, p ≈ 0.0018. Nothing standard produces 0.0038.

The error is conservative — the true nominal p is smaller — so on its own it does not flip the
decision. It matters because it means the number was not reproduced or checked, which is the
same reason to distrust the other computed figures in the doc. If 0.0038 is in fact a
peeking-adjusted value, it is not labelled as one and the label says otherwise.

**Fix:** recompute and state which test, one- or two-sided, and whether adjusted.

### M2 — Analysis unit (form view) is not the randomization unit (visitor)
**Location:** line 9, "Setup"; applies to the whole Results section
**Anchor:** "Traffic split 50/50 on first visit, sticky by cookie. Primary metric: signup completion rate (completed signups ÷ form views)."
**Problem:** Randomization is per browser; the denominator is per view. Two independent
failures follow.

1. *Variance is understated.* Multiple views by the same visitor are correlated, so treating
   36,265 views as 36,265 independent Bernoulli trials makes the SE too small and the p-value
   anti-conservative. Note this pushes the opposite way from M1, so the two errors partially
   cancel and the net direction is unknown until both are fixed.
2. *The point estimate is biased.* A has four fields and therefore more validation failures,
   re-renders and abandon-retry loops, so A accrues more views per visitor than B. That
   inflates A's denominator relative to unique users and mechanically depresses A's completion
   rate. Some unknown share of the measured 11.6% "lift" is this artifact rather than more
   people signing up.

**Fix:** re-run the analysis with unique exposed visitors as the denominator, and use a
cluster-robust or delta-method variance if you keep any view-level metric.

### M3 — Monthly forecast is roughly 65% above what the data implies
**Location:** line 32, "Recommendation"
**Anchor:** "We expect this to add roughly 1,850 signups a month at current traffic."
**Problem:** Working from the readout's own numbers:

    total views over 9 days = 36,265  →  4,029/day  →  ~122,700/month (30.4 days)
    absolute lift           = 0.9152pp
    extra signups/month     = 122,700 × 0.009152 ≈ 1,120

Roughly 1,120, not 1,850. Nothing in the document supports the higher figure. Notably, the
95% CI on the absolute lift is [0.35pp, 1.48pp], which maps to [~420, ~1,820] signups/month —
1,850 is essentially the top of the interval presented as the expectation.

Two further reasons the honest number is below even 1,120: the lift point estimate is inflated
by the stopping rule (C1), and the 9-day window ran Tuesday 14 July to Wednesday 22 July, so it
contains two Tuesdays and two Wednesdays but only one of every other day — over-weighting
midweek traffic when annualizing.

**Fix:** forecast from the de-biased lift, show the interval, and state the traffic base used.

### M4 — The lift is a point estimate with no interval
**Location:** line 20, "Results"
**Anchor:** "Variant B improves completion by **11.5%**."
**Problem:** No confidence interval is given for the effect that the entire recommendation and
forecast rest on. The 95% CI on the relative lift is approximately +4.4% to +18.8%. "The
completion gain is large" (line 30) is defensible at the point estimate and not at the lower
bound, and the forecast is built on the point estimate as if it were known. A decision doc
that asks for a 100% rollout needs the interval on the page.

(Minor arithmetic note folded in here: 11.5% comes from dividing the rounded rates; from raw
counts it is 11.6%. Not material.)

### M5 — The cost of losing "company size" is never accounted for
**Location:** line 30, "Recommendation"
**Anchor:** "Removing the two fields costs us the self-reported attribution data, which marketing says they can live without for a quarter."
**Problem:** Two fields are removed but only one is costed. "Company size" is named in the
Setup as removed and then never mentioned again. It is the field most likely to feed lead
scoring, routing, segment assignment, or pricing-tier logic downstream — none of which is
checked here. The document also proposes a permanent 100% ship while the only sign-off
obtained ("can live without for a quarter") is time-boxed to a quarter, with no stated plan
for what happens at the end of it.

**Fix:** enumerate every downstream consumer of `company_size` and confirm each, and either
scope the ship to the quarter marketing signed off on or get an unbounded sign-off.

---

## Minor

### Mi1 — Relative lift presented without the absolute
**Location:** line 20, "Results"
**Anchor:** "improves completion by **11.5%**"
**Problem:** Bolded and unqualified, "11.5%" reads to many stakeholders as percentage points;
the absolute gain is 0.9pp and is never stated anywhere in the document.

### Mi2 — Support-ticket line is uninformative as presented
**Location:** line 26, "Secondary metrics"
**Anchor:** "Support tickets tagged `signup` were 6 for A and 9 for B over the period."
**Problem:** Raw counts with no exposure base, no rate, and no test, over a 9-day window that
is shorter than typical support-ticket lag — offered in a way that implies reassurance while
supporting no conclusion in either direction.

### Mi3 — No pre-registration or validity checks reported
**Location:** line 9, "Setup" (and line 11)
**Anchor:** "We planned for a two-week run."
**Problem:** No MDE, no power calculation and no pre-specified stopping rule are given, so
"we planned for two weeks" has no stated basis and the dismissal "not significant at n this
size" (line 24) is asserted rather than shown. No validity checks are reported either — SRM,
bot/duplicate filtering, or an A/A instrumentation check. (I ran the SRM check myself and it
passes; the point is that the reader should not have to.)

---

## What would make this shippable

1. Re-report the primary metric per unique exposed visitor, with a sequentially-adjusted p and
   a confidence interval on the lift.
2. Wait out the full day-7 window and report activated-users-per-view with an interval — this
   is the number the decision actually turns on.
3. Rebuild the forecast from the de-biased lift and show the range.
4. Correct the "no secondary metric moved against us" sentence.
5. Confirm no downstream system consumes `company_size`.

If 1–3 hold up, ship. The likely outcome is that B is genuinely better on completion and the
honest expected gain is somewhere near 1,000 signups a month rather than 1,850, with activation
the remaining open risk.
