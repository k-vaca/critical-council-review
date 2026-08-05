# Review — adv-02-ratelimiter.py

Artifact: `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts-adversarial/adv-02-ratelimiter.py`

Reviewed by tracing the implementation against every constraint and promise stated in the module
docstring (12 stateless gateways / one Redis 7 primary / Redis-only clock; unsynchronised ~30 s plan
refreshers; unconditional fail-open; rolling 60 s window; "suspended" as the only no-deploy kill
switch; and the three published guarantees at docs.example.com/limits).

Verdict: the Redis-side mechanics are competently built — the Lua script is genuinely atomic, uses
`TIME` correctly as the single clock, and honours "requests we reject do not count against your
quota". But the Python wrapper breaks two of the header's load-bearing guarantees, one of them the
kill switch itself.

---

## Findings

### 1. CRITICAL — `FleetRateLimiter.check`, lines 112–116: the suspended kill switch never fires

Anchor:

> `limit = PLAN_LIMITS.get(plan)` … `if not limit:` … `limit = PLAN_LIMITS[DEFAULT_PLAN]`

`PLAN_LIMITS["suspended"]` is `0`, which is falsy, so the guard that was written to catch an
*unknown* plan (`None`) also catches the *known* suspended plan and silently re-maps it to the free
ceiling of 60 requests per minute — the header says every request for a suspended key "must then be
refused", and states this is the only kill switch that does not need a deploy, so an abusive or
delinquent key keeps sailing through at 60 rq/min on every one of the 12 gateways. The test must be
`if limit is None:`.

### 2. CRITICAL — `FleetRateLimiter.check`, line 120: the plan name is part of the Redis key

Anchor:

> `keys=[f"{self._prefix}:{plan}:{api_key}"]`

The window is keyed by a *mutable* attribute of the key rather than by the key alone, so one API key
maps to as many windows as it has had plans. Two consequences, both of which the header specifically
sets up:

* The refreshers are explicitly documented as unsynchronised, so for several seconds after a plan
  change some instances resolve `free` and others `pro` for the same api_key. Those instances then
  count into *different* ZSETs concurrently, and the caller gets the sum of both ceilings. That is a
  direct violation of the published promise "your limit is enforced across our fleet, not per
  server — one API key is one window, whichever server answers you."
* Even after the fleet converges, any plan transition starts from an empty ZSET, so usage already
  spent under the old plan is wiped. A key downgraded mid-window gets a full fresh allowance
  immediately, and the stranded old-plan ZSET keeps its own TTL.

The key should be `f"{self._prefix}:{api_key}"`, with the plan supplying only the `limit` argument.

### 3. MAJOR — `_retry_after_seconds`, line 91: Retry-After is rounded down, not up

Anchor:

> `return max(1, int(retry_ms / 1000))`

`int()` truncates toward zero, so every non-integral wait is advertised shorter than the real one —
4 500 ms of remaining wait is reported as `Retry-After: 4`. The header promises "Retry-After is a
whole number of seconds, never shorter than the real wait", and the function's own docstring
restates the intent, but the `max(1, …)` floor only rescues the sub-second case; every other value
is under-reported by up to 999 ms. A compliant client retries early and is rejected again. Needs
`math.ceil(retry_ms / 1000)` (still floored at 1). Arguably critical, since it emits a customer-
visible header that contradicts published documentation on essentially every throttled request;
graded major because the limiter's own accounting stays correct and the wasted retry is itself not
charged against quota.

### 4. MINOR — `FleetRateLimiter.check`, line 123: the fail-open catch is wider than "unreachable"

Anchor:

> `except redis.RedisError:`

The header authorises unconditional fail-open when Redis is *unreachable*. `RedisError` is the base
class, so this also swallows `ResponseError` — a maxmemory OOM rejection of the `ZADD`, a `WRONGTYPE`
on a clobbered key, or a bug introduced in the Lua script. Those are not outages and will not
self-heal: the limiter would sit permanently wide open across all 12 instances with nothing but a
warning line to show for it. Catching `redis.ConnectionError`/`redis.TimeoutError` for the fail-open
path and letting (or at least alerting on) other `RedisError`s distinguishes the two.

### 5. MINOR — `FleetRateLimiter.check`, line 124: one traceback per request during an outage

Anchor:

> `log.warning("rate limiter degraded, admitting request", exc_info=True)`

This logs a full stack trace on every single request while Redis is down, on all 12 gateways at full
production traffic. The stated goal of the fail-open path is that "a limiter outage must not become
an API outage"; unbounded traceback logging is a plausible way for it to become one anyway (disk,
log-pipeline backpressure, CPU on formatting). Rate-limit or sample the warning, or drop `exc_info`
and emit a counter instead.

---

## Traced and found correct (not defects)

Recorded so the absence of a finding is not mistaken for an oversight:

* **Fail-open on Redis failure is sanctioned, not a security hole.** The header states it explicitly,
  including that the abuse team accepts suspended keys getting through during an outage. Finding 4
  is about the *breadth of the catch*, not the policy.
* **"Requests we reject do not count against your quota" is honoured.** `ZADD`/`PEXPIRE` occur only
  inside the `used < limit` branch; the rejection path touches neither the set nor its TTL.
* **The clock is correct.** `redis.call('TIME')` is read once inside the script and used for the
  trim, the score, and the retry computation, so the ~250 ms inter-gateway drift is irrelevant, and
  the comment about Redis 7 effect replication making a non-deterministic read safe before writes is
  accurate.
* **Atomicity holds.** Trim, count, and admit run in a single script invocation, so concurrent
  gateways cannot both consume the last slot.
* **TTL arithmetic is right.** `PEXPIRE window_ms` at each admit expires the key exactly when the
  newest entry would age out, so no live window data is dropped early.
* **`retry_ms` cannot be zero or negative.** `ZREMRANGEBYSCORE` uses the same `now`, so any surviving
  oldest score is strictly greater than `now - window_ms`.
* **`remaining` arithmetic is right.** `limit - used - 1` accounts for the request just admitted.
* **`update_plans` docstring claim is true.** The replacement dict is fully constructed before the
  attribute is rebound, and `check` reads `self._plans` once, so no caller observes a partial map.
* **No empty/missing api_key handling needed.** The header guarantees the gateway authenticates
  first and the id is always resolved and non-empty.

---

## Totals

critical = 2, major = 1, minor = 2
