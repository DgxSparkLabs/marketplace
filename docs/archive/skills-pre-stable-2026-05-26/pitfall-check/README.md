# pitfall-check

Search PITFALLS.md and git history for known issues before starting work on a new area.

## Setup

No setup required. The script is self-contained with no external dependencies.

## Usage

```bash
uv run pitfall-check/scripts/pitfall_check.py auth token refresh
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `keywords` | Yes | One or more search terms (positional) |
| `--dir` | No | Project directory (default: cwd) |
| `--git-log-limit` | No | Max git log entries to search (default: 200) |

### Examples

```bash
# Search for pitfalls related to authentication
uv run pitfall-check/scripts/pitfall_check.py auth login session

# Search in a specific project
uv run pitfall-check/scripts/pitfall_check.py --dir /path/to/project database migration

# Limit git log search depth
uv run pitfall-check/scripts/pitfall_check.py --git-log-limit 50 deploy
```

## As an Agent Skill

```bash
cp -r pitfall-check/ ~/.config/devin/skills/pitfall-check/
```

Then invoke with `/pitfall-check auth token` in a session.
