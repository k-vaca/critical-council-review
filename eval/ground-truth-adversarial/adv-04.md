# Ground truth — adv-04-deprecation-rfc.md (RFC 214, Settlements API v2 sunset)

Three planted defects. Everything else in the artifact is intended to be sound.

---

## Defect 1 — Cursor migration silently drops post-settlement adjustments

- **Severity**: critical

- **Location**: §6 Migration path, first row of the mapping table (`GET /v2/transactions?updated_since=T` → `GET /v3/transactions?cursor=<last_cursor>`, "Mechanically equivalent... nothing else changes"). Supporting facts in §4 (last line), §5 (first paragraph), §8 (first paragraph).

- **The defect**: The document asserts that replacing the `updated_since=T` filter with a `cursor` is a mechanically equivalent, one-line change. It is not. `updated_since` returns every record whose **state changed** after `T`; the v3 cursor is "an opaque offset into an append-only index ordered by `created_at`" (§8). Adjustments in v3 "mutate `status` and `net_amount` on the parent transaction rather than landing as separate offsetting entries" (§5) — so a mutated row does not get a new `created_at` and does not reappear later in the cursor stream. Any consumer that has already advanced its cursor past a transaction will **never** see a chargeback, interchange correction, or fee true-up applied to it. Both named Enterprise accounts drive reconciliation off exactly this call (§4), and adjustments arrive up to 45 days after the original transaction (§5). Following the migration guidance as written produces silently under-reported settlement totals.

- **Why it is real**: Three of the document's own statements are jointly contradictory with the "mechanically equivalent" claim: (a) §4, "which returns every record whose state changed after `T`"; (b) §5, adjustments mutate the parent row in place, up to 45 days later; (c) §8, the cursor is an offset into an append-only index ordered by `created_at`. Append-only + ordered by creation time means an in-place mutation never re-enters the stream behind an already-advanced cursor. The migration table promises equivalence anyway. The two-week soak in §6 does not rescue this: it is far shorter than the 45-day adjustment window and it diffs point-in-time responses rather than longitudinal cursor coverage.

- **Why I expect a reviewer to miss it**: The three facts are deliberately scattered across three sections and each reads as reassuring in isolation — the mutate-in-place line is framed as a *feature* integrators requested, and the append-only line appears inside a paragraph about cursor stability across re-shards, which reads as a robustness guarantee rather than a semantic constraint. Reviewers also tend to audit a migration table for *field* coverage (names, types, units) rather than for *delivery semantics* of the collection endpoint, and §5 already presents a candid "three things v3 does not cover" list, which invites the reviewer to treat the coverage-gap analysis as done.

---

## Defect 2 — Sunset date breaches MSA §7.3 because the notice clock cannot start until v3 is GA

- **Severity**: major

- **Location**: §3 Contractual constraints (quoted §7.3 and the sentence "Our proposed sunset sits twelve months after notice, which clears the §7.3 bar..."), read against §7 Timeline (notice 2026-09-01; v3 GA 2026-11-02; `410 Gone` 2027-09-01).

- **The defect**: §7.3 says the twelve-month notice period "shall not commence until a generally available replacement offering equivalent functionality has been made available to Customer." v3 does not reach GA until **2026-11-02** (§7). The clock therefore starts 2026-11-02, not at the 2026-09-01 notice, and the earliest contractually permitted removal is **2027-11-02**. The RFC schedules `410 Gone` for **2027-09-01** — roughly two months early — for the two accounts the clause covers (Meridian Clearing and Halcyon Bank, 80% of v2 traffic). The `Sunset` header value published to customers on 2026-09-01 is therefore a date the company is not entitled to enforce. The escape hatch in §9 does not close the gap: the maximum extension is 30 days and "no extension runs past 2027-10-01," still short of 2027-11-02.

- **Why it is real**: Every governing fact is stated in the artifact: the commencement clause (§3), the GA date (§7), the sunset date (§7 and §1), the max extension (§9). It is also consequential rather than cosmetic — the compliant date, 2027-11-02, collides with the `settle_pg` extended-support expiry of 2027-10-31 stated in §2, so the whole plan needs re-planning, not a date edit.

- **Why I expect a reviewer to miss it**: The document performs the arithmetic the reviewer is primed to check — 2026-09-01 to 2027-09-01 is exactly twelve months — and immediately reports Legal sign-off, so the box gets ticked and attention moves on. The Legal sentence is scoped narrowly to the *service* mechanism (changelog + email), which is a different requirement from *commencement*; reviewers read it as blanket legal approval. And GA is presented in the timeline as a product milestone among cutover dates, not as the contractual trigger it is, so nobody re-derives the clock from it.

---

## Defect 3 — Mandated 100% traffic mirroring exceeds the shared rate limit for the largest consumer

- **Severity**: major

- **Location**: §6 Migration path (mirror 100% of v2 read traffic for a two-week soak), read against §4 (Meridian Clearing peak sustained 450 req/min of reads against `/v2/transactions`) and §8 (v2 and v3 share one 600 req/min per-account quota, enforced at the edge before version routing, not being raised).

- **The defect**: The prescribed migration procedure is arithmetically impossible for the largest consumer. Meridian sustains 450 req/min of v2 reads at peak; mirroring 100% of that to v3 makes 900 req/min against a shared per-account ceiling of 600 req/min that the RFC explicitly declines to raise. Meridian will be throttled by roughly a third during the soak — and because the quota is shared and enforced before version routing, the throttling hits their **production** v2 reconciliation traffic, not just the shadow copy. The same math breaks any account sustaining more than 300 req/min. A reviewer who identifies the Meridian collision has found this defect; naming other accounts is not required.

- **Why it is real**: Both numbers and the mirroring instruction are stated explicitly, and §8 forecloses the obvious mitigation in the same breath ("We are not raising quotas for the migration"). 450 × 2 > 600 is not arguable. §8 also specifies enforcement happens "before version routing," which rules out the defense that only v3 calls would be shed.

- **Why I expect a reviewer to miss it**: The numbers live three sections apart and each is individually unremarkable — 600 rpm reads as a generous ceiling, 450 rpm reads as a volume statistic in a consumer table, and the mirroring ask reads as diligence. The quota sentence is framed as an anti-abuse control ("migration cannot be used to escape rate limits"), which makes it feel like a policy note rather than a capacity constraint, so reviewers file it under governance and never multiply. Reviewers also concentrate their rollout-mechanics scrutiny on the brownout schedule, which the document has visibly and correctly de-conflicted with Meridian's 02:00–05:00 batch — spending the reviewer's "does the rollout break a named consumer?" budget on a question that checks out.

---

## Intentionally sound (do not credit as findings)

Notice mechanism and channels; reminder cadence; `Deprecation`/`Sunset` headers; rollback flag with stated restore time and retention window; exception process with owner and criteria; disclosed coverage gaps (PDF statements, `payout_method=check`, XML) each with a remedy; brownouts de-conflicted with Meridian's batch window and scheduled outside Halcyon's 1 Dec – 15 Jan freeze; Halcyon cutover placed after that freeze; success metrics; account counts (2 + 341 = 343) and volume shares (62 + 18 + 20 = 100) reconcile; `Sunset: Wed, 01 Sep 2027` is a correct day-of-week; decommission 2027-10-15 sits before support expiry 2027-10-31 and after the 2027-10-01 rollback window closes.
