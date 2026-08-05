# RFC 214 — Sunsetting the Settlements API v2

**Author:** R. Okafor, Platform APIs · **Status:** Draft for API Council review · **Date:** 2026-08-10
**Decision requested:** approve the sunset date and the notice text.

## 1. Summary

Retire `/v2/settlements` and `/v2/transactions`, replacing them with the v3 Settlements API. Proposed sunset: **2027-09-01**, with notice served **2026-09-01**.

## 2. Why now

v2 reads are served from `settle_pg`, a Postgres 11 cluster with no in-place upgrade path (the v2 schema depends on two extensions dropped in PG 12). Vendor extended support ends **2027-10-31**; after that we run unpatched. The v3 store has been the write path of record since 2025-11 with dual-writes at 100%, so v2 is pure read-side legacy carrying ~40% of the settlements on-call load.

## 3. Contractual constraints

Two accounts sit on the 2024 Enterprise MSA. §7.3 reads: *"Provider shall give no less than twelve (12) months' written notice prior to the removal of any Generally Available API. The notice period shall not commence until a generally available replacement offering equivalent functionality has been made available to Customer."* Everyone else is on the standard ToS, which requires 90 days.

Legal has reviewed the notice mechanism — publication to the developer changelog plus email to each account's technical contact of record — and confirmed it satisfies the service requirement in §7.3. They have also confirmed we cannot shorten §7.3 by a unilateral ToS update. Our proposed sunset sits twelve months after notice, which clears the §7.3 bar and still leaves room to decommission `settle_pg` before support lapses.

## 4. Who consumes v2

| Account | Share of v2 requests | Notes |
|---|---|---|
| Meridian Clearing | 62% | Enterprise MSA. Peak sustained **450 req/min** of reads against `/v2/transactions`. Nightly reconciliation batch 02:00–05:00 UTC. |
| Halcyon Bank | 18% | Enterprise MSA. Annual change freeze 1 Dec – 15 Jan. |
| 341 self-serve accounts | 20% combined | Median 4 req/min. 60 have made no successful call in 90 days. |

Both Enterprise accounts drive reconciliation off `GET /v2/transactions?updated_since=T`, which returns every record whose state changed after `T`.

## 5. What v3 covers, and what it does not

v3 keeps the one-row-per-transaction model integrators asked for in the 2025 survey: post-settlement adjustments (chargebacks, interchange corrections, fee true-ups) continue to mutate `status` and `net_amount` on the parent transaction rather than landing as separate offsetting entries. Adjustments arrive up to 45 days after the original transaction.

Three things v3 does not cover today:

1. **PDF statements.** `GET /v2/settlements/{id}/statement.pdf` has no v3 equivalent. We will expose the same renderer at `/v3/settlements/{id}/statement.pdf` on **2026-10-01**, ahead of GA.
2. **`payout_method=check`**, retired in 2024 but still on historical rows. v3 returns `other`; called out in the field mapping.
3. **XML responses** — 0.2% of v2 traffic across three self-serve accounts. v3 is JSON only. Those three get direct outreach in September.

## 6. Migration path

The full field mapping ships with the notice. Two changes matter:

| v2 | v3 | Note |
|---|---|---|
| `GET /v2/transactions?updated_since=T` | `GET /v3/transactions?cursor=<last_cursor>` | Mechanically equivalent. Persist the cursor instead of a timestamp; nothing else changes. |
| `settlement.fees[]` (array) | `settlement.fee_breakdown` (object keyed by fee code) | Codes identical; duplicate codes were already impossible in v2. |

We ask every account above 10 req/min to mirror **100% of their v2 read traffic** to v3 for a two-week soak and diff the responses; our SDKs ship a `dual_read` helper that does exactly this. Meridian and Halcyon each get a named engineer for the soak.

## 7. Timeline

| Date | Milestone |
|---|---|
| 2026-09-01 | Notice published + emailed to all 343 accounts. `Deprecation` and `Sunset: Wed, 01 Sep 2027 00:00:00 GMT` headers enabled on every v2 response |
| 2026-10-01 | `/v3/settlements/{id}/statement.pdf` ships |
| 2026-11-02 | **v3 reaches GA** (public beta since 2026-02-16; 47 accounts have exercised it) |
| 2027-02-09 | Halcyon assisted cutover — deliberately after their freeze ends |
| 2027-04-30 | Meridian assisted cutover |
| 2027-06-15 / 07-20 / 08-17 | Brownouts, all Tuesdays from 14:00 UTC: 1h, then 4h, then 8h. Chosen to miss Meridian's 02:00–05:00 batch |
| 2027-09-01 | v2 returns `410 Gone` |
| 2027-10-15 | `settle_pg` decommissioned |

## 8. Rollout mechanics

Clients must persist cursors across their own deploys. Cursors stay valid through our re-shards because the cursor is an opaque offset into an append-only index ordered by `created_at`.

v2 and v3 draw on the same per-account quota — 600 req/min, enforced at the edge before version routing — so migration cannot be used to escape rate limits. We are not raising quotas for the migration.

Per-account v2 dashboards go to account teams weekly from notice.

## 9. Comms, exceptions, rollback

Notice email, changelog post, console banner and response headers at T-0; reminders at T-6, T-3, T-1 month and T-2 weeks. Self-serve accounts still on v2 at T-1 month get an outbound call from support.

Any account may request one 30-day extension, approved by the API Council with the account team and conditional on a written cutover plan. No extension runs past 2027-10-01.

The sunset is a config flag. Reverting restores v2 in under 15 minutes; we hold the flag and the code path until 2027-10-01.

**Success metrics:** v2 below 1% of settlements traffic by 2027-06-01; zero Enterprise v2 traffic by 2027-07-01; no v3 5xx regression above our 0.1% error budget during any brownout.
