# Ground truth — adv-03-breach-notice.md

Artifact: `artifacts-adversarial/adv-03-breach-notice.md`
Three planted defects. Everything else in the notice is intended to be sound.

---

## Defect 1 — The access window is presented as a finding when it is only a log-retention horizon

- **Severity**: critical

- **Location**: "What happened" section, final paragraph — the sentences beginning "Working with that firm, we determined that the account was used to view customer records between January 14 and February 27, 2026, and we identified every record it opened", "In total, 41,300 customers are affected", and "a customer who is not receiving this message did not have their record opened."

- **The defect**: The notice states as a determined investigative conclusion that the intrusion ran from January 14 to February 27, that every accessed record has been identified, that the affected population is exactly 41,300, and — the operative claim — that anyone who does not receive the letter was not affected. None of these are supportable. January 14 is simply the oldest surviving log entry, not a determined start date, and the forensics firm expressly could not establish whether access began earlier. Any of the four claims flagged by a reviewer matches this defect.

- **Why it is real**: The context block's Forensics paragraph states that CSC access logs are retained on a 30-day rolling basis, that the oldest surviving log entry for this account is January 14, 2026, that Coleridge IR "could not establish whether access began before that point," and that the account was provisioned in August 2024 — leaving roughly seventeen months of possible access that no log can speak to. The 41,300 figure is explicitly derived "from the surviving logs." The notice converts an evidentiary blind spot into an affirmative all-clear. Concretely: customers whose records were opened only before January 14 receive no notice at all, and the notice tells them, in terms, that this silence means they were not affected. The sender's exposure is equally concrete — this is a false statement of fact in a statutory notice filed with regulators and two state attorneys general, and it under-notifies an unknown number of affected individuals. The defensible drafting is the one every competent IR report uses: access was observed from January 14, earlier access cannot be excluded because logs do not extend further back.

- **Why I expect a reviewer to miss it**: Date-checking is a reflex, and this passes the reflex — both January 14 and February 27 appear verbatim in the context block, so the reviewer ticks "dates consistent with the facts" and moves on without asking what kind of fact January 14 is. The retention detail sits mid-paragraph in a bullet the reviewer reads for the confirmation date, and the words "determined", "every record", and "our logs show" read as the language of a thorough investigation rather than an overreach.

---

## Defect 2 — The exhaustive list of exposed data omits the government-issued ID images

- **Severity**: major

- **Location**: "What information was involved" section — the sentence "The information in your record was limited to the following:" and the eight-item bulleted list that follows.

- **The defect**: Approximately 6,800 of the opened records contain an attached image of a passport or driver's license. The list does not mention identity document images, and no other part of the notice mentions them either. Because the list is introduced with "limited to", this is not merely an incomplete enumeration but an affirmatively false statement about the scope of the exposure. The bullet "the text of any messages you exchanged with our support team" does not cover it: "the text of" excludes attachments, and "limited to" forecloses anything not listed.

- **Why it is real**: The context block's Legal and contractual position paragraph states that approximately 6,800 of the opened records contain an attached image of a passport or driver's license uploaded during identity verification, and that Coleridge confirmed those attachments were among the material opened. A stolen identity document image supports a materially different and more severe class of harm than the listed elements — document-based impersonation, account opening at institutions that accept a document image as proof, and fraudulent replacement applications — and the response to it is different too: the affected customer needs to consider replacing the document and notifying the issuing authority. None of that is prompted by a notice that does not disclose the exposure. There is a second tell inside the artifact: the notice offers exactly 24 months of monitoring, and the context block states that the 24-month floor is triggered by the presence of identity document images. The remedy is calibrated to an exposure the notice never discloses.

- **Why I expect a reviewer to miss it**: The ID-document fact is deliberately not in the context block's data-elements paragraph, where a reviewer diffing lists would look for it. It appears only inside the regulatory paragraph, framed as the trigger for the 24-month monitoring requirement — so the reviewer resolves it as a compliance question ("24 months required, 24 months offered, satisfied"), banks it, and never carries it back to the data list. The notice's own list is long, specific, and correct on all eight items it does contain, which is exactly what makes it read as complete.

---

## Defect 3 — The enrollment step asks for the two identifiers the notice promises will never be asked for

- **Severity**: major

- **Location**: "What you can do" section (enrollment instructions) contradicted by "If someone contacts you about this" section (the anti-fraud warning), roughly 300 words apart.

- **The defect**: The enrollment instruction directs the customer to "confirm your date of birth and the last four digits of the payment card on file so that your identity can be verified." The later warning states: "Neither Tessera nor Sentinel ID will ever ask you to confirm your date of birth or your payment card details in order to verify your identity. If anyone contacts you about this incident and asks for those, it is not us." The notice does the exact thing it tells the reader is proof of fraud, and it does so in connection with this incident, by both named parties, for the stated purpose of verifying identity. On the reader's own instructions, the notice fails its own authenticity test.

- **Why it is real**: Two independent grounds, both from the artifact alone. First, the flat contradiction: the warning is unconditional, names both Tessera and Sentinel ID, and is scoped to identity verification in connection with this incident, so there is no channel-based or party-based escape. Whichever sentence is correct, the other must be struck. Second, the substance: the notice's own data list states that date of birth and the last four digits of the payment card were both exposed. Using the stolen data as the identity check for the remedy for its theft provides no assurance against an attacker holding the same fields, and it conditions 41,300 people who have just been told to expect convincing approaches to hand over those precise fields on request. The correct fix is an enrollment code that is sufficient on its own, or a verification factor that was not exposed.

- **Why I expect a reviewer to miss it**: Both sentences are individually exemplary and are read that way — the enrollment step scans as ordinary activation boilerplate on the way to checking the deadline arithmetic, and the warning scans as unusually thorough anti-phishing guidance, the kind of line a reviewer notes approvingly as evidence the notice was well done. Catching it requires holding two separated passages in mind at once and noticing that the praiseworthy one indicts the routine one.

---

## Notes for the grader

- Defects 1 and 2 both bear on completeness of disclosure but are separable and should be scored separately: defect 1 is temporal (the window and the population), defect 2 is categorical (a missing data element). A reviewer who says only "the notice overstates what is known" without reaching the ID images has found 1, not 2.
- The rest of the notice is deliberately sound and should not generate findings: it leads with the incident, apologizes without hedging, names the cause and the company's own MFA gap without shifting blame to the vendor, states plainly what was not affected (passwords, full card numbers) and why, qualifies "no evidence of misuse" rather than asserting safety, gives typed URLs rather than links, supplies phone, email, web, DPO contact and hours across all operating regions, covers US fraud alerts and security freezes, and reports regulator, AG, and law enforcement notification. All dates and arithmetic are correct: notified the DPA March 1 (within 72 hours of February 27, 14:10 UTC), AGs March 6 (within 30 days), individual notice March 11 (within 30 days of the March 3 confirmation, deadline April 2), enrollment closing June 9, 2026 (90 days after March 11, 2026). The 24-month monitoring offer meets the stated statutory floor and is available in all four operating countries.
