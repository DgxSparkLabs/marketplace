# telegram-on-complete

An always-on rule that makes AI agents send a Telegram notification after completing any task. The user gets a concise summary on their phone without needing to ask.

Requires the **[telegram-notify](../../skills/telegram-notify/)** skill to be installed alongside this rule.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-telegram-on-complete@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-telegram-on-complete/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

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
