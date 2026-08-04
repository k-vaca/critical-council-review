# Review — claim-02-survey.md (2026 Customer Needs Survey)

Reviewed: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/claim-02-survey.md`
One expert pass. Findings ordered critical → major → minor.

## Summary judgement

The document is a roadmap-reallocation recommendation resting on a survey whose sampling frame was
selected on the very behaviour the survey purports to measure. The three headline findings are each
compromised — one by circular frame selection, one by a leading question, one by a selection artifact —
and the appendix documents a segment skew severe enough (enterprise ~5.7× over-represented, small
customers ~4× under-represented) that the aggregate figures should not have been reported unweighted.
The arithmetic is internally consistent (both appendix columns sum to 100%; 4.2 mean and 71% top-two-box
are compatible). The problems are inferential and methodological, not computational. As written, a
recipient acting on this would defund the integrations catalogue on evidence that structurally could not
have detected demand for integrations.

---

## Critical

### C1 — Sampling frame is selected on the outcome variable
**Location:** Method, line 8 (consequences at lines 14–16 and 28)
**Anchor:** "distributed as an in-product banner shown to users who opened the analytics dashboard at least three times in the preceding 30 days"
**Problem:** The frame admits only heavy analytics users, so finding 1 ("users want deeper analytics, not broader integrations") is an artifact of who was asked rather than a fact about the customer base.

Users whose need is integrations are, by construction, disproportionately the users who do *not* open the
analytics dashboard three times a month — exactly the population excluded from the frame. The survey
cannot distinguish "our customers prefer analytics" from "analytics users prefer analytics." Any
comparative preference between analytics and integrations is uninterpretable from this design. Fix
requires re-fielding to a frame drawn from the customer base (or at minimum a stratified frame that
includes non-dashboard users), not reanalysis of the existing responses.

### C2 — Aggregate results reported unweighted despite severe, documented segment skew
**Location:** Appendix table, lines 32–36; generalisation at line 28
**Anchor:** "Our customers have told us clearly what they want, and it is not more connectors."
**Problem:** Every headline number is an unweighted respondent average from a sample where 72% of the customer base contributed 18% of responses, yet the conclusions are stated as facts about "our customers."

From the report's own appendix: enterprise is 6% of the base and 34% of respondents (~5.7×
over-represented); small (<50 seats) is 72% of the base and 18% of respondents (~4× under-represented);
mid-market is ~2.2× over-represented. Enterprise and small-business buyers have systematically different
needs regarding analytics depth versus connector breadth. No post-stratification or weighting is applied,
none is discussed, and no weighted figures are shown alongside the raw ones. The reported 1.8/4.1 mean
ranks, the 62%, and the 4.2 are all quantities about a skewed respondent pool being presented as
quantities about the customer base.

### C3 — Premium-tier question is leading, and stated interest is treated as demand
**Location:** Finding 2, line 20; acted on at line 28
**Anchor:** "Given how much time Northwind already saves your team, would you be interested in a premium analytics tier with custom modelling?"
**Problem:** The preamble asserts the product's value before asking, priming assent, and "interested" (with "probably yes" folded in) is reported as evidence sufficient to scope a paid tier.

Three compounding defects in one item: (a) the "Given how much time Northwind already saves your team"
clause is a presupposition that both flatters the respondent and supplies the justification for a yes —
textbook question loading; (b) "would you be interested in" measures costless curiosity, not purchase
intent, and is known to overstate real uptake by a wide margin; (c) collapsing "yes" and "probably yes"
into a single 62% hides how much of that figure is soft. Note also that the Method promises
willingness-to-pay questions (line 10) — a price-anchored WTP item would have been the appropriate
evidence here and is not reported (see M4). The 62% should not be used to justify scoping a commercial
tier.

---

## Major

### M1 — The decision to move capacity *out of* integrations has no supporting evidence of any kind
**Location:** Recommendation, line 28
**Anchor:** "should move engineering capacity out of the integrations catalogue and into the analytics module"
**Problem:** A relative preference ranking among current analytics users says nothing about the revenue, retention, or deal-blocking value of the integrations catalogue that would be forfeited.

Even a perfectly sampled preference survey does not establish marginal return on engineering capacity.
Reallocating away from integrations requires evidence the survey never gathers: integration-driven churn,
deals lost for missing connectors, integration usage among the segments excluded from the frame, and the
cost/benefit of the analytics work being proposed. The recommendation is a strictly stronger claim than
"analytics ranked higher," and nothing in the document supports it.

### M2 — Response rate not reported; self-selection and non-response bias unaddressed
**Location:** Method, line 8
**Anchor:** "1,247 responses were collected from an eligible pool of 31,180 users who saw the banner."
**Problem:** The response rate is 4.0%, it is never stated as such, and the report contains no assessment of how the 96% who declined might differ from the 4% who answered.

At 4% (1,247/31,180), respondents are twice self-selected: first by the dashboard-usage frame (C1), then
by willingness to answer an in-product banner. Users with the strongest opinions about analytics are the
likeliest to click through, which biases in the same direction as the frame. Standard practice is to
report the rate explicitly and to run a non-response check (e.g. compare respondents to non-respondents on
observable account attributes). Neither is done.

### M3 — No per-item base sizes, margins of error, or significance testing anywhere
**Location:** Headline findings, lines 16, 20, 24
**Anchor:** "respondents put \"more powerful analytics\" first (mean rank 1.8) and \"more integrations\" last (mean rank 4.1)"
**Problem:** Every figure is a bare point estimate with no n for the item, no confidence interval, and no test of the differences being asserted.

The reader cannot tell whether 62% is 62% of 1,247 or of some conditional subset, whether the 1.8/4.1 gap
is stable, or how precise 4.2 is. Subgroup or segment comparisons (M5) would be uninterpretable without
these. For a document whose entire purpose is to justify a capacity reallocation, quantified uncertainty
is not optional.

### M4 — Fielded topics that would test the recommendation are not reported
**Location:** Method, line 10, versus the Headline findings section
**Anchor:** "14 questions covering feature satisfaction, unmet needs, and willingness to pay for proposed additions"
**Problem:** Fourteen questions were asked and three results are shown; the omitted willingness-to-pay and unmet-needs data are precisely the evidence the premium-tier and reallocation recommendations require.

This is a selective-reporting pattern: the reported subset is uniformly favourable to the recommendation,
while the two topics that could contradict it (what users actually say is unmet, and what they would
actually pay) are absent. The WTP results in particular are the correct basis for the "scope a premium
tier" recommendation and their absence, when they exist, must be explained or the results published.

### M5 — No segment breakdowns despite the report documenting the skew itself
**Location:** Headline findings (lines 14–24) against Appendix (lines 32–36)
**Anchor:** "| Enterprise (>500 seats) | 34% | 6% |"
**Problem:** The report identifies a large segment imbalance and then reports only pooled aggregates, so the reader cannot tell whether the analytics preference is an enterprise effect.

The obvious and necessary cut — do small customers rank the five investment areas the same way as
enterprise? — is missing. If the analytics-first ranking is driven by the over-represented enterprise
third of respondents, the recommendation inverts for 72% of the customer base. This is answerable from
data already collected and should have been in the first draft.

### M6 — The appendix compares two different units of analysis
**Location:** Appendix table header, line 32
**Anchor:** "| Segment | Share of respondents | Share of customer base |"
**Problem:** "Share of respondents" counts individual users while "share of customer base" is undefined (accounts? seats? revenue?), so the over/under-representation multiples are not apples-to-apples.

If the right-hand column is share of *accounts*, then enterprise over-representation among *users* is
partly mechanical — an enterprise account contains hundreds of seats and can contribute many respondents.
The direction of the skew survives, but its magnitude, and therefore the weighting scheme needed to fix
C2, depends entirely on which unit is meant. The table must define the denominator, and ideally show
respondents-per-account and share of ARR alongside.

### M7 — No limitations section; conclusions stated with unqualified certainty
**Location:** Document level; explicit at line 28
**Anchor:** "Our customers have told us clearly what they want, and it is not more connectors."
**Problem:** A research deliverable driving a capacity reallocation contains no caveats, no statement of frame restrictions, and asserts certainty the design cannot support.

At minimum the report needs a limitations section stating the dashboard-usage frame and what it excludes,
the 4% response rate, the unweighted segment skew, and the fact that finding 2 rests on a single
attitudinal item. As written, a reader who does not scrutinise the Method and Appendix would reasonably
believe this is a representative read of the customer base.

### M8 — Finding 3 does not support the recommendation and is itself a selection artifact
**Location:** Finding 3, lines 22–24, used under the Recommendation at line 28
**Anchor:** "Mean satisfaction with the current analytics module was 4.2 of 5. 71% rated it 4 or 5."
**Problem:** High satisfaction with the existing analytics module is at best neutral and arguably argues against pouring more capacity into it, yet it is presented as part of the supporting case.

Two issues. First, the logic: if the analytics module already scores 4.2/5, the marginal return on
further investment there is plausibly lower than in an area users are dissatisfied with — the report
never engages this tension. Second, the measurement: satisfaction was collected exclusively from users
who opened the module at least three times in 30 days, a group nearly guaranteed to rate it highly.
Dissatisfied users stop opening it and are therefore outside the frame. The 4.2 is close to
uninformative as a product-quality signal.

---

## Minor

### m1 — Questionnaire not appended
**Location:** Method, line 10
**Anchor:** "Respondents answered 14 questions covering feature satisfaction, unmet needs, and willingness to pay"
**Problem:** Only one of fourteen items is quoted verbatim and that one is demonstrably leading (C3), so the remaining thirteen cannot be audited for the same defect.

### m2 — Mean ranks reported without dispersion, and the forced-ranking caveat is absent
**Location:** Finding 1, line 16
**Anchor:** "Asked to rank five investment areas"
**Problem:** A forced ranking is zero-sum — something must come last — so a mean rank of 4.1 does not establish that integrations are unwanted, only that they lost a relative contest among five items. Standard deviations or the full rank distribution should accompany the means, and an absolute-importance item (or MaxDiff) would be needed to support the "not more connectors" phrasing.

### m3 — Eligibility and exposure are conflated in the denominator
**Location:** Method, line 8
**Anchor:** "an eligible pool of 31,180 users who saw the banner"
**Problem:** The phrase merges two different populations (users eligible under the ≥3-opens rule, and users actually served the banner), and does not say whether 31,180 counts unique users or banner impressions — leaving the response-rate denominator ambiguous.

### m4 — No data-quality or processing notes
**Location:** Method section (lines 6–10)
**Anchor:** "1,247 responses were collected"
**Problem:** Nothing is said about partial completes, deduplication (including multiple respondents from one account), straightlining or speeder removal, or whether the 1,247 are completes or starts.

---

## What would make this sound

1. Re-field to a frame drawn from the customer base, or explicitly restrict every claim to "users who open the analytics dashboard ≥3×/month" and remove the reallocation recommendation.
2. Weight to the customer base (defining the unit first, per M6) and publish weighted alongside unweighted figures with per-item n and confidence intervals.
3. Replace the premium-tier item with a neutrally worded, price-anchored WTP measure; report the WTP and unmet-needs data already collected.
4. Publish segment cross-tabs of the ranking item before any capacity decision.
5. Support or drop the "move capacity out of integrations" recommendation using integration-side business data (churn, blocked deals, usage among excluded segments).
6. Add a limitations section and soften the certainty of the closing claim.
