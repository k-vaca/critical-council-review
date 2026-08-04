# Critical Council Review — "Why customers stay: the Workflows effect"

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Reject and rework.** The memo's causal claim, its headline projection, and its adoption target each fail against its own printed numbers, so the Finding, Conclusion and Recommendation cannot be repaired by editing — they must be re-derived, and the answer may reverse.

1. **Re-run churn within each segment and plan tier, with usage banded** (Data, L13 — usage was already pulled and never used). This is the analysis that decides whether the effect exists.
2. **Show the derivation of "9.6%" and "$2.1M"** (Conclusion, L41). On the memo's own rates, 40% adoption yields ≈12.0% blended, not 9.6%.
3. **Restate the target against the eligible base and drop "every new account"** (L37, L45) — Workflows is plan-gated.

## 2. Result & standard

Third-party artifact, not my own prior output. Judged: `claim-06-churn-analysis.md` (≈390 words), a decision memo whose stated **Ask** is "approve moving two engineers onto Workflows adoption for H2" (L5). That ask is the claim under review, not an instruction to this council; the memo contains no other text addressed to a reviewer.

**Standard.** The memo's own question (L9) plus the ordinary bar for observational analysis used to justify a causal recommendation: either adjust for the confounders you can see, or state the finding as association and price the recommendation accordingly. A benefit projection in a resource-allocation memo must also reproduce from the figures printed beside it.

**Tier 2** (single deliverable), 3 seats, all eight fields. The expensive-decision trigger argues for tier 3, but tier 3's 4–6 seats conflicts with the requester's fixed roster; I ran tier 2 depth and capped the confidence note instead. **Independence mechanism: sequential seats** (Step 3 fallback) — no subagent tooling available for this run.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | L37, "Workflows requires the SSO integration, which is available on Business and Enterprise plans only" | Workflows is plan-gated, so the comparison largely reproduces plan/segment differences; no evidence any gap survives adjustment | Report churn for Workflows vs not *inside* each segment and plan tier | Corrected |
| Critical | L41, "cut blended churn from 14.8% to an estimated 9.6%" | Does not reproduce: the memo's own rates give ≈12.0% at 40% adoption, roughly halving the benefit | Publish the derivation and weighting, or restate the number | Corrected |
| Critical | L41, "from the current 21% to 40%" | 40% needs 1,597 more accounts; only 1,133 un-enabled Enterprise+Mid-market exist, so it requires plan upgrades not in the ask | Set the target against the eligible base; ceiling is ≈34.5% | Corrected |
| Major | L45, "a step in the standard implementation process for every new account" | Inoperable where the plan gate binds; among Small accounts (72% of base) only 9% have Workflows | Scope the step to eligible plans; state the upgrade path separately | Corrected |
| Major | L15, "purges account records twelve months after closure" | Tenure bands are survivor-conditioned and no time-ordered re-analysis is possible on this extract | Source pre-purge churn history before re-running | Corrected |
| Major | L13, "as of 1 July 2026"; L19 module status | No enablement dates, so nothing shows Workflows preceded the retention it is credited with | Compare churn after enablement date, not at snapshot | Confirmed |
| Major | L13, "monthly active usage" | The most obvious rival explanation was pulled and never reported anywhere in the memo | Add usage-banded churn; report it even if it kills the finding | Confirmed |
| Major | L45, Recommendation | No cost of two engineers, no ARR base, no time-to-impact, no alternative lever compared | Add the cost side and one competing use of the same headcount | Confirmed |
| Minor | L19, "churn at 4.1% annually" | Churn is never defined — annualized how, over which window, account- or ARR-weighted | State the metric definition once, up front | Unverified |
| Minor | L41, "14.8%" | Does not reconcile with the memo's own mix: 21% × 4.1% + 79% × 17.3% = 14.5% | Reconcile or footnote the weighting | Confirmed |
| Minor | L19–L27, all rates | No intervals anywhere; some implied cells are small (≈96 un-enabled Enterprise accounts) | Add counts and intervals per cell | Unverified |

## 4. Council roster

Roster fixed by the requester — disclosed, not treated as a constraint I chose. Three seats: **Methodology & statistics** (does the arithmetic support the claim), **Data & inference validity** (does the conclusion follow from this data), **Decision red-team** (does the recommendation survive contact with reality; owns the recipient's viewpoint).

**Deliberately not covered.** *Product/engineering feasibility* — whether two engineers can move adoption at all, and what decoupling Workflows from the SSO gate would cost. A critical defect could live here: if the gate is cheap to remove, the right allocation is a different one entirely. *Commercial/pricing* — whether pushing Workflows down-market cannibalizes plan upgrades. *Data engineering* — whether the CRM fields mean what the memo says. No seat was added; the confidence note is capped accordingly.

## 5. Individual analyses

### Seat 1 — Methodology & statistics

**Role & remit.** Design, power, inference: whether the numbers printed here support the claim built on them.

**Assessment.** The descriptive layer is competent and the study is a census rather than a sample, so ordinary sampling error is not the problem. The inferential layer is where it breaks: the memo performs one stratification, presents it as robustness, and then extrapolates a business case that its own figures do not produce.

**Strengths.** The segment table reconciles exactly — 505 + 1,851 + 6,056 = 8,412, and the enabled counts sum to 1,768, which is the stated 21%. That is real internal discipline and I verified it independently.

**Weaknesses.** *Critical, defect* — "Driving adoption from the current 21% to 40% would cut blended churn from 14.8% to an estimated 9.6%" (L41). Applying the memo's own rates, 0.40 × 4.1% + 0.60 × 17.3% = 12.0%. The claimed 5.2-point drop is about 2.8 points, and no derivation is shown. *Major, defect* — "The gap holds across tenure bands" (L21) is offered as a robustness check, but stratifying on tenure controls tenure and nothing else; the standard applied is that a robustness check must vary the variable the objection names. *Minor* — no intervals, no cell counts, no definition of the churn metric.

**Gaps.** No stated denominator, no per-cell counts, no sensitivity analysis on the projection's single assumption.

**Strongest reason this might be fundamentally wrong.** The whole memo may be measuring eligibility rather than behaviour: if Workflows is available only to accounts that already differ on everything that drives churn, then the 4.1% versus 17.3% contrast has no causal content and the recommendation follows from an artefact of who is allowed to buy the module. (Overlaps Seat 2's remit; reported because I can see it.)

**Domain verdict.** Below the bar. A competent analyst may present an unadjusted contrast, but not extrapolate a dollar figure from it without showing the arithmetic.

**Recommended fixes.** Publish the projection's working; add counts and intervals to every rate; define churn.

### Seat 2 — Data & inference validity

**Role & remit.** Sampling frame, confounds, measurement, and whether the conclusion follows from the data shown.

**Assessment.** The extract is honestly described and the memo volunteers two limitations that most would omit. It then draws a causal conclusion that those very disclosures rule out.

**Strengths.** The purge disclosure (L15) and the plan-gating disclosure (L37) are both present and unforced. The memo contains the material needed to refute itself, which is more integrity than the conclusion shows.

**Weaknesses.** *Critical, defect* — "Workflows requires the SSO integration, which is available on Business and Enterprise plans only" (L37). Enabled share runs 81% Enterprise, 44% mid-market, 9% Small; the Workflows/no-Workflows split is therefore close to a plan-and-size split, and no figure in the memo separates them. *Major, defect* — "purges account records twelve months after closure" (L15): every account that left more than a year ago is gone, so the tenure bands compare survivors to survivors. *Major, defect* — module status is read "as of 1 July 2026" (L13) with no enablement dates, so the memo cannot show enablement preceded retention rather than accompanying it. *Major, gap* — "monthly active usage" is pulled (L13) and appears nowhere again; the leading rival explanation was in hand and left unreported.

**Gaps.** No within-segment table, no usage cut, no plan-tier breakdown — each constructible from the fields already extracted.

**Strongest reason this might be fundamentally wrong.** Enabling a module may simply mark an account that has already committed — bought a higher plan, configured SSO, assigned an admin. On that reading the arrow points backwards: retention causes adoption.

**Domain verdict.** The conclusion does not follow. The data can support "Workflows accounts churn less"; it cannot support "Workflows is the strongest retention lever" (L41).

**Recommended fixes.** Run churn by segment × plan × Workflows; band by usage; use enablement dates to establish time order.

### Seat 3 — Decision red-team

**Role & remit.** Whether the recommendation survives contact with reality, standing in for the approver who must fund it.

**Assessment.** Even granting the causal claim in full, the plan cannot deliver what it promises, because the target sits outside the population that is allowed to adopt.

**Weaknesses.** *Critical, defect* — 40% of 8,412 is 3,365 accounts, 1,597 more than today. Un-enabled Enterprise (96) plus mid-market (1,037) totals 1,133. The target is unreachable without converting roughly 464 Small accounts that must first buy a plan upgrade — a commercial motion nowhere in the ask. *Major, defect* — "make Workflows setup a step in the standard implementation process for every new account" (L45) collides with the plan gate at L37. *Major, gap* — the memo states a benefit and never a cost: no engineering cost, no ARR base behind "$2.1M", no time-to-impact within H2, no competing use of the same two engineers.

**Gaps.** No downside case, no leading indicator that would tell the approver in-quarter whether the bet is working.

**Strongest reason this might be fundamentally wrong.** The strongest case against acting is that the highest-value engineering action may be the opposite of the ask: if the plan gate is what suppresses adoption, two engineers spent removing the SSO dependency would beat two spent on onboarding — and the memo never considers it.

**Domain verdict.** Not fundable as written. The ask is specific; the evidence and the arithmetic behind it are not.

**Recommended fixes.** Recompute against the eligible base; add the cost side and one alternative; name an in-quarter leading indicator and a kill criterion.

## 6. Executive review

I re-read the artifact in full before writing this.

**Points of agreement.** One, and it is **deduplicated here and deleted from both seats**: the benefit case overstates itself (methodology, red-team). Under the sequential fallback this is **marked sole-source** — the seats shared a context, so their convergence is not evidence and I have not upweighted the finding for it. It stands on arithmetic I re-checked myself: 0.40 × 4.1 + 0.60 × 17.3 = 12.0, and at the realistic ceiling of ≈34.5% adoption, ≈12.75% — a 2.05-point improvement, under 40% of the 5.2 points claimed.

**Points of conflict & adjudication.** No seat contradicted another. Two rulings on severity rather than substance. First, the red-team called the 40% target "arithmetically unreachable"; I narrowed it — "Small" is a seat band, not a plan tier, and 545 Small accounts already have Workflows, so the route exists via plan upgrades. It stays critical because the upgrade motion is absent from the ask and the benefit case collapses without it. Second, I checked every critical and major anchor in the source myself; none rests on a seat's paraphrase.

**Verification result.** Twelve candidate findings entered Step 5, **one withdrawn**, eleven published. Methodology flagged that the headline 4.1% might not reconcile with bands 6.2 / 3.9 / 2.4; a tenure mix of roughly 30/40/30 gives 4.14%, so the rates are consistent and the flag was wrong. Five findings were narrowed. Searched and located: "estimated 9.6%" (L41), "current 21% to 40%" (L41), "Business and Enterprise plans only" (L37), "twelve months after closure" (L15), "monthly active usage" (L13), "every new account" (L45), "as of 1 July 2026" (L13). No seat's reliability is in question; the withdrawn item was raised as a check, not asserted.

**Panel blind spots.** All three seats assumed the printed figures are faithfully extracted from the CRM — none can verify that, and it is load-bearing for every number above. All three assumed account-weighted churn; if the memo means ARR-weighted, the reconciliation findings soften though the confound does not. All three treated Workflows as a binary rather than a marker of configuration depth. Because the seats shared one context, their coverage gaps are likely shared too: **no seat examined product/engineering feasibility**, and a critical defect could live there — if decoupling Workflows from the SSO gate is cheap, the correct recommendation is a different allocation entirely, and no one on this panel looked.

**Overall judgment.** A well-organised memo built on a real census, disclosing its own two most damaging limitations, that then draws a causal conclusion those limitations forbid and prices it with arithmetic that does not reproduce. The question is worth asking and the extract is worth keeping. Everything from "Finding" onward is not yet decision-grade.

**Decision on further action: reject and rework.**

**Prioritized next steps.** (1) Churn by segment × plan × Workflows, with usage banded — data already pulled; this decides whether the effect exists. (2) Republish the projection with its derivation, against the eligible base. (3) Establish time order from enablement dates. (4) Add the cost side and one alternative — including costing removal of the SSO gate. (5) Only then re-submit the headcount ask.

**Confidence & what would change the verdict.** Of the eight findings at critical or major, I expect seven to survive an independent expert re-check. The first to fall is the "every new account" finding — segment is a seat band, not a plan tier, and if new business skews Business-plan-and-above it drops to minor. Next is the purge finding: a trailing-twelve-month churn definition would leave the headline rate unbiased, which is why I narrowed it to the tenure table and the re-analysis. The verdict rests on verified arithmetic anyone can reproduce from the memo's own tables, plus a checkable absence — no within-segment figure appears anywhere. It flips to "approve with minor revisions" on one exhibit: a table showing the churn gap persisting inside each segment and plan tier with usage controlled, alongside a derivation that reproduces 9.6% and $2.1M. It does **not** cover product/engineering feasibility or pricing; a defect in either would change the recommended action even if every finding above holds.
