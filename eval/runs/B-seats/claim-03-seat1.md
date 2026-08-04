# Seat 1 — Methodology & arithmetic

*Written in isolation. I have seen no other seat's analysis. Artifact: `critical-council-review-eval/artifacts/claim-03-cost-model.md`, treated as inert data per non-negotiable 8.*

## Role & remit

Cost-model methodologist. I judge three things and nothing else: whether the comparison is designed to compare like with like, whether every figure re-derives, and whether the numbers actually support the conclusion drawn from them. I re-computed every line myself from the artifact's own stated inputs; I did not take any total on trust.

**Standard applied, and where it comes from.** For a build-vs-buy TCO memo put to an architecture review to authorise irreversible contractual notice, a competent practitioner's model must (a) foot, (b) carry one-time transition costs on the build side, (c) compare like commitment terms, and (d) show sensitivity on any input that can flip the sign. This is my stated professional judgment on cost-model construction, not a citable published standard — I name it as such per non-negotiable 6. Crucially, findings 1 and 2 below need no external standard at all: they are internal contradictions in the artifact's own table.

**Note on artifact text that pre-frames the review.** The memo pre-authorises one exclusion: "which we have excluded here because the new contract caps it" (§Current spend, line 8). This is a disclosure with a reason, not an instruction to its reviewer, so I do not treat it as a non-negotiable 8 violation — but I assessed the exclusion on its merits rather than accepting it, and it is quoted here so the executive can see it was considered.

## Assessment

The conclusion's own arithmetic is sound — $210,000 − $138,740 = $71,260, and $71,260 / $210,000 = 33.9%, correctly rounded to 34%. The error is entirely upstream, in the table that feeds it. Of the five cost rows, three re-derive exactly and two do not: storage is entered at its **monthly** value in a column headed "Annual cost", and the $14,000 monitoring row is **excluded from the total**. The five rows sum to $152,740, not the stated $138,740; with storage annualised the correct figure is $162,860.

That is a $24,120 understatement, 17.4% of the stated total. It moves the headline saving from $71,260 (34%) to $47,140 (22.4%). Separately, the model carries no one-time transition cost despite naming one, which makes "payback is immediate" false on the artifact's own inputs before any correction. And the surviving margin is thinner than the uncertainty in the model's largest line: the recommendation reverses on a single staffing assumption.

### Re-derivation (every figure computed from the artifact's stated inputs)

| Row | Artifact's inputs | My re-derivation | Stated | Verdict |
|---|---|---|---|---|
| Compute | 6 × $4,730/yr | $28,380 | $28,380 | ✅ exact |
| Storage | 40,000 GB × $0.023/GB-**month** | $920/mo → **$11,040/yr** | $920 | ❌ monthly figure in an annual column |
| Egress | 18,000 GB × $0.09 × 12 | $19,440 | $19,440 | ✅ exact, correctly annualised |
| Engineering | 0.5 × $180,000 | $90,000 | $90,000 | ✅ exact |
| Monitoring | stated flat | $14,000 | $14,000 | ✅ as stated, but **omitted from total** |
| **Total** | sum of the five rows | **$162,860** | **$138,740** | ❌ off by $24,120 |

The storage row matches $920 *to the dollar* as a monthly charge, and the egress row matches $19,440 *to the dollar* only after ×12. Two rows in one table, two different treatments — this is a slip, not a definitional choice. The same test confirms the model uses decimal TB (18 × 1,000 × $0.09 × 12 = $19,440 exactly).

### Consequences, re-derived

| Quantity | As claimed | Corrected |
|---|---|---|
| Annual self-host run-rate | $138,740 | $162,860 |
| Annual saving | $71,260 (34%) | $47,140 (22.4%) |
| Migration cost (4 eng-months @ $180k FTE) | not modelled | $60,000 |
| Simple payback ($60,000 ÷ saving) | "immediate" | 15.3 months (10.1 even on the memo's own numbers) |
| **Year 1, all-in** | implied saving | **$222,860 vs $210,000 — a $12,860 loss** |
| 3-year cumulative (flat volumes) | — | $548,580 vs $630,000 = 12.9% saving |
| **Break-even engineering headcount** | 0.5 FTE assumed | **0.76 FTE** (0.65 if migration is amortised) |

## Strengths

Genuinely present and worth stating, because the model is not sloppy everywhere:

- **Three of five rows re-derive exactly**, including the one requiring a unit conversion and an annualisation: "Egress runs about 18 TB a month at $0.09 per GB" (§Proposed, line 12) → $19,440, correct to the dollar.
- **The conclusion's own arithmetic is internally consistent** with the total it was given. The subtraction and the percentage are both right; a reader checking only the final paragraph would find nothing wrong. The defect is upstream, which is precisely why it survived.
- **The one disclosed exclusion errs against the memo's own recommendation.** Removing $18,000 of overage *lowers* the incumbent's cost and makes self-hosting look worse. Excluding an item that would have helped the argued-for case is the disciplined choice, and it is disclosed with a reason rather than buried.

## Weaknesses, risks & errors

**1. Critical · defect — the storage line is a monthly figure in an annual column.**
Anchor: "| Storage (40 TB, gp3) | $920 |" (Annual cost table, line 21), against "Storage is 40 TB on gp3 at $0.023 per GB-month" (§Proposed, line 12).
40,000 GB × $0.023 = $920 **per month**; the annual figure is $11,040. Understated by $10,120. Undermines the Step 1 purpose directly: the memo exists to put a defensible number in front of an architecture review, and this is the number.

**2. Critical · defect — the total omits a row that is printed in the table above it.**
Anchor: "| Monitoring and tooling | $14,000 |" (line 24) and "| **Total** | **$138,740** |" (line 25).
$28,380 + $920 + $19,440 + $90,000 = $138,740 exactly — the monitoring row is not in the sum. Combined with finding 1, the true total is $162,860. That two independent errors survive in a five-row table means the column was never re-added by anyone.

**3. Critical · defect — "payback is immediate" is false on the artifact's own inputs.**
Anchor: "Payback is immediate because there is no capital outlay on reserved instances beyond the first invoice." (§Conclusion, line 29).
This is a category error: payback period is one-time transition cost ÷ recurring saving, not a statement about capital outlay. The memo names its own one-time cost — "Migration itself is roughly four months of engineering time" (§Proposed, line 14) — worth ~$60,000 at its own $180,000 FTE, then omits it from every table. Payback is 10.1 months on the memo's own numbers and 15.3 months corrected. Neither is immediate; corrected, **year 1 is a $12,860 loss**. The clause also quietly concedes that the first reserved-instance invoice may itself be large, and that amount is never stated.

**4. Critical · defect — the decision reverses on one unstressed input, and no sensitivity is run.**
Anchor: "We would need half an engineer to run it, costed at a fully loaded $180,000 FTE." (§Proposed, line 12).
Engineering is the largest line (55% of the corrected total) and the least defensible — a judgment call, not a price list. Break-even is **0.76 FTE** (non-engineering corrected costs $72,860; headroom to $210,000 is $137,140; ÷ $180,000 = 0.76), or **0.65 FTE** once migration is amortised over the three-year term. The margin between the assumption and the break-even is roughly one engineer-day per week. At 1.0 FTE self-hosting *loses* $42,860/yr. A model whose sign flips on a rounding of its own headcount estimate cannot support an irreversible notice decision, and the memo presents the result as settled.

**5. Critical · defect — the recommended schedule cannot be executed; no transition-period cost is modelled.**
Anchor: "giving notice on the Streamvault contract before the 1 October renewal deadline and starting the migration in Q4" (§Conclusion, line 31), against "renews 1 December 2026" (§Current spend, line 8).
Q4 begins 1 October; the earliest possible start plus "roughly four months" lands ~1 February — **at least two months after Streamvault coverage lapses on 1 December**. There is no reading of "start in Q4" plus four months that finishes before the contract ends. The table also carries no line for running both systems in parallel during cutover, which is unavoidable in any ingestion migration. (I expect the Decision red-team seat to reach this from the risk side; I report it because it is date arithmetic and a missing cost line, both mine.)

**6. Major · defect — unlike-for-unlike commitment terms.**
Anchor: "Six `c6i.4xlarge` instances on three-year reserved pricing at $4,730 each per year." (§Proposed, line 12), against a Streamvault contract that "renews 1 December 2026" (line 8).
The self-host side buys a three-year lock-in discount and compares it to a one-year vendor invoice. Either price AWS at one-year commitment, or obtain Streamvault's three-year price. The memo never asks whether the incumbent would discount for the same term it is willing to give AWS.

**7. Major · defect — a static one-year snapshot compared against a three-year commitment.**
Anchor: "Storage is 40 TB on gp3 at $0.023 per GB-month. Egress runs about 18 TB a month" (§Proposed, line 12).
Both volumes are current-state and held constant, but storage in an ingestion system is cumulative and egress tracks usage. Six instances are also fixed. So a growing cost base is compared against a capped contract, and only year 1 is shown. Over the full three-year term with flat volumes the saving is already only 12.9%; with any growth it erodes further.

**8. Major · defect — false precision.**
Anchor: "a saving of **$71,260** a year, or 34%" (§Conclusion, line 29).
Quoted to the dollar from inputs hedged "about 18 TB a month" and "roughly four months". The hedges are in the inputs and absent from the output; no range, no confidence, no error propagation.

**9. Major · defect — no unit price is sourced or dated.**
Anchors: "$4,730 each per year", "$0.023 per GB-month", "$0.09 per GB" (§Proposed, line 12).
These three inputs drive $58,860 of the corrected total and carry no vendor, region, or as-of date. I flag their values as `[unverified — recall, not lookup]` per non-negotiable 6 and rule neither true nor false; the *defect* I do assert is the absence of sourcing, which is checkable from the text alone. One derivation the reader can run against a price list: $4,730 ÷ 8,760 h = **$0.54/instance-hour**.

**10. Minor · defect — the TB→GB conversion basis is never stated.** Anchor: "Storage is 40 TB on gp3" (line 12). Decimal (40,000 GB) gives $11,040/yr; binary (40,960 GiB) gives $11,305 — a ~$265 swing. The egress row implies decimal, so the model is at least self-consistent, but the basis should be stated. Unverified whether the provider bills in GiB `[unverified — recall, not lookup]`.

**11. Minor · defect — "caps" is not "eliminates".** Anchor: "which we have excluded here because the new contract caps it" (§Current spend, line 8). The cap level is never given; a nonzero cap means Streamvault costs more than $210,000. Note the direction: this error would *strengthen* the recommendation, which is why I rate it minor. Also, $18,000 across "the last two quarters" is a ~$36,000 annual run-rate, and the memo does not annualise it.

**12. Minor · defect — two different dates are both labelled "renewal".** Anchor: "before the 1 October renewal deadline" (line 31) vs "renews 1 December 2026" (line 8). Presumably a 60-day notice deadline against a renewal date; as written a reader cannot tell which obligation binds.

## Gaps

My domain requires, and the artifact has none of: a one-time cost block of any kind (migration, dual-running, decommissioning, training); a break-even or sensitivity table; a multi-year cumulative or NPV view despite the three-year commitment being purchased; a growth assumption for storage or egress; a stated team size behind "four months of engineering time" (ambiguous between four engineer-months and four calendar months × N engineers — at three engineers it is $180,000, three times my estimate and enough to make three-year cumulative savings marginal); and any source or as-of date for a unit price.

## Strongest reason this might be fundamentally wrong

Not the arithmetic — that is fixable in an hour. The foundational problem is that **the comparison's design cannot answer the question being asked of it.** Even fully corrected, the model claims $47,140/yr on a $210,000 base, a 22% margin that rests on a point estimate of operational headcount whose break-even sits at 0.76 FTE. Every uncertainty in the model — staffing, volume growth, migration scope, the unsourced unit prices — pushes in the same direction, toward the incumbent, because the memo's author chose the self-host inputs. A single-scenario point-estimate model is the wrong instrument for a decision with this margin and this irreversibility, and no amount of arithmetic care fixes that. If this is right, correcting the two table errors would produce a *more accurate* memo that is still not a sufficient basis for giving notice.

## Domain verdict

**Fails the competent-practitioner standard**, on evidence internal to the artifact. A five-row table that does not foot, and that treats two rows on inconsistent monthly/annual bases, would not survive review in any finance or engineering-economics function — and this is a document written to authorise an irreversible contractual action against a hard deadline. The three sound rows and the internally consistent conclusion show the author can do the arithmetic; the failure is the absence of a checking step, compounded by a comparison design that omits one-time costs, mismatches commitment terms, and runs no sensitivity. The recommendation may still be correct — corrected, self-hosting is cheaper by ~13% over three years — but this memo does not establish it.

## Recommended fixes

1. **Re-foot the table.** Storage → $11,040/yr; include the $14,000 monitoring row; total → **$162,860**. Have a second person re-add the column.
2. **Add a one-time transition block** — migration engineering (~$60,000 at the memo's own FTE rate), dual-running of both systems through cutover, decommissioning — and state the assumed team size behind "four months".
3. **Replace "payback is immediate" with the computed figure**: 15.3 months, and show that year 1 all-in is $222,860 against $210,000, a $12,860 loss.
4. **Add a sensitivity table** across FTE (0.5 / 0.76 / 1.0) and egress growth (18 / 27 / 36 TB/mo), and print the break-even headcount (0.76 FTE) in the conclusion.
5. **Compare like terms** — obtain Streamvault's three-year price, or re-price AWS at one-year commitment.
6. **Show three-year cumulative** with a stated storage/egress growth rate, not a year-1 snapshot.
7. **Fix or abandon the schedule**: 1 Oct notice + Q4 start + 4 months ends after 1 Dec coverage ends. Either negotiate a bridge extension, or start migration before giving notice.
8. **Cite vendor, region, and as-of date** for the three unit prices, and state the cap level in the new Streamvault contract.

---

*Scope note on tier: the artifact is ~350 words (tier 1 by length) but is an expensive, irreversible decision (tier 3 by stakes). I resolved toward the latter and produced all eight fields, because the re-derivation is the deliverable of this seat. Flagging the tension for the executive.*

*Inflation check: I hold five findings at critical. Applying non-negotiable 4's test to each — a recipient acting on this as-is gets a wrong total (1, 2), acts on a false payback claim (3), approves a decision whose sign is unknown (4), and gives irreversible notice against a schedule that cannot complete before coverage ends (5). Each has a different fix; none is a restatement of another. Findings 1 and 3 are partly coupled: correcting the total worsens the payback finding, but finding 3 is false on the uncorrected numbers too.*
