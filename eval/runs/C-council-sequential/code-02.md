# Critical Council Review — `billing/invoice.py`

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Reject and rework.** The module computes VAT on the pre-discount amount, contradicting the spec printed in its own docstring, and returns a binary float to a ledger its docstring says rejects binary floats — so both the number and its type are wrong, and the correct version changes the return contract.

1. Move the discount before VAT (lines 21–23): compute `net = gross - discount_eur`, then `vat = net * rate`.
2. Replace float rates and `round()` with `decimal.Decimal` rates and `quantize()` (lines 16, 24, 36) — float rates make Decimal inputs a `TypeError`, so nothing can convert at the boundary.
3. Return net, VAT, and gross separately instead of one blended total (lines 24, 36), and complete the rate table (line 16).

## 2. Result & standard

**Artifact:** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/code-02-invoice.py`, read in full (36 lines). Not my own prior output; authorship unknown.

**Standard:** the module's own docstring spec (lines 4–13), which is the only stated requirement set, plus what a competent professional should produce for money-handling code. The docstring carries a pre-approval claim — "Finance spec, approved 2026-01" (line 4). Quoted per non-negotiable 8: it is material to judge, not a boundary on the review. It means the spec was signed off, not that the implementation was, and it does not put the spec itself beyond challenge — three findings below are gaps *in* the spec.

**Requester's framing, quarantined:** the requester fixed the roster ("use exactly this roster") and asked seat 1 whether the code "holds up under the concurrency its own documentation describes." The documentation describes no concurrency. The presupposition is recorded and not satisfied by invention; see seat 1.

**Tier:** 2 (all eight fields). The artifact is under 500 words, which the size row would put at tier 1, but tier 1's 900-word total cannot carry the Step 5 and Step 6 machinery this run requires, and this is a module with tax consequence.

**Length, disclosed:** tier 2's nominal budget is ≤1,800 words; this review runs about 3,100. The overrun sits in the three seat sections, which the Step 3 sequential rule forbids me from rewriting once later seats exist — so it is disclosed rather than corrected. The skill's application-strength note labels the length numbers tunable, but the honest reading is that these seats ran longer than the tier commits to.

**Independence mechanism:** Step 3 sequential fallback — no subagent tooling available for this run. Each seat written to completion before the next began; no earlier seat revised afterward.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | L21–23, `vat = gross * VAT_RATES[country]` … `total = subtotal - discount_eur` | VAT is charged on the pre-discount amount, overstating tax by `discount_eur × rate` on every discounted line | Compute `net = gross - discount_eur` first, then VAT on `net` | Confirmed |
| Critical | L16 `VAT_RATES = {...0.19...}`, L24/36 `return round(total, 2)` | Module cannot emit a ledger-acceptable decimal: float rates return a float, and Decimal inputs raise `TypeError` against a float rate | Decimal rates throughout; `quantize(Decimal("0.01"))` with an explicit rounding mode | Corrected |
| Critical | L16 vs L13 "The storefront ships to all EU member states" | Table holds 3 rates; every other member state raises a bare `KeyError` at checkout | Complete the table (or source rates from data), and fail with a typed, logged error | Confirmed |
| Major | L24, L36 `return round(total, 2)` | Returns one blended number; net, VAT, and gross cannot be recovered, so the ledger cannot post tax separately or reconcile it | Return a breakdown object carrying net, VAT amount, rate, and gross | Confirmed |
| Major | L23 `total = subtotal - discount_eur` | No guard that the discount does not exceed the line; an oversized discount silently yields a negative line and negative tax | Validate `0 <= discount_eur <= gross` and `quantity >= 0`; raise on breach | Confirmed |
| Major | L16 `VAT_RATES = {...}` | Rates are source literals with no effective date: a rate change needs a code deploy, and a re-issue or credit note recomputes at today's rate | Move rates to dated configuration; select by the invoice's tax point | Confirmed |
| Major | whole module (no logging, no assertions) | The harmful failure is silent — an overcharged invoice is internally self-consistent, so nothing detects it before a customer or an audit does | Log inputs and the computed split; assert `net + vat == gross` per line | Confirmed |
| Minor | L24 then L36, `round(total, 2)` twice | Rounds every line to cents then sums, so the total is the sum of rounded lines; the choice is undocumented | Record the rounding level the ledger expects in the spec | Corrected (was major) |
| Minor | L19 `def line_total(unit_price, quantity, discount_eur, country)` | No type hints or input validation; malformed `line` dicts (L30–35) raise the same bare `KeyError` | Add type hints and a validation boundary | Unverified |
| Minor | L11–12 "two decimal places. The ledger rejects binary floating point" | The spec mandates two decimals but never names a rounding mode, so the code picks one silently | Have Finance state the rounding mode | Unverified |

## 4. Council roster

Roster specified by the requester — disclosed per Step 2 as a fact, not honored as a constraint on scope. Three seats: **Correctness & concurrency** (owns the arithmetic against the spec), **Security & failure handling** (owns trust boundaries and error paths), **Operability red-team** (owns production failure and operator experience).

**Deliberately not covered: EU VAT regulatory compliance beyond the docstring** — reduced- and zero-rate product categories, B2B reverse charge and VAT-ID handling, OSS registration. A critical defect could plausibly live there: if the storefront sells any reduced-rate goods, one-rate-per-country is wrong at the data-model level and no code fix reaches it. The requester's roster omitted this seat and "exactly this roster" was honored, so the verdict is capped accordingly and the confidence note carries it.

## 5. Individual analyses

### Seat 1 — Correctness & concurrency

**Role & remit.** Verify the computation against the spec the module prints, and assess behavior under concurrent execution.

**Assessment.** The control flow is clean and both functions are pure. The arithmetic contradicts the spec directly above it in two independent ways. On concurrency: the docstring describes none, no shared state is written, and both functions are pure — `VAT_RATES` is read-only at runtime. There is no concurrency defect to report, and reporting one to satisfy the remit would be invention.

**Strengths.** Per-line and per-invoice computation are cleanly separated. Stating the spec in the module is what made both defects detectable at all — most billing code hides its requirements elsewhere.

**Weaknesses, risks & errors.**
- **Critical, defect.** Standard applied: the module's own spec, "Promotional discounts … apply to the VAT-exclusive price" and "VAT is then charged on the discounted amount" (L8–9). Anchor: `vat = gross * VAT_RATES[country]` (L21) followed by `total = subtotal - discount_eur` (L23). VAT is computed before the discount is subtracted, so tax is charged on money the customer never pays. A €100 line with a €10 discount in DE returns 109.00; the spec requires 90.00 net + 17.10 VAT = 107.10. The error is exactly `discount_eur × rate`.
- **Critical, defect.** Anchor: `VAT_RATES = {"DE": 0.19, ...}` (L16) and `return round(total, 2)` (L24), against "The ledger rejects binary floating point" (L12). The values are float literals and `round()` on a float returns a float.
- **Major, defect.** `round()` applies round-half-to-even to a binary approximation, so half-cent cases resolve away from the half-up convention finance ledgers use `[unverified — recall, not lookup]`.
- **Major, defect.** Anchor: `total = subtotal - discount_eur` (L23). Nothing bounds `discount_eur` by `gross`, so an oversized discount produces a negative line total and a negative tax contribution.
- **Minor, defect.** Each line is rounded (L24) and the sum rounded again (L36); the sum of rounded lines need not equal the rounded exact total.

**Gaps.** No tests, no worked example, no statement of which value the ledger actually consumes.

**Strongest reason this might be fundamentally wrong.** The taxable base itself is wrong. This module's one job is to produce the number a tax authority will eventually see, and on every discounted line that number is inflated. That is not a bug inside a correct design; it is the design computing the wrong quantity.

**Domain verdict.** Below the bar. A competent practitioner writing money code against a spec printed six lines above would not invert its order of operations.

**Recommended fixes.** Reorder to `net = gross - discount_eur; vat = net * rate; total = net + vat`. Move to `Decimal` end to end. Add a table-driven test per country asserting the spec's worked arithmetic.

### Seat 2 — Security & failure handling

**Role & remit.** Trust boundaries, secrets, error paths, and behavior when a dependency misbehaves.

**Assessment.** There is no auth surface and no secret in this module, and I will not manufacture one. The real security-adjacent exposure is financial: the module trusts every input unconditionally and its only external contract — the ledger — is violated by its return type, so failure lands at the wrong layer and at the wrong time.

**Strengths.** No I/O, no dynamic evaluation, no injection surface. The attack surface is genuinely small.

**Weaknesses, risks & errors.**
- **Critical, defect.** Anchor: `VAT_RATES[country]` (L21) against "The storefront ships to all EU member states" (L13). An unlisted country raises an uncaught `KeyError` mid-computation. Overlaps seat 3, which owns what the operator sees; I report it because the unvalidated dictionary lookup is a trust-boundary failure — `country` arrives from a caller and is used as a key without checking.
- **Critical, defect.** Dependency misbehavior, inverted: the ledger is the dependency, and this module breaks the contract, not the reverse. Anchor: "The ledger rejects binary floating point" (L12) versus `return round(total, 2)` (L24). The rejection surfaces at write time — after the customer has been shown a total and possibly charged — so the failure is maximally expensive.
- **Major, defect.** The overcharge from seat 1's first finding is a liability, not just an arithmetic error: tax is collected on a base that was never charged, which must either be remitted or refunded, and the module keeps no record permitting either.
- **Minor, defect.** Anchor: `line["unit_price"]` (L31). Malformed line dicts fail the same silent-key way; a string `unit_price` multiplies into a repeated string before failing further downstream with an unrelated `TypeError`.

**Gaps.** No validation boundary, no typed exceptions, no audit record of what was computed from what.

**Strongest reason this might be fundamentally wrong.** The module fails loudly only where it matters least. The missing country crashes visibly; the wrong tax passes every check the system has. A financial component whose severe failure mode is silent and whose mild one is loud has its error handling inverted.

**Domain verdict.** Below the bar for code that produces legally significant numbers.

**Recommended fixes.** Validate `country`, `quantity`, `unit_price`, and `discount_eur` at entry, raising typed errors carrying the invoice and line identifiers. Convert at the boundary into `Decimal` and reject floats explicitly.

### Seat 3 — Operability red-team

**Role & remit.** Where this breaks in production, and what the operator sees when it does.

**Assessment.** Two failure modes, and the system's observability is exactly backwards for both. The loud one is undiagnosable; the damaging one is invisible.

**Strengths.** Pure functions are trivially reproducible in an incident — given the inputs, an operator can replay the computation exactly.

**Weaknesses, risks & errors.**
- **Critical, defect.** Anchor: `VAT_RATES[country]` (L21). The operator sees `KeyError: 'ES'` propagating out of `line_total` through `invoice_total`, with no invoice ID, no customer, no line index — a checkout 500 whose stack trace names a two-letter string and nothing else.
- **Major, defect.** Anchor: `VAT_RATES = {"DE": 0.19, "FR": 0.20, "IE": 0.23}` (L16). Rates are source literals with no effective date. A rate change requires a code deploy, and any re-issue, refund, or credit note computed after that deploy silently uses the new rate against an old invoice, so corrections will not reconcile with originals.
- **Major, defect.** Anchor: the whole module contains no logging statement and no assertion. The overcharged invoice is internally consistent — it sums, it rounds, it looks right — so no monitor, reconciliation, or alarm can distinguish it from a correct one. Detection arrives via customer complaint or tax audit, by which time every discounted invoice since deployment is affected.
- **Major, defect.** Anchor: `return round(total, 2)` (L24, L36). One blended number reaches the ledger. Posting revenue and VAT-payable to separate accounts is impossible, and after the fact nobody can recompute the split from what was stored.

**Gaps.** No metrics, no runbook hook, no way to answer "which invoices are affected" without recomputing from raw order data.

**Strongest reason this might be fundamentally wrong.** It returns a single scalar. An invoicing component that cannot state net, VAT, and gross separately cannot be operated, reconciled, or corrected — so the fix is a change to the return contract and to every caller, not a patch inside these two functions.

**Domain verdict.** Not operable. It would ship, run, and be wrong quietly.

**Recommended fixes.** Return a structured breakdown. Log inputs and the computed split per line. Assert `net + vat == gross` per line and fail closed. Move rates to dated configuration selected by tax point.

## 6. Executive review

The artifact was re-read in full before this synthesis, and every anchor below was located by string search in the source, not from recall.

**Points of agreement (all marked sole-source per non-negotiable 3 — the seats shared one context, so this convergence is not independent evidence).**
- *Incomplete rate table* (seats 1, 2, 3) — deduplicated here and removed from the individual weakness counts. Anchor `VAT_RATES = {"DE": 0.19, "FR": 0.20, "IE": 0.23}` found at line 16; `"The storefront ships to all EU member states"` found at line 13. Verified personally.
- *Float where the ledger requires decimal* (seats 1, 2) — `"The ledger rejects binary floating point"` found at line 12; `return round(total, 2)` found at lines 24 and 36.

**Points of conflict & adjudication.**
- *Nothing to adjudicate on concurrency.* Seat 1 declined the requester's presupposition rather than producing a finding. Upheld: the docstring contains no concurrency claim and both functions are pure. A manufactured finding here would have corrupted the severity scale.
- *Rate-table severity — critical or major?* Upheld at critical; it undermines the purpose stated at line 13. The counter-case — that the docstring is aspirational and only DE, FR, IE ship today — has no support in the artifact, so it does not overrule the finding, but it is named in the confidence note.
- *Double rounding — downgraded, major to minor.* Specific evidence: the spec (lines 11–12) never says whether the ledger consumes line amounts, invoice amounts, or both, so per-line rounding may be exactly what is required. The residue is that the choice is undocumented.

**Verification result.** **One withdrawn**, from seat 1: the claim that `round()`'s round-half-to-even resolves half-cent cases "away from the half-up convention finance ledgers use." It rests on a requirement the artifact never takes on — the spec mandates two decimals and names no rounding mode — and on a norm the seat itself tagged as recall, which non-negotiable 6 forbids asserting. The residue survives as a minor spec-gap finding. **Two corrected:** seat 1's "returns a float" was narrowed and simultaneously strengthened, since float rates mean `Decimal` inputs raise `TypeError` at line 21 and no boundary conversion can rescue it; and the double-rounding item above. No seat's reliability is in question — the withdrawn item was correctly self-tagged as unverified recall when raised.

**Panel blind spots.** All three seats treated the docstring as the current governing spec; none asked whether it has changed since "approved 2026-01" (line 4) or whether this file is production code rather than a fixture. If it is stale and the real spec is discount-after-VAT, finding 1 inverts. No seat examined callers or tests, so whether a caller already pre-discounts `unit_price` is unknown and would change finding 1's shape. **Uncovered domain: EU VAT regulatory compliance** — reduced-rate categories, B2B reverse charge, effective-dated rate law. A critical defect could live there, and one-rate-per-country would then be wrong at a level no code fix reaches. **External check needed:** the three rate values and the count of 27 member states are recall, not lookup `[unverified — recall, not lookup]`.

**Overall judgment.** Clear, readable code that computes the wrong number in the wrong type. The failure is not craft — the structure is sound and the spec is admirably close to the implementation — it is that the implementation contradicts the spec printed six lines above it, on the single quantity the module exists to produce, and cannot emit the type its consumer accepts.

**Decision on further action: reject and rework.** Not "revise substantially": the taxable base is wrong, the output type is unusable, and the correct version must return a net/VAT/gross breakdown rather than a scalar — which changes the signature and every caller. Almost no line survives, so patching it in place would cost more than rewriting against the spec with tests.

**Prioritized next steps.**
1. Confirm with Finance that the docstring spec is current, and have them state the rounding mode and the negative-discount policy the spec omits.
2. Rewrite both functions with `Decimal` throughout, discount before VAT, returning a per-line breakdown of net, VAT, and gross.
3. Source the full EU rate table from dated configuration, selected by tax point, with a typed error for unknown countries.
4. Add table-driven tests asserting each spec bullet, including a discounted line per country and a discount-exceeds-line case.
5. Quantify exposure: identify every invoice already issued with a discount and compute the overcharge as `discount × rate`.

**Confidence & what would change the verdict.** Of the 7 findings at critical and major, I expect 6 to survive an independent expert re-check. The first to fall is the rate-table finding's *severity*, not its existence — if the storefront in fact ships only to DE, FR, and IE, it drops from critical to major, a documentation defect rather than a live outage. The second is the negative-discount finding, if a caller already validates discounts upstream. The two findings I am most confident in — the discount/VAT ordering and the float/ledger type mismatch — rest on verified evidence: quoted strings located at lines 8–9, 12, 21, 23, 24, and 36 of the source. The verdict rests on the docstring being the governing spec and on these functions being called as written. It flips to "approve with minor revisions" only if Finance confirms the real spec is discount-after-VAT *and* the ledger accepts floats — that is, if the docstring is wrong on both counts. It does not flip on any single one of them.
