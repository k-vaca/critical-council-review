# Review — doc-01-postmortem.md

**Artifact:** `/Users/404notfound/Downloads/Pecorino Project/SKILLS/critical-council-review-eval/artifacts/doc-01-postmortem.md`
**Scope:** one expert review pass against what a competent SRE/incident-management professional should produce.

## Overall assessment

The timeline is clean, the proximate technical cause is correctly identified, and the headline
arithmetic checks out (02:14 → 06:26 = 4h12m). The document is readable and honest about the
order loss.

The analysis, however, stops at the proximate cause and the remediation plan follows it there.
Of the 4h12m outage, 2h26m was detection-and-escalation delay and 0 orders were recoverable —
neither of those failure modes appears in the action items. Structurally, the document has a
"What went well" section but no contributing-factors / "what went wrong" section, which is the
mechanism by which three of the four failures in this incident never became action items. As
written, a recipient would close this incident believing it is prevented when the two largest
multipliers of impact are untouched.

---

## Findings

### CRITICAL

**C1 — Section: "Root cause" + Action item 1**
Anchor: "The 2026-04-10 release added the cart-recommendation call, which holds the full catalogue slice in memory per request."
Problem: The only code-level defect in the incident — an allocation that scales with concurrent
requests — is left in production, and the remediation is an unjustified 4× limit bump (no measured
peak RSS, no headroom calculation, no load test) that will fail again at higher concurrency.

**C2 — Timeline, 02:14 entry + Action items table**
Anchor: "`checkout-api` pods begin restarting. No alert fires."
Problem: The detection gap that accounts for the largest share of the outage is recorded and then
never remediated — there is no action item to alert on CrashLoopBackOff, OOMKill, or 503 rate,
even though the 06:26 entry proves the error-rate signal already exists and was simply not wired
to a page.

**C3 — Header, "Customer impact" + Action items table**
Anchor: "41,300 attempted orders failed. Recovered orders: 0 — the queue was not durable."
Problem: Permanent, unrecoverable business data loss is documented as impact but generates no
action item, so the same non-durable queue will lose orders in the next checkout incident of any
cause.

### MAJOR

**M1 — Timeline, 02:31 and 04:40 entries**
Anchor: "Support escalates to platform on-call after the fifth report."
Problem: 2h09m elapsed between the first customer report of a total checkout outage and
escalation, and no action item addresses support escalation criteria or thresholds.

**M2 — Section: "Lessons"**
Anchor: "The release checklist change in action item 2 should prevent a repeat."
Problem: The document's stated conclusion is unsupported — a manual checklist prompt would not
have caught a per-request unbounded allocation and does nothing about the detection, escalation,
or durability failures, so "prevent a repeat" overstates what the plan delivers.

### MINOR

**mi1 — Section: "What went well"**
Anchor: "Once escalated, diagnosis took 28 minutes."
Problem: Escalation was 04:40 and root cause 05:20, so diagnosis-from-escalation was 40 minutes;
28 minutes is acknowledgement-to-diagnosis, and the mislabel flatters the response in the doc's
own metrics.

**mi2 — Section: "Root cause"**
Anchor: "Under normal evening traffic this exceeded 512Mi and the kubelet killed the pods."
Problem: The trigger is described as evening traffic while the timeline is stamped 02:14 UTC with
no timezone or traffic figures given, leaving a reader unable to tell what load level actually
breaches the limit — which is exactly what is needed to validate 2Gi.

**mi3 — Timeline, 05:44 and 06:26 entries**
Anchor: "Error rate returns to baseline. Incident closed."
Problem: The 42-minute gap between the fix rolling out and recovery is unexplained (rollout pace,
backlog drain, cache warm?), and the incident is closed at the instant of recovery with no soak
or verification period.

**mi4 — Header, "Customer impact"**
Anchor: "checkout returned 503 for all traffic from 02:14 to 06:26 UTC. 41,300 attempted orders failed."
Problem: No revenue or financial impact is attached to the 41,300 lost orders, so the cost of the
durability and alerting gaps cannot be weighed against the cost of fixing them.

**mi5 — Action items table, Owner column**
Anchor: "Audit memory limits on the other 14 services in the checkout path | platform | 2026-05-09"
Problem: Every action item is owned by a team rather than a named individual, and none references
a tracking ticket, so there is no accountable person for the two items still open.

**mi6 — Timeline, 02:31 entry**
Anchor: "First customer report via support chat."
Problem: For a SEV-1 with 41,300 affected orders the document records no customer communication —
no status page, no notification of affected customers — and no follow-up action for it.

---

## Not counted as defects

- Author listed as a role ("platform on-call") rather than a person — convention varies.
- "Status: closed" with two action items still open — normal in orgs that track remediation
  separately from incident state.
- Listing the clean limit rollout under "What went well" — thin, but not incorrect.

**Totals: critical 3, major 2, minor 6.**
