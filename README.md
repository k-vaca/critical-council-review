# Critical Council Review

An Agent Skill that reviews your work with a panel of independent experts and then makes a call.

Ask a model to critique something you wrote and you usually get agreement with extra steps. It reads your framing, infers the answer you want, and finds a diplomatic route there. This skill is built to stop that: the seats run in isolation, your opinion of the work never reaches them, and every finding has to carry a verbatim quote you can check in ten seconds.

It ships with an eval set. That is the unusual part.

## Install

```bash
git clone https://github.com/k-vaca/critical-council-review.git
cp -R critical-council-review/critical-council-review ~/.claude/skills/
```

Or drop `critical-council-review.skill` into Claude Desktop.

Then just ask for a review. It triggers on the ordinary phrasings: "review this", "find the flaws", "is this any good", "tear this apart", "get expert eyes on it".

## What it actually does

**Picks a depth first.** Most review requests do not need a council. Paste 60 lines of code and ask if it looks alright, and you get a quick check: a verdict, up to five findings with anchors, three fixes, under 300 words. The full council fires when you ask for an audit, when the artifact is large, or when the stakes justify it. It tells you which one it chose so you can ask for the other.

**Runs the seats blind.** When subagent tooling is available, each expert gets its own context: the artifact, its remit, the roster, nothing else. No seat sees another's verdict. Neither does the verification pass or the executive that issues the decision. When two seats independently land on the same problem, that means something. When they are all reading each other's homework in one context, it does not, and the skill says so out loud rather than pretending otherwise.

**Quarantines your framing.** Anything you said about the work, who wrote it, or what you expect the verdict to be gets recorded separately and withheld from the panel. It is context for what to check. It is not an input to what they conclude.

**Makes every finding falsifiable.** A finding needs a verbatim quote of 25 words or fewer plus a locator you can check without trusting the reviewer. No anchor, no finding. If something is missing rather than wrong, it quotes the place it should have been.

**Verifies before synthesising.** Every critical and major finding gets re-checked against the source adversarially, asking what would make this false rather than whether it can be supported. Findings get marked confirmed, corrected, or withdrawn, and the withdrawal count is reported. The two things this catches most often are a finding built on a phrase the document does not literally contain, and a passage read outside the context that governs it.

**Commits to a decision.** Approve as-is, approve with minor revisions, revise substantially, reject and rework, or insufficient information. One of those, no hedging. Then a confidence note that has to be operational: of the findings reported at critical and major, how many would survive an independent re-check, which ones fall first, and what new information would flip the verdict. "High confidence" with nothing named underneath it is not a confidence statement.

**Says when the work is fine.** A rubber stamp and a manufactured teardown are both failures. If scrutiny finds the thing sound, the correct output is a short honest review, not invented faults to justify the ceremony.

## The eval set

Most skills are a set of instructions someone found convincing. This one comes with a way to check.

`eval/` holds 18 artifacts across code, prose deliverables, and empirical claims, with 90 defects planted at known severity. Every defect is discoverable from the artifact alone: where a defect turns on a fact, the fact is written into the artifact itself, usually in a header or a constraints block. Nothing needs an external lookup.

Three of the 18 are probes with no critical or major defect in them at all. They are there because recall alone rewards a reviewer for listing everything it can imagine, and the failure people actually hit with review tools is a confident wall of nothing. If a review process manufactures faults, the probes are where it shows.

`eval/scoring.md` has the measures, the run protocol, and a decision rule you are meant to write down before you look at any results.

## Honest about what is not settled

The instruction set is derived from review practice, not from measured reviewer accuracy. The skill says so in its own text, marks which rules are load-bearing and which are tunable defaults, and tells the executing model to trust its own measurements over the file.

The council costs several times a single pass. Whether it earns that is the question the eval exists to answer, and the answer is going to depend on your artifacts. Run it on yours.

Also worth knowing: roughly half of what a review skill gets asked to do has no right answer. "Is this positioning any good" is not scoreable against ground truth, and no offline eval will tell you how the skill does there.

## Contributing

Findings the eval misses are the most useful thing you can send. If a run produces a real defect that is not in `eval/ground-truth.md`, open a PR adding it. The amendment procedure is at the bottom of that file.

Issues that say "this rule is wrong and here is the run that shows it" are more welcome than issues that say "this rule seems wrong".

## Licence

MIT.
