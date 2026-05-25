# document-progress

An always-on rule that requires AI agents to plan large tasks upfront using the `structured-handoff` skill and write progress to disk as they work — so nothing is lost to context compaction, session timeouts, or model forgetfulness.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/document-progress/rule.md" .claude/rules/document-progress.md   # symlink (live updates)
# or:
cp rules/document-progress/rule.md .claude/rules/document-progress.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-document-progress` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


## What it enforces

- Create a structured task plan (via `structured-handoff` skill or manually) before starting multi-step work
- Write progress to disk after each completed step — not just in conversation context
- Update task files as work is done: mark complete, note changes, record decisions
- Commit after every logical step so git history captures durable progress
- Never start multi-step work without a written plan

## Companion skill

This rule is designed to work with the [structured-handoff](../structured-handoff/) skill, which generates the `.tasks/` directory structure automatically. Install both for the full workflow:

```bash
/plugin install skill-structured-handoff@dgxsparklabs-marketplace
/plugin install rule-document-progress@dgxsparklabs-marketplace
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-document-progress/activate.sh
```

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/document-progress.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/document-progress.md` | `alwaysApply: true` |
