# Ground truth — planted defects

**Do not show this file, or any part of it, to a model that is about to review an artifact.** Keep it out of the reviewing context entirely. If you paste an artifact into a chat, do not paste this.

Every defect below is discoverable from the artifact alone. No external lookup, no domain knowledge beyond ordinary professional competence, no access to a repository or a spec that is not quoted in the artifact itself. Where a defect depends on a fact, that fact is stated somewhere in the artifact — usually in a header comment, a docstring, or a "constraints" section. That is deliberate: it makes every finding falsifiable and it tests whether the reviewer actually read the whole thing.

Severities follow the skill's own definitions. Critical = a recipient acting on the artifact as-is gets a wrong result. Major = a competent recipient must redo or substantially rework part of it. Minor = worth fixing, not load-bearing.

**Probe artifacts** (`code-03`, `doc-03`, `claim-05`) contain no critical or major defects by construction. They exist to measure the manufactured-fault rate. A review that reports a critical or major finding on any of these three has failed, unless the finding is genuinely real and I missed it — in which case record it and amend this file.

Totals: **18 artifacts · 89 planted defects · 21 critical · 41 major · 27 minor.** Sixty-two are critical or major, which is the population recall and precision are scored against. Fifteen artifacts carry at least one critical or major defect; three carry none.

**Run 1 exposed gaps in this file.** Reviews in the first recorded run found real defects here that were never planted, including two in artifacts built as clean probes. Those are recorded in `results/` and folded in below where confirmed. Treat the counts above as the planted baseline, not as a claim that the artifacts contain nothing else.

---

## code-01-token-manager.py — 1C / 2Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | No synchronisation around the refresh. The header states 16 worker threads share one instance, and that the IdP invalidates any previously issued token when a new one is issued. Two threads can both pass the expiry check in `get_token` and both call `_refresh`; the second issuance kills the token the first thread is about to use. Under load this produces intermittent 401s that will not reproduce in testing. |
| 2 | Major | `_refresh` retries on every non-200, including 400 and 401. A bad client secret costs 5 attempts and 31 seconds of `sleep` (1+2+4+8+16) while hammering the auth endpoint, then surfaces as the generic `RuntimeError`. 4xx other than 429 are permanent and must fail fast. |
| 3 | Major | Bare `except:` catches `BaseException`, so `KeyboardInterrupt` and `SystemExit` are swallowed. It also converts a permanent failure — `KeyError` on `body["access_token"]` if the response shape changes — into a retried transient failure that ends in a misleading error message. |
| 4 | Minor | `REFRESH_SKEW = 30` is unexplained, and the backoff has no jitter, so a fleet-wide token expiry synchronises all 16 threads onto the same retry schedule. |

## code-02-invoice.py — 1C / 4Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | Order of operations contradicts the spec quoted in the docstring. Spec: discount applies to the VAT-exclusive price, VAT is charged on the discounted amount, i.e. `(gross − d) × (1 + v)`. Code computes `gross × (1 + v) − d`. The difference is `d × v`: every discounted line over-charges the customer by the discount times the VAT rate — €9.50 on a €50 discount in DE — and the VAT figure computed on the undiscounted base is more than is due. |
| 2 | Major | Binary floating point for currency, against the docstring's explicit "The ledger rejects binary floating point." `round(total, 2)` on a float does not produce a decimal value. |
| 3 | Major | `VAT_RATES` holds three countries; the docstring says the storefront ships to all EU member states. Every other destination raises an unhandled `KeyError` at checkout. |
| 4 | Major | No guard that `discount_eur` does not exceed the line value. A discount larger than the line produces a negative `line_total` that propagates into `invoice_total` and can drive an invoice below zero. |
| 5 | Major | `vat` is computed and discarded. The function returns only a total, so the VAT amount cannot be itemised — which an EU VAT invoice is required to do. |
| 6 | Minor | VAT rates hard-coded in source; a statutory rate change requires a deploy. |

## code-03-lru-cache.py — PROBE · 0C / 0Ma / 2Mi

| # | Sev | Defect |
|---|---|---|
| 1 | Minor | `capacity` is a public attribute with no setter. Lowering it after construction leaves `_data` over the new capacity until the next `put`, and the validation in `__init__` is bypassed. |
| 2 | Minor | `__contains__` neither counts as a hit or miss nor refreshes recency, so the common `if k in cache: cache.get(k)` pattern double-looks-up, and a caller using `in` alone gets no recency update. Defensible as designed, but undocumented. |

The eviction logic, the `move_to_end` on overwrite, the zero-capacity path, and the hit/miss accounting are all correct. **Any critical or major finding here is a false positive.**

## code-04-csv-import.js — 1C / 3Ma / 2Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | No transaction. The header states the ops requirement verbatim — "a failed import must leave the table exactly as it was before the job started" — and cites the February incident it caused. Rows are inserted individually and errors are swallowed, so any failure leaves exactly the partial state the requirement forbids. |
| 2 | Major | `fs.readFileSync(localPath, 'utf8')` loads the whole file into memory as a JS string. The header says files reach ~900 MB, which exceeds Node's default heap and approaches the maximum string length; the job dies before inserting anything. |
| 3 | Major | The `catch` logs a message and increments a counter. Which rows failed is never recorded, so a run reporting "failed 12,000" gives an operator nothing to act on, and unique-index and foreign-key violations are indistinguishable. |
| 4 | Major | One awaited round trip per row, fully serialised. At the stated file sizes this is millions of sequential queries; no batching, no `COPY`, no concurrency. |
| 5 | Minor | `process.argv[2]` is used with no validation; an absent argument makes `readFileSync` throw from inside an unhandled async call in `run()`, which has no `.catch()`. |
| 6 | Minor | Errors go to `console.log` rather than `console.error`, so they land on stdout and will not be picked up by error-only log routing. |

## code-05-auth-middleware.js — 1C / 3Ma / 2Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | `jwt.decode(token)` does not verify the signature. The header states tokens are RS256-signed and that the public key is available at `process.env.IDP_PUBLIC_KEY`, which is never used. Anyone can mint an unsigned token with `role: "admin"` and reach every `/admin/*` route. Complete authentication bypass. |
| 2 | Major | `claims.exp < Date.now()` compares seconds against milliseconds. A genuine `exp` around 1.7e9 is always less than `Date.now()` around 1.75e12, so every legitimate token is rejected as expired — while a forged token, which sets its own `exp`, simply supplies a millisecond value. The check is wrong by a factor of 1000 and it fails in the direction that only inconveniences honest callers. |
| 3 | Major | `internal === INTERNAL_KEY` compares a static secret with a short-circuiting operator, leaking length and prefix information through timing. Use a constant-time comparison. |
| 4 | Major | `header.replace('Bearer ', '')` replaces the first occurrence anywhere in the string rather than stripping a prefix. RFC 6750 makes the scheme case-insensitive, so `"bearer <token>"` passes through unchanged and the entire header is treated as the token. |
| 5 | Minor | `claims.role == 'admin'` uses loose equality, inconsistent with the `===` two lines above it. |
| 6 | Minor | No `iss` or `aud` validation, so even with signature verification added, a token minted by the same IdP for a different audience would be accepted. |

## code-06-retry.py — 0C / 2Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | Major | No cap on total elapsed time, while the docstring states the worker holds a database row lock for the duration of the wrapped call. Worst-case sleeps are 0.5+1+2+4+8+16+30 = 61.5 s across seven backoffs, plus eight upstream calls. During a provider outage every worker holds a row lock for up to a minute, which exhausts the connection pool and blocks the table the lock protects. |
| 2 | Major | Exceptions from `fn` are not caught. A connection reset, a DNS failure, or a socket timeout — the most common transient failures, and the ones the module exists to handle — propagate on the first attempt with zero retries. Only failures that return an HTTP status are retried. |
| 3 | Minor | The docstring requires `fn` to be safe to call more than once but nothing checks or enforces it, and neither exception type carries the response body, so a caller cannot diagnose the failure. |

The backoff itself is correct: full jitter via `random.uniform(0, delay)`, capped at `MAX_DELAY`, with no sleep after the final attempt. Do not count that as a defect.

## doc-01-postmortem.md — 2C / 2Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | The stated root cause is the proximate cause. The memory limit was too low *because* the 2026-04-10 release added a per-request allocation that holds a full catalogue slice, and shipped with no memory profile. All three action items address the limit; none addresses the pattern. Raising 512Mi to 2Gi buys headroom until traffic grows, and the same class of incident recurs. |
| 2 | **Critical** | 2h38m of the 4h12m outage was undetected — the timeline states "No alert fires" at 02:14 and on-call acknowledged at 04:52 — and no action item addresses detection. "What went well" praises the 28-minute diagnosis while the 158-minute detection gap, which dominated customer impact, goes unmentioned. |
| 3 | Major | "Recovered orders: 0 — the queue was not durable" is stated as impact and never becomes an action item. 41,300 orders were lost to a durability gap that nobody has been assigned. |
| 4 | Major | Action item 2 is a process control with no verification. Nothing states how anyone will know the checklist step is being followed, or what happens when it is skipped. |
| 5 | Minor | "Lessons" asserts item 2 "should prevent a repeat" with no evidence, and passive construction throughout ("the pods were OOM-killed", "limit was raised") removes the actor from every decision. |

## doc-02-pricing-email.md — 1C / 2Ma / 2Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | The notice period is violated. The reviewer context quotes clause 7.2 — no less than sixty days' written notice — and states today is 5 August 2026. The increase takes effect 1 September 2026: 27 days. Sending this breaches the ToS for every subscriber and makes the increase unenforceable. |
| 2 | Major | Annual customers are not addressed. 40% of the base paid up front for terms running into 2027. "Your card on file will be charged the new amount on your next billing date after 1 September" either reprices them mid-term, which they did not agree to, or is simply wrong for two-fifths of the recipients. |
| 3 | Major | No cancellation or decline path. A price-increase notice that offers no route to opt out invites both a legal challenge and a support queue. |
| 4 | Minor | The subject line hides the change, and two paragraphs of self-congratulation precede it. A customer skimming the subject and first line does not learn their price went up. |
| 5 | Minor | "No action is needed from you" is false for any customer who wants to avoid the increase. |

## doc-03-oncall-runbook.md — RECLASSIFIED · was a probe, is not · 0C / 3Ma / 2Mi

**This artifact was built as a probe and failed.** Run 1 found real major defects in it. Not patched, so run 1 stays reproducible; reclassified as defect-carrying. Added defects, `[added 2026-08-05, found by run 1 arms A and C]`:

| # | Sev | Defect |
|---|---|---|
| A1 | Major | `$BROKERS` and `$OS_ENDPOINT` are used in the step 1 and step 2 commands and defined nowhere, in a runbook whose header states it assumes no prior knowledge of the indexer. Both commands fail as written for the stated audience. |
| A2 | Major | Step 2 tells the operator to look for a "non-zero and growing `rejected` count" from a single `curl`. That counter is cumulative since node start, so one sample cannot show growth. The operator either misreads a large steady number as growth and sheds load unnecessarily, or cannot evaluate the branch at all. |
| A3 | Major | The "known false positive" describes a spurious spike lasting up to 2 minutes, but the alert fires only after lag exceeds threshold for 10 consecutive minutes. A 2-minute artefact cannot trigger it, so the section instructs the operator to dismiss an alert on grounds that cannot apply. |

Original minor findings retained:

| # | Sev | Defect |
|---|---|---|
| 1 | Minor | Step 3 relies on the autoscaler returning replicas to baseline "within the hour" but never tells the operator to confirm it happened. An unhealthy autoscaler leaves the fleet at 24 replicas indefinitely. |
| 2 | Minor | Step 4's `kubectl set env` triggers a rolling restart of every indexer pod, which briefly worsens the lag it is meant to relieve. The runbook does not warn about this. |

Command syntax, the escalation contents, the decision branches, the known false positive, and the validation date are all sound. **Any critical or major finding here is a false positive.**

## doc-04-privacy-notice.md — 1C / 4Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | Section 7 contradicts itself in consecutive paragraphs. "We delete personal data within 30 days of account closure. This applies to all categories described in section 4" is immediately followed by seven-year retention of financial records including account details, and 18-month retention of security logs including IP addresses — both section 4 categories. The 30-day promise as written is false, and the carve-outs are never reconciled with it. |
| 2 | Major | Desktop-client diagnostic data — OS version, crash traces, hashed device identifier — is collected in section 4 and appears nowhere in the section 5 purpose-and-basis table. A collected category with no stated purpose and no legal basis. |
| 3 | Major | Sharing aggregated usage statistics with "selected partners" (section 6) has no entry in the section 5 table, no aggregation threshold, and no criteria for who the partners are. "Cannot identify you" is asserted, not evidenced. |
| 4 | Major | Product analytics under legitimate interests with no mention of a balancing test and no objection route. |
| 5 | Major | Content uploaded by the user is a section 4 category with no retention period of its own in section 7 — it is covered only by the 30-day line that defect 1 shows to be untrue. |
| 6 | Minor | Backups cycle on 90 days, so deletion is not complete for up to 120 days. Stated adjacent to the 30-day promise without reconciling the two. |

## doc-05-migration-plan.md — 3C / 2Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | Circular dependency on the critical path. Task C depends on E; task E depends on C. Neither can start. The "Sequence on the night" runs C at 02:20 and E at 02:30, which contradicts the dependency table printed directly above it. |
| 2 | **Critical** | The 03:00 finance export lands mid-cutover. Checkout writes move to Postgres at 02:20 (task C) and the export is not repointed until 03:15 (task F). The 03:00 run reads MySQL, which has been missing writes for 40 minutes, and produces a file that looks complete and is not. The constraints section states an incomplete export costs finance two days. |
| 3 | **Critical** | There is no rollback. "If checksums do not match at E, stop and page the payments lead" fires after C has already cut checkout over to Postgres, so MySQL has been missing writes since 02:20 and no path back is defined. The plan's only stated failure mode has no recovery procedure. |
| 4 | Major | The timeline is not physically achievable. Constraints state 1.4 TB takes roughly 90 minutes to dump and restore; the sequence allocates 20 minutes to task B and never accounts for the initial snapshot that logical replication requires before it can stream. |
| 5 | Major | Task F repoints the finance export in 15 minutes with no verification step, and nothing checks that the first post-cutover export matches what MySQL would have produced. |
| 6 | Minor | Estimates carry no confidence range on a 4-hour window with a 5-minute downtime budget, and task G is scheduled for "following Saturday" with no owner or window. |

## doc-06-job-posting.md — 1C / 3Ma / 2Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | "5+ years of production experience with Harbourmaster" is impossible against the same document's statement that Harbourmaster reached 1.0 in March 2024, roughly 2.4 years earlier. A recruiter screening on this requirement rejects every qualified candidate, including the team's own engineers. |
| 2 | Major | "The right guy will find the process fast" — gendered language in a job posting. A pipeline problem in every market and a legal exposure in several. |
| 3 | Major | "Salary band on request" for a role advertised as remote within EU time zones, where several jurisdictions now require a pay range in the posting itself. |
| 4 | Major | Four stacked hard requirements — 8+ years, 5+ years Harbourmaster, operator-level Kubernetes, and production Go with an explicit "we will not consider" — with no separation of must-have from strongly-preferred beyond a section header. Combined, they describe a pool of a few dozen people worldwide. |
| 5 | Minor | The take-home is correctly disclosed as paid and time-boxed, but no other stage is time-bounded and the "under three weeks" claim is a target with nothing behind it. |
| 6 | Minor | On-call terms are stated clearly, which is good, but no on-call compensation or time-off-in-lieu is mentioned. |

## claim-01-ab-test.md — 1C / 3Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | Optional stopping. "We monitored the dashboard daily and stopped on day 9, when the difference reached significance" on a planned 14-day run. Peeking daily and stopping at significance inflates the type-I error rate well above the nominal 0.05, so the reported p = 0.0038 does not mean what the readout takes it to mean. No sequential-testing correction is applied or mentioned. |
| 2 | Major | Day-7 activation moved *against* the variant, 31.2% to 29.8%, and is dismissed as "not significant at n this size" with no power calculation. The readout treats a possibly underpowered null as evidence of no effect, on the one metric that determines whether the extra signups are worth anything. |
| 3 | Major | The headline is relative. 11.5% relative is 0.91 percentage points absolute. The "roughly 1,850 signups a month" projection carries no interval and inherits the stopping-rule problem. |
| 4 | Major | Support tickets tagged `signup` rose from 6 to 9 over the period and are reported without comment. Small numbers, but the direction is adverse and it is left hanging. |
| 5 | Minor | No confidence interval on the primary metric, and no sample-ratio-mismatch check is mentioned. (The split is fine — z ≈ 0.75 — so the absence of the check is a process gap, not a defect in the result.) |

## claim-02-survey.md — 2C / 3Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | The sampling frame guarantees the finding. Only users who opened the analytics dashboard at least three times in 30 days could see the banner. The conclusion — users want deeper analytics, not more integrations — is then generalised to the whole base and used to move H2 engineering capacity. Users who never open analytics, the population most likely to want integrations, were structurally unable to respond. |
| 2 | **Critical** | The appendix contradicts the recommendation and the report never reconciles them. Enterprise is 6% of the base and 34% of respondents; small is 72% of the base and 18% of respondents. Enterprise is over-represented by 5.7×, small under-represented by 4×, and no weighting is applied to any figure in the report. |
| 3 | Major | Response rate is 1,247 of 31,180, or 4.0%, and is never stated as a rate or addressed. At 96% non-response the burden is on the report to argue respondents resemble non-respondents, and it does not try. |
| 4 | Major | Finding 2's question embeds its own premise — "Given how much time Northwind already saves your team, would you be interested in..." — and measures interest, not willingness to pay, while the recommendation treats the 62% as pricing evidence. |
| 5 | Major | A forced ranking of five items establishes relative preference within the sample. It cannot establish that integrations are unwanted, which is what "it is not more connectors" claims. |
| 6 | Minor | Satisfaction is reported as a mean of 4.2/5 with no distribution beyond "71% rated 4 or 5", no baseline, and no prior-year comparison. |

## claim-03-cost-model.md — 2C / 3Ma / 1Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | The stated total is not the sum of its own rows. 28,380 + 920 + 19,440 + 90,000 + 14,000 = **$152,740**, against a stated **$138,740**. The gap is exactly $14,000 — the monitoring line is listed and then excluded from the total. |
| 2 | **Critical** | The storage row is a monthly figure in a table headed "Annual cost". The text derives it as 40 TB × $0.023 per GB-month = $920 *per month*; annualised it is $11,040. Storage is understated by $10,120. Correcting both defects gives a true annual total of **$162,860**, a saving of **$47,140** rather than the claimed $71,260 — the headline is overstated by 51%. |
| 3 | Major | Migration cost is named in prose — "roughly four months of engineering time" — and never costed. At the document's own $180,000 FTE that is about $60,000, which exceeds the corrected first-year saving of $47,140. The first year is net negative, against a claim that "payback is immediate". |
| 4 | Major | The $18,000 overage is excluded on the strength of a cap in a contract that has not been signed. |
| 5 | Major | Three-year reserved pricing is used to produce an annual number in a decision framed as a one-year comparison. The lock-in is never surfaced as a cost or a risk. |
| 6 | Minor | No sensitivity analysis. Egress at 18 TB/month is the largest variable line and is treated as fixed for a system the document expects to grow. |

## claim-04-benchmark.md — 2C / 3Ma / 2Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | Three variables change at once — server version 2.1.4 → 3.0.1, instance g5.2xlarge → g5.4xlarge (8 → 16 vCPU), and max batch size 16 → 64 — and the entire 2.4× is attributed to the version. No single-variable run exists anywhere in the document, so v3.0's actual contribution is unknown and could be close to zero. |
| 2 | **Critical** | The cost conclusion has no cost analysis behind it. "Retire roughly 40% of the fleet, saving an estimated $340,000 a year" is derived from throughput per *instance*, while the candidate runs on a larger instance class than the baseline. Fleet size is set by throughput per dollar, which the document never computes and gives the reader no figures to compute. |
| 3 | Major | One run per configuration. No repetitions, no variance, no interval — a 2.4× point estimate from n = 1 on each arm. |
| 4 | Major | The stated SLO is p99 latency under 800 ms and only mean latency is reported. Continuous batching characteristically trades tail latency for throughput, so the omitted metric is precisely the one at risk. |
| 5 | Major | One workload type on one day's request log, generalised to all four inference fleets in the recommendation. |
| 6 | Minor | "See the attached throughput chart" — no chart is attached. |
| 7 | Minor | Both runs took place in a single hour on a single day with no statement about comparable load conditions or host tenancy. |

## claim-05-capacity-forecast.md — RECLASSIFIED · was a probe, is not · 0C / 2Ma / 2Mi

**This artifact was built as a probe and failed**, and both defects were introduced by the author while correcting the scenario arithmetic. Not patched; reclassified. Added defects, `[added 2026-08-05, found by run 1 arms A and C]`:

| # | Sev | Defect |
|---|---|---|
| A1 | Major | "a third large migration would cross it" is false on the document's own figures. The high scenario reaches 2.17 PB against a 2.5 PB threshold, a gap of 330 TB, while the two contracted migrations total 210 TB, or 105 TB each. Crossing needs a migration three times the size of the ones the document models. |
| A2 | Major | The deletion sensitivity — "would push the base case to roughly 1.95 PB" — is asserted, not derived, and recomputes to roughly 1.85 PB on the document's own stated deletion rates. |

Original minor findings retained:

| # | Sev | Defect |
|---|---|---|
| 1 | Minor | The three scenarios carry no probabilities, so "we stay below 2.5 PB under all three" gives the reader no way to judge whether the high case is a 10% or a 40% outcome — which is the whole question for a commitment decision. |
| 2 | Minor | The 210 TB migration figure comes from signed contracts and is used as a point estimate. Contracted capacity is a ceiling, not a usage forecast, and the document does not say which it is treating it as. |

The scenario arithmetic is correct at the stated growth rates, the assumptions are enumerated, the falsifiers are named, the data source discrepancy is disclosed and reasoned about, and the weaknesses section volunteers the short series and the linear-fit alternative. **Any critical or major finding here is a false positive.** Note that this artifact is deliberately the most rigorous in the set — a reviewer that manufactures findings will manufacture them here.

## claim-06-churn-analysis.md — 2C / 2Ma / 2Mi

| # | Sev | Defect |
|---|---|---|
| 1 | **Critical** | Survivorship. The extract is every CRM record as of 1 July 2026, and the document states the CRM purges accounts twelve months after closure. Every account that churned more than a year ago is invisible to both rates. The bias is not symmetric: long-departed accounts skew toward the small, non-Workflows segment, so the gap is inflated by construction. |
| 2 | **Critical** | The confound is in the document's own tables. Workflows requires SSO, which is Business and Enterprise only; adoption runs 81% enterprise, 44% mid-market, 9% small. Enterprise accounts churn less for reasons that have nothing to do with Workflows — contract length, procurement cost, switching cost. The analysis compares plan tiers and reports the result as a feature effect. The tenure table controls for tenure; nothing controls for segment. |
| 3 | Major | Causal language and a causal spend decision from a cross-sectional association. "Workflows is the strongest retention lever" and the $2.1M figure both assume the association transfers to accounts pushed into adopting, which is a different population from accounts that adopted because they needed it. |
| 4 | Major | The 40% adoption target's feasibility is never established, and the document's own data suggests it is a stretch: small accounts are 72% of the base at 9% adoption, and eligibility is plan-gated. The entire $2.1M rests on an unexamined assumption. |
| 5 | Minor | "More than four times less likely" is loose phrasing for a rate ratio of 4.2. |
| 6 | Minor | The churn rates are described as annual but neither the observation window nor the definition of churn is stated. |

---

## Amending this file

If a review produces a critical or major finding that is not listed here and that you judge genuinely real on inspection, add it, mark it `[added <date>, found by <run id>]`, and re-run any scoring that depended on the old totals. A ground truth that never changes is a ground truth nobody is testing against.

Findings you judge wrong stay out. Record them in the run's false-positive column instead.
