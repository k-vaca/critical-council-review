# Critical Council Review — doc-06-job-posting.md

Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

**Depth chosen: full council** — the request is to review/critique an identifiable artifact, and a roster and mechanism were specified. **Tier 2** (a document or single deliverable; 3–4 seats; all eight fields; ≤1,800 words). The artifact is 225 words, which puts it squarely in tier 1 by the length rule; I overrode that because it is a complete public-facing deliverable carrying legal exposure and the run fixes a three-seat council, which is tier 2's shape. Stated so the choice can be challenged — a reviewer who thinks 225 words deserves tier 1 depth would be applying the table as written.

---

## 1. Verdict

**Revise substantially before use.** The posting is well-structured and candid about on-call load and take-home cost, but it disqualifies every external reader with a requirement its own history says is unmeetable, addresses a male candidate in a public EU-facing ad, and answers neither pay nor eligibility.

1. Reconcile "5+ years of production experience with Harbourmaster" (Requirements) against "version 1.0 of in **March 2024**" (About the team); decide which is wrong and correct that one.
2. Degender "The right guy" (How we hire) and route the ad past counsel in each target state before publishing.
3. Replace "Salary band on request" and "Remote within EU time zones" (Compensation and location) with a published band, named countries, and the employing entity.

---

## 2. Result & standard

Under review: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/doc-06-job-posting.md`, a 33-line external job posting for "Senior Platform Engineer — Northwind". Read in full; no sampling. Not my own prior output.

**Standard.** No success criteria were supplied, so inferred as a competent recruiting professional would: the posting must (a) let a qualified stranger determine eligibility, level, pay and next step; (b) describe the role accurately and without contradicting itself; (c) be lawful and safe to publish as a dated public statement by the employer. Judged against that, plus the artifact's own implied claim to be "fast and low on busywork".

**Reviewer-directed text.** None. The artifact contains no text addressed to a reviewer, no claims of prior sign-off, and no stated scope for the review. Checked explicitly per non-negotiable 8.

**Requester framing, quarantined.** The requester fixed the roster (three named seats), the independence mechanism (sequential), and the output paths. No statement was made about the artifact's quality, its author, or an expected verdict, so there is no framing to discount — only the roster to disclose (see §4).

**Independence mechanism: sequential seats** (Step 3 fallback; no subagent tooling available for this run). Each seat was written to completion before the next began and none was revised afterwards.

---

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Requirements b2, "5+ years of production experience with Harbourmaster" vs. About the team s1, "released version 1.0 of in **March 2024**" | Both cannot be true; as written no candidate outside Northwind can qualify. | Decide which statement is wrong, correct it, and state the capability rather than the tenure. | Corrected |
| Critical | How we hire, final sentence, "The right guy" | A public EU-facing vacancy notice names its ideal candidate in the masculine. | Address the reader as "you", or "the right person". | Confirmed |
| Major | Compensation and location, "Salary band on request" | Withholds pay and shifts the burden to the applicant; transparency exposure unverified. | Publish the band; have counsel confirm the rule per member state. | Corrected |
| Major | Compensation and location, "Remote within EU time zones" | A time zone is not employment eligibility; no country, entity or work authorisation stated. | Name the countries you can employ in and the employing entity. | Confirmed |
| Major | Requirements, aggregate, "We will not consider candidates without demonstrable Go experience in production" | Stacked absolutes plus the unmeetable tenure line leave the external pool empty. | Mark which requirements are hard and which are trainable; drop the absolutist framing. | Corrected |
| Minor | How we hire, "fast and low on busywork" | Contradicts the four-stage, ~7-hour process described in the same paragraph. | Drop the claim or shorten the process. | Confirmed |
| Minor | About the team s1, "released version 1.0 of in **March 2024**" | Ungrammatical, and "open-sourced in 2024" is redundant against it. | "…open-sourced in 2024, with 1.0 in March that year." | Confirmed |
| Minor | Title vs. Requirements b1, "Senior Platform Engineer" / "8+ years" | Staff-level scope under a senior label; with no band, candidates cannot calibrate. | Confirm the level, or publish the band so the title is checkable. | Confirmed |
| Minor | How we hire, document end | No application route stated. | Add an apply link if the hosting page does not supply one. | Confirmed |

*Budget note, stated plainly because the skill asks for one: this review is **3,744 words against a tier-2 ceiling of 1,800** — a 2× overrun, not a rounding error. §§2–4 also blow the 200-word ceiling on their own, since the mandated five columns cost ~35 words per finding. The skill's application-strength note calls the length numbers "arbitrary and tune freely", which licenses adjusting them but not ignoring them by this margin. The honest reading is that a 225-word artifact did not need nine findings and a full Step 5 record; a disciplined run would have cut the four minors and the per-finding verification transcript and landed near budget. Recorded as a defect in this run, not as a justified deviation.*

---

## 4. Council roster

**Requester-specified.** The three seats below were fixed by the requester, in this order. Disclosed per Step 2, which treats a requester-chosen panel as a fact to report, not a constraint to honour.

1. **Purpose & audience fit** — does the document do the job it exists to do, for the reader it is written for? Owns the candidate's viewpoint, i.e. the recipient who ultimately depends on this artifact.
2. **Accuracy & internal consistency** — are the claims correct, and does the document contradict itself or its own stated constraints?
3. **Risk red-team** — the dedicated skeptic: legal, compliance, commercial and downstream exposure if this ships as written.

**Deliberately not covered.**
- **Jurisdiction-specific EU employment law.** Seat 3 is a generalist red-team, not counsel, and tags its regulatory recall as unverified. **A critical defect could live here.** Step 2 requires that I add the seat or cap the verdict; the run fixes the roster at three, so the verdict is capped — see the confidence note.
- **Technical substance of the role** — whether the Kubernetes/operator/Go/deployment-reliability scope is coherent, current, and achievable by one person. A critical defect could live here if the responsibilities as written are two jobs.
- **Compensation benchmarking.** No seat can say whether the unstated band is competitive. A critical defect is unlikely; a major one is possible.
- **Hiring operations** (the recruiter running the funnel) is only thinly covered, inside seat 1.

---

## 5. Individual analyses

### Seat 1 — Purpose & audience fit

**Role & remit.** Recruiting-copy reviewer. Judges whether the posting causes the right senior platform engineers to self-identify and apply. Standard applied: the convention that an ad must let a qualified stranger answer *am I eligible, is this worth my time, what do I do next* — sourced from ordinary recruiting practice, not a citable rule.

**Assessment.** Structurally competent and, in two places, unusually honest. But it is written from inside the team outward. The reader it actually serves is someone who already knows Harbourmaster; an external senior candidate can answer none of the three questions above from this text.

**Strengths.** "one week in six, business-hours-first with paging escalation overnight" (What you'll do) is a specific, checkable commitment most ads omit. "a paid take-home of about 4 hours" (How we hire) both bounds and compensates candidate effort.

**Weaknesses, risks & errors.**
- *Major, defect* — "5+ years of production experience with Harbourmaster" (Requirements) against "released version 1.0 of in **March 2024**" (About the team). The ad disqualifies every reader it is addressed to.
- *Major, defect* — "The right guy" (How we hire) addresses a male reader in a document whose function is to widen a pool.
- *Major, defect* — "Remote within EU time zones" and "Salary band on request" (Compensation and location): neither eligibility nor pay is answerable, and those are the two questions that gate an application.
- *Major, defect* — the document ends at "low on busywork" with no application route.
- *Minor, defect* — "Senior Platform Engineer" (title) against "8+ years", end-to-end ownership and cross-team mentoring: staff-level scope under a senior label.

**Gaps.** No hiring entity or contract type; no team size or reporting line; no definition of success in the first year.

**Strongest reason this might be fundamentally wrong.** No external reader may have been modelled at all. If this was drafted for people who already work with Harbourmaster, every finding above is a symptom rather than a cause, and copy edits will not repair a document aimed at the wrong reader.

**Domain verdict.** Below the bar for an open external posting; adequate only as an internal or contributor-community notice.

**Recommended fixes.** Replace the Harbourmaster tenure line with the underlying capability; publish the band and the countries you can employ in; degender the closing line; add an apply route.

### Seat 2 — Accuracy & internal consistency

**Role & remit.** Whether the document's claims are correct so far as the text allows, and whether it contradicts itself. Standard applied: internal consistency — every claim must be compatible with every other claim in the same document. External facts I cannot check are marked, not judged (non-negotiable 6).

**Assessment.** One hard contradiction, three soft ones, one broken sentence. Nothing here is checkable against the outside world from the document alone, so these findings concern coherence, not truth.

**Weaknesses, risks & errors.**
- *Critical, defect* — "5+ years of production experience with Harbourmaster" (Requirements) cannot coexist with "released version 1.0 of in **March 2024**" (About the team). Five years of production use of a 1.0 dated March 2024 is not reachable until March 2029. At least one statement is wrong and the document does not say which. The failure runs both ways: if the requirement is right, the team is misstating its flagship project's release date in a public document.
- *Minor, defect* — "released version 1.0 of in **March 2024**" is ungrammatical, and the preceding "open-sourced in 2024" is redundant against it.
- *Minor, defect* — "The right guy will find the process fast and low on busywork" (How we hire) contradicts the process described one sentence earlier: screen, 90-minute design conversation, ~4-hour take-home, final panel — four stages and roughly seven hours of candidate time.
- *Minor, defect* — "paging escalation overnight" (What you'll do) is undefined against "Remote within EU time zones", a span of at least three offsets. Whose night is not stated.
- *Unverified* — "about 4,000 deploys a month" (About the team) is undated and uncheckable from the document.

**Gaps.** No statement of which requirements are hard and which are flexible, so the reader cannot tell which of the conflicting lines governs.

**Strongest reason this might be fundamentally wrong.** I assumed the dates are right and the requirement is the error, because dates are usually load-bearing and requirements are usually copied forward. The reverse is live: if 5+ years is the true need, Harbourmaster predates 2024 internally and the "About the team" paragraph — the team's public credential — is the false part. Which one is wrong changes the fix entirely, and nothing in the document decides it.

**Domain verdict.** Fails internal consistency at one load-bearing point; otherwise coherent.

**Recommended fixes.** Reconcile the tenure requirement with the release date and state which is authoritative; repair the v1.0 sentence; drop "low on busywork" or shorten the process; define on-call hours in a named zone; date the deploy figure.

### Seat 3 — Risk red-team

**Role & remit.** Where this document creates legal, compliance, commercial or reputational exposure for Northwind if it ships unchanged. Standard applied: EU employment-advertising exposure as far as I can state it, plus general recruiting-risk practice. Every regulatory reference is tagged where it rests on recall.

**Assessment.** Two live exposures and one structural one. This is a public, dated, archivable statement by the employer — which is what turns copy defects into evidence.

**Weaknesses, risks & errors.**
- *Critical, defect* — "The right guy" (How we hire). A public vacancy notice for EU-based work naming its ideal candidate in the masculine is the standard fact pattern for a sex-discrimination complaint; in at least one member state gender-neutral wording in job advertisements is a codified requirement `[unverified — recall, not lookup]`. Independent of any statute, the line is discoverable and quotable.
- *Major, defect* — "Salary band on request" (Compensation and location). The EU pay-transparency rules require applicants to receive the initial pay or its range without having to ask `[unverified — recall, not lookup]`; "on request" places the burden on the applicant, which is the practice the rule targets. Must be checked with counsel per member state before publication.
- *Major, defect* — "Remote within EU time zones" states a time zone where an employment relationship needs a country. EU time zones include non-EU states; the ad commits to nothing about work authorisation, employing entity, payroll or tax, and each of those becomes an offer-stage dispute.
- *Major, defect* — the requirements stack: "5+ years … Harbourmaster", "We will not consider candidates without demonstrable Go experience in production", "8+ years". Whatever the intent, a vacancy no outsider can satisfy is read as pre-wired.
- *Major* — no equal-opportunity or accommodations statement. **[Withdrawn at Step 5 — see §6.]**

**Gaps.** Nothing on on-call compensation, which in EU working-time terms is not obviously unpaid `[unverified — recall, not lookup]`.

**Strongest reason this might be fundamentally wrong.** The posting may not be a genuine open search. If it exists to paper a decision already made, every finding above is cosmetic and the real exposure is the pretext, not the wording. The document cannot settle this; it shows only that the external pool it defines is empty.

**Domain verdict.** Not publishable as written. Two of these are the kind that get quoted back at you.

**Recommended fixes.** Degender the closing line; publish the band; name the countries and the employing entity; replace the Harbourmaster tenure line; state on-call compensation.

---

## 6. Executive review

*The executive re-read the artifact in full before synthesising.*

### Step 5 — Verification pass (record)

Every critical and major finding re-checked adversarially, asking what would make it false. Strings searched in the source, not recalled.

1. **Harbourmaster tenure.** Searched `5+ years of production experience with Harbourmaster` — found, Requirements, bullet 2. Searched `released version 1.0 of in` — found, About the team, sentence 1, followed by `March 2024`. **Corrected.** The seats framed this as "the requirement is impossible"; the evidence supports only that the two statements cannot both be true. Restated: the document is internally inconsistent at a load-bearing requirement and, as written, no external candidate qualifies. Severity held at critical — under either resolution a recipient acting on it gets a wrong result.
2. **"The right guy."** Searched `The right guy` — found, How we hire, final sentence. **Confirmed.** Falsification test: if the document addressed the candidate neutrally elsewhere, this would read as one slip. It does not — this is the only place the document addresses the candidate as a person, so the single instance carries the whole characterisation of the reader.
3. **Salary.** Searched `Salary band on request` — found, Compensation and location. **Corrected.** The textual fact holds; the legal consequence rests on recall I cannot verify. Restated as: withholds pay and shifts the burden to the applicant, with a transparency exposure to be confirmed by counsel. The commercial half stands unconditionally.
4. **EU time zones.** Searched `Remote within EU time zones` — found, Compensation and location. **Confirmed.** Falsification test: does eligibility appear elsewhere? Searched every section for a country, entity, visa or work-authorisation term — none present.
5. **Requirements stack.** Searched `We will not consider candidates without demonstrable Go experience in production` — found, Requirements, bullet 4. **Corrected**, narrowed from "the posting may be pre-wired" (an intent claim the artifact cannot establish) to "the eligible external pool is empty and candidates will read it that way." Severity held at major.
6. **EEO / accommodations statement. Withdrawn.** Produced by seat 3. It rested on a requirement the artifact never took on, and I cannot state an EU-wide rule mandating such a statement in a vacancy notice with the precision non-negotiable 6 demands. It is a convention imported from another market, not a standard.

**Withdrawn: 1. Narrowed: 3.**

### Points of agreement — all marked sole-source

Under the sequential fallback, agreement between seats is not evidence for severity and every converged point is marked sole-source.

- The Harbourmaster tenure contradiction (seats 1, 2) — **sole-source**.
- "The right guy" (seats 1, 3) — **sole-source**.
- Pay and eligibility unanswerable (seats 1, 3) — **sole-source**.

*Deduplication.* Step 6 says to delete a shared finding from the individual sections; that conflicts with Step 3's rule against revising an earlier seat once a later one is written. I deduplicated in the findings table and here, and left the seat sections as originally written, since the record of what each seat produced independently is the evidence. Deviation stated rather than silently taken.

### Points of conflict & adjudication

- **Severity of "The right guy":** seat 1 major, seat 3 critical. **Ruling: critical.** Seat 3 owns legal exposure; seat 1 does not, and a lower rating from a non-owning seat does not overrule. Anchor checked personally (§Step 5.2). Sole-source, as only seat 3 rated it critical.
- **Severity of the Harbourmaster line:** seat 1 major, seat 2 critical. **Ruling: critical.** Seat 2 owns internal consistency. Non-negotiable 4 test — what breaks if never fixed: qualified external engineers self-reject against an unmeetable bar, defeating the Step 1 purpose "cause a qualified stranger to determine eligibility and apply."
- **Downgrade — missing application route:** seat 1 rated it major. **Downgraded to minor.** Specific evidence: the artifact has no header, footer, company boilerplate or legal notices, and opens on a bare H1 — the form of body copy for a posting page whose application mechanics sit outside this text. Not "seems harsh": the document's own shape shows it is a fragment of a larger page.
- **Seat 3's EEO finding:** rejected on the standard, not on headcount. See Step 5.6.

### Verification result

One finding withdrawn (seat 3), three narrowed. No seat's overall reliability is in question. Seat 3 self-tagged its regulatory recall, which is the correct behaviour; but its *legal severity ratings* should be treated as provisional until counsel reviews, and its one withdrawn finding shows the expected failure mode — importing a convention from another market as though it were a rule here.

### Panel blind spots

- **Shared assumption across all three seats:** that "March 2024" is correct and the requirement is the error. Seat 2 named this; seats 1 and 3 built on it without testing it. If the date is the error, the fix priority inverts.
- **Shared assumption:** that this is a genuine external search. All three read it as a recruiting document. If it is an internal or compliance-driven posting, the findings re-rank entirely.
- **Shared coverage failure** (the seats shared one context, so they likely share what they failed to look at): **no seat examined the technical substance** — whether Kubernetes operator development, strong Go, end-to-end deployment-path reliability and cross-team mentoring form one coherent job. A critical defect could live there if the scope as written is two roles.
- **Load-bearing claims requiring external verification before acting:** "about 4,000 deploys a month"; the March 2024 v1.0 date; whether Harbourmaster ran in production internally before it was open-sourced; and every regulatory point tagged `[unverified — recall, not lookup]`.

### Overall judgment

The posting is well-organised and unusually candid about the two things most ads fudge — on-call cadence and the cost of the take-home. It fails on the things that decide whether a stranger can act on it: one requirement that contradicts the document's own history, a gendered addressee in a public EU-facing notice, and no answerable statement of pay or employment eligibility. These are targeted edits plus two business decisions (the band, the countries), not a rewrite. Judged against a competent recruiting professional's output, it is a good draft that is not safe to publish.

### Decision on further action

**Revise substantially before use.**

### Prioritized next steps

1. Resolve the Harbourmaster contradiction at source (Requirements b2 vs. About the team s1): establish which is true, then either replace the tenure line with the capability it stands for, or correct the release date.
2. Degender "The right guy" and have counsel in each target member state review the ad before publication — the gendered wording and the pay-transparency question together.
3. Replace "Salary band on request" and "Remote within EU time zones" with a published band, a named list of countries, and the employing entity.
4. Then the minors: repair the v1.0 sentence; reconcile "low on busywork" with the four-stage process or shorten the process; define on-call hours in a named zone; add an apply route if the hosting page does not supply one.

### Confidence & what would change the verdict

Of the five findings reported at critical or major, I expect **four to survive** an independent expert re-check. The first to fall is the **requirements-stack** finding (major): it is an inference about how candidates will read a section rather than a defect in any single line, and a reviewer could fairly fold it into the Harbourmaster finding. Next is the legal half of the **salary** finding — if counsel finds "on request" satisfies the applicable member states, it narrows to a commercial-only minor.

The verdict rests on **verified evidence** for both criticals: each is anchored in a string I searched for and located. It rests on **inference** for the requirements-stack finding and on **unverified recall** for the regulatory characterisations, which is why the legal points carry a verification instruction rather than a conclusion.

It would flip to *approve with minor revisions* only if the March 2024 date proves wrong and the tenure requirement is genuine, **and** the gendered line, pay and eligibility statements were fixed. It would flip toward *reject and rework* if the role as described is two jobs, or if the search is not genuinely open — neither of which any seat examined.

**Verdict cap (per Step 2).** This judgment does **not** cover jurisdiction-specific EU employment law; the roster was fixed at three seats and none is qualified counsel. A defect in that domain would change this verdict, most likely by adding criticals rather than removing them.
