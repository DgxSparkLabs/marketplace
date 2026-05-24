# blast-radius

An always-on rule that enforces change-scoping discipline for AI agents — estimate blast radius before editing, prefer small atomic changes, commit frequently, and stop when stuck instead of spiraling.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-blast-radius@dgxsparklabs-marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-blast-radius/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- Plan and identify affected files before writing any code
- Prefer small, atomic changes — one logical change per edit session
- Commit after every logical change — never accumulate uncommitted work
- Stop and reassess when stuck instead of spiraling through failed attempts
- Keep it simple — no over-engineering, no meta-tools, no unnecessary abstractions
- Acknowledge complexity limits — break large tasks into manageable pieces

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/blast-radius.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/blast-radius.md` | `alwaysApply: true` |
