# Critical Council Review — doc-04-privacy-notice.md

*Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.*

---

## 1. Verdict

**Revise substantially before use.** Section 7 opens with a deletion promise the same section then contradicts three times, and sections 5 and 6 omit disclosures a transparency notice is expected to carry.

1. **§7, line 29** — delete the sentence "This applies to all categories described in section 4" and make the 30-day rule expressly subject to the exceptions that follow it.
2. **§5, lines 11–17** — add a "Legal obligation" row for the seven-year tax retention that §7 already commits to.
3. **§6, lines 21–25** — add international transfers, legally compelled disclosure, and business-transfer sharing; qualify "cannot identify you" and "We do not sell personal data".

---

## 2. Result & standard

Judged: the whole supplied artifact, sections 4–7 of a Northwind privacy notice, read in full. Not my own prior output. **Tier 2** (a single deliverable; the sub-500-word row would have forced cutting real legal findings — alternative reading noted). **Independence mechanism: sequential seats** — no subagent tooling available for this run.

Standard: a customer-facing transparency notice that lets a reader learn what is collected, why, who receives it and for how long, at the level a competent privacy drafter would produce. The artifact's own §5 uses GDPR Article 6 vocabulary ("Performance of a contract", "Legitimate interests", "Consent"), so that framework is taken from the text, not imported.

Text addressed to a reviewer: the title reads "Privacy Notice — Sections 4 to 7 (draft for legal review)" (line 1). Quoted per non-negotiable 8. It is a status label, not a scoping instruction or a claim of pre-approval, so it does not narrow this review and is not itself reported as a finding.

Length: this review runs to roughly 3,200 words against the tier-2 ceiling of 1,800. Tuned deliberately under the skill's own classification of the length budget as arbitrary — the mandated three-seat roster plus the full Step 4 field list, the Step 5 pass and the Step 6 structure will not compress further without dropping a seat or a finding, and neither is a trade worth making on a legal document. Nothing was truncated and no seat was dropped.

Boundary limit carried into the verdict: this is an excerpt. Sections 1–3 and any section 8+ were not supplied, so findings about material that conventionally lives elsewhere in a notice (data-subject rights, transfers) are marked excerpt-bounded rather than asserted absent from the whole document.

---

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | §7 line 29, "This applies to all categories described in section 4" | The 30-day deletion promise is contradicted by the seven-year, 90-day and 18-month periods in the same section. | Strike the sentence; make the 30-day rule expressly subject to the exceptions below. | Confirmed |
| Major | §5 lines 11–17, table of legal bases | No "Legal obligation" row, yet §7 retains records seven years "as required by tax law". | Add a tax/accounting-compliance purpose on a legal-obligation basis. | Confirmed |
| Major | §5 line 13, "Providing the service you signed up for" with §4 "work email, company" | Addresses the reader as the contracting party; in employer-provisioned B2B seats that basis is unavailable. | Confirm who signs up; if seats are employer-provisioned, re-base and re-address. | Confirmed |
| Major | §6 line 21, "cloud hosting, email delivery, payment processing" | No international-transfer disclosure or safeguard, though §7 cites "the jurisdictions where we operate". | Name the regions and the transfer mechanism, or point to the section that does. | Corrected |
| Major | §6 line 21, "We share personal data with service providers who process it on our behalf" | Reads as exhaustive; omits legally compelled disclosure and transfer on merger or acquisition. | Add both categories as separate paragraphs. | Confirmed |
| Major | §6 line 23, "This data is aggregated and cannot identify you" | Absolute re-identification claim with no method or threshold; small B2B accounts are attributable. | State the aggregation method and minimum threshold; drop the absolute. | Confirmed |
| Major | §6 line 25, "We do not sell personal data." | Unqualified public representation that omits the separate US "share" concept. | Scope it to the statutory definitions and verify it against the analytics and partner arrangements. | Corrected |
| Major | §7 line 29 applied to §4 "content you upload" | Commits publicly to deleting customer content in 30 days with no export window or contract reference. | Reconcile against the customer agreement and DPA; state the export window. | Confirmed |
| Major | §5 line 16, "Product analytics and improvement \| Legitimate interests" | If analytics stores or reads data on the user's device, EU/UK e-privacy rules require consent for that step. | Confirm the mechanism; if device storage is used, move to consent. | Unverified |
| Minor | §4 line 5, "billing details processed by our payment provider" | Implies Northwind does not hold billing data; §7 says it keeps invoices and attached account details seven years. | Say the provider handles card data and Northwind retains invoices. | Confirmed |

---

## 4. Council roster

The requester specified this roster; disclosed as a fact, not treated as a limit on what each seat could report. Each seat was given the full roster and told that another seat owning a topic is not a reason to skip something it can see.

1. **Purpose & audience fit** — owns whether a reader can actually answer "what happens to my data", and who that reader is.
2. **Accuracy & internal consistency** — owns contradictions between sections and claims that are wrong on the artifact's own terms.
3. **Risk red-team** — owns legal, compliance, commercial and downstream exposure if this ships as written.

**Deliberately not covered.** *Operational feasibility* — no seat checked whether Northwind's systems can perform 30-day deletion across subprocessors or expire backups on schedule; a critical defect could live there, and the verdict does not cover it. *US state-privacy specifics beyond the "sell/share" point* — sensitive-data and consumer-health regimes were not assessed; a critical defect could live there. *Plain-language and translation obligations* — a defect there would be minor. Had the roster been mine, I would have added an operational/data-engineering seat; I did not, and the confidence note is capped accordingly.

---

## 5. Individual analyses

### Seat 1 — Purpose & audience fit

**Role & remit.** Judges whether sections 4–7 let their intended reader — an individual whose data Northwind holds — learn what is kept, why, and for how long, without needing a lawyer.

**Standard applied.** A transparency notice fails on audience fit when a reader following its plain text reaches a conclusion the same document later reverses. Source: the notice's own purpose, stated by its structure (each heading is a reader question).

**Assessment.** Clearly organised and written in ordinary language; the headings are the right four questions. It fails on the one section where a reader is most likely to act on what they read.

**Strengths.** §7 line 33 — "Data deleted from production remains in backups until the backup containing it expires" — is unusually candid; most notices omit the backup lag entirely. §4 line 7 enumerates "operating system version, crash traces, and a hashed device identifier" instead of hiding behind "device information".

**Weaknesses, risks & errors.**
- **Major, defect** — the notice addresses the reader as the person who bought the product: §5 line 13, "Providing the service you signed up for", alongside §4 line 5, "account details you give us (name, work email, company)". A work email and a company name point to seats provisioned by an employer, in which case the reader never signed up and never contracted. The document would then be speaking to the wrong person throughout.
- **Major, defect** — §6 line 23, "This data is aggregated and cannot identify you", asks the reader to accept an absolute claim with nothing behind it. There is no aggregation threshold and no way for the reader to test it.
- (The §7 retention contradiction is raised here first and consolidated in the Executive.)

**Gaps.** A reader who uploaded work product cannot learn from §7 whether they can retrieve it before the 30-day clock runs, or how.

**Strongest reason this might be fundamentally wrong.** If Northwind's users are employees provisioned by a corporate customer rather than self-serve signups, this is not a document needing edits — the addressee, the contract basis in §5 and the consent framing for marketing all attach to the wrong party, and sections 4–7 need restructuring around a controller/processor split.

**Domain verdict.** Below the bar. The prose is competent; the document misdirects the reader at the exact point it matters most.

**Recommended fixes.** Qualify the 30-day sentence. Add an export window for uploaded content. Replace the absolute aggregation claim with a stated method. Confirm who the reader is before anything else.

### Seat 2 — Accuracy & internal consistency

**Role & remit.** Judges whether the claims are correct on the artifact's own terms and whether sections contradict each other or their own stated constraints.

**Standard applied.** A statement fails if another statement in the same document makes it false. This needs no external authority — only both sentences. Source: internal consistency, the artifact's own text.

**Assessment.** One outright self-contradiction, one structural omission in the §5 table, one reconcilable but misleading pairing. The rest of the document is internally sound.

**Strengths.** §5 correctly separates purpose from basis and puts marketing on consent (line 17) rather than stretching legitimate interests to cover it. §6 line 21 — "Each is bound by a written processing agreement" — uses the correct processor framing.

**Weaknesses, risks & errors.**
- **Critical, defect** — §7 line 29 states "We delete personal data within **30 days** of account closure. This applies to all categories described in section 4." The following three paragraphs contradict it: financial records including "the account details attached to them" for seven years (line 31), backups on a 90-day cycle so real deletion runs to roughly 120 days (line 33), and security and audit logs "including IP addresses" for 18 months (line 35). IP address and account details are both §4 categories, so "all categories" is false as written on three counts.
- **Major, defect** — the §5 table (lines 11–17) lists only contract, legitimate interests and consent. §7 line 31 commits to seven-year retention "as required by tax law in the jurisdictions where we operate", which is a legal-obligation purpose with no row in the table. §5 therefore does not account for processing §7 promises.
- **Minor, defect** — §4 line 5 says "billing details processed by our payment provider", implying Northwind does not hold them; §7 line 31 says Northwind retains invoices and attached account details for seven years. Reconcilable (card data at the provider, invoices at Northwind) but not as drafted.

**Gaps.** No criteria are given for how any retention period was chosen, so none of the four can be checked for proportionality.

**Strongest reason this might be fundamentally wrong.** No foundational failure found. The strongest candidate is the §7 contradiction, which is critical for the retention statement but not fundamental, because the document's structure and its other sections hold and the fix is one deleted sentence plus a qualifier.

**Domain verdict.** Fails on accuracy in §7 and on completeness in §5; sound elsewhere.

**Recommended fixes.** Rewrite §7's opening as a default with named exceptions. Add the legal-obligation row to §5. Split the §4 billing sentence.

### Seat 3 — Risk red-team

**Role & remit.** Judges what Northwind is exposed to if this text is published unchanged — regulatory, contractual and commercial.

**Standard applied.** A published privacy notice is an enforceable public representation; the exposure is the distance between what it states and what the company can prove it does. Source: stated as this seat's professional judgment, not a cited rule.

**Assessment.** The exposure is concentrated in §6, where the notice makes two categorical claims it does not support and omits three disclosure categories that regulators and acquirers both look for.

**Weaknesses, risks & errors.**
- **Major, defect** — §6 line 21 lists processor categories but discloses no international transfer or safeguard, while §7 line 31 establishes multi-jurisdiction operation. Cloud hosting and email delivery almost always cross borders.
- **Major, defect** — §6 line 21 reads as the complete list of recipients. It omits disclosure compelled by law and transfer of the database in a merger or acquisition. Publishing an apparently exhaustive list and then doing either is the harder position to defend.
- **Major, defect** — §6 line 25, "We do not sell personal data.", is a categorical representation with no scoping. US state law treats "sell" broadly and treats "share" for cross-context advertising as a separate concept the sentence does not address.
- **Major, defect** — §7 line 29 commits publicly to deleting §4's "content you upload" within 30 days of account closure, with no export window and no reference to the customer agreement. Whether this conflicts with Northwind's MSA or DPA cannot be determined from the artifact and requires an actual check against those documents.
- **Major, defect, `[unverified — recall, not lookup]`** — §5 line 16 bases "Product analytics and improvement" on legitimate interests. Where analytics is delivered by storing or reading information on the user's own device, EU/UK e-privacy rules require consent for that step regardless of the Article 6 basis chosen. Whether that applies here depends on the analytics mechanism, which the artifact does not state.

**Gaps.** No named period or criterion for the diagnostic data in §4 line 7 beyond the contradicted 30-day default.

**Strongest reason this might be fundamentally wrong.** The real exposure may not be anything missing from the text but the gap between the text and operations: 30-day deletion across every subprocessor, an 18-month log ceiling actually enforced, backups that genuinely expire. If those cannot be evidenced, every precise number here becomes a representation Northwind cannot meet, and tightening the drafting makes that worse rather than better.

**Domain verdict.** Not safe to publish as drafted. The defects are localised and fixable; none require abandoning the document.

**Recommended fixes.** Add transfers, compelled disclosure and business-transfer paragraphs to §6. Scope the no-sale sentence. Check §7 against the MSA and DPA. Confirm the analytics mechanism before keeping legitimate interests in §5.

---

## 6. Executive review

The executive re-read the artifact in full before reading any seat output.

**Points of agreement.** Two, both marked **sole-source** per non-negotiable 3, because the sequential fallback means concurrence here is not independent evidence.

- *The §7 retention contradiction* (Seats 1 and 2). Stated once here and cut from Seat 1's section. The anchor was checked personally: the string "This applies to all categories described in section 4" appears at line 29; "seven years" at line 31; "90-day schedule" at line 33; "**18 months**" at line 35. Upheld at critical.
- *The absolute aggregation claim in §6* (Seats 1 and 3). Anchor "This data is aggregated and cannot identify you" found at line 23. Upheld at major.

The assumption both agreements rest on is that §7's "all categories" refers to §4's enumerated list. The artifact establishes this itself — the sentence names section 4 explicitly — so the agreement survives the test in non-negotiable 3.

**Points of conflict & adjudication.**
- *Severity of the aggregation claim.* Seat 1 framed it as a reader-comprehension problem, Seat 3 as a misrepresentation. Ruling: major, on Seat 3's framing. Seat 1's version understates it; the sentence is a factual assertion about re-identifiability, not a clarity choice.
- *The transfers gap.* Seat 3 reported it as an omission from the notice. Ruling: narrowed. §6 is where transfers would normally sit and they are absent there, but sections 1–3 and 8+ were not supplied. Held at major, marked excerpt-bounded — not raised to critical, which would require knowing the whole notice.
- *The no-sale sentence.* Seat 3's original draft asserted the §6 partner sharing contradicts it. Rejected on evidence: line 23 states the shared statistics are aggregated and non-identifying, so on the artifact's own terms no personal data is involved and the sentence is not contradicted. Narrowed to the unqualified drafting and the omitted "share" concept, which stand.
- *Seat 1's audience finding.* Raised only by the seat that owns audience fit; no contrary evidence in the artifact overrules it, and silence from the other two is not disagreement. Upheld at major, conditional on Northwind's signup model.

**Verification result.** Two findings withdrawn, two narrowed. Withdrawn: (a) Seat 2's claim that §5 gives no legal basis for the §4 diagnostic data — §5 is keyed to purposes, not data categories, and "Providing the service you signed up for" and "Security monitoring and fraud prevention" plausibly cover crash traces and the hashed identifier; the finding rested on a requirement the artifact never took on. (b) Seat 1's claim that the notice never tells the reader they can object to legitimate-interests processing — that belongs to a rights section outside sections 4–7 and cannot be confirmed absent. Narrowed: the transfers finding and the no-sale finding, as adjudicated above. No seat's reliability is in question; both withdrawals were scope errors, not misreadings of text.

**Panel blind spots.** All three seats assumed a GDPR-style regime because §5 borrows Article 6 vocabulary. If Northwind operates only in the US and that vocabulary is inherited from a template, the §5 findings soften considerably and the §6 US-law finding becomes the dominant one. No seat examined operational feasibility — whether deletion, backup expiry and log ceilings can actually be performed — and a critical defect could live there; Seat 3 named the risk but could not test it. No seat examined the sections not supplied. Being one context, the seats likely share what they failed to look at, so treat this coverage list as incomplete rather than exhaustive.

**Overall judgment.** Competent, well-organised drafting with better-than-average candor on backups, undermined by one false statement in §7 and by §6 omitting the disclosures a notice of this kind is expected to carry. This is a document to fix, not to restart: every finding is localised, and none of them touches the structure.

**Decision on further action.** **Revise substantially before use.**

**Prioritized next steps.**
1. Rewrite §7's opening (line 29) as a default subject to the exceptions that follow; delete "This applies to all categories described in section 4".
2. Confirm the signup model. If seats are employer-provisioned, re-base §5 line 13 and re-address the document before any other edit.
3. Add to §6: international transfers and safeguard, legally compelled disclosure, business-transfer sharing.
4. Add the legal-obligation row to §5; qualify the aggregation and no-sale sentences in §6.
5. Check §7's 30-day content deletion against the MSA and DPA, and confirm the analytics mechanism behind §5 line 16.

**Confidence & what would change the verdict.** Of the nine findings at critical or major, I expect six to survive an independent expert re-check. First to fall: the analytics/e-privacy finding, which is conditional on a mechanism the artifact never states and is labelled unverified; then the transfers finding, if a transfers section exists at section 8; then the audience-fit finding, if Northwind is genuinely self-serve. The verdict does not rest on any of those three — it rests on the §7 contradiction, which is verified text against verified text and needs no external information. What would flip it: supply of the full notice showing transfers and rights disclosures already present, plus a qualifier on line 29, would move this to *approve with minor revisions*. Evidence that Northwind cannot operationally meet the stated periods would move it to *reject and rework*, and that is the one input this council could not obtain.
