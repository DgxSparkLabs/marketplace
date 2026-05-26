---
name: pitfall-check
description: Search PITFALLS.md and git log for known issues before starting work
argument-hint: "[keyword]"
allowed-tools:
  - exec
  - Bash
  - read
  - Read
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Pitfall Check

Search for known pitfalls related to what you're about to work on. Checks both PITFALLS.md and git history.

## When to Use

- Before starting complex implementation work
- Before touching an unfamiliar area of the codebase
- When you encounter a confusing bug that might have been seen before

## Usage

```
uv run $SKILL_DIR/scripts/pitfall_check.py <keyword> [keyword2 ...]
```

### Options

- Positional arguments: one or more keywords to search for
- `--dir` — project directory (default: current working directory)
- `--git-log-limit` — max git log entries to search (default: 200)

## Instructions

1. Extract keywords from the area you're about to work on (function names, module names, error types, feature names).
2. Run the script with those keywords.
3. Read the output. If related pitfalls exist, factor them into your approach before writing code.
4. If no pitfalls are found, proceed normally — but remember to add an entry if you discover one.

User arguments: $ARGUMENTS
