# Expert review — `doc-03-oncall-runbook.md`

**Artifact:** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/doc-03-oncall-runbook.md`
**Review type:** single careful pass, one reviewer (platform/SRE perspective)
**Standard applied:** what a competent platform engineer should hand to an on-call peer, not perfection.

## Overall assessment

This is an above-average runbook. It scopes itself explicitly, names its audience, carries a
validation date and method, states a paging policy, gives a decision tree with explicit
branch outcomes rather than a wall of commands, quantifies the tradeoff of its most
dangerous action, gates that action behind an incident commander, specifies what to include
in an escalation, and documents a known false positive. Most runbooks do none of this.

The defects below are real, but they cluster in two places: the diagnostic commands are
under-specified relative to the "no prior knowledge assumed" audience the doc claims, and
the decision tree has dead ends where a branch terminates with no exit or escalation path.
One finding is critical because a literal reader is routed into the load-shedding step
unnecessarily.

---

## Critical

### C1 — Step 2's rejection check cannot be performed with the command given, and defaults to a false positive

- **Severity:** critical
- **Location:** Step 2 — Check whether OpenSearch is rejecting writes (L28–32)
- **Anchor:** "A non-zero and growing `rejected` count means OpenSearch is the bottleneck, not the indexer. If so, go to step 4."
- **Problem:** `rejected` in `_cat/thread_pool` is a counter cumulative since node start, so a single invocation cannot show whether it is *growing*, and on any cluster that has ever had a write burst it is non-zero — a literal reader sees a non-zero value from one sample, concludes OpenSearch is the bottleneck, skips step 3 entirely, and goes straight to step 4 load shedding.

**Why critical:** the recipient gets a wrong result acting on it as-is. Step 4 requires an
incident commander, drops attachment freshness for all users, and creates a backfill
obligation. Routing into it on a stale cumulative counter is a materially wrong action, and
it also skips the cheap, safe remediation (step 3) that would likely have fixed the problem.

**Fix:** mirror step 1's discipline — instruct the reader to run the command twice 60 seconds
apart and compare `rejected` deltas per node, and state explicitly that a non-zero absolute
value alone means nothing.

---

## Major

### M1 — `$BROKERS` and `$OS_ENDPOINT` are never defined

- **Severity:** major
- **Location:** Step 1 (L16–19) and Step 2 (L29); against the audience claim at L4
- **Anchor:** "**Audience:** platform on-call, no prior knowledge of the indexer assumed."
- **Problem:** The first two commands both depend on shell variables that the runbook never defines or tells the reader where to source, so for the stated audience both commands fail on first invocation.

Note the shell subtlety that makes this worse: in the step 1 command `$BROKERS` is unquoted
and therefore expanded by the *operator's local shell* before `kubectl` runs, not inside the
`kafka-tools` pod — so an on-call who assumes it is preset in the pod environment gets an
empty `--bootstrap-server` and a confusing failure. Either hardcode the values, point at the
config/secret they come from, or add a one-line "export these first" preamble.

### M2 — The "flat" branch of step 1 is mislabelled benign and is an infinite loop

- **Severity:** major
- **Location:** Step 1 (L23)
- **Anchor:** "**Falling or flat:** the indexer is keeping up or catching up. Note the number in the alert thread and stop here. Re-check in 30 minutes."
- **Problem:** Flat lag above 50,000 is not "keeping up" in any user-visible sense — the doc itself says steady lag degrades freshness — and the branch has no exit condition, so an on-call facing permanently flat high lag re-checks every 30 minutes forever with no remediation and no escalation.

This contradicts L11 within the same document ("Steady lag above the threshold degrades
freshness"). The branch needs to separate *falling* (genuinely benign, will self-resolve)
from *flat* (a real freshness regression), and the flat path needs a bound — e.g. "if still
flat above threshold after two re-checks, proceed to step 3 during business hours / file a
ticket."

### M3 — Step 3's remediation is undone by the autoscaler, and the stop condition is premature

- **Severity:** major
- **Location:** Step 3 — Scale the indexer (L39–42)
- **Anchor:** "If lag begins falling, stop here and record the change in the alert thread; the deployment autoscaler will return replicas to baseline within the hour."
- **Problem:** A manual `kubectl scale` on a deployment under an autoscaler is contested — the autoscaler will pull replicas back to baseline while a 50,000+ message backlog is still draining, so declaring success the moment lag "begins falling" reliably produces a re-alert.

Two compounding gaps: the runbook never states the baseline replica count or what the
autoscaler scales on (if it were lag-aware it should already have scaled up, which suggests
it is not — worth saying), and it never tells the operator to check current replicas before
scaling. The correct stop condition is lag back *below* the alert threshold and holding, not
lag merely trending down; and the runbook should say whether to pause/annotate the
autoscaler for the duration.

### M4 — The documented false positive is impossible under the stated alert definition

- **Severity:** major
- **Location:** Known false positive (L62), against the alert definition at L9
- **Anchor:** "A broker restart resets the consumer group's committed offset reporting for up to 2 minutes and can show a large spurious lag."
- **Problem:** The alert only fires after lag exceeds 50,000 for 10 *consecutive* minutes, so a spurious reading lasting at most 2 minutes cannot satisfy the firing condition — the section as written is internally inconsistent with the alert it documents.

Either the alert definition at L9 is wrong, the 2-minute window is wrong, or (most likely)
the real failure mode is different — e.g. a restart that causes a prolonged rebalance, or an
offset-reporting gap that makes the metric pipeline hold a stale high value past the
evaluation window. As written it invites an on-call to dismiss a genuine alert as a known
false positive. The remedy given ("re-run step 1") limits the blast radius, which is why
this is major rather than critical, but the reasoning needs to be corrected or removed.

### M5 — Step 4 is gated on an incident commander who may not exist, and escalation is only reachable through step 4

- **Severity:** major
- **Location:** Step 4 (L48) and Escalation (L58), against the paging policy at L11
- **Anchor:** "Only with an incident commander's agreement, because it drops freshness for one document class."
- **Problem:** The document states this is not a paging alert out of hours, so there is often no incident commander and no instructions for summoning one, while escalation to the search team lead is triggered only "20 minutes after step 4" — leaving a solo on-call with rising lag blocked at step 4 with no defined path forward.

Also missing: an escalation trigger for lag that is *flat and high* after step 4 rather than
still rising, and an escalation trigger for the case where step 4 could not be applied. The
escalation section should be reachable independently of step 4 — e.g. "if you cannot reach
an incident commander within N minutes, page the search team lead instead."

---

## Minor

### m1 — Staleness cannot be derived from the numbers given

- **Severity:** minor
- **Location:** What the alert means (L9)
- **Anchor:** "a document edited now may not appear in search for as long as the lag implies"
- **Problem:** Lag is expressed in messages but the impact is a duration, and the doc gives no throughput figure or conversion, so the on-call cannot tell a stakeholder how stale search actually is.

A single sentence ("at a typical consume rate of ~X msg/s, 50,000 lag is roughly N minutes
of staleness") would close this and would also make the severity of the alert legible.

### m2 — Step 1's comparison is manual and the sampling window is thin

- **Severity:** minor
- **Location:** Step 1 (L21)
- **Anchor:** "Run it twice, 60 seconds apart. Compare the `LAG` column totals."
- **Problem:** `kafka-consumer-groups --describe` prints per-partition rows and no total, so the on-call must sum 24 numbers by hand twice under time pressure, and a single 60-second delta is noisy compared with the alert's own 10-minute evaluation window.

Either pipe through an `awk` sum in the snippet, or point at the lag dashboard/graph, which
answers "is it rising" far more reliably than two hand-summed point samples.

### m3 — The backfill depends on a timestamp nobody is told to record

- **Severity:** minor
- **Location:** Step 4 (L54)
- **Anchor:** "Backfill by removing the variable and running `bin/reindex --since <timestamp>`."
- **Problem:** The backfill window is the moment the flag was set, but step 4 — unlike step 3 — never instructs the operator to record that time or log the change in the alert thread, and `bin/reindex` has no stated execution context (which pod, image, or repo).

Small, but this is the step whose omission silently leaves attachment content permanently
unindexed. Add "record the current UTC time in the alert thread before applying" and name
where `bin/reindex` runs.

### m4 — No warning that steps 3 and 4 themselves cause a temporary lag increase

- **Severity:** minor
- **Location:** Step 3 (L39) and Step 4 (L51)
- **Anchor:** "kubectl -n search set env deploy/search-indexer SKIP_ATTACHMENT_INDEXING=true"
- **Problem:** Both scaling and setting an env var trigger a consumer-group rebalance and (for the env change) a rolling restart, briefly pausing consumption and pushing lag *up* before it comes down, which an unwarned on-call will read as the remediation failing.

This interacts badly with the escalation clock: step 4's "20 minutes" starts precisely when
lag is expected to spike from the restart. One sentence setting the expectation is enough.

### m5 — The broker-restart check can miss an in-place container restart

- **Severity:** minor
- **Location:** Known false positive (L62)
- **Anchor:** "`kubectl -n search get pods -l app=kafka --sort-by=.status.startTime`"
- **Problem:** Pod `.status.startTime` does not change when a container is restarted in place by the kubelet, so a broker that crashed and restarted without pod replacement will not show up in this check.

Adding the restart count to the output (`-o wide`, or a `RESTARTS`-bearing custom-columns
selection) would cover both cases.

### m6 — No urgency budget for the broker disk-pressure outcome

- **Severity:** minor
- **Location:** What the alert means (L11)
- **Anchor:** "rising lag ends in disk pressure on the brokers, which is a page."
- **Problem:** No indication of how long that takes at typical rise rates or what the retention headroom is, so the on-call cannot judge whether they have 20 minutes or 8 hours.

---

## What is done well (not defects — recorded so the fix list is not read as a verdict)

- Explicit scope line with a pointer to the sibling runbook for the adjacent alert (L3).
- Validation date *and* method, including which steps were actually exercised (L5).
- Paging policy stated up front, with the reason (broker disk pressure) rather than just the rule (L11).
- Every branch in steps 1 and 2 has a named outcome; no dangling "if it looks wrong" language.
- Step 4 quantifies its own tradeoff (60% of write volume, 4% of queries) so the incident commander can decide rather than guess.
- The escalation section enumerates exactly what to include in the page.

## Priority of fixes

1. C1 — step 2 needs two samples and an explicit "absolute value means nothing" note.
2. M5 and M2 — close the dead ends in the decision tree; an on-call must never be stuck.
3. M3 — correct the stop condition and address the autoscaler contention.
4. M1 — define the two variables.
5. M4 — correct or remove the false-positive section.
6. Minors as convenient.

## Totals

critical = 1, major = 5, minor = 6
