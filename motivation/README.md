# motivation

Completeness checker — report what's actually unfinished before stopping. Replaces pep talks with state-based feedback.

## Setup

No external dependencies or API keys needed. Requires `uv` installed.

## Usage

```bash
uv run motivation/scripts/motivate.py
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--json` | No | Output as JSON |

### Sample Output

```
============================================================
COMPLETENESS CHECK
============================================================

  2 issue(s) found:

  [git] 3 modified file(s) not staged
  [handoff] HANDOFF.md has not been updated in the last commit(s) — may be stale

  Fix these before declaring done.

============================================================
```

### JSON Output

```bash
uv run motivation/scripts/motivate.py --json
```

```json
{
  "complete": false,
  "issues": {
    "git": ["3 modified file(s) not staged"],
    "handoff": ["HANDOFF.md has not been updated in the last commit(s)"],
    "tests": [],
    "build": []
  },
  "total_issues": 2
}
```

## What It Checks

- **git**: uncommitted changes, unstaged modifications, untracked files
- **handoff**: HANDOFF.md existence and freshness (stale if not updated in recent commits)
- **tests**: test runner existence
- **build**: build system present but no build directory

## As an Agent Skill

```bash
cp -r motivation/ ~/.config/cognition/skills/motivation/
```

The skill is both user-triggered (`/motivation`) and model-triggered. The agent invokes it before stopping to verify nothing is incomplete.
