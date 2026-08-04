# Critical Council Review — `doc-06-job-posting.md`

## 1. Verdict

**Revise substantially before use.** One requirement no external applicant can satisfy makes the advert unable to recruit the audience it addresses; the surrounding material is good and the defects are surgical, not a rewrite.

1. **Fix Requirements L16** — "5+ years of production experience with Harbourmaster." against a tool whose 1.0 shipped March 2024 (L5). Replace with the transferable skill wanted, or state the internal first-production date and lower the floor to what it permits.
2. **Delete the last sentence of "How we hire" (L32)** — "The right guy will find the process fast and low on busywork."
3. **Rewrite L28** — publish the salary band inline and replace "Remote within EU time zones." with the countries Northwind can actually employ in.

## 2. Result & standard

**Under review:** `artifacts/doc-06-job-posting.md`, 225 words, a public recruitment advert for a Senior Platform Engineer at Northwind. Not the model's own prior output.

**Standard:** the artifact's own implied purpose — an external advertisement must let a qualified reader determine eligibility, see why they would want the role, and act on it — plus, for the risk seat, what a competent talent-ops or employment-counsel review would clear for publication in the jurisdictions the advert itself names. No success criteria were supplied by the requester.

**Tier:** 1 (under ~500 words) — 3 seats, six-field list. **Independence mechanism:** parallel isolated seats; none saw another's analysis, and none received requester framing. This verification pass and executive were run as a separate pass with independent re-reading of the artifact, per Step 6.

**Non-negotiable 8:** the artifact contains no text addressed to its reviewer. The only second-person passage (L32) addresses candidates. Nothing to quote; nothing to report on this head. All three seats reached the same conclusion independently.

**Date basis:** 2026-08-05. The critical finding's arithmetic depends on it.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Requirements L16, "5+ years of production experience with Harbourmaster." | No external candidate can hold five years on a tool public since March 2024 (L5), so the advert disqualifies the entire audience it exists to reach | Replace with the transferable skill actually wanted, or state Harbourmaster's internal first-production date and lower the floor to what it permits | Confirmed |
| Major | How we hire L32, "The right guy will find the process fast and low on busywork." | Gendered address in the sentence describing the ideal hire, against the neutral register used everywhere else ("candidates" L18, "engineers" L11) | Delete the sentence | Confirmed |
| Major | Compensation and location L26–28, "Salary band on request." | The heading promises compensation and the section delivers none; senior passive readers screen on pay before spending an outbound step | Publish the band inline; confirm each target country's pay-disclosure position with counsel | Confirmed (legal leg unverified) |
| Major | Compensation and location L28, "Remote within EU time zones." | A time zone is not a jurisdiction, so eligibility is undecidable — the UK, Switzerland, Norway and the Western Balkans share EU time zones and are not EU member states | Name the countries Northwind can employ in, the employment structure, and the required overlap hours | Confirmed |
| Major | How we hire L32, document ends at "...low on busywork." | No application route, contact, link or next step anywhere in the document | Add the apply route, or confirm the ATS/careers page supplies it | Corrected (down from critical; conditional) |
| Major | Requirements L17–18 against What you'll do L9–11 | The absolute Go screen and the operator-development bar map to no duty in the section that describes the work | Add the engineering duties that justify the screens, or drop the screens | Corrected (narrowed) |
| Minor | About the team L5 and whole document | Never states what Northwind sells, team size, benefits, equity or growth path | Add three to five lines of company and offer context | Unverified |
| Minor | How we hire L32, "low on busywork" | Contradicted by the four-stage process described in the same sentence | Drop the claim, or state total candidate hours | Unverified |
| Minor | What you'll do L10, "one week in six, business-hours-first with paging escalation overnight" | An overnight paging obligation is disclosed with no indication of whether it is compensated | State on-call compensation beside the duty | Corrected (down from major) |
| Minor | About the team L5, "the internal deployment tool **Harbourmaster**, which we open-sourced in 2024" | "Internal" and "open-sourced" sit together, and the open-source month is missing while 1.0 is dated — the reader cannot reconstruct the timeline the requirements depend on | Give the open-source month; drop "internal" or date the transition | Unverified |
| Minor | About the team L5, "Harbourmaster now runs about 4,000 deploys a month." | Unverifiable from the artifact and carries no denominator, so the figure conveys no scale | Verify against real metrics; add teams or services served | Unverified |
| Minor | Requirements L15 and L18, "We will not consider candidates without demonstrable Go experience in production." | A fixed year floor and an absolute exclusion foreclose equivalent evidence | Restate as a capability requirement rather than a year count or a bar | Unverified |

**Totals:** 1 critical, 5 major, 6 minor. **Withdrawn at Step 5:** 2. **Severity-corrected or narrowed:** 5.

One preference-tagged item was cut as least load-bearing: Seat 2's observation that the "Senior" title (L1) undersells an 8+ years / operator-development / mentoring bar (L15). It is a real observation and not actionable enough to survive the cut.

## 4. Council roster

- **Seat 1 — Purpose & audience fit.** Owns whether the document does what a job advert exists to do. Belongs because the artifact's dominant failure mode is a document that screens well and sells nothing.
- **Seat 2 — Accuracy & internal consistency.** Owns whether the stated facts are mutually satisfiable. Belongs because the artifact makes dated factual claims that its requirements depend on.
- **Seat 3 — Risk red-team.** The dedicated skeptic; owns legal, compliance and downstream exposure on publication. Belongs because the artifact is a public advert naming a multi-jurisdiction footprint.

Seat 1 also carries the recipient viewpoint — the candidate is the party who ultimately depends on this document.

**Deliberately not covered:**
- **Country-specific advertising and employment compliance.** A critical defect could plausibly live here. All three seats reached the boundary of this domain and correctly stopped, labelling their statutory recall `[unverified — recall, not lookup]`. **The verdict is capped accordingly: this judgment does not cover whether the advert is lawful in any specific target country, and a defect there would raise the severity, not lower it.**
- **Recruiting-market competitiveness** — whether one-in-six on-call, 8+ years and undisclosed pay are competitive terms for the EU senior platform market. A defect here would make the advert underperform, not make it wrong; no seat added.
- **Truth of Northwind's factual claims** (the March 2024 date, the 2024 open-sourcing, 4,000 deploys/month). Not checkable from the artifact by any seat. See blind spots.

## 5. Individual analyses

The three seat analyses are preserved verbatim at `runs/B-seats/doc-06-seat1.md`, `doc-06-seat2.md` and `doc-06-seat3.md`. Per the tier-1 length budget they are not reproduced here; per the Step 6 deduplication rule the following items are struck from the individual sections and stated once in section 3 above:

- **Harbourmaster 5+ years** — struck from Seat 1 (finding 2), Seat 2 (finding 1) and Seat 3 (finding 1).
- **"The right guy"** — struck from Seat 1 (finding 3), Seat 2 (row 3) and Seat 3 (finding 2).
- **"Salary band on request."** — struck from Seat 1 (finding 4), Seat 2 (row 5) and Seat 3 (finding 3).
- **"Remote within EU time zones."** — struck from Seat 1 (finding 5) and Seat 3 (finding 4).
- **"low on busywork"** — struck from Seat 2 (row 4) and Seat 3 (finding 6, second half).

Convergence on these five is evidence for one finding's severity each, not for eleven findings.

## 6. Executive review

### Points of agreement

All three seats, working without sight of each other and without requester framing, independently reached the same reading on five items (listed in section 5). The strongest is the Harbourmaster requirement, which all three ranked at or near the top and all three anchored on the same two strings.

Per non-negotiable 3, I tested *why* they agree rather than counting the agreement. The shared assumption beneath the critical finding is **that the "5+ years" clause is meant to be satisfiable by external applicants** — that this is a genuinely open external requisition. The artifact establishes this only weakly: it reads as a public advert (an "About the team" section, a hiring-process section, a stated remote geography) but never says it is external. The assumption survives attack, because a document that spends its words on candidate-facing recruiting content is most plausibly a candidate-facing advert. Notably, all three seats independently nominated *the same alternative reading* — a requisition written around a pre-selected internal candidate — as their strongest-reason-fundamentally-wrong. Three isolated seats converging on both the finding and its best counter-argument is a genuine signal that the reading came from the artifact rather than from a shared frame. I do not assert the pre-selection hypothesis; intent cannot be established from this text, and non-negotiable 6 bars inventing it. It should be put to the requester directly before publication.

### Points of conflict & adjudication

**1. Severity of "The right guy" — Seat 3 said critical; Seats 1 and 2 said major. Ruled: major.** Seat 3 owns the risk domain, so I do not overrule it on headcount. I overrule it on the evidence its own severity rested on: the critical rating leans on "several EU member states require gender-neutral advertising outright", which Seat 3 correctly labelled `[unverified — recall, not lookup]`. Non-negotiable 6 bars me from ruling that claim true, and without it the harm is a materially narrowed pool plus a quotable line — "materially weakens", not "the recipient acting on it gets a wrong result". The specific evidence for the downgrade: the defect is contained to twelve words, costs nothing to delete, and does not propagate into the requirements or the process, all of which use a neutral register. If the statutory claim is verified in any target country, this returns to critical.

**2. Shape of the Harbourmaster finding — Seat 2 called it "arithmetically impossible"; Seats 1 and 3 called it impossible for outsiders. Ruled: Seats 1 and 3.** Seat 2's arithmetic overreaches. A 1.0 release date does not bound production use — internal tools routinely run in production for years before a 1.0, and the artifact itself calls Harbourmaster "the internal deployment tool ... which we open-sourced in 2024", which positively implies internal use predating public availability. What is established is narrower and still critical: *no external candidate* can hold five years, since the tool has been public roughly two years and five months at the review date. Seat 2's second leg is upheld — the document never states when internal production use began, so even internal satisfiability is unstated.

**3. The on-call clause — Seat 2 read L10 as self-contradictory; Seat 3 read the same twenty words as a plain overnight paging obligation. Ruled: Seat 3.** "Business-hours-first with paging escalation overnight" is a compressed description of a common two-tier policy — handled in business hours where possible, paged overnight for genuine escalations. It is terse, not contradictory, and a reader *can* determine that overnight paging exists. Seat 2's finding is withdrawn. What is undetermined is frequency, threshold and compensation — the last of which survives at minor.

### Verification result

Every one of the twelve anchor strings was searched in the source file rather than recalled; all twelve resolve verbatim. The three absence claims were checked the same way (no `apply`/`contact`/`email`/URL token anywhere; no benefits, equity, headcount or growth token anywhere; no description of Northwind's business beyond the platform team's own internals). No seat fabricated a quote.

**Withdrawn: 2.**
- Seat 1's major "nothing in the document gives the reader a reason to say yes". The supporting sub-claim is literally true (no mission, team size, growth, budget, benefits or equity appears), but the finding as filed — "the posting asks for a great deal and offers, in text, nothing" — is contradicted by the artifact: remote work (L28), ownership of an open-sourced tool running 4,000 deploys a month (L5), end-to-end ownership (L9), a paid take-home and a sub-three-week process (L32) are all offers. Withdrawn as a major; the narrow remnant is folded into the minor company/offer-context finding. Seat 1 flagged this one itself as the finding it expected to fall first — correct self-calibration.
- Seat 2's major on-call contradiction, per adjudication 3.

**Corrected: 5.** Seat 2's critical narrowed in framing (severity held); Seat 3's critical on "the right guy" down to major; Seat 1's critical on the missing apply route down to major; Seat 1's major on requirements/duties narrowed; Seat 3's major on on-call terms down to minor.

The apply-route correction deserves its reasoning stated, since it moved a critical. Asked adversarially what would make it false: a job advert body is very often published through an ATS or careers page that supplies the Apply control, in which case this markdown is complete as body copy and the finding dissolves entirely. Step 5 withdraws findings resting on "a requirement the artifact never took on", and a body-copy document does not obviously take on the apply route. It does not fully dissolve either, because nothing in the artifact establishes that a platform surrounds it. Major, conditional on that question, is the honest position.

The on-call correction likewise: an advert is not an employment contract, standby pay and rest handling are contract and policy matters, and Seat 3's legal leg was `[unverified]`. What survives is that a material term affecting self-selection is undisclosed — the same family as the withheld salary band, at minor.

**Seat reliability.** Seat 2's two errors share a type: reading compressed text as contradiction, and stating an inference as arithmetic. Its contradiction-class findings warrant a second look on future artifacts. Its anchoring discipline is not in question — every quote it produced verified verbatim, so the issue is inference, not fabrication. Seat 3's labelling discipline was the best of the three: every statutory claim carried `[unverified — recall, not lookup]` and it flagged the pay-transparency claim as load-bearing and needing external verification. That is exactly right, and it is also why three of its six findings cannot be rated above what non-statutory reasoning supports. Seat 1's single withdrawal was a rhetorical overreach it predicted itself.

### Panel blind spots

1. **The entire critical finding is downstream of one date the panel could not check.** All three seats took "March 2024" (L5) as given. No seat could do otherwise from the artifact, but if that date is wrong — if Harbourmaster's 1.0 actually shipped in 2019–2021 — the critical finding dissolves and the decision drops a level. **This is the single highest-value external verification before acting.** The same applies to "about 4,000 deploys a month".
2. **Every "missing X" finding rests on one shared, unestablished assumption: that this markdown file is the complete candidate-facing surface.** Missing apply route, missing salary, missing benefits, missing company context — all four assume no careers page, no ATS chrome, no linked benefits page. Three isolated seats shared this assumption because it is the natural reading of a file handed over as an advert, not because they shared a frame. It remains the assumption most likely to be wrong, and it is why one critical was corrected to major.
3. **Country-specific employment and advertising law was examined by no seat.** All three reached its edge and stopped, correctly. A critical defect could plausibly live there — a pay-disclosure or non-discrimination advertising rule in a target country would be a publication blocker in its own right. The verdict is capped: it does not cover this domain.
4. **No seat considered whether the terms are market-competitive** — whether one-in-six on-call, an 8+ year floor and undisclosed pay would attract the seniority sought. A defect there degrades performance rather than correctness, which is why the roster did not add the seat.

### Overall judgment

The underlying material is better than the document. The on-call disclosure is unusually candid and precisely quantified; the take-home is paid and time-boxed; the process is fully disclosed with a stated end-to-end duration; the deploy volume gives a reader real scale; and "a track record of owning systems in production, not just building them" (L19) describes the job rather than a keyword. These are the bones of a strong advert and a competent professional produced them.

What sits on top of those bones fails its purpose. The advert filters hard and sells not at all; it leaves eligibility undecidable on pay, on geography, and — through L16 — on the central requirement, where the answer for every external reader is that they are ineligible. A single read-through against the document's own facts would have caught the Harbourmaster clause, and a single read-through for register would have caught L32. That is below the bar a competent professional should clear, but the distance to clearing it is short: six edits, five of them one line each.

### Decision on further action

**Revise substantially before use.**

Not *approve with minor revisions*: a requirement that disqualifies the entire external audience is a publication blocker under every reading of the artifact. Not *reject and rework*: the structure, the candour and the specific content are sound, and nothing here requires starting over. Not *insufficient information to decide*: the artifact was read in full, and although two open questions (is the requisition genuinely open; is this standalone or body copy) change the *shape* of findings, under every branch L16 and L32 must change before publication.

### Prioritized next steps

1. **Resolve L16 with the hiring manager.** Establish Harbourmaster's internal first-production date and the actual intended bar. If five years is deliberate, confirm the requisition is genuinely open before anything is published.
2. **Delete the last sentence of L32.** One line, zero cost, removes the discrimination exposure and the unearned claim about the reader's reaction in one edit.
3. **Publish the salary band at L28**, and confirm the pay-disclosure position for each target country with counsel — the one legal question in this review that is both load-bearing and unresolved.
4. **Replace "Remote within EU time zones."** with the named countries Northwind can employ in, the employment structure (direct entity, EOR, or contractor) and the required overlap hours.
5. **Confirm whether an apply route is supplied by the publication surface.** If not, add it — a candidate who wants the role must be able to act.
6. **Align "What you'll do" (L9–11) with Requirements (L17–18)**, then add company context, on-call compensation, and the open-source month at L5.
7. **Verify the March 2024 and 4,000 deploys/month claims** against internal records before publishing.

### Confidence & what would change the verdict

Of the six findings reported at critical and major, **I expect four to survive an independent expert re-check with severity unchanged**: the Harbourmaster requirement, "the right guy", the withheld salary band, and the undefined geography. Each is anchored in text verified verbatim, and each was raised by at least two isolated seats on independent reasoning.

**The two I expect to fall first**, in order: the missing application route, which drops to nothing if the document is body copy for a careers page or ATS that supplies the apply control; then the requirements-versus-duties mismatch, where a reviewer may fairly read the platform team's stated ownership of Harbourmaster and the Kubernetes fleet (L5) as implying the hands-on engineering that L9–11 omits, dropping it to minor.

**The verdict rests on:** verified evidence for every quoted anchor and every absence claim; on inference for the central finding, namely that no external candidate can hold five years on a tool public since March 2024 — sound but dependent on the artifact's own date and on a review date of 2026-08-05; and on the assumption that this file is the complete candidate-facing artifact.

**What would flip it.** If the March 2024 date is wrong and Harbourmaster's 1.0 predates 2021, the critical finding dissolves and the decision drops to *approve with minor revisions*. If the requester confirms the role is internal-only or pre-filled, the critical finding changes character — from an error to a failure to disclose a closed search — but the decision does not change. If country-specific pay-transparency or gender-neutral advertising rules are confirmed to bind in the target jurisdictions, severity rises and the decision moves toward *reject and rework* pending legal sign-off.
