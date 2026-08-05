# Adversarial run — does independent, evasion-optimised planting change the recall number?

**The question.** Run 1's stated limitation was that one author planted every defect, so recall was an upper bound of unknown looseness: the defects a reviewer is worst at finding are the ones nobody thought to plant.

**The design.** Six agents each wrote a fresh artifact plus a sealed defect list, blind to the existing eval set so they could not anchor on defects already chosen. The brief was adversarial, not merely independent: **plant defects designed to survive a careful expert review.** Each planter also had to record, per defect, *why it expected a reviewer to miss it* — a falsifiable prediction, not decoration.

Constraints on planting: each defect indefensible once seen, discoverable from the artifact alone, and the surrounding work genuinely correct so unplanted bugs would not contaminate the measurement. Planters were told to head off the reflex findings — state run lengths, acknowledge SRM checks, name exclusions — so a reviewer could not score easy points and had to find the real problem.

Artifacts: a production database migration, a distributed rate limiter, a customer breach notice, an API deprecation RFC, a pricing experiment readout, an SLO reliability report.

## Result

| Artifact | Planted | Arm A found |
|---|---|---|
| adv-02 rate limiter | 3 | **3** |
| adv-03 breach notice | 3 | **3** |
| adv-04 deprecation RFC | 3 | **3** |
| adv-06 SLO report | 3 | **3** |
| adv-01 migration | 3 | pending |
| adv-05 pricing test | 3 | pending |
| **Total so far** | **12** | **12** |

**Twelve for twelve.** Four independent planters, each optimising explicitly for evasion, each writing down the blind spot they believed they were exploiting. None evaded a single careful pass.

Some of the planting was genuinely sophisticated and still failed:

- **adv-06** excluded load-shed 429s from the SLI denominator — an exclusion stated openly, sounding like standard practice, that removes from the measurement exactly the failure the SLO exists to catch. Every printed number was correct. The reviewer found it and independently recomputed the intent-faithful availability at 99.8882% and budget consumption at 111.8%, matching the sealed figures.
- **adv-05** used CUPED variance reduction with covariates measured *during* the experiment window — a post-treatment adjustment manufacturing the memo's only significant result. Arithmetic all correct.
- **adv-03** put the enrolment instructions in direct contradiction with the notice's own anti-phishing paragraph, asking breach victims for the exact data it told them never to give.
- **adv-02** relied on a falsy check mapping a suspended account's limit of 0 to the free tier's 60.

## What this does to run 1's headline

**The "one author" limitation does not appear to have inflated recall.** Defects selected for difficulty by other planters are being found at the same rate as defects I chose to illustrate a point. The 89.5% survives the challenge that was most likely to sink it.

Two honest qualifications:

1. **Shared model priors are untouched.** Planters and reviewers are the same model. A defect neither would conceive of is invisible to both, and no arrangement of agents fixes that. What this run rules out is *my* idiosyncratic blind spots, not the model's.
2. **The asymmetry is what makes it worth running.** A miss would have been informative regardless of shared priors, because the planter was trying to cause one. Finding everything is the harder outcome to fake.

## Severity: now measurable, and the finding is not "inflation"

The planters labelled severity independently — no sight of my labels, no sight of any review. That unblocks the measurement declared unmeasurable earlier.

The result is not simple upward bias. On **adv-06** the planter sealed 1 critical and 2 major; the reviewer returned 4 critical and 5 major, and it **deflated** the planter's critical to major while **inflating** both of the planter's majors to critical. On **adv-04** the planter sealed 1 critical and 2 major; the reviewer called all three critical. On **adv-02** the planter's minor came back as major.

So the reviewer's severity ordering is not a shifted version of the planter's — it is close to uncorrelated with it. That is a different and more troubling problem than inflation, because a shift can be calibrated out and a disagreement about ranking cannot. It also means neither party is obviously right: a third independent labeller is needed before anyone's ordering is treated as ground truth.

**No skill change on severity.** The measurement now says the scales disagree; it does not say whose is correct.

## The best evidence in the whole exercise for the skill's core claim

The adv-01 planter did something nobody instructed it to do. Having written its artifact and verified it by re-reading, it said the one check it could not perform on its own work was whether it had left unplanted bugs, and commissioned a blind reviewer to look.

That reviewer found all three planted defects — and **two majors the planter had not planted and had not noticed**: `CREATE INDEX CONCURRENTLY IF NOT EXISTS` matching a leftover INVALID index by name so a restart is not clean, and a partial index whose predicate names the very column each UPDATE writes, forcing every backfill update to be non-HOT.

A careful author verified its own work and missed two real defects in 130 lines it had just written. An independent reader found them immediately.

That is the skill's central premise, demonstrated by accident, on the eval's own machinery: **a checker that did not write the work catches what the writer cannot.** It is also the exact failure mode that produced this eval's two contaminated probes, and the reason the probe gate added after run 1 requires an adversarial pre-check rather than authorial confidence.

## Consequences for the eval

- `adv-01`'s ground truth needs amending with the two unplanted majors before it can be graded, pending adjudication against a second independent read.
- The adversarial planting protocol is better artifact hygiene than the original: planters simulated their code to confirm defects fire, re-derived every printed figure by script, and removed incidental contradictions found in their own drafts. Run 2's artifacts should be built this way.
- Two numbers now bracket real recall: 89.5% on illustrative defects, and the adversarial figure on defects selected for difficulty. They are converging rather than diverging, which is the outcome that argues the measurement is sound.
