# Critical Council Review

**An Agent Skill that reviews your work with a panel of independent experts, then commits to a verdict.**

Ask a model to critique something you wrote and you usually get agreement with extra steps. It reads your framing, works out the answer you're hoping for, and finds a diplomatic route there. Every reviewer who ever wanted to keep the peace does the same thing. The difference is that a model does it instantly and sounds confident while doing it.

This skill is built to stop that. The seats run in isolation, your opinion of the work never reaches them, and every finding has to carry a verbatim quote you can check in ten seconds.

Then it does the thing almost nothing else does: **it throws findings away.** A verification pass re-opens the artifact and attacks every critical and major finding before the executive ever sees it. Anything resting on a misreading gets withdrawn, and the withdrawal is reported.

Handed an artifact that was genuinely fine, it withdrew six of its own findings, kept the one that was real, and returned **approve with minor revisions**. That's the whole pitch in one sentence.

## Install

```bash
git clone https://github.com/k-vaca/critical-council-review.git
cp -R critical-council-review/critical-council-review ~/.claude/skills/
```

Or drop `critical-council-review.skill` into Claude Desktop.

Then just ask for a review. It fires on the ordinary phrasings: "review this", "find the flaws", "is this any good", "tear this apart", "get expert eyes on it".

## What it does

**Sizes the job first.** Paste 60 lines and ask if it looks alright, and you get a quick check: verdict, up to five anchored findings, three fixes, under 300 words. The full council fires when you ask for an audit, when the artifact is large, or when the stakes justify it. It tells you which one it picked so you can ask for the other.

**Runs the seats blind.** Each expert gets its own context: the artifact, its remit, the roster, nothing else. No seat sees another's verdict. Neither does the verification pass, nor the executive that issues the decision.

**Quarantines your framing.** Anything you said about the work, who wrote it, or what verdict you expect gets recorded separately and withheld from the panel. It's context for what to check. It never touches what they conclude.

**Anchors every finding.** A finding needs a verbatim quote of 25 words or fewer plus a locator you can verify without trusting the reviewer. No anchor, no finding. If something is missing rather than wrong, it quotes the place it should have been.

**Verifies before it synthesises.** Every critical and major finding gets re-checked against the source adversarially, asking what would make this false rather than whether it can be supported. Across the recorded runs, the verification pass withdrew or narrowed findings in 14 of 18 reviews.

**Tests why the panel agrees.** Convergence between blind readers looks like strong evidence and often isn't, because they can inherit the same unexamined premise from the same source text. The executive names the shared premise before it credits the agreement. On one run, three seats that couldn't see each other landed on the same silent assumption, and the verification pass caught it.

**Commits to a decision.** Approve as-is, approve with minor revisions, revise substantially, reject and rework, or insufficient information. One of those, no hedging. Then a confidence note that has to be operational: how many findings would survive an independent re-check, which fall first, and what would flip the verdict.

**Ranks what it gives you.** Findings are capped by tier and ordered by what breaks for the recipient. Minor findings get cut first and cut hardest. The verdict block leads with the three fixes that matter and names where each applies, so a reader who stops after 120 words already knows what to change and in what order.

**Says when the work is fine.** A rubber stamp and a manufactured teardown are both failures. When scrutiny finds the thing sound, a short honest review is the right output.

## It ships with an eval

Most skills are a set of instructions someone found convincing. This one comes with the receipts.

`eval/` holds 18 artifacts across code, prose deliverables and empirical claims, carrying 89 defects planted at known severity, plus the sealed defect lists, the scoring protocol, and every raw review the runs produced. You can read exactly what it wrote.

There's a second round in there too. Six independent authors each wrote a fresh artifact and were briefed to plant defects **designed to survive a careful expert review**, recording in advance which blind spot they thought they were exploiting. Load-shed responses quietly excluded from an availability calculation. A statistical adjustment computed from data measured after treatment. A falsy check mapping a suspended account to the free tier. Every printed number correct, so there were no cheap points on offer.

`eval/scoring.md` has the protocol and a decision rule you write down before you look at any results. Point it at your own artifacts and see what it does.

## Why this one

Review tools are easy to write and hard to trust. The usual failure isn't missing things, it's burying you: fifteen confident findings, most of them technically true, none of them ranked, and no way to tell which three actually matter. You end up doing the triage the tool was supposed to do for you.

This one is built against exactly that. It caps what it publishes, ranks by consequence, withdraws what doesn't survive a second look, and puts a checkable quote under every claim it makes.

And it will tell you your work is good when your work is good.

## Contributing

Findings the eval misses are the most useful thing you can send. If a run turns up a real defect that isn't in `eval/ground-truth.md`, open a PR adding it. The amendment procedure is at the bottom of that file.

Issues that say "this rule is wrong and here's the run that shows it" are more welcome than issues that say "this rule seems wrong."

## Licence

MIT. Take it, fork it, ship it.
