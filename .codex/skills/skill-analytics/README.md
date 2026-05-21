# skill-analytics

Analyze your installed skills' usage patterns and generate an interactive HTML dashboard.

## Setup

No setup required. The script reads directly from the Devin CLI sessions database.

**Prerequisites:**
- `uv` installed
- Devin CLI sessions database at `~/.local/share/devin/cli/sessions.db`

## Usage

The script is self-contained with inline dependencies (PEP 723). No install step needed:

```bash
uv run skill-analytics/scripts/generate_dashboard.py
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--output PATH` | No | Where to write the HTML file (default: `./skill_audit.html`) |
| `--db PATH` | No | Path to sessions database (default: `~/.local/share/devin/cli/sessions.db`) |
| `--skills-dir PATH` | No | Path to installed skills directory (default: `~/.config/devin/skills`) |
| `--window N` | No | Rolling window size in sessions (default: 10) |
| `--json` | No | Output raw analysis data as JSON instead of HTML |

### Examples

```bash
# Generate dashboard (default location)
uv run skill-analytics/scripts/generate_dashboard.py

# Custom output path
uv run skill-analytics/scripts/generate_dashboard.py --output /tmp/my_skills.html

# Analyze a sessions.db from another machine
uv run skill-analytics/scripts/generate_dashboard.py --db /path/to/sessions.db

# Analyze a foreign DB with its matching skills directory
uv run skill-analytics/scripts/generate_dashboard.py --db /path/to/sessions.db --skills-dir /path/to/skills/

# Get raw JSON data for scripting
uv run skill-analytics/scripts/generate_dashboard.py --json > skill_data.json

# Use a 20-session rolling window
uv run skill-analytics/scripts/generate_dashboard.py --window 20
```

## What the Dashboard Shows

- **Usage Funnel** — how many skills go from "installed" to "consistently used"
- **Session Spread vs Invocations** — which skills are broadly useful vs one-off
- **Timeline** — when skills were used across your session history
- **Rolling Usage Rate** — sustained adoption over a sliding window
- **Installed Skills Table** — every skill with size, session count, and invocations
- **Context Budget** — how much system prompt space your skills consume

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r skill-analytics/ ~/.config/devin/skills/skill-analytics/

# Project-specific
cp -r skill-analytics/ /path/to/project/.devin/skills/skill-analytics/
```

Then ask your agent: "analyze my skill usage" or "which skills should I remove?"
