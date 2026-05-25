# autonomous-persistence

An always-on rule that prevents agents from pausing to ask unnecessary questions -- keep working autonomously until the task is done or you are explicitly stopped.

Inspired by the autonomous experimentation loop in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-autonomous-persistence@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-autonomous-persistence/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- Never ask "should I keep going?" or "is this a good stopping point?"
- Only pause for things the human must genuinely provide (credentials, policy decisions)
- When stuck, think harder -- re-read code, search, try combinations, try radical approaches
- Exhaust all tools and approaches before asking the human for help

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/autonomous-persistence.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/autonomous-persistence.md` | `alwaysApply: true` |
