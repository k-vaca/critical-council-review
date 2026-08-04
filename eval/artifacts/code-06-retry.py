# net/retry.py
"""Retry helper for calls to the payments provider.

The provider's published guidance: retry on 429 and on 5xx, back off
exponentially, add jitter so that a fleet recovering from an outage does
not synchronise. Do not retry 4xx other than 429 — those are permanent.

This helper wraps every charge, refund, and payout call the billing
worker makes. The worker holds a database row lock for the duration of
the wrapped call so that a charge cannot be issued twice.
"""

import random
import time

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
BASE_DELAY = 0.5
MAX_DELAY = 30.0
MAX_ATTEMPTS = 8


class PermanentError(Exception):
    pass


class TransientError(Exception):
    def __init__(self, status):
        super().__init__(f"transient upstream status {status}")
        self.status = status


def call_with_retry(fn, *args, **kwargs):
    """Call fn(*args, **kwargs); retry transient failures.

    fn must return an object with a `.status_code` attribute and must be
    safe to call more than once with the same arguments.
    """
    last_status = None

    for attempt in range(MAX_ATTEMPTS):
        resp = fn(*args, **kwargs)

        if resp.status_code < 400:
            return resp

        if resp.status_code not in RETRYABLE_STATUS:
            raise PermanentError(f"upstream status {resp.status_code}")

        last_status = resp.status_code

        if attempt == MAX_ATTEMPTS - 1:
            break

        delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
        time.sleep(random.uniform(0, delay))

    raise TransientError(last_status)
