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

### 2b. Prioritisation (added after run 1)

Precision as defined above scored roughly 99% in run 1, which is true and useless. Almost every unplanted finding was *defensible*; very few were *load-bearing*. One arm reported 10 majors on a privacy notice and 7 on a churn memo, mostly completeness observations that a recipient has to triage before acting. Defensibility and prioritisation are different properties and only the first was being measured.

Score both:

```
top-3 hit rate = planted criticals appearing in the review's own top three fixes / min(3, planted criticals)
slot efficiency = C+M findings published / total findings published
```

The verdict block names the top three fixes in order. That ordering is the review's own claim about what matters, and it is checkable against the ground truth without any judgment call.

### 3. Manufactured-fault rate (the gate)

```
manufactured = C+M findings reported across the three probe artifacts
```

**Only `code-03-lru-cache.py` is a probe.** `doc-03` and `claim-05` were built as probes and are not: run 1 found real critical-or-major defects in both, some of them introduced by the author while editing. They are reclassified as ordinary defect-carrying artifacts and their ground-truth entries amended. They were **not** patched, so run 1 stays reproducible against the artifacts it actually ran on.

**Before any artifact ships as a probe, it must pass an adversarial pre-check.** Dispatch an agent whose only instruction is to find a critical or major defect in it, with no mention that it is meant to be clean. It ships as a probe only if that pass comes back empty. Intending an artifact to be clean is not evidence that it is; two of three failed that test in run 1 and the failure was invisible until reviewers hit them. Run 2 needs two new probes built and pre-checked this way.

Target is **zero**. Anything above zero is a direct violation of non-negotiable 1 and it outweighs a recall gain: a review process that invents a critical finding on sound work is worse than one that misses a real one, because the false one costs engineering time and the missed one is usually caught downstream.

Report it as a raw count, not a rate. Three artifacts is too few for a rate to mean anything.

### 4. Severity agreement — not measurable by one author

Run 1 recorded 39 findings tagged critical against 21 planted and called it inflation. That conclusion does not hold. The same person wrote the artifacts, chose the planted severities, and graded the outputs. When three independent reviewers rate "binary floats for currency, against a spec line saying the ledger rejects them" as critical and the ground truth says major, the data cannot distinguish reviewer inflation from author deflation.

**Do not report a severity-calibration result until the planted severities have been labelled by someone who did not write the artifacts.** Two labellers, disagreements resolved by a third, labels frozen before any run. Until that exists, record the distributions and draw no conclusion from them.

Once it exists, of the matched findings only:

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
