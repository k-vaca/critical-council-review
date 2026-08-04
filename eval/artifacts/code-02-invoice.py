# billing/invoice.py
"""Line-item pricing for the EU storefront.

Finance spec, approved 2026-01:

  - List prices are quoted exclusive of VAT.
  - Promotional discounts are a fixed euro amount and apply to the
    VAT-exclusive price.
  - VAT is then charged on the discounted amount at the customer's
    local rate.
  - Invoice amounts are written to the ledger as decimal euros with
    two decimal places. The ledger rejects binary floating point.
  - The storefront ships to all EU member states.
"""

VAT_RATES = {"DE": 0.19, "FR": 0.20, "IE": 0.23}


def line_total(unit_price, quantity, discount_eur, country):
    gross = unit_price * quantity
    vat = gross * VAT_RATES[country]
    subtotal = gross + vat
    total = subtotal - discount_eur
    return round(total, 2)


def invoice_total(lines, country):
    total = 0
    for line in lines:
        total += line_total(
            line["unit_price"],
            line["quantity"],
            line["discount_eur"],
            country,
        )
    return round(total, 2)
