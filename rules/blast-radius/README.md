# blast-radius

An always-on rule that enforces change-scoping discipline for AI agents — estimate blast radius before editing, prefer small atomic changes, commit frequently, and stop when stuck instead of spiraling.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/blast-radius/rule.md" .claude/rules/blast-radius.md   # symlink (live updates)
# or:
cp rules/blast-radius/rule.md .claude/rules/blast-radius.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-blast-radius` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


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
