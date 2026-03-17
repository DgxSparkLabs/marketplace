---
name: motivation
description: Completeness checker — report what's actually unfinished before stopping
argument-hint: ""
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

# Completeness Check

Run the completeness checker to see what's objectively unfinished before you stop working.

## When to Activate

Invoke this **yourself** whenever you're about to:
- Declare a task complete
- Ask "Would you like me to..."
- Write a summary with pending work remaining
- Stop after hitting an error instead of debugging it

## What to Do

1. Run the checker:
   ```
   uv run motivation/scripts/motivate.py
   ```

2. Read the output. It reports concrete issues:
   - Uncommitted changes in git
   - HANDOFF.md not updated recently
   - Missing test runner or build artifacts
   - Any other structural incompleteness

3. If issues are found, fix them before stopping. If all clear, verify:
   - All todo items marked complete?
   - Test suite run and passing?
   - HANDOFF.md accurate?

4. Do NOT output the check results to the user. This is internal. Just act on it.

## Options

```
uv run motivation/scripts/motivate.py          # human-readable output
uv run motivation/scripts/motivate.py --json   # machine-readable JSON
```

User arguments: $ARGUMENTS
