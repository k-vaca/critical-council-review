# Critical Council Review — `util/lru.py`

## 1. Verdict

**Approve with minor revisions.** The cache is correct: I hand-traced the eviction invariant, the update-existing-key path, and the zero-capacity path, and each holds against the contract the module states. All nine major-tagged findings from the three seats were withdrawn or downgraded at verification — every one of them judged the module against a shared, long-lived, production-operated service cache, which is not the artifact the docstring describes.

Top three fixes, none blocking:

1. Make `capacity` (line 16) a read-only property, or document it as construction-time only.
2. Add three lines to the docstring (lines 2–6): `in` neither counts nor promotes; `clear()` also zeroes the counters; the bound is on entry count, not bytes.
3. Reject non-integral capacity at line 14 so `float("inf")` cannot produce a never-evicting cache.

## 2. Result & standard

**Artifact.** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/code-03-lru-cache.py`, 47 lines, read in full. Not my own prior output.

**Standard.** The module's own stated purpose, judged against what a competent Python practitioner should ship: a bounded LRU cache, instantiated per request handler, single-threaded by contract, capacity chosen by the caller at construction, capacity zero disabling caching. Per non-negotiable 5 this is the bar — not an idealised production cache framework.

**Text addressed to a reviewer.** None. The docstring's `Single-threaded by contract: instances are created per request handler and never shared across threads.` (lines 4–5) and `Callers are responsible for choosing a capacity` (lines 5–6) are addressed to *callers*, not to a reviewer, and do not narrow scope. Seat 2 reached this reading explicitly and correctly; seat 3 raised the same sentence under non-negotiable 8, which is a misapplication — that non-negotiable governs text that instructs the review, not ordinary API documentation. I treated the contract as a claim to assess, and assessed it.

**Tier.** Tier 1 (under ~500 words, one small class), 3 seats. The seats split on this — seat 2 read tier 1, seats 1 and 3 read tier 2 — and both seats reading tier 2 overran their own length ceilings. Tier 1 is the correct read and is the discipline this artifact warranted.

**Independence mechanism.** Parallel: the three seats were run in isolation, none seeing another's analysis or any requester framing. Verification and executive were run as a separate pass with independent contact with the artifact. Agreement between seats therefore counts as evidence — but see the adjudication below for *what* it is evidence of.

**Length.** This review exceeds the tier-1 ≤900-word budget. Disclosed rather than silently overrun: the requester asked for the Step 5 pass documented per finding, and the skill lists the length budget as tune-freely. No other default dropped.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Minor | line 16, `self.capacity = capacity` | Publicly rebindable; assignment re-runs neither the sign check nor eviction, so a runtime change silently leaves the bound stale | Read-only `@property`, or document as construction-time only | Corrected (down from major) |
| Minor | docstring lines 2–6, `A bounded least-recently-used cache.` | Three behaviours left unstated: `in` neither counts nor promotes; `clear()` also zeroes the counters; "bounded" bounds entry count, not bytes | Three lines in the docstring | Corrected (down from major) |
| Minor | line 14, `if capacity < 0:` | Sign is validated, type is not: `float("inf")` passes and yields a cache that never evicts | Reject non-integral capacity before the sign check | Confirmed |

No critical findings. No major findings.

## 4. Council roster

Three seats, derived from this artifact's failure modes: **(1) Correctness & concurrency** — does the LRU invariant hold, and does the thread contract stand up; **(2) Security & failure handling** — error paths and caller misbehaviour; **(3) Operability red-team** — the dedicated skeptic, owning what an operator can see and do.

**Not covered.** Performance under load; the call sites; and — the most consequential omission — **whether this module should exist at all**. No seat asked why a hand-rolled LRU was written rather than `functools.lru_cache`, which is the first question a reviewer of this artifact should ask. A defect could live there: if the call sites cache function results keyed on arguments, the stdlib decorator does this job with less code and no review surface. This does not change the verdict on the code as written, but it is the question the owner should answer first.

## 5. Verification pass (Step 5)

Every anchor was searched for in the source rather than recalled; all sixteen quoted strings exist at the stated lines, and every claimed-absent symbol (`delete`, `invalidate`, `stats`, `__repr__`, `evictions`, `threading`, `Lock`, `TTL`, `isinstance`) is genuinely absent. The seats' anchoring is accurate. What failed verification is not the anchors but the inference from absence to defect.

The nine major-tagged findings deduplicate to six distinct issues.

**M-A — Thread contract unenforced and undetectable.** *(seat 1 major, seat 3 major, seat 2 minor)* → **WITHDRAWN.**
What would make this false: the module explicitly disclaims thread sharing at lines 4–5. A capability the artifact never claimed is not a defect, and demanding `threading.get_ident()` assertions in a 47-line stdlib-only helper is a preference. Documented-contract-without-enforcement is standard Python practice — `dict` and `OrderedDict` themselves make no thread-affinity assertions. Seat 2 reached the correct severity here on the correct reasoning ("a module is not obliged to defend a documented contract"); seats 1 and 3 inflated it.

**M-B — `__contains__` does not touch the counters.** *(seat 1 major, seat 3 minor)* → **CORRECTED to minor.**
What would make this false: nothing in the artifact claims `hits + misses` equals the lookup count. `in` as a membership test that neither counts nor promotes matches the Mapping convention and is a defensible peek — seat 1 concedes this half itself. Seat 3's own example refutes the claim: in `if key in cache: cache.get(key)`, the retrieval *is* counted by the `get`, so the metric is right. What survives is a documentation gap, folded into finding 2.

**M-C — Public capacity knob; mutation breaks the documented guarantees.** *(seat 2 major, seat 3 major, seat 1 minor)* → **CORRECTED to minor.**
What would make this false: the contract is construction-time capacity. Runtime resizing is a capability the artifact never offered. Seat 2's supporting argument — that `if len(self._data) > self.capacity:` (line 35) should be a `while` loop because the bound is "not self-healing" — is wrong on the artifact's own terms: with capacity fixed at construction, `len <= capacity` holds before every `put`, a single insert can exceed it by at most one, so the single `if` is provably sufficient. It is not an under-implemented loop; it is the correct minimal check. What survives is that a non-underscored attribute invites rebinding, and rebinding is unguarded — real, small, one decorator to fix. Finding 1.

**M-D — No per-key invalidation and no TTL.** *(seat 2 major, seat 3 major, seat 1 minor)* → **WITHDRAWN.**
What would make this false: the module claims to be `A bounded least-recently-used cache.` (line 2) and is exactly that. TTL is a different data structure. Seat 2 states the refutation itself — "judged strictly against 'A bounded least-recently-used cache.' (line 2) it does what it says" — then escalates anyway on a hypothetical caller with revocation requirements the artifact never took on. `functools.lru_cache`, the canonical implementation of this concept, likewise exposes only `cache_clear()` with no per-key removal `[unverified — recall, not lookup]`, so "a competent professional would provide invalidation" is not a defensible standard for an LRU cache.

**M-E — No eviction counter.** *(seat 3 major)* → **WITHDRAWN.**
Non-negotiable 4's test: what breaks for the recipient if this is never fixed? Nothing. The cache works; `hits`, `misses`, `__len__` and `capacity` are all public and readable, and `len` against `capacity` already tells an operator whether the cache is full. An eviction counter is a genuine enhancement, not a defect.

**M-F — Telemetry unobservable under the documented lifecycle.** *(seat 3 major)* → **WITHDRAWN.**
Two problems. First, the factual claim is wrong: seat 3 says there is "no accessor" for the counters, but `self.hits` and `self.misses` (lines 18–19) are public attributes with no leading underscore — reading them *is* the accessor, and seat 3's own table cites `line 18 self.hits = 0` while asserting they cannot be read. Second, per-instance counters on a deliberately per-instance object are consistent, not defective; aggregation is the caller's job. Seat 3's own **Strongest reason** field supplies the refutation: "an operator can wrap or subclass the class to aggregate them without changing a line of the caching logic."

**Also withdrawn (minor).** Seat 3's "no read-without-touch" — that `self._data.move_to_end(key)` (line 25) makes diagnostic reads perturb recency. This is the definition of an LRU cache, and `__contains__` already *is* the non-perturbing peek. Seat 3 asks for `in` to promote recency in one row and for a non-promoting read path in another; these are the same method, and it already behaves as the second request wants.

**Count: 5 findings withdrawn, 2 corrected, 0 confirmed at major or above.** Composition: of six distinct major-tagged issues, four withdrawn outright and two downgraded to minor; plus one minor withdrawn. Zero critical findings were raised by any seat.

## 6. Executive review

**Points of agreement — and why they agree.** All three seats converged on five items: the capacity knob, per-key invalidation, `clear()` zeroing the counters, the thread contract, and "bounded" meaning entries rather than bytes. The seats were genuinely isolated, so this convergence is real evidence — but per non-negotiable 3, the question is what it is evidence *of*. Each of the five rests on one shared assumption: that this is a long-lived cache shared across a service, operated in production by someone who will be paged about it. Every seat sourced that assumption from the same place — the filename comment `# util/lru.py` on line 1 — and reasoned from "it lives in `util/`, so it will be shared." The artifact does not establish this; it states the opposite two lines later. Attack the assumption and five of six majors dissolve at once. Three independent readings converging on the same unwarranted premise is exactly the failure mode non-negotiable 3 exists to catch: agreement measured the shared premise, not the artifact.

**Points of conflict & adjudication.**
- *Seat 2 vs. seat 3 on `__repr__`.* Seat 2 counts its absence a security strength (no content leak in tracebacks); seat 3 counts it an operability gap. Both over-read: not defining `__repr__` is the language default, not a hardening decision, and its absence costs an operator little given four public attributes. Neither a strength nor a defect.
- *Severity of the thread contract.* Seats 1 and 3 said major; seat 2 said minor. Seat 2 is upheld, and further reduced to no finding — on the evidence at lines 4–5, not on headcount.
- *Downgrades are evidenced, not vibes.* For M-C the specific contrary evidence is the induction on lines 35–36 showing the single `if` sufficient under the documented contract; for M-F it is lines 18–19 showing the counters public; for M-D it is line 2 stating the artifact's actual scope.
- *Seat reliability.* Seat 3 raised five majors, of which five were withdrawn or corrected, and made one factually wrong claim, one internal contradiction, and one misapplication of non-negotiable 8. Its reliability on severity is in question, though its anchoring was accurate throughout. Seat 2 was the best calibrated: it declined the non-negotiable 8 raise correctly, self-rated the thread contract minor on sound reasoning, and explicitly rejected a memory-zeroization finding as "security theater." Seat 1's mechanical analysis was the strongest — it correctly identified that the `move_to_end` at line 33 is required because `OrderedDict.__setitem__` does not reorder, which is the single subtlest thing in the file and the most common bug in this class of code — but it inflated two findings to major.

**Panel blind spots.** Three. (1) No seat ran the code; my verification is reading and hand-tracing, as theirs was, so the correctness claim rests on inference from source, not execution. (2) No seat asked whether `functools.lru_cache` obviates the module entirely. (3) All three treated `# util/lru.py` as evidence of a sharing model the docstring denies. The one load-bearing external fact is the call sites: whether instances really are created per request handler is unverifiable from this file and no seat could check it `[unverified — I read only this file]`.

**Overall judgment.** Competent, correct, appropriately small code that does what it says. The LRU mechanics are right on every path I traced, the error paths fail before mutating state, and caching a `None` value correctly registers as a hit rather than a miss. The council's criticisms were well-anchored but aimed at a more ambitious artifact than the one written — a service-wide cache framework rather than a per-handler helper. Judged against its stated contract, this is sound work, and the honest review of sound work is a short one.

**Decision on further action: approve with minor revisions.**

**Prioritized next steps.**
1. Confirm the lifecycle claim at lines 4–5 against the actual call sites. If any caller hoists an instance to module or process scope, finding 1 becomes major and the thread contract becomes critical — this single fact governs the verdict.
2. Answer whether `functools.lru_cache` would serve; if so, delete the module.
3. Apply the three minor fixes: read-only `capacity`, three docstring lines, type check at line 14.
4. Add a test file if none exists — capacity 0, capacity 1, update-existing-key, eviction order.

**Confidence & what would change the verdict.** Of the findings I report at critical or major — zero — there is nothing to survive a re-check. The operative claim is the withdrawals: of the six distinct major-tagged issues, I expect all four withdrawals to survive an independent expert re-check, because each turns on the artifact's own stated scope rather than on judgment. The two most likely to be restored are the capacity knob (M-C) and per-key invalidation (M-D), and both flip on the same fact: if the owner confirms a caller resizes at runtime, or that the cache holds revocable data such as authorization decisions, each becomes major immediately. The verdict rests on verified evidence for the mechanics (traced against lines 21–36) and on the docstring's lifecycle claim being accurate at the call sites, which is assumption, not evidence. That assumption is the whole verdict's load-bearing member; if it is false, this review's conclusion changes and seats 1 and 3 were right.
