# Review — doc-06-job-posting.md

Artifact: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/doc-06-job-posting.md`
Review date: 2026-08-05
Scope: one expert pass, hiring/recruiting-content review. Judged against what a competent recruiter or hiring manager should ship.

## Summary

The posting is well structured and unusually honest in places — the on-call load is quantified (one week in six, overnight paging), the take-home is paid and time-boxed, and the hiring timeline is stated. Those are above-average.

But it carries one requirement that is arithmetically impossible to satisfy, which alone makes the posting non-functional: it would reject every applicant. Two further defects create legal and self-selection exposure for EU-based hiring. Five smaller items are worth fixing before publication.

Total: 1 critical, 2 major, 5 minor.

---

## Critical

### C1 — Requirement is impossible to meet; screens out 100% of applicants

- **Severity:** critical
- **Location:** line 16 (Requirements), interacting with line 5 (About the team)
- **Anchor:** "**5+ years of production experience with Harbourmaster.**"
- **Problem:** Harbourmaster was open-sourced in 2024 and hit 1.0 in March 2024, so no external candidate can have more than roughly 2 years and 5 months with it as of August 2026, making the requirement unsatisfiable by anyone outside the company.

**Detail.** The posting itself supplies the contradicting fact two sections earlier: the tool is described as internal, open-sourced in 2024, with 1.0 released March 2024. Maximum possible public production exposure is ~29 months. Even generously counting pre-open-source use, nothing in the document supports a five-year history, and any such history would be internal-only — i.e. available only to people already at Northwind, which defeats the purpose of an external posting. A recruiter screening literally against this bullet rejects the entire funnel; a candidate reading it self-rejects. Either way the posting fails at its job.

**Fix.** Drop the bullet, or restate it as what is actually being tested — e.g. "Experience operating an internal deployment/release platform at scale; familiarity with Harbourmaster is a plus." Cross-check every other year-count against the timeline in "About the team" while doing this.

---

## Major

### M1 — Gendered language in the closing line

- **Severity:** major
- **Location:** line 32 (How we hire)
- **Anchor:** "The right guy will find the process fast and low on busywork."
- **Problem:** "Guy" genders the ideal candidate, which measurably suppresses applications from women and, in several EU jurisdictions the posting is targeting, makes a job advertisement legally challengeable.

**Detail.** The role is advertised "Remote within EU time zones." Several member states prohibit gender-specific job advertising outright and attach penalties to it, so this is not only a tone problem — it is publication risk on a document whose whole purpose is publication. It also sits in the last line, the position readers retain best.

**Fix.** "The right person will find the process fast and low on busywork." One-word change; no other edit needed. Sweep the rest of the copy for the same pattern while there.

### M2 — Salary withheld from an EU-targeted posting

- **Severity:** major
- **Location:** line 28 (Compensation and location)
- **Anchor:** "Salary band on request."
- **Problem:** Withholding the band from an EU-facing posting conflicts with pay-transparency obligations now in force across the EU and drives measurable candidate drop-off at exactly the seniority this role targets.

**Detail.** The EU pay transparency directive's transposition deadline (7 June 2026) has passed as of this review date, and applicants are entitled to initial pay information without having to ask; some member states already required ranges in the advertisement itself before that. Beyond compliance: senior platform engineers with the Kubernetes-plus-Go profile described here are in a candidate's market and routinely skip postings that hide the band. The section heading promises "Compensation" and then delivers none, which reads as a signal about the band rather than about process.

Secondary omission in the same section: the posting mandates a one-week-in-six rotation with overnight paging (line 10) but says nothing about on-call compensation, time off in lieu, or paging frequency. For senior candidates this is a material term.

**Fix.** Publish the band and the currency/basis, note the leveling, and state the on-call arrangement (paid, TOIL, or built into base).

---

## Minor

### m1 — "EU time zones" conflates working hours with employment eligibility

- **Severity:** minor
- **Location:** line 28 (Compensation and location)
- **Anchor:** "Remote within EU time zones."
- **Problem:** A time zone is not a hiring jurisdiction, so candidates cannot tell which countries Northwind can actually employ or contract in, or whether right-to-work sponsorship exists.

**Fix.** Name the countries or entities you can hire in (or say "via EOR in X, Y, Z"), state employee vs contractor, and state the required overlap hours separately.

### m2 — Redundant and imprecise dating of Harbourmaster's release

- **Severity:** minor
- **Location:** line 5 (About the team)
- **Anchor:** "which we open-sourced in 2024 and released version 1.0 of in **March 2024**"
- **Problem:** The sentence states the same year twice at two different precisions and the "released version 1.0 of in" construction is awkward, leaving the open-source and 1.0 milestones ambiguously ordered.

**Fix.** "which we open-sourced and released as 1.0 in March 2024" — or give the two distinct dates if they genuinely differ.

### m3 — Advertised level is below the level the requirements describe

- **Severity:** minor
- **Location:** line 1 (title) vs. lines 9–11 and 15
- **Anchor:** "Senior Platform Engineer — Northwind" / "8+ years of professional software engineering experience."
- **Problem:** End-to-end ownership of the deployment path plus cross-organization mentoring plus an 8-year floor is staff-level scope, so the "Senior" label will attract and price the wrong candidates.

**Fix.** Either retitle to Staff, or lower the years floor and narrow the ownership language to match a senior IC.

### m4 — No route to apply

- **Severity:** minor
- **Location:** line 32 (How we hire), end of document
- **Anchor:** "We aim to go from first contact to offer in under three weeks."
- **Problem:** The document describes the process in detail but never says how "first contact" is made — no link, no address, no named recruiter.

**Fix.** Add an apply link or contact address as the final line.

### m5 — No description of Northwind, benefits, or equal-opportunity statement

- **Severity:** minor
- **Location:** document-level (no section covers it)
- **Anchor:** "The platform team owns the substrate every product team builds on"
- **Problem:** The posting opens on the team without ever saying what the company does, and omits benefits and an EO statement, all of which competent postings at this level include.

**Fix.** Add two sentences on Northwind's product and market, a short benefits line, and a standard equal-opportunity statement.

---

## Things that are right, and should survive editing

- On-call load is quantified honestly rather than buried ("one week in six, business-hours-first with paging escalation overnight"). Most postings hide this.
- The take-home is paid and explicitly time-boxed to ~4 hours.
- The Go requirement is stated as an absolute filter instead of a soft preference, which saves both sides time.
- Line 19 tests for operational ownership rather than another tool keyword — a good, non-proxy requirement.
- Total pipeline length is committed to in writing.
