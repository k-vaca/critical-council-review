# Critical Council Review — "Experiment readout: simplified signup form"

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

---

## 1. Verdict

**Revise substantially before use.** The headline 11.5% gain is on a proxy metric the change mechanically inflates; on the artifact's own numbers the downstream metric that matters — activated users per form view — is 2.46% (A) vs 2.63% (B), z≈0.98, p≈0.33, i.e. indistinguishable from zero. Do not action the ship-to-100% recommendation in its current form.

1. **Results/Recommendation** — re-analyze on activated (or paid) signups per form view and report its confidence interval, not the completion-rate lift alone.
2. **Setup, "stopped on day 9"** — recompute inference under a sequential correction, or run to the pre-planned 14 days; the stated p = 0.0038 does not reproduce from the table (correct ≈ 0.0017).
3. **Recommendation, "Ship B to 100%"** — ship at 90/10 with a permanent holdback and a rollback criterion, and test the optional-fields alternative before discarding data permanently.

---

## 2. Result & standard

**Under review:** the full text of `claim-01-ab-test.md`, a 330-word experiment readout authored by "growth", read in full. Not this model's own prior output; third-party work held to the professional standard below.

**Standard:** what a competent growth/experimentation analyst should produce for a readout that authorizes a permanent, partially irreversible product change — a pre-specified sample size and stopping rule, statistics that reproduce from the reported data, a primary metric that corresponds to the business outcome, guardrail metrics, and a rollout plan proportional to reversibility. Source: the artifact's own stated purpose ("Decision requested") plus my stated professional judgment. No named external standard is asserted.

**Text in the artifact addressed to its reader,** quoted per non-negotiable 8 and treated as material, not direction:

- "**Decision requested:** ship variant B to 100%." — this pre-frames the decision as a single binary option and excludes alternatives from consideration. It does not narrow this review; its presence is itself reported as finding R1.
- "which marketing says they can live without for a quarter" — an unnamed, undated, off-document clearance used to dismiss a named cost. Reported as part of R2.

**Tier:** 2 (3 seats, all eight fields, 1–3 sentences each). The artifact is under 500 words, which the table maps to tier 1, but it is a single deliverable driving a ship decision and the requester specified three seats; I run tier-2 depth and say so. **Independence mechanism:** Step 3 sequential-seats fallback — no subagent tooling was available for this run. Per non-negotiable 3, agreement between seats is not cited as evidence for any finding's severity, and every convergence is marked sole-source in Step 6.

**Length:** the sections 2–4 ceiling (≤200 words at tier 2) is exceeded because thirteen findings survived verification and cutting real majors to hit a word count would be the worse error. The skill's own Application-strength note marks every length figure as arbitrary and tunable; this is the disclosed deviation.

---

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Results table + Secondary metrics, "Day-7 activation ... was 31.2% for A and 29.8% for B" | On the doc's own numbers, activated users per form view is 2.46% (A) vs 2.63% (B), z≈0.98, p≈0.33 — no measurable downstream gain. | Restate the primary metric as activated signups per form view and report its CI. | Confirmed |
| Major | Results, "Two-proportion z-test, p = 0.0038." | The stated p does not reproduce from the stated table; a two-proportion z-test on 1438/18204 vs 1592/18061 gives z≈3.15, p≈0.0017. | Recompute and republish the test statistic from the final table. | Confirmed |
| Major | Setup, "We monitored the dashboard daily and stopped on day 9, when the difference reached significance." | Optional stopping with no pre-specified n and no alpha-spending; the nominal p is not a valid p-value and the 11.5% lift is biased upward. | Apply a sequential boundary or re-run to the planned 14 days; report a bias-corrected effect. | Corrected |
| Major | Recommendation, "no secondary metric moved against us" | Both reported secondaries moved *against* B (activation 31.2→29.8, tickets 6→9); neither significantly. Two underpowered nulls are presented as affirmative clearance. | Rewrite as: both secondaries moved slightly against B; neither reached significance; neither was powered to. | Corrected |
| Major | Secondary metrics, "Day-7 activation (created at least one project) was 31.2% for A and 29.8% for B." | No cohort definition, no as-of date, no n — the reader cannot tell whether all 3,030 signups have a mature 7-day window or only early cohorts. | State the activation cohort, the as-of date, the n per arm, and the CI on the difference. | Corrected |
| Major | Recommendation, "We expect this to add roughly 1,850 signups a month at current traffic." | Not reproducible: 36,265 views ÷ 9 days × 30 × 0.92pp absolute lift ≈ 1,100 extra signups/month; the stated figure is ~67% higher. | Recompute from observed traffic and the bias-corrected lift; state the traffic base used. | Confirmed |
| Major | Results table vs Secondary metrics | Backing out B's 154 extra signups implies they activate at ~17% vs ~31% for the base — roughly half. No signup-quality guardrail (email verification, bot screen, paid conversion) is reported. | Segment the marginal cohort by activation and verification rate before shipping. | Corrected |
| Major | Recommendation, "Removing the two fields costs us the self-reported attribution data" | Two fields are removed but only one field's cost is accounted for; nothing states what consumed "company size". | Enumerate downstream consumers of company size (routing, scoring, segmentation) and sign each off. | Confirmed |
| Major | Recommendation section (alternatives absent) | The dominating alternative — making the fields optional or capturing them post-signup — is never considered; the doc frames the choice as binary. | Test progressive profiling as variant C before discarding the fields permanently. | Confirmed |
| Major | Recommendation, "which marketing says they can live without for a quarter" | A one-quarter, off-document verbal concession is used to authorize a permanent ship with no sunset, revisit trigger, or owner. | Add an explicit revisit date matching the quarter, with a named owner and a decision record. | Confirmed |
| Major | Recommendation, "Ship B to 100%." | Shipping to 100% forfeits the holdback; no rollback criteria, no guardrail monitoring, no day-30 or paid-conversion check. Form-field data cannot be backfilled. | Ship 90/10 with a permanent holdback and pre-declared rollback thresholds. | Confirmed |
| Minor | Setup, "completed signups ÷ form views" + "sticky by cookie" | Analysis unit (views) is not reconciled to the randomization unit (cookie); no user counts are given, so the z-test's independence assumption cannot be verified. | Report randomized-user counts and analyze per user. | Unverified |
| Minor | Secondary metrics, "Not significant at n this size." | No n and no interval are given; the claim is true (recomputed z≈0.84, p≈0.40) but unsupported as written. | State n, the observed difference, and its CI. | Confirmed |

**Totals:** critical 1 · major 10 · minor 2. **Withdrawn at Step 5:** 3.

---

## 4. Council roster

Three seats, specified by the requester — disclosed per Step 2 as a fact, not honored as a constraint. The seats were derived against this artifact's specific failure modes (a stopped-early test, a proxy primary metric, a permanent irreversible ship).

1. **Methodology & statistics** — owns design, power, stopping rule, and whether the reported statistics follow from the reported data. Belongs because the artifact's entire claim rests on one significance test.
2. **Data & inference validity** — owns sampling, confounds, measurement, and whether the conclusion follows from the data shown. Belongs because the primary and secondary metrics point in opposite directions.
3. **Decision red-team** — owns whether the recommendation survives contact with reality. Belongs as the mandated skeptic and as the proxy for whoever lives with the rollout.

Each seat was given the full roster (names and remits only, no findings) and told that another seat owning a topic is not a reason to skip something it can see.

**Deliberately not covered.** The requester's roster forbids adding seats, so the verdict is capped rather than extended, per Step 2:

- **Engineering / instrumentation** — nobody could inspect whether the "form view" event fires under identical conditions on both variants. A variant-specific denominator bug would produce exactly this result and would be a **critical** defect. The verdict does not cover this domain and a defect there would change it.
- **Data governance / downstream consumers** of the removed fields — a major-or-worse defect could live here (see the company-size finding).
- **Fraud & abuse** — no seat could examine signup-quality logs; a critical defect could live here.

---

## 5. Individual analyses

### Seat 1 — Methodology & statistics

**Role & remit.** Experimentation statistician. Judges design, power, stopping rule, and whether the reported numbers support what is claimed.

**Standard applied, and where it comes from.** An online controlled experiment is credible when the sample size or stopping rule is fixed in advance, the analysis unit matches the randomization unit, and every reported statistic reproduces from the reported data. This is my stated professional judgment, not a citation; no named standard is asserted.

**Assessment.** The experiment was executed cleanly but analyzed loosely. The split is balanced, the metric is defined, and the test is named — which is precisely why the analysis is checkable, and it does not check out.

**Strengths.** No sample ratio mismatch: 18,204 vs 18,061 against a 50/50 split is chi-square ≈ 0.56, p ≈ 0.45 — the assignment mechanism looks sound. The primary metric's denominator is explicitly stated ("completed signups ÷ form views"), which many readouts omit. Randomization is concurrent, so seasonality and day-of-week cannot confound the A/B comparison itself.

**Weaknesses, risks & errors.**
- **Major, defect** — the headline statistic does not reproduce. Anchor: "Two-proportion z-test, p = 0.0038." (Results). Pooled p̂ = 3030/36265 = 0.08355, SE = 0.002906, z = 3.149, two-sided p ≈ 0.0017. Unpooled and Yates-corrected variants give 0.0016–0.0018; no standard two-proportion test yields 0.0038. The error runs *conservative*, so it does not weaken the significance claim — but a reader cannot reproduce the doc's own number from the doc's own table. *Inference, labelled as such:* p = 0.0038 corresponds to about 84% of the reported sample, i.e. roughly the day-8 data — consistent with a p captured at the look that triggered the stop while the table reports day 9. That reconstruction is inference, not fact.
- **Major, defect** — optional stopping. Anchor: "We monitored the dashboard daily and stopped on day 9, when the difference reached significance." (Setup). Daily looks with no pre-registered sequential design mean the nominal p is not a valid p-value, and stopping at the moment of significance biases the effect estimate upward, so 11.5% overstates the true lift. The design statement is a duration, not a target: "We planned for a two-week run." No MDE, no power calculation, no pre-specified n appears anywhere in Setup.
- **Minor** — analysis unit vs randomization unit. Anchors: "completed signups ÷ form views" and "sticky by cookie" (Setup). Assignment is per cookie; analysis is per view. If any user views the form more than once, those trials are correlated and the variance is understated. No user counts are reported, so this cannot be verified either way.
- **Minor** — "Not significant at n this size." (Secondary metrics) gives neither n nor an interval. Recomputed at n = 1,438/1,592 the claim is true (z ≈ 0.84, p ≈ 0.40) — but it is unsupported as written, and a bare "not significant" invites the reader to hear "no effect."

**Gaps.** No confidence interval on the primary effect; no absolute lift stated (0.92 percentage points); no MDE; no per-user counts; no statement of how many looks were taken.

**Strongest reason this might be fundamentally wrong.** The statistics may be immaculate and still irrelevant: removing two fields raises form-completion rate close to mechanically, so rigor applied to that metric cannot establish the business claim. Note the overlap — quantifying this sits in Seat 2's remit, and I report it because I can see it.

**Domain verdict.** Below the bar for a readout authorizing a permanent change. The *direction* of the primary-metric effect is probably real — z ≈ 3.15 leaves margin to survive a sequential correction — but the reported p is invalid, the magnitude is inflated, and one stated number does not reconcile with the table above it.

**Recommended fixes.** (1) Recompute the test from the final table and publish the corrected p. (2) Apply an alpha-spending boundary or re-run to 14 days. (3) Report absolute lift with a CI, not only relative lift. (4) Report randomized-user counts and analyze per user. (5) State the MDE the design could detect.

---

### Seat 2 — Data & inference validity

**Role & remit.** Analytics reviewer. Judges sampling, confounds, measurement definitions, and whether the stated conclusion follows from the data shown.

**Standard applied, and where it comes from.** A conclusion must follow from the quantity actually measured; the measured quantity must correspond to the business outcome being claimed; and prose summaries must not contradict the tables above them. My stated judgment, applied against the artifact's own stated purpose.

**Assessment.** The data collection looks sound and the reporting is honest — including where it hurts. The *inference* is where it fails: the doc measures a proxy, observes that the one downstream signal disagrees, and reports the disagreement as clearance.

**Strengths.** The secondary metrics that cut against the recommendation are reported rather than suppressed — both the activation dip and the ticket increase are on the page. The known cost of the change is named. The 9-day run reconciles exactly with the stated dates (14–22 July inclusive).

**Weaknesses, risks & errors.**
- **Critical, defect** — the decision metric shows nothing. Anchors: the Results table and "Day-7 activation (created at least one project) was 31.2% for A and 29.8% for B." (Secondary metrics). Composing them gives activated users per form view: A = 1,438 × 0.312 ÷ 18,204 = 2.465%; B = 1,592 × 0.298 ÷ 18,061 = 2.627%. Two-proportion test: z ≈ 0.98, p ≈ 0.33. The 95% interval on the relative difference spans roughly −7% to +20%. The purpose from Step 1 — justifying a permanent ship on the strength of a measured gain — is undermined: the artifact's own data does not establish a downstream gain at all.
- **Major, defect** — the sentence carrying the recommendation misstates the evidence above it. Anchor: "no secondary metric moved against us" (Recommendation). Activation moved from 31.2% to 29.8% and signup tickets from 6 to 9. Both moved against B. Neither significantly — but "did not move against us" and "moved against us without reaching significance" are different claims, and only the second is true.
- **Major, gap** — the activation figure has no denominator. Anchor: the Day-7 activation sentence. There is no cohort definition, no as-of date, and no n. If computed as of the 22 July stop, only the earliest signup cohorts have a mature 7-day window and the effective n is a fraction of 3,030, which would widen the interval far enough for the composite above to go clearly negative. If computed later, it is mature. The document does not let the reader tell which.
- **Major, defect** — the forecast does not reconstruct. Anchor: "We expect this to add roughly 1,850 signups a month at current traffic." (Recommendation). 36,265 views over 9 days is 4,029/day; a 30-day month is ~120,900 views; at the observed 0.92pp absolute lift that is ~1,100 extra signups, not 1,850. Reaching 1,850 requires about 67% more traffic than the test observed, a figure that appears nowhere in the document. *Assumption named:* that test-period traffic represents "current traffic" — the doc supplies no other traffic base.
- **Major, defect** — the gain is concentrated in low-activating signups. Holding the base population's 31.2% activation constant, B's 154 marginal signups must activate at ~17% to produce B's observed 29.8% — roughly half the base rate. *Assumption named:* this decomposition assumes the non-marginal population is unchanged across arms, which the data cannot confirm.
- **Major, gap** — one of the two deleted fields is never costed. Anchor: "Removing the two fields costs us the self-reported attribution data" (Recommendation). The sentence removes two fields and accounts for one. Nothing states what consumed "company size."

**Gaps.** No definition of "form view"; no signup-quality measure (email verification, paid conversion); no segmentation of the marginal cohort; no interval on any secondary metric.

**Strongest reason this might be fundamentally wrong.** The readout may be measuring the wrong thing while the right thing shows nothing. If activated signups per view is the objective, this is a null result presented as an 11.5% win — and the recommendation inverts the evidence rather than merely overstating it.

**Domain verdict.** The conclusion does not follow from the data shown. The primary-metric result is probably real; the business claim built on it is not supported by anything in the document.

**Recommended fixes.** (1) Make activated (or paid) signups per form view the primary metric and report its CI. (2) State the activation cohort, as-of date, and n per arm. (3) Recompute the monthly forecast and name the traffic base. (4) Segment the 154 marginal signups by activation and verification. (5) Rewrite the "no secondary metric moved against us" sentence to match the table.

---

### Seat 3 — Decision red-team

**Role & remit.** Adversarial reviewer of the recommendation, and proxy for whoever operates the result. Judges whether "ship B to 100%" survives contact with reality and states the strongest case against acting.

**Standard applied, and where it comes from.** A ship recommendation must beat the obvious alternatives, state its reversibility honestly, and carry monitoring and rollback proportional to what cannot be undone. My stated judgment.

**Assessment.** The recommendation is probably not wrong in *direction*, but it is unsafe in *form*: it is the most irreversible version of the change, chosen without comparison, with no way to detect being wrong afterwards.

**Strengths.** The requested decision is explicit and unambiguous rather than buried. A named cost is disclosed rather than hidden. A quantified forecast is offered, which makes the claim falsifiable after the fact.

**Weaknesses, risks & errors.**
- **Major, defect** — the dominating alternative is never considered. Anchor: "**Decision requested:** ship variant B to 100%." (header) and the Recommendation section, where alternatives would appear and do not. Making the two fields optional, or capturing them post-signup during onboarding, plausibly captures the friction reduction *and* keeps the data. The doc presents a binary where a third option beats both on both axes. Severity held at major, not critical: the ship is not wrong in direction and a recipient can still act coherently — they simply take an avoidable loss.
- **Major, defect** — presented as reversible; partly is not. Anchor: "which marketing says they can live without for a quarter" (Recommendation). The form can be restored tomorrow; company-size and attribution data for everyone who signs up in the interim can never be backfilled. And a concession explicitly bounded at one quarter is being used to authorize a permanent ship with no sunset date, no revisit trigger, and no named owner. The clearance is also unverifiable as recorded — unnamed person, undated, off-document.
- **Major, gap** — 100% forfeits the ability to detect being wrong. Anchor: "Ship B to 100%." (Recommendation). No holdback, no guardrail thresholds, no rollback criteria, no day-30 retention or paid-conversion check. Once at 100% with no holdout, a delayed regression is invisible: there is nothing left to compare against.
- **Major, gap** — signup quality is never measured. The observed pattern — more signups, lower activation, more support tickets — is equally consistent with a genuine friction win and with an influx of low-intent or automated signups, and the document reports nothing that could separate them (no email-verification rate, no bot screen, no paid conversion). Shortening a signup form is a recognized abuse surface; I state that as professional judgment, not as a claim that abuse occurred here.

**Gaps.** No rollback plan, no monitoring window, no owner, no revisit date, no success criteria for the post-ship period, no consideration of who else consumes the deleted fields.

**Strongest reason this might be fundamentally wrong.** If the marginal signups are low-intent or automated, B does not merely fail to help — it adds support load and pollutes the funnel while destroying the two fields you would need to diagnose it. The doc would then be recommending a change that is self-concealing.

**Domain verdict.** Do not ship as proposed. The direction may well be right; the form of the rollout is unsafe and the alternative that dominates it was never tested.

**Recommended fixes.** (1) Ship at 90/10 with a permanent holdback. (2) Run progressive profiling as variant C before discarding fields. (3) Define rollback thresholds and a revisit date matching the quarter marketing agreed to, with a named owner. (4) Add email-verification rate and paid conversion as guardrails. (5) Re-baseline the forecast before it is quoted onward into planning.

---

## Step 5 — Verification pass

Every critical and major finding was re-checked against the artifact adversarially — asking what would make it false — and each quoted string was searched in the source rather than recalled.

**Strings located and confirmed present, verbatim:** "Two-proportion z-test, p = 0.0038." (Results) · "We monitored the dashboard daily and stopped on day 9, when the difference reached significance." (Setup) · "We planned for a two-week run." (Setup) · "completed signups ÷ form views" and "sticky by cookie" (Setup) · "Day-7 activation (created at least one project) was 31.2% for A and 29.8% for B." and "Not significant at n this size." (Secondary metrics) · "no secondary metric moved against us" · "Removing the two fields costs us the self-reported attribution data, which marketing says they can live without for a quarter." · "We expect this to add roughly 1,850 signups a month at current traffic." · "Ship B to 100%." (Recommendation) · "**Decision requested:** ship variant B to 100%." (header). Absence findings were anchored to the section where the missing content belongs.

**Arithmetic re-derived from the table, not recalled:** 1438/18204 = 7.899% and 1592/18061 = 8.815%, matching the doc's 7.90% and 8.81%. Composite activation-per-view robustness-checked at the rounding extremes of the 31.2/29.8 figures; z stays below 1.05 in every case, so the critical finding does not depend on rounding. The 9-day run reconciles with the stated dates.

**Corrected (6)** — narrowed to what the evidence supports:
1. *Optional stopping* — originally implied significance itself might not hold. Narrowed: at true p ≈ 0.0017 the primary-metric direction most likely survives a sequential correction; what is invalid is the nominal p and the magnitude, which is biased upward.
2. *"no secondary metric moved against us"* — narrowed from "factually false" to "materially misleading as written," since a charitable reading of "moved against us" as "moved significantly" is available.
3. *Activation cohort* — narrowed from "the data is censored" to "no as-of date, cohort, or n is given, so the reader cannot tell." Censoring cannot be established; the run ended 22 July and the readout may postdate maturity.
4. *Analysis unit vs randomization unit* — narrowed and **downgraded to minor**: the doc reports no user counts, so an independence violation is unverifiable rather than demonstrated.
5. *Marginal signup quality* — narrowed to one arithmetically consistent reading, with its assumption (unchanged base population) stated on the face of the finding.
6. *Abuse/bot vector* — narrowed from "bots are the likely explanation" to "no signup-quality guardrail exists, so the doc cannot distinguish the two explanations." Merged with finding 5.

**Withdrawn (3)** — dropped entirely, with the producing seat named:
1. **Seat 2** — a day-of-week composition objection (the 9-day window double-counts two midweek days). Withdrawn: it rests on a weekday derived by calculation rather than looked up, and even if correct it cannot bias the A/B comparison, since randomization is concurrent. Its only real effect is on the monthly extrapolation, where it is subsumed by the forecast finding.
2. **Seat 1** — the reported 11.5% lift versus the 11.59% computed from unrounded rates. Withdrawn: this is a 0.1pp rounding artifact of dividing the rounded percentages, not a defect. Reporting it would be manufacturing a problem.
3. **Seat 3** — the observation that the owning team's incentives favor the chosen metric. Withdrawn: it rests on an assumed norm about how growth teams are measured that I cannot state precisely or defend from the artifact, and non-negotiable 6 forbids asserting it.

**Reliability.** No seat misquoted the artifact and no finding rested on text not present. Two of the three withdrawals (Seat 1's rounding note, Seat 3's incentive note) were preference or norm claims rather than defects — a mild tendency to reach, worth noting but not enough to put any seat's reliability in question.

---

## 6. Executive review

The executive re-read the artifact in full before synthesis; the quotes and arithmetic above were re-derived against the source, not taken from the seat reports.

**Points of agreement — and the sequential-run caveat.** All three seats independently landed on the same underlying issue: the artifact's recommendation is stronger than its evidence, because the metric that carries the claim is not the metric that carries the value. Under the Step 3 sequential fallback this convergence is **not** evidence for severity, and per non-negotiable 3 every point of agreement is marked **sole-source**: the seats shared one context and later seats saw earlier ones, so what looks like three readings is closer to one. The severity ratings below rest on the artifact's own numbers, which I checked myself, and on nothing else.

**Deduplicated before publishing.** Two convergences were stated once and cut from the individual sections:
- *The proxy-metric problem* (Seats 1 and 2). Seat 1 raised it as its foundational-failure candidate and flagged the overlap; Seat 2 owns the remit and did the quantification. Published once, as the critical finding. **Sole-source.**
- *Marginal signup quality* (Seats 2 and 3). Seat 2's decomposition (~17% activation on the marginal cohort) and Seat 3's missing-guardrail gap are one issue: the doc cannot tell a friction win from a quality dilution. Published once as a single major. **Sole-source.**

**Points of conflict & adjudication.**
1. *Seat 1 says the primary-metric direction probably survives correction; Seat 2 says the conclusion does not follow.* Not a genuine conflict, and adjudicated as complementary: the completion-rate gain is likely real, its magnitude is inflated by early stopping, and neither fact establishes downstream value. Both stand.
2. *Severity of the composite finding — critical or major?* The strongest case against my own ruling: the doc's explicit claim is about **signups**, not activated users, so on a narrow reading it is internally consistent and the composite is a reviewer's added standard. **Ruling: upheld at critical.** The doc does not stay on the narrow reading — it uses the secondary metrics as affirmative clearance for a business decision ("no secondary metric moved against us"), which is a claim about downstream value. Once it makes that claim, the composite is the test of it, and the composite is null. Anchor personally checked: 1,438 × 0.312 ÷ 18,204 = 2.465% vs 1,592 × 0.298 ÷ 18,061 = 2.627%, z ≈ 0.98.
3. *Should the unconsidered-alternative finding be upgraded to critical?* Argued for on the grounds that the data loss is irreversible. **Ruling: held at major.** Specific evidence for the downgrade: shipping B is not itself an incorrect action — the recipient acting on it gets a defensible if suboptimal outcome, which fails the critical test. It is the *irreversibility*, not the choice, that stings, and that is already carried by the holdback finding.
4. *Silence noted, not counted.* No seat examined instrumentation; that is not a clearance (see blind spots).

Every critical and major finding upheld here had its anchor personally checked against the source; none is upheld on a seat's assertion alone.

**Verification result.** Three findings withdrawn, six narrowed, one downgraded from major to minor. No seat's reliability is in question; no finding rested on text the artifact does not contain. Two withdrawals were reaches rather than misreadings.

**Panel blind spots.** The strongest case the whole council is wrong: **all three seats assumed day-7 activation is a valid proxy for value.** If the real objective is paid conversion or day-30 retention, then the composite calculation that carries the critical finding is itself on the wrong axis — it would need redoing, and could land either way. All three also assumed test-period traffic equals "current traffic," and all three read "form views" as an event the artifact never defines. Under the sequential fallback, coverage is suspect as well as agreement: the seats shared one context and therefore likely share what they failed to look at.

**A domain no seat examined, as required by the roster cap: engineering instrumentation.** Nobody could inspect whether the "form view" event fires under identical conditions on both variants. Variant B is a structurally different form; if its view event fires on slightly different conditions, the *denominator* differs between arms and the entire completion-rate comparison is invalid — a critical defect, sitting upstream of everything above, that this council is structurally unable to detect. The requester fixed the roster at three seats, so the verdict is capped rather than extended: **this judgment does not cover instrumentation, and a defect there would change it.**

**Overall judgment.** A cleanly executed experiment with an honestly reported dataset and an analysis that does not survive scrutiny. The credit is real: the split is balanced with no sample ratio mismatch, the metric denominator is defined, the test is named, and the two secondary metrics that cut against the recommendation are on the page rather than buried. But the readout stops the test at the moment of significance, reports a p that does not reproduce from its own table, forecasts a number ~65% above what its own traffic supports, describes two adverse secondary movements as no adverse movement, and recommends the most irreversible available version of the change without comparing it to the alternative that dominates it. The direction of the effect is probably real; almost nothing else in the document is load-bearing as written. This is below what a competent growth analyst should produce for a readout authorizing a permanent change — not through dishonesty, but through a chain of small inferential shortcuts that all lean the same way.

**Decision on further action.** **Revise substantially before use.** The underlying data is sound and reusable — the experiment does not need re-running to be salvaged — but the Results and Recommendation sections must be rebuilt on the right metric, the right inference, and a staged rollout. The ship-to-100% recommendation should not be actioned in its current form.

**Prioritized next steps.**
1. Re-analyze on activated signups per form view with a confidence interval; state the activation cohort, as-of date, and n per arm. This single step determines whether there is a result at all.
2. Recompute the significance test from the final table under a sequential correction, and publish the corrected p and a bias-adjusted effect size.
3. Confirm with engineering that the "form view" event is instrumented identically on both variants — this is upstream of every other number and no seat could check it.
4. Rebuild the monthly forecast from the observed traffic base and state that base explicitly, before 1,850 is quoted into a planning document.
5. Reduce the rollout to 90/10 with a permanent holdback, pre-declared rollback thresholds, and a revisit date matching the quarter marketing agreed to.
6. Test optional fields or post-signup capture as variant C before deleting the fields permanently; enumerate what consumes "company size" and get each consumer to sign off.

**Confidence & what would change the verdict.** Of the 11 findings reported at critical and major, I expect **9 to survive** an independent expert re-check. The two I expect to fall first: the company-size accounting gap (an expert with system access may show nothing consumed the field, dropping it to minor) and the marginal-signup-quality finding (segment data could show the decomposition's constant-base assumption is false, which would dissolve it). The findings I expect to be hardest to dislodge are the three I re-derived arithmetically from the artifact's own table — the composite null, the non-reproducing p-value, and the forecast gap — because they require only the numbers already printed in the document.

The verdict rests on **verified arithmetic** (the composite, the z-test, the forecast reconstruction), on **confirmed absences** (no MDE, no holdback, no alternative considered, no quality guardrail), and on one **assumption**: that test-period traffic is representative of "current traffic," which the artifact never states.

What would flip it: if day-7 activation proves mature across all 3,030 signups *and* a properly powered downstream metric — paid conversion or day-30 retention — shows B at parity or better, the critical finding collapses to minor and the decision moves to **approve with minor revisions**. What would make it worse: if the "form view" event is instrumented differently across the two variants, the primary comparison is invalid at the root and the decision becomes **reject and rework**.
