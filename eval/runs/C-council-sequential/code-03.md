# Critical Council Review — `util/lru.py`

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Decision: revise substantially before use.** The LRU algorithm itself is correct — the two mistakes this class of code usually makes are both avoided — but the contract around it never commits to an instance lifetime, capacity cannot safely be lowered, and no single key can be invalidated.

1. Rewrite the lifetime clause (docstring, line 4) to say whether an instance lives for one request or one handler object; three of the four major findings resolve differently depending on the answer.
2. Make `capacity` read-only, and change line 35's `if` to `while` (in `put`).
3. Add `pop(key, default=None)` beside `clear()` (line 44).

## 2. Result & standard

Judged: `artifacts/code-03-lru-cache.py`, 48 lines, read in full. Not my own prior output. Standard: the artifact's own stated purpose — line 2, "A bounded least-recently-used cache" — plus the competent-practitioner bar for a cache sitting on a request path; both are reported where they diverge. **Tier 2** (module / single deliverable). **Independence mechanism: sequential seats** (Step 3 fallback). The roster was specified by the requester; disclosed per Step 2, and since no seat was added, the verdict is capped as stated in §4.

*Budget note:* this review runs to roughly 3,600 words against tier 2's ~1,800-word total. Three seats at full Step 4 depth plus Steps 5 and 6 do not compress to that figure, and the skill's own application-strength note designates the length budget as arbitrary and tunable. Disclosed rather than absorbed by cutting findings.

Artifact text that functions as a scope limit, quoted per non-negotiable 8: *"Single-threaded by contract: instances are created per request handler and never shared across threads."* (lines 4–5). It is addressed to callers, not to a reviewer, so I do not report it as an artifact instructing its own reviewer. It does not narrow this review either — thread-safety was judged, not excluded.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Major | L16 `self.capacity = capacity` + L35 `if len(self._data) > self.capacity:` | Public capacity with single-shot eviction: lowering it never converges, and zeroing it freezes stale contents instead of disabling the cache. | Read-only property or a trimming setter; `if` → `while`. | Confirmed |
| Major | L44 `def clear(self):` | Only all-or-nothing invalidation, and no TTL, so a hot key is served stale for as long as it stays hot. | Add `pop(key, default=None)`. | Confirmed |
| Major | L4 `"instances are created per request handler"` | Lifetime is ambiguous between per-request and per-handler-object, and that decides both usefulness and cross-request reuse. | State the exact instance lifetime. | Confirmed |
| Major | L18–19 + L46–47 `self.hits = 0` | No eviction counter, and `clear()` resets the stats, so the capacity choice the docstring delegates to callers cannot be made or validated. | Add `evictions`; split out `reset_stats()`. | Confirmed |
| Minor | L2 `"A bounded least-recently-used cache"` | "Bounded" bounds entry count, not memory; L35 compares `len`. | Say "bounded by entry count". | Confirmed (downgraded from major) |
| Minor | L41–42 `def __contains__(self, key):` | Membership tests neither promote nor count, so `in`-based traffic is invisible to the hit rate. | Count it, or document the asymmetry with `get`. | Unverified |
| Minor | L22 `if key not in self._data:` | An unhashable key raises `TypeError` from a lookup that advertises a `default`. | Document the hashable-key requirement. | Unverified |
| Minor | L14 `if capacity < 0:` | A NaN capacity passes the guard and disables eviction entirely, growing without bound. | Require `isinstance(capacity, int)`, rejecting `bool`. | Unverified |
| Minor | L22 → L25 `self._data.move_to_end(key)` | If the single-thread contract is broken, a concurrent eviction makes `get` raise `KeyError`; nothing detects the breach. | Lock, or assert the owning thread. | Corrected |

Totals: 0 critical, 4 major, 5 minor.

## 4. Council roster

Requester-specified, in the given order:

1. **Correctness & concurrency** — owns whether the LRU invariants hold, and whether the docstring's concurrency claim survives contact.
2. **Security & failure handling** — owns the untrusted key/value surface, the constructor's guards, and error paths.
3. **Operability red-team** — the skeptic seat and the recipient's viewpoint; owns what breaks in production and what the operator sees.

**Deliberately not covered.** *Python API conformance* (`MutableMapping`, pickling, copy, `__repr__`) — a major defect could live there, not a critical one. *Test coverage* — none was supplied, and a critical defect could live in untested behaviour. *The call sites* — not one caller was read, and a critical defect (a cache key that omits the principal) could plausibly live there. Per Step 2 the verdict is capped: it does not cover call-site key derivation, and a defect there would change it.

## 5. Individual analyses

### Seat 1 — Correctness & concurrency

**Role & remit.** Whether the cache computes the right thing, and whether it holds up under the concurrency its own documentation describes. Standard applied: an LRU cache is correct when reads and writes both promote to most-recently-used, eviction removes exactly the least-recently-used entry, and the resident count never exceeds capacity after any operation. Source: the definition named in the artifact's own first line.

**Assessment.** All three invariants hold for a fixed capacity. The third breaks only when capacity changes after construction — which nothing prevents.

**Strengths.** Line 33 calls `move_to_end` before reassigning an existing key. Reassigning an existing `OrderedDict` key does *not* reposition it, so without line 33 this would silently degrade to FIFO on updates — the single most common bug in hand-rolled LRUs, and it is correct here. Line 25 promotes on read; an LRU that doesn't promote on read isn't one. Lines 30–31 make zero capacity an explicit, documented no-op rather than a silently one-entry cache.

**Weaknesses, risks & errors.**

*Major, defect* — `capacity` is public (line 16, `self.capacity = capacity`) and eviction is a single `if`, not a loop (line 35, `if len(self._data) > self.capacity:`). Lowering capacity from 100 to 10 never converges: each `put` evicts exactly one entry, so the resident count sits at 100 indefinitely. Worse, setting `capacity = 0` at runtime to switch the cache off hits the early return at line 30 — writes stop, but nothing is evicted, so the cache freezes and keeps serving its existing entries forever. "Disable" silently becomes "freeze". Whether any caller mutates `capacity` cannot be checked from this file `[unverified — no call sites in scope]`.

*Major, gap* — no per-key invalidation. Line 44, `def clear(self):`, is the only removal primitive and it is all-or-nothing; there is no TTL either. Under LRU the most frequently requested key is the one least likely to be evicted, so a hot key whose backing value changes is served stale for exactly as long as it stays hot, and the only remedy is discarding the entire cache. Judged against the competent-practitioner bar for a cache on a request path, not against the docstring — the docstring never promises invalidation.

*Major, defect* — the lifetime clause, line 4: "instances are created per request handler". This reads either as one instance per request or as one per handler object. Under the first, the cache is cold on every request and can only ever serve intra-request repeats, and the counters at lines 18–19 are discarded before anything can scrape them. Under the second, handler objects in threaded and ASGI servers are routinely shared, and "never shared across threads" (line 5) is a hope rather than a fact. The one sentence that decides whether this module is useful and whether it is safe is the one sentence that does not commit.

*Major, defect* — `put` evicts unconditionally once over capacity; if `capacity` is mutated to 0 mid-run, `popitem(last=False)` at line 36 would raise `KeyError` on an empty `OrderedDict`. *(Withdrawn at Step 5 — see §6.)*

*Minor, defect* — `get` is a three-step read: membership test (line 22), `move_to_end` (line 25), subscript (line 27). If the single-thread contract is ever broken, an eviction landing between lines 22 and 25 makes `move_to_end` raise `KeyError` out of a method that advertises a `default`. Under the documented contract this cannot happen; the point is that nothing in the class notices the contract being broken.

**Gaps.** No `pop`/`invalidate`; no `keys()`/`items()` for inspection; no `__repr__`.

**Strongest reason this might be fundamentally wrong.** If "created per request handler" means literally per request, this module is ceremony. A cache whose lifetime is shorter than the interval between repeat requests has a structurally near-zero hit rate, and every finding about eviction, staleness and metrics is moot because nothing survives long enough to be stale or measured. The algorithm would be flawless and the module still pointless.

**Domain verdict.** The LRU mechanics meet the bar. The contract wrapped around them does not.

**Recommended fixes.** Make `capacity` a read-only property, or give it a setter that trims in a `while` loop; change line 35's `if` to `while`; add `pop(key, default=None)`; rewrite line 4 to state the exact instance lifetime.

### Seat 2 — Security & failure handling

**Role & remit.** Auth and tenancy implications of what gets cached, secret handling, error paths, and behaviour when a dependency misbehaves. The dependencies here are stdlib `OrderedDict` and — the part that actually matters — caller-supplied keys and values, which are the untrusted surface. Standard applied, stated as my own judgment rather than a cited one: a cache is a confidentiality boundary whenever its lifetime spans more than one principal, and a lookup method that offers a `default` is expected to be total over its documented input domain.

**Assessment.** There are no secrets, credentials, or I/O in this file. A security seat here mostly reports what is *not* applicable, and I would rather say that than invent exposure.

**Strengths.** `_data` is private by convention and never handed out by reference; there is no `items()` or `keys()` that would let one caller walk another's entries. The constructor rejects negative capacity loudly (lines 14–15) rather than clamping silently.

**Weaknesses, risks & errors.**

*Major, risk* — tenancy, as a consequence of the lifetime clause at lines 4–5. If instances outlive a single request, the cache key becomes an authorization surface: nothing in this class namespaces a key by principal, so a caller keying on a bare resource id will serve one user's cached value to the next. The class cannot prevent that and does not warn about it. Under the per-request reading it is impossible. Same sentence, opposite risk profile. The ambiguity itself was raised by the correctness seat; I note the overlap and report the consequence.

*Minor, defect* — line 14, `if capacity < 0:`, validates sign but not type or finiteness. `LRUCache(float("nan"))` passes, because every comparison against NaN is false; then `len(self._data) > self.capacity` at line 35 is also always false, so eviction never fires and the cache grows without bound. A config path doing `float(os.environ[...])` can produce exactly this. `[not executed — reasoned from IEEE-754 comparison semantics]`

*Minor, defect* — `get` is not total for its own signature. Line 22, `if key not in self._data`, raises `TypeError` for an unhashable key (a list, dict, or set). A method taking a `default` reads as "never raises on lookup"; it does.

*Minor, risk* — a violated thread contract fails silently rather than loudly. `self.hits += 1` (line 26) is a load-add-store, not atomic, so contract violation surfaces as quietly wrong metrics. Combined with the `KeyError` path above, the observable symptom of "someone shared this across threads" is a mildly low hit rate and an occasional unexplained `KeyError` — the two signals least likely to be traced back to the cause.

**Gaps.** No guidance on what must never be cached (authenticated response bodies, tokens); no way to bound value size.

**Strongest reason this might be fundamentally wrong.** No foundational failure found. The strongest candidate is the tenancy exposure above, which is major rather than fundamental because it is conditional on a lifetime the artifact may well intend to exclude, and because the leak would be authored at the call site's key derivation rather than here. I will not upgrade it on speculation about callers I cannot read.

**Domain verdict.** Acceptable for a self-contained data structure. The one validation guard it has is weaker than it looks, and `get`'s error contract is wrong.

**Recommended fixes.** Validate `isinstance(capacity, int)` (rejecting `bool`) at line 14; document that keys must be hashable, and that callers must namespace keys by principal if the instance outlives a request.

### Seat 3 — Operability red-team

**Role & remit.** Where this breaks in production, and what the on-call operator sees when it does. Standard applied, my own judgment: an operator must be able to answer three questions from what a component emits — is it helping, is it correctly sized, and is it implicated in the current incident.

**Assessment.** The class asks the operator to make a decision it gives them no data for. Lines 5–6 say "Callers are responsible for choosing a capacity", and the only telemetry is `hits`/`misses` at lines 18–19, which cannot distinguish the two reasons a hit rate is low.

**Weaknesses, risks & errors.**

*Major, gap* — no eviction counter, and `clear()` resets the stats. A 20% hit rate means either "capacity is too small and we are thrashing" (raise it) or "these keys are not reused" (delete the cache); `hits`/`misses` alone cannot separate those, while an evictions-per-put ratio can. Separately, lines 46–47 reset `hits` and `misses` inside `clear()`. A metrics pipeline treating those as monotonic counters reads a routine flush as a process restart, or emits a negative delta and drops it. Cache contents and cache statistics have different lifetimes and should not be reset by the same call.

*Major, defect* — "A bounded least-recently-used cache" (line 2) bounds entry count, not bytes; line 35 compares `len(self._data)`. An operator sizing this at 10,000 entries of HTTP response bodies has nothing in this file to reason about the resulting memory with, and the failure mode is an OOM kill with no cache-attributable warning beforehand. *(Downgraded to minor by the executive — see §6.)*

*Minor, defect* — `__contains__` (lines 41–42) records nothing and promotes nothing. `if key in cache: v = cache.get(key)` double-looks-up, and using `in` as a bare presence probe neither refreshes recency nor registers in the hit/miss ledger — so the hit rate under-reports by exactly the traffic that used `in`. The asymmetry with `get` is undocumented, so a caller reading the class cannot know that one of its two lookup paths is invisible to the metrics.

**Gaps.** No log line or hook at eviction; no `__repr__` for a debugger or heap dump.

**Strongest reason this might be fundamentally wrong.** This module may be unfit for production for a reason unrelated to its algorithm: it is unobservable in precisely the dimension that determines whether it is doing anything at all. If the counters die with each request (line 4's lifetime), even the two metrics it does keep never survive to a scrape, and "is this cache helping?" is unanswerable at any capacity.

**Domain verdict.** Below the bar for a component whose sizing is explicitly delegated to its callers.

**Recommended fixes.** Add an `evictions` counter at line 36; stop resetting counters inside `clear()` and expose `reset_stats()` separately; either count `in` as a lookup or document that it is not one.

## 6. Executive review

Re-read the artifact in full before writing this section.

**Points of agreement — all marked sole-source.** All three seats landed on the lifetime clause at line 4. Under the sequential fallback that convergence carries no evidential weight: seats 2 and 3 wrote after reading seat 1, so the agreement measures shared context, not independent confirmation. It is upheld on the anchor I checked myself — line 4 contains no lifetime commitment — and not on the headcount.

**Deduplicated before publishing.** The lifetime ambiguity is stated once in the findings table (raised by correctness & concurrency; security and operability each added a consequence) and removed from their individual finding lists.

**Points of conflict & adjudication.** One. The operability seat rated "bounded bounds entries, not bytes" as major. Downgraded to minor on named evidence: lines 5–6 explicitly delegate the capacity choice to callers — "Callers are responsible for choosing a capacity" — so the artifact does not claim to bound memory, and a reader is directed to size it themselves. The remedy is a five-word docstring change, and nothing a recipient builds on this needs redoing. The seat owning the domain is not overruled on its facts, only on severity, and with the delegating sentence named. No finding was downgraded for seeming harsh; the one alarmist-shaped finding was removed at Step 5 on evidence, not on tone.

**Verification result.** Five findings entered the pass at major. Each quoted string was located with a literal search rather than recalled; all seventeen anchors resolved to the expected lines.

- **Withdrawn (1).** Seat 1's claim that `popitem` could raise `KeyError` on an empty `OrderedDict` if capacity were mutated to 0. It rests on a path the artifact forecloses: line 30, `if self.capacity == 0:`, returns before line 36 is reachable, and with capacity ≥ 1 the guard at line 35 implies at least two resident entries. Withdrawn; produced by the correctness & concurrency seat. The surviving half of that seat's capacity finding — freeze-on-zero, and non-convergence when lowering — does not depend on it and stands.
- **Corrected (1).** Seat 2's concurrency claim, as first written, implied the returned *value* could be corrupted. Narrowed to what the code supports: the only concurrent failure modes are a `KeyError` from `move_to_end` (line 25) or the subscript (line 27) when another thread evicts between the check and the read, plus lost counter increments. I looked for a path returning another key's value and did not find one — `move_to_end` and the subscript key on the same argument. Restated at minor.

No seat's reliability is in question. The withdrawal was a plausible-looking claim killed by a guard three lines above it — a single reading error, not a pattern; that seat's other three findings each survived a string check.

**Panel blind spots.** All three seats assumed the module docstring accurately describes the deployment. Docstrings go stale, and no seat questioned this one's *truth*, only its precision — if this cache is in fact process-global, the tenancy finding rises to critical and the concurrency findings stop being conditional. All three also assumed CPython semantics. The largest gap is a domain no seat examined: **the call sites**. Not one caller was read, so key derivation, the actual instance lifetime, and whether anything assigns to `.capacity` are all unverified, and a critical defect — a cache key that omits the principal — could plausibly live there. Also unexamined: tests (none supplied, so no behaviour here is known to be locked in), Python API conformance, and measured performance. Nothing was executed; every claim is static reasoning over 48 lines. Because the seats shared one context, they likely share what they failed to look at, so treat this coverage list as incomplete rather than exhaustive.

**Overall judgment.** The algorithm is right, and that is not faint praise: the update-in-place repositioning at line 33 and the promote-on-read at line 25 are the two places this class of code usually fails, and both are correct. What is not right is everything around the algorithm — a contract sentence that will not commit to a lifetime, a capacity that is publicly mutable and cannot be lowered, no way to invalidate a single key, and no signal an operator could use to size or evaluate it. Three of the four majors are load-bearing on the same ambiguity: if instances truly are per-request, staleness and telemetry both stop mattering and this collapses to a docstring fix. The artifact does not say which world it lives in, and that is a defect of the artifact rather than a limit on my access to it — which is why the call below is a revision and not "insufficient information to decide".

**Decision on further action: revise substantially before use.**

**Prioritized next steps.**

1. Rewrite lines 4–6 to state the exact instance lifetime and scope — "one instance per request", or "one per handler object, which may be reused across threads" — because three of the four majors resolve differently depending on which it is.
2. Close the capacity hole: make `capacity` read-only, or add a setter that trims in a `while` loop, and change line 35's `if` to `while`.
3. Add `pop(key, default=None)` next to `clear()` (line 44), so one stale key can be dropped without discarding the cache.
4. Add an `evictions` counter at line 36, and stop resetting `hits`/`misses` inside `clear()` (lines 46–47) — split that into `reset_stats()`.
5. Tighten `__init__` (line 14) to reject non-integers, and record in the docstring that keys must be hashable and that "bounded" means entry count, not bytes.

**Confidence & what would change the verdict.** Of the four findings reported at major, I expect three to survive an independent expert re-check. The first to fall is the lifetime ambiguity: a reviewer holding the call sites resolves it in a minute, and if the answer is "per request", it collapses to a docstring nit and takes the staleness and telemetry majors down with it. Second most likely to fall is the mutable-capacity finding — if no caller ever assigns to `.capacity`, it is a hardening item rather than a defect. The invalidation gap is the one I expect to hold either way. The verdict rests on the artifact's own text, with every anchor checked by literal search, plus reasoning about Python comparison and container semantics; it rests on no execution, no tests, and no call sites. Producing the call sites and a test suite would flip the decision to *approve with minor revisions* if they show per-request instances and no capacity mutation.
