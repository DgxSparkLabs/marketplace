# session-wrapup

End-of-session audit that checks whether a project is ready for the next agent: docs fresh, commits clean, knowledge captured.

## Setup

No setup required. The script is self-contained with no external dependencies.

## Usage

```bash
uv run session-wrapup/scripts/session_wrapup.py
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--dir` | No | Project directory (default: cwd) |
| `--json` | No | Output as JSON |

### Examples

```bash
# Audit current project
uv run session-wrapup/scripts/session_wrapup.py

# Audit a specific project
uv run session-wrapup/scripts/session_wrapup.py --dir /path/to/project

# Machine-readable output
uv run session-wrapup/scripts/session_wrapup.py --json
```

## Checks Performed

| Check | PASS | FAIL |
|-------|------|------|
| Uncommitted changes | Clean working tree | Uncommitted work exists |
| HANDOFF.md freshness | Updated after last commit | Stale or missing |
| PITFALLS.md exists | File present | No knowledge capture file |
| CHANGELOG.md exists | File present | No history file |

## As an Agent Skill

```bash
cp -r session-wrapup/ ~/.config/devin/skills/session-wrapup/
```

Then invoke with `/session-wrapup` in a session.
