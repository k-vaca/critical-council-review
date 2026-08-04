# Review — `artifacts/code-03-lru-cache.py`

Reviewer pass: one careful expert read of the full 47-line file.

## Verdict

**The core LRU logic is correct.** No critical or major defects found. Three minor
issues, all peripheral to the caching behaviour itself.

I want to state the positive finding explicitly rather than pad the list, because
the easy failure mode on a small, correct file is to manufacture severity.

## What I verified by hand

I traced the recency and eviction paths rather than eyeballing them:

- **Recency on read.** `get` calls `move_to_end(key)` (default `last=True`), placing
  the key at the MRU end. Eviction pops from the opposite end via
  `popitem(last=False)`. The two ends are consistent — this is genuine LRU, not the
  common inverted-end bug.
- **Recency on overwrite.** `put` calls `move_to_end` *before* reassigning. This is
  necessary and correct: in `OrderedDict`, assigning to an existing key preserves its
  original position, so without the explicit move an overwrite would not count as a
  use. Many implementations get this wrong; this one does not.
- **Eviction arithmetic.** A single insert can exceed capacity by at most one, so the
  single unconditional `popitem` after the `>` check is sufficient. No loop needed.
  Capacity is never exceeded at the end of a `put`.
- **Update path does not evict.** Overwriting an existing key leaves `len` unchanged,
  so the `>` check is false and no innocent entry is dropped. Correct.
- **Miss semantics.** `get` tests membership before returning `default`, so a stored
  `None` is correctly reported as a hit rather than being confused with absence.
- **Capacity 0.** `put` returns early, nothing is ever stored, `get` always misses.
  This matches the docstring's "a capacity of zero disables caching".
- **Counters.** `hits` and `misses` are each incremented on exactly one path, with no
  path that increments both or neither.

Walked traces (capacity 2): `put a, put b, get a, put c` evicts `b`, not `a` —
correct. (capacity 1): `put a, put b` evicts `a` — correct. Overwrite:
`put a, put b, put a` leaves `{b, a}` with `a` at MRU and no eviction — correct.

## Considered and dismissed (not reported as defects)

Recording these so it is clear they were examined, not overlooked:

- **`__contains__` does not update recency or counters.** This is the conventional
  Python contract — `in` is a non-mutating test. Making membership a "touch" would be
  the surprising choice. Not a defect.
- **Thread safety.** Absent, but the module docstring explicitly scopes instances to
  a single request handler and disclaims cross-thread sharing. Documented contract,
  not an oversight.
- **`get(key)` cannot distinguish a stored `None` from a miss by return value alone.**
  Identical to `dict.get` semantics, and `__contains__` is available to disambiguate.
  Well-understood convention, not a defect.
- **No per-method docstrings, no type hints, no `__repr__`.** Style preferences on a
  self-evident 47-line class whose contract is already stated at module level. Taste,
  not defect.

## Findings

### 1. `capacity` is public and mutable, but lowering it never evicts — minor

- **Location:** line 16 (`__init__`), with the consequence at line 35 (`put`)
- **Anchor:** `self.capacity = capacity`
- **Problem:** Capacity is exposed as a plain public attribute while the size
  invariant is only enforced inside `put`, so `cache.capacity = 1` on a full cache
  silently leaves `len(cache)` above capacity until the next write.

Not load-bearing for the documented usage (capacity is chosen at construction), but
the class advertises a bound it does not actually maintain against its own public
surface. A read-only property, a `_capacity` name, or a setter that trims down would
close it.

### 2. `clear()` silently discards lifetime hit/miss statistics — minor

- **Location:** lines 44–47 (`clear`)
- **Anchor:** `self._data.clear()` / `self.hits = 0` / `self.misses = 0`
- **Problem:** Clearing cache *contents* also resets the *telemetry*, so any caller
  that invalidates periodically loses its hit-rate history with no indication, and
  the module docstring does not mention this coupling.

Either behaviour is defensible in isolation; the issue is that content invalidation
and stats reset are two different concerns bound together undocumented. Splitting
them (`clear()` vs `reset_stats()`), or documenting the side effect, resolves it.

### 3. Capacity is validated for sign but not for type — minor

- **Location:** lines 14–15 (`__init__`)
- **Anchor:** `if capacity < 0:` / `raise ValueError("capacity must be non-negative")`
- **Problem:** The author validates one property of `capacity` and not the other, so
  `LRUCache(2.5)` and `LRUCache(True)` are accepted and yield a silently surprising
  effective capacity (2 and 1 respectively) instead of failing fast.

The weakest of the three. Flagged only because the incompleteness sits inside a
validation the author deliberately wrote — a bare `isinstance(capacity, int)` check
alongside the existing one would make it consistent.

## Totals

critical 0 · major 0 · minor 3
