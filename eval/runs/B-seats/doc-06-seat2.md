# Seat 2 — Accuracy & internal consistency

*Tier 1 inferred (artifact ≈280 words), so the six-field list applies; Strengths and Gaps dropped per Step 4's ceiling rule. Written in isolation; no other seat's output seen.*

**Role & remit.** Fact-checker for the posting: are its claims correct, arithmetically possible, and mutually consistent? Standard applied: a job ad's stated facts must be self-consistent and satisfiable by the audience it addresses — derived from the artifact's own text, not an external convention.

**Assessment.** The document states a date and a requirement that cannot both be true for its stated audience. Several other claims are in tension with facts the document itself supplies one line earlier. The technical description (Kubernetes fleet, CI, operator development, production ownership) is internally coherent; the timeline, the on-call terms, and the self-characterisation are not.

**Weaknesses, risks & errors**

| Sev | Type | Anchor (locator + quote) | Problem |
|---|---|---|---|
| Critical | Defect | §About the team, L5: "released version 1.0 of in **March 2024**" vs §Requirements, L16: "5+ years of production experience with Harbourmaster." | Arithmetically impossible. A tool released 1.0 in March 2024 cannot yield 5 years of production experience before March 2029. No external candidate can qualify, and the document never states the tool existed internally 5+ years, so even internal satisfiability is unestablished. Undermines the posting's core purpose (letting a qualified reader self-assess and apply): a recruiter screening on it rejects everyone; a qualified candidate self-rejects. |
| Major | Defect | §What you'll do, L10: "business-hours-first with paging escalation overnight" | Self-contradictory in one clause. "Business-hours-first" implies overnight is not the on-call engineer's burden; "paging escalation overnight" implies it is. A reader cannot determine whether the rotation wakes them. |
| Major | Defect | §How we hire, L32: "The right guy will find the process fast and low on busywork." | Gendered "guy" contradicts the neutral register used everywhere else ("candidates", L18; "engineers", L11). Also asserts the reader's future subjective reaction, which the document cannot know. *(Overlaps seats 1 and 3; reported because visible from my remit as a voice/claim inconsistency.)* |
| Minor | Defect | §How we hire, L32: "a paid take-home of about 4 hours" vs same sentence "low on busywork" | Four stages totalling roughly 7+ candidate hours is characterised as low-effort in the sentence that describes it. The "fast" half is supported by "under three weeks"; the "low on busywork" half is contradicted by the process just listed. |
| Minor | Defect | §Compensation and location, L26–28: "Salary band on request." | Heading promises compensation; section delivers none. Half the heading is unfulfilled. *(Any pay-transparency obligation is seat 3's; I flag only the heading/content mismatch. `[unverified — recall, not lookup]` that EU ad-level pay disclosure rules now bind.)* |
| Minor | Defect | §About the team, L5: "the internal deployment tool **Harbourmaster**, which we open-sourced in 2024" | Two imprecisions that become load-bearing given the critical finding above: a tool described as "internal" is simultaneously described as open-sourced, and "in 2024" is vaguer than the "March 2024" given for 1.0, leaving the open-sourcing/1.0 order undefined. The reader cannot reconstruct the timeline the requirements depend on. |
| Minor | Unverified | §About the team, L5: "Harbourmaster now runs about 4,000 deploys a month." | Cannot be verified from the artifact and carries no denominator — no team size, fleet size, or product-team count is given, so the figure conveys no scale. Recommend an actual check against internal deploy metrics before publication. |
| Minor | Preference | Title L1: "Senior Platform Engineer" vs §Requirements, L15: "8+ years of professional software engineering experience." | The bar (8+ years, operator development, mentoring, end-to-end ownership) sits above what the "Senior" label signals. `[unverified — recall, not lookup]` on the market norm; the internal point stands on the document's own text. |

**Strongest reason this might be fundamentally wrong.** The Harbourmaster clause may not be an error at all. An impossible-for-outsiders requirement, a withheld salary band, and "the right guy" together read as a requisition written around a specific known person. If that is what this is, my accuracy fixes are cosmetic and the document's real defect is that it presents a closed role as an open search — which no amount of date-correcting repairs.

**Domain verdict.** Below the bar a competent professional should produce. One requirement is impossible against a date the document itself supplies; a second is self-contradictory within a single clause; a third contradicts the process described in the same sentence. These are not the ordinary imperfections of good work — they are checkable errors that a single read-through against the document's own facts would catch.

**Recommended fixes** (ordered by impact)

1. Resolve L16. Either state the actual internal first-production date for Harbourmaster and reduce the requirement to what that date permits, or replace it with the transferable skill actually wanted (e.g. "experience owning an internal deployment/PaaS tool"). If the role is genuinely internal-only, say so.
2. Rewrite L10 to state plainly who carries the pager overnight and what the escalation path is.
3. Delete "The right guy will find the process fast and low on busywork." (L32). If a claim about the process is wanted, make it checkable — total candidate hours, and the fact that the take-home is paid.
4. Fix the L5 timeline: give the open-source month, and describe Harbourmaster as "our deployment tool, open-sourced in <month> 2024" rather than "internal ... which we open-sourced."
5. Either publish the band under L28 or rename the heading "Location" and move compensation elsewhere.
6. Verify the 4,000 deploys/month figure against real metrics, and add a denominator (teams or services served) so it means something.
