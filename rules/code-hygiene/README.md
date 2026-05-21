# code-hygiene

An always-on rule that enforces core software engineering practices: DRY definitions, single-responsibility files, centralized types, human-readable naming, and structural organization.

Prevents the gradual entropy that makes codebases unmaintainable — duplicate definitions scattered across files, oversized modules with mixed responsibilities, and naming that only makes sense to the agent that wrote it.

## Quick Install

```bash
git clone https://github.com/DgxSparkLabs/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/rules/code-hygiene/install.sh

# Install globally (all projects)
/tmp/marketplace/rules/code-hygiene/install.sh --global

# Install for a specific tool only
/tmp/marketplace/rules/code-hygiene/install.sh --format windsurf
/tmp/marketplace/rules/code-hygiene/install.sh --format cursor
/tmp/marketplace/rules/code-hygiene/install.sh --format agents
```

## Manual Install

### AGENTS.md (universal)

```bash
cat rules/code-hygiene/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp rules/code-hygiene/formats/windsurf.md .windsurf/rules/code-hygiene.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp rules/code-hygiene/formats/cursor.md .cursor/rules/code-hygiene.md
```

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
