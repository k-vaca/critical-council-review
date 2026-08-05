"""
Distributed rate limiter for the public API gateway.

Context
-------
* 12 stateless gateway instances behind the ALB; any of them can answer any
  request for any API key, and one Redis 7 primary backs all twelve. Gateway
  clocks are NTP-synced but drift ~250 ms against each other, so the script
  below timestamps from redis TIME: Redis is the only clock here.
* The gateway authenticates first: api_key is always a resolved, non-empty id.
* A background refresher pushes a plan snapshot into each instance via
  update_plans() every ~30 s. The refreshers are not synchronised, so after a
  plan change some instances hold the old snapshot for a few more seconds.
* If Redis is unreachable we fail open, unconditionally: a limiter outage must
  not become an API outage, and the abuse team accepts that a brief outage
  lets even suspended keys through.

Contract
--------
* Rolling 60 s window per API key; the key's plan picks the ceiling.
* "suspended" is a real plan. Support flips an abusive or delinquent key to it
  through the plans API, and every request for that key must then be refused.
  It is the only kill switch we have that does not need a deploy.
* Promised at docs.example.com/limits: "your limit is enforced across our
  fleet, not per server -- one API key is one window, whichever server answers
  you"; "requests we reject do not count against your quota"; "Retry-After is
  a whole number of seconds, never shorter than the real wait."
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Mapping
from dataclasses import dataclass

import redis

log = logging.getLogger(__name__)

WINDOW_SECONDS = 60
DEFAULT_PLAN = "free"

# Requests allowed per rolling WINDOW_SECONDS window.
PLAN_LIMITS: Mapping[str, int] = {
    "free": 60,
    "pro": 1200,
    "enterprise": 6000,
    "suspended": 0,
}

# Atomic check-and-admit, returns {allowed, remaining, retry_ms}. Redis 7
# replicates script effects, so reading TIME in here is safe.
_CHECK_SCRIPT = """
local window_ms = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
local clock = redis.call('TIME')
local now = tonumber(clock[1]) * 1000 + math.floor(tonumber(clock[2]) / 1000)
redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, now - window_ms)
local used = redis.call('ZCARD', KEYS[1])
if used < limit then
    redis.call('ZADD', KEYS[1], now, ARGV[3])
    redis.call('PEXPIRE', KEYS[1], window_ms)
    return {1, limit - used - 1, 0}
end

-- Nothing admitted: the set and its TTL are untouched. Say when the oldest
-- entry ages out of the window, which is when a slot frees up.
local oldest = redis.call('ZRANGE', KEYS[1], 0, 0, 'WITHSCORES')
if oldest[2] == nil then
    return {0, 0, window_ms}
end
return {0, 0, tonumber(oldest[2]) + window_ms - now}
"""


@dataclass(frozen=True)
class Decision:
    allowed: bool
    limit: int
    remaining: int
    retry_after: int  # whole seconds, sent as Retry-After; 0 when allowed
    degraded: bool = False


def _retry_after_seconds(retry_ms: int) -> int:
    """Whole seconds a throttled caller should sleep.

    Never 0: a client told to wait zero seconds hot-loops all 12 gateways.
    """
    return max(1, int(retry_ms / 1000))


class FleetRateLimiter:
    """Rolling-window limiter shared by every gateway instance."""

    def __init__(self, client: redis.Redis, plans: Mapping[str, str],
                 prefix: str = "rl") -> None:
        self._prefix = prefix
        self._plans = dict(plans)
        self._script = client.register_script(_CHECK_SCRIPT)

    def update_plans(self, plans: Mapping[str, str]) -> None:
        """Install a fresh api_key -> plan snapshot from the refresher.

        Rebinding is atomic: a concurrent check() never sees a partial dict.
        """
        self._plans = dict(plans)

    def check(self, api_key: str) -> Decision:
        plan = self._plans.get(api_key, DEFAULT_PLAN)
        limit = PLAN_LIMITS.get(plan)
        if not limit:
            # A tier that shipped after this instance was deployed; hold the
            # caller to the cheapest ceiling until the next refresh lands.
            limit = PLAN_LIMITS[DEFAULT_PLAN]

        try:
            allowed, remaining, retry_ms = self._script(
                keys=[f"{self._prefix}:{plan}:{api_key}"],
                args=[WINDOW_SECONDS * 1000, limit, uuid.uuid4().hex],
            )
        except redis.RedisError:
            log.warning("rate limiter degraded, admitting request", exc_info=True)
            # Not counting while degraded, so advertise the untouched quota.
            return Decision(True, limit, limit, 0, degraded=True)

        if allowed:
            return Decision(True, limit, remaining, 0)
        return Decision(False, limit, 0, _retry_after_seconds(retry_ms))
