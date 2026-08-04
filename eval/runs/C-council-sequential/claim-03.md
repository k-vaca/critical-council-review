# Critical Council Review — "Build vs buy: replacing Streamvault with self-hosted ingestion"

> **Independence caveat (Step 3 fallback):** Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

---

## 1. Verdict

**Revise substantially before use.** The cost table does not equal the sum of its own rows and the storage line is the monthly cost printed as an annual figure, so the headline $138,740 understates the memo's own model by ~17%; the acknowledged migration effort is never costed, and the recommended sequencing terminates the vendor before the replacement exists.

1. **Refoot the table and annualize storage** (Annual cost table, lines 18–25): rows sum to $152,740, not $138,740; storage is $11,040/yr, not $920. Corrected total **$162,860**, saving **$47,140 (22%)**, not $71,260 (34%).
2. **Cost the migration and delete "Payback is immediate"** (Conclusion, line 29): ≥$60,000 at the memo's own FTE rate ⇒ payback ≥15 months.
3. **Do not give notice before the replacement carries production traffic** (Conclusion, line 31).

---

## 2. Result & standard

**Under review:** a ~330-word build-vs-buy memo recommending termination of the Streamvault contract and migration to self-hosted ingestion, prepared for a September architecture review. Read in full; nothing sampled. Not my own prior output.

**Standard:** what a competent finance-literate engineering leader should produce for a board-level build-vs-buy paper — a cost table that foots, units consistent across lines, one-time switching costs included in payback, a like-for-like comparison against what the vendor price bundles, and the load-bearing assumptions sourced. Named from the artifact's own stated purpose ("Prepared for: the September architecture review", "Recommendation: move off Streamvault and self-host") plus standard TCO practice.

**Text in the artifact that sets its own scope** (quoted per non-negotiable 8, line 8): *"which we have excluded here because the new contract caps it."* The artifact declares one cost category out of scope. That does not bind this review; the exclusion is judged below and its presence is itself reported (minor 2).

**Tier 3** — chosen on stakes, not length: the paper drives $210,000/yr of recurring spend, a three-year compute commitment, and an irreversible contract termination. Tier 3 calls for 4–6 seats.

**Independence mechanism:** sequential seats (Step 3 fallback), per the requester's instruction; no subagent tooling available for this run.

**Requester framing (quarantined):** the requester fixed the three-seat roster and the sequential mechanism and expressed **no view on the artifact's quality**. Per Step 2, a requester-chosen panel is disclosed, not honored as a bound on coverage — see the roster caps in §4.

---

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Annual cost table, line 25 — `\| **Total** \| **$138,740** \|` | The five listed rows sum to $152,740; the $14,000 monitoring row is excluded from the stated total. | Refoot the table; every row must be in the total. | Confirmed |
| Critical | Annual cost table, line 21 — `\| Storage (40 TB, gp3) \| $920 \|` | 40,000 GB × $0.023/GB-month = $920 **per month**; the annual figure is $11,040 (12× understated). | Restate storage as $11,040/yr. | Confirmed |
| Critical | Conclusion, line 29 — "Payback is immediate because there is no capital outlay on reserved instances" | Migration is acknowledged (line 14) but never costed; payback measures recovery of switching cost, not absence of capital outlay. At the memo's own $180,000 FTE, four person-months ≥$60,000 ⇒ payback ≥15 months. | Add a migration line and compute a real payback period. | Corrected |
| Critical | Conclusion, line 31 — "before the 1 October renewal deadline and starting the migration in Q4" | Notice ends Streamvault 1 Dec 2026; migration starting Q4 and running "roughly four months" completes ~Feb 2027 — a ≥2-month gap with no ingestion platform, and notice is irreversible. | Migrate first, then terminate; or negotiate a bridge past 1 Dec 2026. | Confirmed |
| Critical | Proposed setup, line 12 — "half an engineer to run it, costed at a fully loaded $180,000 FTE" | The entire recommendation rests on an unsourced 0.5 FTE. Break-even is 0.82 FTE on the memo's own figures and 0.76 FTE corrected — above that, self-hosting costs more than Streamvault. | Evidence the 0.5, or model 0.5 / 0.75 / 1.0 and show where it breaks. | Confirmed |
| Major | Annual cost table, lines 18–25 (whole table) | No line for disaster recovery, backups, redundancy, or on-call; 0.5 FTE cannot provide 24/7 coverage that a managed vendor price bundles. Not like-for-like. | Add DR/backup/on-call, or state explicitly which vendor capabilities are being dropped and who accepted that. | Confirmed |
| Major | Current spend, line 8 — "Volume-based overage in the last two quarters added a further $18,000" | Volume is demonstrably growing on the vendor side, yet the build side is modelled static (6 instances, 40 TB, 18 TB/mo) with no growth or headroom. | Model 2–3 years with the observed growth rate applied to both sides. | Confirmed |
| Major | Proposed setup, line 12 — "three-year reserved pricing at $4,730 each per year" | A three-year compute commitment is compared against a one-year vendor contract; the reversibility asymmetry is never disclosed. | Disclose the commitment term, or price on-demand/1-year reserved for a like-for-like horizon. | Confirmed |
| Major | Proposed setup, line 12; Conclusion, line 29 — "$0.023 per GB-month", "$0.09 per GB", "$138,740" | Every external unit price is unsourced and undated, yet results are stated to the dollar. Egress is applied as one flat rate with no tiering assumption stated. | Cite a dated quote for each input and present the total as a range. | Unverified — external prices cannot be checked from the artifact |
| Major | Title, line 1 — "Build vs buy" | Only two options are priced. Renegotiating with Streamvault using the build number as leverage — the cheapest option in many such cases — is never evaluated. | Price a third column: renegotiated vendor terms. | Confirmed |
| Minor | Conclusion, line 31 — "before the 1 October renewal deadline" | No year is given, and "renewal deadline" is used for 1 October while the renewal date is 1 December 2026; the notice period is asserted, never cited from the contract. | Date the deadline and cite the contract's notice clause. | Confirmed |
| Minor | Current spend, line 8 — "which we have excluded here because the new contract caps it" | The cap rests on a "new contract" that is never quoted or confirmed signed, so $210,000 may not be the go-forward price. | Confirm the contract is executed and quote the cap clause. | Unverified |

**Totals:** critical 5 · major 5 · minor 2. **Withdrawn at Step 5: 0. Corrected: 1.**

---

## 4. Council roster

Three seats, **fixed by the requester** and disclosed as such:

1. **Methodology & statistics** — owns model design, arithmetic, unit consistency, and whether the numbers support the claim. Belongs because the memo's entire load is carried by one five-line table.
2. **Data & inference validity** — owns provenance of inputs, like-for-like scope, confounds, and whether the conclusion follows from the data shown. Belongs because a build-vs-buy comparison fails most often on what the vendor price silently bundles.
3. **Decision red-team** — owns whether the recommendation survives contact with reality. Belongs because the memo asks for an irreversible act (contract notice) on a deadline.

Each seat was given the full roster (roles and remits only, no findings) and told that another seat owning a topic is not a reason to skip something it can see.

**Deliberately not covered — and whether a critical defect could live there:**

- **Capacity / infrastructure architecture** — *yes, a critical defect could live here.* Nothing in the artifact or this review establishes that 6 × c6i.4xlarge, 40 TB, and 18 TB/mo egress actually carry the workload. No throughput, IOPS, retention, or replication analysis appears anywhere.
- **Commercial / contract law** — *yes.* Actual notice length, termination penalties, and whether the capped-overage contract is executed are all unexamined.
- **Security, compliance & data residency** — *yes.* Bringing ingestion in-house moves data custody; no seat examined the certification or residency consequences.

**Verdict cap:** this judgment does not cover those three domains. A critical defect in any of them would change it — in the direction of a harder decision, not a softer one.

---

## 5. Individual analyses

### Seat 1 — Methodology & statistics

**Role & remit.** Reviews the cost model as a piece of quantitative work: does it foot, are units consistent, does the inference from the table to the recommendation hold.

**Assessment.** The model's *shape* is right — annual run-rate on both sides, inputs exposed line by line so a reader can recompute. The execution fails twice on arithmetic and once on what a build-vs-buy payback calculation is for. The document's single most important number is not the sum of its own rows.

**Strengths.** Two of the four derived lines are computed correctly and prove the author knew the method: compute is 6 × $4,730 = $28,380 exactly, and egress is 18,000 GB × $0.09 × 12 = $19,440 exactly — correctly annualized. Exposing every input rather than presenting a single total is what made both errors findable at all; that is genuine good practice.

**Weaknesses, risks & errors.**
- **Critical, defect** — the total omits a row. Anchor: line 25, `| **Total** | **$138,740** |`. The listed rows sum to $152,740; the difference is exactly $14,000, the monitoring line. Standard applied: a cost table must equal the sum of its rows (basic accounting convention). This is not a judgment call.
- **Critical, defect** — unit inconsistency in storage. Anchor: line 21, `| Storage (40 TB, gp3) | $920 |` against line 12, "$0.023 per GB-month". 40,000 × 0.023 = 920 **per month**; annual is $11,040. That the egress line on the same table *was* annualized correctly is what identifies this as an error rather than a different convention.
- **Critical, defect** — payback is asserted from the wrong quantity. Anchor: line 29, "Payback is immediate because there is no capital outlay on reserved instances beyond the first invoice." Capital outlay and switching cost are different things; payback in a build-vs-buy is the time to recover the one-time cost of switching. Line 14 states that cost exists — "roughly four months of engineering time" — and no table row carries it.
- **Major, defect** — every external unit price is unsourced and the output is stated to the dollar. Anchor: "$0.023 per GB-month", "$0.09 per GB" (line 12); "$138,740" (line 29).

**Gaps.** No migration line. No sensitivity on the two inputs that move the answer most (FTE allocation, egress volume). No multi-year view, despite a three-year compute commitment. No statement of what "roughly four months of engineering time" means in headcount.

**Strongest reason this might be fundamentally wrong.** Engineering is $90,000 of a corrected $162,860 — **55% of the build cost**. Strip the four small lines away and this five-line model is a restatement of one unsourced staffing guess. If that guess is wrong upward, the arithmetic corrections are beside the point because the conclusion inverts.

**Domain verdict.** Below the bar. A table that does not equal its own rows and a line item off by 12× would not clear a finance review, regardless of whether the conclusion happens to survive.

**Recommended fixes.** Refoot; annualize storage; add a migration row with headcount × months × rate; replace "payback is immediate" with a computed payback period; present the total as a range with dated sources per input.

---

### Seat 2 — Data & inference validity

**Role & remit.** Reviews where the numbers came from, whether the two sides of the comparison measure the same thing, and whether the recommendation follows from the evidence shown.

**Assessment.** The vendor side is measured (an invoice, an observed overage). The build side is entirely assumed, and assumed *static*, on the same page that documents the vendor side growing. The two sides are also not scoped alike: one is a managed service price, the other is a machine rental plus half a person.

**Strengths.** The overage exclusion is **disclosed rather than buried** (line 8), and — contrary to how it first reads — it is *conservative against the memo's own recommendation*: removing $18,000 from Streamvault's cost lowers the baseline and shrinks the computed saving. The author gave up ground rather than took it. Separately, the vendor side carries no internal engineering cost at all while the build side carries $90,000, another asymmetry that works against the recommendation. Neither is cherry-picking.

**Weaknesses, risks & errors.**
- **Major, defect** — the comparison is not like-for-like. Anchor: the cost table, lines 18–25, has rows for compute, storage, transfer, engineering, and tooling, and none for disaster recovery, backup, or on-call; line 12 budgets "half an engineer to run it". A managed vendor price bundles redundancy, support, upgrades and around-the-clock coverage. Half an FTE is not an on-call rota. Standard applied: in a build-vs-buy, the build side must reproduce everything the vendor price includes, or the difference must be named as a capability being dropped.
- **Major, defect** — the build side ignores the trend the artifact itself documents. Anchor: line 8, "Volume-based overage in the last two quarters added a further $18,000". Overage is evidence of rising volume; the build model is fixed at 6 instances, 40 TB, and 18 TB/month with no growth term and no headroom.
- **Minor, unverified** — the capped-overage rationale. Anchor: line 8, "because the new contract caps it". No clause is quoted and no confirmation the contract is signed; if the cap is a term still being negotiated, $210,000 is not the go-forward baseline either.

**Gaps.** No provenance for 40 TB or 18 TB/month — neither is tied to a measured Streamvault volume, so nothing establishes that the self-hosted design is sized for the same workload it is replacing. No retention policy behind the 40 TB. No statement of what service level the self-hosted option is expected to meet.

**Strongest reason this might be fundamentally wrong.** If Streamvault's $210,000 buys materially more than the proposed setup delivers — redundancy, an SLA, vendor support, managed upgrades — the two numbers are not comparable at all, and the "saving" is simply the price of a capability reduction that nobody in the document has agreed to. Under that reading no arithmetic fix rescues the paper; the comparison itself is the defect.

**Domain verdict.** Below the bar for a decision paper. A measured baseline is set against an assumed, differently-scoped, no-growth alternative, and the conclusion is stated with a confidence the evidence does not carry.

**Recommended fixes.** Tie 40 TB and 18 TB/month to measured Streamvault volumes; add DR/backup/on-call or explicitly name the capabilities being dropped and who signed off; model 2–3 years with the observed growth applied to both sides; confirm the capped-overage contract is executed.

---

### Seat 3 — Decision red-team

**Role & remit.** Assumes the model is arithmetically fixed and asks whether the recommended *action* survives contact with reality. Owns the strongest case against acting.

**Assessment.** The recommendation is well-formed as a decision — a named action, a named deadline, a named start date — which is more than most architecture papers manage. But the action it recommends is the irreversible half of the plan, executed first, on a margin thin enough to vanish under one plausible staffing outcome.

**Strengths.** The memo commits: it names the action ("giving notice"), the deadline ("before the 1 October renewal deadline"), and the start ("starting the migration in Q4"). It also discloses the migration effort (line 14) even though it failed to cost it — the fact was not concealed, only unused.

**Weaknesses, risks & errors.**
- **Critical, defect** — the sequencing guarantees an outage. Anchor: line 31, "giving notice on the Streamvault contract before the 1 October renewal deadline and starting the migration in Q4", against line 8, "renews 1 December 2026". Notice ends the service 1 Dec 2026. A migration starting at the very earliest 1 Oct and running "roughly four months" (line 14) is ready ~1 Feb 2027 — a two-month gap with no ingestion platform, and that gap is a *floor*, since Q4 permits a later start and migrations rarely finish early. Notice, once given, cannot be recalled.
- **Critical, defect** — the recommendation break-evens at three-quarters of an engineer. Anchor: line 12, "half an engineer to run it, costed at a fully loaded $180,000 FTE". Holding every other line as printed, self-hosting equals Streamvault's $210,000 at **0.82 FTE**; on the corrected totals, at **0.76 FTE**. No evidence of any kind is offered for 0.5 — no comparable system, no current on-call load, no vendor-managed hours displaced. One ordinary staffing outcome flips the entire paper, and by then the contract is gone and the compute is committed for three years.
- **Major, defect** — commitment asymmetry. Anchor: line 12, "three-year reserved pricing at $4,730 each per year". A three-year lock is compared against a contract that renews annually. The build option is the *less* reversible one, and the memo never says so.
- **Major, gap** — a paper titled "Build vs buy" (line 1) prices two options. The third — take the $138,740 figure to Streamvault and renegotiate — costs nothing to attempt, is fully reversible, and is not mentioned.
- **Minor, defect** — the deadline is undated and unsourced. Anchor: line 31, "the 1 October renewal deadline". No year; "renewal deadline" is used for a date two months before the stated renewal; the notice period is never cited from the contract. If notice is 90 days rather than 60, the real deadline was in early September and the September architecture review is already too late.

**Gaps.** No fallback if migration slips. No trigger for abandoning the migration. No named owner. No answer to what happens to the ingestion pipeline between 1 Dec 2026 and go-live.

**Strongest reason this might be fundamentally wrong.** The paper may be answering the wrong question. Nobody has shown that 6 × c6i.4xlarge can carry this workload at all. If the binding constraint is capacity or capability rather than cost, then the cheaper option is not an option, and every number in the document is a well-formed answer to a question that does not decide anything.

**Domain verdict.** The recommendation does not survive contact with reality as sequenced. The direction may be right; the plan as written trades a 22% saving for a guaranteed service gap and an irreversible commitment made before the alternative is proven.

**Recommended fixes.** Invert the order — migrate, run in parallel, cut over, *then* give notice; if the notice window forces the issue, negotiate a short extension. Get a written statement of the notice period from the signed contract this week. Run the model at 0.5 / 0.75 / 1.0 FTE and show the board where it breaks. Price the renegotiation option before terminating anything.

---

## 6. Executive review

The executive re-read the artifact in full before synthesis; nothing below rests solely on the seats' reports.

**Points of agreement — all marked sole-source.** Under the sequential fallback, agreement between seats carries **no evidential weight** and is not used to support any severity rating (non-negotiable 3). Two points converged: (a) the 0.5 FTE assumption is load-bearing and unsupported — raised by seats 1 and 3; (b) the migration cost is acknowledged and uncounted — raised by seats 1 and 3. Both are marked sole-source. **Deduplicated:** each is stated once in the findings table — the FTE break-even credited to seat 3, the migration/payback defect to seat 1 — and not double-counted.

*Why they agree, tested:* both rest on one assumption — that running self-hosted ingestion is genuinely a fractional-headcount job. The artifact does not establish that; it asserts it. The seats did not inherit it from each other, they each declined to grant it. The assumption is the right target, and it is attacked directly in critical 5 rather than treated as settled.

**Points of conflict & adjudication.**

- *Seat 2 raised the overage exclusion (line 8) as a possible thumb on the scale; seat 1's framing treated the memo's exclusions as systematically self-serving.* **Downgraded to minor.** Named evidence: removing $18,000 from Streamvault's cost *lowers* the comparison baseline and *reduces* the computed saving. The exclusion cuts against the memo's own recommendation. What survives is only the unverified-cap point. This is a real correction to the review's own posture: the memo is not uniformly biased, and two of its choices (this one, and charging engineering to the build side only) are conservative.
- *Are the two arithmetic errors critical when the recommendation survives correction?* **Upheld as critical, on correctness rather than reversal.** Named reasoning: the purpose established in Step 1 is to produce a defensible annual cost figure for a board decision, and that figure is false — the table contradicts itself and a line is off by 12×. Stated plainly so the reader does not over-read the count: **corrected, self-hosting is still cheaper** (~$47,140/yr, 22%). None of the five criticals reverses the direction on its own; critical 5 is the one that could.
- *Seat 1 framed the unsourced-inputs finding partly as missing sensitivity analysis.* **Narrowed.** The operative defect is that the inputs are unsourced and undated; a sourced point estimate would be acceptable at this stage of a decision. Held at major on provenance, not on the absence of ranges.
- **Anchors personally checked.** Every critical and major anchor was located in the artifact and every derived figure recomputed by the executive. No critical or major finding is upheld on a seat's word alone.

**Verification result (Step 5).** Twelve findings re-checked adversarially, each quoted string searched in the source rather than recalled. **0 withdrawn, 1 corrected.** The correction: seat 1's migration cost of "$60,000" was restated as a **floor**, not an estimate — line 14 says "four months of engineering time", not four *person*-months, and headcount is never stated, so the true cost is $60,000 at absolute minimum and unbounded from the document. Searches: "$138,740" found line 25 and line 29 (rows sum to $152,740 — confirmed by addition); "$920" found line 21 against "$0.023 per GB-month" line 12 (= exactly one month — confirmed); "Payback is immediate" found line 29 (no migration row exists in the table — confirmed); "before the 1 October renewal deadline" found line 31 against "renews 1 December 2026" line 8 and "roughly four months" line 14 (confirmed); "half an engineer" found line 12 (break-even recomputed at 0.818 on printed figures, 0.762 corrected — confirmed). No seat's reliability is in question; the single correction was a precision issue, not a misreading.

**Panel blind spots.** The council ran in one context, so its *coverage* is as suspect as its agreement — the seats likely share what they failed to look at, not just what they concluded.

- **No seat examined capacity or architecture.** Nothing establishes that 6 × c6i.4xlarge, 40 TB, and 18 TB/month egress carry this workload. A critical defect could live here and would change the decision from "revise" to "reject and rework".
- **No seat examined the contract itself** — notice length, termination penalty, whether the capped-overage agreement is executed. A defect here could mean the deadline is already missed.
- **No seat examined security, compliance, or data residency** consequences of bringing data custody in-house.
- **Shared assumption all three seats granted:** that the artifact's external unit prices ($4,730/instance-yr, $0.023/GB-month, $0.09/GB, $180,000 fully loaded FTE) are approximately right. None was verified; all four are load-bearing and should be checked against a dated quote before acting. Likewise the $210,000 invoice figure, which is the entire baseline and is asserted, not evidenced.
- **Shared framing all three seats initially granted:** that "stay" and "build" exhaust the options. Only seat 3 broke it. A fourth seat in commercial negotiation would likely have led with it.

**Overall judgment.** This is a decision-shaped paper with its inputs exposed, which is more than many such memos manage, and its author gave up ground in two places rather than taking it. But it fails its standard on the thing it exists to do. The arithmetic is wrong twice; the headline understates the memo's own model by ~17% ($138,740 stated, $162,860 corrected); the switching cost is acknowledged on one page and absent from the table on the next; the payback claim is a category error; the recommended sequencing guarantees a two-month ingestion gap and makes the irreversible move first; and the whole margin rests on a staffing number with no evidence behind it that break-evens at 0.76–0.82 FTE. Corrected, the direction may well hold — ~$47,000/yr before migration — so the work is salvageable and should be salvaged rather than restarted. But nothing in this document should go to a review board as it stands, and no notice should be given on its authority.

**Decision on further action:** **revise substantially before use.**

**Prioritized next steps.**
1. Refoot the table and annualize storage; restate the total as $162,860 and the saving as ~$47,140 (22%). *(One hour; fixes two criticals.)*
2. Add a migration cost line (headcount × months × $180,000/12) and replace "Payback is immediate" with a computed payback period. *(Fixes the third critical; likely lands ≥15 months.)*
3. Resequence: do not give notice until the replacement carries production traffic. If the notice window forces the choice, open a bridge/extension conversation with Streamvault this week. *(Fixes the fourth critical; removes the outage.)*
4. Get the notice period in writing from the signed contract and date the "1 October" deadline. *(Blocks a decision that may already be moot.)*
5. Evidence the 0.5 FTE, or publish the model at 0.5 / 0.75 / 1.0 and show the board that it breaks at 0.76. *(Fixes the fifth critical.)*
6. Add DR, backup and on-call to the build side, or name the vendor capabilities being dropped and who accepted that.
7. Price the third option — renegotiated Streamvault terms — before terminating anything.
8. Commission the capacity analysis no seat could do: does the proposed hardware actually carry the workload?

**Confidence & what would change the verdict.** Of the **10 findings at critical or major, I expect 9 to survive an independent expert re-check.** Criticals 1, 2 and 5 are arithmetic on the artifact's own printed figures and cannot fall — they are verifiable by addition, and critical 5 holds at 0.82 FTE even if my corrections are rejected wholesale. Criticals 3 and 4 are inference from the artifact's own statements placed side by side, and I expect both to hold. **First to fall:** the "no third option priced" major — a reviewer could reasonably rule renegotiation outside a paper that declared itself build-vs-buy. **Second:** the three-year commitment major, which weakens substantially if the organization can redeploy reserved capacity elsewhere.

The verdict rests on **verified arithmetic inside the artifact** (criticals 1, 2, 5) plus **inference from the artifact's own text** (criticals 3, 4). It rests on **no external fact I could not check**, and deliberately makes no ruling on whether the four unit prices are correct.

It would **harden to "reject and rework"** if a capacity analysis showed 6 × c6i.4xlarge cannot carry the workload, or if the contractual notice period proves longer than 60 days so the 1 October deadline is already past. It would **soften to "approve with minor revisions"** only if the two arithmetic errors turn out to be transcription slips from a correct underlying model *and* a costed migration plan, a proven-then-terminate sequencing, and evidence for the 0.5 FTE all already exist elsewhere. I have no evidence that any of those exist; the paper does not reference them.

**Verdict cap (per §4):** this judgment does not cover capacity/architecture, contract law, or security/compliance. A critical defect in any of the three would change it — toward a harder decision, not a softer one.
