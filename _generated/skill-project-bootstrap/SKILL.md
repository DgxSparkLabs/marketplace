---
name: project-bootstrap
description: Initialize project docs — AGENTS.md, HANDOFF.md, CHANGELOG.md, PITFALLS.md
argument-hint: "[project-name]"
allowed-tools:
  - exec
  - Bash
  - read
  - Read
  - edit
  - Edit
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Project Bootstrap

Create the three-tier documentation structure for a new or existing project so agents have the files they need from the start.

## When to Use

- Starting a new project
- Joining a project that has no AGENTS.md, HANDOFF.md, or CHANGELOG.md
- After noticing that project docs are missing or incomplete

## Usage

```
uv run $SKILL_DIR/scripts/bootstrap.py
```

### Options

- `--name` — project name for the AGENTS.md header (default: current directory name)
- `--dir` — target directory (default: current working directory)
- `--force` — overwrite existing files (default: skip files that exist)
- `--dry-run` — show what would be created without writing

## What It Creates

| File | Purpose |
|------|---------|
| `AGENTS.md` | Project-specific rules and conventions (Tier 1) |
| `HANDOFF.md` | Current project state — what works, how to build/test, what's next (Tier 2) |
| `CHANGELOG.md` | History — append-only milestone log (Tier 3) |
| `PITFALLS.md` | Knowledge base of bugs encountered and lessons learned |

Each file is created with a minimal template. Existing files are preserved unless `--force` is used.

## Instructions

If the user provides a project name, use `--name`. Otherwise let it default.
Run the script, then report which files were created and which were skipped.

User arguments: $ARGUMENTS
