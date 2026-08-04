# Review — claim-06-churn-analysis.md

**Artifact:** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/claim-06-churn-analysis.md`
**Review type:** single expert pass (quantitative analysis / causal inference / decision memo)

## Verdict

The memo does not support its conclusion. The headline comparison is confounded by a
constraint the document itself states but never acts on, the central projection contains
an arithmetic error that roughly doubles the claimed benefit, and the adoption target that
drives the dollar figure is not reachable given the eligibility structure shown in the
memo's own segment table. The recommendation should not be approved as written.

## What is sound

- Segment table is internally consistent: 505 + 1,851 + 6,056 = 8,412, and the weighted
  enablement rate (409 + 814 + 545 = 1,769 accounts) reproduces the stated 21% adoption.
- The CRM purge window is disclosed up front rather than buried, which is good practice
  and is more transparency than most memos of this kind offer.
- The question, the ask, and the data pull are stated plainly at the top.

---

## Findings

### CRITICAL

**C1 — Finding section (lines 19–27), read against line 37: the comparison is confounded and no segment control is presented.**
Anchor: *"Workflows requires the SSO integration, which is available on Business and Enterprise plans only."*
Problem: Because Workflows is gated behind higher plan tiers, the "not enabled" group is
overwhelmingly small accounts (6,056 of 8,412, with 9% adoption), so the 4.1% vs 17.3% gap
measures plan tier and account size at least as much as it measures Workflows — and the
memo never shows churn within segment, which is the one table that would separate the two.

Supporting detail: with 81% Enterprise adoption and 9% small-account adoption, the
Workflows cohort is composed almost entirely of the accounts you would expect to retain
best regardless of module usage. Nothing in the memo rules that out.

**C2 — Conclusion (line 41): the projected churn figure is arithmetically wrong.**
Anchor: *"Driving adoption from the current 21% to 40% would cut blended churn from 14.8% to an estimated 9.6%"*
Problem: Applying the memo's own rates at 40% adoption gives 0.40 x 4.1% + 0.60 x 17.3%
= **12.0%**, not 9.6%, so the claimed reduction (5.2pp) is roughly double the reduction the
stated assumptions actually produce (~2.5pp), and the $2.1M ARR figure inherits the same
overstatement.

Supporting detail: the same 2.5pp results from the shift-based framing
(19pp of accounts moving from 17.3% to 4.1% = 0.19 x 13.2 = 2.5pp). No reading of the
memo's numbers yields 9.6%; that value corresponds to ~58% adoption, not 40%.

**C3 — Conclusion / Recommendation (lines 41, 45): the 40% adoption target is not reachable through onboarding.**
Anchor: *"Driving adoption from the current 21% to 40%"*
Problem: 40% of 8,412 requires ~3,365 enabled accounts versus ~1,769 today, a gap of ~1,596,
but total remaining headroom in Enterprise (96 accounts) plus Mid-market (1,037) is only
~1,133 — so even 100% adoption across both larger segments lands near 34%, and the target
cannot be hit without a plan-upgrade motion for small accounts that the memo never mentions
and the two-engineer ask does not fund.

---

### MAJOR

**M1 — Finding section (line 21): the robustness check stratifies on the wrong variable.**
Anchor: *"The gap holds across tenure bands:"*
Problem: Tenure is not the suspected confounder — plan tier and account size are — so a
tenure-stratified table creates an impression of having controlled for selection while
leaving the actual confound entirely untested.

**M2 — Conclusion (line 41): an observed rate among self-selected adopters is applied to induced adopters.**
Anchor: *"Workflows is the strongest retention lever in the product."*
Problem: The projection assumes accounts pushed onto Workflows by an onboarding mandate will
churn at 4.1%, the rate observed among accounts that chose it and qualified for it, which is
an effect-on-the-treated silently reused as an effect-on-everyone with no supporting evidence.

**M3 — Conclusion (line 41): the dollar figure has no derivation.**
Anchor: *"worth roughly $2.1M in retained ARR"*
Problem: No ARR base, no revenue per account, no assumption about whether retained accounts
are valued at average or segment-specific ARR is given, so the figure cannot be checked,
adjusted, or reproduced by the approver.

**M4 — Recommendation (line 45): the operational instruction contradicts the eligibility constraint stated in the same document.**
Anchor: *"make Workflows setup a step in the standard implementation process for every new account"*
Problem: Line 37 states Workflows requires SSO, available only on Business and Enterprise
plans, so this step is not executable for the small-account majority (72% of the base) and
the recommendation needs to be rescoped to eligible accounts before it can be actioned.

**M5 — Data section (line 13): the module-enabled field is a point-in-time snapshot with no stated temporal relationship to churn.**
Anchor: *"which product modules the account has enabled"*
Problem: Enablement is read as of 1 July 2026 while churn is measured over a prior window,
and if the CRM clears or downgrades module flags on closure, churned accounts would
systematically appear as non-adopters and would manufacture the entire finding — the memo
must establish that enablement was measured *before* the churn window and that closed
accounts retain their flags.

**M6 — Data and Finding sections: churn is never defined and no counts are shown.**
Anchor: *"Accounts with the Workflows module enabled churn at 4.1% annually."*
Problem: There is no churn definition (logo vs revenue), no measurement window, no
denominator statement for whether the 8,412 mixed open-and-closed extract is the base, and
no cell counts or confidence intervals anywhere in the tenure table — so a reader cannot
tell whether the 3+ year Workflows cell rests on 15 accounts or 1,500, nor reproduce any
figure.

**M7 — Data section (line 13): the most relevant control was collected and then not used.**
Anchor: *"we pulled tenure, seat count, segment, monthly active usage, and which product modules the account has enabled"*
Problem: Monthly active usage and seat count are exactly the engagement and size controls
that would test whether Workflows adoption is a cause of retention or merely a marker of
already-engaged accounts, and neither appears anywhere in the analysis.

---

### MINOR

**m1 — Conclusion (line 41): the stated baseline does not reconcile with the memo's own inputs.**
Anchor: *"cut blended churn from 14.8%"*
Problem: 21% adoption at 4.1% and 79% at 17.3% gives 14.5%, not 14.8%, so either the
baseline comes from a different (undisclosed) calculation or one of the inputs is stale.

**m2 — Finding section (line 19): loose statistical phrasing.**
Anchor: *"Workflows users are more than four times less likely to leave."*
Problem: 17.3 / 4.1 = 4.2 is a relative risk ratio, and "four times less likely" is an
imprecise way to state it that invites misquotation in downstream decks.

**m3 — Ask and Recommendation (lines 5, 45): a headcount request with no cost side.**
Anchor: *"approve moving two engineers onto Workflows adoption for H2."*
Problem: The memo presents an upside estimate with no cost of the two engineers, no
opportunity cost of what they stop working on, and no comparison against alternative
retention levers, which is the minimum an approver needs.

---

## What would fix this

1. Rebuild the headline comparison **within** plan tier and segment — churn for Workflows
   vs non-Workflows accounts restricted to Business/Enterprise accounts only. If the gap
   survives that cut, the argument has a foundation; if it collapses, the memo is done.
2. Establish temporal ordering: enablement state as of the start of the churn window, and
   confirm the CRM does not strip module flags at closure.
3. Recompute the projection. On the memo's own (still-confounded) rates, 40% adoption gives
   12.0%, and the ARR figure should be roughly halved and shown with its derivation.
4. Re-derive an achievable adoption ceiling from eligible accounts only, and rescope the
   recommendation to eligible accounts.
5. Publish cell counts and confidence intervals for every rate.

## Totals

Critical: 3 | Major: 7 | Minor: 3
