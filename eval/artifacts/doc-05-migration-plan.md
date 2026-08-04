# Plan: move `orders` from MySQL to Postgres

**Goal:** cut over the orders service to Postgres with no more than 5 minutes of write downtime.
**Window:** Saturday 12 September 2026, 01:00–05:00 UTC.
**Owner:** payments platform.

## Constraints

- The orders table is 1.4 TB and takes roughly 90 minutes to dump and restore at current sizes.
- `orders` is written by the checkout service and read by fulfilment, support tooling, and the finance export.
- The finance export runs at 03:00 UTC daily and must not be skipped; a missed or incomplete export triggers a manual reconciliation that takes finance two days.

## Tasks

| ID | Task | Depends on | Estimate |
|---|---|---|---|
| A | Provision the Postgres cluster and apply the schema | — | 45 min |
| B | Start logical replication from MySQL into Postgres | A | 20 min |
| C | Cut over the checkout service to write to Postgres | E | 10 min |
| D | Repoint fulfilment and support tooling reads to Postgres | C | 15 min |
| E | Verify row counts and checksums match between the two databases | C | 40 min |
| F | Repoint the finance export to Postgres | D | 15 min |
| G | Decommission the MySQL cluster | F | 30 min |

## Sequence on the night

1. 01:00 — run A and B.
2. 02:15 — pause checkout writes.
3. 02:20 — run C.
4. 02:30 — run D and E.
5. 03:15 — run F.
6. 03:30 — declare the cutover complete and resume normal monitoring.
7. Following Saturday — run G.

## Rollback

If checksums do not match at E, stop and page the payments lead.

## Success criteria

- Write downtime under 5 minutes.
- Row counts identical across both databases at cutover.
- The finance export completes on Sunday 13 September without manual intervention.
