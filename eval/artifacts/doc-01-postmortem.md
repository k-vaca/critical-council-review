# Incident 2026-04-11 — Checkout unavailable for 4h12m

**Status:** closed
**Author:** platform on-call
**Severity:** SEV-1
**Customer impact:** checkout returned 503 for all traffic from 02:14 to 06:26 UTC. 41,300 attempted orders failed. Recovered orders: 0 — the queue was not durable.

## Timeline

- **02:14** — `checkout-api` pods begin restarting. No alert fires.
- **02:31** — First customer report via support chat.
- **04:40** — Support escalates to platform on-call after the fifth report.
- **04:52** — On-call acknowledges. Finds `checkout-api` in CrashLoopBackOff.
- **05:20** — Root cause identified: the pods were OOM-killed. Memory limit was 512Mi.
- **05:44** — Limit raised to 2Gi, pods roll out.
- **06:26** — Error rate returns to baseline. Incident closed.

## Root cause

The `checkout-api` memory limit of 512Mi was too low. The 2026-04-10 release added the cart-recommendation call, which holds the full catalogue slice in memory per request. Under normal evening traffic this exceeded 512Mi and the kubelet killed the pods. The pods restarted, took traffic, and were killed again.

## What went well

- Once escalated, diagnosis took 28 minutes.
- The rollout of the new limit was clean and needed no rollback.

## Action items

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Raise `checkout-api` memory limit to 2Gi | platform | done |
| 2 | Add a memory-limit review step to the release checklist | platform | 2026-04-25 |
| 3 | Audit memory limits on the other 14 services in the checkout path | platform | 2026-05-09 |

## Lessons

Memory limits set before a service's workload is understood will eventually be wrong. The release checklist change in action item 2 should prevent a repeat.
