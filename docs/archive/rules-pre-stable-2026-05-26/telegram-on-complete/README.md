# telegram-on-complete

An always-on rule that makes AI agents send a Telegram notification after completing any task. The user gets a concise summary on their phone without needing to ask.

Requires the **[telegram-notify](../../skills/telegram-notify/)** skill to be installed alongside this rule.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/telegram-on-complete/rule.md" .claude/rules/telegram-on-complete.md   # symlink (live updates)
# or:
cp rules/telegram-on-complete/rule.md .claude/rules/telegram-on-complete.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-telegram-on-complete` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- Agent ALWAYS sends a Telegram message after completing a task
- Agent ALWAYS notifies on failure if it cannot recover
- Agent ALWAYS notifies after long-running operations finish
- Agent does NOT spam notifications for mid-task progress updates

## Prerequisites

- The **telegram-notify** skill must be installed (provides the API call instructions and setup flow)
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` must be set (see the skill's README for setup instructions)

## How it works

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/telegram-on-complete.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/telegram-on-complete.md` | `alwaysApply: true` |
