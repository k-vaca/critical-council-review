# Seat 1 — Purpose & audience fit

**Artifact:** `artifacts/doc-06-job-posting.md` — "Senior Platform Engineer — Northwind" (~290 words).
**Tier read:** Tier 1 (under ~500 words). Field list per the tier-1 row, plus a short **Strengths** field — dropped by that row, restored here because the posting contains specific earned strengths and suppressing them would skew the seat negative (non-negotiable 1). Deviation stated per the skill's "strong defaults, overridable" clause.
**Isolation:** written without sight of any other seat. No text in the artifact is addressed to its reviewer, so non-negotiable 8 raises nothing to quote.

---

## Role & remit

Hiring-content reviewer. I judge one thing: does this posting do the job a job posting exists to do — get a qualified, largely passive senior platform engineer to read it, correctly self-select, want the role, and apply? Standard applied: a job ad fails if a qualified reader finishes it unable to determine whether they are eligible, unable to see why they would want it, or unable to act on it. That is the artifact's own implied purpose (an open external advertisement), not an imported convention.

## Assessment

The posting reads as a screening document written for the hiring manager's convenience, not as an advertisement written for the candidate. It is precise and honest about what it demands — on-call load, process length, ownership expectations — and near-silent on everything the reader needs to decide in the other direction: pay, eligibility, company, product, growth, and how to apply. The audience it targets (8+ years, employed, choosing between options) is exactly the audience least tolerant of that asymmetry. Two defects are terminal rather than merely costly: a reader who wants the job cannot apply, and a reader who reads the requirements literally is disqualified before they try.

## Strengths

- **Quantified on-call, stated up front.** "one week in six, business-hours-first with paging escalation overnight" (line 10, "What you'll do") — the single fact senior platform candidates screen hardest on, disclosed voluntarily and precisely. Rare and genuinely good.
- **A calibratable scale signal.** "Harbourmaster now runs about 4,000 deploys a month." (line 5, "About the team") lets a reader size the system instead of guessing.
- **A requirement that describes the job rather than a keyword.** "A track record of owning systems in production, not just building them." (line 19, "Requirements").
- **Full process disclosure, take-home paid and time-boxed.** "a paid take-home of about 4 hours" (line 32, "How we hire") — respects the reader's time and reduces drop-off.

## Weaknesses, risks & errors

1. **Critical, defect — there is no way to apply.** The document ends without a link, address, contact, or next step. Absence anchored at the section where it should appear: "We aim to go from first contact to offer in under three weeks." (line 32, "How we hire") is the final substantive sentence. A motivated, perfectly qualified reader finishes the posting and can take no action. This defeats the purpose established above outright.

2. **Critical, defect — the requirement set disqualifies the entire external audience the posting exists to reach.** Anchor: "5+ years of production experience with Harbourmaster." (line 16, "Requirements"), against "we open-sourced in 2024 and released version 1.0 of in March 2024" (line 5, "About the team"). By the artifact's own internal arithmetic, five years of production use of a tool whose 1.0 shipped in March 2024 is available to essentially no one outside Northwind. Reasoned from the artifact only; I have not verified the posting's publication date, and if it were published in 2029 or later this narrows to minor. *Overlaps seat 2 (accuracy/internal consistency) — reported here because the audience consequence is mine: qualified external readers self-select out at the requirements list, which is precisely where the funnel dies.*

3. **Major, defect — the closing line tells the reader the employer pictures a man, and tells him how he will feel.** Anchor: "The right guy will find the process fast and low on busywork." (line 32, "How we hire"). Two failures in twelve words: gendered address narrows the addressable pool against the posting's own interest, and asserting the candidate's reaction pre-empts the legitimate objection a four-hour take-home invites rather than answering it. Tonally it also breaks with the neutral register of every preceding section. *Overlaps seat 3 (risk) on discrimination exposure.*

4. **Major, defect — no compensation figure for a senior, remote, multi-jurisdiction role.** Anchor: "Salary band on request." (line 28, "Compensation and location"). For a passive candidate weighing a move, pay is a gating filter; making them ask converts a zero-cost read into a costly outbound step, and the readers most likely to skip it are the ones with the most options. Pay-range disclosure may additionally be mandatory in some EU jurisdictions this ad targets `[unverified — recall, not lookup]` — flagged for seat 3, not relied on here.

5. **Major, defect — "Remote within EU time zones." (line 28, "Compensation and location") is not a filter a reader can apply.** It does not distinguish time-zone overlap from right to work from countries Northwind can legally employ in. A candidate in Istanbul, Lisbon, or London cannot tell whether they are eligible, so the posting either loses them or wastes both parties' time in screen.

6. **Major, defect — the posting states requirements the described job does not obviously use.** Anchor: "Deep knowledge of Kubernetes, including operator development." (line 17, "Requirements") and "Strong Go. We will not consider candidates without demonstrable Go experience in production." (line 18) — against a "What you'll do" section (lines 9–11) whose three bullets are reliability ownership, on-call, and mentoring, none of which mention building anything. The reader cannot picture the actual week: hands-on operator engineering, or firefighting and coaching. That ambiguity is the difference between attracting a builder and attracting an operator.

7. **Major, defect — nothing in the document gives the reader a reason to say yes.** Absence anchored at the section carrying that burden: "Own reliability for the deployment path end to end." (line 9, "What you'll do") — the section lists three duties, two of them burdens, and no mission, autonomy, team size, growth path, budget, benefits, or equity anywhere in the document. The posting asks for a great deal and offers, in text, nothing. This is the weakest of the majors and the one I would expect an independent reviewer to challenge first, on the grounds that terse ads still convert; I hold it because the ask here is unusually heavy.

8. **Minor, defect — the reader never learns what Northwind is or does.** Anchor: "The platform team owns the substrate every product team builds on: our Kubernetes fleet, the CI pipeline, and the internal deployment tool Harbourmaster" (line 5, "About the team") — the only company context in the document, and it describes the team's internals rather than the business. A senior candidate evaluating a move cannot assess the company; the open-source credential is doing work the product description should do.

## Strongest reason this might be fundamentally wrong

The posting may not be an open external advertisement at all. An impossible tool-specific tenure requirement (weakness 2) is the classic signature of a role already earmarked — an internal backfill, a known-candidate hire, or a compliance posting that must exist publicly but is not meant to convert. Under that purpose the document is doing its job well: narrow, unwelcoming, and unactionable is the point, and my entire critique is measured against a goal it never had. I do not adopt this reading, because nothing in the text signals it and the posting spends its words on genuine recruiting content — team scale, on-call honesty, process transparency — that a compliance posting would not bother with. But if the requester confirms it, findings 1, 3, 4, 6, and 7 mostly dissolve, and the correct finding becomes a different one: a closed role dressed as an open ad wastes applicant time and damages the employer brand it is nominally protecting.

## Domain verdict

**Fails the competent-practitioner standard for its purpose.** A competent recruiting professional does not ship a job ad without an application route; that alone is disqualifying regardless of the copy's quality. Beneath it, the document is well above average on candour and well below average on conversion — it filters hard, sells not at all, and leaves eligibility undecidable on both pay and geography. The underlying material is good: the on-call disclosure, the deploy volume, and the ownership requirement are the bones of a strong ad. It is not a rewrite from zero; it is a substantial revision.

## Recommended fixes

1. Add an application route at the end of "How we hire" — link or address, plus what to send. Nothing else on this list matters until this exists.
2. Resolve "5+ years of production experience with Harbourmaster." (line 16) — almost certainly it should read as Kubernetes/deployment-tooling experience with Harbourmaster familiarity as a nice-to-have. Confirm the intended bar with the hiring manager before publishing.
3. Delete "The right guy will find the process fast and low on busywork." (line 32). Replace with the reason the process is shaped this way, or with nothing.
4. Publish the salary band (line 28), and replace "Remote within EU time zones." with the list of countries Northwind can actually employ in and the required overlap hours.
5. Rewrite "What you'll do" (lines 9–11) so the duties account for the Go and operator requirements, and add three to five lines on Northwind's business, the team's size, and what the person gets — scope, budget, autonomy, growth.
6. Add two or three sentences of company context to "About the team" (line 5) covering what Northwind sells and to whom.

---

*Scope note: analysed within the Purpose & audience fit remit only. Findings 2, 4, and 6 touch territory owned by seats 2 and 3 (internal consistency; legal/reputational risk); reported here per the roster instruction, with the overlap named at each.*
