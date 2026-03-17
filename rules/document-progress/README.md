# document-progress

An always-on rule that requires AI agents to plan large tasks upfront using the `structured-handoff` skill and write progress to disk as they work — so nothing is lost to context compaction, session timeouts, or model forgetfulness.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/document-progress/install.sh

# Install globally (all projects)
/tmp/marketplace/document-progress/install.sh --global

# Install for a specific tool only
/tmp/marketplace/document-progress/install.sh --format windsurf
/tmp/marketplace/document-progress/install.sh --format cursor
/tmp/marketplace/document-progress/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat document-progress/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp document-progress/formats/windsurf.md .windsurf/rules/document-progress.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp document-progress/formats/cursor.md .cursor/rules/document-progress.md
```
## What it enforces

- Create a structured task plan (via `structured-handoff` skill or manually) before starting multi-step work
- Write progress to disk after each completed step — not just in conversation context
- Update task files as work is done: mark complete, note changes, record decisions
- Commit after every logical step so git history captures durable progress
- Never start multi-step work without a written plan

## Companion skill

This rule is designed to work with the [structured-handoff](../structured-handoff/) skill, which generates the `.tasks/` directory structure automatically. Install both for the full workflow:

```bash
cp -r /tmp/marketplace/structured-handoff ~/.config/devin/skills/structured-handoff
/tmp/marketplace/document-progress/install.sh --global
```

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/document-progress.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/document-progress.md` | `alwaysApply: true` |
