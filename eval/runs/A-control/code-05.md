# Review — `artifacts/code-05-auth-middleware.js`

Single expert pass. Target: `middleware/requireAdmin.js`, 49 lines, Express middleware gating
`/admin/*` with two authentication paths (RS256 bearer JWT, and a static shared key for internal
callers).

**Verdict:** not shippable. The bearer path neither verifies the token signature nor evaluates
expiry correctly; as written the JWT branch rejects every legitimate token, and the moment the
expiry bug is fixed the gate accepts forged admin tokens from anyone. Two critical, three major,
six minor.

---

## Critical

### C1 — Token signature is never verified (line 31)

> `const claims = jwt.decode(token);`

`jwt.decode` parses the JWT payload without validating the signature — it is a decoder, not a
verifier. Any caller can base64url-encode `{"sub":"x","role":"admin","exp":<future>}`, append any
signature (or none), and be granted admin. This is a complete authentication bypass on the primary
path.

The file's own header comment states the tokens are "signed RS256" and that the public key is
"available at process start as `process.env.IDP_PUBLIC_KEY`" — that variable is never read anywhere
in the module, which is the tell.

The fix is `jwt.verify`, and it must carry an explicit algorithm allowlist. Verifying without
pinning `algorithms` reintroduces two classic attacks: `alg: none`, and RS256→HS256 confusion where
the attacker signs with HMAC using the (public, therefore known) RSA public key as the shared
secret. `jwt.verify` also throws on malformed/invalid tokens, so it needs a `try/catch` returning
401 — the current code has no error handling because `decode` returns `null` instead of throwing.

```js
let claims;
try {
  claims = jwt.verify(token, process.env.IDP_PUBLIC_KEY, {
    algorithms: ['RS256'],
    issuer: EXPECTED_ISS,
    audience: EXPECTED_AUD,
  });
} catch (err) {
  return res.status(401).json({ error: 'unauthorized' });
}
```

### C2 — Expiry compares seconds against milliseconds (line 37)

> `if (claims.exp < Date.now()) {`

The JWT `exp` claim is *seconds* since the Unix epoch (RFC 7519 §4.1.4); `Date.now()` returns
*milliseconds*. A current token's `exp` is on the order of 1.8e9 while `Date.now()` is on the order
of 1.8e12, so the comparison is true for every non-absurd token. Every bearer request is rejected
with `401 {"error":"expired"}` — the entire JWT path is dead, and the failure looks like an identity
service problem rather than a middleware bug, so it will burn debugging time.

The comparison must be `claims.exp * 1000 < Date.now()` (or `claims.exp < Date.now() / 1000`), but
the correct fix is to delete the check and let `jwt.verify` enforce `exp` and `nbf` with the
standard clock-skew tolerance.

Note the interaction with C1: today the code fails *closed* only by accident. Someone triaging
"admin login is broken," fixing the unit mismatch, and shipping would silently open the bypass in
C1. These two must be fixed together.

---

## Major

### M1 — Loose equality on the role check (line 41)

> `if (claims.role == 'admin') {`

`==` performs type coercion on a value that comes straight out of an attacker-influenceable JSON
payload. `["admin"] == 'admin'` evaluates to `true` because the array coerces via `toString()`, as
does any object with a matching `toString`. A security decision must use `===`, and ideally an
explicit type guard (`typeof claims.role === 'string' && claims.role === 'admin'`). The
inconsistency is visible in the file itself — line 17 uses `===` for the internal key, line 41 uses
`==` for the privilege check.

### M2 — Non-constant-time comparison of the shared secret (line 17)

> `if (internal === INTERNAL_KEY) {`

`===` on strings short-circuits at the first differing byte, leaking a timing signal that can be
used to recover a static, long-lived secret byte by byte. Use `crypto.timingSafeEqual` over buffers,
guarding the length check first (`timingSafeEqual` throws on length mismatch, which is itself a
leak — hash both sides, or compare lengths before and always run the comparison):

```js
const a = Buffer.from(internal);
const b = Buffer.from(INTERNAL_KEY);
if (a.length === b.length && crypto.timingSafeEqual(a, b)) { ... }
```

Remote timing attacks over a network are noisy and hard to land, but this is a static credential
guarding an admin gate with unlimited attempts — the cost of the correct primitive is one line.

### M3 — A client-controlled header short-circuits to full admin (lines 15–22)

> `const internal = req.headers['x-internal-key'];`

`X-Internal-Key` is an ordinary request header. Nothing in this middleware establishes that the
request actually originated inside the trust boundary — no mTLS check, no source-address check, no
assertion that an upstream proxy strips client-supplied copies of the header. If the service is
ever reachable directly, or the edge proxy forwards rather than overwrites this header, possession
of one static string is unconditional permanent admin.

Compounding problems on this path: the key never expires and there is no rotation or versioning
story; every internal caller collapses into the single identity `{ sub: 'internal' }`, so the audit
trail cannot distinguish which service acted; and the branch is evaluated *before* the bearer path,
so merely presenting the header suppresses normal authentication.

At minimum, restrict this path to a trusted network/mTLS-verified peer, give each service its own
credential so `sub` is meaningful, and document the rotation procedure. mTLS or a signed
service-to-service token (client-credentials JWT) is the right long-term shape.

---

## Minor

### m1 — Bearer prefix stripping is unanchored and case-sensitive (line 25)

> `const token = header.replace('Bearer ', '');`

`String.prototype.replace` with a string pattern removes the first occurrence *anywhere* in the
value, not a prefix. It is also case-sensitive, while RFC 7235 defines the auth-scheme as
case-insensitive — a compliant client sending `authorization: bearer <jwt>` gets a 401. Parse
explicitly instead:

```js
const m = /^Bearer\s+(\S+)$/i.exec(req.headers.authorization || '');
if (!m) return res.status(401).json({ error: 'unauthorized' });
const token = m[1];
```

Failures here are fail-closed (401), so this is an interop/robustness defect rather than a security
hole.

### m2 — A token with no `exp` claim passes the expiry check (line 37)

> `if (claims.exp < Date.now()) {`

If `exp` is absent, `undefined < <number>` is `false`, so the token is treated as unexpired — a
non-expiring admin token. Presence of `exp` must be required, not assumed. Independent of the unit
bug in C2: fixing the units does not fix this. `jwt.verify` alone does not close it either (it only
enforces `exp` when present), so require the claim explicitly or set `maxAge`.

### m3 — No startup validation that `INTERNAL_API_KEY` is set (line 12)

> `const INTERNAL_KEY = process.env.INTERNAL_API_KEY;`

Read once at module load. If the variable is unset, `INTERNAL_KEY` is `undefined`; a string header
can never `===` `undefined`, so the path fails closed (403) rather than opening — that part is
sound. But the misconfiguration is silent: every internal caller gets an indistinguishable 403 with
no diagnostic. Fail fast at boot (`throw` if unset) so a bad deploy is caught at start rather than
in production traffic.

### m4 — No issuer or audience validation

Nothing constrains which tokens are accepted beyond `role` and `exp`. If the identity service issues
tokens for multiple relying parties, a token minted for an unrelated service — with a `role: admin`
claim that means something entirely different in that context — is accepted at this gate. Pass
`issuer` and `audience` to `jwt.verify` and reject anything else.

### m5 — HTTP auth semantics are wrong on two responses

> `return res.status(403).json({ error: 'forbidden' });` (line 21)

A *wrong* internal key is a failed authentication, not an authorization denial: it should be 401,
not 403. Separately, none of the 401 responses carry a `WWW-Authenticate` header, which RFC 7235
§3.1 requires on every 401. Cosmetic to a browser, but it breaks well-behaved API clients that key
retry/refresh logic off the challenge.

### m6 — No audit logging on the admin gate

Every rejection path returns a status code and nothing else — no log line, no metric, no request
correlation. An admin-privilege boundary with a static shared secret and unlimited retries should
emit an auditable event on both grant and denial, and denials on the internal-key path in particular
should be alertable (they are the signal that someone is probing the key). If this is genuinely
handled by an upstream access-log middleware, disregard; it is not visible here.

---

## What is correct

Worth stating so the rework does not churn what already works:

- `req.headers['x-internal-key']` uses the lowercase form, which matches Node's normalization of
  incoming header names. Correct.
- An empty or absent `authorization` header degrades cleanly to `''` and is caught by the `!token`
  guard rather than reaching `jwt.decode`. Correct.
- Every branch terminates with an explicit `return`, so there is no accidental fall-through calling
  `next()` twice or after a response. Correct.
- Each failure path in the current code returns a rejection; nothing here fails open at runtime
  *today*, though C1 means it fails open the instant C2 is patched in isolation.

## Suggested order of work

1. Replace `jwt.decode` with `jwt.verify` + `algorithms: ['RS256']` + `issuer`/`audience` +
   `try/catch` (C1, m4), and delete the hand-rolled expiry comparison in favour of the library's
   (C2, m2). These are one change and must land together.
2. Tighten the two comparisons: `===` with a type guard on `role` (M1), `timingSafeEqual` on the
   internal key (M2).
3. Decide the internal-caller story (M3) — network restriction plus per-service credentials, or
   drop the path in favour of mTLS/client-credentials tokens.
4. Cleanups: header parsing (m1), boot-time config validation (m3), status codes and
   `WWW-Authenticate` (m5), audit logging (m6).
5. Add tests that would have caught C1 and C2: a token signed with the wrong key must be rejected,
   an `alg: none` token must be rejected, a token expiring in one hour must be accepted, and a token
   that expired one minute ago must be rejected.
