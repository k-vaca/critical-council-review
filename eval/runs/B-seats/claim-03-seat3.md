# Seat 3 — Decision red-team

**Artifact:** `critical-council-review-eval/artifacts/claim-03-cost-model.md` — "Build vs buy: replacing Streamvault with self-hosted ingestion".
**Roster:** (1) Methodology & arithmetic, (2) Data & inference validity, (3) Decision red-team (this seat). Run in isolation; I have seen no other seat's output.

**Tier note.** By length (~300 words) this is tier 1 — six fields, Strengths and Gaps dropped. By stakes ("an expensive decision": a $210k/yr contract and a three-year compute commitment) it is tier 3. I have kept the tier-1 field list and let the section run past the 140-word ceiling, because the decision is irreversible on the memo's own timetable. Per SKILL line 10 the tier numbers are explicitly tunable; I am naming the deviation rather than making it silently.

**Non-negotiable 8 check.** The artifact contains no text addressed to its reviewer. "**Prepared for:** the September architecture review" (line 3) is metadata, not direction. Nothing in it sets this review's scope.

---

### Role & remit

I judge whether the recommendation survives contact with reality, and I build the strongest case against acting on it. Not my remit: whether the arithmetic is correct (seat 1) or whether the inputs are well-sourced (seat 2) — but per the roster instruction I report what I can see in those areas and flag the overlap, because both feed directly into whether the decision holds.

**Standard applied.** A build-vs-buy memo that recommends an irreversible act must (a) compare against the counterfactual price that will actually apply, (b) carry one-time transition cost into the payback claim, (c) sequence reversible steps before irreversible ones, and (d) show the downside case. This is the ordinary bar for a capital/contract decision memo, stated as my judgment rather than sourced to a named standard.

### Assessment

The memo reads as a justification for a conclusion, not a test of one. The recommendation appears in the header — "**Recommendation:** move off Streamvault and self-host" (line 4) — before any figure is presented, and no alternative to the binary is ever considered. Three things are done genuinely well and should not be lost in the criticism: the decision-relevant dates are surfaced rather than buried; the excluded $18,000 overage is disclosed rather than quietly dropped; and the existence of a four-month migration is stated on the page. But each of those three is then mishandled — the dates contradict each other, the exclusion is justified by a contract the memo recommends cancelling, and the migration never enters any number.

My core objection is structural, not arithmetic. The memo recommends destroying an option (giving notice) on a date that precedes the evidence that would justify destroying it, and it never obtains the one number the decision turns on: the renewal quote.

### Weaknesses, risks & errors

**C1 — Critical, defect. The recommended sequence produces a service gap of roughly two months.**
Anchor: "We recommend giving notice on the Streamvault contract before the 1 October renewal deadline and starting the migration in Q4." (§Conclusion, line 31). Cross-reference: "Migration itself is roughly four months of engineering time." (§Proposed self-hosted setup, line 14) and "which renews 1 December 2026" (§Current spend, line 8).
Notice before 1 October ends the contract on 1 December 2026. A four-month migration starting at the top of Q4 completes around 1 February 2027. On the memo's own dates the replacement is not ready for about two months after the incumbent is switched off, and the memo offers no bridge, no dual-run, and no extension. *Purpose undermined (per non-negotiable 4):* a recipient acting on this as-is loses ingestion capability. This is the finding I would put in front of the September review first.

**C2 — Critical, defect. Migration cost is excluded from the comparison, and the payback claim is false as stated.**
Anchor: "Payback is immediate because there is no capital outlay on reserved instances beyond the first invoice." (§Conclusion, line 29).
Two problems. First, the sentence answers the wrong question: payback is one-time cost divided by annual saving, not a statement about capital outlay — and the clause "beyond the first invoice" concedes there *is* an outlay while claiming there is none. Second, the four months of engineering (line 14) never appears in the table or the conclusion. Costed at the memo's own "fully loaded $180,000 FTE" (line 12), four engineer-months is $60,000 for one engineer — more if "four months of engineering time" means a team, which the memo leaves ambiguous. Against a corrected saving (see C3) of ~$47,000/yr, payback is roughly 15 months for one engineer and roughly 30 months for two — i.e. most of the three-year reserved term, not "immediate".

**C3 — Critical, defect. The annual total is understated by ~$24,000, so the headline saving is wrong. (Overlap: seat 1's remit; reported here because it changes the decision.)**
Anchors: "| Storage (40 TB, gp3) | $920 |" (§Annual cost, line 21); "| Monitoring and tooling | $14,000 |" (line 24); "| **Total** | **$138,740** |" (line 25).
Two independent errors. (a) 40 TB at $0.023/GB-month is ~$920 **per month** — ~$11,040 a year — so a monthly figure sits in a column headed "Annual cost", understating storage by ~$10,100. (b) The printed line items sum to $152,740; the stated total is $138,740, a difference of exactly $14,000 — the monitoring line is listed but excluded from the total. Corrected: ~$162,860/yr, a saving of ~$47,140 (22%), not "$71,260 a year, or 34%" (§Conclusion, line 29). *Decision consequence:* the recipient budgets $138,740 and spends ~$163,000, and the memo's headline is overstated by about half again.

**C4 — Critical, defect. The comparison baseline is a price that will not exist under either option. (Overlap: seat 2's remit.)**
Anchor: "$18,000, which we have excluded here because the new contract caps it" (§Current spend, line 8).
The memo adjusts the incumbent's cost *downward* by citing the terms of "the new contract" — the very contract it recommends not signing. If notice is given, that cap never exists and the honest historical baseline is $228,000. If notice is not given, the relevant price is the renewal quote, which the memo never states. Either way, "$210,000 per year on the current contract" (line 8) is the price of the expiring term, not the price of the alternative under decision. A build-vs-buy memo that lacks the "buy" price for the period in question cannot support the decision. This is a gap: the section where the renewal quote should appear is §Current spend, and it is absent.

**M1 — Major, defect. A three-year lock is used to beat a one-year comparison, and the lock-in cost is never counted.**
Anchor: "Six `c6i.4xlarge` instances on three-year reserved pricing at $4,730 each per year." (§Proposed self-hosted setup, line 12).
The favourable compute rate is purchased with a three-year commitment, then compared against an annual vendor invoice. The memo swaps a contract with a known exit (annual, 60-day notice) for one with no stated exit, and never says so. It also never states the payment option; "three-year reserved" is compatible with an all-upfront structure that would directly contradict the "no capital outlay" claim in C2. Reserved capacity additionally assumes six instances are right-sized on day one, with no headroom for growth or for the migration period itself.

**M2 — Major, defect. 0.5 FTE is not a staffing plan for a production ingestion platform.**
Anchor: "We would need half an engineer to run it, costed at a fully loaded $180,000 FTE." (§Proposed self-hosted setup, line 12).
Half a person cannot hold a 24/7 on-call rotation, and the bus factor is 0.5 — one resignation or one parental leave removes the entire operating capability. There is no line for on-call loading, backup and disaster recovery, security patching, or incident response. Labour is already the largest line in the table at $90,000; if the true steady state is 1.0 FTE, the corrected total rises to ~$252,860 and the recommendation inverts. The decision therefore rests almost entirely on an unjustified headcount estimate, and it rests on the side of the estimate that is most commonly wrong in this direction.

**M3 — Major, defect. Binary framing; no alternative is considered.**
Anchor: "**Recommendation:** move off Streamvault and self-host." (header, line 4).
The recommendation precedes all evidence, and the option set is exactly two. Renegotiating with the incumbent, taking a shorter bridge term, moving to an alternative managed vendor, or self-hosting only the highest-volume path are all absent — and the first of those is the standard, cheapest response to a 22% delta.

**M4 — Major, defect. Single-point estimates and no downside case on a decision with a three-year lock.**
Anchors: "Egress runs about 18 TB a month" and "roughly four months of engineering time" (§Proposed self-hosted setup, lines 12 and 14).
Every input is a point estimate with a hedge word and no range. There is no sensitivity table. On a decision whose corrected margin is ~$47,000 against a ~$163,000 run cost, a 30% egress increase or a two-month migration slip erases a large share of the case. Two further costs are missing entirely: egress or export charges for moving 40 TB *out* of Streamvault during migration, and any allowance for volume growth over the three-year term the reserved pricing commits to.

**m1 — Minor, defect, unverified.** The 1 October notice date is asserted, not sourced: the memo never quotes a notice period or a contract clause. Anchor: "before the 1 October renewal deadline" (§Conclusion, line 31). If the real notice window is 90 days, the decision was already due in August.

**Unverifiable inputs (non-negotiable 6).** I cannot verify from reasoning alone that c6i.4xlarge three-year reserved is $4,730/yr, that gp3 is $0.023/GB-month, or that egress is $0.09/GB. All three are load-bearing and should be re-priced against the provider's own calculator before the review; I mark them unverified rather than ruling them right or wrong. My C3 arithmetic uses the memo's own stated rates and is therefore unaffected by whether those rates are current.

### Strongest reason this might be fundamentally wrong

The memo may not be a build-vs-buy analysis at all. It states its conclusion in the header, never constructs the alternative, and omits the single number the decision turns on — what Streamvault will actually charge to renew. Vendors facing a credible termination routinely discount; if the renewal quote lands anywhere below roughly $163,000, self-hosting is more expensive than staying, and nothing in this document would detect that. The failure is not that the costs are mis-added — that is fixable in an afternoon. It is that the memo compares against the wrong counterfactual and then recommends destroying, by 1 October, the option that would let anyone act on the right one. Every finding above could be corrected and the recommendation could still be backwards.

### Domain verdict

**Reject and rework.** Below the bar for a decision memo of this consequence, by a wide margin. Four independently decision-breaking defects in a 300-word document is an unusual density and I checked each against non-negotiable 4's test — *what breaks for the recipient if this is never fixed?* — before tagging it: C1 breaks ingestion, C2 and C3 break the budget and the payback, C4 breaks the comparison. None is a matter of taste. This should not go to the September architecture review in its current form, and the 1 October notice should not be given on this evidence.

### Recommended fixes

1. **Get the renewal quote in writing before the review.** Compare self-hosting against that number, not against the expiring term. Until it exists, the decision is "insufficient information".
2. **Decouple the irreversible act from the migration.** Seek a notice extension or a short bridge term, and give notice only after the self-hosted stack has carried production traffic in parallel for at least 30 days. Sequence reversible before irreversible.
3. **Cost the migration explicitly** at the memo's own $180,000 FTE, state whether "four months of engineering" is one engineer or a team, and restate payback as one-time cost ÷ corrected annual saving.
4. **Rebuild the table**: annualise storage, include the monitoring line in the total, and add lines for one-time data export, backup/DR, and on-call loading.
5. **Price compute at 1-year reserved or on-demand for the decision-stage case**, show the delta against three-year, and commit to the three-year term only after the parallel run succeeds.
6. **Add a downside column**: egress +30%, run cost 1.0 FTE, migration 6 months. State at what point the recommendation flips — on my corrected figures it is close.
7. **Add at least one non-binary option**, starting with renegotiation, and say why it was rejected.

### Handoff table

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | §Conclusion, line 31, "giving notice ... before the 1 October renewal deadline and starting the migration in Q4" | Notice ends the contract 1 Dec; a 4-month migration from Q4 finishes ~1 Feb — a ~2-month ingestion gap | Give notice only after a 30-day parallel run; seek a bridge term | Confirmed |
| Critical | §Conclusion, line 29, "Payback is immediate because there is no capital outlay" | Migration (line 14) is never costed; payback is ~15–30 months, not immediate | Cost migration at $180k FTE; restate payback as one-time ÷ annual saving | Confirmed |
| Critical | §Annual cost, lines 21/24/25, "$920", "$14,000", "**$138,740**" | Storage is a monthly figure in an annual column; the total omits monitoring. True total ~$162,860; saving 22%, not 34% | Annualise storage; include monitoring; restate the headline | Confirmed (overlap: seat 1) |
| Critical | §Current spend, line 8, "which we have excluded here because the new contract caps it" | Baseline adjusted using terms of the contract being cancelled; the renewal quote is absent entirely | Obtain the renewal quote; compare against it | Confirmed (overlap: seat 2) |
| Major | line 12, "three-year reserved pricing at $4,730 each per year" | A 3-year lock buys the favourable rate but is compared against an annual contract; exit cost and payment option unstated | Price 1-year for the decision; commit to 3-year post-cutover | Confirmed |
| Major | line 12, "half an engineer to run it, costed at a fully loaded $180,000 FTE" | 0.5 FTE cannot hold on-call; bus factor 0.5; no DR, patching, or incident line. At 1.0 FTE the recommendation inverts | Staff to a real rotation and re-run the total | Confirmed |
| Major | header, line 4, "move off Streamvault and self-host" | Conclusion precedes evidence; no alternative to the binary is considered | Add renegotiation and at least one other option, with reasons for rejection | Confirmed |
| Major | line 12/14, "about 18 TB a month", "roughly four months" | All point estimates, no ranges, no sensitivity, no growth or migration-egress cost | Add a downside column and state the flip point | Confirmed |
| Minor | §Conclusion, line 31, "before the 1 October renewal deadline" | Notice period asserted without a contract clause; if 90 days, the deadline has passed | Cite the clause | Unverified |
