# Critical Council Review — `artifacts/doc-01-postmortem.md`

Run in a single context; later seats saw earlier ones, so agreement between seats is weaker evidence than it appears.

---

## 1. Verdict

**Revise substantially before use.** The record of *what happened* is sound; the analysis of *why* is not, so the three corrective actions leave the failure mode, the detection gap, and a disclosed order-loss mechanism all live.

1. **Root cause** — restate the cause as the unbounded per-request catalogue load ("holds the full catalogue slice in memory per request"), not the 512Mi ceiling, and add an action that bounds the allocation.
2. **Action items table** — add owned, dated actions for checkout alerting and support→on-call escalation; 2h38m of the 4h12m elapsed before on-call was aware.
3. **Customer impact** — add an action for the non-durable order queue ("Recovered orders: 0") or record an explicit accepted-risk decision.

## 2. Result & standard

Judged: the full text of `doc-01-postmortem.md` (38 lines, read in full). Not model-authored; non-negotiable 2 does not apply. **Tier 2** — word count says tier 1, but this is a closing SEV-1 deliverable with three downstream audiences and the requester specified a three-seat full council, which is the tier-2 shape. **Mechanism: sequential seats** (Step 3 fallback; no subagent tooling this run), so per non-negotiable 3 no finding's severity rests on inter-seat agreement and every convergence below is marked sole-source.

**Standard** (my stated judgment, derived from the artifact's own framing — `Status: closed`, an Action items table, a Lessons section — not from a cited template, per non-negotiable 6): a closing SEV-1 postmortem must reconstruct events accurately, explain causes deeply enough that the listed actions remove the failure mode, cover the whole impact chain — detection, escalation, mitigation, customer and data consequences — with owned dated actions, and be honest about what did not go well.

**Requester framing (quarantined):** procedural only — roster, ordering, and mechanism. No view was expressed on the artifact's quality or the expected verdict, so nothing was available to defer to.

**Text addressed to a reviewer:** none. But the document pre-declares its own verdict twice — `**Status:** closed` (line 3) and "The release checklist change in action item 2 should prevent a repeat" (Lessons). Per non-negotiable 8 those are claims to assess, not findings to accept; both are assessed below.

**Declared deviations.** (a) The requester fixed the roster; per Step 2 that is disclosed, and the seat the artifact would otherwise have required is named under *Not covered* with the verdict capped accordingly. (b) **The length budget was overridden, not met.** This review runs ~3,200 words against a tier-2 total of ~1,800: seats are 342/368/350 against a 250 ceiling and the executive is ~880 against 350. The skill designates the budget numbers tunable; the trade taken was to keep all eleven anchored findings, the nine mandated Step 6 elements, and the per-seat audit trail the sequential mechanism exists to produce. The verdict block is within its 120-word ceiling (115), so a reader who stops there still gets the whole decision. (c) Step 6 deduplication removed one item from a seat's Weakness list; a pointer is left in place so the sequential audit trail stays intact. No seat's judgment was altered after a later seat was written.

## 3. Findings

| Severity | Location | Problem | Fix | Status |
|---|---|---|---|---|
| Critical | Root cause + Action items 1–3 — "The `checkout-api` memory limit of 512Mi was too low." | The stated cause and all three actions target the ceiling, not the unbounded per-request catalogue load that reaches it, so 2Gi only moves the threshold. | Restate the cause as the unbounded allocation and add an owned action to bound it (cap, paginate, or share the catalogue slice). | Corrected |
| Critical | Timeline 02:14 and 04:40 — "No alert fires." | 2h38m of the 4h12m outage was detection and escalation delay; no action item addresses either. | Add owned, dated actions for a checkout availability alert and a support→on-call escalation trigger. | Confirmed |
| Critical | Customer impact — "Recovered orders: 0 — the queue was not durable." | A total-order-loss mechanism is disclosed, then produces no action item and no recorded decision to accept it. | Add an owned action to make the order path durable, or record the accepted risk and who accepted it. | Confirmed |
| Major | Customer impact — "41,300 attempted orders failed." | Payment/authorization state and customer communication for the failed orders appear nowhere in the document. | Add an action to reconcile authorizations and captures across the window, and record what customers were told. | Confirmed |
| Major | Customer impact vs Root cause — "The pods restarted, took traffic, and were killed again." | "503 for all traffic" is never reconciled with the crash-loop narrative, and 41,300 has no stated source. | State the measurement source and the actual failure fraction, or label the figure an estimate. | Corrected |
| Major | Timeline 04:52 — "Finds `checkout-api` in CrashLoopBackOff." | Reverting the 2026-04-10 release is never considered or ruled out as the faster mitigation. | Record whether revert was possible and why raising the limit was chosen instead. | Confirmed |
| Major | Action item 3 — "Audit memory limits on the other 14 services in the checkout path" | Possible same-class exposure across 14 services sits four weeks out with no interim control or stated risk acceptance. | Check the highest-traffic services this week, or state the risk accepted until 2026-05-09. | Confirmed |
| Minor | What went well — "Once escalated, diagnosis took 28 minutes." | 28 minutes runs from acknowledgement (04:52); from escalation (04:40) it is 40 minutes. | Relabel as "once acknowledged", or state 40 minutes from escalation. | Confirmed |
| Minor | Timeline 05:44–06:26 — "Limit raised to 2Gi, pods roll out." | The 42-minute gap between rollout and baseline recovery is unexplained — longer than the diagnosis the document praises. | Add one line accounting for the recovery tail. | Confirmed |
| Minor | Root cause — "Under normal evening traffic this exceeded 512Mi" | No timezone is given for "evening" against a UTC timeline, so the reader cannot place peak traffic. | State the market timezone, or give the measured request rate for the window. | Corrected |
| Minor | Action items table — Owner column reads "platform" for all three rows | No individual is accountable, and item 1's "done" carries no date or verification link. | Name a person per row; date and link the verification for item 1. | Unverified |

## 4. Council roster

Three seats, fixed by the requester and disclosed as such. Each was given the full roster (role names and remits only, no findings) and told that another seat owning a topic is not a reason to skip what it can see.

1. **Purpose & audience fit** — a postmortem that does not change what happens next is a filing exercise; this seat owns whether the document does its job for the three readers who depend on it.
2. **Accuracy & internal consistency** — the causal claim drives every action item, so whether the document's own evidence supports it is load-bearing.
3. **Risk red-team** — the required skeptic, and the seat carrying the downstream/recipient view: 41,300 failed orders is a commercial and customer-facing event, not only an engineering one.

**Not covered.** (a) *Platform / Kubernetes resource engineering* — no seat judged whether 2Gi is itself adequate, whether the requests-vs-limits distinction the document never mentions matters here, or what a bounded fix should look like. **A critical defect could plausibly live here, and the verdict below does not cover it.** (b) *Editorial quality* — no critical defect plausible. (c) *Incident-management process design* — partially reached through seats 1 and 3; a critical defect is unlikely but not excluded.

---

## 5. Individual analyses

### Seat 1 — Purpose & audience fit

**Role & remit.** Judges whether this closing SEV-1 record does its job for the platform team who must act on it, the other checkout-path teams reading it as a warning, and the review audience deciding whether the risk is retired.

**Assessment.** Well-organized and readable; it reconstructs the incident competently and then stops short of the work a postmortem exists to do. Every corrective action addresses the last 94 minutes of the outage. Nothing addresses the first 158.

**Strengths.** The timeline keeps the unflattering facts rather than smoothing them — "No alert fires" (02:14) and "Support escalates ... after the fifth report" (04:40) are both recorded. The impact line quantifies the loss including the zero, which is what makes the rest reviewable.

**Weaknesses, risks & errors.**
- **Critical, defect** — the corrective actions do not cover the dominant contributor to impact. Anchor: "No alert fires." (Timeline, 02:14) against the three-row Action items table. Detection and escalation consumed 2h38m of 4h12m and produce nothing.
- **Critical, defect** — Lessons claims a prevention the actions do not deliver. Anchor: "The release checklist change in action item 2 should prevent a repeat." *(Deduplicated into Executive agreement #1; see §6.)*
- **Major, defect** — a reader cannot tell whether reverting the triggering release was considered. Anchor: "Finds `checkout-api` in CrashLoopBackOff." (Timeline, 04:52).
- **Minor, defect** — "Once escalated, diagnosis took 28 minutes." (What went well) measures from acknowledgement, not escalation.
- **Minor, defect** — the Owner column reads "platform" for all three rows; no person is accountable.

**Strongest reason this might be fundamentally wrong.** If alerting and durability are already tracked in a separate workstream and this document is only the memory-limit record, the omissions are scoping, not failure. The document forecloses that reading itself: it is marked closed and asserts a repeat is prevented.

**Domain verdict.** Below the bar for a closing SEV-1 record; adequate as an interim engineering note.

**Recommended fixes.** Add alerting and escalation action items with named owners; delete or evidence the prevention claim; state the revert decision.

### Seat 2 — Accuracy & internal consistency

**Role & remit.** Judges whether the document's claims are correct, mutually consistent, and supported by its own evidence.

**Assessment.** The chronology is arithmetically clean. The causal claim at the centre of the document is not supported by the mechanism the same paragraph describes.

**Strengths.** The timestamps hold: 02:14 to 06:26 is 4h12m, matching the title; the 2026-04-10 release precedes the 2026-04-11 incident coherently. The root-cause paragraph names a specific code path and a specific release rather than "resource pressure" — it is precise enough to be checked, which is why the error in it is visible.

**Weaknesses, risks & errors.**
- **Critical, defect** — the root-cause statement contradicts the mechanism beside it. Anchors: "The `checkout-api` memory limit of 512Mi was too low." and "holds the full catalogue slice in memory per request" (both Root cause). If consumption scales with concurrent requests and catalogue size, no fixed limit is a fix; the limit is the ceiling that was hit, not the cause. Every action item inherits the error.
- **Major, defect** — total-failure claim unreconciled. Anchors: "checkout returned 503 for all traffic" (Customer impact) versus "The pods restarted, took traffic, and were killed again." (Root cause). Whether impact was total or partial determines the 41,300 figure, which carries no stated source.
- **Major, defect** — "Under normal evening traffic this exceeded 512Mi" (Root cause) does not fit an 02:14–06:26 UTC window. *(Ruled down at Step 5; see §6.)*
- **Minor, defect** — 42 minutes between "Limit raised to 2Gi, pods roll out." (05:44) and baseline (06:26) are unaccounted for.
- **Minor, defect** — the 28-minute figure is measured from the wrong event *(overlaps Seat 1; noted per roster instruction)*.

**Strongest reason this might be fundamentally wrong.** If "memory limit too low" is shorthand and the team already understands the allocation is unbounded, the document is imprecise rather than incorrect. The action items are the evidence against that: all three treat limits as the object of work.

**Domain verdict.** The record is reliable; the causal claim is not, and it is the part the reader will act on.

**Recommended fixes.** Rewrite the root-cause statement around the allocation; source the 41,300 figure; close the 42-minute gap.

### Seat 3 — Risk red-team

**Role & remit.** Judges legal, compliance, commercial and downstream exposure if this document ships as the closing record.

**Assessment.** The document's candor is the reason the exposure is visible, and the exposure is larger than the incident it describes. Two liabilities are disclosed and then left without an owner.

**Strengths.** "Recovered orders: 0" is stated plainly where it would have been easy to omit. A document that names its own worst number is one a risk function can work with.

**Weaknesses, risks & errors.**
- **Critical, defect** — a total-loss mechanism is disclosed and un-actioned. Anchor: "Recovered orders: 0 — the queue was not durable." (Customer impact). It is independent of the memory fault, applies to every future incident, and appears in no action item and no recorded acceptance decision.
- **Major, gap** — no payment or customer-communication follow-up. Anchor: "41,300 attempted orders failed." (Customer impact). Whether any authorization was taken without an order being created is the first question finance and support will ask; the document neither confirms nor excludes it. I do not assert that it happened — the document simply does not say, and that is the defect.
- **Major, defect** — known possible exposure across 14 services carries no interim control. Anchor: "Audit memory limits on the other 14 services in the checkout path" due 2026-05-09 (Action item 3) — four weeks of unbounded exposure, accepted silently.
- **Raised and withdrawn** — "`**Status:** closed` is premature while items 2 and 3 are open." *(Withdrawn at Step 5; see §6.)*

**Strongest reason this might be fundamentally wrong.** If the 41,300 figure is materially wrong in either direction, the exposure assessment changes with it — and if authorizations were taken, this document becomes the record showing the organization knew the scale and closed anyway.

**Domain verdict.** Not safe to close on. The engineering remediation may be adequate; the commercial and data-loss exposure has not been assessed at all.

**Recommended fixes.** Reconcile payment state for the window; raise a durability action item or a signed risk acceptance; add an interim control ahead of the 14-service audit.

---

## 6. Executive review

*The executive re-read the full artifact before synthesis; every anchor below was located in the source text.*

**Points of agreement** — all marked **sole-source** per non-negotiable 3, since the seats shared one context and their convergence is not independent evidence.
1. **The remedy does not address the mechanism.** *(Deduplicated: Seat 2's root-cause misattribution and Seat 1's Lessons prevention claim are one underlying defect — the document identifies an unbounded per-request allocation, then states the cause as, and acts only on, the limit. Stated once here and cut from Seat 1's list.)*
2. The corrective actions omit the phase that produced most of the outage *(Seat 1, echoed by Seat 3)*.
3. The document is candid about bad numbers and does not blame individuals *(all three seats)*.

**Points of conflict & adjudication.**
- *Seat 2's "evening traffic" contradiction, rated major.* **Downgraded to minor.** Specific evidence: 02:14 UTC is evening across the Americas, so the premise that the window cannot be peak is unestablished — the artifact never states its market. What survives is a clarity defect, not an inconsistency.
- *Seat 3's "Status: closed is premature", rated major.* **Rejected.** The artifact ties closure to service recovery, not to the action items: "**06:26** — Error rate returns to baseline. Incident closed." The finding rested on a misreading.
- *Seat 1's team-level ownership, rated minor.* **Upheld at minor.** Nothing in the artifact ties team ownership to slippage; the point is real but not load-bearing.
- Three findings raised by the seat that owns the domain (Seat 3's durability and payment findings; Seat 2's causal finding) were not contradicted by evidence elsewhere in the artifact and stand. No finding was upheld on headcount.

**Verification result.** Every critical and major finding was re-checked adversarially against the source. **1 withdrawn** (Seat 3, "Status: closed"), **3 narrowed**: the root-cause critical was narrowed from "the document misidentifies the cause" to "the causal *statement* and all three actions target the ceiling while the prose names the mechanism correctly"; the total-failure major was narrowed from "self-contradiction" to "unreconciled and unsourced", because a pod can take a connection and still fail every request; the evening-traffic major fell to minor. Strings searched and located: "memory limit of 512Mi was too low" (Root cause), "No alert fires" (Timeline 02:14), "Recovered orders: 0 — the queue was not durable" (Customer impact), "took traffic, and were killed again" (Root cause), "the other 14 services in the checkout path" (Action item 3), "Once escalated, diagnosis took 28 minutes" (What went well). **No seat's reliability is in question** — the withdrawn item was a defensible reading of an ambiguous status field, not a fabrication.

**Panel blind spots.** Under the sequential fallback, coverage is as suspect as agreement: one context means one set of things not looked at.
- **Uncovered domain: platform/Kubernetes resource engineering.** No seat asked whether 2Gi is any less arbitrary than 512Mi, whether the requests-vs-limits distinction the artifact never mentions changes the eviction story, or what bounding the allocation should look like. **A critical defect could live here**, and this verdict does not cover it.
- **Shared assumption 1 (load-bearing):** that this document is the complete corrective record. If alerting and queue-durability work is tracked elsewhere, findings 2 and 3 drop from critical to major — "not recorded here" rather than "un-actioned".
- **Shared assumption 2:** that the timeline, the 41,300 count, and "the other 14 services" are accurate. All three seats took them at face value; none is verifiable from the document, and each should be confirmed externally before acting.

**Overall judgment.** A well-written record of the wrong depth. The document does the reporting job — accurate chronology, a named mechanism, honest numbers — and fails the analytical one: it converts a release-triggered unbounded-memory fault into a limits-configuration story, and closes with three action items that between them address neither the failure mode, the 2h38m detection gap, nor the disclosed loss of 41,300 orders. Its structure is worth keeping; its conclusions are not.

**Decision on further action.** **Revise substantially before use.**

**Prioritized next steps.**
1. Rewrite the root cause around the unbounded per-request catalogue load and add an action that bounds it; treat 2Gi as mitigation, not fix.
2. Add owned, dated action items for checkout alerting and support→on-call escalation.
3. Raise a durability action item for the order queue, or record a signed acceptance of total order loss in future incidents.
4. Reconcile payment/authorization state for the window and record customer communications.
5. Add an interim exposure check ahead of the 2026-05-09 audit; correct the 28-minute figure and the 42-minute recovery gap.

**Confidence & what would change the verdict.** Of the 7 findings at critical or major, I expect **5 to survive** an independent expert re-check. First to fall: the impact-reconciliation major, if load-balancer data confirms 100% failure — it drops to minor immediately; then the 14-service exposure major, if that audit is already in flight. The two detection/durability criticals narrow to major if corrective tickets exist outside this document. The verdict rests on verified quoted text plus one assumption — that the Action items table is the complete set of corrective actions. What would flip it to *approve with minor revisions*: tracked tickets for alerting and queue durability, plus a bounded-allocation fix, at which point only the causal-statement rewrite and the arithmetic corrections remain.
