# Build vs buy: replacing Streamvault with self-hosted ingestion

**Prepared for:** the September architecture review
**Recommendation:** move off Streamvault and self-host.

## Current spend

Streamvault invoices us **$210,000 per year** on the current contract, which renews 1 December 2026. Volume-based overage in the last two quarters added a further $18,000, which we have excluded here because the new contract caps it.

## Proposed self-hosted setup

Six `c6i.4xlarge` instances on three-year reserved pricing at $4,730 each per year. Storage is 40 TB on gp3 at $0.023 per GB-month. Egress runs about 18 TB a month at $0.09 per GB. We would need half an engineer to run it, costed at a fully loaded $180,000 FTE.

Migration itself is roughly four months of engineering time.

## Annual cost

| Line | Annual cost |
|---|---|
| Compute (6 × c6i.4xlarge, reserved) | $28,380 |
| Storage (40 TB, gp3) | $920 |
| Data transfer (18 TB/month egress) | $19,440 |
| Engineering (0.5 FTE) | $90,000 |
| Monitoring and tooling | $14,000 |
| **Total** | **$138,740** |

## Conclusion

Self-hosting costs **$138,740** a year against Streamvault's **$210,000**, a saving of **$71,260** a year, or 34%. Payback is immediate because there is no capital outlay on reserved instances beyond the first invoice.

We recommend giving notice on the Streamvault contract before the 1 October renewal deadline and starting the migration in Q4.
