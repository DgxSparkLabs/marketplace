# code-hygiene

An always-on rule that enforces core software engineering practices: DRY definitions, single-responsibility files, centralized types, human-readable naming, and structural organization.

Prevents the gradual entropy that makes codebases unmaintainable — duplicate definitions scattered across files, oversized modules with mixed responsibilities, and naming that only makes sense to the agent that wrote it.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-code-hygiene@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-code-hygiene/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- **Search before defining** — grep for existing types/constants before creating new ones
- **Centralize definitions** — types, enums, constants in dedicated files, not inline
- **Import, don't redefine** — zero tolerance for duplicate definitions
- **Single responsibility** — one file, one job, ~300 line target
- **Human-readable names** — no `utils`, `helpers`, `misc`, `processData()`
- **Refactor alongside** — consolidate duplication when you touch code
- **Delete dead code** — remove unused imports, branches, functions on sight
- **CODEBASE.md** — maintain a structural map of the project
- **Directory structure** — `src/`, `docs/`, `scripts/`, `config/`

## Companion skill

Use with [code-health-audit](../../skills/code-health-audit/) to scan an existing codebase for violations and produce a prioritized refactoring plan.

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/code-hygiene.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/code-hygiene.md` | `alwaysApply: true` |
