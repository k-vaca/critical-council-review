# Critical council review — Storage capacity forecast, object store, FY27

Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Revise substantially before use.** The forecasting core is sound — all three scenario endpoints reconcile exactly from the stated inputs — but the decision built on it is not: the one number converting bytes into the procurement call is unsourced and untested, and the section telling the reader when to revisit names no trigger that would cross the threshold.

1. Derive and sensitivity-test the 2.5 PB threshold (§What we are forecasting) — the two prices, the term, the shortfall terms.
2. Recompute the 1.95 PB deletion sensitivity (§What would change this, bullet 3); the stated units give ~1.85 PB.
3. Replace "a third large migration would cross it" (§Conclusion) with the TB required — >330 TB, ~3× the contracted average.

## 2. Result & standard

Judged: the artifact in full (51 lines, ~640 words), no sampling. Not my own prior output. **Standard:** its own stated purpose — "decide whether to commit to a larger reserved-capacity tier before the 1 November deadline" — plus what a competent forecaster owes a document that issues a procurement recommendation: reproducible arithmetic, honest uncertainty, a sourced decision criterion. **Tier 2**, 3 seats, all eight fields. **Sequential seats** (Step 3 fallback) — no subagent tooling this run. No text in the artifact is addressed to its reviewer; the nearest line, "See "What would change this" before acting", directs the decision-maker and does not bound this review. The requester fixed the roster and made no claim about quality, so there is no framing to quarantine.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | §What we are forecasting: "the 2.5 PB threshold at which the next reserved tier becomes cheaper than on-demand" | The sole criterion converting forecast into recommendation is unsourced and never sensitivity-tested, while four lesser inputs are | State prices, term, shortfall terms; test ±20% | Corrected |
| Major | §Conclusion: "close enough that a third large migration would cross it" | False at the document's own sizing; crossing needs >330 TB against a ~105 TB contracted average | Give the TB required to cross | Corrected |
| Major | §What would change this: "roughly 1.95 PB" | Overstates the deletion effect ~8× under assumption 4's denominator, or silently re-bases it | Recompute to ~1.85 PB, or state the basis | Confirmed |
| Major | §Conclusion: "Under all three scenarios we stay below 2.5 PB on 31 October 2027." | Three hand-built paths presented as a bound; no interval, and named triggers sit outside them | Say these are paths; add a combined-trigger path | Confirmed |
| Major | §Recommendation: "will have either landed or lapsed" vs §Method: "Neither has a confirmed date." | Asserts a resolution the document denies exists; no decision shown to be available in April | Tie review to a contract milestone; state the decision calendar | Confirmed |
| Major | §Method: "Growth returns to 38%/yr" vs §Known weaknesses: "it covers only one enterprise migration" | Never says whether that migration was stripped from the 38%; the high case may double-count inflow | State it; recompute organic growth if not | Confirmed |
| Major | §Assumptions we are making, items 1–3 | Every named risk moves the total away from the threshold; only contracted migrations push toward it | Name and size one unmodelled upside driver | Confirmed |
| Minor | §What would change this: "diverging by more than 5%, which would mean one of them is wrong" | They already disagree 1–3% every month, so one is already wrong; 5% is arbitrary | Reconcile the gap or state it as known bias | Confirmed |
| Minor | §Method: "the two pending enterprise migrations land in Q1" | 210 TB bolted on flat, uncompounded (~+45–70 TB by Oct 2027); "Q1" undefined | Compound from landing date; define the fiscal calendar | Confirmed |

## 4. Council roster

Roster specified by the requester — disclosed per Step 2, honored as given, verdict capped below.

1. **Methodology & statistics** — the load-bearing output is computed figures; someone must check the arithmetic and whether stated uncertainty matches the real one.
2. **Data & inference validity** — the forecast rests on one of two disagreeing sources and a named assumption set; someone must check the conclusion follows.
3. **Decision red-team** — the artifact issues a procurement recommendation, not just a forecast; the required skeptic, and the seat standing in for whoever must act.

**Not covered.** *Procurement / cloud cost engineering* — the threshold's derivation, term, reversibility, shortfall penalties; a critical defect could live here and seat 3 can flag the absence but not verify the number. *Storage systems engineering* — replication factor, erasure-coding overhead, whether billed bytes include replicas, metadata or abandoned multipart uploads; a critical defect could live here, since a replication change moves the baseline by a multiple, not a percent.

## 5. Individual analyses

### Seat 1 — Methodology & statistics

**Role & remit.** Forecast design, arithmetic reproducibility, and whether stated uncertainty matches actual uncertainty.

**Assessment.** Point arithmetic correct and independently reproducible; the uncertainty representation is not. Three hand-built paths are presented as though they bounded the outcome.

**Strengths.** All three endpoints reconcile from the stated inputs under the document's own monthly compounding: 1.31 × 1.22^1.25 = 1.68, × 1.31^1.25 = 1.84, × 1.38^1.25 + 0.21 = 2.17 PB; 2.17/2.5 = 87%. It also tests a competing functional form — "a linear fit to the last 12 months gives 1.71 PB" — and reports it though it does not flatter the model.

**Weaknesses, risks & errors.** *Major, defect* — the deletion sensitivity fails its own units. Standard applied: a sensitivity figure must be recomputable from the model it perturbs. Assumption 4 sets deletion at "2–4% of monthly writes"; dropping below 1% shifts net monthly growth ~0.05pp, giving ~1.85 PB, not "roughly 1.95 PB" — ~8× overstated, unless the trigger silently re-bases to percent-of-total, which is never said. *Major, defect* — "Under all three scenarios we stay below 2.5 PB on 31 October 2027" claims coverage the method cannot supply: no probabilities, no interval, and the document's own triggers name events outside the high path. *Minor, defect* — migrated bytes are added flat rather than compounded from landing, and "Q1" is tied to no stated fiscal calendar.

**Gaps.** No interval, no probability weights, no seasonality or serial-correlation treatment, and no stated error on a base rate annualised from only six points.

**Strongest reason this might be fundamentally wrong.** If the one observed enterprise migration sits inside the trailing-12-month window, the 38% is contaminated by a one-off step and the high scenario double-counts — an inflated rate plus two further migrations. Stripping ~105 TB from a ~0.95 PB base puts organic growth nearer 27% and the high case nearer 1.98 PB. The document never says when it landed.

**Domain verdict.** Arithmetic competent and checkable; uncertainty representation below the bar for a forecast used to decline a procurement option.

**Recommended fixes.** Say whether the observed migration was stripped from the rate. Recompute the deletion sensitivity or declare its denominator. State that the scenarios are paths, not bounds, and add one combined-trigger path.

### Seat 2 — Data & inference validity

**Role & remit.** Sampling, measurement, confounds, and whether the conclusion follows from the data shown.

**Assessment.** The data choice is defensible and disclosed. The inference to "we stay below 2.5 PB" leans on an assumption set running almost entirely one way.

**Strengths.** It discloses that its sources conflict — "The two disagree by 1–3% in every month" — and forecasts the billing export with a stated reason: it is the figure charged on. For a cost decision that is the right source, and naming the conflict beats burying it.

**Weaknesses, risks & errors.** *Major, defect* — the risk register is asymmetric. Standard applied: a forecast used to *decline* capacity must enumerate how it could be too low, the only direction in which it is costly. Assumptions 1–3 are all downside — shortened retention removes 340 TB, a departing account removes bytes, the encoder is unchanged — so every violation moves further from the threshold. The only upward driver anywhere is the two contracted migrations; no unmodelled upside (new products or regions, replication or backup policy, a less-compressible data type, pipeline beyond the named deals) appears at all. Anchor: "Our three largest accounts hold 41% of stored bytes between them." *Minor, defect* — the divergence trigger contradicts the data section: if the sources disagree *every* month, one is already wrong, so 5% cannot be where that becomes true. Immaterial to the decision (±3% on the base is ±55 TB against 660 TB headroom), hence minor.

**Gaps.** No per-account or per-workload decomposition. The 41% concentration is stated then never used; growth is modelled only in aggregate.

**Strongest reason this might be fundamentally wrong.** Aggregate-only modelling may hide a mix shift. If the 38%→31% deceleration comes mostly from the three largest accounts saturating while a long tail keeps compounding, the aggregate is a blend that re-accelerates as the tail's weight grows, and both base and low are biased low. Nothing in the artifact lets a reader rule this in or out.

**Domain verdict.** Data handling sound and honestly disclosed; the inference is under-supported, because the risk set is one-sided in exactly the direction that matters here.

**Recommended fixes.** Add and size one upside driver not tied to the contracted migrations. Decompose growth into top-3 accounts versus the tail and show both rates.

### Seat 3 — Decision red-team

**Role & remit.** Whether the recommendation survives contact with reality, and the strongest case against acting on it.

**Assessment.** This document does not stop at a forecast; it makes a procurement call. It sources every input except the one the call turns on.

**Strengths.** It commits to a specific action rather than hedging, states confidence as moderate rather than certain, and volunteers its own weaknesses — the high scenario "rests on a single prior observation" — unprompted. Forecasting the horizon endpoint is also the right conservative statistic for a crossing question, since under monotone growth the endpoint is the maximum.

**Weaknesses, risks & errors.** *Critical, defect* — the 2.5 PB threshold is asserted with no source, no derivation and no sensitivity, while four lesser inputs get sensitivity treatment. No price, rate, commitment term or shortfall penalty appears anywhere. This undermines the Step 1 purpose directly — "decide whether to commit to a larger reserved-capacity tier before the 1 November deadline" — because if the true crossover sits nearer 1.9 PB the base case already crosses and the recommendation inverts, and nothing in the artifact lets the reader check. `[unverified — recall, not lookup]` as to the threshold's real value; the defect claimed is the absence of basis and of sensitivity, not that the number is false. *Major, defect* — the recommendation asserts a future fact its own text denies: "will have either landed or lapsed" against "Neither has a confirmed date." Undated contracts do not acquire a resolution date by being deferred. Compounding it, the document never says whether the 1 November deadline recurs or the tier can be entered mid-term, so "Re-run this forecast in April 2027" may attach to no available decision.

**Gaps.** No cost of being wrong in either direction. Reserved commitments are typically asymmetric — shortfall penalty against forgone discount — and this treats the call as a symmetric comparison of bytes to a line.

**Strongest reason this might be fundamentally wrong.** It answers "will we cross 2.5 PB on one date" when the procurement question is "which pricing is cheaper across the term". Those coincide only if the crossover is a level threshold on peak usage. If it is defined on average usage, or on committed rather than consumed volume, the byte forecast — however accurate — is the wrong statistic and does not decide the question it exists to decide.

**Domain verdict.** Not decision-grade. The forecast is usable; the recommendation built on it is not.

**Recommended fixes.** Put the two prices, the term and the shortfall terms in the document. Sensitivity-test the threshold as it already does four lesser inputs. State the decision calendar and whether April 2027 is actionable.

## 6. Verification pass (Step 5)

Every critical and major finding re-checked adversarially; each quoted string searched for in the artifact rather than recalled. Minors were verified too, so none is labelled unverified.

- **Threshold unsourced** — searched "the 2.5 PB threshold at which the next reserved tier becomes cheaper than on-demand", found §What we are forecasting. **Corrected.** Challenge: a capacity forecast need not re-derive vendor pricing. It survives only because this document makes the call itself ("do not commit to the larger tier this year"); restated as *a document that makes the call must source the criterion it turns on*.
- **Third migration crosses** — searched "close enough that a third large migration would cross it", found §Conclusion. **Corrected.** Challenge: "large" is undefined, so not flatly false. Crossing needs >330 TB; at the only sizing given ("210 TB combined", ~105 TB each) a third yields 2.275 PB. Restated as unsupported-as-written, true only above ~3× the contracted average.
- **1.95 PB sensitivity** — searched "roughly 1.95 PB" and "2–4% of monthly writes", found §What would change this and assumption 4. **Confirmed**; the ~8× gap follows from the document's own denominator.
- **Scenarios as bound** — searched "Under all three scenarios we stay below 2.5 PB on 31 October 2027.", found §Conclusion. **Confirmed**; the trigger list beneath names events outside all three paths.
- **April resolution** — searched "Neither has a confirmed date." and "will have either landed or lapsed", found §Method and §Recommendation. **Confirmed**; direct internal contradiction.
- **Rate contamination** — searched "it covers only one enterprise migration", found §Known weaknesses. **Confirmed**; the migration's timing is absent, which is the finding.
- **One-sided assumptions** — searched "Our three largest accounts hold 41% of stored bytes between them.", found §Assumptions item 2. **Confirmed**; all three named risks run away from the threshold.

**Withdrawn: 1.** A drafted criticism that the base case wrongly holds 31% flat while growth visibly decelerates (38%→31%) was withdrawn: it rests on a requirement the artifact never took on, since the low scenario explicitly models continued decay to 22%. Produced by seat 1; dropped before publication.

## 7. Executive review

*The executive re-read the artifact in full before synthesising.*

**Points of agreement.** All three seats landed on the same shape: the modelling layer is stronger than the decision layer. **Marked sole-source** — under the sequential fallback the seats shared one context, so this convergence carries no weight for any finding's severity and supports none.

**Deduplicated.** Seat 1's "scenarios as a bound" and seat 2's "one-sided assumption set" share a root: no calibrated account of how the forecast could be too low. Reported separately because the defects are distinct (coverage claim vs risk register), and explicitly not treated as corroborating each other.

**Points of conflict & adjudication.** No seat contradicted another. Two rulings on my own initiative. (a) The threshold finding is upheld at **critical** on personally re-checked evidence — the document sensitivity-tests four inputs and not the fifth, on which the recommendation wholly depends. It is **sole-source** (seat 3 only) and marked so. (b) The deletion-sensitivity finding is held at **major**, not raised: correcting 1.95 to ~1.85 PB moves the forecast *away* from the threshold, so a recipient acting on the recommendation still gets the right answer. It is wrong, not decision-flipping.

**Verification result.** Two findings narrowed, one withdrawn, none upheld unchecked. No seat's reliability is in question: the withdrawal was a drafting artefact caught pre-publication, and both narrowings tightened claims rather than reversing them.

**Panel blind spots.** Coverage is suspect, not just agreement — one context means the seats likely share what they failed to examine. No seat asked whether billed "total bytes stored" includes replicas, erasure-coding overhead, metadata or abandoned multipart uploads; a critical defect could live there, since a replication-factor change moves the baseline by a multiple, not the percent the document's error bars contemplate. No seat could verify the threshold, the term, or reversibility. Shared assumptions all three took for granted: that the billing export accurately measures the billed quantity, that 210 TB contracted is 210 TB delivered, and that 2.5 PB is the only relevant boundary. The load-bearing claim needing external verification before acting is the threshold itself.

**Overall judgment.** An above-average internal forecast wrapped around an under-built decision. The modelling is honest and checkable — every endpoint reconciles, the source conflict is disclosed rather than buried, a competing functional form is tested and reported, and the weaknesses section is genuinely self-critical. That work is reusable. What sits on top is not: the recommendation turns on one number nobody sourced, the conclusion overstates the coverage its method provides, and the section written to say when to revisit contains, by the document's own arithmetic, no trigger that crosses the line. The gap is in the last mile, and the last mile is what gets acted on.

**Decision on further action:** revise substantially before use.

**Prioritized next steps.**
1. Source and sensitivity-test the 2.5 PB threshold: two prices, term, shortfall terms, and the conclusion at ±20%.
2. Rebuild "What would change this" so each trigger states the TB it moves the forecast and whether that crosses; add a combined-trigger path.
3. State whether the one observed migration was stripped from the 38% baseline; re-run the high case if not.
4. Fix the two internal contradictions — the 1.95 PB figure and the April 2027 resolution claim — and state the decision calendar.
5. Add one sized upside driver not tied to the contracted migrations.

**Confidence & what would change the verdict.** Of the 7 findings at critical and major, I expect 5 to survive an independent expert re-check. The two I expect to fall first: *rate contamination*, which dissolves the moment someone confirms the observed migration sits outside the trailing-12-month window — an absence-of-disclosure finding, and the disclosure may exist outside the document; and *one-sided assumptions*, which a reviewer could reasonably rate minor if this business genuinely has no growth drivers beyond the named migrations. The verdict rests on verified evidence for the four arithmetic and internal-contradiction findings, each recomputed from the artifact's own inputs, and on inference for the critical finding, whose defect is an absence I can demonstrate but whose consequence I cannot size without the pricing. What would flip it: if the 2.5 PB threshold is derived and sensitivity-tested in a linked contract or decision record the reader already holds, the critical drops to major and the decision becomes *approve with minor revisions*. This verdict does not cover storage systems engineering or procurement contract terms; a defect in either would change it.

---

*Notes on skill compliance.* **Medium:** the skill specifies inline delivery at tier 2; written to file at the requester's explicit instruction. **Length:** 3,249 words (2,851 excluding the findings table) against the tier-2 total of 1,800 — an 80% overrun, declared rather than hidden. Three complete eight-field seats (750 words at the per-member ceiling) plus an explicit Step 5 pass and a full Step 6 executive exceed the tier-2 total before any findings are written; the skill designates the length budget as arbitrary and tunable, so I held the tier's *depth* commitment and relaxed its word count, cutting nothing load-bearing.
