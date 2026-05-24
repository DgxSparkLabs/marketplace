# code-health-audit

Audit a codebase for maintainability problems and produce a prioritized refactoring plan. Combines automated scanning (file sizes, duplicate definitions, naming) with agent-driven semantic analysis (hidden coupling, responsibility overload, architecture legibility).

Designed to work with the [code-hygiene](../../rules/code-hygiene/) rule — the rule prevents new problems, the skill finds existing ones.

## Setup

No setup required. The scan script has no external dependencies.

## Usage

Invoke in an agent session:

```
/code-health-audit [directory]
```

Or run the scan script directly:

```bash
uv run code-health-audit/scripts/scan_codebase.py [directory]
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `directory` | No | Path to scan (default: current directory) |
| `--max-lines` | No | Line threshold for "large file" (default: 300) |
| `--json` | No | Output as JSON for programmatic use |

### Examples

```bash
# Scan current project
uv run code-health-audit/scripts/scan_codebase.py

# Scan with a lower threshold
uv run code-health-audit/scripts/scan_codebase.py --max-lines 200 src/

# JSON output for scripting
uv run code-health-audit/scripts/scan_codebase.py --json > health.json
```

## What it detects

### Automated (script)

- **Large files** — over the line threshold (default 300)
- **Duplicate definitions** — type, class, enum, const, function names appearing in multiple files
- **High-density files** — files with 20+ definitions (likely mixed responsibilities)
- **Generic file names** — `utils`, `helpers`, `misc`, `common`, etc.
- **Missing CODEBASE.md** — no structural documentation

### Semantic (agent analysis)

- **Scattered definitions** — same concept independently defined in multiple modules
- **Hidden coupling** — modules sharing state through files or conventions instead of imports
- **Responsibility overload** — files handling multiple concerns
- **Naming clarity** — functions like `process()`, `handle()`, `getData()` without qualifiers
- **Architecture legibility** — whether directory structure reflects system boundaries

## CODEBASE.md

The skill reads `CODEBASE.md` at the project root for project-specific context. This file should document:

- Module boundaries and their responsibilities
- Where shared types and constants live
- Directory purpose map
- Key abstractions and data flow
- Project-specific conventions

The companion [code-hygiene](../../rules/code-hygiene/) rule instructs agents to maintain this file.

## As an Agent Skill

```bash
ln -s "$(pwd)/skills/code-health-audit" ~/.config/devin/skills/code-health-audit
```

Then invoke with `/code-health-audit` or `/code-health-audit src/` in a session.
