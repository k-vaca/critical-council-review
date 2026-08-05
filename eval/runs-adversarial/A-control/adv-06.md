# Review — Q2 2026 Reliability Review, Checkout API (adv-06-slo-report.md)

Single expert pass. Every figure on the page was re-derived independently.

## What checks out

Before the defects, the parts that are correct, because they bound where the problems are:

- April: 78,000 / 396.0M → 99.98030% ✓ (reported 99.9803%)
- May: 117,000 / 410.0M → 99.97146% ✓ (99.9715%)
- June: 580,000 / 434.0M → 99.86636% ✓ (99.8664%)
- Q2 pooled: 775,000 / 1,240.0M → 99.93750% ✓ (99.9375%)
- Monthly valid sums to 1,240.0M ✓; monthly bad sums to 775,000 ✓
- Unweighted mean of the three months = 299.8182/3 = 99.9394% ✓; delta vs pooled = 0.0019pp ✓
- Q2 2026 = 30+31+30 = 91 days; 91 × 1440 = 131,040 minutes ✓
- 3 May 04:10–04:32 = 22 minutes ✓
- Incident failed-request column sums to 720,400 ✓; 775,000 − 720,400 = 54,600 ✓; 54,600 / 91 = 600.0/day ✓
- Per-month reconciliation is exact: April 60,000 + 18,000 = 78,000; May 45,000 + 53,400 + 18,600 = 117,000; June 447,000 + 115,000 + 18,000 = 580,000 ✓
- Budget maths: 0.1% × 1,240.0M = 1,240,000; 775,000/1,240,000 = 62.5%; remainder 465,000 = 37.5% ✓
- 580,000/775,000 = 74.84% ✓; 580,000/1,240,000 = 46.77% ✓
- Counterfactual: (775,000 − 447,000)/1,240.0M → 99.97355% ✓ (99.9735%)
- 268/131,040 → 99.7955%, rounds to 99.80% ✓
- Impact windows INC-4471 (46), INC-4519 (51), INC-4562 (47), INC-4633 (42) all correct ✓
- 280 − 268 = 12 ✓ (arithmetic correct; input is not — see C1)

The data layer is genuinely well constructed and internally consistent. The defects are concentrated in one arithmetic slip and in the policy/judgment layer built on top.

---

## Critical

### C1 — INC-4610 impact window is understated by 20 minutes; this flips the contractual conclusion

**Location:** §3 incident table, INC-4610 row; propagated to the Total row and to §4 MSA cross-check.

**Anchor:** `INC-4610 | 11 Jun | 14:05–15:47 | 82 | 447,000 | Write-path saturation`

**Problem:** 14:05 to 15:47 is 102 minutes, not 82, making the quarter's true total 288 impact-minutes, which breaches the 280-minute MSA cap by 8 minutes rather than clearing it by 12.

Derivation: 15:47 − 14:05 = 1h42m = 102 min. Corrected total = 46 + 51 + 47 + **102** + 42 = **288**. The other four rows are correct, and 46+51+47+82+42 does equal the stated 268 — so the table is internally consistent with the wrong cell, which is exactly why the error survives a casual check.

Consequences:
- §4's "at 268 minutes we closed 12 minutes inside the cap" inverts to **8 minutes over the cap** → service credits are owed, not avoided. A recipient acting on this as-is under-reserves for a contractual liability.
- The orientation figure also moves: 288/131,040 → 99.7802%, i.e. 99.78%, not 99.80%.

This is the single highest-value correction on the page: a one-cell arithmetic error is the sole thing standing between "no credits owed" and "credits owed."

### C2 — The release-freeze conclusion is evaluated on the wrong window; the freeze is in fact active

**Location:** §4, final sentence (bolded); policy defined in §1 "Windows".

**Anchor:** `We are not in a release freeze under the error budget policy: 37.5% of the budget remains.`

**Problem:** The policy freezes releases on the trailing 30-day window, not the quarterly budget, and the 1–30 June window is 133.6% consumed — so checkout is in a freeze, the opposite of what §4 concludes.

Derivation, using the report's own definitions:
- §1 states the freeze rule verbatim: "The error budget policy is evaluated on a trailing 30-day window: releases to checkout pause while that window is more than 100% consumed," and fixes the window: "At this quarter's close the trailing 30-day window is 1–30 June."
- §1 states the budget rule: "0.1% of valid requests in the window, computed on the same denominator as the SLI."
- June valid = 434.0M → 30-day budget = **434,000**.
- June bad = **580,000**.
- Consumption = 580,000 / 434,000 = **133.6% — over 100%. Freeze condition met.**

The 37.5% quarterly headroom is real but irrelevant to the freeze test; §4 substitutes the reporting window for the policy window. The report defines the correct rule in §1 and then never applies it, which is the most likely way a reader misses it too.

Follow-on that the report should have stated: at the 2 July publication date the trailing window (~3 Jun – 2 Jul) still contains INC-4610 (447,000) and INC-4633 (115,000) plus ~18,000 background ≈ 580,000 against a ~434,000 budget ≈ 134% — still frozen. INC-4610 rolls out of the window around 12 July, after which burn falls to ~133,000 (~31%) and the freeze lifts. The proposed 13 July cadence change therefore sits one day past the earliest lawful resumption, on the assumption of a clean first eleven days of July. That is a fact leadership needs and the memo does not surface at all.

### C3 — The recommendation defers the capacity work that addresses the quarter's dominant failure mode, while doubling change rate into growing traffic

**Location:** §5.

**Anchor:** `move the release train from weekly to twice-weekly starting 13 July, and defer the two open reliability epics`

**Problem:** Both deferred epics — write-path capacity headroom and shed-aware client retries — target precisely the INC-4610 failure mode that produced 78% of incident failures, and traffic is compounding at ~4.7%/month toward the volumes that saturated the write path.

The stated mitigation does not cover the deferred risk. §3 says the fix was "reverted the same day and a capacity guardrail added to the pre-merge suite" — a CI guardrail catches a *config regression that shrinks the pool*. It does not create headroom, and it does not protect against the write path being exhausted by organic traffic growth at unchanged configuration. The report treats a regression guard as if it were a capacity fix.

Growth, from the report's own table: 410/396 = +3.54%; 434/410 = +5.85%; geometric mean **+4.69%/month**. Extrapolated: Jul 454.4M, Aug 475.7M, Sep 497.9M → Q3 ≈ 1,427.9M vs Q2 1,240.0M = **+15.2%**.

That last figure is the finding: §5 names ">+15%" as a condition that would invalidate the recommendation (see M5), and the quarter's own observed run rate already lands there. Recommending deferral of capacity headroom, doubling of change rate, or both, on this evidence is not supportable as written.

---

## Major

### M1 — The 612,000 shed 429s are excluded from the SLI, and under the SLO doc's own stated intent the quarter misses objective and blows the budget

**Location:** §1 exclusion (c); §3 INC-4610 narrative; conclusion in §5.

**Anchor:** `turned away a further 612,000 checkout requests with HTTP 429 until the write path recovered`

**Problem:** §1 defines the SLO's intent as the share of customer checkout attempts the platform completes, yet excludes edge-rejected 429s — so the platform's own load-shedding removes its largest failure population from the denominator instead of counting it.

The report itself supplies both halves of the contradiction: §1 says the intent is "to measure the share of customer checkout attempts that the platform completes successfully," and §1(c) excludes "requests rejected at the edge with HTTP 429 and never dispatched." A customer shed at the edge did not complete a checkout. The carve-out is defensible for third-party abuse rate-limiting — which is what "the platform SLI template's standard rate-limit carve-out" was written for — and indefensible for self-inflicted adaptive shedding during a self-inflicted outage. As applied, the SLI rewards shedding: the more aggressively checkout sheds, the better it scores.

Re-derived on the intent-faithful denominator:
- Valid = 1,240.0M + 0.612M = 1,240.612M
- Bad = 775,000 + 612,000 = 1,387,000
- Availability = 1 − 1,387,000/1,240,612,000 = **99.8882% — below the 99.9% objective**
- Budget = 0.1% × 1,240.612M = 1,240,612 → consumption = **111.8% — budget exhausted**
- June alone: 1,192,000 / 434.612M → **99.7257%**; 30-day consumption **274%**

So the headline claim in §5 — "The quarter finished above objective with over a third of the budget unspent" — holds only under the carve-out and inverts under the doc's own stated intent. The memo never runs this sensitivity, never states the 612,000 as a percentage of anything, and never flags that its single largest customer-impact population sits outside every number in §3 and §4. Leadership cannot make the roadmap call without it.

### M2 — The impact-window definition is deflated by the same exclusion, so impact-minutes are also understated

**Location:** §3 definition paragraph; INC-4610 row and narrative.

**Anchor:** `Impact window is first to last 1-minute bucket above a 1% checkout error ratio`

**Problem:** The error ratio is computed on valid requests, which exclude shed 429s, so once the shedder engaged at 14:11 the measured ratio fell mechanically and the window can close while customers are still being turned away.

The shedder "engaged at 14:11 ... until the write path recovered." Every request it rejected left the denominator *and* the numerator of the error ratio. The window is therefore not a measure of when customer harm stopped; it is a measure of when *counted* harm stopped. INC-4610's true customer-impact duration is not recoverable from this document, and the corrected 102 minutes (C1) is itself a floor, not an estimate. This matters directly for the MSA cap, where the metric is minutes.

### M3 — The MSA cross-check applies an in-house, deliberately narrow definition to a contractual cap without confirming the contract's definition

**Location:** §4, MSA cross-check; definition in §3.

**Anchor:** `impact minutes are the length of that window, not time-to-resolve. Postmortem clocks (detection to all-clear) run longer`

**Problem:** The report measures against MSA Schedule C using its own narrowest available clock while acknowledging a longer clock exists, without establishing which definition the contract actually binds.

The report concedes the alternative measure "run[s] longer" and then reports a 12-minute margin — a margin smaller than the gap between definitions is likely to be, and, after C1, a margin that does not exist at all. Two independent reasons the contractual conclusion is unsafe: the arithmetic (C1) and the definitional choice (here). Either alone warrants counsel review before this is asserted to leadership; together, "we closed inside the cap" should not appear in the memo without a quoted MSA definition of unavailability.

### M4 — "Unrelated to release velocity" is wrong on its own facts; 2 of 5 incidents and ~70% of incident failures were change-induced

**Location:** §5, second paragraph.

**Anchor:** `the other four were unrelated to release velocity — a config push, a planned failover, a cert expiry`

**Problem:** A bad config push is a change event, so the argument that only one incident related to change velocity misclassifies INC-4471 and undercounts the change-induced share used to justify doubling cadence.

From the report's own table: INC-4610 was "A connection-pool sizing change shipped that morning" (447,000) and INC-4471 was a "Bad config push, pricing sidecar" (60,000). That is **507,000 of 720,400 incident failures = 70.4%**, across 2 of 5 incidents, attributable to changes reaching production. The memo's central causal claim for doubling the release train is that change velocity was not implicated in Q2; its own data says change velocity was the majority of Q2's incident load. Whether config pushes ride the release train is a fair question — but the memo asserts irrelevance rather than establishing it.

### M5 — The RUM discrepancy is dismissed without accounting for the known, quantified server-side cause sitting in the same document

**Location:** §2, second paragraph.

**Anchor:** `That gap is expected — RUM also captures client network failures, app crashes, and session abandonment`

**Problem:** The gap is attributed entirely to client-side causes when the excluded 612,000 shed 429s — a server-side cause the report itself reports — account for roughly two-thirds of it.

Derivation: RUM 99.86% vs SLI 99.9375% → gap **0.0775pp** ≈ 961,000 requests. The shed 429s are 612,000 / 1,240.0M = **0.0494pp**, i.e. **~64% of the gap**. Adding them back gives 99.888%, materially closer to RUM's 99.86% and consistent with the residual being genuine client-side loss. The RUM signal is corroborating M1, and the report reads it as noise. Using the divergence as evidence *for* the carve-out being wrong is the analysis that should have been run; instead the paragraph closes the question.

---

## Minor

### m1 — Good/bad/valid do not partition, and §2 describes a formula the table does not use

**Location:** §1 definitions; §2 pooling description; §3 table.

**Anchor:** `Quarterly availability is pooled — total good over total valid`

**Problem:** A 429 that was dispatched to the service is valid but is neither good (excluded by "4xx other than 429") nor bad (not 5xx, not a timeout), so good/valid and 1 − bad/valid are not the same quantity.

Every figure in the table is 1 − bad/valid, verified above. If dispatched 429s are non-zero, §2's stated method and the table's actual method diverge. Either widen "good" to cover them, or state that availability is computed as 1 − bad/valid. Low materiality, but it is a definitional hole in a document whose numbers are otherwise exact.

### m2 — Fail-closed fraud declines: classification unstated, and the SLI would score them as good

**Location:** §3 incident table, INC-4562.

**Anchor:** `Expired mTLS cert, fraud service; risk-threshold requests failed closed`

**Problem:** If fail-closed declines surfaced to clients as non-429 4xx they count as good requests under §1, so the 53,400 figure may not capture the full customer impact of this incident.

The per-month reconciliation confirms 53,400 *were* counted as bad, so the stated number is not itself in doubt. The open question is whether additional declines were emitted as 4xx and silently scored as successes. One sentence naming the status code returned during the incident would close this.

### m3 — A planned operation that produced 51 minutes and 45,000 failures is waved past rather than analysed

**Location:** §3 INC-4519; §5 characterisation.

**Anchor:** `a planned failover`

**Problem:** Framing INC-4519 as planned is used to excuse it from the velocity argument, but a scheduled failover costing 45,000 checkouts is a reliability finding in its own right that the memo never engages.

Correctly out of scope for *release velocity*. Incorrectly out of scope for a quarterly reliability review, since planned-operation impact is among the more tractable things on this list.

### m4 — Re-evaluation triggers are unowned and partly undefined

**Location:** §5, final paragraph.

**Anchor:** `This changes if a second saturation-class incident lands in July, or if the Q3 traffic forecast is revised above +15%`

**Problem:** Neither trigger names an owner, a review date, or a definition of "saturation-class," and no baseline Q3 forecast appears anywhere in the document to revise against.

Separately from C3 — which is that the +15% trigger is already met by observed data — a trigger with no owner and no stated baseline cannot fire. If these conditions genuinely gate the recommendation, they need a named owner and a scheduled checkpoint.

---

## Bottom line

The measurement and data work is strong: every availability figure, sum, budget percentage and per-month reconciliation is exact, and four of five impact windows are right. The failures are not in the arithmetic engine but in one uncaught cell and in the reasoning stacked on top of it.

Three things must change before this goes to leadership:

1. **Fix INC-4610 to 102 minutes.** The quarter is 288 impact-minutes and 8 minutes *over* the MSA cap. Escalate the credit exposure rather than reporting headroom.
2. **Re-run the freeze test on the trailing 30-day window.** June is 133.6% consumed; checkout is frozen, and the earliest lawful resumption is ~12 July — the memo's "not in a release freeze" statement is the reverse of its own policy.
3. **Report the quarter both ways on the 429 carve-out.** With the 612,000 shed requests counted, Q2 is 99.888% — below objective — and the budget is 111.8% consumed. The recommendation currently rests on a carve-out that removes the quarter's largest customer-impact population from every number.

The "Ship" recommendation does not survive any of the three corrections, and least of all the combination of deferring write-path capacity while traffic compounds at ~4.7%/month toward the +15% threshold the memo itself names as disqualifying.

**Totals: critical 3, major 5, minor 4.**
