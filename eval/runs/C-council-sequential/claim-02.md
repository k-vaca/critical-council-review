# Critical Council Review — `claim-02-survey.md`

Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

---

## 1. Verdict

**Reject and rework.** The memo generalizes to "our users" from a sample that was eligible only if it already used analytics heavily, and reports it unweighted against a customer base it inverts; no edit to the text fixes a frame that selects on the outcome.

1. Re-field the investment-priority question (Headline finding 1) to a random sample of the full customer base, outside the analytics dashboard.
2. State the target population and re-report every number weighted to it (Appendix table); until then label all findings "analytics-active users only".
3. Publish the willingness-to-pay items the Method section says were collected (Method, ¶2) before scoping any premium tier.

---

## 2. Result & standard

**Artifact.** `critical-council-review-eval/artifacts/claim-02-survey.md`, read in full (36 lines) — a survey findings memo ending in a recommendation to reallocate H2 engineering capacity from integrations to analytics and to scope a paid tier. Not my own prior output.

**Text addressed to its reviewer.** None. The artifact contains no instructions to a reviewer, no claim that any part is pre-approved, and no stated success criteria. Nothing to quote under non-negotiable 8.

**Requester framing (quarantined).** The requester fixed the roster, the independence mechanism, and the output path, and said nothing about the artifact's quality or an expected verdict. Nothing to discount.

**Standard.** The artifact's own purpose: to be a sufficient evidentiary basis for moving engineering capacity and opening a paid tier. Judged against what a competent product researcher should produce for a resource-allocation decision — the population the claim names must be the population sampled, the instrument must not encode the conclusion, and the report must disclose weighting, per-item n, and dispersion. This is my stated professional judgment; it also tracks the disclosure elements in AAPOR's standard `[unverified — recall, not lookup]`.

**Tier 3**, on the "expensive decision" row rather than on length: the artifact is ~350 words but commits a half-year of engineering capacity. **Independence mechanism: sequential seats** (Step 3 fallback) — no subagent tooling was available for this run.

**Declared deviations.** (a) The roster was fixed at three seats by the requester; tier 3 calls for four to six. Disclosed per Step 2, with the uncovered domains named in §4 and the verdict capped accordingly. (b) The length budget is overrun: sections 2–4 exceed their 300-word sub-ceiling in order to keep all eleven anchored findings, and the review totals ~3,485 words against the tier's 3,000, with the executive section the largest overrun. The sequential fallback adds mandatory Step 6 work that the parallel path does not — sole-source marking, the shared-assumption test, and the coverage-suspicion pass. The skill designates every length number as tunable; the overrun is declared rather than absorbed by cutting findings.

---

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Method ¶1 — "shown to users who opened the analytics dashboard at least three times in the preceding 30 days" | The eligibility rule selects respondents on the very preference the headline generalizes to all users. | Re-field the priority question to a random sample of the full base; until then scope finding 1 to analytics-active users. | Confirmed |
| Critical | Appendix — "Small (<50 seats) \| 18% \| 72%" | Results are unweighted while the sample inverts the base, so no reported number estimates a company-wide preference. | Name the target population, post-stratify to it (by seats or by revenue), and re-report every headline number with its interval. | Confirmed |
| Major | Recommendation — "told us clearly what they want, and it is not more connectors" | A mean rank of 4.1 on a 1–5 scale is not unanimity (that would be 5.0), and last-of-five is not absence of demand. | Drop "clearly"; support any cut with an absolute demand measure per area. | Confirmed |
| Major | Method ¶1 — "distributed as an in-product banner" | Respondents ranked analytics against integrations while inside the analytics dashboard, priming the answer. | Re-field on a neutral surface (email or account-level in-app) and compare the two rankings. | Confirmed |
| Major | Finding 2 — "Given how much time Northwind already saves your team, would you be interested in a premium analytics tier with custom modelling?" | The preamble asserts the benefit before asking, and stated interest merged with "probably yes" cannot carry a paid-tier decision. | Re-ask neutrally with a price-anchored item; report "yes" separately from "probably yes". | Confirmed |
| Major | Method ¶2 — "willingness to pay for proposed additions" | WTP was collected but no WTP figure appears anywhere, while the memo recommends scoping a paid tier. | Publish the WTP items in full, including any null result, before scoping. | Corrected |
| Major | Method ¶1 — "1,247 responses were collected from an eligible pool of 31,180 users who saw the banner" | A 4.0% response rate with no comparison of respondents to non-respondents on any observable. | Compare respondents and non-respondents on seats, tenure and feature use; report the deltas. | Confirmed |
| Major | Method ¶1 (frame) applied to Recommendation — "move engineering capacity out of the integrations catalogue" | Prospects and churned accounts lost over a missing connector cannot appear in this frame, so integration demand is invisible by construction. | Add lost-deal and churn-reason data by segment before cutting integrations capacity. | Confirmed |
| Major | Finding 3 — "Mean satisfaction with the current analytics module was 4.2 of 5" | Presented as support for more analytics investment though it is non-probative and equally consistent with diminishing returns. | Drop it from the case, or pair it with an importance-versus-satisfaction gap measure. | Corrected |
| Minor | Finding 1 — "(mean rank 1.8)" and "(mean rank 4.1)" | Ranks given with no dispersion, no per-item n, and three of the five investment areas never named. | Report full rank distributions, per-item n, and all five option labels. | Confirmed |
| Minor | Recommendation — "The roadmap for H2 should move engineering capacity out of the integrations catalogue" | States no magnitude, no cost, and no observable result that would reverse the move. | Specify the share of capacity, the period, and the reversal criterion. | Confirmed |

Overlapping observations are consolidated here and appear once; the seat sections below cite row numbers rather than restating them.

---

## 4. Council roster

Derived from this artifact's specific failure modes: a preference survey whose frame is defined by the behaviour under study, whose respondent mix is disclosed as unrepresentative, and whose conclusion is a capital-allocation call.

1. **Methodology & statistics** — owns design, estimation and disclosure; this memo's numbers are asked to carry a resource decision.
2. **Data & inference validity** — owns sampling, confounds, measurement and whether the conclusion follows; the artifact's three findings each name a broader population than they measure.
3. **Decision red-team** — owns whether the recommendation survives reality, and carries the recipient's viewpoint (the product or engineering leader who must execute the reallocation), per Step 2's requirement to seat whoever depends on the result.

**Deliberately not covered.** *Instrument QA* — 11 of the 14 questions are never shown; a critical defect (question order, double-barrelled items, a broken scale) could live there and no seat could see it. *Pricing and commercial viability* — whether a premium tier is economically sound is unexamined; a critical defect could live there, and so could independent support for that half of the recommendation. *Engineering cost and delivery* — the actual cost and revenue role of the integrations catalogue is unexamined; a critical defect could live there. The verdict is capped accordingly: it judges the memo as an evidentiary basis, not the underlying business bet.

---

## 5. Individual analyses

### Seat 1 — Methodology & statistics

**Role & remit.** Survey methodologist. Judges frame construction, estimation and disclosure — whether the reported numbers can bear the weight placed on them. Does not judge the business call.

**Standard applied.** A survey report used for a resource decision discloses frame, response rate, weighting scheme, per-item n and dispersion around every statistic, and reports estimates for a named population. Stated professional judgment; tracks AAPOR's disclosure elements `[unverified — recall, not lookup]`.

**Assessment.** This is a convenience sample whose eligibility rule correlates with the outcome variable, reported without weights. n is ample — 1,247 gives tight precision — so nothing here is a power problem, and "collect more responses" is the wrong fix. Every defect is bias, and the report omits the machinery that would let a reader size it.

**Strengths.** Genuine and load-bearing: the Method section discloses the eligibility rule, the field window, the exposure count and the response count (¶1), and the Appendix voluntarily reports the segment skew (lines 32–36). The evidence that falsifies the memo's headline is inside the memo. Most internal readouts of this kind disclose less.

**Weaknesses, risks & errors.** Row 1 (critical, defect) — the frame is defined by the behaviour under study. Row 2 (critical, defect) — unweighted estimates from an inverted sample; enterprise and mid-market are 82% of respondents against 28% of the base. Row 7 (major, defect) — 4.0% response rate, no nonresponse analysis. Row 3 (major, defect) — "clearly" is arithmetically unsupported by a 4.1 mean. Row 10 (minor, defect) — no dispersion, no per-item n, three of five options unnamed. Additionally (minor, defect): the base's absolute size is never given, so the eligible pool cannot be sized against it — Appendix column header "Share of customer base" is the only reference to the base's composition.

**Gaps.** No weighting scheme; no intervals; no question order; wording shown for 2 of 14 items; results shown for 3 of 14; no prior wave to read 4.2 against.

**Strongest reason this might be fundamentally wrong.** The instrument measures relative preference within a closed list, among people selected for engagement with one item on that list. If that is right, no re-analysis of this dataset yields a company-wide demand estimate — the remedy is a new study, not a better write-up.

**Domain verdict.** Below the standard for a document that reallocates engineering capacity. Adequate as an internal readout for analytics-active users, if relabelled.

**Recommended fixes.** Name the target population; post-stratify and re-report with intervals; publish rank distributions and per-item n; add a respondent-versus-non-respondent comparison on telemetry; release all 14 items.

### Seat 2 — Data & inference validity

**Role & remit.** Judges sampling, confounds, measurement, and whether the stated conclusion follows from the data shown.

**Standard applied.** A conclusion is supported only when it holds for the population it names and is measured by an instrument that does not encode it. Stated professional judgment.

**Assessment.** Each of the three headline findings names a wider population or a stronger construct than its data supports, and the Recommendation compounds all three into a single claim about "our customers". The gap is not subtle: the memo's own Appendix shows the group it speaks for is 18% of respondents and 72% of the base.

**Strengths.** Finding 1 reports the actual rank means rather than a verbal summary, which is what makes the overstatement in the Recommendation checkable against the memo's own body.

**Weaknesses, risks & errors.** Row 4 (major, defect) — context priming: the survey was served inside the analytics dashboard, so the analytics-versus-integrations ranking was taken in the analytics context. Row 5 (major, defect) — the premium-tier item asserts its own premise ("Given how much time Northwind already saves your team") and then merges "probably yes" into a headline percentage. Row 6 (major, defect) — willingness to pay is listed as collected but no WTP result is reported. Row 9 (major, defect) — satisfaction is presented as a supporting finding for more analytics investment. Row 3 (major, defect) — the forced-rank-to-absent-demand conversion; overlaps Seat 1's arithmetic reading of the same sentence, noted rather than skipped. Minor, defect — the scope language "Our users" (Headline 1) and "Our customers" (Recommendation) appears with no caveat anywhere in the document.

**Gaps.** No segment cut of the rankings — the memo cannot show whether small-seat customers rank the same way. No revealed-behaviour cross-check against telemetry. No competing explanation considered anywhere.

**Strongest reason this might be fundamentally wrong.** If the small-seat segment — 72% of the base, 18% of respondents — ranks integrations first, the recommendation is not merely unsupported but inverted. The memo contains no segment breakdown that could detect this, and its own Appendix is what makes the possibility live.

**Domain verdict.** The conclusion does not follow from the data shown.

**Recommended fixes.** Publish the rankings cut by segment; re-ask the tier question without a preamble and with a price anchor; restate all three findings with their true population; release the WTP items.

### Seat 3 — Decision red-team

**Role & remit.** The strongest case against acting on this recommendation, and the viewpoint of the leader who must execute it.

**Standard applied.** A recommendation to move capacity states magnitude, cost, reversal criteria, and the failure mode it accepts. Stated professional judgment.

**Assessment.** The recommendation is one-directional and unbounded, rests on stated preference rather than demand or revenue, and proposes cutting the one area whose demand signal lives mostly outside surveys.

**Strengths.** It commits to a direction and names two concrete actions rather than recommending "invest in analytics" — a reader knows what would change on Monday.

**Weaknesses, risks & errors.** Row 8 (major, defect) — the frame cannot contain anyone who left or never bought over a missing connector; integration demand is invisible by construction, so "it is not more connectors" is a conclusion the study design guarantees. Row 11 (minor, defect) — no magnitude, no cost, no reversal criterion, no downside case. Minor, defect — no non-survey evidence is cited either way; a capacity decision resting on a single instrument, with churn, sales-loss and telemetry data presumably available, is under-evidenced regardless of that instrument's quality (Recommendation, whole section). *A fourth item — that the H2 window may already be partly committed by the time this is read — was raised here and withdrawn at Step 5.*

**Gaps.** No cost of reversal; no statement of what the integrations catalogue currently earns or blocks; no options considered between "move capacity out" and "leave it".

**Strongest reason this might be fundamentally wrong.** The recommendation may well be correct — analytics may be the better bet — but the memo gives a decision-maker no way to tell. The failure is evidentiary rather than directional, which is the worse case for a reviewer: the plan could succeed and still teach the organisation that this quality of evidence is sufficient.

**Domain verdict.** Not safe to act on as written.

**Recommended fixes.** Hold the current allocation; pull lost-deal and churn-reason data by segment; restate the recommendation with a share, a period and a reversal criterion; decide after the re-field.

---

## 6. Executive review

The executive re-read the artifact in full before synthesis; every anchor below was checked against the source text rather than against the seat reports.

**Points of agreement.** One: the sample does not represent the customer base (Seats 1, 2, 3). Per the sequential fallback, this convergence is **not** treated as evidence of severity and is **marked sole-source** — one context produced all three readings. Testing the shared assumption as non-negotiable 3 requires: it rests on the memo intending a company-wide claim. The artifact establishes that itself — "Our users" (Headline 1), "Our customers" (Recommendation), and an Appendix column headed "Share of customer base", which is only relevant if the base is the target. The assumption is established by the artifact, not inherited from framing, so the agreement stands on its own anchors. Rows 1 and 2 are upheld at critical on the quoted text alone.

**Points of conflict & adjudication.** No seat contradicted another. Two rulings were still required. (a) Row 5, the leading premium-tier question, was argued toward critical: rejected, held at major. The recommendation asks only to "begin scoping", a cheap and reversible step, so the recipient must rework the demand case rather than act on a wrong result — the major test, not the critical one. (b) Row 9, satisfaction, was argued as contradicting the recommendation: narrowed. High satisfaction with the module's current scope and demand for more of it are compatible, so the defect is that a non-probative number is presented as one of three converging findings, not that it refutes the case.

**Verification result.** All nine critical and major findings were re-checked by searching the source for each quoted string: the frame clause, the banner clause and the "1,247 … 31,180" sentence in Method ¶1; "willingness to pay for proposed additions" in Method ¶2; the premium-tier question in Headline 2; "Mean satisfaction … 4.2 of 5" in Headline 3; "clearly … not more connectors" and the H2 sentence in the Recommendation; and the "Small (<50 seats) | 18% | 72%" row in the Appendix. All located as quoted. Both minor findings were verified too rather than shipped unverified. **Two corrected:** Seat 2's "no willingness-to-pay evidence" became "WTP was collected but not reported" — a material change, since the fix is to request existing data rather than to field a new study; and Seat 2's satisfaction finding was narrowed as adjudicated above. **One withdrawn:** Seat 3's claim that the H2 window is already partly committed. The artifact states a fielding window but no circulation or decision date, so the claim rested on a fact not present in it. Its salvageable core — that the memo names no decision timing or committed work — is already carried by row 11 and is not reinstated here. No seat's reliability is in question; the withdrawn item was the only one that reached outside the text.

**Panel blind spots.** Three seats shared one context, so coverage is as suspect as agreement. Nobody examined the 11 unreported questions, and a critical defect — a broken scale, question order effects, a double-barrelled item — could live there undetected. Nobody examined pricing or commercial viability; a defect could live there, and so could independent support for the premium tier. Nobody examined the integrations catalogue's actual cost and revenue role. All three seats also assumed the printed figures are accurate: 1,247, 31,180, the two rank means, and the Appendix percentages are load-bearing and cannot be checked from the artifact — they should be verified against the raw survey export before any decision. The council also assumed no other evidence exists behind the recommendation, because the memo cites none.

**Overall judgment.** The memo is transparent enough to be checked and does not survive the check. Its Method and Appendix honestly disclose an eligibility rule that selects on the outcome and a respondent mix that inverts the customer base — and its three headline findings and its recommendation then ignore both. The underlying survey is genuine evidence about how analytics-active, enterprise-skewed users rank a fixed list of options; it is not evidence about what the customer base wants, and the document's purpose requires the latter.

**Decision on further action.** **Reject and rework.** Chosen over "revise substantially before use" because the central defect is in the frame, not the write-up: a fully rescoped version of this document could no longer make the recommendation that is its point.

**Prioritized next steps.**
1. Do not move H2 capacity on this memo; hold the current integrations allocation until step 4 reports.
2. Pull the willingness-to-pay items from the existing survey export and publish them in full, including any null result — cheapest step, available in days, and it settles half of the premium-tier question.
3. Re-report every headline number weighted to a named target population, with rank distributions, per-item n, segment cuts, and finding 1 relabelled "analytics-active users".
4. Re-field the investment-priority question to a random sample of the full base, off the analytics surface, with a neutral, price-anchored tier question.
5. Bring in what a survey cannot produce: churn and lost-deal reasons by segment, integration-request volume, and revenue at risk. Then decide.

**Confidence & what would change the verdict.** Of the 9 findings reported at critical or major, I expect 8 to survive an independent expert re-check. The first to fall is row 9 (satisfaction) — a reviewer could reasonably rule it presentational and downgrade it to minor. Row 2 (weighting) is the next most likely to move: it narrows if the team can show the skew was a deliberate, stated revenue-weighted design, though the memo's "Our users" language would still be wrong. Rows 1, 3, 7 and 10 rest on quoted text and arithmetic and should be immovable. The verdict rests on verified evidence for the defects and on one inference: that no evidence outside this memo backs the recommendation. Producing such evidence — a random-sample study, churn analysis, or revenue data pointing the same way — would move the decision from "reject and rework" to "revise substantially before use", because the memo would then be a badly argued case for a possibly sound call. Nothing in the artifact itself would change the verdict; the defects are structural.
