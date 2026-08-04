# Critical Council Review — `middleware/requireAdmin.js`

> Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

## 1. Verdict

**Reject and rework.** The gate never verifies token signatures, and its expiry check compares seconds against milliseconds — so it admits forged admin tokens while rejecting every genuine one; both halves of its only job fail, in opposite directions.

1. Replace `jwt.decode(token)` (line 31) with `jwt.verify(token, IDP_PUBLIC_KEY, { algorithms: ['RS256'], issuer, audience })` inside a `try/catch`.
2. Delete the hand-rolled expiry check (line 37); let `verify` enforce `exp`, and reject tokens that carry none.
3. Decide the machine-caller path (lines 12–22): per-service credentials with their own identity, or remove it — a single static key is not repairable by editing.

## 2. Result & standard

**Judged:** the whole 49-line file, read in full. Not my own prior output. **Standard:** the file's own stated contract (lines 2–8) plus what a competent backend engineer must produce for an authorization gate — verify before trusting, fail closed, leave an audit trail. **Tier 2**, chosen over tier 1 despite the size because this is a complete deliverable whose failure mode is a live admin bypass: 3 seats, all eight fields, ≤1,800 words. **Independence mechanism: sequential seats** (Step 3 fallback) — no subagent tooling in this run. Per non-negotiable 3, no finding's severity rests on seats agreeing; all convergence is marked sole-source. **Reviewer-directed text:** none present. The header comments are claims to test, and they are the strongest evidence against the code: line 5 promises the public key "is available at process start as process.env.IDP_PUBLIC_KEY", and that variable never appears in the executable code. **Roster:** specified by the requester — disclosed per Step 2, with the seat it omits named in §4. **Declared deviation:** this review overruns the ≤1,800-word tier budget. The skill marks the length budget as tunable; twelve anchored findings plus the Step 5 evidence table would not compress further without deleting real defects, which the budget rule ranks below keeping them.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | line 31, `const claims = jwt.decode(token);` | `decode` parses the payload without checking the signature, so any hand-built token claiming `role: admin` is accepted. | Use `jwt.verify` with the public key, `algorithms: ['RS256']`, and issuer/audience binding. | Confirmed |
| Critical | line 37, `if (claims.exp < Date.now())` | `exp` is in seconds and `Date.now()` in milliseconds, so every real token reads as expired; a token with no `exp` skips the check entirely. | Let `verify` enforce `exp` with a small clock tolerance; require the claim to be present. | Confirmed |
| Major | line 12, `const INTERNAL_KEY = process.env.INTERNAL_API_KEY;` | The machine key is captured once at module load with no second accepted value, so rotation needs a full restart and breaks mid-rollout. | Accept a list of valid keys from a re-readable source, so old and new overlap during rotation. | Confirmed |
| Major | line 18, `req.user = { sub: 'internal', role: 'admin' };` | One shared secret maps every machine caller to the same unscoped admin identity, unattributable in any downstream audit. | Issue per-service credentials carrying their own `sub` and the narrowest role each caller needs. | Confirmed |
| Major | line 25, `header.replace('Bearer ', '')` | `replace` is unanchored, so a header with no scheme is accepted as a token, while the RFC-legal lowercase `bearer` is not stripped and 401s. | Match `/^Bearer +(.+)$/i` and reject anything that does not match. | Confirmed |
| Major | lines 14–47 (whole function) | No logging, metrics, or correlation on any decision path — an operator sees nothing during a lockout or a brute force against the internal key. | Log every decision with route, outcome, credential type, and `sub`; emit a counter per outcome. | Confirmed |
| Minor | line 17, `internal === INTERNAL_KEY` | A static secret is compared in non-constant time. | `crypto.timingSafeEqual` over equal-length buffers. | Unverified |
| Minor | line 41, `claims.role == 'admin'` | Loose equality coerces, so a `role` of `["admin"]` matches. | Use `===` and reject non-string roles. | Unverified |
| Minor | lines 16–22, `if (internal) { ... }` | Sending any `X-Internal-Key` takes over the request, so a stale key 403s a caller who also holds a valid admin token. | Fall through to the bearer path when the internal key does not match. | Corrected (downgraded) |
| Minor | line 42, `req.user = claims;` | The entire decoded payload, including unknown attacker-shaped fields, is handed to downstream handlers. | Assign a whitelisted projection: `{ sub, role }`. | Corrected (downgraded) |
| Minor | lines 31–39, no `try`/`catch` in the file | There is no error path at all; the mandatory move to `jwt.verify`, which throws, turns every bad token into a 500 unless one is added. | Wrap verification in `try/catch` and map thrown errors to 401. | Corrected (narrowed) |
| Minor | line 12, no startup validation | An unset `INTERNAL_API_KEY` silently 403s every machine caller and looks identical to a wrong key. | Fail fast at boot if the required env vars are missing. | Unverified |

## 4. Council roster

Requester-specified; disclosed as a fact, not honored as a constraint.

1. **Correctness & concurrency** — owns whether the access decision is computed correctly and whether the lifecycle the comments describe (key loaded at process start) survives concurrent traffic and rotation.
2. **Security & failure handling** — owns authentication, secret handling, and behavior when a token or dependency misbehaves.
3. **Operability red-team** — owns production failure and what the operator can see.

**Not covered.** *The token issuer's actual claim schema* — could hide a critical: even a fixed gate may accept tokens minted for another audience. *Performance* — RS256 verification per request with no cached key parse is a real cost, not plausibly critical. *The downstream consumer of `req.user`* — the viewpoint Step 2 requires and this roster omits; partially reached by the `req.user = claims` finding, never examined on its own. A defect there would not change today's decision, which is already the most severe available.

## 5. Individual analyses

### Seat 1 — Correctness & concurrency

**Role & remit.** Backend correctness engineer; judges whether the function computes the intended access decision and whether it holds under the lifecycle its own comments describe.

**Assessment.** The control flow is clean and the request path is genuinely concurrency-safe, but two of the four comparisons it makes are wrong, and the one value it holds across requests cannot be rotated.

**Strengths.** No shared mutable state: every decision derives from `req` alone, and the only cross-request value, `INTERNAL_KEY` (line 12), is an immutable `const`. No cache, no async boundary, no shared object — so no request can observe another's partial state, and every branch terminates in exactly one response.

**Weaknesses, risks & errors.**
- **Critical, defect** — `if (claims.exp < Date.now())` (line 37). JWT `exp` is seconds since epoch; `Date.now()` is milliseconds, roughly a thousand times larger, so the condition holds for every genuinely issued token and every admin is locked out with `{"error":"expired"}`. The same line also fails open: with no `exp`, `undefined < Date.now()` is `false` and the check is skipped. (`exp` as NumericDate seconds is *[unverified — recall, not lookup]*; the magnitude gap itself is arithmetic.)
- **Major, defect** — `const INTERNAL_KEY = process.env.INTERNAL_API_KEY;` (line 12) is read once and never re-read, and only one value is ever accepted. Rotation therefore requires restarting every process, and during a rolling restart old-key and new-key pods coexist, so one cohort of callers is rejected whichever order you use.
- **Minor, defect** — `claims.role == 'admin'` (line 41): loose equality coerces, so `["admin"]` matches. Not the identity check it reads as.
- *Overlap:* the missing signature check belongs to seat 2; noted because lines 37 and 41 are only reachable through it.

**Gaps.** No `nbf` check and no clock tolerance for skew between the IdP and this host.

**Strongest reason this might be fundamentally wrong.** If the identity service emits `exp` in milliseconds — non-standard, but possible for an in-house IdP — line 37 is correct as written and my critical collapses to a latent trap. The file says only that tokens "carry ... `exp`" (line 4) and gives no units.

**Domain verdict.** Fails. Concurrency-safe, arithmetically wrong.

**Recommended fixes.** Drop line 37 and let verification enforce expiry with a tolerance; accept a set of internal keys so rotation has an overlap window; use `===`.

### Seat 2 — Security & failure handling

**Role & remit.** Application security reviewer; judges authentication, secret handling, error paths, and behavior when a dependency misbehaves.

**Assessment.** On the bearer path this performs no authentication at all. It parses an untrusted string and trusts its contents.

**Strengths.** The internal path fails closed when the env var is unset: `if (internal)` requires a truthy string, and a string can never `===` `undefined`, so a missing `INTERNAL_API_KEY` yields 403 rather than open access. The 401/403 split is used correctly — unauthenticated versus authenticated-but-insufficient.

**Weaknesses, risks & errors.**
- **Critical, defect** — `const claims = jwt.decode(token);` (line 31). Decoding is not verifying. Anyone can base64url-encode `{"role":"admin","sub":"anyone"}`, attach any header and signature, and receive admin on every `/admin/*` route. The standard applied is verify-then-trust; the file's own comment names an RS256 public key it never loads.
- **Major, defect** — `const token = header.replace('Bearer ', '');` (line 25). String `replace` rewrites the first occurrence anywhere and does not anchor, so `Authorization: eyJ...` with no scheme passes through unchanged and is accepted, while lowercase `bearer` is left in place and 401s a conformant client.
- **Major, defect** — `req.user = { sub: 'internal', role: 'admin' };` (line 18). One static, non-expiring, bearer-equivalent secret collapses every machine caller into one unscoped admin; nothing downstream can distinguish which service acted.
- **Minor, defect** — `internal === INTERNAL_KEY` (line 17) is a non-constant-time secret comparison.
- **Minor, defect** — `req.user = claims;` (line 42) forwards the whole attacker-shaped payload.
- **Major, defect** — no `try`/`catch` appears anywhere in the file, so there is no error path for a throwing token parse.

**Gaps.** No `iss`/`aud` binding — once verification is added, any token the IdP mints for any audience still opens `/admin/*`. No algorithm pin — a fix must pass `algorithms: ['RS256']` or accept HS256 forgeries signed with the public key.

**Strongest reason this might be fundamentally wrong.** If an upstream gateway already verifies signatures and this file only re-reads a trusted token, my critical narrows to defense-in-depth. Nothing in the file claims that, and the comment's promise of a public key argues the opposite.

**Domain verdict.** Fails. This is not an authentication check.

**Recommended fixes.** Verify with a pinned algorithm, issuer, and audience inside `try/catch`; anchor the scheme with a case-insensitive regex; replace the shared key with per-service credentials; `crypto.timingSafeEqual`; project `req.user`.

### Seat 3 — Operability red-team

**Role & remit.** Production and on-call reviewer; where this breaks in production and what the operator sees when it does.

**Assessment.** Every failure mode here is silent. The file emits no logs, no metrics, and nothing that lets an operator tell a bug from an attack.

**Strengths.** The three response bodies (`unauthorized`, `expired`, `forbidden`) are distinct enough that a proxy log could separate the failure classes without changing this file.

**Weaknesses, risks & errors.**
- **Major, defect** — no logging anywhere in the function (lines 14–47 contain no `console` and no logger). The day this ships, every admin receives `{"error":"expired"}` and the operator sees a wall of 401s with nothing distinguishing "tokens really expired" from "the gate broke". A brute force against `x-internal-key` produces an unbounded stream of 403s with no counter, no alert, and no attribution.
- **Major, defect** — `if (internal)` (lines 16–22) lets the mere presence of the header take over the request: a caller with a stale internal key and a valid admin bearer token is 403'd, and the response says nothing about which credential failed.
- **Major, defect** — no rate limiting or lockout on the internal key path; the static secret can be guessed at full line rate.
- **Minor, defect** — nothing validates at startup that `INTERNAL_API_KEY` (line 12) is set; a deploy that forgets it rejects every machine caller and looks identical to a wrong key.

**Gaps.** No correlation id on the auth decision, and no metric separating the internal path from the token path — so nobody can tell whether the internal key is still in use before rotating it.

**Strongest reason this might be fundamentally wrong.** No foundational failure found in my domain. The strongest candidate is the total absence of logging, which is major rather than fundamental because it lengthens time-to-diagnosis rather than causing the incident; the incidents themselves come from seats 1 and 2.

**Domain verdict.** Fails the bar for a privileged-access gate — unobservable by design.

**Recommended fixes.** Log every decision with route, outcome, credential type, and `sub`; emit per-outcome counters; fail fast at boot on missing env vars; fall through to the token path when an internal key does not match.

## 6. Verification pass (Step 5)

Re-opened the file and searched it for every quoted string behind a critical or major finding, asking what would make each finding false.

| Finding | String searched | Located | Result |
|---|---|---|---|
| No signature verification | `jwt.decode(token)` | line 31 | **Confirmed.** Falsifier tested: does the file verify elsewhere? `process.env.IDP_PUBLIC_KEY` occurs only in the comment on line 5, never in code; `jwt.verify` does not appear. |
| Expiry unit mismatch | `claims.exp < Date.now()` | line 37 | **Confirmed.** Falsifier tested: no conversion to or from seconds appears anywhere in lines 10–47. |
| Key rotation | `const INTERNAL_KEY = process.env.INTERNAL_API_KEY;` | line 12 | **Confirmed.** Module scope, single value, no re-read. |
| Shared machine identity | `req.user = { sub: 'internal', role: 'admin' };` | line 18 | **Confirmed.** Literal, unconditional, no per-caller distinction. |
| Bearer parsing | `header.replace('Bearer ', '')` | line 25 | **Confirmed.** Falsifier tested: no regex, no `startsWith`, no case handling elsewhere. |
| No observability | `console` / `log` | absent, lines 1–49 | **Confirmed.** |
| No `try`/`catch` | `try` | absent, lines 1–49 | **Corrected → minor.** The claim that this crashes today rests on `jwt.decode` throwing, which I cannot check from the artifact and label *[unverified — recall, not lookup]* (I recall it returns `null`). Narrowed to what the file shows: there is no error path, and the mandatory move to `verify` — which does throw — requires one. |
| Internal-key short-circuit | `if (internal) {` | line 16 | **Corrected → minor.** Anchor confirmed; severity narrowed (see adjudication). |
| No rate limiting on the internal path | — | — | **Withdrawn** (seat 3). A requirement the artifact never took on: neither the code nor its comments claim throttling, which normally lives at the edge. The surviving residue — no failed-auth signal is emitted — is already counted under the observability finding. |

Minor findings not listed above had their anchors located verbatim but did not receive the adversarial re-check, and are marked `unverified` in §3. **Withdrawn: 1. Corrected or narrowed: 3.**

## 7. Executive review

*The executive re-read the file before synthesizing.*

**Points of agreement — all sole-source under the sequential fallback.** (a) The bearer path performs no authentication: owned by seat 2; seats 1 and 3 reference it, but they shared one context and inherited the reading, so it carries the weight of one seat. (b) The header comments describe behavior the code does not implement (seats 1, 2). The assumption beneath (b) is that the comment states intent rather than being a stale copy of an older version. Attacking that assumption does not save the file: if the comment is accurate the code is wrong, and if it is stale the file misleads its next reader.

**Points of conflict & adjudication.**
- Seat 3 rated the internal-key short-circuit **major**; **downgraded to minor**. Named evidence: lines 16–22 affect only a request that chose to send the header, so no end user or admin path is touched, and the remedy is a one-line fallthrough — a support cost, not rework.
- Seat 2 rated the missing `try`/`catch` **major**; **downgraded to minor** on the Step 5 correction — as the file stands, the crash claim is unverified; the hazard is real only once `verify` lands.
- Seat 1 flagged that the `exp` critical would collapse if the IdP emitted milliseconds. **Upheld critical**: seconds is the overwhelming default and the file gives no evidence of an in-house variant — but this is the single assumption most likely to move, and it is named again in the confidence note.
- Seat 1's `role == 'admin'` at **minor** was not contested; **upheld**. Exploiting it requires the IdP to emit a non-string role, which nothing here suggests, and once signatures are verified the attacker no longer controls the claim.
- No seat contradicted another on a matter of fact.

**Verification result.** One finding withdrawn (seat 3's rate limiting), three corrected or narrowed. No seat's reliability is in question: both errors were over-reach at the boundary of the file's scope, not misreadings of its text.

**Panel blind spots.** All three seats assumed `jwt` on line 10 is the npm `jsonwebtoken` package with its documented `decode` and `verify` semantics — the `require` says so, the behavior is recall. All three assumed nothing upstream verifies the token first. Under the sequential fallback, coverage is as suspect as agreement: the seats shared what they failed to look at. No seat examined **the issuer's actual claim schema** — whether `role` is a string, whether `exp` is present, whether an `aud` exists to bind against — and a critical could live there, because a corrected gate could still accept a valid token minted for a different service. No seat examined **performance**: RS256 verification per request with no cached key parse is a genuine cost at admin-route volume, but not plausibly critical. The load-bearing claims that should be checked outside this review are the two labeled recall items: NumericDate seconds, and `jwt.decode` returning `null` rather than throwing.

**Overall judgment.** Measured against what a competent backend engineer must produce for an authorization gate, this fails at the level of purpose, not polish. Both directions of the access decision are wrong — forged tokens in, genuine tokens out — and the file's own comments describe a verification step the code never performs, which means the defect survived whatever review produced it. The structure is sound and each fix is individually well understood; that is the honest argument for repairing rather than rejecting, and I reject it anyway: twelve independent defects in thirty-five executable lines, two of them total failures, plus a shared-secret design that needs a decision rather than an edit.

**Decision on further action.** **Reject and rework.**

**Prioritized next steps.**
1. Rewrite the bearer path around `jwt.verify` with the public key, `algorithms: ['RS256']`, issuer and audience, inside `try/catch` — this closes the bypass and the expiry bug together (lines 25–39).
2. Decide the machine-caller path: per-service credentials with distinct identities, or delete it (lines 12–22). Do not patch the static key in place.
3. Add decision logging and per-outcome counters before redeploying, so the next defect is visible (lines 14–47).
4. Add regression tests for: forged signature, `alg: none`, HS256 signed with the public key, missing `exp`, seconds-valued `exp`, lowercase `bearer`, no scheme, `role: ["admin"]`, and both credentials presented at once.
5. Re-review after the rewrite; do not treat this review as sign-off on the replacement.

**Confidence & what would change the verdict.** Of the six findings at critical or major, I expect five to survive an independent expert re-check unchanged. First to fall: the `Bearer` parsing finding (line 25) — a reviewer whose clients all send the canonical prefix could reasonably narrow it to minor. Second: key rotation (line 12), if the deployment already restarts every process on a secret change. The verdict rests on verified text — every anchor above was searched and found in the file — plus one recall-based assumption (`decode` does not verify, `verify` does) and one inference (nothing upstream verifies first). It flips only if `jwt` on line 10 is not the package it names, or if a gateway already verifies signatures; the first would require the `require` to be lying, and the second would still leave the expiry critical standing, so neither changes the decision.
