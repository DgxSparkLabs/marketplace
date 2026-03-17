# telegram-on-complete

An always-on rule that makes AI agents send a Telegram notification after completing any task. The user gets a concise summary on their phone without needing to ask.

Requires the **[telegram-notify](../telegram-notify/)** skill to be installed alongside this rule.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/telegram-on-complete/install.sh

# Install globally (all projects)
/tmp/marketplace/telegram-on-complete/install.sh --global

# Install for a specific tool only
/tmp/marketplace/telegram-on-complete/install.sh --format windsurf
/tmp/marketplace/telegram-on-complete/install.sh --format cursor
/tmp/marketplace/telegram-on-complete/install.sh --format agents
```

Don't forget to also install the skill:

```bash
cp -r /tmp/marketplace/telegram-notify/ ~/.config/cognition/skills/telegram-notify/
```

## Manual Install

### AGENTS.md (universal)

```bash
cat telegram-on-complete/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp telegram-on-complete/formats/windsurf.md .windsurf/rules/telegram-on-complete.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp telegram-on-complete/formats/cursor.md .cursor/rules/telegram-on-complete.md
```

## What it enforces

- Agent ALWAYS sends a Telegram message after completing a task
- Agent ALWAYS notifies on failure if it cannot recover
- Agent ALWAYS notifies after long-running operations finish
- Agent does NOT spam notifications for mid-task progress updates

## Prerequisites

- The **telegram-notify** skill must be installed (provides the send script and setup flow)
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` must be set (the skill's setup script handles this)

## How it works

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/telegram-on-complete.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/telegram-on-complete.md` | `alwaysApply: true` |
