# Review — `net/retry.py` (code-06-retry.py)

Single expert pass. Reviewed against the contract the module states about itself:
it wraps **every charge, refund, and payout call** the billing worker makes, and the
worker **holds a database row lock for the duration of the wrapped call**.

## Summary

The backoff mathematics are correct and the jitter strategy is sound (full jitter,
`uniform(0, delay)`, which is the AWS-recommended form and genuinely does desynchronise a
recovering fleet — the docstring's stated goal is met). Exponential growth, the `MAX_DELAY`
cap, and the "sleep between attempts but not after the last one" structure are all right.

The problems are not in the arithmetic. They are in what the retry loop is being asked to
retry. This helper sits in front of money movement, and it retries `500/502/503/504` on
non-idempotent operations with no idempotency key and no way for the caller to learn that a
retried request may have been applied upstream. That is the finding that matters; everything
else below is secondary.

---

## Findings

### C1 — CRITICAL — `call_with_retry`, lines 40–55 (retry of 5xx on charge/payout calls)

**Anchor:** `"The worker holds a database row lock for the duration of the wrapped call so that a charge cannot be issued twice."`

**Problem:** The row lock prevents *concurrent workers* from issuing the same charge, but it
does nothing about this loop re-issuing the same charge up to eight times inside one lock
hold, so a 502/504 on a charge that the provider actually processed produces a double charge.

**Detail.** `500`, `502`, `503`, `504` are all in `RETRYABLE_STATUS`. Of these, only `429`
(and arguably a clean `503` from the edge) reliably means "the provider did not process your
request." A `504` is precisely the case where the request *was* forwarded to the payments
backend, may have been fully applied, and the gateway simply stopped waiting for the answer.
A `502` from an edge proxy is the same story. Retrying that request byte-for-byte charges the
customer again.

The module has two defences against this and neither holds:

1. The docstring's claim that the row lock means "a charge cannot be issued twice." A row lock
   serialises writers against *your* database row. It has no relationship to how many HTTP
   requests you send to the provider while you hold it. The sentence is a false reassurance,
   and it is load-bearing — it is the reason a reader would accept this loop as safe.
2. The precondition on line 36, `"must be safe to call more than once with the same arguments"`.
   This is unenforced and unenforceable at this layer, and it is in direct tension with the
   module docstring's statement that the helper wraps charges and payouts, which are the
   canonical non-idempotent operations.

There is no idempotency key anywhere in the design — not generated here, not required of the
caller, not documented as a precondition. Every serious payments provider supports one
precisely so that this retry loop is safe; the correct shape is to require the caller to pass
a stable idempotency key per logical operation and to refuse to retry 5xx without one.

A second consequence, same root cause: when retries are exhausted the caller receives
`TransientError(last_status)` carrying only an integer. The caller cannot distinguish
"definitely not charged, safe to re-enqueue" from "may have been charged, must reconcile
before re-enqueuing." A worker that treats `TransientError` as "retry later" — the obvious
reading of the name — will double-charge on the next pass as well.

**Fix direction:** require an idempotency key for any 5xx retry; without one, retry `429`
only and surface 5xx as an indeterminate outcome that forces reconciliation rather than a
blind retry.

---

### M1 — MAJOR — line 16, `RETRYABLE_STATUS`

**Anchor:** `RETRYABLE_STATUS = {429, 500, 502, 503, 504}`

**Problem:** The set contradicts the retry policy stated four lines above it ("retry on 429 and
on 5xx"), so genuinely transient 5xx codes outside the allowlist are converted into a
permanent failure.

**Detail.** `507`, `508`, `509`, and the Cloudflare-family `520`–`527` (notably `522`
connection timed out and `524` origin timed out) are all 5xx and all transient, and all of
them fall through to line 47 and raise `PermanentError`. For a billing worker, `PermanentError`
on a payout almost certainly means "mark failed and stop," so a transient edge blip becomes a
permanently failed payment.

Note the interaction with C1: `522`/`524` are timeout semantics, so they are simultaneously
the codes most likely to indicate an *applied* charge. Whichever way this is resolved, the
docstring and the constant must be made to agree — right now a reader cannot tell which one
states the intended policy, and the two lead to opposite behaviour.

---

### M2 — MAJOR — line 41 (no exception handling around `fn`)

**Anchor:** `resp = fn(*args, **kwargs)`

**Problem:** Any exception raised by `fn` — connection reset, DNS failure, TLS error, client-side
read timeout — propagates straight out of the loop, so the most common class of transient
failure is never retried at all.

**Detail.** The function's own docstring promises to "retry transient failures." In practice a
provider outage rarely presents as a tidy `503`; it presents as connections refused, resets
mid-flight, and read timeouts. None of those reach line 43. The caller gets a raw
`ConnectionError`/`Timeout` from whatever HTTP library `fn` wraps, which is neither
`TransientError` nor `PermanentError`, so callers written against this module's two-exception
contract will not handle it.

The retryability question here is also not uniform and needs deciding explicitly: a connection
error *before* the request was sent is safe to retry; a read timeout *after* the request was
sent has the same "may have been applied" hazard as C1 and is arguably the single most common
way a double charge happens in production.

---

### M3 — MAJOR — lines 19, 51–55 (unbounded retry window while a row lock is held)

**Anchor:** `delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)`

**Problem:** With `MAX_ATTEMPTS = 8` the loop can sleep up to 61.5 s (≈30.8 s expected) plus
eight full request durations, all while the billing worker holds a database row lock, and
there is no overall deadline to bound it.

**Detail.** Sleep budget per attempt: 0.5, 1, 2, 4, 8, 16, then `min(32, 30) = 30`; the eighth
attempt does not sleep. Worst case 61.5 s of pure sleeping. Add eight upstream calls — whose
duration this helper does not and cannot bound, since `fn` is opaque and no timeout is required
of it — and a single wrapped call can hold its row lock for minutes.

This is exactly the scenario the retry logic exists for: during a provider outage, *every*
worker enters this path simultaneously. Locks held for a minute each, connections pinned to
the pool for the whole window, and lock-wait timeouts firing elsewhere in the application.
The jitter prevents thundering-herd on the *provider*; it does nothing for the pressure this
puts on your own database.

What is missing is a wall-clock budget (deadline checked before each sleep, so the loop exits
early rather than always burning all eight attempts) and a documented requirement that `fn`
carry its own request timeout. Alternatively the lock should not span the retry loop at all.

---

### mi1 — MINOR — line 43 (3xx treated as success)

**Anchor:** `if resp.status_code < 400:`

**Problem:** Any 3xx is returned to the caller as a successful response, so an unfollowed
redirect would be handed back as though the charge had completed.

Most HTTP clients follow redirects by default, which is why this is minor rather than major —
but the check should be `200 <= status < 300`, with 3xx handled explicitly. A payments API
returning a redirect is never a completed operation.

---

### mi2 — MINOR — line 55 (`Retry-After` ignored)

**Anchor:** `time.sleep(random.uniform(0, delay))`

**Problem:** The delay is computed purely from the attempt number, discarding any `Retry-After`
header the provider sends with a `429`, which is the one case where the provider has told you
exactly how long to wait.

On the first `429` this sleeps a jittered 0–0.5 s regardless of a header that may say 60. That
both wastes attempts from the budget and risks escalating rate-limit enforcement. `Retry-After`
should take precedence (clamped to `MAX_DELAY`) when present.

---

### mi3 — MINOR — line 47 vs. lines 26–29 (`PermanentError` carries less than `TransientError`)

**Anchor:** `raise PermanentError(f"upstream status {resp.status_code}")`

**Problem:** `PermanentError` embeds the status only in its message string while `TransientError`
exposes it as `.status`, so callers must string-parse to branch on a permanent failure.

Neither exception retains the response object, so the provider's decline code and error body
are discarded at exactly the point they matter most — a caller cannot tell `card_declined`
from `invalid_api_key`, and cannot surface a decline reason. Give `PermanentError` a `.status`
attribute for symmetry and attach the response to both.

---

### mi4 — MINOR — whole function (no observability)

**Anchor:** `for attempt in range(MAX_ATTEMPTS):`

**Problem:** The loop emits no log line, metric, or counter, so a fleet spending 30 s per call
retrying a degraded provider is indistinguishable from a healthy one until something else
breaks.

For a component that can silently absorb a minute of latency per operation on the money path,
at minimum: a counter per retry tagged by status, and a log at exhaustion.

---

### mi5 — MINOR — lines 38, 57 (latent `TransientError(None)`)

**Anchor:** `raise TransientError(last_status)`

**Problem:** If `MAX_ATTEMPTS` were ever set to 0 or a negative value the loop body never runs
and this raises `TransientError(None)`, yielding the message "transient upstream status None".

Unreachable with the current constant of 8, so this is latent rather than live — but the
constant is module-level and the kind of thing that gets tuned in an incident. Validate it at
import, or make the exhaustion path assert that at least one attempt occurred.

---

## Not defects (checked and sound)

- **Full jitter.** `random.uniform(0, delay)` is the correct, literature-backed choice for
  desynchronising a fleet, and it satisfies the stated goal. It is not "not backing off."
- **Backoff arithmetic and the `MAX_DELAY` cap.** Correct.
- **Attempt accounting.** `MAX_ATTEMPTS` is honoured as a total attempt count, and the loop
  correctly skips the sleep after the final attempt rather than sleeping pointlessly before
  raising.
- **Non-cryptographic `random`.** Appropriate for jitter; no security implication.
