# Run: <date> · <model + version> · <who graded>

**Decision rule, written before the first run:**
> <e.g. council wins if recall +≥15pp, precision not lower, manufactured faults = 0>

**Graded blind to condition?** yes / no
**Runs per artifact per condition:** 1
**Notes on setup:** <skill version hash, temperature, anything non-default>

---

## Headline

| | Control (one pass) | Treatment (full council) | Δ |
|---|---|---|---|
| Recall (C+M) | | | |
| Precision (C+M) | | | |
| Manufactured faults (probes) | | | |
| Severity exact match | | | |
| Severity adjacent | | | |
| Output tokens (total) | | | |
| Wall clock (total) | | | |

**Cost multiple:** ×
**Verdict against the rule stated above:**

---

## Per artifact

C+M only. `found / planted` for recall, and the raw count of spurious findings.

| Artifact | Planted C+M | Control found | Control spurious | Council found | Council spurious |
|---|---|---|---|---|---|
| code-01 token manager | 3 | | | | |
| code-02 invoice | 5 | | | | |
| **code-03 lru cache (probe)** | **0** | | | | |
| code-04 csv import | 4 | | | | |
| code-05 auth middleware | 4 | | | | |
| code-06 retry | 2 | | | | |
| doc-01 postmortem | 4 | | | | |
| doc-02 pricing email | 3 | | | | |
| **doc-03 runbook (probe)** | **0** | | | | |
| doc-04 privacy notice | 5 | | | | |
| doc-05 migration plan | 5 | | | | |
| doc-06 job posting | 4 | | | | |
| claim-01 a/b test | 4 | | | | |
| claim-02 survey | 5 | | | | |
| claim-03 cost model | 5 | | | | |
| claim-04 benchmark | 5 | | | | |
| **claim-05 forecast (probe)** | **0** | | | | |
| claim-06 churn | 4 | | | | |
| **Total** | **62** | | | | |

---

## Unplanted but real

Findings neither arm's ground-truth entry covers, judged genuine on inspection. Add each to `ground-truth.md` after this run.

| Artifact | Condition | Finding | Severity | Added to ground truth? |
|---|---|---|---|---|

## Spurious findings worth recording

The ones that reveal a pattern, not every miss. What did the reviewer invent, and does it recur?

| Artifact | Condition | What it claimed | Why it's wrong |
|---|---|---|---|

---

## Observations

Things the numbers do not carry. Did the council's verdict differ from the control's decision, and would that have changed what you did? Did the verification pass withdraw anything, and was the withdrawal correct? Did either arm miss a whole category — e.g. all the security defects, all the arithmetic?

## What I would change about this eval

