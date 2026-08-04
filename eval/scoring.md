# Scoring

Three numbers per condition, plus one gate. Everything else is diagnostic.

## The four measures

### 1. Recall (critical + major only)

```
recall = planted C+M findings the review identified / planted C+M findings in the artifacts run
```

A planted defect counts as identified when the review names the same underlying problem. Different wording is fine. Different *cause* is not: "the memory limit is too low" does not match doc-01 defect 1, which is that the root cause is proximate and the action items address the wrong layer. If you find yourself arguing for a partial match, score it 0.5 and note it — but if more than about 15% of your matches are halves, your ground truth entries are too vague and need rewriting.

Minor defects are excluded from recall. They are noise at this sample size and nobody makes a decision on them.

### 2. Precision (critical + major only)

Sort every C/M finding the review reported into three buckets:

| Bucket | Counts as |
|---|---|
| **Matched** — maps to a planted defect | true positive |
| **Unplanted, real** — not in the ground truth, but you judge it a genuine defect on inspection | true positive, *and* amend `ground-truth.md` |
| **Spurious** — wrong, invented, unanchorable, or a preference tagged as a defect | false positive |

```
precision = (matched + unplanted-real) / all C+M findings reported
```

Grade the unplanted-real bucket honestly and grade it *before* you know which condition produced it. This is where the eval is easiest to fool yourself with — a plausible-sounding finding you can't be bothered to check will inflate precision for whichever arm you were rooting for.

### 3. Manufactured-fault rate (the gate)

```
manufactured = C+M findings reported across the three probe artifacts
```

Probes are `code-03-lru-cache.py`, `doc-03-oncall-runbook.md`, `claim-05-capacity-forecast.md`. Target is **zero**. Anything above zero is a direct violation of non-negotiable 1 and it outweighs a recall gain: a review process that invents a critical finding on sound work is worse than one that misses a real one, because the false one costs engineering time and the missed one is usually caught downstream.

Report it as a raw count, not a rate. Three artifacts is too few for a rate to mean anything.

### 4. Severity agreement

Of the matched findings only:

```
exact = matched findings where reported severity == planted severity
adjacent = matched findings off by exactly one band
```

Report both. Systematic inflation (major → critical) and systematic deflation are different failures with different causes, so record the direction, not just the magnitude.

## The comparison

The only question this eval exists to answer is whether the council earns its cost. Run every artifact twice:

- **Control:** one careful pass. Same model, no skill invoked, prompt: *"Review this artifact critically. Report every defect you find with a severity of critical, major, or minor, an anchoring quote, and a location."*
- **Treatment:** the full council path of `critical-council-review`, tier as the skill selects it.

Log tokens and wall-clock for both. The treatment has to beat the control by enough to justify the multiple:

```
cost multiple = treatment output tokens / control output tokens
```

**A useful decision rule, set before you look at the results:** the council is worth its cost if it gains at least 15 percentage points of recall over the control *and* does not lose precision *and* holds the manufactured-fault gate at zero. If it gains recall by inventing findings, that is not a gain. If it gains 4 points of recall for 7× the tokens, keep the single pass and delete the ceremony.

Write your threshold down before the first run. Deciding what counts as a win after seeing the numbers is how every internal eval talks itself into the answer it wanted.

## Protocol

1. **Fresh context per artifact per condition.** 36 runs. A model that has already reviewed an artifact under one condition cannot be trusted to review it under the other.
2. **Never put `ground-truth.md` in a reviewing context.** Not as a file, not as a path the model can read, not summarised.
3. **Randomise order.** Do not run all controls then all treatments; drift in your own grading over a long session is real and it will correlate with condition.
4. **Grade blind where you can.** Strip the condition label from the outputs before grading, or have the grading done by someone who does not know which is which. If you are grading your own runs and know the condition, say so in the results file — it is a limitation, not a disqualifier.
5. **One artifact, one run, per condition.** Do not re-roll a bad run. If you want variance estimates, run the whole set three times and report the spread rather than picking.

## What this does not measure

Say it out loud in any writeup, because the temptation to over-claim from 18 artifacts is strong.

- **Not generality.** Eighteen artifacts across three domains, all written by one author, all with defects that author chose to plant. Defects nobody thinks to plant are exactly the defects a review process is worst at finding, and they are absent here by construction.
- **Not real-world value.** Recall against planted defects is a proxy. The thing that matters is whether the review changed what the recipient did, and no offline eval measures that.
- **Not calibration on open-ended quality.** Every defect here has a right answer. "Is this positioning any good" does not, and roughly half of what the skill gets used for is that kind of question.
- **Not the independence mechanism in isolation.** The treatment arm bundles independence with seat diversity, a verification pass, and an executive re-read. If it wins, you know the bundle wins. To isolate independence you need a third arm: the same seats, same fields, run sequentially in one context.

The third arm is worth adding if the first comparison is close. If the council loses outright, the mechanism question is moot.
