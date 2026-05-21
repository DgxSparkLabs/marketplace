# revert-on-failure

An always-on rule that enforces a commit-experiment-measure-revert loop for speculative changes -- commit a known-good baseline, try one thing, measure, keep if improved, revert if not.

Inspired by the experiment loop in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-revert-on-failure@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-revert-on-failure/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- Always commit a clean baseline before making speculative changes
- Test each change individually -- no batching untested experiments
- Keep changes that measurably improve, revert everything else
- Use judgment on crashes: fix trivial issues, abandon broken ideas
- Abandon an approach after 3 failed attempts -- try a different angle

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/revert-on-failure.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/revert-on-failure.md` | `alwaysApply: true` |
