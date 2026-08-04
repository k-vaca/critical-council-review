# Critical Council Review — doc-02-pricing-email.md

Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

---

## 1. Verdict

**Revise substantially before use.** The email sets an effective date 27 days out against the 60-day notice term it quotes for itself, and never says what happens to the ~40% of the base on prepaid annual plans.

1. Move the effective date to no earlier than **4 October 2026** — body para 3, "Starting **1 September 2026**".
2. Split the send and add an annual-plan variant stating the prepaid term keeps its price until renewal — body para 4, "Your card on file will be charged the new amount…".
3. Rewrite the subject to name the price change and its date — Subject, "A few updates to your Northwind account".

## 2. Result & standard

Under review: the whole file — the reviewer note plus the email that ships. This is not the model's own prior output.

The artifact contains text addressed to its reviewer, quoted verbatim per non-negotiable 8:

> "**Context for the reviewer (not part of the email):** Our standard Terms of Service, clause 7.2, says: 'Subscriber will be given no less than sixty (60) days' written notice prior to any increase in fees taking effect.' Today is 5 August 2026. About 40% of the base is on annual plans; the rest are monthly. Annual customers paid up front for terms that end at various points through 2027."

The block supplies facts rather than directing a verdict, and it did not narrow this review. Its contents are treated as the artifact's own stated constraints, not as verified fact; its presence is reported as a finding below.

**Standard.** A mass price-increase notice from a B2B SaaS vendor must (a) satisfy the notice term it is subject to, (b) tell every recipient what they will pay and from when, (c) be identifiable as a price notice on arrival, and (d) give a route to act. (a) and the 40% split come from the artifact's own note; (b)–(d) are my stated judgment of competent practice, not a cited regulation.

**Tier 2** — chosen over tier 1 despite the artifact being under 500 words, because a whole-base pricing send with contractual exposure is an expensive decision. **Independence mechanism: sequential seats (Step 3 fallback)** — no subagent tooling available for this run. Tier 2's word budget is exceeded (~3,000 vs. 1,800); the budget is one of the values the skill marks as freely tunable, and the overage was spent on anchors and the Step 5 record rather than on additional findings.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | body para 3, "Starting **1 September 2026**" (vs. line 3, "no less than sixty (60) days' written notice") | 5 Aug to 1 Sep is 27 days; the quoted clause requires 60. | Re-date the increase to 4 October 2026 or later. | Confirmed |
| Critical | body para 4, "Your card on file will be charged the new amount on your next billing date after 1 September." | Only timing statement in the email; leaves ~40% on prepaid annual terms unable to tell if they are protected. | Add an annual-plan variant stating the price holds to renewal. | Corrected |
| Major | Subject, "A few updates to your Northwind account" | Subject identifies neither a price change nor a date, on a communication whose value depends on being read. | Name the change and the effective date in the subject. | Confirmed |
| Major | body para 4–5, "No action is needed from you." / "our team is here" | No pricing link, no contact address, no downgrade or cancellation route; the only instruction is to do nothing. | Add pricing page, named contact, and a downgrade/cancel path. | Corrected |
| Minor | body para 2, "cut average sync time by more than half" | Measurable claim used to justify the increase carries no substantiation. | Put the measurement on record or cut the claim. | Unverified |
| Minor | line 3, "**Context for the reviewer (not part of the email):**" | The governing 60-day obligation exists only in a block that is stripped before send. | Record the obligation on the send approval. | Confirmed |
| Minor | body paras 3–4 | No proration rule and no per-customer effective date. | State that the new rate applies from the first full cycle on or after the effective date. | Confirmed |

## 4. Council roster

Requester-specified. Disclosed per Step 2 as a fact about the panel, not a constraint honored on the merits.

1. **Purpose & audience fit** — does this do the job it exists to do, for the reader it is written for? Carries the recipient's viewpoint.
2. **Accuracy & internal consistency** — are the claims correct, and does the document contradict itself or its own stated constraints?
3. **Risk red-team** — legal, compliance, commercial and downstream exposure if this ships as written. The mandatory skeptic seat.

**Deliberately not covered.** *Billing-system implementation* — whether the platform can hold prepaid terms at the old rate and apply per-segment dates: **a critical defect could live here.** *Deliverability and proof of receipt* — a critical defect could live here. *Currency and tax presentation for non-US subscribers* — a major could. *Copy craft* — no. The verdict is capped accordingly: it does not cover billing implementation or notice delivery, and a defect in either would change it.

## 5. Individual analyses

### Seat 1 — Purpose & audience fit

**Role & remit.** Whether this email does the job it exists to do — notify a paying customer of a price change — for the person who opens it.

**Assessment.** As customer communication it is warm, short and states the new prices plainly. As a *notice* it fails at the point of arrival: the subject does not say a price is changing, and the change sits in the third paragraph behind a paragraph of company achievements.

**Strengths.** Prices are given as explicit before/after pairs with the unchanged plan named — "moves from $29 to $39 per seat per month… The Starter plan is unchanged" (para 3). No percentages to decode, no ambiguity about Starter.

**Weaknesses, risks & errors.**
- **Major, defect** — the subject line does not identify the email. Standard applied: a notice whose commercial and legal value depends on being opened must be identifiable in the inbox (my stated judgment of competent practice). Anchor: "A few updates to your Northwind account" (Subject).
- **Major, defect** — no route to act. Anchors: "No action is needed from you." (para 4); "If you have questions, our team is here." (para 5). No link, no address, no downgrade or cancellation path; the sole instruction is passive.
- **Minor, defect** — the justification precedes the news; ~40 words of achievements run before the reader learns why the email exists. Anchor: "We've been busy this year." (para 2).
- The annual-plan silence and the effective-date problem both fall in my line of sight; seats 2 and 3 own them and I note the overlap rather than restating them.

**Gaps.** No per-customer effective date, no proration statement, no worked example at a realistic seat count, no pricing-page or FAQ link.

**Strongest reason this might be fundamentally wrong.** If the send is already segmented and annual subscribers get a different email, my read of the audience is wrong and this is a competent monthly-plan notice with a weak subject line. Nothing in the artifact indicates segmentation, and the reviewer note describes a single base.

**Domain verdict.** Below the bar. The copy is fine; the notice architecture is not.

**Recommended fixes.** Name the change and date in the subject; move para 3 above para 2; add the annual variant; add a pricing link, a named contact and a downgrade/cancel route.

### Seat 2 — Accuracy & internal consistency

**Role & remit.** Whether the claims are correct, and whether the document contradicts itself or the constraints it states about itself.

**Assessment.** The price table is internally sound and plan names are consistent. The document contradicts the single constraint it states about itself: it sets an effective date inside the notice period its own quoted clause requires.

**Strengths.** The before/after figures are consistent and the unchanged plan is stated explicitly, so no reader can be misled about which plan moved.

**Weaknesses, risks & errors.**
- **Critical, defect** — the effective date breaches the stated notice term. Standard applied: the artifact's own quoted clause 7.2. Anchor: "Starting **1 September 2026**" (para 3) against "no less than sixty (60) days' written notice prior to any increase in fees taking effect" (line 3). 5 August to 1 September is 27 days; 60 days from 5 August 2026 is 4 October 2026. Adversarial check: even on the reading most favourable to the sender — that the increase "takes effect" per customer at their first increased charge rather than on 1 September — every customer whose first increased charge falls before 4 October is still inside the window, which on monthly billing is most of them.
- **Critical, defect** — the charging sentence is the email's only statement of *when* the new price applies, and it does not resolve for prepaid annual subscribers. Anchor: "Your card on file will be charged the new amount on your next billing date after 1 September." (para 4). It is not literally false for them — an annual subscriber renewing in 2027 does have a next billing date after 1 September — but set against "Starting 1 September 2026" and "No action is needed from you", ~40% of the base cannot tell whether the term they already paid for is protected.
- **Minor, unverified** — measurable performance claims carry no substantiation and are the stated justification for the increase. Anchor: "cut average sync time by more than half" (para 2); likewise "from 19 to 34 connectors". Neither is verifiable from the artifact.

**Gaps.** No proration rule, no per-customer effective date, no currency or tax qualification on the dollar figures.

**Strongest reason this might be fundamentally wrong.** If clause 7.2 is quoted incompletely — a carve-out, or a definition of "taking effect" pinned to the billing date — my lead finding narrows or falls, and this becomes a subject-line and segmentation problem. I am reasoning from a quoted fragment of a contract I have not seen.

**Domain verdict.** Fails. One stated constraint, and the document breaches it.

**Recommended fixes.** Re-date to 4 October 2026 or later; state explicitly that prepaid annual terms keep their price until renewal; state the proration rule; put the sync-time measurement on record or cut it.

### Seat 3 — Risk red-team

**Role & remit.** Where this breaks after it ships — legal, compliance, commercial, and the downstream mess.

**Assessment.** Exposure is concentrated in one place: the draft creates a documented, self-evident breach of a notice term the company itself quotes, in a communication sent to the whole base at once. The email is the evidence of the breach. That is what makes an otherwise ordinary draft dangerous.

**Strengths.** The clause is in hand and the arithmetic is checkable before send, so the exposure is avoidable at no cost beyond a date change and a re-plan of the announcement window.

**Weaknesses, risks & errors.**
- **Major, defect** — as a pattern, a subject line that conceals the change, plus "No action is needed from you." and no contact route, is what a complainant or a regulator would characterize after the fact as suppressing response to a price rise. Standard applied: my stated judgment of how the communication reads in hindsight, not a cited regulation. Anchors as seat 1's. `[unverified — recall, not lookup]` on any specific consumer-protection provision; I am not naming one.
- **Minor, defect** — the governing constraint exists only in a block marked "not part of the email", so nothing in the shipped package or its approval trail records the 60-day obligation. Anchor: "**Context for the reviewer (not part of the email):**" (line 3).
- **Major, withdrawn at Step 5** — whether email constitutes "written notice" and how receipt is deemed under the full ToS. See verification result.
- The clause 7.2 breach is the dominant risk in my remit; seat 2 owns it and it is stated once in the executive rather than restated here.

**Gaps.** No legal or finance sign-off recorded on the artifact; no statement of what happens to a customer who declines the new rate; no reference to the notice clause anywhere in the send package.

**Strongest reason this might be fundamentally wrong.** That the artifact is the wrong instrument rather than a flawed one: a 34% (Team) and 25% (Business) increase delivered as one untargeted blast with no retention offer and no account-manager motion may cost more in churn than the increase earns — in which case fixing the date and the subject line fixes nothing that matters.

**Domain verdict.** Do not send. One date change removes most of the legal exposure; the commercial question is separate and unresolved.

**Recommended fixes.** Hold the send; re-date to 4 October 2026 or later; have legal confirm the notices clause and deemed-receipt timing against the full ToS; add a stated path for customers who want to downgrade or cancel; record the 60-day obligation on the send approval.

## 6. Executive review

The artifact was re-read in full before this section was written.

**Points of agreement.** The effective-date breach (seats 2, 3) and the concealing subject line (seats 1, 3). Per non-negotiable 3, under the sequential fallback both are marked **sole-source**: the seats shared one context, so their convergence is not evidence for either finding's severity and is not counted as such.

**Deduplicated.** The effective-date finding is stated once, owned by seat 2, and removed from seat 3's list. The annual-plan finding is stated once, owned by seat 2, and removed from seat 1's list. The subject-line finding is stated once, owned by seat 1, and removed from seat 3's list. Each appears exactly once in the findings table.

**Points of conflict & adjudication.** No seat contradicted another on the merits. One severity call is mine: seats 1 and 3 both rate the subject line major, and a copy-craft reviewer would call it preference. **Upheld as major** — the specific evidence is that the email's function as notice depends on being opened, so a subject naming neither price nor date is a defect against the function, not a stylistic choice. Both critical anchors were checked personally in the source before being upheld.

**Verification result.** Five findings entered Step 5 at critical or major: **1 withdrawn, 2 corrected.**
- *Withdrawn* (seat 3): "the email may not satisfy 'written notice'." It rests on a requirement the artifact never took on — the email cannot establish its own notice method — and on a clause not in evidence. Carried below as an external verification item instead.
- *Corrected* (seat 2): the annual-plan finding, narrowed from "the charging sentence is false for annual subscribers" — it is not, it is literally satisfiable — to "it is the only timing statement and does not resolve for them."
- *Corrected* (seat 3): narrowed from "fails to disclose the right to cancel", which I cannot establish without the ToS, to "gives no route to any option."
- Strings searched and located: "sixty (60) days" — line 3; "Starting **1 September 2026**" — line 13; "your next billing date after 1 September" — line 15; "A few updates to your Northwind account" — line 7; "No action is needed from you" — line 15.
- No seat's reliability is in question; both corrections were over-reach in scope, not misreadings of the text.

**Panel blind spots.** All three seats took the reviewer note as true — the clause text, the 5 August date and the 40% split are unverified and load-bearing, and the verdict turns on the first two. All three assumed a single unsegmented send. Under the sequential fallback coverage is suspect as well as agreement: sharing one context, the seats likely share what they failed to look at. No seat examined **billing-system implementation** — whether the platform can hold prepaid annual terms at the old rate and apply per-segment effective dates. A critical defect could live there and would be invisible in the email: if the system applies the new rate on 1 September regardless of what the email says, the wording is the smaller problem. Also unexamined: proof of delivery, and currency/tax presentation for any non-US subscribers.

**Overall judgment.** A competently written customer email with a defective notice. Prose, price presentation and tone meet or exceed the standard. The two things that make it a notice rather than an announcement — a compliant date and coverage of every billing segment — are wrong and missing respectively.

**Decision on further action.** **Revise substantially before use.**

**Prioritized next steps.**
1. Re-date the increase to no earlier than 4 October 2026, and confirm that date against the full notices clause including deemed-receipt timing.
2. Segment the send; write the annual-plan variant stating the prepaid term keeps its price until renewal.
3. Rewrite the subject to name the change and the effective date.
4. Add the routes: pricing page, named contact, downgrade/cancel path.
5. Confirm with billing that prepaid terms are held and the new effective date is configurable per segment.
6. Put the sync-time measurement on record or cut the claim.

**Confidence & what would change the verdict.** Of the 4 findings reported at critical or major, I expect **3 to survive** an independent expert re-check at their stated severity. The first to fall is the annual-plan critical: a reviewer who treats notice validity as satisfied for the 60% on monthly plans would re-grade it major and call the annual variant a segmentation task — the finding survives either way, the severity may not. Second most likely to move is the subject-line major, argued down to preference. The verdict rests on **assumption rather than verified evidence in exactly one place**: the reviewer note's quotation of clause 7.2 and the 5 August date. If clause 7.2 carries a carve-out, or defines "taking effect" as the customer's billing date in a way that clears 60 days, the lead critical falls and the decision moves to *approve with minor revisions*. Nothing else found here would move it that far.
