# simplicity-bar

An always-on rule that enforces a complexity cost/benefit check on every change -- weigh the improvement magnitude against the complexity added, and prefer deletion over addition.

Inspired by the simplicity criterion in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-simplicity-bar@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-simplicity-bar/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- Weigh complexity cost against improvement magnitude before keeping any change
- Prefer code deletion over code addition when results are preserved
- Reject marginal improvements that add disproportionate complexity
- Treat every added line as a maintenance liability that must earn its place

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/simplicity-bar.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/simplicity-bar.md` | `alwaysApply: true` |
