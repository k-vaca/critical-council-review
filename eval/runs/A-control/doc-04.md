# Expert review — doc-04-privacy-notice.md (Sections 4–7, draft for legal review)

Reviewed as a data-protection / privacy counsel would review a client draft, against
GDPR Arts. 5, 6, 13–14 and 28, the ePrivacy Directive Art. 5(3), and CCPA/CPRA.
Judged against a competent professional draft, not perfection.

## What is sound

- Section 4 is a serviceable inventory: it separates volunteered data, observed usage data,
  uploaded content, and billing, and it discloses desktop-client telemetry — which many
  notices quietly omit.
- Section 5's contract basis for service delivery and billing, and consent for cross-product
  marketing, are conventional and defensible mappings.
- Section 6 correctly states that processors are bound by written processing agreements
  (Art. 28), and uses recipient *categories*, which is permitted.
- Section 7 discloses that deleted production data persists in backups. This is honest and
  frequently omitted; the defect below is that it is not reconciled with the 30-day promise,
  not that it was disclosed.

The document is not sound overall. Section 7 contains a flat self-contradiction on its face,
and Sections 5 and 6 omit content that Art. 13 makes mandatory and that belongs in these
specific sections rather than elsewhere in the notice.

---

## Critical

### C1 — Section 7, line 29: the blanket deletion promise is contradicted two lines later

**Anchor:** "We delete personal data within **30 days** of account closure. This applies to all categories described in section 4."

**Problem:** Lines 31 and 35 then retain two section-4 categories far longer — billing details
for seven years and IP addresses for eighteen months — so the "all categories" sentence is
false on the face of the document and anyone implementing or relying on it deletes the wrong
data or makes a false public commitment.

Note the contradiction is textual, not merely arguable: "IP address" is named in section 4
(line 5) and named again in the 18-month log retention (line 35); "billing details" is named
in section 4 (line 5) and swept into the seven-year financial-records rule (line 31). The fix
is to make line 29 the default rule and state the carve-outs as express exceptions.

---

## Major

### M1 — Section 7, line 33: backup persistence is not reconciled with the 30-day commitment

**Anchor:** "Backups are cycled on a 90-day schedule. Data deleted from production remains in backups until the backup containing it expires."

**Problem:** Personal data can survive up to roughly 90 days after the promised 30-day
deletion, and the draft never qualifies line 29 accordingly nor commits to re-deleting
restored data, so the stated deletion window is unachievable as written.

### M2 — Section 7 line 31 vs. Section 5 table: seven-year retention has no legal basis in the table

**Anchor:** "retained for **seven years** from the date of the transaction, as required by tax law in the jurisdictions where we operate"

**Problem:** Retention compelled by tax law rests on Art. 6(1)(c) legal obligation, but the
section 5 table lists only contract, legitimate interests and consent — so the notice claims a
processing purpose it has not given a lawful basis for.

### M3 — Section 7, line 31: a single seven-year figure is asserted for all jurisdictions

**Anchor:** "as required by tax law in the jurisdictions where we operate"

**Problem:** Statutory retention for accounting records is not seven years everywhere —
several EU jurisdictions require ten — so a single unverified number stated as a legal
conclusion, without naming the jurisdictions, will need per-jurisdiction rework and may leave
records destroyed before the law permits.

### M4 — Section 7, line 29: the deletion trigger only works for account holders

**Anchor:** "within **30 days** of account closure"

**Problem:** Account closure is the sole trigger, but desktop-client diagnostic data keyed to a
hashed device identifier, and marketing suppression/consent records that must outlive an
account to honour unsubscribes and evidence consent under Art. 7(1), have no account-closure
event — so those categories have no stated retention rule at all.

### M5 — Section 5, lines 15–16: legitimate interests relied on but never identified

**Anchor:** "| Security monitoring and fraud prevention | Legitimate interests | | Product analytics and improvement | Legitimate interests |"

**Problem:** Art. 13(1)(d) expressly requires the notice to state *which* legitimate interests
are pursued where that basis is used; the table names the purpose but never the interest, so
the mandatory disclosure is missing for three of five processing purposes.

### M6 — Section 5, line 16: product analytics on the desktop client is unlikely to survive on legitimate interests

**Anchor:** "| Product analytics and improvement | Legitimate interests |"

**Problem:** The analytics feed includes desktop-client telemetry and a hashed device
identifier (line 7), i.e. storing and accessing information on the user's terminal equipment,
which ePrivacy Art. 5(3) requires consent for unless strictly necessary to the requested
service — analytics is not.

### M7 — Section 6: no international transfer disclosure anywhere in the sharing section

**Anchor:** "cloud hosting, email delivery, payment processing, customer support tooling, and analytics"

**Problem:** Art. 13(1)(f) requires disclosure of transfers to third countries, the transfer
mechanism relied on, and how to obtain a copy of the safeguards; the section that identifies
recipients says nothing about where those recipients are, which for hosting and analytics is
almost never purely domestic.

### M8 — Section 6, line 23: unqualified anonymity claim for the partner data feed

**Anchor:** "We also share aggregated usage statistics with selected partners... This data is aggregated and cannot identify you."

**Problem:** Aggregation alone does not make data anonymous under GDPR Recital 26, and the
draft gives no aggregation threshold, no de-identification standard, no contractual
re-identification ban, and does not identify the "selected partners" even by category — so an
absolute "cannot identify you" is an unsupported guarantee.

### M9 — Section 6, line 25: the no-sale statement is unqualified and untested against CCPA/CPRA

**Anchor:** "We do not sell personal data."

**Problem:** CCPA/CPRA define "sell" and "share" broadly enough to capture disclosures for
cross-context behavioural advertising and some analytics arrangements, and the draft neither
addresses "sharing" nor mentions an opt-out — an unqualified no-sale claim is the exact fact
pattern California has enforced against.

### M10 — Section 6: two standard recipient categories are missing

**Anchor:** "We share personal data with service providers who process it on our behalf"

**Problem:** The section omits disclosures compelled by law or legal process (courts,
regulators, law enforcement) and disclosures in a merger, acquisition or insolvency, both of
which are recipient categories Art. 13(1)(e) requires and both of which will occur despite the
notice's silence.

---

## Minor

### m1 — Section 7, line 31: "account details" is undefined and conflicts with Section 4

**Anchor:** "Financial records, including invoices and the account details attached to them"

**Problem:** "Account details" could mean bank/card details or user account records, and
section 4 implies the payment provider holds billing details, leaving it unclear what
Northwind itself retains for seven years.

### m2 — Section 7, line 33: the backup schedule is ambiguous

**Anchor:** "Backups are cycled on a 90-day schedule."

**Problem:** "Cycled on a 90-day schedule" does not state whether 90 days is the rotation
interval or the maximum lifetime of any backup, so no outer bound on residual retention is
actually given.

### m3 — Section 7, line 35: eighteen months for security logs carries no justification

**Anchor:** "Security and audit logs, including IP addresses and authentication events, are retained for **18 months**."

**Problem:** Storage limitation under Art. 5(1)(e) requires proportionality, and 18 months
exceeds the 6–12 months several supervisory authorities treat as the norm for security
logging, so the period should carry a stated rationale.

### m4 — Section 5: no reference to the right to object or to withdraw consent

**Anchor:** "| Marketing emails about other Northwind products | Consent |"

**Problem:** Art. 13(2)(c) requires the withdrawal right to be stated where consent is the
basis and Art. 21(4) requires the objection right to be presented explicitly and separately
where legitimate interests are used; neither appears here, though both may sit in a section
outside this excerpt.

### m5 — Section 4: the sources of the data are never stated

**Anchor:** "When you use Northwind we collect: account details you give us (name, work email, company)"

**Problem:** The section describes only data obtained from the user and the product, and never
says whether any personal data arrives from third parties such as SSO providers, resellers or
enrichment vendors, leaving Art. 14 coverage unresolved.

---

## Totals

critical = 1, major = 10, minor = 5
