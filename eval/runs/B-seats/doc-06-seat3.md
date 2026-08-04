# Seat 3 — Risk red-team

*Artifact: `doc-06-job-posting.md` (~280 words) → tier 1 field list: Role & remit, Assessment, Weaknesses, Strongest reason, Domain verdict, Recommended fixes. Strengths and Gaps dropped per the tier table.*

*Budget note: the tier-1 per-seat ceiling is ≤140 words; this seat runs over because six anchored findings will not compress further. If the executive must cut, findings 5 then 6 are least load-bearing.*

*Date basis: assessed as of 2026-08-05. Findings 1 and 3 depend on that date — re-run the arithmetic if the review date differs.*

*Non-negotiable 8 check: no text in the artifact is addressed to its reviewer. The one second-person passage (line 32) addresses candidates.*

**Role & remit.** Pre-publication risk review of a public recruitment advert: the legal, compliance, commercial and downstream exposure Northwind assumes if this ships verbatim. Standard applied: what a competent employment counsel or talent-ops lead would clear for publication in the jurisdictions the advert itself names ("Remote within EU time zones", line 28). Source: standard pre-publication advert review. Legal instruments named from memory are labelled `[unverified — recall, not lookup]`; no severity below depends on a citation being exact.

**Assessment.** Exposure runs on three independent axes: a headline requirement no outside applicant can satisfy, wording and omissions that are live compliance issues in the exact jurisdictions targeted, and material terms — pay, country, on-call compensation — left undefined in a document candidates read as an offer preview. The paid take-home (line 32) is the one genuinely risk-reducing element present. I would not clear this for publication.

**Weaknesses, risks & errors.**

1. **Critical · defect — the headline requirement is satisfiable only by an insider.** Anchor: "5+ years of production experience with Harbourmaster." (Requirements, line 16), read against "we open-sourced in 2024 and released version 1.0 of in March 2024" (About the team, line 5). At 2026-08-05 the tool has been public roughly two years five months, so five years of production use implies use inside Northwind about three years before it was public. Purpose undermined (non-negotiable 4): an advert exists to solicit applications from people who can be hired; line 16 disqualifies every external reader, so it cannot do that job. Exposure: a requirement only an incumbent can meet is the standard fingerprint of a role written around a pre-selected candidate — the pattern regulators probe in labour-certification and public-procurement settings `[unverified — recall, not lookup]`. Overlap noted: seat 2 owns the timeline arithmetic; I own what publishing it costs.

2. **Critical · defect — gendered wording in an advert aimed at EU jurisdictions.** Anchor: "The right guy will find the process fast and low on busywork." (How we hire, line 32). "Guy" is masculine-coded and sits in the sentence describing the ideal hire. In a public advert that is quotable documentary evidence for a rejected applicant's sex-discrimination claim, and several EU member states require gender-neutral advertising outright `[unverified — recall, not lookup]`. Statute aside, it narrows the pool for a role already hard to fill. One word, zero cost to fix, open-ended downside.

3. **Major · defect — no pay information disclosed.** Anchor: "Salary band on request." (Compensation and location, line 28). The EU pay-transparency regime requires applicants to be told initial pay or its range before interview, with member-state transposition due June 2026 — before this review date `[unverified — recall, not lookup; load-bearing, verify against each target country's transposed law before publishing]`. Commercially it also screens out senior candidates who decline to enter a process blind.

4. **Major · defect — employment geography undefined, and wrong as stated.** Anchor: "Remote within EU time zones." (line 28). A time zone is not a jurisdiction: the UK, Switzerland, Norway and the Western Balkans share EU time zones and are not EU member states. The advert names no country Northwind can actually employ in, no employer-of-record or contractor structure, and no right-to-work condition — attracting applications that cannot convert and deferring payroll, social-security and permanent-establishment questions until after an offer.

5. **Major · defect — an on-call duty with no compensation or rest terms.** Anchor: "Take part in the platform on-call rotation (one week in six, business-hours-first with paging escalation overnight)." (What you'll do, line 10). Overnight paging is a standby obligation with working-time and daily-rest consequences across EU jurisdictions, and standby has been held to count as working time depending on the constraint imposed `[unverified — recall, not lookup]`. Stating the duty while omitting standby pay and rest handling is the classic setup for a post-hire dispute; it compounds finding 3.

6. **Minor · defect — absolute screens stated in absolute language.** Anchors: "8+ years of professional software engineering experience." (line 15) and "We will not consider candidates without demonstrable Go experience in production." (line 18). Fixed year-count floors act as an age proxy and hard exclusions foreclose equivalent evidence. Both are common practice, so exposure is modest — but "we will not consider" is the sentence read back in a complaint. Lower still, same line 32: the advert calls the process "low on busywork" while describing a screen, 90 minutes, a four-hour take-home and a panel, a claim candidates can check against that same paragraph.

**Strongest reason this might be fundamentally wrong.** That this is not a genuine open requisition. Finding 1 is not a typo pattern — a five-year floor on a two-year-old public tool is what a role written around an already-chosen internal candidate looks like. If so, every other fix here is cosmetic and the real exposure is publishing a pretextual advert, collecting applications that were never live, and the cost when that becomes visible. I cannot establish intent from the text and do not assert it; I can say the text is indistinguishable from that case, and the requester should be asked directly before publication.

**Domain verdict.** Fails the pre-publication bar on more than one independent ground. No competent employment-counsel or talent-ops review clears this as written; findings 1 and 2 are each individually blocking.

**Recommended fixes.**
1. Resolve line 16 — delete the Harbourmaster year floor or replace it with "experience with a comparable internal deployment platform"; if five years is deliberate, confirm the requisition is genuinely open before anything is published.
2. Delete "the right guy"; rewrite the sentence without a gendered noun and run the full text through a gender-coded-language check.
3. Publish the salary band inline at line 28, and confirm the pay-transparency position for each target country with counsel.
4. Replace "EU time zones" with the named countries Northwind can employ in, plus the employment structure (direct entity, EOR, or contractor) and a right-to-work line.
5. Add on-call compensation and rest-period terms beside line 10.
6. Soften line 18 to a capability statement, and either drop the "low on busywork" claim or state the total candidate time the process consumes.
