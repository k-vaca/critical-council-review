# Critical Council Review — `util/lru.py`

## 1. Verdict

**Approve with minor revisions.** The LRU algorithm, the capacity bound, and the eviction
direction are correct — I hand-traced and then executed every path — and the module honors its
own documented contract; the one finding that survives at major is that the file advertises
`capacity` as a public knob whose mutation silently breaks two things the docstring promises.

1. Close the capacity knob — rename to `_capacity` with a read-only property, or add a setter
   that re-validates and evicts in a loop; change `if` to `while` at line 35.
2. Say in the docstring (lines 4–6) that capacity is construction-time only, that it bounds
   entry count rather than bytes, and that the single-thread rule is unenforced.
3. Add `invalidate(key)` and a `reset_stats()` separate from `clear()` (lines 44–47).

## 2. Result & standard

Under review: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/code-03-lru-cache.py`,
47 lines, read in full. Not my own prior output. **Standard:** the artifact's own stated purpose
— "A bounded least-recently-used cache." (line 2) under the lifecycle in lines 4–6 — plus my
stated judgment of what a competent Python practitioner ships as a small internal cache helper.

**Tier 2** (a module / single deliverable), three seats. **Independence mechanism:** parallel —
the three seats were run in isolation, none saw another's analysis, and none received requester
framing. This verification-and-executive pass also received no framing. Seats disagreed on tier
(1 and 3 read tier 2; 2 read tier 1); immaterial, all three emitted anchored findings.

**Text in the artifact addressed to its reviewer:** none. Lines 4–6 state a deployment contract
and hand capacity choice to callers; that is documentation aimed at callers, not direction aimed
at a reviewer, and it does not narrow this review. Seat 3 raised it under non-negotiable 8; that
characterization is withdrawn (see W-4). Seat 2 ruled correctly on the same text.

*Budget note: this review exceeds the tier-2 section ceilings. The skill lists the length budget
as tune-freely; the Step 5 ledger is load-bearing here because seven of nine major findings moved.*

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Major | line 16 `self.capacity = capacity`; line 35 `if len(self._data) > self.capacity:` | Public unguarded knob: lowering capacity pins the cache at its high-water mark, setting it to 0 freezes rather than disables (`get` keeps serving), setting it negative bypasses the `__init__` check and stores nothing — all silently | Make capacity a read-only property or a validating setter that evicts in a `while` loop | Confirmed (narrowed) |
| Minor | lines 4–5 `Single-threaded by contract: instances are created per request handler and never shared across threads.` | Contract is asserted in prose with no enforcement or detection; a violation corrupts counters and can raise `KeyError` from `move_to_end` (line 25) | Record `threading.get_ident()` in `__init__` and assert it under a debug flag | Corrected (was major, seats 1 & 3) |
| Minor | line 42 `return key in self._data` | `in` neither counts nor promotes, and nothing documents it as a peek, so an `in`-only lookup is invisible to `hits`/`misses` | Count `in` as a lookup, or document it as a deliberate non-counting, non-promoting peek | Corrected (was major, seat 1) |
| Minor | line 44 `def clear(self):` | Only removal path in the public surface; no per-key removal, and the docstring never states entry lifetime | Add `invalidate(key) -> bool`; state in the docstring that entries never expire | Corrected (was major, seats 2 & 3) |
| Minor | line 36 `self._data.popitem(last=False)`; lines 18–19 counters | No eviction counter, no `stats()`, no `__repr__`, no instance identity, so per-instance counters are inconvenient to aggregate | Add an `evictions` counter and a `stats()` returning capacity, size, hits, misses, evictions | Corrected (was major, seat 3) |
| Minor | line 46 `self.hits = 0` (inside `clear`) | Flushing data also zeroes the metrics; a monitor reading `hits` as monotonic sees it go backwards | Split into a data-only `clear()` plus an explicit `reset_stats()` | Confirmed |
| Minor | line 14 `if capacity < 0:` | Sign-only validation: `float("inf")` builds a never-evicting cache (verified: 6 entries at "capacity" inf), `True`→1, `2.5`→2, and `None`/`"10"` raise a bare `TypeError` rather than the module's own `ValueError` | Reject non-integral, non-finite, and bool capacity before the sign check, naming the value | Confirmed |
| Minor | line 2 `A bounded least-recently-used cache.` | "Bounded" bounds entry count, not bytes; the docstring hands capacity choice to callers (lines 5–6) without the byte dimension needed to choose | State the bound is on entry count; note worst-case memory is capacity × largest value | Confirmed |

No critical findings. None of the three seats raised one either.

## 4. Council roster

Convened: **Seat 1 — correctness & concurrency** (owns LRU/capacity invariants and thread
safety); **Seat 2 — security & failure handling** (owns error paths and caller misuse);
**Seat 3 — operability red-team** (owns diagnosability and incident-time controls; the required
skeptic seat). Seats 2 and 3 between them carry the dependent's viewpoint — the caller adopting
the module and the operator paged about it.

**Deliberately not covered.** (a) *API/typing conventions* — no seat examined that the module
carries no type annotations at all and implements `__len__`/`__contains__` without `__iter__`
(verified: `LRUCache` object is not iterable). A critical defect could not live here; it is a
maintainability gap. (b) *Test coverage* — outside this file, so no seat could check it; a
critical defect could live in untested behavior, but I executed the core paths myself and found
none. (c) *Call sites* — out of scope for every seat and the single load-bearing external fact
(see blind spots).

## 5. Individual analyses

Deduplicated per Step 6: findings raised by more than one seat are stated once in §3 and §6 and
removed from the seat sections. What remains below is each seat's distinct contribution.

**Seat 1 — correctness & concurrency.** Verified the LRU mechanics and found no computational
defect; correctly identified that `self._data.move_to_end(key)` (line 33) is genuinely required
because `OrderedDict.__setitem__` does not reorder an existing key — the most commonly botched
line in this class of code, present and correct. I confirmed this by execution (update-existing
at capacity leaves size at 2 and returns the new value, evicting nothing). Its one preference,
not a defect: `get` performs three hash lookups (lines 22, 25, 27) where `try`/`except KeyError`
would do one. Seat 1's foundational-risk field is the sharpest thing any seat wrote: if real
reuse is cross-request, hoisting to a shared instance is exactly what invalidates the thread
contract — the fix and the hazard are the same action.

**Seat 2 — security & failure handling.** Best-calibrated seat of the three. Its positive
findings are earned and I confirm them: no I/O, no deserialization, no logging, no credential
handling, no `__repr__` to leak contents, and an unhashable key raises `TypeError` at the
membership test *before* any counter increment or mutation, so a bad key cannot leave the cache
half-written. It alone rated the thread contract minor with the correct reason — a module is not
obliged to defend a documented contract — and it alone declined the non-negotiable 8 trap.
Its "considered and rejected" note (zeroizing secrets in CPython would be security theater) is
the kind of disclosure that makes a seat auditable.

**Seat 3 — operability red-team.** Its anchors are all real and its recommended fixes are the
most concrete of the three, but its factual sub-claims about what the module *lacks* are
unreliable: it asserted three absences the artifact actually provides (see W-1, W-2, W-5, W-6).
It also holds two mutually inconsistent lifecycles across its own findings — instances too
short-lived to read counters (Major3) yet long-lived enough for entries to grow "arbitrarily
old" (Major4). Its surviving distinct contribution is the eviction-counter gap and the
observation that `capacity` is the only operator knob and it fails silently when turned.

## 6. Executive review

### Points of agreement

All three seats converge on: (a) the LRU algorithm and capacity bound are correct as written;
(b) the public `capacity` attribute is the module's weak point; (c) every property the docstring
promises is enforced by prose and nothing else; (d) `clear()` destroying the counters; (e)
"bounded" bounding entries rather than bytes. I independently confirm (a) through (e).

### Testing why they agree (non-negotiable 3)

The agreement on **facts** is sound and I verified it directly. The agreement on **severity** is
not. All three seats landed on "below the competent-practitioner bar," and all three got there
through the same assumption: that `# util/lru.py` (line 1) means a long-lived, widely-shared
utility whose callers will not read the docstring. The artifact does not establish that. Line 1
is a path comment; lines 4–6 state the opposite lifecycle — instances created per request
handler. Seats 2 and 3 both then argued that missing per-key invalidation is major because a
stale entry cannot be revoked, which an instance that dies with its request handler cannot
suffer from. The seats inherited a standard from a directory name and judged against it while
the docstring contradicted it. That single shared assumption is why five of the nine major tags
came down. Attack the assumption; the agreement itself stands.

### Points of conflict & adjudication

- **Thread contract — seat 1 major, seat 3 major, seat 2 minor.** Ruled **minor**, with seat 2.
  Not headcount: the specific evidence is that the contract is stated plainly in the first
  sentence of the module docstring, and shipping a non-thread-safe container with a documented
  single-thread contract is ordinary practice, not a defect. Non-negotiable 4's test — what
  breaks if this is never fixed? — answers "nothing, for a caller who honors the stated
  contract." Seat 1's mechanisms (lost counter increments, `KeyError` from `move_to_end` at line
  25 after the line 22 membership test) are all real; they are consequences of breaking the
  contract, not of the code.
- **Per-key invalidation — seats 2 and 3 major.** Ruled **minor**. Contrary evidence in the
  artifact: expiry and invalidation are requirements the module never took on, and its documented
  per-handler lifecycle bounds an entry's staleness to one request. Seat 2 conceded the point
  itself — "judged strictly against 'A bounded least-recently-used cache.' (line 2) it does what
  it says" — then rated it major anyway on an imported revocable-data use case. `[unverified —
  recall, not lookup]` the stdlib's own `functools.lru_cache` exposes only `cache_clear()` with
  no per-key eviction, which if correct puts this module at the same surface as the language's
  reference implementation.
- **Capacity knob — seats 2 and 3 major, seat 1 minor.** Ruled **major**, upheld against seat 1.
  Seat 1's reason for minor (conditional on a caller mutating the field) is true but is answered
  by the file's own naming convention: `capacity` has no leading underscore where `_data` does,
  so the file advertises the attribute as public surface. The domain owners (2 and 3) rated it
  major and I verified all three failure modes by execution. Narrowed, not upheld wholesale —
  see below.
- **Eviction accounting — seat 3 major.** Ruled **minor**, and its central claim withdrawn.

### Verification result

Nine findings entered Step 5 tagged major; zero were tagged critical by any seat. **Two
confirmed** (the capacity knob, raised independently by seats 2 and 3 — one finding after
deduplication), **seven corrected/downgraded**, **zero withdrawn outright**. Within those,
**six discrete sub-claims were withdrawn** as false or unsupportable:

- **W-1** (seat 3, Major1) — "nothing here distinguishes [thrashing from no locality]." False.
  `__len__` (line 38) against the public `capacity` shows saturation: verified 10/10 on a
  thrashing cache versus 50/1000 on an unsaturated one. Seat 3 listed `__len__` as a strength
  without connecting it to its own diagnostic claim.
- **W-2** (seat 3, Major3) — "Counters are per-instance with no accessor." False. `self.hits`
  and `self.misses` (lines 18–19) are public attributes; verified `cache.hits`/`cache.misses`
  read back 1 and 1 directly.
- **W-3** (seat 3, Major4) — "On a low-traffic instance an entry can be arbitrarily old."
  Contradicts the per-request-handler lifecycle the same seat relies on in its Major3.
- **W-4** (seat 3, Major5) — lines 4–5 are "a scope-narrowing claim inside the artifact" under
  non-negotiable 8. False: the text addresses callers about runtime deployment, not a reviewer
  about review scope.
- **W-5** (seat 3, minor at line 25) — "No read-without-touch." False. `__contains__` (lines
  41–42) is exactly a non-promoting read: verified that a key checked with `in` is still evicted
  first, so `in` does not refresh recency. The surviving narrower claim — no way to read a
  *value* without promoting — is folded into the `__contains__` finding.
- **W-6** (seat 3, minor at line 42) — "the common `if key in cache: cache.get(key)` probe is
  invisible to the metrics." False: verified that idiom yields hits=1, misses=0 — one logical
  lookup, one hit, correct accounting. The real defect is narrower: an `in`-only lookup that
  never calls `get` is uncounted (verified: counters unmoved at 0/0 across an `in` miss).

**Narrowing on the surviving major.** Seat 2's "the cache stays pinned at 100 forever" is
confirmed for the new-key path (verified: 60 new-key puts after lowering 100→10 left size at
100) but is silent on the existing-key path, where each put does drain one entry (verified:
100→95 over five puts). The diagnosis — a single `if` rather than a `while`, so the bound never
re-heals in bulk — is correct and is the right fix.

**Seat reliability.** Seat 3 produced four of the six withdrawn claims and two more at minor,
and its severity scale is systematically inflated: five of nine findings tagged major, of which
one survives at that level. Its anchors are accurate; its assertions about what the module does
*not* provide are not, and it twice claimed an absence the file supplies. Treat its severity tags
and its absence-claims as requiring independent check. Seats 1 and 2 were factually accurate
throughout; seat 1 over-rated two findings, seat 2's calibration was the best of the three.

### Panel blind spots

The strongest case the whole council is wrong: all three seats judged this against a shared-
utility standard sourced from a path comment, and all three treated the absence of hardening
(enforcement, invalidation, telemetry) as defect rather than as scope. If the module is what its
docstring says — a small per-handler helper — then the council collectively over-reviewed it,
and my downgrades may not have gone far enough.

Domains no seat examined: **typing and API conventions** (no annotations anywhere; `__len__` and
`__contains__` without `__iter__`, so the class is not a `Mapping` and `for k in cache` raises —
verified; a critical defect could not live here), and **test coverage** (outside the file; a
critical defect could in principle live in untested behavior, so I executed the core paths
myself — correct LRU eviction order, no spurious eviction on update-at-capacity — and found none).

**Load-bearing external fact requiring an actual verification pass:** the docstring's deployment
claim at lines 4–5, `[unverified — I am scoped to this one file and cannot inspect any call
site]`. Seats 1 and 2 independently named this as their strongest foundational risk. Grep the
call sites before treating this as settled.

### Overall judgment

A small, correct, clean LRU cache that does what it says. The one thing implementations of this
shape usually get wrong — reordering on update — is right, and I verified the eviction order,
the update-at-capacity path, and the zero-capacity path by execution. What it lacks is hardening
against callers who step outside the documented contract, and one of those exits is signposted
by the file's own naming. That is a real defect and a small fix, not a rework.

### Decision on further action

**Approve with minor revisions.**

### Prioritized next steps

1. Grep the call sites for the lifecycle claim in lines 4–5. It gates the severity of three
   findings and costs one search.
2. Close the capacity knob: `_capacity` plus a read-only property, or a validating setter; change
   `if` to `while` at line 35.
3. Rewrite lines 4–6 to state that capacity is construction-time only, bounds entry count not
   bytes, and that the single-thread rule is unenforced.
4. Add `invalidate(key)`, split `reset_stats()` out of `clear()`, add an `evictions` counter and
   a `stats()`.
5. Validate capacity type in `__init__` (reject bool, non-integral, non-finite) naming the value.
6. Document whether `in` is a deliberate non-counting, non-promoting peek — then leave it alone.

### Confidence & what would change the verdict

Of the one major and seven minor findings reported, I expect the major to survive an independent
re-check: it is anchored in three lines I traced by hand and then reproduced by execution, and
two seats reached it independently by the same mechanism. Of the minors, the two I expect to fall
first are the observability gap and the missing per-key removal — both are missing-feature claims
against a standard no seat could cite, and both were already downgraded once here.

The verdict rests on **verified evidence** for every code behavior (I executed each disputed
path) and on **inference** for the standard: that this is the per-handler helper its docstring
describes rather than the hardened shared utility all three seats assumed. That inference is what
would flip it. If the call sites show instances hoisted to module scope or reused across a thread
pool, the thread-contract and invalidation findings return to major, a data-race becomes a live
correctness risk rather than a contract violation, and the decision moves to **revise
substantially before use**.
