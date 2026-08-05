# Review — adv-03-breach-notice.md (Tessera customer breach notification)

Single expert pass. Findings ordered by severity. "Facts" refers to the reviewer-context block above the notice; the notice is judged against those facts and against what a competent breach-notification drafter should produce.

---

## Critical

### C1 — Exposure window stated as an established fact when forensics could not establish it

**Location:** "What happened", third paragraph.

**Anchor:** "we determined that the account was used to view customer records between January 14 and February 27, 2026, and we identified every record it opened"

**Problem:** January 14 is only the oldest *surviving* log entry under a 30-day rolling retention policy — Coleridge expressly could not establish whether access began earlier, and the account was provisioned in August 2024 — so the notice converts a log-retention boundary into a factual start date.

**Why it matters:** A recipient reading this concludes the intrusion lasted six weeks. The true unbounded window is up to eighteen months. That changes what a recipient does — how far back they review statements, whether they treat a 2024 or 2025 fraud incident as related, and how seriously they weigh the disclosure. Regulators treat a stated-as-known window that is actually unknown as a material misstatement in the notice itself, not merely an omission.

**Fix:** State the confirmed window and the uncertainty explicitly, e.g. "Our access logs are kept for 30 days. They show activity from January 14 to February 27, 2026. Because of that retention limit, our forensics firm could not determine whether access began earlier; the account has existed since August 2024, and we cannot rule out earlier access."

---

### C2 — Notice affirmatively tells non-recipients they were not affected, which the evidence cannot support

**Location:** "What happened", third paragraph, final sentence (and the "41,300 customers are affected" claim in the same paragraph).

**Anchor:** "a customer who is not receiving this message did not have their record opened"

**Problem:** The 41,300 figure and the individual identification derive solely from the surviving 30 days of logs, so anyone whose record was opened before January 14 is both unidentified and, by this sentence, actively told they are safe.

**Why it matters:** This is the most damaging line in the document. It is a false negative assurance issued to an unknown but potentially large population, published in a letter that will be quoted verbatim in press coverage and on the incident page. It suppresses protective action by exactly the people who cannot be reached individually. Three claims in one paragraph rest on the same error — "we identified every record it opened", "In total, 41,300 customers are affected", and the non-recipient assurance — and all three must go.

**Fix:** Delete the assurance. Frame the count as "at least 41,300 customers whose records we can confirm were opened", and pair the individual notices with a public notice explaining that customers not individually contacted may still have been affected in periods no longer covered by logs.

---

### C3 — "Limited to the following" omits the government-issued ID images for roughly 6,800 recipients

**Location:** "What information was involved", opening line and bullet list.

**Anchor:** "The information in your record was limited to the following:"

**Problem:** Coleridge confirmed that passport and driver's licence images attached to approximately 6,800 of the opened records were among the material accessed, yet the list omits them entirely while the framing word "limited" makes the omission an affirmative false statement to those recipients.

**Why it matters:** A scanned passport or licence is categorically more damaging than the rest of the list combined — it supports account takeover at institutions that accept document images, new-account fraud, and document forgery, and it cannot be changed the way a card number can. Telling 6,800 people their exposure was "limited to" name, email and last-four is the difference between them replacing a document and doing nothing. It is also the exact data element that triggers the state statute cited in the facts, so the omission is simultaneously a consumer-harm problem and a compliance problem.

**Fix:** Produce a second variant of the notice for the ~6,800 affected records that adds the ID image to the list, or add a conditional block. Do not send a single template that says "limited to" across a population with materially different exposure.

---

### C4 — The anti-phishing rule directly contradicts the enrollment instructions

**Location:** "If someone contacts you about this", second paragraph, versus "What you can do", first paragraph.

**Anchor:** "Neither Tessera nor Sentinel ID will ever ask you to confirm your date of birth or your payment card details"

**Problem:** Sentinel ID enrollment, three paragraphs earlier, requires the recipient to confirm precisely their date of birth and the last four digits of the payment card, so the notice's own instructions are the first thing its fraud rule tells recipients to reject.

**Why it matters:** Every recipient who follows the document lands somewhere wrong. The cautious ones refuse to enroll and forgo the monitoring the company is legally required to offer to at least part of this population. The compliant ones learn that the "we will never ask" rule has exceptions, which is exactly the reasoning a competent social engineer needs. The support line will absorb the confusion either way. A contradiction of this kind between two operative instructions in the same letter is a defect regardless of which side is right.

**Fix:** Resolve by changing the enrollment flow (see M2), then make the rule absolute and specific: name the enrollment code as the only credential either party will ever request, and state that neither company will ever ask for date of birth, card details, or passwords by phone, email, or text.

---

## Major

### M1 — No remediation guidance for compromised identity documents

**Location:** "What you can do", both paragraphs.

**Anchor:** "please read your bank and card statements closely and report anything you do not recognize"

**Problem:** The advice addresses only financial-account monitoring and credit freezes, which does nothing for the ~6,800 recipients whose passport or driver's licence image was taken and who need document-specific steps.

**Why it matters:** Those recipients need materially different actions: reporting the document to the issuing authority, considering replacement, and — in the UK and Ireland — registering with a document-misuse protective registration service. A credit freeze does not stop someone presenting a copy of their passport. This is a distinct defect from C3: even if the data list were corrected, the remediation section would still be inadequate for that group, and someone rewriting the notice must add content, not just a bullet.

**Fix:** Add document-specific guidance to the variant notice, per jurisdiction (passport agency / DMV / DVLA / NDLS equivalents), and say plainly that the document image cannot be "reset" and warrants replacement.

---

### M2 — Enrollment verifies identity using the two data elements confirmed stolen

**Location:** "What you can do", first paragraph.

**Anchor:** "confirm your date of birth and the last four digits of the payment card on file so that your identity can be verified"

**Problem:** Date of birth and card last-four are both on the list of data the attacker exfiltrated, so they authenticate the attacker as readily as the customer.

**Why it matters:** Independent of the wording contradiction in C4, this is a broken control. Anyone holding the stolen dataset can enroll on a victim's behalf and thereby control the monitoring account, the alerts, and the case worker channel — a known pattern in post-breach fraud. Fixing C4 by editing the phishing paragraph would leave this intact, which is why it needs separate treatment: the enrollment flow itself has to change.

**Fix:** Verify with the per-recipient enrollment code alone, or code plus a separate out-of-band factor sent to the address of record. Remove date of birth and card data from the flow entirely.

---

### M3 — The enrollment code the notice depends on does not exist in the document

**Location:** "What you can do", first paragraph.

**Anchor:** "enter the enrollment code at the top of this message"

**Problem:** The letter is a merge template — it carries a `[First name]` field — but contains no enrollment-code field at the top or anywhere else, so as drafted the single action the notice asks recipients to take cannot be completed.

**Why it matters:** This blocks the remedy the company is contractually and, for the ID-document population, statutorily obliged to deliver. It also generates a predictable call spike to a support line staffed for a known volume. It reads as a production oversight rather than a judgement error, but it is load-bearing and would ship.

**Fix:** Add the merge field to the header block and verify it populates in the merge test before send.

---

## Minor

### mi1 — Statutory contact details deferred to a web page rather than included in the notice

**Location:** "What you can do", second paragraph.

**Anchor:** "the page listed below explains how, and gives contact details for the three national credit bureaus and the Federal Trade Commission"

**Problem:** Several US state breach-notification statutes require the credit-bureau and FTC contact information to appear in the notice itself, so pointing to a URL may fall short of the content requirement in the two states whose AGs were notified.

**Fix:** Inline the bureau names, phone numbers, and FTC identity-theft resource in the notice; keep the page as the supplement rather than the sole source.

---

### mi2 — "Local time" is ambiguous across four countries and multiple time zones

**Location:** "Reaching us", second paragraph.

**Anchor:** "Monday to Friday 8:00 to 20:00 and Saturday 9:00 to 17:00, local time."

**Problem:** Two phone numbers cover the US, Canada, the UK, and Ireland, spanning at least six time zones, and "local time" does not say whose.

**Fix:** State the zone per number (e.g. ET for the North American line, GMT/IST for the UK and Ireland line).

---

## Checked and sound

Recorded so a reader knows these were tested rather than skipped.

- **Enrollment close date.** March 11, 2026 plus 90 days is June 9, 2026. The stated date is correct.
- **Individual-notice deadline.** Confirmation March 3 plus 30 days is April 2. Sending March 11 is inside the window and consistent with "without undue delay".
- **Regulator timing.** Awareness February 27 at 14:10 UTC; DPA notified March 1, inside 72 hours. State AGs notified March 6, inside 30 days. Law enforcement March 4. All consistent with the facts.
- **Twenty-four-month service requirement.** The state statute triggered by the ID-document images requires an offer of at least 24 months at no cost; Sentinel ID provides 24 months in all four operating countries. The offer itself satisfies the requirement — the failure is disclosure (C3), not duration.
- **Password and card-number statements.** Both accurately reflect the facts: bcrypt hashes in a system the Console cannot reach, full PANs held only by the processor.
- **Containment and MFA remediation.** Same-day disablement, session revocation, and the March 5 extension of MFA to all Console-capable accounts are all stated accurately.
- **Exfiltration.** "Data was copied out of our systems" correctly reflects Coleridge's confirmation that data left the environment; the notice does not soften it to "may have been accessed".
- **Tone and ownership.** The apology, the named CEO signature, and the plain-language explanation of the MFA gap are appropriate and above the norm for this document type. Not a defect.

---

## Overall assessment

The prose, tone, and structure are strong — better than most notices of this kind. The defects are not stylistic; they are in the factual claims. Four of them are the same species of error: the drafters treated the boundaries of their evidence as the boundaries of the incident (C1, C2) and treated a heterogeneous affected population as homogeneous (C3, M1). Combined with the self-contradicting enrollment instructions (C4, M2) and a missing merge field (M3), the notice should not be sent in this form. C1, C2, C3, and C4 each require a change to what the notice asserts, not how it is phrased.
