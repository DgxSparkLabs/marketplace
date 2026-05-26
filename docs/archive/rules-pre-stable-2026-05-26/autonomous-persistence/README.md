# autonomous-persistence

An always-on rule that prevents agents from pausing to ask unnecessary questions -- keep working autonomously until the task is done or you are explicitly stopped.

Inspired by the autonomous experimentation loop in [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md).

Unlike a skill (which must be invoked), this is a **rule** -- it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/autonomous-persistence/rule.md" .claude/rules/autonomous-persistence.md   # symlink (live updates)
# or:
cp rules/autonomous-persistence/rule.md .claude/rules/autonomous-persistence.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-autonomous-persistence` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


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
