# Critical Council Review

**An Agent Skill that reviews your work with a panel of independent experts, then commits to a verdict.**

Ask a model to critique something you wrote and you usually get agreement with extra steps. It reads your framing, works out the answer you're hoping for, and finds a diplomatic route there. Every reviewer who has ever wanted to keep the peace does the same thing. The difference is that a model does it instantly and sounds confident while doing it.

This skill is built to stop that. The seats run in isolation, your opinion of the work never reaches them, and every finding has to carry a verbatim quote you can check in ten seconds.

Then it goes further, and this is the part that matters: **it throws findings away.** A verification pass re-opens the artifact and attacks every critical and major finding before the executive ever sees it. Findings that turn out to rest on a misreading get withdrawn and reported as withdrawn.

It ships with an eval. That's the unusual part.

## Install

```bash
git clone https://github.com/k-vaca/critical-council-review.git
cp -R critical-council-review/critical-council-review ~/.claude/skills/
```

Or drop `critical-council-review.skill` into Claude Desktop.

Then just ask for a review. It fires on the ordinary phrasings: "review this", "find the flaws", "is this any good", "tear this apart", "get expert eyes on it".

## The numbers

Most skills are a set of instructions someone found convincing. This one has been run against 18 artifacts carrying 89 defects planted at known severity, with every raw review committed to this repo so you can read what it actually produced.

| | One careful pass | This skill |
|---|---|---|
| Planted defects found | 89.5% | **94.4%** |
| Findings withdrawn at verification | none possible | **14 of 18 runs** |
| On a deliberately sound artifact | 3 findings | **withdrew 6, approved the work** |

That last row is the one to look at. Give a review tool something that's actually fine and watch what happens: most of them find problems anyway, because finding problems is what they were asked to do. This one withdrew six of its own findings, kept the one that was real, and returned **approve with minor revisions**.

It also caught things the single pass didn't. A stacked set of hiring requirements that no candidate could satisfy. A retention clause with no coverage for user-uploaded content. And on a cost model, three seats that couldn't see each other still converged on the same unexamined assumption, which the verification pass caught and corrected rather than rubber-stamping.

## What it actually does

**Picks a depth first.** Most review requests don't need a council. Paste 60 lines and ask if it looks alright, and you get a quick check: verdict, up to five anchored findings, three fixes, under 300 words. The full council fires when you ask for an audit, when the artifact is large, or when the stakes justify it. It tells you which one it chose so you can ask for the other.

**Runs the seats blind.** Each expert gets its own context: the artifact, its remit, the roster, nothing else. No seat sees another's verdict. Neither does the verification pass or the executive that issues the decision.

**Quarantines your framing.** Anything you said about the work, who wrote it, or what verdict you expect gets recorded separately and withheld from the panel. It's context for what to check. It's never an input to what they conclude.

**Makes every finding checkable.** A finding needs a verbatim quote of 25 words or fewer plus a locator you can verify without trusting the reviewer. No anchor, no finding. If something is missing rather than wrong, it quotes the place it should have been.

**Tests why the panel agrees.** Convergence between blind readers looks like strong evidence and often isn't, because they can inherit the same unexamined premise from the same source text. The executive has to name the shared premise before it credits the agreement.

**Commits to a decision.** Approve as-is, approve with minor revisions, revise substantially, reject and rework, or insufficient information. One of those, no hedging. Then a confidence note that has to be operational: how many findings would survive an independent re-check, which fall first, and what would flip the verdict.

**Says when the work is fine.** A rubber stamp and a manufactured teardown are both failures. When scrutiny finds the thing sound, a short honest review is the correct output.

## The eval

`eval/` holds the whole thing: 18 artifacts across code, prose deliverables and empirical claims, the sealed defect lists, the scoring protocol, and every review from both arms.

There's a second round in there too. Six independent authors each wrote a fresh artifact and were briefed to plant defects **designed to survive a careful expert review**, recording in advance which blind spot they thought they were exploiting. Load-shed responses quietly excluded from an availability calculation. A statistical adjustment using data measured after treatment. A falsy check mapping a suspended account to the free tier. Every printed number correct, so there were no easy points to score.

Read `eval/scoring.md` for the protocol and the decision rule you're meant to write down before looking at any results. Then run it on your own artifacts, because that's the only number that decides anything for you. Everything you need is in the repo.

## Why this one

Review skills are easy to write and hard to trust. The usual failure isn't that they miss things, it's that they bury you: fifteen confident findings, most of them technically true, none of them ranked, and no way to tell which three actually matter. You end up doing the triage the tool was supposed to do.

This one is built against that. Findings are capped by tier and ranked by what breaks for the recipient. Minor findings get cut first and cut hardest. The verdict block leads with the three fixes that matter and names where each one applies, so a reader who stops after 120 words already knows what to change and in what order.

And when it's wrong, you can tell immediately, because every finding carries the quote it rests on.

## Contributing

Findings the eval misses are the most useful thing you can send. If a run turns up a real defect that isn't in `eval/ground-truth.md`, open a PR adding it. The amendment procedure is at the bottom of that file.

Issues that say "this rule is wrong and here's the run that shows it" are more welcome than issues that say "this rule seems wrong."

## Licence

MIT. Take it, fork it, ship it.
