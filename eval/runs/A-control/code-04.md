# Review — `artifacts/code-04-csv-import.js` (jobs/importSubscribers.js)

One expert review pass. 49 lines. Reviewed against the requirements the file states about
itself: nightly import, inputs 40 MB–900 MB, `subscribers` has a unique index on `email` and
an FK `segment_id -> segments(id)`, and the 2026-02 ops requirement that **a failed import
must leave the table exactly as it was before the job started**.

Summary: the job does not meet the one requirement it explicitly documents, and it cannot
process the input sizes it explicitly documents. Both are structural, not polish.

Findings: **3 critical, 6 major, 3 minor.**

---

## Critical

### C1 — No transaction; a failed import leaves partial state (the exact February failure mode)
**Location:** lines 23–34 (insert loop) with lines 43–45 (`run`)
**Anchor:** `` `for (const row of rows) { try { await db.query('INSERT INTO subscribers ...` ``
**Problem:** Every row is committed independently in autocommit, so when the job exits 1 the
table retains every row inserted before the failure — directly violating the stated ops
requirement.

The header comment states the requirement in plain terms and the code contains no `BEGIN`,
no `COMMIT`, no `ROLLBACK`, and no staging-table swap. Worse, the failure path is *guaranteed*
to leave partial state: the loop deliberately swallows each row error and keeps inserting, so
by the time `process.exit(1)` runs, every valid row in a partially-bad file is already
durably committed. A reviewer signing this off would be re-creating the February incident.

Fix requires one of: a single transaction around the whole load (with the caveat that a
multi-million-row transaction holds locks and bloats WAL), or — better at this size — load
into a staging table and do an atomic swap/merge in one short transaction at the end.

### C2 — Whole file read into a string and parsed synchronously; cannot handle the stated 900 MB inputs
**Location:** lines 17–18
**Anchor:** `` `const raw = fs.readFileSync(localPath, 'utf8'); const rows = parse(raw, { columns: true, skip_empty_lines: true });` ``
**Problem:** Reading a 900 MB file into a single UTF-8 JS string exceeds V8's maximum string
length (~512 MiB, `buffer.constants.MAX_STRING_LENGTH`) and throws `ERR_STRING_TOO_LONG`
before a single row is inserted.

Two independent blowups stacked on one line:

1. `readFileSync(path, 'utf8')` materialises the entire file as one JS string. Above roughly
   512 MiB this is a hard engine limit, not a tuning problem — `--max-old-space-size` will
   not save it.
2. Even under that ceiling, `csv-parse/sync` returns the complete array of row objects. Each
   CSV row becomes a JS object with four string properties; the in-memory expansion over the
   raw bytes is typically several-fold. A 400 MB file will sit in multiple GB of heap
   alongside the original string.

The documented input range starts at 40 MB and goes to about 900 MB, so this fails on the
upper half of its own stated range. This needs the streaming API
(`fs.createReadStream(...).pipe(parse({...}))`) with bounded batching, not a larger heap.

### C3 — No header or required-field validation; a BOM or renamed column silently inserts NULL rows and reports success
**Location:** line 18 (parse options) and line 27 (parameter binding)
**Anchor:** `` `[row.email, row.name, row.segment_id, row.signed_up_at]` ``
**Problem:** If the export's header differs at all from the four expected names, `row.email`
is `undefined`, node-postgres binds `undefined` as SQL NULL, and the job cheerfully inserts
millions of empty rows, prints `failed 0`, and exits 0.

This is not hypothetical. `csv-parse` defaults to `bom: false`, so a UTF-8 BOM — extremely
common in marketing-platform CSV exports — makes the first column name `"﻿email"`, not
`"email"`. From that moment `row.email` is `undefined` for every row. The same happens if the
vendor ships `Email` instead of `email`.

What makes it critical rather than merely annoying is that nothing catches it:

- A PostgreSQL unique index permits **many** NULLs, so the `email` unique index raises no
  error on repeated NULLs. The file only claims a unique index, not `NOT NULL`.
- The success criterion is `result.failed > 0`. Zero errors means exit 0, so the scheduler
  records a clean nightly run over a corrupted table.

Even in the friendlier case where `email` is `NOT NULL`, the job issues one failing INSERT
per row for the entire file before reporting. Either way the code needs an explicit header
assertion before the first insert, plus `bom: true`.

---

## Major

### M1 — Row-at-a-time awaited INSERTs will not finish in a nightly window
**Location:** lines 25–28
**Anchor:** `` `await db.query('INSERT INTO subscribers (email, name, segment_id, signed_up_at) VALUES ($1, $2, $3, $4)', ...)` ``
**Problem:** One serialized network round-trip per row means a multi-million-row file takes
hours, because each `await` waits for a full client-server round-trip before the next row
starts.

At 900 MB the row count is plausibly in the tens of millions. Even at an optimistic 0.5 ms
per round-trip, 10M rows is 83 minutes of pure latency with the database mostly idle. The
correct shapes are `COPY ... FROM STDIN` (via `pg-copy-streams`) or multi-row `VALUES`
batches of ~1–5k rows; either is one to two orders of magnitude faster and composes naturally
with the streaming fix in C2 and the staging table in C1.

### M2 — Blanket `catch` treats infrastructure failures as ordinary bad rows
**Location:** lines 30–33
**Anchor:** `` `} catch (err) { console.log('row failed: ' + err.message); failed++; }` ``
**Problem:** The handler cannot distinguish a duplicate-email violation from a dropped
connection, a full disk, or an FK violation, so a mid-run database outage is silently
recorded as N failed rows while the loop keeps hammering a dead server.

There is no classification on `err.code` and no fail-fast threshold. Three consequences worth
separating:

- A transient outage at row 50,000 of 5,000,000 produces 4,950,000 logged "row failed"
  lines and a meaningless summary.
- Genuine data-quality problems (duplicate email, missing segment) are indistinguishable in
  the output from operational ones, so nobody can triage the morning after.
- Once C1 is fixed by wrapping the load in a transaction, this pattern becomes actively
  broken: in PostgreSQL the first error aborts the transaction, and every subsequent
  statement fails with `current transaction is aborted`. Continuing past an error inside a
  transaction is not a valid strategy without savepoints.

### M3 — `run()` has no rejection handler, no main guard, and no argument validation
**Location:** lines 40–48
**Anchor:** `` `const path = process.argv[2]; const result = await importSubscribers(path); ... run();` ``
**Problem:** Any throw from `readFileSync` or `parse` — a missing file, a malformed row, the
`ERR_STRING_TOO_LONG` from C2 — escapes as an unhandled promise rejection with no controlled
exit path or cleanup.

Specifics:

- `process.argv[2]` is never checked. Invoking the job with no argument calls
  `readFileSync(undefined, 'utf8')`, producing a type error rather than a usable message.
- `run()` is called bare. On Node ≥ 15 an unhandled rejection terminates the process, so the
  exit code happens to be non-zero, but the job skips any rollback or cleanup it would
  otherwise need, and on older runtimes it prints a warning and **exits 0** — a failed
  import reported to cron as a success.
- `csv-parse` throws on a column-count mismatch, so one malformed line anywhere in the file
  takes this path. That error never reaches the `failed` counter.

Needs `run().catch(err => { ... process.exitCode = 1; })` plus argument validation.

### M4 — No idempotency or re-run strategy against the unique email index
**Location:** line 26
**Anchor:** `` `'INSERT INTO subscribers (email, name, segment_id, signed_up_at) VALUES ($1, $2, $3, $4)'` ``
**Problem:** A plain INSERT with no `ON CONFLICT` clause means any re-run — the normal
response to a failed nightly job — collides with the unique index on `email` for every row
already loaded.

For a recurring import against a uniquely-indexed column the code has to state an intent, and
this one states none. Either the import is incremental and needs
`ON CONFLICT (email) DO UPDATE`/`DO NOTHING`, or it is a full replace and needs a staging
table plus swap. As written, the second run of the same file reports every row as failed and
exits 1, which is indistinguishable from a real failure. Note this also affects the *first*
run whenever the export itself contains a duplicated email.

### M5 — Empty CSV fields arrive as `''`, not `null`, and abort typed columns
**Location:** line 27
**Anchor:** `` `[row.email, row.name, row.segment_id, row.signed_up_at]` ``
**Problem:** `csv-parse` yields an empty string for a blank field, and `''` sent to the
integer FK `segment_id` or the timestamp `signed_up_at` raises `invalid input syntax`, so
every row with an optional field left blank is silently dropped by the C1/M2 catch.

Rows with no segment assignment are exactly the ones a marketing export will leave blank.
They should become NULL (subject to the FK, which permits NULL) rather than errors. Needs an
explicit empty-string-to-null coercion, e.g. `csv-parse`'s `cast` option or a per-field
normaliser, before binding.

### M6 — No connection cleanup; `process.exit(1)` cuts the process off mid-flight
**Location:** lines 40–46
**Anchor:** `` `if (result.failed > 0) { process.exit(1); }` ``
**Problem:** Nothing ever closes the database pool, so on the success path the process can
hang on open idle handles, and on the failure path `process.exit()` terminates immediately
without draining pending writes.

Two distinct issues:

- **Success path:** `run()` resolves and returns. If `../db` exports a `pg.Pool` (the
  overwhelmingly common shape for this import), the idle clients keep the event loop alive
  and the job never exits until an idle timeout fires — a nightly cron job that fails to
  terminate risks overlapping runs against a table with a unique index. Needs `db.end()` in a
  `finally`.
- **Failure path:** `process.exit(1)` is synchronous and does not flush asynchronous stdout
  writes to a pipe, so the final summary line can be truncated in exactly the runs where the
  logs matter most. `process.exitCode = 1` and a natural return is the correct idiom.

---

## Minor

### mi1 — Row failures are logged to stdout with no identity and no stack
**Location:** line 31
**Anchor:** `` `console.log('row failed: ' + err.message);` ``
**Problem:** The message carries no line number, no email and no stack, and goes to stdout
rather than stderr, so at scale it is both unactionable and capable of flooding the log
pipeline with millions of identical lines.

Should be `console.error` with the row index and the offending key, and capped (log the first
N, then aggregate by `err.code`).

### mi2 — `signed_up_at` is passed through as an unparsed string
**Location:** line 27
**Anchor:** `` `row.signed_up_at` ``
**Problem:** Handing a raw CSV string to a timestamp column delegates parsing to the server's
`DateStyle`, so an ambiguous value like `05/06/2026` is accepted under either DMY or MDY and
silently stored as the wrong date.

Truly malformed values error out and are caught, but ambiguous ones do not — parse to a
`Date` (or assert ISO-8601) at the boundary instead.

### mi3 — Module executes on import and exports nothing
**Location:** line 48
**Anchor:** `` `run();` ``
**Problem:** With no `module.exports` and no `require.main === module` guard, the job cannot
be unit-tested or invoked programmatically, and merely `require`-ing the file runs a
production import.

---

## What is sound

Worth stating so the findings above are read in proportion:

- **Queries are correctly parameterised.** `$1..$4` with a separate values array — no SQL
  injection, despite the input being untrusted third-party CSV. This is the single most
  common defect in code of this shape and it is absent.
- **The header comment is genuinely good.** It records the input size range, the relevant
  schema constraints, the ops requirement and its incident provenance. That documentation is
  what makes C1 and C2 assessable at all; most files of this kind supply nothing.
- `columns: true` and `skip_empty_lines: true` are the right baseline parse options as far as
  they go.
- Counting and returning `{ inserted, failed }` rather than only logging is the right
  instinct for a job that a scheduler has to interpret.

## Suggested order of work

C1 and C2 cannot be fixed independently of each other, and fixing them dictates the shape of
M1, M2 and M4. The efficient sequence is: stream-parse in bounded batches (C2) → `COPY` into
a staging table (M1) → validate headers and coerce fields before load (C3, M5) → atomic
swap/merge in one short transaction (C1, M4) → classify errors and fail fast (M2) → tidy the
entry point and shutdown (M3, M6, mi1–mi3).
