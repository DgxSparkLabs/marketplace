# stay-motivated

Prevent the agent from stopping prematurely — keep working until truly done. An always-on rule that fires every session, reminding the agent to check its todo list, debug errors instead of reporting them, and keep shipping until all tasks are complete.

## Why This Exists

Agents tend to stop early: they ask "would you like me to..." instead of doing, they report errors instead of debugging, and they declare "done" with pending tasks. This rule injects a persistent nudge into every session based on patterns observed across 58 real sessions.

Pairs with the [motivation](../motivation/) skill for on-demand encouragement from the user's own words.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/stay-motivated/rule.md" .claude/rules/stay-motivated.md   # symlink (live updates)
# or:
cp rules/stay-motivated/rule.md .claude/rules/stay-motivated.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-stay-motivated` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What It Does

The rule is passive — no scripts, no dependencies. It adds a checklist to the agent's context that triggers before any "stopping" behavior:

1. **Self-check**: 7 questions to ask before stopping (pending todos? untested code? errors to debug?)
2. **Recovery**: Points to the `/motivation` skill for a real quote from session history
3. **Standing instructions**: 5 direct quotes from the user establishing the expected work ethic
4. **Definition of done**: Concrete checklist (todos complete, tests pass, committed, notified)

## Supported Formats

| Format | File | Activation |
|--------|------|------------|
| AGENTS.md | `rule.md` | Always active |
| Windsurf | `formats/windsurf.md` | `trigger: always_on` |
| Cursor | `formats/cursor.md` | `alwaysApply: true` |
