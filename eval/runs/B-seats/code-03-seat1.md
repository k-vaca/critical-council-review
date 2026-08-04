# Seat 1 — Correctness & concurrency

*Tier read: 2 (the artifact is a module / single deliverable, `# util/lru.py` line 1), so all eight Step 4 fields. Seat written in isolation; I have seen no other seat's analysis.*

**Role & remit.** Reviewer for computational correctness and thread/task safety: does `LRUCache` maintain LRU and capacity invariants, and does it hold up under the concurrency its own docstring describes?

**Assessment.** The LRU mechanics are correct. I hand-traced capacity-1 eviction, the update-an-existing-key path, and put-at-capacity; ordering and bound hold in each. The concurrency story is where it weakens: the module's entire safety argument is one prose sentence, with no enforcement, no detection, and a silent failure mode if a caller breaks it. Separately, `__contains__` is an accounting hole in the hit/miss counters.

**Strengths.**
- `self._data.move_to_end(key)` (line 33) is genuinely required — `OrderedDict.__setitem__` does *not* reorder an existing key. Omitting it is the single most common bug in this class of code; it is present and correct.
- `popitem(last=False)` (line 36) evicts the oldest, not the newest — correct direction.
- `if self.capacity == 0:` (line 30) short-circuits before insertion, so eviction can never run against an empty dict on the documented zero-capacity path.

**Weaknesses, risks & errors.** All quotes re-checked against the source before writing.

| # | Sev / kind | Anchor (locator + verbatim) | Problem |
|---|---|---|---|
| W1 | **Major, defect** | lines 4–5: `Single-threaded by contract: instances are created per request handler and never shared across threads.` | Asserted, never enforced or detected. Nothing records an owning thread. If violated, failures are silent or intermittent, not loud: `self.hits += 1` (line 26) is a non-atomic read-modify-write, so increments are lost; `self._data.move_to_end(key)` (line 25) runs *after* the membership test on line 22, so a concurrent eviction in that window raises `KeyError`; `popitem(last=False)` (line 36) can hit an emptied dict. The claim itself describes deployment facts unverifiable from this file — marked `[unverified — cannot be checked from the artifact]` per non-negotiable 6. Narrowing, in fairness: under *cooperative* concurrency (asyncio, gevent) no method contains an await or I/O yield point, so the code is genuinely safe there and the docstring's "across threads" phrasing is adequate for that case. |
| W2 | **Major, defect** | line 42: `return key in self._data` | A lookup through `in` increments neither counter, so `hits + misses` is not the lookup count and any hit rate derived from the two public fields is wrong by however many `in` checks occurred. The counters are the only stats surface, so this is not recoverable downstream. `in` also skips `move_to_end`, meaning an entry accessed only via `in` ages out; that half is defensible as a peek, but no line of the docstring says so. |
| W3 | **Minor, defect** | line 16: `self.capacity = capacity` | Plain public attribute; the bound is re-established only inside `put`. Lowering it after construction never shrinks the cache, and setting it to `0` does **not** disable caching — `put` returns at line 31 while `get` keeps serving existing entries, contradicting `a capacity of zero disables caching.` (lines 5–6). A negative assignment also bypasses the check at lines 14–15. Conditional on a caller mutating the field, hence minor. |
| W4 | **Minor, defect** | line 45: `self._data.clear()` | No single-entry invalidation exists anywhere in the class, so keeping the cache coherent with a changed source of truth requires discarding everything — and `clear()` also zeroes `hits`/`misses` (lines 46–47), destroying metric history as a side effect of an unrelated operation. Overlaps the operability seat; reported per the roster instruction. |
| W5 | **Minor, defect** | line 2: `A bounded least-recently-used cache.` | "Bounded" bounds entry count, not bytes; no per-entry size accounting, so N large values are unbounded in memory. Overlaps the failure-handling seat. |

One preference, not a defect: `get` performs three hash lookups (lines 22, 25, 27) where a `try`/`except KeyError` around one would do.

**Gaps.** No thread-affinity assertion or lock; no `invalidate(key)`; no `reset_stats()` separate from `clear()`; no documented access semantics for `in` versus `get`; no stated type contract on `capacity` (a float is accepted and silently floors the bound).

**Strongest reason this might be fundamentally wrong.** The deployment model in the docstring may make the cache pointless. If `instances are created per request handler and never shared across threads` (lines 4–5), each instance dies with its handler, so it pays off only when one handler looks up the same key more than once — and the docstring never states the intra-request reuse pattern that would justify it. If the real reuse is cross-request (the usual reason to reach for an LRU), the design is wrong at its core, and the obvious fix — hoisting to one shared instance, which the `util/` path on line 1 already invites — is precisely what invalidates the thread contract and activates every mechanism in W1 at once. This is the strongest candidate for a foundational error; I cannot resolve it from the artifact alone, because the calling code is not in scope.

**Domain verdict.** Within its stated contract, the data structure is correct and I found no computational defect in the LRU logic. Against what a competent practitioner should ship into a shared `util/` module, it falls short on two counts: the safety argument rests entirely on an unverifiable, unenforced deployment claim whose violation fails quietly, and the observability counters are wrong the moment a caller uses `in`. Adequate as private per-handler code; below bar for a shared utility path where callers will not read the docstring.

**Recommended fixes.**
1. Resolve the lifetime question first — it gates everything else. If reuse is cross-request, this must be a shared instance with a `threading.Lock` around `_data` mutations and the counter updates. If it is truly per-request, state the intra-request reuse pattern in the docstring.
2. Make the contract detectable rather than merely documented: record `threading.get_ident()` in `__init__` and assert it in `get`/`put`. Ship a lock or a guard — not the current unguarded middle.
3. Route `__contains__` through the same accounting as `get`, or rename it a peek and document that it neither counts nor promotes, so `hits + misses` equals the lookup count.
4. Make `capacity` a read-only property, or re-run eviction in its setter so `capacity = 0` really does disable caching as line 6 claims.
5. Add `invalidate(key)`, and move the counter reset out of `clear()` into a separate `reset_stats()`.
