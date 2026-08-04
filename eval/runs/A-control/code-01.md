# Review — `auth/token_manager.py`

Single expert pass. Reviewed against the two stated operating facts in the file header, which
are load-bearing for correctness:

1. 16 worker threads share **one** `TokenManager` instance.
2. The IdP keeps **one active token per `client_id`** — issuing a new token immediately kills
   the previous one.

Almost every finding below follows from taking those two facts seriously.

---

## Findings

### 1. CRITICAL — no synchronization around refresh; concurrent refreshes hand out dead tokens

**Location:** `get_token()` / `_refresh()`, lines 25–46 (also `__init__`, lines 22–23)

**Anchor:**
> `if self._token is None or time.time() > self._expires_at - REFRESH_SKEW:`

**Problem:** `get_token()` performs a check-then-act on shared mutable state with no lock, so
multiple of the 16 threads will enter `_refresh()` simultaneously and — because the IdP
invalidates the prior token on each issuance — the losers return tokens that were already
revoked before the caller ever used them.

**Detail.** The window is not theoretical; it is the *expected* case. All 16 threads are driven
by the same clock and the same `_expires_at`, so at `_expires_at - 30` they all fail the guard on
line 26 within microseconds of each other and all call `_refresh()`. Each successful refresh
revokes the token the previous refresh just handed out. Concretely:

- Thread A refreshes, gets `T1`, `get_token()` returns `T1`.
- Thread B refreshes a millisecond later, gets `T2`. `T1` is now dead.
- Thread A's in-flight outbound API call authenticates with `T1` → `401`.

With 16 threads you get up to 15 revoked tokens per refresh cycle and a burst of 401s that will
look intermittent and unreproducible in single-threaded testing.

There is a second, independent race in the same code: lines 44–45 write `_token` and
`_expires_at` as two separate unsynchronized stores. A reader between them sees the **new** token
paired with the **old** expiry, concludes the token is expired, and triggers yet another refresh —
which revokes the token it was just about to use.

**Fix direction:** guard the refresh with a `threading.Lock` and use double-checked locking, so
that a thread that blocks on the lock re-tests `_expires_at` after acquiring it and returns the
token the winner just fetched instead of issuing its own. `get_token()` must read `_token` and
`_expires_at` under the same lock (or as a single immutable `(token, expires_at)` tuple swapped
atomically) so the torn-read path disappears too.

---

### 2. MAJOR — bare `except:` swallows every error class, including bugs and `KeyboardInterrupt`

**Location:** `_refresh()`, line 48

**Anchor:**
> `except:`

**Problem:** A bare `except` catches `BaseException`, so real defects (`KeyError` on a missing
`access_token`/`expires_in`, `ValueError` from `resp.json()` on a non-JSON body) and control-flow
exceptions (`KeyboardInterrupt`, `SystemExit`) are all treated as transient network errors,
retried five times, and then discarded with no record of what actually went wrong.

**Detail.** Three separate consequences:

- **Diagnostics are destroyed.** Lines 43–45 are inside the `try`. If the IdP returns `200` with a
  body shaped `{"error": "..."}`, the `KeyError` is caught, slept on, and retried — and the
  operator's only signal is `RuntimeError("could not refresh token")` on line 50, with no cause,
  no status code, no response body, and no logging anywhere in the module. That message is
  actively misleading: it points at the network when the real failure may be a contract change in
  the IdP response.
- **No exception chaining.** Because the exception is never bound (`except Exception as e:`),
  line 50 cannot `raise ... from e`. The traceback the on-call engineer sees contains nothing
  about the underlying failure.
- **Shutdown hangs.** `KeyboardInterrupt` during a refresh is caught and followed by
  `time.sleep(2 ** attempt)`. Ctrl-C is ignored for up to 16 seconds, and a second interrupt is
  caught the same way on the next iteration.

**Fix direction:** catch `requests.RequestException` (and `ValueError`/`KeyError` separately, as
non-retryable) rather than everything; bind the exception; log status code and a redacted response
excerpt on each failed attempt; `raise RuntimeError(...) from last_exc`.

---

### 3. MAJOR — non-retryable 4xx responses are retried identically to transient failures

**Location:** `_refresh()`, lines 42–47

**Anchor:**
> `if resp.status_code == 200:` … `time.sleep(2 ** attempt)`

**Problem:** Every non-200 status is treated as retryable, so a permanent, deterministic failure
such as `400 invalid_client` or `401 invalid_client_secret` burns all five attempts and ~31 s of
sleeping before surfacing — and surfaces as a generic timeout-flavoured error rather than "your
credentials are wrong."

**Detail.** OAuth2 client-credentials errors are well-classified and the code ignores the
classification entirely:

- `400` / `401` (`invalid_client`, `invalid_grant`, `unauthorized_client`) will never succeed on
  retry. They should fail fast and loudly.
- `429` *is* retryable but carries `Retry-After`; the code ignores the header and substitutes its
  own `2 ** attempt`, which may retry far sooner than the IdP asked and deepen the rate limit.
- `5xx` and connection errors are the only cases where blind exponential backoff is appropriate.

At startup with a misconfigured secret, this turns an instant, obvious misconfiguration into a
process that hangs for well over a minute per thread and then reports something unhelpful.

**Fix direction:** branch on status class — retry `5xx`/`429`/connection errors, honour
`Retry-After`, and raise immediately with the parsed `error`/`error_description` on `4xx`.

---

### 4. MAJOR — retry budget can outlive the token; a failed proactive refresh discards a still-valid token

**Location:** `REFRESH_SKEW` (line 15), `_refresh()` retry loop (lines 31–50), `get_token()` (26–28)

**Anchor:**
> `REFRESH_SKEW = 30`

**Problem:** The refresh only starts 30 s before expiry, but a degraded IdP can keep `_refresh()`
running far longer than 30 s, so the token expires *while the retry loop is still running* and the
final `raise` propagates out of `get_token()` even in cases where the current token was still
usable.

**Detail.** The worst-case duration of `_refresh()` is not 30 s and is not bounded anywhere:

- `timeout=10` in `requests` is **not** a total-request budget. It is applied to the connect phase
  and the read phase separately, so a single attempt can consume ~20 s.
- Sleeps sum to `1 + 2 + 4 + 8 + 16 = 31 s`.
- Five attempts therefore give a worst case of roughly `5 × 20 + 31 ≈ 131 s` — over four times the
  30 s of headroom the skew provides. There is no overall deadline that would cut the loop short.

Two distinct failure modes result:

- **Expiry mid-retry.** The token dies at second 30 of a 131 s refresh; the remaining ~100 s of
  retrying happens with every worker already unable to authenticate.
- **Throwing away a good token.** The refresh is *proactive* — it fires while the current token is
  still valid. If it fails fast (e.g. immediate `502`s, ~7 s), `get_token()` raises on line 50 even
  though `self._token` is still good for another ~23 s. The correct degraded behaviour is to serve
  the existing token until it actually expires and only then hard-fail.

**Fix direction:** set the skew above the worst-case refresh budget (or bound the budget with an
explicit deadline), pass `timeout=(connect, read)` deliberately, and in `get_token()` fall back to
the existing token when a refresh fails but `time.time() < self._expires_at`.

---

### 5. MAJOR — no failure caching: a down IdP gets hammered by every call from every thread

**Location:** `get_token()` / `_refresh()`, lines 25–50

**Anchor:**
> `raise RuntimeError("could not refresh token")`

**Problem:** Failure leaves `_token`/`_expires_at` untouched and records nothing, so the *next*
`get_token()` call — from any of the 16 threads, immediately — re-enters the full five-attempt
retry cycle, turning an IdP outage into a self-inflicted request flood.

**Detail.** During an outage the arithmetic is unpleasant: 16 threads × 5 requests per call, with
each thread re-entering as soon as its caller retries. There is no circuit breaker, no
"don't try again before *t*" marker, and (per finding 1) no lock to even serialize the attempts.
This is exactly the amplification pattern that keeps a recovering identity provider down. Note
that fixing finding 1 alone does **not** fix this: a lock serializes the threads, but each queued
thread still runs its own full retry cycle on release unless failures are cached.

**Fix direction:** record the last failure time under the lock and short-circuit subsequent calls
within a cooldown window, re-raising the cached error rather than re-attempting.

---

### 6. MINOR — the final attempt sleeps before giving up

**Location:** `_refresh()`, lines 47 and 49 (loop iteration `attempt == 4`)

**Anchor:**
> `time.sleep(2 ** attempt)`

**Problem:** On the last iteration the code sleeps 16 seconds and then falls straight through to
`raise` on line 50, delaying the inevitable failure by 16 s for no benefit.

**Fix direction:** skip the sleep when `attempt == attempts - 1`.

---

### 7. MINOR — backoff has no jitter, so 16 threads retry in lockstep

**Location:** `_refresh()`, lines 47 and 49

**Anchor:**
> `time.sleep(2 ** attempt)`

**Problem:** All threads enter the retry loop at essentially the same instant and sleep for
exactly the same deterministic intervals, so every retry wave arrives at the IdP as a synchronized
burst instead of being spread out.

**Fix direction:** full or decorrelated jitter, e.g. `random.uniform(0, 2 ** attempt)`.

---

### 8. MINOR — expiry tracked against the wall clock, and computed after the response

**Location:** `get_token()` line 26, `_refresh()` line 45

**Anchor:**
> `self._expires_at = time.time() + body["expires_in"]`

**Problem:** `time.time()` is wall-clock time and can jump backwards or forwards under NTP
correction — a backward step makes an expired token look valid, a forward step forces a spurious
refresh storm — and computing the deadline *after* the response arrives credits the token with the
request's own latency, overstating its remaining life.

**Detail.** The token's clock starts when the IdP issues it, not when the response is parsed. On a
slow call this can silently eat several seconds of the already-thin 30 s skew. Both issues are
individually small; they matter here only because finding 4 leaves so little margin.

**Fix direction:** use `time.monotonic()` for all interval arithmetic, and capture the timestamp
immediately *before* `requests.post` so the deadline is measured from request start.

---

## What the code gets right

Worth stating so the findings are read in proportion:

- A timeout is set on the outbound call (line 40) — the single most commonly omitted safeguard in
  code of this shape.
- The refresh-skew concept exists at all; the problem is its size, not its presence.
- Credentials are sent form-encoded in the POST body per the client-credentials grant, not in the
  URL or a query string.
- Non-200 responses are at least noticed rather than blindly `.json()`-parsed.
- Secrets are never logged — though only because nothing is logged at all (see finding 2).

## Summary

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | Critical | `get_token`/`_refresh`, 25–46 | Unsynchronized refresh; threads return already-revoked tokens |
| 2 | Major | line 48 | Bare `except:` hides bugs, kills diagnostics, blocks Ctrl-C |
| 3 | Major | lines 42–47 | Permanent 4xx errors retried; `Retry-After` ignored |
| 4 | Major | line 15 + 31–50 | Retry budget (~131 s) far exceeds 30 s skew; good token discarded |
| 5 | Major | lines 25–50 | No failure caching; outage amplified by 16 threads × 5 attempts |
| 6 | Minor | line 47 | Sleeps 16 s on the final attempt before raising |
| 7 | Minor | lines 47, 49 | Backoff lacks jitter; synchronized retry bursts |
| 8 | Minor | lines 26, 45 | Wall-clock expiry; deadline computed after the response |

**Totals: 1 critical, 4 major, 3 minor.**

The critical finding is the one that decides whether this module works: as written, on the stated
16-thread deployment against an IdP that permits one live token per `client_id`, this code will
distribute revoked tokens on every refresh cycle. Nothing else should be merged before the lock.
