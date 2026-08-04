# Critical Council Review — `net/retry.py`

Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

---

## 1. Verdict

**Revise substantially before use.** The loop arithmetic and jitter shape are competent, but this helper retries money-moving calls with no deduplication token, never retries the transport failures that dominate real outages, and sleeps for up to a minute inside a held database lock — while its docstring asserts a double-charge guarantee it does not deliver.

1. Add a required idempotency key, sent unchanged on every attempt (`call_with_retry`, line 32), and delete the docstring sentence claiming the row lock prevents double charges (lines 9–11).
2. Catch transport exceptions at line 41 and retry them on the same budget.
3. Move `time.sleep` (line 55) outside the lock, or cap total in-lock time.

## 2. Result & standard

Judged: all 57 lines of `net/retry.py`, read in full. Not this model's prior output as far as this session can establish; held to the third-party bar either way. **Standard:** the artifact's own stated purpose — survive a payments-provider outage without double-issuing a charge and without a recovering fleet synchronising — plus what a competent payments engineer should produce for a helper wrapping every charge, refund and payout. **Tier 2** (a module), **3 seats**, **sequential independence mechanism**, per the requester's instruction.

No text in the artifact is addressed to a reviewer. The docstring does assert a safety property — "The worker holds a database row lock for the duration of the wrapped call so that a charge cannot be issued twice" (lines 9–11) — treated per non-negotiable 8 as a claim under test, not a fact granted. It did not survive.

**Length.** This review measures ~3,250 words (`wc -w`, table markup included) against the tier-2 ceiling of 1,800, and sections 2–4 run ~330 against 200. Declared rather than hidden, and it is a real overrun, not a rounding: the skill classes the length budget as tunable, and the overage buys the ten-row findings table and the Step 5 evidence trail. A reader who wants the tier-2 length can stop after section 4 — sections 1–4 carry every finding and fix.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| critical | L36–37, "safe to call more than once with the same arguments" | Retries a charge with no idempotency key; a lost 5xx after upstream success charges twice. | Require an idempotency key; send it unchanged on every attempt. | confirmed |
| critical | L41 `resp = fn(*args, **kwargs)` | Transport errors (reset, timeout, DNS, TLS) get zero retries and escape as an undeclared type. | Catch transport errors, retry on the same budget, convert to `TransientError`. | confirmed |
| critical | L54 delay formula + L9–11 lock claim | Up to 61.5s of sleep plus eight undeadlined calls run inside a held DB row lock. | Sleep outside the lock, or cap total in-lock time to a stated budget. | confirmed |
| major | L35–36, "fn must return an object with a `.status_code` attribute" | `Retry-After` on 429/503 is structurally unreachable; the helper re-hits the rate limit on its own schedule. | Widen the contract to status + headers + body; use `Retry-After` as a delay floor. | confirmed |
| major | L13–14 `import random` / `import time`; loop L40–57 | No logs, metrics or spans anywhere; `TransientError` omits attempt count and elapsed time. | Log each attempt; emit counters; add `attempts`, `elapsed`, `possibly_applied`. | confirmed |
| major | L47 `raise PermanentError(f"upstream status {resp.status_code}")` | Discards the response body, so callers cannot separate a decline reason from a validation error. | Attach status, headers and body to `PermanentError`. | confirmed |
| major | L19 `MAX_ATTEMPTS = 8` | Up to 8x request volume against an already-failing provider; no circuit breaker or shared budget. | Add a retry budget / circuit breaker; lower attempts on the money path. | confirmed |
| major | L55 `time.sleep(random.uniform(0, delay))` | Prefork workers inherit one RNG state, so jitter repeats and the fleet re-synchronises. | Reseed per worker after fork, or use `random.SystemRandom`. | corrected |
| major | L41 `resp = fn(*args, **kwargs)` | Identical args replayed for ~60s; timestamped signatures or nonces go stale and read as auth failures. | Rebuild time-sensitive credentials per attempt via a callable. | corrected |
| minor | L43 `if resp.status_code < 400:` | 3xx is returned as success, so a redirect could be recorded as a completed charge. | Treat non-2xx as an error unless explicitly allowed. | corrected |

## 4. Council roster

Derived from how *this* module can fail its purpose: it does arithmetic on time, it runs inside someone else's lock, it talks to a paid dependency, and it is the last thing standing during an outage.

1. **Correctness & concurrency** — owns whether the loop computes the right thing and whether it holds up under the concurrency the docstring itself describes.
2. **Security & failure handling** — owns auth, secrets, error paths, and behaviour when the dependency misbehaves.
3. **Operability red-team** — owns where this breaks in production and what the operator sees when it does.

**Deliberately not covered:** tests and CI (none in scope; a critical defect cannot live in *this file* because of it, though the untested state raises the odds these defects ship); typing, packaging and style (no critical defect can live there); the calling billing worker (a critical defect **could** live there — see blind spots); and the provider's actual published guidance, unverifiable from the artifact.

## 5. Individual analyses

### Seat 1 — Correctness & concurrency reviewer

**Role & remit.** Whether `call_with_retry` computes the right thing, and whether it holds up under the concurrency model its own docstring asserts.

**Assessment.** The retry arithmetic is right; the safety model is not. Attempt counting, the backoff curve and the skipped final sleep are all correct. The invariant the module claims to protect is protected nowhere in the file.

**Strengths.** `if attempt == MAX_ATTEMPTS - 1: break` (line 51) yields exactly 8 calls and 7 sleeps, avoiding the off-by-one that sleeps after the last try. `random.uniform(0, delay)` (line 55) is full jitter — the right anti-synchronisation shape, and a deliberate choice rather than an accident.

**Weaknesses, risks & errors.**
- **Critical, defect** — retry after upstream success double-charges. Anchor: "safe to call more than once with the same arguments" (lines 36–37). A 504 or 500 often means the charge *was* applied and the response lost; line 41 re-calls `fn` with byte-identical arguments. The row lock serialises workers but cannot deduplicate, because the duplicate originates inside the lock. Purpose undermined (Step 1): never issue a charge twice.
- **Critical, defect** — transport failures get zero retries. Anchor: `resp = fn(*args, **kwargs)` (line 41). Connection resets, socket timeouts, DNS and TLS errors propagate uncaught on attempt one — and these dominate the outage this helper exists for. The escaping exception is neither `PermanentError` nor `TransientError`, so callers catching the documented pair miss it.
- **Critical, defect** — up to 61.5s of sleeping inside the held lock. Anchors: `delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)` (line 54) and lines 9–11. The seven caps sum to 0.5+1+2+4+8+16+30 = 61.5s (expected ~30.8s under full jitter), plus eight upstream calls the contract never requires to carry a timeout. Purpose undermined: a provider brownout becomes lock-table and pool exhaustion across the billing fleet.
- **Major, defect** — 3xx returned as success. Anchor: `if resp.status_code < 400:` (line 43). A redirect is handed back as a completed charge. *(Corrected to minor at Step 5.)*
- **Minor** — `last_status` could reach line 57 as `None`. *(Withdrawn at Step 5.)*

**Gaps.** No idempotency parameter, no total deadline, no per-attempt timeout in the `fn` contract, no way for the caller to learn how many attempts ran.

**Strongest reason this might be fundamentally wrong.** The module's entire safety argument is one sentence of prose asserting a lock prevents double charges — the only statement of the invariant in the file, inherited by every caller and reviewer. The foundational failure is not a missing feature but a documented guarantee the code does not provide, which suppresses the fix more effectively than documenting nothing would.

**Domain verdict.** Below the bar for a money path: arithmetic competent, invariant unsound.

**Recommended fixes.** Require an idempotency key passed identically on every attempt; wrap `fn` in `try/except` for transport errors and fold them into the same budget; move the sleep outside the locked region or cap in-lock wall-clock; require `fn` to carry a timeout.

### Seat 2 — Security & failure-handling reviewer

**Role & remit.** Auth, secrets, error paths, and what happens when the dependency misbehaves rather than simply fails.

**Assessment.** Secret hygiene is clean; the failure taxonomy is too coarse for money. The module discards everything in a response except the status line, and has no concept of a credential that expires mid-retry.

**Strengths.** `raise PermanentError(f"upstream status {resp.status_code}")` (line 47) emits only a status code — no body, headers or request echo — so card numbers, tokens and keys cannot leak into exception text or logs.

**Weaknesses, risks & errors.**
- **Major, defect** — `Retry-After` ignored and structurally unreachable. Anchor: "fn must return an object with a `.status_code` attribute" (lines 35–36). Honouring `Retry-After` on 429/503 is standard client behaviour `[unverified — recall, not lookup: 429 defined in RFC 6585; Retry-After in RFC 9110]`. The contract exposes only a status code, so the helper cannot honour a backoff the provider explicitly requested and instead re-hits the limit on its own schedule.
- **Major, defect** — identical arguments replayed for up to a minute. Anchor: line 41. If the provider requires a timestamped signature or single-use nonce, attempts five to eight carry credentials minted ~60s earlier; the failure surfaces as 401/403 → `PermanentError` and gets misdiagnosed as a rotated key. *(Narrowed at Step 5: the artifact never states the provider signs requests.)*
- **Major, defect** — the response body is discarded on the permanent path. Anchor: line 47. For 402/422 the decline reason lives in the body; the caller receives a bare integer and cannot choose between dunning, re-prompting and paging a human.

**Gaps.** No separation of 401/403 (re-authenticate) from other permanent statuses; no redaction policy for callers who will want the body once it is exposed.

**Strongest reason this might be fundamentally wrong.** No foundational failure found. The strongest candidate is the `.status_code`-only contract, which is major rather than fundamental because it is an interface widening — the model of the problem is right, the aperture is too narrow.

**Domain verdict.** Acceptable on secret hygiene, below the bar on error semantics.

**Recommended fixes.** Widen the contract to status + headers + body; treat `Retry-After` as a floor on the computed delay; accept a callable that rebuilds time-sensitive credentials per attempt; attach body and headers to `PermanentError`.

### Seat 3 — Operability red-team

**Role & remit.** Where this breaks in production, and what the operator sees at 3am when it does.

**Assessment.** The module is invisible. It emits nothing — no log line, no metric, no span — for any attempt, backoff or give-up. During the outage it exists to survive, an operator observes latency, then a bare exception with a number in it.

**Strengths.** The four tuning constants sit at the top of the file (lines 16–19), separate from the logic, so an incident responder can cut `MAX_ATTEMPTS` or `MAX_DELAY` without reading the loop.

**Weaknesses, risks & errors.**
- **Major, defect** — zero observability, by construction. Anchor: the module imports only `import random` / `import time` (lines 13–14), and nothing in lines 40–57 emits anything. Missing: a per-attempt record of index, status, chosen delay and correlation id. `TransientError` reaches the caller carrying one integer, so nobody can distinguish a 2-second blip from a 4-minute stall or reconcile against the provider's ledger.
- **Major, defect** — retry amplification. Anchor: `MAX_ATTEMPTS = 8` (line 19). A fleet-wide 503 multiplies volume against an already-failing provider by up to 8x. Jitter spreads retries in *time* but not in *volume*; there is no circuit breaker, shared budget or shedding. This is the standard path from brownout to a metastable failure the provider cannot exit.
- **Major, defect** — prefork workers share a jitter sequence. Anchor: `time.sleep(random.uniform(0, delay))` (line 55) against the stated goal, "add jitter so that a fleet recovering from an outage does not synchronise" (lines 5–6). `random` uses one module-global generator whose state survives `os.fork()`; workers forked after import and never reseeded draw identical delays — the exact lockstep the docstring names as the reason jitter is there. *(Narrowed at Step 5: conditional on a prefork model the artifact does not state.)*

**Gaps.** Nothing tells the operator the one thing that decides the runbook: whether a failed call may already have moved money.

**Strongest reason this might be fundamentally wrong.** If the billing worker treats `TransientError` as "definitely not charged" and re-enqueues, this module's silence about possible partial success turns every 504 storm into a duplicate-charge storm at the queue level. The module would then be wrong not in its loop but in the contract it hands its only caller — and the loop could be perfect without helping.

**Domain verdict.** Not production-ready on a money path.

**Recommended fixes.** Log each attempt with index, status, delay and correlation id; emit counters for attempts and give-ups by status; add `attempts` and `elapsed` to `TransientError`; add a `possibly_applied` flag set whenever the request was fully sent and the last status was 5xx; add a circuit breaker keyed on the provider.

## 6. Verification pass (Step 5)

Every critical and major finding was re-checked adversarially — asking what would make it false — with each quoted string searched in the source rather than recalled.

**Confirmed (7).** Located verbatim: "safe to call more than once with the same arguments" → L36–37; `resp = fn(*args, **kwargs)` → L41; `delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)` → L54, with the seven caps re-summed independently to 61.5s; "The worker holds a database row lock … so that a charge cannot be issued twice" → L9–11; "fn must return an object with a `.status_code` attribute" → L35–36; `raise PermanentError(f"upstream status {resp.status_code}")` → L47; `MAX_ATTEMPTS = 8` → L19; `import random` / `import time` → L13–14, with no logging import anywhere in the file.

**Corrected (3).** 3xx-as-success (seat 1) restated from **major to minor** — the artifact never states whether `fn` follows redirects, and mainstream Python clients do by default, so the trigger requires a non-default configuration the artifact gives no reason to assume; impact stays severe if triggered, likelihood is contingent. Fork-inherited RNG (seat 3) narrowed to conditional on a prefork model — the artifact says "billing worker" (line 8) and nothing about process model. Stale signed credentials (seat 2) narrowed to conditional on timestamped signing, which the artifact does not state.

**Withdrawn (1).** Seat 1's minor claim that `last_status` could reach line 57 as `None`. `MAX_ATTEMPTS` is the literal `8` at line 19, so the loop always runs at least once and always assigns `last_status` (line 49) before any path reaching line 57. Dead path, withdrawn as unreachable — not a misquote, so seat 1's reliability is not in question.

## 7. Executive review (Step 6)

The executive re-read all 57 lines before synthesis.

**Points of agreement.** Seats 1 and 3 both arrive at "the caller cannot tell whether money moved" — seat 1 from the missing idempotency key, seat 3 from the empty error payload. Under the sequential fallback this convergence is **sole-source** and carries no weight for severity; both stand on their own anchors, which I checked personally.

**Deduplication.** Seat 2's "body discarded" and seat 3's "no attempt/elapsed context" are facets of *errors carry no diagnostic context*, but have distinct fixes (widen the exception payload vs. instrument the loop) and remain separate rows.

**Points of conflict & adjudication.**
- Seat 1 rated 3xx-as-success major. **Downgraded to minor.** Named evidence: the artifact specifies nothing about redirect handling in `fn`, and default client behaviour makes the path unreachable absent a deliberate non-default configuration. The anchor is real; the trigger is contingent.
- Seat 1 was silent on header semantics where seat 2 raised `Retry-After`. **Silence is not disagreement** — seat 1 never examined that area, so seat 2's finding stands unopposed and is upheld.
- Seat 1's in-lock-sleep critical depends most on facts outside the file (lock scope, pool sizing, DB timeouts). **Upheld at critical:** the 61.5s figure is arithmetic I recomputed from line 54, and lines 9–11 are the module's own statement of its deployment. It undermines the Step 1 purpose directly — the helper converts the outage it exists to survive into a database incident.

**Verification result.** One finding withdrawn (seat 1, unreachable `None` path), three narrowed. No seat's reliability is in question; the withdrawal was latent-path speculation, not a misquote, and every retained anchor was located verbatim.

**Panel blind spots.** All three seats took the docstring's account of the deployment at face value — the row lock, the single caller, and the "provider's published guidance" at lines 4–7. None of that is verifiable from the artifact and it is load-bearing: **check the provider's live retry documentation, and whether it mandates idempotency keys, before acting.** Because the seats ran sequentially in one context, treat coverage as suspect too, not only agreement — they likely share what they failed to look at. No seat examined the calling billing worker, and **a critical defect could live there**: if it treats `TransientError` as "not charged" and re-enqueues, finding 1 compounds into duplicate charges at the queue level. No seat examined tests or typing; a critical defect could not live there for this file.

**Overall judgment.** Competent mechanics wrapped around an unsound safety model. The backoff curve, attempt count and jitter choice are what a good engineer would write. But a retry helper for money that retries without a deduplication token, ignores the transport failures that dominate real outages, holds a database lock across a minute of sleeping, and tells its reader that double-charging is impossible is not merely incomplete — its documentation actively discourages the fix it most needs.

**Decision on further action: revise substantially before use.**

**Prioritized next steps.**
1. Add a required idempotency key threaded through every attempt, and delete the claim at lines 9–11 that the lock prevents double charges.
2. Catch transport exceptions at line 41, retry them on the same budget, convert to `TransientError`.
3. Move the sleep outside the locked region, or cap total in-lock wall-clock to a stated budget.
4. Widen the `fn` contract to expose headers and body; honour `Retry-After`; attach the body to `PermanentError`.
5. Instrument the loop (per-attempt logs, counters) and add `attempts`, `elapsed`, `possibly_applied` to `TransientError`.
6. Add a circuit breaker or shared retry budget before the 8-attempt fan-out.

**Confidence & what would change the verdict.** Of the nine findings at critical or major, I expect **seven to survive** an independent expert re-check. First to fall: stale signed credentials, conditional on timestamped signing the artifact never mentions; then fork-inherited RNG, conditional on a prefork worker model also unstated. The three criticals rest on verified evidence — text quoted from the file and arithmetic I recomputed — plus the assumption that the docstring's account of the deployment is accurate. What would flip the verdict: if the provider deduplicates server-side on a request hash, finding 1 narrows to minor and the decision drops to *approve with minor revisions*; if the row lock at lines 9–11 is not in fact held across the wrapped call, finding 3 narrows to major but the decision holds.
