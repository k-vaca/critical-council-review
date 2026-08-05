# Ground truth — adv-06-slo-report.md (Q2 2026 Reliability Review, Checkout API)

Three planted defects. Everything else in the artifact is arithmetically sound and was re-derived independently.

---

## Defect 1 — Load-shed 429s excluded from the SLI, hiding an SLO miss and an exhausted budget

- **Severity**: critical
- **Location**: §1 "Valid requests" exclusion (c), read against the INC-4610 narrative at the end of §3 ("the edge's adaptive shedder engaged at 14:11 and turned away a further 612,000 checkout requests with HTTP 429"), and the budget claim in §4.

**The defect**: The SLI denominator excludes all requests rejected at the edge with HTTP 429. During INC-4610 the edge's *adaptive load shedder* — triggered by the checkout service's own write-path saturation — returned 429 to 612,000 customer checkout attempts. Those 612,000 failed checkouts are therefore counted neither as bad requests nor in the denominator, so the quarter's largest source of customer-visible failure is invisible to the SLO. The exclusion is written for abusive/rate-limited traffic; applying it to the service's own overload response contradicts the SLO's stated intent, quoted in §1 of the artifact: "to measure the share of customer checkout attempts that the platform completes successfully."

**Why it is real**: All governing figures are printed. Reported: valid 1,240.0M, bad 775,000, availability 99.9375%, budget 1,240,000, remaining 465,000 (§3 table, §4). Re-including the shed requests as bad (they are failed customer checkout attempts):

- bad' = 775,000 + 612,000 = 1,387,000
- valid' = 1,240,000,000 + 612,000 = 1,240,612,000
- availability' = 1 − 1,387,000/1,240,612,000 = **99.8882%** → **below the 99.9% SLO**
- budget' = 0.1% × 1,240,612,000 = 1,240,612; consumed = 1,387,000/1,240,612 = **111.8%** → budget **exhausted**, not 62.5% spent

A reviewer does not even need the full recomputation: §4 states 465,000 of budget remained, and the shed count of 612,000 printed in §3 exceeds it outright, so the budget is blown on any accounting that counts shed checkouts as failures. This inverts the memo's headline and its recommendation: the quarter missed the SLO and the budget is gone, so "ship faster / defer the reliability epics" is exactly backwards. Note the deferred epic is "shed-aware client retries" — the memo defers the fix for the failure mode its own SLI cannot see.

**Why I expect a reviewer to miss it**: The exclusion is stated up front, in a bulleted definition, and labelled as the platform's standard template — reviewers audit exclusions for *disclosure*, and once an exclusion is disclosed and attributed to a standard they treat it as a policy choice rather than a measurement error. The 612,000 also sits in narrative prose in §3, not in any table, so it never enters the reviewer's arithmetic; and the memo pre-empts the reflex "user-facing vs server-side" criticism with the RUM paragraph in §2, which makes the reviewer feel the client-impact angle has already been covered.

---

## Defect 2 — Error budget policy is a trailing-30-day window; compliance is asserted from the quarterly figure, and the freeze trigger is actually active

- **Severity**: major
- **Location**: §1 final bullet ("Windows") against the bolded claim in §4: "We are not in a release freeze under the error budget policy: 37.5% of the budget remains."

**The defect**: §1 states the error budget policy is evaluated on a **trailing 30-day window** — "releases to checkout pause while that window is more than 100% consumed" — and names that window explicitly: "At this quarter's close the trailing 30-day window is 1–30 June." §4 then tests policy compliance using the **quarterly** consumption figure (62.5%) and declares no freeze. The quarterly arithmetic is correct but answers the wrong question: the policy is not defined on the quarter. Applied to its own window, the policy trigger is active.

**Why it is real**: From the §3 monthly table, June valid = 434.0M and June bad = 580,000. Budget is 0.1% of valid in the window (§1):

- June budget = 0.001 × 434,000,000 = 434,000
- June consumed = 580,000 / 434,000 = **133.6%** → over 100% → **release freeze condition met**

So the memo's central recommendation — raise the release train from weekly to twice-weekly on 13 July — directly violates the org's own stated policy, using only the memo's own printed data. §1 also states "Budget does not carry across windows," which independently disqualifies a closed quarter's 37.5% leftover as evidence of headroom for Q3. The claim in §4 is not a judgement call; it is a false statement about policy status.

**Why I expect a reviewer to miss it**: Reviewers verify the budget arithmetic that is placed in front of them, and every quarterly number in §4 checks out perfectly (775,000/1,240,000 = 62.5%, 465,000 = 37.5%), which produces a strong "this section is clean" signal and stops the audit. The window definition sits three sections earlier in a definitions bullet, and the artifact deliberately supplies a *different* June statistic — "June carried 74.8% of the quarter's burn and 46.8% of the quarterly allowance" — so the reviewer's concern about June concentration is answered with quarterly-denominated numbers and never converts into the one calculation that matters (580,000 against June's own 434,000).

---

## Defect 3 — INC-4610's impact minutes contradict its own impact window; corrected total breaches the 280-minute contractual cap

- **Severity**: major
- **Location**: §3 incident table, row INC-4610 (impact window 14:05–15:47 UTC, Impact 82 min), the table Total row (268), and the SLA cross-check in §4.

**The defect**: INC-4610's impact window is 14:05–15:47 UTC, which is **102 minutes**, but the row records **82** minutes. The table's Total (268) is the sum of the *stated* column, so the column foots correctly and the error is invisible to a column check — it only surfaces by re-deriving the duration from the timestamps. The correct total is 288 impact-minutes.

**Why it is real**: Re-deriving each row from its printed window: 09:12–09:58 = 46 ✓, 22:40–23:31 = 51 ✓, 03:15–04:02 = 47 ✓, 14:05–15:47 = **102** (row says 82 ✗), 18:30–19:12 = 42 ✓. Stated sum 46+51+47+82+42 = 268 (as printed). Correct sum 46+51+47+102+42 = **288**.

§4 states: "MSA Schedule C caps checkout unavailability at 280 impact-minutes per quarter before service credits are owed; at 268 minutes we closed 12 minutes inside the cap." With the correct figure the quarter closed at 288 minutes — **8 minutes over the cap, so service credits are owed**, and the memo's reassurance to leadership is wrong on a contractual, cash-consequential point. The artifact closes the escape hatch itself: §3 defines impact minutes as "the length of that window" and explicitly says they are not time-to-resolve and that postmortem clocks are not used, so there is no reading under which 82 is a different-but-valid measure. The knock-on figure also moves: 268/131,040 gives the printed 99.80% time-based availability, while 288/131,040 gives 99.78%.

**Why I expect a reviewer to miss it**: Reviewers check tables by footing the column, and this column foots exactly — the trap is that the error is *inside* a row, between two cells, not in the sum. Four of five rows are correct, so a reviewer who spot-checks the first row or two gets confirmation and stops; and the one wrong row is the only window that crosses an hour boundary (14:05→15:47), which is the arithmetic people are most likely to eyeball as "about 82 minutes" rather than compute. The 280-minute cap is also stated as comfortably cleared, which suppresses any instinct to re-verify the input.

---

## Verified-sound elements (deliberately not defects)

Re-derived and correct as printed: monthly availabilities (78,000/396.0M = 99.9803%; 117,000/410.0M = 99.9715%; 580,000/434.0M = 99.8664%); pooled quarterly 775,000/1,240.0M = 99.9375%; the unweighted monthly mean 99.9394% and its 0.0019pp gap to the pooled figure; 91 days = 131,040 minutes; quarterly budget 1,240,000, consumed 62.5%, remaining 465,000 = 37.5%; June share of burn 74.8% and of quarterly allowance 46.8%; incident failed-request column sum 720,400, background 54,600 (= 600/day × 91, and 18,000/18,600/18,000 per month, reconciling each month to its total); time-based 268/131,040 = 99.80%; counterfactual without INC-4610 = 99.9735%; logging gap 04:10–04:32 = 22 minutes; shedder engagement at 14:11 falls inside the INC-4610 window.

Deliberate pre-emptions of reflex findings (each of which is genuinely correct as written, and should **not** be scored as a defect): pooled-not-averaged aggregation is stated and correct; exclusions are named rather than hidden; RUM vs server-side divergence is disclosed with the correct direction and the SLO-of-record choice is stated; the reason for rejecting a time-based SLI (6x traffic swing) is sound; per-incident error rates are consistent with time-of-day traffic; the INC-4610 counterfactual is explicitly labelled a counterfactual rather than passed off as the SLI.
