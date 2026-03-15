---
name: _template
description: REPLACE — Short description of what this skill does (under 80 chars)
argument-hint: "[arg1] [arg2]"
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

# REPLACE: Skill Title

One-sentence summary of what this skill does.

## Prerequisites

List what must be set up before the skill can work:
- Environment variables: `export SOME_API_KEY="..."`
- Tools: `uv`, `curl`, etc.
- Services: accounts, API access, etc.

If a prerequisite is missing, tell the user what to do.

## Usage

Show the exact command(s) the agent should run:

```
uv run _template/scripts/example.py --flag "value"
```

### Options

- `--flag` — description of the flag (required/optional)

## Instructions

Parse the user's request and extract the necessary parameters.
Run the command with the appropriate arguments.
Report the result to the user.

User arguments: $ARGUMENTS
