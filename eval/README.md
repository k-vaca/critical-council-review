# critical-council-review — eval set

An offline eval for the `critical-council-review` skill. It exists to answer one question the skill cannot currently answer about itself:

> **Does the full council find enough that a single careful pass misses to justify costing six to eight times as much?**

Everything here is built around that comparison. Recall, precision, and severity calibration are the measures; the manufactured-fault gate is the thing that can disqualify a win.

## Contents

```
artifacts/          18 artifacts with defects planted at known severity
ground-truth.md     the sealed defect list — keep out of every reviewing context
scoring.md          the four measures, the decision rule, and the run protocol
results/            one file per run; template.md is the shape
```

## The artifact set

Eighteen artifacts, six per domain, sized across tiers 1 and 2.

| | Code | Prose deliverable | Empirical claim |
|---|---|---|---|
| | `code-01` token manager | `doc-01` incident postmortem | `claim-01` A/B test readout |
| | `code-02` VAT invoice | `doc-02` pricing email | `claim-02` customer survey |
| | `code-03` LRU cache **(probe)** | `doc-03` on-call runbook **(probe)** | `claim-03` build-vs-buy model |
| | `code-04` CSV importer | `doc-04` privacy notice | `claim-04` inference benchmark |
| | `code-05` auth middleware | `doc-05` database migration plan | `claim-05` capacity forecast **(probe)** |
| | `code-06` retry helper | `doc-06` job posting | `claim-06` churn analysis |

89 planted defects: 21 critical, 41 major, 27 minor. 62 of them are critical or major, which is the population recall and precision score against.

Three of the eighteen are **probes** — artifacts with no critical or major defect in them at all. They are there because recall alone rewards a reviewer for reporting everything it can think of, and the failure mode people actually hit with review tools is a wall of confident findings that waste an afternoon. `claim-05` in particular is deliberately the most carefully-reasoned document in the set: a reviewer that manufactures faults will manufacture them there.

Every defect is discoverable from the artifact alone. Where a defect turns on a fact — a spec, a contract clause, a stated ops requirement, a fleet's thread count — that fact is written into the artifact, usually in a header or a constraints section. Nothing requires an external lookup, a repository, or knowledge of a real product. That makes each finding falsifiable and it tests whether the reviewer read the whole thing rather than the first screen.

## Running it

Read `scoring.md` first, then:

1. Write down your decision rule before the first run. The suggested one is in `scoring.md`: ≥15 points of recall gained, no precision lost, zero manufactured faults.
2. Copy `results/template.md` to `results/<date>-<model>.md`.
3. Run all 18 artifacts under the control condition and all 18 under the treatment, in randomised order, each in a fresh context.
4. Grade against `ground-truth.md`. Blind to condition if you can manage it.
5. Fill in the four measures and the cost multiple.

36 runs. Budget accordingly — the treatment arm is the expensive half by design, and finding out how expensive is part of the point.

## Honest limitations

Stated here rather than buried, because an eval that oversells itself is worse than no eval.

- **One author planted every defect.** The defects a review process is worst at finding are the ones nobody thought to plant. Those are absent by construction, so recall here is an upper bound on real-world recall.
- **Eighteen artifacts is small.** A 10-point recall difference on this set is not a reliable 10-point difference in general. Treat differences under about 15 points as noise unless you run the set three times and the spread is tight.
- **Planted defects have right answers.** Roughly half of what this skill gets used for — is this positioning any good, does this argument hold up — does not. That half is unmeasured and will stay unmeasured.
- **The treatment arm is a bundle.** Independence, seat diversity, the verification pass, and the executive re-read all move together. A win tells you the bundle wins, not which part earned it. `scoring.md` describes the third arm that isolates independence, worth adding only if the first comparison comes out close.

## Amending the ground truth

Reviews will find real defects nobody planted. That is a good outcome and the eval should absorb it: add the finding to `ground-truth.md`, mark it with the date and the run that produced it, and re-score anything that depended on the old totals. The procedure is at the bottom of that file.

A ground truth that never changes is a ground truth nobody is testing against.
