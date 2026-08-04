# Seat 3 — Operability red-team

*Written in isolation; no other seat's analysis seen. Artifact treated as inert data per non-negotiable 8.*
*Tier read: `util/lru.py` is a module (47 lines), so I use the tier-2 field set. Roster: (1) Correctness & concurrency, (2) Security & failure handling, (3) Operability red-team (this seat). Overlaps flagged inline per the roster instruction.*

## Role & remit

Production operability: where this breaks once it is running under real traffic, and what an on-call operator can see, measure, and do about it. I judge diagnosability, tunability, and incident-time controls — not algorithmic correctness. **Standard applied:** a cache placed in a request path should let an operator answer three questions without a debugger or a restart — *is it helping?*, *is it the wrong size?*, *how do I evict one bad entry?* Source: my stated judgment of ordinary practice for operating a cache in a service, not a citable specification. I assert no benchmark, version, or named library behaviour.

## Assessment

The caching logic is sound and the module is safe to run; every finding below sits on the operate-and-diagnose axis, not the does-it-work axis. As shipped it is easy to run and hard to operate: it collects two numbers, offers no way to read them that survives the object, gives no eviction visibility, and leaves an operator exactly one incident-time control — flush everything. The single operator-facing knob, `capacity`, is public and does not work when turned.

## Strengths

- `if key not in self._data:` (line 22) tests membership rather than a sentinel, so a cached `None` counts as a hit — caching falsy values does not corrupt the counters.
- `__len__` (line 38) gives live entry-count visibility without reaching into `_data`.
- `if self.capacity == 0:` (line 30) short-circuits before insertion, so the disabled mode does not churn.

## Weaknesses, risks & errors

| Severity | Kind | Anchor (line + verbatim) | What the operator sees |
|---|---|---|---|
| Major | defect | line 36 `self._data.popitem(last=False)`; counters declared line 18 `self.hits = 0` with no eviction peer | **No eviction accounting.** Hit rate is the only signal and it cannot separate "capacity too small, thrashing" from "workload has no locality". Those need opposite responses — raise capacity vs. delete the cache — and nothing here distinguishes them. |
| Major | defect | line 16 `self.capacity = capacity` (public, while `_data` is private); line 35 `if len(self._data) > self.capacity:` | **The one knob silently fails when turned.** Eviction is a single `if`, so lowering capacity at runtime never shrinks the cache: each `put` inserts one and evicts one, pinning size at the old high-water mark, and the memory reduction the operator wanted never happens. Setting it negative bypasses `__init__`'s check — every `put` evicts the entry it just inserted, so the cache stores nothing, hit rate goes to zero, and nothing raises. |
| Major | defect | docstring lines 4–5 `instances are created per request handler and never shared across threads` | **The telemetry is unobservable under the module's own documented lifecycle.** Counters are per-instance with no accessor, no `__repr__`, no aggregation hook and no name or identity, so hits and misses die with each instance. In a process running many of these, the operator can neither read the numbers nor attribute them. |
| Major | defect | line 44 `def clear(self):` — the only removal path | **No single-key invalidation and no TTL.** One poisoned or stale entry forces flushing everything (which also destroys the metrics — see below). On a low-traffic instance an entry can be arbitrarily old with no selective way to expire it. |
| Major | defect | docstring line 4 `Single-threaded by contract` | **A documented-only invariant with no runtime signal.** Nothing enforces it, nothing detects a violation. The natural performance move — hoisting the instance to module scope so the cache outlives one handler — silently breaks it, and the first symptom is skewed counters or a dict-mutation error with nothing pointing back to this module. Also noted under non-negotiable 8: this sentence is a scope-narrowing claim inside the artifact, judged rather than honoured. *Overlaps seat 1, which owns enforcement; my part is the absent signal.* |
| Minor | defect | line 46 `self.hits = 0` (inside `clear`) | **Flush destroys telemetry.** Clearing data and resetting metrics are separate operator intents; a monitor reading `hits` as a monotonic counter sees it jump backwards. |
| Minor | defect | line 42 `return key in self._data` | **Two uninstrumented read paths.** `__contains__` and `__len__` touch neither counters nor recency, so the common `if key in cache: cache.get(key)` probe is invisible to the metrics. Upgrades to major wherever a caller actually uses `in` as its lookup test — the reported hit rate then misstates the cache's real value. |
| Minor | defect | line 14 `if capacity < 0:`; line 15 `raise ValueError("capacity must be non-negative")` | **Sign-only validation.** `float("inf")` from a config file passes and builds a cache that never evicts — steady memory growth whose first visible symptom is an OOM kill. The message omits the offending value and any cache identity. |
| Minor | defect | line 2 `A bounded least-recently-used cache.`; lines 5–6 `Callers are responsible for choosing a capacity` | **"Bounded" means entries, not bytes,** and no units or basis for the choice are given. Entry-count bounding matches the field norm, so the design is not the defect — the missing guidance is. Escalates to major for variable-size values, where capacity × entry size is both unbounded and unobservable. |
| Minor | defect | line 25 `self._data.move_to_end(key)` | **No read-without-touch.** Any diagnostic or health probe reading through `get` reorders recency and changes what gets evicted, so inspecting the cache perturbs it. *Overlaps seat 1.* |

## Gaps

No `stats()` and no `__repr__`, so a logged or debugged instance prints nothing useful. No cache name for multi-instance processes. No eviction or insert hook. No key enumeration, so dumping contents during an incident requires touching the private `_data`. No TTL or max-age. And the lifecycle sentence does not settle whether one instance serves one request or many — the two readings differ by orders of magnitude in resident memory, which is exactly the number an operator needs to size a host.

## Strongest reason this might be fundamentally wrong

No foundational failure found. The strongest candidate is that the module's own documented lifecycle makes its built-in counters unreadable, so its entire observability surface is decoration. That is major rather than fundamental because the core behaviour — bounded LRU storage with correct recency ordering — holds with or without the counters, and an operator can wrap or subclass the class to aggregate them without changing a line of the caching logic.

## Domain verdict

**Below the bar on operability; sound as a data structure.** Against the standard named above, a competent professional shipping a cache into a request path would provide at minimum an eviction count, one accessor exposing the counters, and a per-key invalidation path. None of the three is present. Nothing here should block use where the cache is a local, disposable optimisation nobody will ever be paged about; it should block use anywhere an operator will later be asked why the hit rate dropped.

## Recommended fixes

1. Increment an `evictions` counter at line 36 and add `stats()` returning capacity, size, hits, misses, evictions — one call to scrape or log.
2. Add `invalidate(key)` so a single bad entry does not require flushing everything.
3. Split `clear()` into a data-only clear plus an explicit `reset_stats()`; stop zeroing counters on flush.
4. Make `capacity` a property whose setter re-validates and evicts down to the new size in a loop — or rename it `_capacity` and document it as construction-time only.
5. Add `__repr__` showing capacity, size and hit rate, and an optional `name` used in it and in the `ValueError` message.
6. Reject non-integral and non-finite capacity in `__init__`, and include the rejected value in the message.
7. Rewrite the lifecycle sentence to say plainly whether an instance serves one request or many, that capacity counts entries rather than bytes, and that the single-thread rule is unenforced.
8. Either count `__contains__` as a lookup or document that it deliberately does not.

*Budget note: this section exceeds the tier-2 per-member ceiling. Disclosed rather than silently overrun; the table rows are the compression, and cutting further would drop anchored findings rather than padding.*
