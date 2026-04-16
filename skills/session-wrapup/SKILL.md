---
name: session-wrapup
description: End-of-session audit — check docs, commits, and readiness for the next agent
argument-hint: ""
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

# Session Wrapup

Audit the project's handoff readiness before ending a session. Different from `/motivation` (which checks task completeness) — this checks whether the next agent can pick up smoothly.

## When to Use

- Before ending a session
- After completing a major piece of work
- When switching to a different project

## Usage

```
uv run $SKILL_DIR/scripts/session_wrapup.py
```

### Options

- `--dir` — project directory (default: current working directory)
- `--json` — output as JSON for programmatic use

## What It Checks

| Check | What it means |
|-------|--------------|
| Uncommitted changes | Work in progress that could be lost |
| HANDOFF.md freshness | Was it updated recently relative to last commit? |
| HANDOFF.md exists | The next agent needs this file to start |
| PITFALLS.md exists | Knowledge capture file should be present |
| CHANGELOG.md exists | History file should be present |
| Stale TODO markers | `TODO` comments that may need resolution |

## Instructions

1. Run the script.
2. Read the output. Each check reports PASS, WARN, or FAIL.
3. Fix any FAIL items before ending the session.
4. WARN items are advisory — address if time permits.
5. Do NOT show the raw output to the user. Just act on the findings.

User arguments: $ARGUMENTS
