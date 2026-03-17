# structured-handoff

Generate structured task files (rules, scope, research, and sequential tasks) for autonomous AI agent sessions.

## Setup

1. Ensure `uv` is installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

No API keys or environment variables are required.

## Usage

The script is self-contained with inline dependencies (PEP 723). No install step needed:

```bash
uv run structured-handoff/scripts/generate_handoff.py --task "Refactor the auth module to use dependency injection"
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--task` | Yes | Description of what needs to be done |
| `--dir` | No | Output directory (default: `.tasks`) |
| `--num-tasks` | No | Number of task files to generate (default: `5`) |

### Examples

```bash
# Basic usage — generates 5 task files in .tasks/
uv run structured-handoff/scripts/generate_handoff.py --task "Migrate database layer from SQLite to PostgreSQL"

# Custom output directory and task count
uv run structured-handoff/scripts/generate_handoff.py --task "Add OAuth2 support" --dir ".agent-tasks" --num-tasks 8

# Minimal — just 2 tasks
uv run structured-handoff/scripts/generate_handoff.py --task "Fix pagination bug in /api/users" --num-tasks 2
```

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r structured-handoff/ ~/.config/cognition/skills/structured-handoff/
# or: cp -r structured-handoff/ ~/.windsurf/skills/structured-handoff/

# Project-specific
cp -r structured-handoff/ /path/to/project/.cognition/skills/structured-handoff/
# or: cp -r structured-handoff/ /path/to/project/.windsurf/skills/structured-handoff/
```

Then invoke with `/structured-handoff` in a session.
