# Expert review — `billing/invoice.py`

**Artifact:** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/code-02-invoice.py`
**Scope:** one careful review pass, judged against the finance spec in the module docstring.
**Verdict:** Not fit to ship. Three critical defects, two of which put wrong money on the ledger and one of which makes the module unusable for most of its stated market. The module contradicts three of the five bullets in its own docstring.

---

## Critical

### C1 — Discount is applied after VAT, inverting the specified order

**Location:** `line_total`, lines 21–23

**Anchor:**
```
vat = gross * VAT_RATES[country]
subtotal = gross + vat
total = subtotal - discount_eur
```

**Problem:** The spec requires the discount to reduce the VAT-exclusive price and VAT to be charged on the discounted amount, but the code charges VAT on the full undiscounted price and then subtracts the discount from the VAT-inclusive figure.

**Detail.** The code computes `gross*(1+r) - d`. The spec requires `(gross - d)*(1+r)`. The difference is exactly `d * r` — the customer is overcharged by the discount multiplied by the VAT rate, on every discounted line. Verified: unit_price 100.00, qty 1, discount 10.00, DE (19%) yields **109.00** from this code versus **107.10** per spec — a EUR 1.90 overcharge on a single line.

The tax consequence is worse than the customer-facing one. The code declares VAT of 19.00 on a taxable base that the spec says is 90.00. The VAT actually remitted to the tax authority is overstated, and the VAT amount on the invoice will not reconcile against the net amount at any published rate. This is a filing defect, not just a pricing defect.

**Fix:** `taxable = gross - discount_eur; total = taxable * (1 + rate)`.

---

### C2 — Binary floating point throughout, in a module whose ledger rejects binary floating point

**Location:** line 16 (`VAT_RATES`), line 24 and line 36 (`round(..., 2)`), line 28 (`total = 0`)

**Anchor:**
```
VAT_RATES = {"DE": 0.19, "FR": 0.20, "IE": 0.23}
```

**Problem:** Every value the module produces is a Python `float`, but the docstring states the ledger accepts only decimal euros and rejects binary floating point, so no output of this module is acceptable to its declared consumer.

**Detail.** `0.19`, `0.20` and `0.23` are not exactly representable in binary; neither is the product of a price and a rate in the general case. `round(x, 2)` does **not** return a decimal — it returns a `float` that is merely the nearest binary double to a 2-decimal value. `round(109.0, 2)` is `109.0`, not `109.00`; there is no scale information to carry to the ledger, and re-summing such values drifts (`0.1 + 0.2 == 0.30000000000000004`).

Whether this manifests as a hard rejection at the ledger boundary or as a silently coerced value depends on the ledger adapter, and neither outcome is acceptable in a billing path. The whole module needs to be rebuilt on `decimal.Decimal`: rates as `Decimal("0.19")`, the accumulator on line 28 as `Decimal("0.00")`, and the final scaling via `.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`.

**Fix:** Move to `decimal.Decimal` end to end. Construct rates from strings, never from float literals (`Decimal(0.19)` inherits the binary error and is a common mis-fix).

---

### C3 — VAT table covers 3 of 27 member states; every other country raises `KeyError`

**Location:** line 16, consumed unguarded at line 21

**Anchor:**
```
VAT_RATES = {"DE": 0.19, "FR": 0.20, "IE": 0.23}
```

**Problem:** The docstring states the storefront ships to all EU member states, but the rate table holds three countries and `VAT_RATES[country]` raises an unhandled `KeyError` for the other twenty-four.

**Detail.** The three rates present are themselves correct standard rates (DE 19%, FR 20%, IE 23%), so this is a completeness failure rather than a data-accuracy failure. But it is load-bearing: an order from ES, IT, NL, PL or any of the remaining members crashes inside the pricing path with a bare `KeyError`, in a code path that a checkout flow will call synchronously. There is no fallback, no explicit validation, and no error message naming the unsupported country.

Related and cheap to fix at the same time: the lookup is case- and whitespace-sensitive, so `"de"` or `"DE "` fails identically. Normalise the key and raise a domain-specific exception (`UnsupportedCountryError`) rather than letting a `KeyError` escape.

**Fix:** Populate all 27 member states, and guard the lookup with an explicit check that fails with a meaningful error.

---

## Major

### M1 — `round()` is banker's rounding, not the half-up rounding invoicing requires

**Location:** `line_total` line 24, `invoice_total` line 36

**Anchor:**
```
return round(total, 2)
```

**Problem:** Python's built-in `round()` rounds halves to even rather than half-up, so cent-level amounts differ from the commercial convention finance and tax authorities expect.

**Detail.** `round(0.125, 2)` returns `0.12`, not `0.13`. Compounded with C2, the result is doubly unpredictable: `round(2.675, 2)` returns `2.67` because the stored double is fractionally below 2.675, so the direction of the error is not even consistently "toward even". Every affected line is off by one cent, and those cents land on tax filings.

This is listed separately from C2 because fixing the type without fixing the rounding mode leaves the bug in place — `Decimal.quantize()` defaults to `ROUND_HALF_EVEN` too.

**Fix:** `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`, with the chosen mode documented against the finance spec.

---

### M2 — No input validation; a discount larger than the line value silently produces a negative charge

**Location:** `line_total` lines 19–23

**Anchor:**
```
def line_total(unit_price, quantity, discount_eur, country):
```

**Problem:** Nothing constrains the inputs, so a fixed-euro promotion that exceeds the line value (a EUR 10 coupon on an EUR 8 item) yields a negative line total that silently credits the customer against the rest of the invoice.

**Detail.** This is a realistic scenario for exactly the promotion type the spec describes — a fixed euro amount, not a percentage — and the failure is silent: the negative line offsets other lines inside `invoice_total`, so the invoice still looks plausible. Negative `quantity` and negative `unit_price` are equally unguarded, and a negative `discount_eur` becomes a surcharge. In a billing path these are money-leak paths, not hygiene issues.

**Fix:** Reject negative `unit_price`, `quantity` and `discount_eur`; clamp the discount at the line's net value (`max(gross - discount_eur, 0)`) or raise, per finance's decision — and get that decision recorded, since the spec is silent on it.

---

## Minor

### m1 — Only a single combined figure is returned; no net/VAT split

**Location:** `line_total` return value, line 24

**Anchor:**
```
return round(total, 2)
```

**Problem:** The function collapses net, VAT and gross into one number, so no downstream consumer can produce the VAT breakdown an EU invoice and a VAT return require without recomputing it.

Returning a small structure (net, vat, gross) or at minimum a parallel `line_vat()` would avoid every caller re-deriving the tax component and drifting from this module's rounding.

---

### m2 — Rounding granularity is an unrecorded policy choice

**Location:** `line_total` line 24 combined with `invoice_total` lines 30–36

**Anchor:**
```
total += line_total(
```

**Problem:** The code rounds every line to two decimals and then sums the rounded values, but the spec only says "invoice amounts" are two-decimal, leaving it unstated whether rounding belongs per line or per invoice.

Per-line and per-invoice rounding give different totals once you have several lines, and both are defensible depending on jurisdiction and finance policy. The defect is that the choice is implicit — a reviewer or auditor cannot tell whether it was decided or fell out of the implementation. Note also that `invoice_total` re-rounds an already-rounded sum on line 36, which is a no-op that reads as if it were doing something.

**Fix:** Confirm the policy with finance and state it in the docstring next to the existing bullets.

---

### m3 — VAT rates hardcoded with no effective date or provenance

**Location:** line 16

**Anchor:**
```
VAT_RATES = {"DE": 0.19, "FR": 0.20, "IE": 0.23}
```

**Problem:** Rates are baked into the module with no effective-from date and no source, so a statutory rate change requires a code deploy and historical invoices cannot be reproduced after one.

Member states change standard rates, sometimes at short notice and sometimes temporarily. Re-issuing or auditing an invoice raised before a change will silently apply today's rate. Rate data belongs in dated configuration keyed by `(country, effective_from)`, with the invoice date as an input.

---

## Not defects

Recorded so the absence is deliberate, not an oversight:

- The three rates present are the correct current standard rates for DE, FR and IE.
- Keying VAT off the customer's country is right for B2C distance selling under the spec as written; B2B reverse charge and reduced/zero rates for specific goods are out of scope of the stated spec, not omissions from it.
- Missing type hints and docstrings on the two functions are style, not defects.

---

## Summary

| Severity | Count |
|---|---|
| Critical | 3 |
| Major | 2 |
| Minor | 3 |

C1 and C2 each make every output of this module wrong or unusable, and they are independent — fixing one does not mask the other. C3 makes the module unusable for 24 of the 27 markets it claims to serve. M1 must be fixed in the same change as C2 or it will survive the migration to `Decimal`. Recommend a rewrite of `line_total` rather than patching in place, with test cases pinned to worked examples signed off by finance — starting with the 100.00 / 10.00 / DE case, which must produce 107.10.
