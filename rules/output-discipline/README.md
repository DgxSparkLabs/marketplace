# output-discipline

An always-on rule that enforces context hygiene -- redirect verbose command output to files and extract only what you need with targeted reads.

Inspired by the output management strategy in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-output-discipline@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-output-discipline/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- Redirect verbose commands to log files instead of flooding agent context
- Use targeted extraction (grep, tail, head) to read only what's needed
- Diagnose failures from the end of logs, not the beginning
- Clean up temporary output files after use

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/output-discipline.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/output-discipline.md` | `alwaysApply: true` |
