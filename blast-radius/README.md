# blast-radius

An always-on rule that enforces change-scoping discipline for AI agents — estimate blast radius before editing, prefer small atomic changes, commit frequently, and stop when stuck instead of spiraling.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/blast-radius/install.sh

# Install globally (all projects)
/tmp/marketplace/blast-radius/install.sh --global

# Install for a specific tool only
/tmp/marketplace/blast-radius/install.sh --format windsurf
/tmp/marketplace/blast-radius/install.sh --format cursor
/tmp/marketplace/blast-radius/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat blast-radius/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp blast-radius/formats/windsurf.md .windsurf/rules/blast-radius.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp blast-radius/formats/cursor.md .cursor/rules/blast-radius.md
```
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
