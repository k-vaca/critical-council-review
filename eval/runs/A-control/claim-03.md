# Expert review — claim-03-cost-model.md

**Artifact:** Build vs buy: replacing Streamvault with self-hosted ingestion
**Review type:** single careful expert pass, cost-model and decision-memo standards

## Verdict

The document should not be presented to the September architecture review in its current
state. The recommendation may still be directionally right, but it is not supported by the
model as written. Two independent arithmetic errors in the cost table, a one-time cost that
is mentioned and then never costed, and a timeline that strands the business without an
ingestion path are each individually sufficient to require a rework.

The corrected annual saving is roughly **$47,000 (22%)**, not the **$71,260 (34%)** claimed —
and the single largest assumption in the model (0.5 FTE) is untested and, if wrong by one
half-head, reverses the conclusion entirely.

One structural observation worth flagging to the author: the recommendation is stated in the
header before any analysis, and every arithmetic error found points the same direction
(making self-hosting look cheaper). That pattern is worth an author self-check even if each
error is individually innocent.

---

## Corrected model

| Line | As stated | Corrected | Note |
|---|---|---|---|
| Compute (6 × c6i.4xlarge, reserved) | $28,380 | $28,380 | arithmetic correct; rate itself needs verification (minor 4) |
| Storage (40 TB, gp3) | $920 | **$11,040** | stated figure is monthly, not annual |
| Data transfer (18 TB/month egress) | $19,440 | $19,440 | correct |
| Engineering (0.5 FTE) | $90,000 | $90,000 | arithmetic correct; assumption untested (major 1) |
| Monitoring and tooling | $14,000 | $14,000 | present in table, excluded from total |
| **Total** | **$138,740** | **$162,860** | |

Against Streamvault at $210,000: saving **$47,140 / 22.4%**, not $71,260 / 34%.

Adding the uncosted migration (four months of engineering time — roughly $60,000 if that
means one engineer, $120,000 if two), payback is approximately **15 to 30 months**, not
"immediate."

At 1.0 FTE rather than 0.5, the total becomes $252,860 and self-hosting costs **$42,860 more
per year** than the incumbent.

---

## Findings

### CRITICAL

**C1 — Storage line is a monthly figure presented as annual**
*Location:* Annual cost table, row "Storage (40 TB, gp3)" (line 21)
*Anchor:* "| Storage (40 TB, gp3) | $920 |"
*Problem:* 40,000 GB × $0.023/GB-month = $920 **per month**; the annual figure is $11,040, so
the table understates storage by $10,120.

Note that the egress line directly beneath it *was* correctly annualized
(18,000 × $0.09 × 12 = $19,440), which rules out a deliberate monthly-column convention and
confirms this as an error rather than a labelling choice.

**C2 — Table total omits a line item it lists**
*Location:* Annual cost table, "Total" row (line 25)
*Anchor:* "| **Total** | **$138,740** |"
*Problem:* The column sums to $152,740; the stated total is exactly $14,000 lower, silently
excluding the "Monitoring and tooling" row that appears immediately above it.

Combined with C1, the headline conclusion on line 29 — "a saving of **$71,260** a year, or
34%" — is wrong by roughly $24,000 per year. The internal consistency of the conclusion
(71,260 ÷ 210,000 does equal 34%) means the error propagates cleanly and is not self-evident
to a reader checking only the final paragraph.

**C3 — Migration cost is acknowledged and then never costed; "payback is immediate" is false**
*Location:* "Proposed self-hosted setup" (line 14) and "Conclusion" (line 29)
*Anchor:* "Payback is immediate because there is no capital outlay on reserved instances
beyond the first invoice."
*Problem:* Four months of engineering time is stated as a requirement but appears in no line
item and no payback calculation, so the memo claims zero switching cost while describing a
substantial one.

Three separate defects sit in this one sentence:

1. The four-month migration is a real one-time cost. At the memo's own $180,000 fully loaded
   rate it is ~$60,000 for one engineer. It is excluded entirely.
2. The stated reason is a non sequitur. Payback measures recovery of one-time switching
   costs; the absence of capital outlay on instances says nothing about whether the migration
   labour has been recovered.
3. "Four months of engineering time" does not specify headcount. Four months of one engineer
   and four months of a three-person team differ by a factor of three in cost and are not
   distinguishable from the text. This ambiguity must be resolved before the number means
   anything.

With the corrected $47,140 annual saving, payback is roughly 15 months at one engineer and
roughly 30 months at two — material to a decision framed around a 1 December deadline.

**C4 — The recommended timeline leaves a service gap with no ingestion**
*Location:* "Current spend" (line 8), "Proposed self-hosted setup" (line 14), "Conclusion"
(line 31)
*Anchor:* "giving notice on the Streamvault contract before the 1 October renewal deadline
and starting the migration in Q4"
*Problem:* Notice by 1 October ends Streamvault on 1 December, but a four-month migration
starting in Q4 completes around February, leaving roughly two months with the vendor gone and
the replacement not ready.

A reader acting on this recommendation as written commits to terminating the incumbent before
the replacement exists. The memo contains no parallel-run period, no overlap budget, and no
fallback if migration slips — and migration estimates of this kind routinely slip. Either the
notice decision needs to be deferred by a renewal cycle, or a bridging arrangement (short
extension, month-to-month, parallel run) must be costed into the model. Neither is present.

### MAJOR

**M1 — The 0.5 FTE assumption is load-bearing, untested, and reverses the conclusion if wrong**
*Location:* "Proposed self-hosted setup" (line 12)
*Anchor:* "We would need half an engineer to run it, costed at a fully loaded $180,000 FTE."
*Problem:* Engineering is 55% of the corrected total and rests on a single unexplained
estimate; at 1.0 FTE the self-hosted option costs $252,860 and becomes $42,860 per year *more
expensive* than Streamvault.

Any assumption that can flip the sign of the recommendation on its own needs either a
derivation or an explicit sensitivity range. The memo offers neither, and offers no basis for
why half a head is sufficient to operate a 24/7 ingestion platform including on-call
rotation, patching, capacity management, and incident response — work the vendor currently
absorbs.

**M2 — The Streamvault baseline mixes the current contract's price with the new contract's terms**
*Location:* "Current spend" (line 8)
*Anchor:* "invoices us **$210,000 per year** on the current contract, which renews 1 December
2026"
*Problem:* The $210,000 is the *current* contract price, but the overage exclusion is
justified by the *new* contract's terms, and the new contract's actual annual price is never
stated anywhere in the memo.

The comparison is against a price that will not be in effect during the period being modelled.
Two sub-issues compound it:

- "we have excluded here because the new contract caps it" — a cap is not zero. A capped
  overage still carries cost up to the cap, and that cost belongs in the baseline. (This
  exclusion is conservative, i.e. it makes the incumbent look cheaper and works against the
  memo's own recommendation, so it is not a directional-bias concern — but it is still
  methodologically unjustified.)
- The $18,000 is described as covering "the last two quarters." Whether the annualized figure
  is $18,000 or $36,000 is not resolvable from the text.

**M3 — Three-year commitment compared against a one-year contract, and the RI purchase mechanics are misdescribed**
*Location:* "Proposed self-hosted setup" (line 12), "Conclusion" (line 29)
*Anchor:* "Six `c6i.4xlarge` instances on three-year reserved pricing at $4,730 each per year."
*Problem:* The model commits to three years of capacity to beat a contract that renews
annually, without pricing that asymmetry or the risk it creates.

Two distinct concerns:

- **Commitment asymmetry.** If volumes change, the platform is retired, or the migration
  fails, the reserved instances remain a liability while the alternative (staying with
  Streamvault) carried only a one-year commitment. This optionality difference has real value
  and is not acknowledged.
- **"No capital outlay ... beyond the first invoice"** misdescribes how three-year RIs are
  purchased. Three-year reserved pricing is available as all-upfront, partial-upfront, or
  no-upfront, and the rate quoted needs to be tied to whichever structure is intended. The
  no-upfront variant that would match this claim carries a *higher* effective rate than the
  upfront variants. Either way it is a binding three-year obligation, not a first-invoice
  arrangement.

**M4 — Flat volumes assumed over a three-year horizon despite documented volume growth**
*Location:* "Current spend" (line 8) vs. "Proposed self-hosted setup" (line 12)
*Anchor:* "Volume-based overage in the last two quarters added a further $18,000"
*Problem:* The memo cites two consecutive quarters of overage as evidence of growing volume,
then models 40 TB storage and 18 TB/month egress as static for a three-year commitment.

This is internally inconsistent, and the inconsistency is asymmetric in a way that favours the
recommendation: under the vendor, growth is capped by contract; self-hosted, growth flows
straight into storage and egress lines with no ceiling. Storage in particular compounds if
retention is cumulative. There is no sensitivity analysis, no growth rate, and no
break-even volume at which the two options converge.

**M5 — Recurring cost categories are missing from the self-hosted side**
*Location:* "Proposed self-hosted setup" (line 12) and the Annual cost table
*Anchor:* "Storage is 40 TB on gp3 at $0.023 per GB-month."
*Problem:* The build side omits several categories that a managed vendor bundles into its
price, so the two sides of the comparison are not like-for-like.

Not costed anywhere:

- **Backup, replication, and disaster recovery.** Six instances and 40 TB with no stated
  redundancy factor, no snapshot storage, and no DR provision. For an ingestion system
  replacing a managed vendor this is the most significant omission in this group.
- **Cross-AZ and inter-instance data transfer**, which is billed separately from internet
  egress and is non-trivial for a six-node ingestion cluster.
- **AWS support plan**, which for a production workload of this size is typically a
  percentage of spend.
- **gp3 provisioned IOPS and throughput above the included baseline**, which an ingestion
  workload at 40 TB will very likely require.
- **Load balancing / networking components.**

### MINOR

**mi1 — The monitoring and tooling figure appears only in the table**
*Location:* Annual cost table (line 24), vs. "Proposed self-hosted setup"
*Anchor:* "| Monitoring and tooling | $14,000 |"
*Problem:* Every other line in the table traces back to a stated assumption in the setup
section; this one is asserted without any basis, unit, or vendor.

**mi2 — Two different dates are both presented as the contract deadline**
*Location:* "Current spend" (line 8) and "Conclusion" (line 31)
*Anchor:* "before the 1 October renewal deadline"
*Problem:* The memo states the contract "renews 1 December 2026" but later calls 1 October
the "renewal deadline," and gives no year for 1 October.

The charitable reading is a two-month notice period ending 1 October ahead of a 1 December
renewal, which is plausible — but the memo asks the reader to take an irreversible action
against this date and should not require the reader to infer it. State the notice period and
the contractual clause explicitly.

**mi3 — Instance count is asserted with no capacity rationale**
*Location:* "Proposed self-hosted setup" (line 12)
*Anchor:* "Six `c6i.4xlarge` instances on three-year reserved pricing"
*Problem:* Nothing ties six instances of this size to the measured ingestion workload, so the
largest infrastructure line cannot be checked by a reviewer.

**mi4 — No region or price-list date, and the reserved rate looks high for a three-year term**
*Location:* "Proposed self-hosted setup" (line 12)
*Anchor:* "three-year reserved pricing at $4,730 each per year"
*Problem:* No AWS region or pricing-as-of date is cited, and $4,730/year works out to roughly
$0.54/hour — only about 20% below c6i.4xlarge on-demand, whereas three-year reserved terms
normally land closer to 50–60% below.

Flagging this to verify rather than as a confirmed error, and the direction is conservative
(it overstates self-hosted cost, so correcting it would strengthen the recommendation). But
the rate should be re-derived from a current price list with the region and purchase option
named, because $0.023/GB-month gp3 and $0.09/GB egress are also region-specific and none of
the three prices is sourced.

---

## Summary

| Severity | Count |
|---|---|
| Critical | 4 |
| Major | 5 |
| Minor | 4 |

**Required before this goes to the architecture review:**

1. Fix the storage annualization and the total (C1, C2), and restate the conclusion with the
   corrected $47,140 / 22% figure.
2. Cost the migration explicitly, with headcount, and replace "payback is immediate" with a
   real payback period (C3).
3. Rebuild the timeline so the replacement is proven before Streamvault is terminated, or
   defer the notice decision by one renewal cycle (C4).
4. Justify or sensitivity-test the 0.5 FTE assumption, and state plainly that 1.0 FTE reverses
   the recommendation (M1).
5. Restate the baseline against the new contract's actual price (M2).

Items C1, C2, and C3 all move the answer the same direction as the stated recommendation. That
does not imply intent, but it does mean the corrected model should be re-derived independently
rather than patched line by line.
