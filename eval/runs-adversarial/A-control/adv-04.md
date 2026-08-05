# Expert review — RFC 214, Sunsetting the Settlements API v2

Artifact: `artifacts-adversarial/adv-04-deprecation-rfc.md`
One review pass. 12 findings: 3 critical, 6 major, 3 minor.

## Overall assessment

The RFC is well-organised and unusually honest about gaps (it names the PDF, `check`,
and XML shortfalls rather than hiding them). The comms cadence, brownout ramp, and
extension policy are competently designed, and the dates check out arithmetically —
2027-06-15, 2027-07-20 and 2027-08-17 really are Tuesdays, the 14:00 UTC brownout
windows really do miss Meridian's 02:00–05:00 batch even at 8 hours, `Sunset: Wed, 01
Sep 2027` really is a Wednesday, and 341 + 2 = 343 reconciles with the mailing count.

The problems are not in the presentation. They are in three load-bearing claims that
the document asserts confidently and that do not survive contact with facts stated
elsewhere in the same document: the contractual notice clock, the cursor's ability to
replace `updated_since`, and the rate-limit budget for the mandated soak. Each is
internally contradicted by text in another section. All three break the decision the
Council is being asked to make.

---

## Critical

### C1 — The §7.3 notice clock cannot start on 2026-09-01, so the proposed sunset date is unlawful under the MSA

**Location:** §3 Contractual constraints, read against §7 Timeline
**Anchor:** *"The notice period shall not commence until a generally available replacement offering equivalent functionality has been made available to Customer."*

**Problem:** §7 places v3 GA at 2026-11-02, so under the clause's own commencement
condition the twelve-month clock for the two Enterprise MSA accounts cannot start
before 2026-11-02, making the earliest lawful removal 2027-11-02 — 62 days after the
proposed 2027-09-01 sunset.

The RFC's counter-assertion — *"Our proposed sunset sits twelve months after notice,
which clears the §7.3 bar"* — measures from notice *publication* (2026-09-01) and
silently ignores the second sentence of the clause it just quoted. Publishing notice
and commencing the notice period are two different events, and §7.3 explicitly
decouples them. On 2026-09-01 v3 has been in *public beta* since 2026-02-16; a public
beta is not a "generally available replacement." The RFC's own timeline row is the
evidence against it.

Two consequences the RFC does not confront:

1. **The stated rationale collapses.** §2 justifies the whole exercise by PG 11 vendor
   extended support ending 2027-10-31. A corrected sunset of 2027-11-02 puts v2 still
   serving from `settle_pg` past the support cliff, and pushes decommission (currently
   2027-10-15) into unpatched territory. The RFC's claim that the date *"still leaves
   room to decommission `settle_pg` before support lapses"* is false once the clock is
   computed correctly.
2. **The knock-on dates all move.** A 2027-11-02+ sunset pushes the 30-day extension
   ceiling (currently capped at 2027-10-01) and the brownout ramp, and brings the
   window within reach of Halcyon's 1 Dec – 15 Jan freeze.

There is also a live argument that "equivalent functionality" is not met even at GA —
see C2. If v3 cannot reproduce `updated_since` semantics, an Enterprise customer can
credibly argue the clock never started at all.

The Council cannot approve 2027-09-01 as drafted. Either the sunset moves to
2027-11-02 or later (and §2's PG 11 rationale must be re-planned, e.g. by isolating or
migrating `settle_pg` independently of the API sunset), or v3 GA is pulled forward to
on/before 2026-09-01 so notice and commencement coincide.

---

### C2 — A `created_at`-ordered cursor cannot reproduce `updated_since`, so both Enterprise reconciliations will silently lose adjustments

**Location:** §6 Migration path, migration table row 1, read against §5 and §8
**Anchor:** *"Mechanically equivalent. Persist the cursor instead of a timestamp; nothing else changes."*

**Problem:** §8 states the cursor is *"an opaque offset into an append-only index
ordered by `created_at`"*, which by construction can only surface newly-created rows,
whereas §4 states `updated_since=T` *"returns every record whose state changed after
T"* — so every post-settlement mutation to an already-created transaction falls behind
the cursor and is never returned.

This is not a nuance; it is the entire reconciliation use case. Chain the three facts
the RFC itself supplies:

- §5: adjustments (chargebacks, interchange corrections, fee true-ups) *"continue to
  mutate `status` and `net_amount` on the parent transaction rather than landing as
  separate offsetting entries"*, and *"Adjustments arrive up to 45 days after the
  original transaction."*
- §8: the v3 cursor advances over an append-only index **ordered by `created_at`**.
- A mutation does not change `created_at`. The parent row's position in that index is
  fixed at creation and is already behind any cursor the client holds.

Therefore a v3 client polling by cursor receives new transactions and **never** sees
the adjustment that later changes a 30-day-old transaction's `status` and
`net_amount`. §4 says both Enterprise accounts — 80% of v2 traffic — drive
reconciliation off exactly this endpoint. The failure mode is silent: no error, no gap
in the stream, just settlement totals that quietly stop matching, for up to 45 days of
tail per transaction.

The RFC presents the one-row-per-transaction model in §5 as a feature integrators
asked for. Combined with a `created_at` cursor it is precisely the thing that makes the
migration lossy, and §6 asserts the opposite without reconciling the two sections.

Either v3 must expose an update-ordered feed (a cursor over an `updated_at` /
change-log index, or a retained `updated_since` parameter), or the RFC must state
plainly that reconciliation clients need a redesigned re-scan strategy — which is a
substantial integrator work item, not *"nothing else changes"*, and which materially
weakens the "equivalent functionality" position in C1.

---

### C3 — The mandated dual-read soak exceeds Meridian's rate limit and will throttle their production traffic

**Location:** §6 Migration path, read against §8 Rollout mechanics and §4
**Anchor:** *"v2 and v3 draw on the same per-account quota — 600 req/min, enforced at the edge before version routing"*

**Problem:** §6 requires accounts above 10 req/min to *"mirror 100% of their v2 read
traffic to v3 for a two-week soak"*, but §4 records Meridian at a peak sustained 450
req/min on v2 — so the soak demands 900 req/min against a 600 req/min ceiling that §8
says will not be raised.

Because the quota is *"enforced at the edge before version routing"*, the overage does
not politely shed the mirrored test traffic. The edge sees one account at 900 req/min
and throttles indiscriminately — roughly a third of requests rejected, hitting v2 and
v3 alike. That means Meridian's **production** nightly reconciliation batch
(02:00–05:00 UTC per §4) takes 429s for two weeks, caused by a procedure this RFC
instructs them to run.

The RFC closes the door on the fix in the next sentence: *"We are not raising quotas
for the migration."* As written, §6 and §8 are mutually unsatisfiable for the account
representing 62% of v2 traffic, and Halcyon at 18% may be close to the same wall
depending on its peak (which §4 does not give — see also the missing peak figure for
Halcyon).

Resolve by one of: a migration-scoped quota uplift (600 → at least 1000 for accounts
in soak), exempting mirrored v3 traffic from the shared counter, or replacing the 100%
mirror with a sampled diff (e.g. 10–20%) for the highest-volume accounts. Whichever is
chosen, §6 and §8 must agree.

---

## Major

### M1 — Legal's sign-off covers notice *delivery*, and the RFC extends it to notice *commencement*

**Location:** §3 Contractual constraints
**Anchor:** *"confirmed it satisfies the service requirement in §7.3"*

**Problem:** The described legal review addresses the mechanism for serving notice
(changelog plus email to the technical contact of record) and the impossibility of
unilateral shortening, but the RFC then leans on that same review to support the date
arithmetic in C1, which Legal is not reported to have examined. The Council should not
read a delivery-mechanism opinion as a date opinion; the notice-commencement question
needs to go back to Legal explicitly.

### M2 — A two-week soak cannot validate against a 45-day adjustment tail

**Location:** §6 Migration path
**Anchor:** *"mirror 100% of their v2 read traffic to v3 for a two-week soak and diff the responses"*

**Problem:** §5 states adjustments arrive up to 45 days after the original
transaction, so a 14-day diff window observes at best a third of the adjustment
distribution and can return clean while the divergence in C2 is fully present. The
soak as specified is capable of producing a false pass on the exact defect it exists
to catch; it needs to run at least one full 45-day adjustment cycle, or explicitly
replay historical adjustment-bearing transactions rather than relying on live traffic.

### M3 — The 15-minute rollback assumes `settle_pg` stays current, which nothing in the RFC commits to

**Location:** §9 Comms, exceptions, rollback, read against §2
**Anchor:** *"The sunset is a config flag. Reverting restores v2 in under 15 minutes; we hold the flag and the code path until 2027-10-01."*

**Problem:** Restoring v2 only helps if `settle_pg` still holds current data, and §2
establishes only that dual-writes have run *"since 2025-11"* — the RFC never states
that dual-writes are maintained through the 2027-09-01 → 2027-10-01 rollback window.
If dual-writes stop at sunset (the natural assumption, since v2 is then dark), flipping
the flag back restores an API silently serving stale settlement data to financial
customers, which is materially worse than the outage it is meant to remedy. The RFC
must commit explicitly to keeping dual-writes at 100% until the flag and code path are
retired, and should state the maximum staleness a revert can introduce.

### M4 — No cursor bootstrap or re-anchor path is defined

**Location:** §8 Rollout mechanics
**Anchor:** *"Clients must persist cursors across their own deploys."*

**Problem:** The RFC imposes a hard durability requirement on clients but specifies no
recovery when it is violated — with `updated_since=T` a client that lost its state
simply picked a timestamp and re-read, whereas an opaque cursor offers no documented
way to re-anchor at a known point. The migration guide needs to state, at minimum: how
to obtain an initial cursor, whether cursors expire, and how a client that has lost its
cursor resumes without either re-reading all history or skipping records. This is a
predictable day-one support burden across 343 accounts.

### M5 — The `fees[]` → `fee_breakdown` conversion rests on an unevidenced claim, and is lossy if the claim is wrong

**Location:** §6 Migration path, migration table row 2
**Anchor:** *"Codes identical; duplicate codes were already impossible in v2."*

**Problem:** Flattening an array into an object keyed by fee code is lossless only if
no code ever repeats, and that precondition is asserted without a source, without a
stated validation against historical rows, and in tension with §5's description of fee
true-ups and interchange corrections mutating transactions post-settlement. §5 also
demonstrates that historical rows carry shapes no longer producible today (the
retired `payout_method=check`), which is exactly the case where a "this was always
impossible" invariant tends to fail. If a duplicate code exists anywhere in history,
the object form silently drops one entry and fee totals diverge with no error. Run the
uniqueness check across the full v2 history and cite the result before shipping the
mapping. Note also that the array→object change discards ordering, which the RFC does
not mention.

### M6 — The Council is asked to approve a notice text that the RFC does not contain

**Location:** Header, "Decision requested"
**Anchor:** *"Decision requested: approve the sunset date and the notice text."*

**Problem:** Half of the requested decision has no corresponding artifact — the notice
text appears nowhere in the document, in an appendix, or as a linked reference (§6
mentions only that the field mapping *"ships with the notice"*, and §9 describes
channels and cadence, not wording). The Council can act on the date, but cannot approve
text it has not seen; the notice draft needs to be attached before this item is
decidable.

---

## Minor

### mi1 — The comms schedule's reference point `T` is self-contradictory

**Location:** §9 Comms, exceptions, rollback
**Anchor:** *"Notice email, changelog post, console banner and response headers at T-0; reminders at T-6, T-3, T-1 month and T-2 weeks."*

**Problem:** The reminders count backwards from the sunset (T-1 month = 2027-08-01,
consistent with the outbound-call trigger), but the notice is placed at T-0, which
under that same reading would put notice on sunset day rather than twelve months
earlier. Intent is inferable, but whoever builds the comms calendar has to guess; state
the anchor explicitly (notice at S-12 months, reminders at S-6/S-3/S-1 month, S-2
weeks).

### mi2 — "Opaque offset" is the one cursor design that re-sharding does invalidate

**Location:** §8 Rollout mechanics
**Anchor:** *"Cursors stay valid through our re-shards because the cursor is an opaque offset into an append-only index ordered by `created_at`."*

**Problem:** The sentence offers "it is an offset" as the *reason* for re-shard
durability, but a positional offset into an index is precisely what shifts when data is
redistributed across shards — durable cursors normally encode a sort key plus tiebreak
(e.g. `created_at` + id), not a position. Either the wording is loose and the cursor
actually encodes a key (in which case say so), or the durability claim is wrong and
every client's cursor breaks at the next re-shard. Given that the entire migration
hangs on cursor durability, the mechanism should be stated rather than asserted.

### mi3 — Success metrics have no owner, gate, or consequence

**Location:** §9, Success metrics
**Anchor:** *"v2 below 1% of settlements traffic by 2027-06-01; zero Enterprise v2 traffic by 2027-07-01"*

**Problem:** The thresholds are sensible but nothing states who evaluates them, at
what checkpoint, or what happens if they are missed — there is no defined go/no-go
before flipping to `410 Gone`, and no abort criterion tied to the brownout results even
though the brownouts exist to surface exactly that signal. Name the decision point
(e.g. Council review at 2027-07-15), the owner, and the action if a metric is red.

---

## Not flagged (checked and sound)

- Brownout dates 2027-06-15 / 07-20 / 08-17 are all Tuesdays; 14:00 UTC + 8h ends 22:00
  UTC and does not touch Meridian's 02:00–05:00 batch.
- `Sunset: Wed, 01 Sep 2027 00:00:00 GMT` — 2027-09-01 is a Wednesday; format matches
  RFC 8594.
- Account arithmetic: 341 + 2 = 343 (matches the mailing count); 62% + 18% + 20% = 100%.
- Halcyon's cutover (2027-02-09) correctly clears the 1 Dec – 15 Jan freeze.
- Extension ceiling (2027-10-01) is consistent with sunset + 30 days and with the
  rollback code-path retention date — under the *drafted* dates. It does not survive C1.
- The PDF statement gap is closed 2026-10-01, ahead of the stated GA date.
- The XML and `payout_method=check` gaps are disclosed rather than concealed, with
  named remediation.

## Totals

critical 3 · major 6 · minor 3
