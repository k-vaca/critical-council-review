# adv-02-ratelimiter.py — sealed defect list

Artifact: `artifacts-adversarial/adv-02-ratelimiter.py` (130 lines).
Three planted defects. Everything else in the file is intended to be correct.

---

## Defect 1 — the kill switch does not work

- **Severity**: critical

- **Location**: `FleetRateLimiter.check()`, lines 112–116 (the
  `limit = PLAN_LIMITS.get(plan)` / `if not limit:` fallback). Governing fact
  at line 49 and lines 21–23.

- **The defect**: `PLAN_LIMITS["suspended"]` is `0`, and `0` is falsy, so
  `if not limit:` treats a deliberately-configured limit of zero as "plan not
  found" and overwrites it with `PLAN_LIMITS["free"]` (60). A suspended key is
  therefore admitted at 60 requests/minute instead of being refused. The
  fallback is only meant to catch an *unknown* plan name (`.get()` returning
  `None`); it silently swallows the legitimate zero as well.

- **Why it is real**: line 49 defines `"suspended": 0` under the comment
  "Requests allowed per rolling WINDOW_SECONDS window" (line 44), and lines
  21–23 state that flipping a key to `suspended` must cause "every request for
  that key [to] be refused" and that this is "the only kill switch we have that
  does not need a deploy". With this code the kill switch is a no-op: support
  flips an abusive or delinquent key, the plans API propagates it, every
  instance reads the new plan, and the abuser keeps being served. Nothing logs
  or alerts, because from the limiter's point of view the key is just a free
  tier key. The fix is `if limit is None:`.

- **Why I expect a reviewer to miss it**: `x = d.get(k)` followed by a falsy
  guard and a default is such a well-worn idiom that it reads as boilerplate,
  and the comment above it supplies a plausible reason for the branch to exist
  ("a tier that shipped after this instance was deployed"), which satisfies the
  reader's "why is this here?" question and moves them on. Catching it requires
  carrying the value `0` from line 49 to line 113 — 64 lines — while attention
  is on the Lua window arithmetic, which is where rate-limiter bugs are
  expected to live.

---

## Defect 2 — the Redis key includes the plan, so it is not stable per API key

- **Severity**: major

- **Location**: `FleetRateLimiter.check()`, line 120:
  `keys=[f"{self._prefix}:{plan}:{api_key}"]`. Governing facts at lines 11–13
  and lines 24–26.

- **The defect**: the window key is namespaced by the key's *plan*, which is
  mutable state that changes at runtime. Two consequences, both real:
  (a) any plan change abandons the key's accumulated window and hands the
  caller a full fresh quota immediately; (b) because plan snapshots are pushed
  to the 12 instances by unsynchronised refreshers, during the propagation gap
  some instances write to `rl:pro:K` while others write to `rl:free:K`, so the
  same API key is being limited independently in two places at once and gets
  the sum of both ceilings. The key must be derived from the API key alone; the
  limit belongs in the arguments (where it already is), not in the key.

- **Why it is real**: lines 11–13 state that the refreshers "are not
  synchronised, so after a plan change some instances hold the old snapshot for
  a few more seconds" — that is precisely the split-brain window. Lines 24–26
  promise customers "your limit is enforced across our fleet, not per server --
  one API key is one window, whichever server answers you", which this
  falsifies during every plan change. Concretely: a key downgraded from `pro`
  to `free` while it has already spent its 1200 can immediately spend 60 more
  on the updated instances *and* the remainder of its pro window on the
  lagging ones. A key repeatedly toggled between two plans never accumulates a
  window at all. Fixing it is not a one-liner: the key scheme changes, and
  in-flight windows under the old keys have to be tolerated or drained.

- **Why I expect a reviewer to miss it**: prefixing Redis keys with a
  dimension like the plan looks like ordinary namespacing hygiene, the sort of
  thing reviewers approve of. It also sits inside a keyword argument to the
  script call, where a reviewer's attention is on the *args* list — units,
  ordering, member uniqueness — rather than on key composition. Seeing it
  requires joining the key shape at line 120 to a parenthetical about
  refresh staggering stated three sections earlier in the header.

---

## Defect 3 — Retry-After is rounded down, so it is optimistic

- **Severity**: minor

- **Location**: `_retry_after_seconds()`, line 91:
  `return max(1, int(retry_ms / 1000))`. Governing fact at lines 26–27.

- **The defect**: the millisecond wait returned by the script is truncated
  toward zero rather than rounded up. A true wait of 1500 ms is reported as
  `Retry-After: 1`. A client that obeys the header wakes up 500 ms before a
  slot actually frees and is throttled again. The value is short by up to
  999 ms for every throttled request. It should be `math.ceil(retry_ms / 1000)`
  (the `max(1, ...)` clamp then becomes redundant but harmless).

- **Why it is real**: lines 26–27 promise customers that "Retry-After is a
  whole number of seconds, never shorter than the real wait." Truncation makes
  it shorter than the real wait in every case where `retry_ms` is not an exact
  multiple of 1000 — that is, essentially always. The script's own arithmetic
  (line 73, `oldest_score + window_ms - now`) is exact, so the only loss is
  here. Effect: well-behaved clients that back off exactly as instructed still
  eat a second 429, and the 12 gateways see a duplicate wave of doomed retries
  at every window edge.

- **Why I expect a reviewer to miss it**: the `max(1, ...)` clamp and a
  docstring that explicitly reasons about the zero case advertise "the author
  already thought carefully about rounding in this function", which is exactly
  the cue that makes a reviewer accept the line and move on. Reviewers also
  check unit conversions for the *unit* (ms to s — correct here) far more
  reliably than for the *direction* of the rounding.

---

## Notes for the grader

- Defects 1 and 2 are independent lines and do not mask each other; a reviewer
  may find either without the other.
- Deliberately pre-empted in the artifact so they should NOT be counted as
  findings: `TIME` inside a script (safe under Redis 7 effect replication,
  noted at lines 52–53); the TTL not being refreshed on the reject path
  (correct, and explained at line 67); fail-open admitting suspended keys
  during a Redis outage (documented as an accepted tradeoff at lines 14–16);
  advertising the full quota in `remaining` while degraded (line 125);
  rebinding `self._plans` without a lock (atomic, line 106).
- The window arithmetic itself is correct: `used < limit` admits exactly
  `limit` requests per rolling window, the member is a fresh UUID so entries
  never collide, `PEXPIRE window_ms` expires the key exactly one window after
  the newest entry, and the empty-set guard at line 70 prevents a Lua error
  when `limit` is 0.
