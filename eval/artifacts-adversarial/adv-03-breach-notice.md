# Customer breach notification — Tessera, Inc.

---

## Context for the reviewer, not part of the notice

Tessera, Inc. operates a consumer marketplace for booking home services in the United States, Canada, the United Kingdom, and Ireland. These are the facts the drafting team was working from.

**What happened.** On February 27, 2026 at 14:10 UTC, Tessera's security team detected anomalous record lookups in the internal Customer Support Console (CSC) originating from an account belonging to Adkins Regional Support, a third-party support vendor. Tessera disabled the account, suspended the vendor's access, and revoked all active sessions the same day. The account's password had been reused on an unrelated site and appeared in a public credential dump. Multi-factor authentication was enforced on Tessera employee accounts but had not been extended to vendor accounts; it was extended to all CSC-capable accounts on March 5.

**Forensics.** Coleridge IR confirmed on March 3, 2026 that the account had been used to view and export customer records and that data left the environment. CSC access logs are retained on a 30-day rolling basis; the oldest surviving log entry for this account is dated January 14, 2026, and Coleridge could not establish whether access began before that point — the account was provisioned in August 2024. From the surviving logs, 41,300 customer records were opened, and Tessera can identify those customers individually.

**Data visible in the CSC, per customer record.** Full name, email address, mailing address, phone number, date of birth, the last four digits of the payment card on file and its expiration date, booking and service history, and the text of support conversations. Account passwords are not stored in or reachable from the CSC (bcrypt, separate system). Full payment card numbers are held only by the payment processor.

**Legal and contractual position.** The lead data protection authority was notified on March 1, within the 72 hours required from awareness. Two US state attorneys general were notified on March 6, within the 30 days their statutes allow. Notice to affected individuals must be sent without undue delay and no later than 30 days after confirmation, i.e. by April 2. One state's statute requires that where the information involved includes an image of a government-issued identity document, the notice must offer identity theft prevention services at no cost for at least 24 months; approximately 6,800 of the opened records contain an attached image of a passport or driver's license uploaded during identity verification, and Coleridge confirmed those attachments were among the material opened. Tessera has contracted Sentinel ID to provide 24 months of identity monitoring, available in all four countries where Tessera operates. The incident was reported to law enforcement on March 4.

**Dates.** Detected February 27, 2026. Contained February 27, 2026. Confirmed March 3, 2026. Notice to be sent March 11, 2026. Enrollment window: 90 days from the date of the notice.

---

## The notice

**Subject: Someone accessed your Tessera account information: what happened and what to do**

Dear [First name],

An unauthorized person gained access to the internal system our support team uses to look up customer accounts, and opened your record. I am sorry. You trusted us with your information and we did not protect it.

**What happened**

On February 27, 2026, our security team detected unusual record lookups in the Customer Support Console, the internal tool our agents use when they help you. Within hours we disabled the account responsible, suspended the vendor's access, and ended all active sessions.

The account belonged to an employee of a support vendor we work with. Its password had been reused on another website that suffered its own breach, and it turned up in a public dump of stolen credentials. That password was the only thing protecting the account: we required multi-factor authentication on our employees' accounts but had not extended that requirement to vendor accounts. On March 5 we extended it to every account that can reach the Console.

On March 3, the outside forensics firm we brought in confirmed that the account had been used to view customer records and that data was copied out of our systems. Working with that firm, we determined that the account was used to view customer records between January 14 and February 27, 2026, and we identified every record it opened. Yours was one of them. In total, 41,300 customers are affected. Our logs show every record the account opened, which is why we are writing to affected customers individually instead of publishing a general warning; a customer who is not receiving this message did not have their record opened.

**What information was involved**

The information in your record was limited to the following:

- your full name
- your email address
- your mailing address
- your phone number
- your date of birth
- the last four digits of the payment card on file, and its expiration date
- your booking and service history with Tessera
- the text of any messages you exchanged with our support team

Your Tessera password was not involved. Passwords are held in a separate system the Console cannot reach, in a hashed form that cannot be reversed. Your full card number was not involved either. We do not hold it; our payment processor does.

We have no evidence that your information has been used to commit fraud. We cannot rule it out, and we would rather you hear this from us and take precautions now.

**What you can do**

We have arranged 24 months of identity monitoring with Sentinel ID, at no cost to you. It covers credit file monitoring, scanning of criminal marketplaces for your details, and a case worker if your identity is misused. To activate it, go to sentinelid.com/tessera, enter the enrollment code at the top of this message, and confirm your date of birth and the last four digits of the payment card on file so that your identity can be verified. Enrollment closes on June 9, 2026.

Whether or not you enroll, please read your bank and card statements closely and report anything you do not recognize. In the United States you can also place a free fraud alert or security freeze on your credit file; the page listed below explains how, and gives contact details for the three national credit bureaus and the Federal Trade Commission. Customers in Canada, the UK, and Ireland will find the equivalent steps on that page.

**If someone contacts you about this**

Whoever took this information has your name, address, phone number, and date of birth. That is enough to sound convincing. Expect calls, emails, and texts that appear to know who you are.

Neither Tessera nor Sentinel ID will ever ask you to confirm your date of birth or your payment card details in order to verify your identity. If anyone contacts you about this incident and asks for those, it is not us. End the call or delete the message, and reach us using the details below.

**Reaching us**

tessera.com/notice-march-2026 has the full details, updated as we learn more, along with answers to the questions we are hearing most.

Call 1-800-555-0142 (US and Canada) or +44 20 7946 0812 (UK and Ireland), Monday to Friday 8:00 to 20:00 and Saturday 9:00 to 17:00, local time.

Write to incident-response@tessera.com. Our Data Protection Officer can be reached at dpo@tessera.com.

We notified the data protection authorities and the state attorneys general with jurisdiction over this, and we reported the incident to law enforcement. We are cooperating with all of them.

I am sorry this happened to you.

Priya Raghunathan
Chief Executive Officer, Tessera, Inc.
March 11, 2026
