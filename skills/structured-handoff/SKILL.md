---
name: structured-handoff
description: Generate structured task files for autonomous agent sessions
argument-hint: "[task description]"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Structured Handoff

Generate a structured set of files — rules, scope, research, and sequential tasks — to prepare work for autonomous AI agent execution.

This skill creates a `.tasks/` directory (or custom location) with:
- **rules.md** — Coding conventions, linting preferences, architecture patterns, file conventions, and testing requirements
- **scope.md** — High-level objective, context, success criteria, and constraints
- **research.md** — References to all files involved, dependencies, and external links
- **tasks/** — Numbered task files (task-00.md, task-01.md, ...) that can be queued up for sequential autonomous execution

This approach is based on a workflow pattern for running long autonomous coding sessions: break work into structured, sequential tasks with clear acceptance criteria so an agent can execute them one by one without further guidance.

## Prerequisites

- `uv` must be available on the PATH

No API keys or environment variables are required.

## Usage

```
uv run structured-handoff/scripts/generate_handoff.py --task "TASK_DESCRIPTION" [--dir OUTPUT_DIR] [--num-tasks N]
```

### Options

- `--task` — Description of what needs to be done (required)
- `--dir` — Output directory (optional, default: `.tasks`)
- `--num-tasks` — Number of task files to generate (optional, default: `5`)

## Instructions

1. Parse the user's request to extract the task description and any preferences for output directory or number of tasks.
2. Run the generate command:
   ```
   uv run structured-handoff/scripts/generate_handoff.py --task "USER_TASK" --dir ".tasks" --num-tasks 5
   ```
3. After generating the structure, read the created files and help the user fill in the details based on the project:
   - Analyze the codebase to populate `research.md` with relevant file paths
   - Break the task into concrete sequential steps in the task files
   - Suggest coding conventions for `rules.md` based on existing project patterns
   - Expand `scope.md` with context derived from the codebase

User arguments: $ARGUMENTS
