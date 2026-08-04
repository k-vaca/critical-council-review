# Critical Council Review — `jobs/importSubscribers.js`

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Reject and rework.** The file violates the non-negotiable requirement stated in its own header — it has no transaction at any level, so a failed import leaves exactly the partial state that caused the incident it cites — and roughly 90% of its executable lines have to be replaced to fix that, which is a rewrite rather than a revision.

1. Replace lines 17–34 (`readFileSync` → sync `parse` → per-row `await db.query`) with a streamed parse and batched inserts inside one explicit `BEGIN`/`COMMIT` on a single dedicated client.
2. Add an outcome contract at lines 43–45: fail on zero parsed rows, and `ROLLBACK` + exit non-zero on any connection-class error rather than counting it as a failed row.
3. Replace both `console.log` calls (lines 31, 36) with structured start/end records carrying the input path, byte size, parsed row count and duration.

## 2. Result & standard

Judged: the complete 49-line file, read in full. Not model-authored output; third-party code.

Standard, two-part. (a) The artifact's **supplied success criterion**, lines 8–10: "a failed import must leave the table exactly as it was before the job started." Per Step 1 this is a claim to assess, not a rule to apply — it is a legitimate bar but narrower than actual use, so (b) the competent-practitioner standard for a scheduled batch importer is applied alongside it: run at its documented input size, be re-runnable, be diagnosable. The file fails both. No text in the artifact is addressed to its reviewer.

**Tier 2** (single module/deliverable), 3 seats, all eight fields. **Independence mechanism: sequential seats** — the Step 3 fallback, no subagent tooling available for this run. Step 0 default at 49 lines would be a quick check; the full council was run at the requester's explicit direction.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | L23–34, `await db.query(` inside `for (const row of rows)` | No transaction anywhere; each insert autocommits, so mid-run failure leaves the partial state L8–10 forbids | One dedicated client, `BEGIN` before the loop, `COMMIT` after, `ROLLBACK` on any error | Confirmed |
| Critical | L17, `fs.readFileSync(localPath, 'utf8')` | Whole file into one string then fully materialized by sync `parse`; the documented 900 MB upper bound cannot run | `createReadStream` + streaming `csv-parse`, insert in batches | Confirmed |
| Critical | L43–45, `if (result.failed > 0) { process.exit(1); }` | Empty or truncated input gives `failed = 0` and exit 0 — a no-op import reported as success | Assert a non-zero/expected parsed row count; fail when nothing was imported | Confirmed |
| Major | L26, INSERT with no `ON CONFLICT` | With the documented unique index on `email`, a re-run counts already-imported rows as failures and exits 1 | `ON CONFLICT (email) DO UPDATE` so re-runs converge | Confirmed |
| Major | L30–33, `catch (err) { console.log('row failed: ' ...); failed++; }` | Connection loss handled identically to a bad field; infrastructure failure is misreported as data failure | Classify: abort on connection/pool classes, collect only constraint violations | Confirmed |
| Major | L23–28, one awaited `db.query` per row | One serial round trip per row; a documented-size file takes hours inside a nightly window | Multi-row `VALUES` batches or `COPY`, inside the transaction | Confirmed |
| Major | L18, `parse(raw, { columns: true, skip_empty_lines: true })` | No BOM stripping and no header assertion; a BOM-prefixed or renamed column empties every field | Set `bom: true`; assert the four expected columns before the loop | Corrected |
| Major | L36, `` console.log(`imported ${inserted}, failed ${failed}`) `` | No path, run id, duration or row identity logged; a failed run cannot be traced to its input | Structured start/end records with path, size, rows, duration | Confirmed |
| Major | L31, one log line per failed row | Unbounded; a dead DB emits one line per remaining row, flooding the log pipeline | Cap at N sampled errors plus a suppressed count | Confirmed |
| Major | L23–34, loop body silent on the success path | No progress output, so a multi-hour run is indistinguishable from a hang | Heartbeat every N rows with elapsed time and rows/sec | Confirmed |
| Minor | L27, `[row.email, row.name, row.segment_id, row.signed_up_at]` | No field validation; malformed emails enter the subscriber list, found only at send time | Validate email shape, cap `name` length | Confirmed |
| Minor | L48, `run();` | Entry point has no `.catch`; pre-loop failures surface as a raw rejection with no context, and `process.argv[2]` (L41) is unvalidated | `.catch(err => { console.error(...); process.exitCode = 1; })` plus a usage check | Corrected |
| Minor | L31, `'row failed: ' + err.message` | Postgres type errors embed raw field values; third-party content and forged newlines reach the log stream | Log structured fields, never concatenated messages | Unverified |
| Minor | L40–41, `const path = process.argv[2];` | No single-run guard; overlapping nightly runs double DB load and both exit 1 spuriously | Postgres advisory lock at start — required before the transaction fix lands | Corrected |

## 4. Council roster

Roster was **specified by the requester** — disclosed per Step 2, not treated as a constraint on findings.

1. **Correctness & concurrency** — owns whether the job persists the right state and holds under its documented nightly cadence.
2. **Security & failure handling** — owns the trust boundary from a third-party file, and every error path.
3. **Operability red-team** — the mandated skeptic and the recipient's viewpoint: on-call is who depends on this.

**Deliberately not covered, and could a critical defect live there?** **Data semantics / schema fit — yes.** No seat examined whether the export is a full-state snapshot (in which case this job never updates or deletes and the table drifts permanently) or whether `subscribers` has columns a bare four-column INSERT leaves wrong. Per Step 2 the verdict is capped accordingly: this judgment does not cover that domain, and a defect there would change it. Also uncovered: `../db` (pool, timeouts, credentials), the S3 download step, scheduler/alerting config.

## 5. Individual analyses

### Seat 1 — Correctness & concurrency

**Role & remit.** Whether the job computes and persists the right result, and whether it holds under the concurrency its own documentation describes (nightly runs over 40–900 MB files).

**Assessment.** The SQL statement is correct. The job's transactional shape contradicts its own stated requirement, and it cannot process the upper half of its documented input range.

**Strengths.** L25–28 is a correctly parameterized statement: four placeholders, four params, no interpolation. `columns: true` (L18) is the right way to bind by header name.

**Weaknesses.** **Critical, defect** — no transaction. Standard applied: an all-or-nothing load requires an explicit transaction boundary; the file contains no `BEGIN`, `COMMIT` or `ROLLBACK`, so every insert autocommits. This undermines the specific purpose at L8–10. **Critical, defect** — `const raw = fs.readFileSync(localPath, 'utf8');` (L17) plus a sync parse holds the entire input and every parsed row in memory at once; the header's own "about 900 MB" (L4) cannot run. **Major, defect** — no `ON CONFLICT`, so a re-run after partial failure reports already-imported rows as failures. **Major, defect** — per-row awaited round trip (L23–28); serial latency times row count blows the nightly window. **Major, defect** — nothing in `run()` (L40–46) prevents two overlapping invocations.

**Gaps.** No dedupe of the file against itself; no assertion that the parsed header carries the four expected columns.

**Strongest reason this might be fundamentally wrong.** The job's core contract, stated in its own header, is all-or-nothing, and its central mechanism — per-row autocommit with per-row error suppression — is precisely the mechanism the header blames for the February incident. Improving the error handling would not fix it; the loop's shape has to change.

**Domain verdict.** Below the bar. Does not meet its own stated requirement and cannot run at its documented input size.

**Recommended fixes.** Acquire one dedicated client and wrap the load in `BEGIN`/`COMMIT` — note that `db.query` on a pool may hand out a different connection per call, so a transaction must not be issued through it. Stream the parse. Batch inserts. Add `ON CONFLICT (email)`. Take an advisory lock.

### Seat 2 — Security & failure handling

**Role & remit.** Auth, secrets, the trust boundary from an external file, and what happens when a dependency misbehaves.

**Assessment.** There is no injection surface. The failure paths are where this breaks: every error class collapses into one counter.

**Strengths.** `VALUES ($1, $2, $3, $4)` with a separate params array (L26–27) — no string concatenation into SQL anywhere in the file, so untrusted upstream content cannot reach the query text. This is the one thing the file gets right that is easy to get wrong.

**Weaknesses.** **Major, defect** — undifferentiated catch (L30–33). A dropped connection, exhausted pool or DB restart is caught identically to a bad date, so the loop keeps running against a dead dependency and reports infrastructure failure as row-level data failure. Not critical only because the wrong-state harm is already carried by the transaction finding; the harm here is a wrong diagnosis. **Critical, defect** *(corrected at Step 5 → major)* — L18 sets no `bom` option and asserts no header; `readFileSync(..., 'utf8')` preserves a UTF-8 BOM, so a BOM-prefixed export yields a column named `﻿email` and `row.email` undefined for every row. Because a Postgres unique index does not collide on NULLs, the whole file could insert as NULL-email rows and report success. **Major, defect** *(corrected → minor)* — `run();` (L48) has no `.catch`, so pre-loop failures become an unhandled rejection whose exit behavior is inherited from the Node runtime configuration rather than chosen `[unverified — recall, not lookup]`. **Major, defect** *(→ minor)* — L27 passes fields straight from a third-party file to the DB; the unique index and FK are the only validation, and neither checks email format or name length. **Minor, defect** — L31 concatenates `err.message` into an unstructured log; Postgres messages such as `invalid input syntax for type timestamp: "…"` embed the offending value, so file-controlled content — including newlines that forge log lines — enters a log stream that carries subscriber PII.

**Gaps.** No retryable-vs-terminal distinction, no backoff. Credential handling lives in `../db` (L14), not read, so not assessed.

**Strongest reason this might be fundamentally wrong.** The catch block is not error handling, it is error suppression with a counter. Every other failure-handling finding is downstream of the single decision that any error is a row error; map the dependency's real failure modes and the transaction, retry policy and exit semantics all follow from that.

**Domain verdict.** Injection hygiene is fine. Failure handling is below the bar for a job carrying a stated recovery requirement.

**Recommended fixes.** Classify errors and abort on connection/pool/timeout classes. Wrap `run()`. Set `bom: true` and assert the expected header before the loop. Validate email shape. Log structured records, not concatenated strings.

### Seat 3 — Operability red-team

**Role & remit.** The skeptic seat and the recipient's viewpoint: where this breaks in production, and what on-call sees when it does.

**Assessment.** Nearly unobservable, and it has one failure mode indistinguishable from success.

**Strengths.** It does exit non-zero when rows fail (L43–45), so the one failure class it models is at least visible to a scheduler.

**Weaknesses.** **Critical, defect** — L43–45 makes a non-zero failure count the only failure test. A zero-byte or truncated S3 download parses to zero or partial rows, gives `failed = 0`, and exits 0. Nightly, that is a silent no-op the scheduler records green — and it undermines the purpose stated at L3. **Major, defect** — L36 logs two integers and nothing else: no path, no run id, no timestamps, no duration, no parsed-row count. On-call sees a red job and cannot identify which S3 object it was processing or where it stopped. **Major, defect** — L31 emits one line per failed row with no cap; in the dead-DB case that is one line per remaining row, and the log flood can become the outage. **Major, defect** — the loop (L23–34) emits nothing on the success path, so a multi-hour run cannot be distinguished from a hang. **Major, defect** *(withdrawn at Step 5)* — nothing bounds runtime, so a stalled DB call parks the job indefinitely. **Minor, defect** — `process.exit(1)` (L44) can drop buffered stdout on a pipe, losing the final counts in exactly the case they are needed `[unverified — recall, not lookup]`. **Minor, gap** — L41 uses `process.argv[2]` unvalidated, and the header says files arrive on S3 while nothing here fetches them.

**Gaps.** No metrics, no alert hook, no run id to grep, no dry-run, no resume path.

**Strongest reason this might be fundamentally wrong.** There is a failure mode indistinguishable from success. Every other finding eventually produces a signal someone can chase; a green exit over an empty table produces none, and a nightly job that can silently do nothing is worse than one that fails loudly.

**Domain verdict.** Not production-ready. It would pass a code read and fail its first bad night.

**Recommended fixes.** Assert a minimum parsed-row count. Log one structured start record and one end record. Cap per-row error logging. Set `process.exitCode` instead of calling `process.exit`.

## 6. Executive review

I re-read the file in full before synthesizing.

**Points of agreement (deduplicated here, removed from the seat sections above).** All three seats reached the missing-transaction finding by different routes — no `BEGIN` (seat 1), catch-and-continue (seat 2), no recovery path (seat 3). Under the Step 3 sequential fallback this agreement is **not** evidence for severity and the finding is marked **sole-source**. Testing why they agree: the header states the requirement in plain language and the file contains no transaction keyword, so the artifact establishes it rather than the seats inheriting it — but the severity rests on my own direct check, not on the convergence. Same treatment for logging inadequacy (seats 2 and 3), also **sole-source**.

**Points of conflict & adjudication.**
- *BOM/header, seat 2 rated critical → **major**.* Named evidence: the header states only "a unique index on `email`", never that the column is nullable. The silent-corruption path requires nullability the artifact does not establish; if `email` is `NOT NULL`, every row fails loudly and the job exits 1 — bad, not silent.
- *Missing field validation, seat 2 rated major → **minor**.* Named evidence: the header documents a unique index and an FK, so the schema already rejects the two fields with referential meaning. What remains is email *format* checking — an addition, not rework.
- *Concurrency guard, seat 1 rated major → **minor**.* Named evidence: the documented unique index means a second concurrent run's inserts are rejected, not duplicated, so the residual harm is doubled DB load and a spurious failure count. This inverts once the transaction fix lands — the lock becomes necessary then, so ship both together.
- *No seat contested any critical.* Silence from the other seats on each domain is not treated as agreement.

**Verification result.** 1 withdrawn, 3 corrected (one critical→major, two major→minor). **Withdrawn:** seat 3's "no timeout, hangs forever" — `const db = require('../db');` (L14) means timeout configuration lives in a module I did not read; the claim was about code outside the reviewed artifact. The residual concern (no overall run deadline) is real but minor and folded into the progress finding. All three criticals were checked by direct search of the source, not recall: `BEGIN`, `COMMIT`, `ROLLBACK`, `transaction`, `ON CONFLICT`, `createReadStream`, `.catch` — zero occurrences in 49 lines; `fs.readFileSync(localPath, 'utf8')` located at L17; `if (result.failed > 0) {` at L43. I also tested the transaction finding adversarially: if `../db` somehow wrapped calls in an implicit transaction, the file still never issues a `COMMIT`, so it would import nothing — the finding holds under both readings. The 900 MB finding does not depend on my recalled V8 string-length constant; the parsed-object memory cost is independently fatal. No seat's reliability is in question: the withdrawal and both downgrades came from claims about code outside this file or schema details the header does not state — a scope-discipline issue, not fabrication.

**Panel blind spots.** Under the sequential fallback the seats shared one context, so they likely share what they *failed* to look at, not just what they found. The domain no seat examined is **data semantics**: nobody checked whether the marketing export is a full-state snapshot or an append-only delta. **A critical defect could live there** — if it is a snapshot, this job never updates or deletes, so unsubscribes never propagate and the table drifts permanently from the source of truth, a defect larger than anything reported here and invisible from this file. All three seats also shared the unstated assumption that the target is PostgreSQL; `$1` placeholders make it likely but the file never says so, and several fixes (`ON CONFLICT`, NULL behavior under a unique index, `COPY`) are Postgres-specific. Load-bearing claim to verify externally: V8's maximum string length against the deployed Node version, before sizing the streaming fix.

**Overall judgment.** Line by line this is competently written — parameterized SQL, correct arity, clear naming, honest counters. Structurally it is wrong for the job its own header describes. This is not missing polish: the loop's shape is the mechanism the header blames for the February incident, and the file reproduces it.

**Decision on further action: reject and rework.**

**Prioritized next steps.**
1. Replace L17–34 with a streamed parse and batched inserts inside one explicit transaction on a dedicated client — criticals 1 and 2 share this fix.
2. Add the outcome contract at L43–45: fail on zero parsed rows; `ROLLBACK` and exit non-zero on connection-class errors instead of counting them.
3. Make re-runs safe and single-instance: `ON CONFLICT (email) DO UPDATE` plus an advisory lock taken at start.
4. Replace both `console.log` calls with structured start/end records and a capped error sample.
5. Before implementing, confirm with the marketing platform whether the export is a snapshot or a delta. If it is a snapshot, the fix list above is incomplete and this job is missing update and delete handling entirely.

**Confidence & what would change the verdict.** Of the 3 critical and 7 major findings, I expect **9 of 10** to survive an independent expert re-check. The first to fall is the unbounded per-row logging major — if the log collector already rate-limits, its impact narrows to minor. Next most likely to move is the BOM/header major, already corrected once; it depends on whether this platform's export has ever carried a BOM, which I cannot check. The three criticals rest on verified evidence — strings present or provably absent in the file, plus the header's own stated requirement — not on inference. What would move the verdict: if `../db` turns out to expose a batching, transaction-wrapping `query`, critical 1 narrows; if real inputs never approach the header's stated 900 MB, critical 2 falls to major. Either alone leaves the decision unchanged; both together would move it to *revise substantially before use*, which is also where a reviewer weighting the reusable SQL more heavily would land — the practical difference between the two calls is small. Nothing identified would move it to approve. Per the roster cap, this verdict does not cover data semantics; a snapshot-vs-delta defect there would change it.
