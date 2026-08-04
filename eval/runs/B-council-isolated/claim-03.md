# Critical council review — `artifacts/claim-03-cost-model.md`

*Verification pass (Step 5) and executive synthesis (Step 6). Three seats were run in isolation; none saw another's analysis and none received requester framing. This pass re-read the artifact in full before touching any seat output, per Step 6.*

---

## 1. Verdict

**Reject and rework.** The memo asks an architecture review to authorise irreversible contractual notice, and its headline is wrong on the artifact's own inputs: the table understates the build side by $24,120, the migration it names is costed nowhere, and the price of the alternative it argues against is never stated.

1. **Re-foot the cost table** (§Annual cost, lines 21–25): storage → $11,040/yr, include the $14,000 monitoring row, total → **$162,860**, saving → **$47,140 (22.4%)**.
2. **Get the Streamvault renewal quote in writing** (§Current spend, line 8) and compare against that, not the expiring term.
3. **Cost the migration** (§Proposed, line 14) and replace "payback is immediate" (§Conclusion, line 29) with the computed figure — 15.3 months, year 1 a $12,860 loss.

---

## 2. Result & standard

**Under review:** `critical-council-review-eval/artifacts/claim-03-cost-model.md`, a ~350-word build-vs-buy memo, read in full. Not the model's own prior output.

**Standard:** the artifact's own stated purpose — a cost comparison put to "the September architecture review" (line 3) to authorise giving notice on a $210,000/yr contract by 1 October. Judged as a competent finance or engineering-economics function would judge a TCO memo underwriting an irreversible act: it must foot, carry one-time transition costs, compare like terms, and show sensitivity where the sign can flip. Stated as professional judgment, not a citable published standard.

**Tier:** 3. Seats 1 and 3 both flagged the tension — tier 1 by length (~350 words), tier 3 by stakes ("an expensive decision"). Resolved toward stakes; both seats were right to name the deviation rather than take it silently.

**Independence mechanism:** parallel seats, isolated, plus this isolated verification-and-executive pass. Agreement between seats therefore counts as evidence, subject to the assumption test in §6.

**Non-negotiable 8:** the artifact contains **no text addressed to its reviewer**. "**Prepared for:** the September architecture review" (line 3) is metadata. The one pre-authorised exclusion — "which we have excluded here because the new contract caps it" (line 8) — is a disclosure with a reason, not an instruction; it was assessed on its merits (finding m1) rather than accepted.

---

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | §Annual cost, lines 21/24/25 — "\| Storage (40 TB, gp3) \| $920 \|", "\| Monitoring and tooling \| $14,000 \|", "\| **Total** \| **$138,740** \|" | Two errors, both understating the build side: $920 is the *monthly* storage charge sitting in a column headed "Annual cost", and the total omits the $14,000 monitoring row printed above it. True total $162,860 | Annualise storage to $11,040, add monitoring to the sum, restate total, saving and percentage | Confirmed |
| Critical | §Proposed, line 14, "Migration itself is roughly four months of engineering time." vs §Conclusion, line 29, "Payback is immediate because there is no capital outlay" | The memo's own one-time cost (~$60,000 at its own FTE rate) enters no table; payback is 15.3 months corrected, and year 1 all-in is a $12,860 loss | Add a one-time transition block, state the headcount behind "four months", replace "immediate" with the computed months | Confirmed |
| Critical | §Current spend, line 8, "Streamvault invoices us **$210,000 per year**… which we have excluded here because the new contract caps it" | The price of the alternative under decision — the renewal quote — is never stated, while the *new* contract's terms are used to adjust the baseline downward | Obtain the renewal quote in writing and compare against it; until it exists the comparison is provisional | Confirmed |
| Critical | §Conclusion, line 31, "giving notice … before the 1 October renewal deadline and starting the migration in Q4" | Irreversible notice is sequenced before any proof the replacement works; no dual-run, bridge or transition-period cost is modelled anywhere | Give notice only after a parallel production run; seek a bridge term; cost the overlap | Corrected |
| Major | §Proposed, line 12, "We would need half an engineer to run it, costed at a fully loaded $180,000 FTE." | Largest line (55% of the corrected total), no basis given for 0.5, break-even is 0.76 FTE, and no sensitivity analysis appears anywhere | State the evidence for 0.5; publish the break-even (0.76 FTE) and a sensitivity table | Corrected |
| Major | §Annual cost, lines 18–25, and §Current spend, line 8 | Neither side's scope is stated: no backup/DR, redundancy, on-call or support line on the build side, and Streamvault's inclusions are never described | Add the missing rows, or state that the build option accepts a lower service level and have the review accept that knowingly | Confirmed |
| Major | §Proposed, line 12, "three-year reserved pricing at $4,730 each per year" | A three-year committed rate is compared against an annually renewing contract; exit cost, payment option and any multi-year view are all absent | Price one-year for the decision case, show the delta, add a three-year cumulative view | Corrected |
| Major | §Proposed, line 12, "Storage is 40 TB on gp3… Egress runs about 18 TB a month" | Volumes and instance count held flat across a three-year commitment, though the memo's own overage line is evidence that volume varies and rises | Model at least one growth scenario for storage and egress | Confirmed |
| Major | §Proposed, line 12, "$4,730 each per year", "$0.023 per GB-month", "$0.09 per GB" | Three prices driving $58,860 of the corrected total carry no vendor, region or as-of date | Cite vendor, region and as-of date; re-price against the provider's own calculator | Confirmed |
| Major | Header, line 4, "**Recommendation:** move off Streamvault and self-host." | Only two options are ever considered; renegotiation, a bridge term and alternative vendors are absent from a decision to give irreversible notice | Add at least one non-binary option with reasons for rejection | Corrected |
| Minor | §Current spend, line 8, "because the new contract caps it" | A cap is a ceiling, not zero, and its level is never given; the $18,000 is also not annualised | State the cap level | Confirmed |
| Minor | Line 8, "renews 1 December 2026" vs line 31, "before the 1 October renewal deadline" | Two different dates are both labelled "renewal" and no notice clause is cited | Cite the notice clause and distinguish the two dates | Confirmed |
| Minor | §Conclusion, line 29, "a saving of **$71,260** a year, or 34%" | Dollar-exact output from an input hedged "about 18 TB a month" | Express the saving as a range | Corrected |
| Minor | §Proposed, line 12, "Storage is 40 TB on gp3" | Decimal/binary conversion basis unstated (~$265 swing); the egress row implies decimal | State the basis | Confirmed |

---

## 4. Council roster

| Seat | Remit | Why it belongs |
|---|---|---|
| 1 — Methodology & arithmetic | Does the comparison compare like with like, does every figure re-derive, do the numbers support the conclusion | The artifact's core deliverable is a table and a headline number |
| 2 — Data & inference validity | Inputs, stated and unstated assumptions, exclusions, whether the recommendation follows | The decision turns on inputs no one has sourced |
| 3 — Decision red-team | Whether the recommendation survives contact with reality; the strongest case against acting | Required skeptic seat; also carries the recipient's viewpoint (the architecture review) |

**Deliberately not covered — and whether a critical defect could live there:**

- **Technical sizing / capacity engineering.** Not covered. **Yes, a critical defect could live here.** No seat asked whether six `c6i.4xlarge` actually carry the workload implied by 40 TB stored and 18 TB/month egress. If the sizing is wrong, both the compute line and the FTE line move, and the verdict changes.
- **Contract law.** Not covered. **Yes.** No seat had the Streamvault agreement; all three reasoned from two dates in the memo. A termination fee, an auto-renewal mechanic or a 90-day notice window would each change the decision.
- **Security, compliance and data residency.** Not covered. **Yes.** Certifications or controls the vendor supplies and self-hosting must replace are priced at zero by default.

The verdict is capped accordingly: it does not cover these three domains, and a defect in any would change it.

---

## 5. Individual analyses

*Findings raised by two or more seats are stated once in §3 and in §6's points of agreement, and deleted from the sections below per the Step 6 deduplication rule. What remains is each seat's unique contribution, verdict and foundational objection.*

### Seat 1 — Methodology & arithmetic

*Unique contributions, all re-derived independently in this pass and confirmed:* the full re-derivation table; the corrected consequence set (year 1 $222,860 vs $210,000; three-year cumulative $548,580 vs $630,000 = 12.9%); the **break-even headcount of 0.76 FTE** (0.65 amortised), which is the single most useful number the council produced and appears nowhere in the memo; the decimal-vs-binary test that proves the model uses decimal TB (18 × 1,000 × $0.09 × 12 = $19,440 exactly, where binary gives $19,907); the unit-price sanity check $4,730 ÷ 8,760 h = $0.54/instance-hour; the unsourced-price finding, which no other seat raised as a defect.

*Also unique, and correct:* the observation that **the one disclosed exclusion errs against the memo's own recommendation** — removing $18,000 of overage lowers the incumbent's cost and makes self-hosting look worse. This is genuinely a strength and it is decisive in adjudicating conflict 3 below.

*Domain verdict (upheld):* fails the competent-practitioner standard on evidence internal to the artifact. Three of five rows re-derive exactly, so the author can do the arithmetic; the failure is the absence of a checking step.

*Strongest reason this might be fundamentally wrong (upheld):* the comparison's design cannot answer the question asked of it. Corrected, the model claims $47,140 on a $210,000 base — a 22% margin resting on a point estimate whose break-even sits at 0.76 FTE, with every uncertainty pushing toward the incumbent because the author chose the build-side inputs. Correcting the two table errors yields a more accurate memo that is still not a sufficient basis for giving notice.

*Corrected in this pass:* finding 5's claim that "there is no reading of 'start in Q4' plus four months that finishes before the contract ends" is too strong — see conflict 6. The inference that "the column was never re-added by anyone" is unanchored process speculation and is dropped.

### Seat 2 — Data & inference validity

*Unique contributions:* the **wrong-counterfactual finding** — the decision is whether to sign the renewal, so the comparison should be against the renewal price; the memo demonstrably knows the new contract's terms because it cites the overage cap, yet never states its price. Upgraded to critical here (conflict 2). Also unique and confirmed: that the memo's **own overage evidence** — volume-based overage in two consecutive quarters — is proof that volume is variable and rising, which makes holding storage and egress flat across a three-year commitment a defect rather than a simplification. Also the like-for-like scope finding (no DR, redundancy, on-call, support plan).

*Also unique, and correct:* the explicit refusal to treat header placement as a defect — "stating the recommendation in the header before the evidence is normal memo practice, not bias in itself." This is the right call and it settles conflict 4.

*Domain verdict (upheld):* below the bar. A competent analyst would state the counterfactual price, carry the one-time migration cost into the payback claim, and show a break-even on the largest soft assumption. The memo does none of the three.

*Strongest reason this might be fundamentally wrong (upheld):* not that the saving is overstated but that **its sign is unestablished** — the build side is understated by two figure errors and by omissions that all push one way, while the vendor side is compared against a price that is not the one on offer.

*Corrected in this pass:* finding 6's asymmetric-exclusion framing is downgraded to minor (conflict 3). Anchor variance noted and dismissed: seat 2 quotes "Streamvault invoices us $210,000 per year" without the artifact's bold markers; rendered text is identical, so this is formatting, not misquotation.

### Seat 3 — Decision red-team

*Unique contributions:* the **sequencing objection** — the memo recommends destroying an option (giving notice) on a date that precedes the evidence that would justify destroying it, and the fix is to sequence reversible before irreversible: give notice only after the self-hosted stack has carried production traffic in parallel. This is the most actionable recommendation the council produced and no other seat reached it. Also unique: the observation that a vendor facing credible termination routinely discounts, so the renewal quote is precisely the number the decision turns on; and the binary-framing finding.

*Domain verdict (upheld, and adopted as the executive decision):* reject and rework. Should not go to the September review in its current form, and the 1 October notice should not be given on this evidence.

*Strongest reason this might be fundamentally wrong (upheld):* the memo may not be a build-vs-buy analysis at all — it omits the single number the decision turns on. If the renewal quote lands below roughly $163,000, self-hosting is more expensive than staying and nothing in this document would detect it.

*Corrected or withdrawn in this pass:* the "~2-month service gap" is narrowed (conflict 6); the "$228,000 honest historical baseline" is corrected — it assumes zero overage in the two unobserved quarters, and annualising the two-quarter figure would instead give $246,000, so no exact historical annual figure is derivable from the artifact; the all-upfront payment speculation is narrowed to "payment option unstated" and marked `[unverified — recall, not lookup]`; the "half a person cannot hold a 24/7 on-call rotation" claim is narrowed, since the artifact never states a service level or on-call requirement — the checkable defect is the absent coverage line. **Two sub-claims withdrawn** (see §6).

---

## 6. Executive review

### Points of agreement (deduplicated)

All three seats, independently and without shared framing, reached: the two table errors and the corrected total of $162,860 (seats 1, 2, 3); the uncosted migration and the false payback claim (seats 1, 2, 3); the schedule/sequencing risk (seats 1, 2, 3); that 0.5 FTE is the model's soft spot (seats 1, 2, 3); that no sensitivity analysis exists anywhere (seats 1, 2, 3).

**Testing *why* they agree**, per non-negotiable 3. The table findings rest on arithmetic the artifact fully establishes — I re-derived every row from the stated inputs and every seat figure matched to the dollar, including the exact coincidence that $28,380 + $920 + $19,440 + $90,000 = $138,740, which is what proves the monitoring row was dropped rather than mistyped. That agreement is load-bearing. The migration and sensitivity findings rest on absences I confirmed by search: the strings "sensitivity", "break-even", "renewal quote", "on-call", "backup", "redundan", "parallel", "dual", "growth", "upfront", "region" and "notice period" return **zero hits** in the artifact.

The schedule finding is different, and the assumption test caught it. All three seats read "roughly four months of engineering time" (line 14) as four *calendar* months and "Q4" as calendar Q4 — and then built a ~2-month service gap on that reading. Every seat separately flags the headcount ambiguity elsewhere in its own analysis, yet none carried it into this finding. The artifact does not establish either reading: at two engineers, four engineer-months elapses in two calendar months and completes before 1 December, with no gap. The seats agree here because they inherited the phrase's most natural reading, not because the artifact settles it.

### Points of conflict & adjudication

1. **0.5 FTE severity** — seats 1 and 2 critical, seat 3 major. **Ruled major.** Naming the specific evidence that makes critical overblown: the artifact contains no *false* statement about staffing, only an unsupported one plus an absent sensitivity analysis, and the sign flips only above 0.76 FTE — which no seat established. Non-negotiable 4 requires naming the purpose undermined before assigning critical; here the recipient gets a result whose confidence is overstated, not a wrong result. That is the major test, not the critical one.
2. **Baseline severity** — seat 2 major, seat 3 critical, seat 1 raised only the related cap point as minor. **Ruled critical.** Adjudicated by evidence, not headcount: seat 3 owns the decision domain, seat 2 offered a lower tag rather than contrary evidence, and a build-vs-buy comparison that lacks the buy-side price for the period under decision cannot support the decision it recommends. I checked the anchor personally — no renewal price appears anywhere.
3. **Overage exclusion severity** — seat 1 minor, seat 2 major. **Ruled minor,** with seat 1. Seat 2 did not address the direction: excluding $18,000 *lowers* the incumbent's cost and makes self-hosting look worse, so it cannot evidence bias toward the recommendation. Its magnitude does not change the decision.
4. **Header placement as evidence of motivated reasoning** — seat 3 yes, seat 2 explicitly no. **Ruled with seat 2:** bottom-line-up-front is normal memo practice. Seat 3's broader reading survives on other evidence (all omissions run one way, no downside case), but motive is not established — the one disclosed adjustment runs *against* the author's own case, which is equally consistent with carelessness.
5. **False precision severity** — seat 1 major, seat 2 minor. **Ruled minor.** Only one hedged input ("about 18 TB a month") feeds the total, contributing 14% of it; "roughly four months" feeds nothing because migration is excluded entirely.
6. **The service gap** — asserted as derived fact by all three. **Corrected, not withdrawn.** What survives is not contingent on the duration reading: the memo commits to an irreversible act before the replacement is proven, models no dual-run, bridge or transition cost, and leaves the migration duration ambiguous. Seat 1's absolute phrasing ("no reading … finishes before the contract ends") is specifically wrong and is struck.

### Verification result

Every critical and major finding was re-checked against the artifact by string search rather than recall; all 18 anchors resolve to real lines, and all 16 claimed absences return zero hits. Every arithmetic claim was re-derived independently — including the ones that would have been easiest to take on trust, such as 0.76 break-even, 12.9% three-year saving, and $0.54/instance-hour — and **every seat figure matched exactly**.

**Two sub-claims withdrawn**, both seat 3, both peripheral to otherwise sound findings:

- *"Egress or export charges for moving 40 TB out of Streamvault during migration"* (M4). The artifact never states that Streamvault holds this data; the 40 TB is the *proposed* self-hosted storage. The costed item does not follow from the text. What survives is already covered: one-time transition costs beyond engineering are unmodelled.
- *"The bus factor is 0.5"* (M2). This reads a headcount out of a capacity figure. "Half an engineer" does not state how many individuals supply the 0.5 FTE; it could be two people at 25%. The absent coverage line survives; the single-person-dependency inference does not.

**Four findings corrected** (schedule scope, FTE severity, baseline severity, exclusion severity), plus three narrowings within seat 3 and one within seat 1.

**No seat's reliability is in question.** Seat 3's two withdrawals are sub-claims inside findings whose central anchors held, and seat 3 also produced the council's single best recommendation. Seat 1's arithmetic was flawless across every one of roughly twenty derived figures. Seat 2 produced the two findings the others missed.

### Panel blind spots

The strongest case the whole council is wrong: **all three seats, and this pass, accepted the artifact's technical premises without examining them.** No one asked whether six `c6i.4xlarge` instances actually carry a workload with 40 TB stored and 18 TB/month egress. If they do not, the compute line, the FTE line and the whole comparison move — and a critical defect there would change the verdict. That domain had no seat.

Three shared assumptions the panel may have taken for granted: that giving notice ends coverage on 1 December 2026 (the artifact says "renews", which is reasonable but not identical); that the memo's own $180,000 fully-loaded FTE is the right rate for migration engineering as well as steady-state operations; and that the three unit prices are usable as stated. Every seat correctly declined to rule on the real-world accuracy of those prices — which is the right call under non-negotiable 6, but it means **36% of the corrected total rests on figures nobody verified**.

Load-bearing claims requiring external verification before acting: the three unit prices, against the provider's current price list for the target region `[unverified — recall, not lookup]`; whether $210,000 is the renewal price; the actual notice period and any termination fee in the Streamvault agreement; and the capacity sizing.

### Overall judgment

The memo is not sloppy everywhere — three of five rows re-derive exactly, the unit rates are disclosed so a reader can audit them, and the one exclusion the author chose to make runs against their own recommendation. That makes the failure specific rather than general: **there was no checking step, and no adversarial pass over the recommendation.** A five-row table that does not foot and that treats two rows on inconsistent monthly/annual bases would not survive review in any finance function. On top of that sit three defects that no amount of arithmetic care would fix — the buy-side price is missing, the memo's own one-time cost is excluded from every table, and the irreversible act is sequenced before the evidence that would justify it.

Corrected, self-hosting is still cheaper — $47,140/yr, 12.9% over three years. The recommendation may well be right. **This memo does not establish it.**

### Decision on further action

**Reject and rework.**

Not "revise substantially": that would imply the recommendation survives revision. The missing renewal quote is not an editing defect — it has to be obtained, and its value can invert the conclusion. Below roughly $163,000, staying is cheaper than self-hosting on run-rate alone.

### Prioritized next steps

1. **Obtain the Streamvault renewal quote in writing** before the September review. Until it exists, the honest status of this decision is "insufficient information".
2. **Re-foot the table** — storage $11,040, monitoring included, total $162,860, saving $47,140 (22.4%) — and have a second person re-add the column.
3. **Do not give notice on 1 October on this evidence.** Seek a bridge term or notice extension, and give notice only after the self-hosted stack has carried production traffic in parallel.
4. **Add a one-time transition block** — migration engineering (~$60,000, with headcount stated), dual-running, decommissioning — and replace "payback is immediate" with 15.3 months.
5. **Publish the break-even (0.76 FTE)** and a sensitivity table across FTE (0.5 / 0.76 / 1.0) and egress growth.
6. **Establish scope parity** — add DR, redundancy, on-call and support lines, or state that the build option accepts a lower service level.
7. **Source the three unit prices** with vendor, region and as-of date, and have an infrastructure engineer confirm the six-instance sizing.
8. **Price at least one non-binary option**, starting with renegotiation.

### Confidence & what would change the verdict

Of the 10 findings at critical and major, **I expect 8 to survive an independent expert re-check.**

The two I expect to fall first: the **sequencing finding** — if the contract's notice window permits a later decision, or if "four months of engineering" resolves to a compressed calendar schedule, it narrows from critical to major; and **"no alternatives considered"** — a reviewer could fairly argue that a document titled "Build vs buy" declares a two-option scope, and that fixing the renewal-quote finding discharges most of it anyway.

The four I expect to be unarguable are the ones resting on nothing but the artifact's own text: the table errors (pure arithmetic, re-derivable in two minutes), the uncosted migration, the absent renewal price, and the unsourced unit prices — all four are either a computation or a confirmed absence.

**What the verdict rests on:** verified evidence for the table, the migration, the missing renewal price and the missing sourcing; inference for the sequencing severity and the staffing risk; assumption for nothing load-bearing.

**What would flip it:** a written renewal quote above ~$163,000, together with a corrected table and a costed migration, would move the decision from *reject and rework* to *revise substantially before use* — the recommendation's direction would then hold on evidence. A renewal quote below ~$163,000 would invert the memo's recommendation outright. A capacity finding that six instances are undersized would also flip it, and no seat examined that.
