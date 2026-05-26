---
name: code-health-audit
description: Audit codebase for DRY violations, oversized files, and scattered definitions
argument-hint: "[directory]"
allowed-tools:
  - read
  - Read
  - exec
  - Bash
  - grep
  - Grep
  - glob
  - Glob
triggers:
  - user
  - model
---

# Code Health Audit

Scan a codebase for maintainability problems and produce a prioritized refactoring plan. The goal is to identify what makes the codebase hard for a human to maintain — not style nits.

## Step 1: Read project context

Check for `CODEBASE.md` at the project root. If it exists, read it — it documents module boundaries, shared type locations, and project-specific conventions. Use this to calibrate your analysis: violations of the project's own documented structure are higher severity.

If `CODEBASE.md` doesn't exist, note this as the first finding.

## Step 2: Run the automated scan

```bash
uv run $SKILL_DIR/scripts/scan_codebase.py $1
```

Options:
- First argument: directory to scan (default: current directory)
- `--max-lines N`: line threshold for large files (default: 300)
- `--json`: output as JSON for programmatic use

The script detects:
- Files exceeding size threshold
- Definition names that appear in multiple files (potential duplication)
- Files with high definition density (many classes/functions)
- Files with generic names (`utils`, `helpers`, `misc`)
- Missing `CODEBASE.md`

## Step 3: Semantic analysis

The script catches mechanical patterns. You must also investigate:

**Scattered definitions.** For each duplicate name the script found, read the actual definitions. Are they truly the same concept defined twice? Same concept in two places = critical finding. Also check for directory paths hardcoded as string literals in multiple files — if the same path appears in 3+ files, it should be defined once in a config module.

**Hidden coupling.** Look for modules that share state through implicit means — both reading the same config file, both hardcoding the same magic string, both defining the same data shape without a shared type. Also look for parallel mappings that duplicate grouping that already exists elsewhere (e.g., a tag→subdirectory dict that copies what tags already express). The data should derive from the existing source, not copy it.

**Responsibility overload.** For each large file, read the first 30 lines (imports and initial declarations reveal scope). List what the file actually does. If it handles N concerns, suggest N files.

**Config vs code boundary.** Look for data hardcoded in source code that should be in config files. The test: if a non-developer needs to add an entry (a new resource, option, or mapping), do they edit Python/TypeScript, or YAML/JSON? Hardcoded registries, lookup tables, and feature lists that change independently of logic should be extracted to config.

**Architecture legibility.** Does the directory structure reflect system boundaries? Could a new developer look at top-level directories and understand what this project is? Are file and function names self-describing, or do they force readers to open the implementation?

**Documentation health.** Check whether docs help a human get oriented and operate the system:

- Does `README.md` exist and is it a concise TL;DR (under ~100 lines)? Or is it a 500-line wall of text that buries the quick start?
- Does a `docs/` directory exist? Are guides named by topic (`getting-started.md`, `deployment.md`) or by artifact (`notes.md`, `TODO.md`)?
- **Hand-holding test**: pick the most important guide. Does it walk a newcomer through step by step — prerequisites, exact commands, expected output, troubleshooting? A good guide reads like a patient mentor. A bad guide reads like notes the author wrote for themselves.
- **Operational runbooks**: for every recurring task (adding a feature, registering a resource, deploying), is there a step-by-step guide? Can someone who has never done it complete the task by following the doc alone?
- Are any docs orphaned (not linked from README or other docs)? Are docs stale (documented commands don't match actual code)? Is terminology consistent?

## Step 4: Report findings

Structure your output as:

```
## Code Health Audit — [project name]

### Critical (fix now)
Duplicate definitions, scattered constants — highest maintenance risk because
changes require updating N places and forgetting one causes bugs.

### Important (fix soon)
Oversized files, mixed responsibilities — hard to navigate and review.

### Suggestions
Naming improvements, structural reorganizations — lower risk but improve
developer experience.

### Documentation
README quality, missing/orphaned/stale guides, hand-holding gaps.

### CODEBASE.md status
Missing / outdated / accurate
```

Each finding must include:
- **What**: the specific problem (e.g., "WorkflowCategory defined in 3 files")
- **Where**: exact file paths
- **Fix**: concrete action ("extract to src/types/workflow.ts, import everywhere")
- **Impact**: why it hurts ("changing a category requires editing 3 files")

## Step 5: Create action items

Convert findings into a prioritized todo list using todo_write. Order by:
1. Duplicate definitions (highest risk — silent breakage)
2. Missing CODEBASE.md (blocks future audits)
3. Oversized files (hardest to navigate)
4. Missing centralization (scattered config, magic strings)
5. Documentation gaps (missing guides, stale docs, no hand-holding for newcomers)
6. Naming improvements (lowest effort, good quick wins)

User arguments: $ARGUMENTS
