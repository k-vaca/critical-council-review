# Review — doc-02-pricing-email.md

**Artifact:** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/doc-02-pricing-email.md`
**Review type:** single expert pass (contract compliance + billing accuracy + customer-notice practice)
**Verdict:** Not sendable. Two critical defects — the effective date breaches the contractual notice period, and the billing paragraph is wrong or materially misleading for the ~40% of the base on annual plans.

---

## Findings

### 1. CRITICAL — Effective date breaches the 60-day notice requirement in clause 7.2
**Location:** line 13
**Anchor:** "Starting **1 September 2026**, the Team plan moves from $29 to $39 per seat per month"
**Problem:** Sending on 5 August 2026 for a 1 September effective date gives 27 days' notice, well short of the "no less than sixty (60) days" required by clause 7.2, so the increase is unenforceable and the send itself is a breach.

Notice math: 5 Aug 2026 + 60 days = **4 October 2026** is the earliest compliant effective date. Anything before that is non-compliant for every affected subscriber. Practical fix: move the effective date to 5 October 2026 or later (a clean 1 November 2026 gives buffer for send-date slippage and any per-customer send delays), or delay the send. Note the deadline is per-customer: the 60 days runs from when *that* subscriber receives notice, so a staggered or partially-failed send does not get the benefit of the 5 August date.

### 2. CRITICAL — The billing paragraph is wrong or materially misleading for annual subscribers (~40% of the base)
**Location:** line 15
**Anchor:** "Your card on file will be charged the new amount on your next billing date after 1 September. No action is needed from you."
**Problem:** Annual customers prepaid for terms running into 2027, so this sentence either (mis)states that they will be repriced from 1 September mid-term, or — if read literally as "at renewal" — leaves 40% of recipients with no idea when or at what rate they are actually affected.

Both readings are bad. If billing systems are configured to match the literal instruction, annual subscribers get charged mid-term on a prepaid term, which is a second contract problem on top of the notice defect. If they are not, the email tells 40% of the base something that does not describe what will happen to them. The email needs an explicit carve-out along the lines of: annual plans keep their current rate for the remainder of the paid term and move to the new rate at their next renewal on or after [date], with clause-7.2-compliant notice given ahead of that renewal.

Also note that any annual renewal falling before ~4 October 2026 cannot be repriced on this notice either.

### 3. MAJOR — No cancellation or downgrade path; "No action is needed" forecloses the customer's options
**Location:** line 15
**Anchor:** "No action is needed from you."
**Problem:** A price-increase notice must tell the customer what to do if they do *not* accept — cancel, downgrade, or reduce seats before the effective date — and this line affirmatively implies there is no alternative.

This is standard practice for fee-change notices and, in several jurisdictions, a condition of the change being fairly imposed on a continuing contract. It is also the paragraph most likely to be screenshotted in a complaint. It needs an explicit "if you'd prefer not to continue at the new rate, you can cancel or change your plan before [effective date]" with a link.

### 4. MAJOR — Subject line conceals the purpose of the notice
**Location:** line 7
**Anchor:** "**Subject:** A few updates to your Northwind account"
**Problem:** A vague subject on what is meant to be formal contractual notice of a fee increase undercuts the argument that adequate written notice was given, and predictably suppresses opens on the one email customers most need to read.

Clause 7.2 requires written notice; notice a reasonable recipient would not identify as a fee change is weak ground if the increase is later disputed. The subject should name the change and the date, e.g. "Important: Northwind pricing changes effective [date]". The same issue runs into the body — line 11 opens with three sentences of product wins before the change is mentioned. The achievements framing is fine as justification, but the change and its date should be visible above the fold.

### 5. MINOR — Assumes every subscriber pays by stored card
**Location:** line 15
**Anchor:** "Your card on file will be charged the new amount"
**Problem:** Business-tier and annual customers are commonly invoiced by ACH, wire or PO rather than a stored card, so this sentence will read as inaccurate to part of the base and should be neutral ("your next invoice / your usual payment method").

### 6. MINOR — Support offer with no channel attached
**Location:** line 17
**Anchor:** "If you have questions, our team is here."
**Problem:** No email address, link, or reply-to instruction is given, so a customer who wants to query the increase has nowhere to click at the exact moment they are motivated to act.

### 7. MINOR — No link to updated pricing and no per-customer impact figure
**Location:** line 13
**Anchor:** "the Business plan moves from $79 to $99 per seat per month"
**Problem:** Only per-seat monthly list prices are given — there is no link to the updated pricing page, no annual-plan rate, and no merge field for the recipient's own new total, so each customer has to compute their own impact.

Given `{{first_name}}` is already merged in, plan, seat count, new monthly/annual total, and the customer's own effective date are all cheap to merge and would remove most of the ambiguity flagged in findings 1 and 2.

---

## Checked and sound

- Arithmetic and internal consistency of the stated prices ($29→$39, $79→$99, Starter unchanged) — no contradiction anywhere in the draft.
- Justification framing (product investment before the ask) is a legitimate and common structure; my objection at finding 4 is to its *position* relative to the disclosure, not to its presence.
- Tone of "We know price changes are never fun, and we didn't take this lightly" is a judgement call, not a defect, and I have not scored it.

## One thing to verify outside this document

Clause 7.2 requires "written notice" — confirm the ToS notices clause accepts email to the account address as written notice. If it specifies post or an in-product mechanism, this email is not sufficient service regardless of the date fix. I could not check this from the excerpt supplied and have not counted it as a finding.

---

**Totals:** critical 2 · major 2 · minor 3
