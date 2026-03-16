# motivation

Encourage the agent to keep working instead of stopping prematurely. Pulls real quotes from past session history where the user pushed for continuation, autonomy, and persistence.

## Setup

No external dependencies or API keys needed. The script reads the local Devin CLI session database at `~/.local/share/cognition/cli/sessions.db` for live quotes, with a curated fallback set.

Requires:
- `uv` installed

## Usage

```bash
uv run motivation/scripts/motivate.py
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--json` | No | Output as JSON |

### Examples

```bash
# Get a motivational nudge (human-readable)
uv run motivation/scripts/motivate.py

# Get structured output
uv run motivation/scripts/motivate.py --json
```

### Sample Output

```
============================================================
MOTIVATION CHECK
============================================================

Yorai said: "as long as you have ideas worth while implement it.
as long as there are tasks to be done think about them and implement
them. surely you hadn't yet reached the goal? right?"

  --> The user trusts you to keep going. Don't stop to ask — investigate.

============================================================
Now get back to work.
============================================================
```

## How It Works

1. Queries the Devin CLI session database for real user messages that match motivational patterns (e.g., "continue working", "be autonomous", "have fun", "keep going")
2. Picks a random match as a live quote
3. Falls back to a curated set of 17 real quotes mined from session history if the DB is unavailable
4. Pairs the quote with a random self-talk nudge designed to reframe agent behavior

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r motivation/ ~/.config/cognition/skills/motivation/

# Project-specific
cp -r motivation/ /path/to/project/.cognition/skills/motivation/
```

The skill is both user-triggered (`/motivation`) and model-triggered. The agent can invoke it autonomously whenever it detects it's about to stop prematurely, ask unnecessary permission, or declare "done" with pending tasks.
