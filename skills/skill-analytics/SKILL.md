---
name: skill-analytics
description: "Analyze skill usage patterns and generate an interactive HTML dashboard"
argument-hint: "[--output path]"
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

# Skill Analytics

Generate an interactive HTML dashboard showing how your installed skills are actually being used — which ones get invoked, how often, in how many sessions, and where the context budget goes.

## Prerequisites

- **uv** installed
- A Devin CLI sessions database (`sessions.db`). Default location: `~/.local/share/devin/cli/sessions.db`

## Usage

```
uv run $SKILL_DIR/scripts/generate_dashboard.py [options]
```

### Options

- `--output PATH` — where to write the HTML file (default: `./skill_audit.html`)
- `--db PATH` — path to sessions database (default: `~/.local/share/devin/cli/sessions.db`)
- `--skills-dir PATH` — path to installed skills directory (default: `~/.config/devin/skills`)
- `--window N` — rolling window size in sessions (default: 10)
- `--json` — output raw analysis data as JSON instead of HTML

## Instructions

When the user asks about skill usage, skill health, which skills to keep or remove, or wants a dashboard of their skill statistics:

1. Run the dashboard generator:
   ```
   uv run $SKILL_DIR/scripts/generate_dashboard.py --output /tmp/skill_audit.html
   ```

2. Tell the user where the file is and suggest opening it in a browser.

3. If the user wants raw data for further analysis, use `--json`:
   ```
   uv run $SKILL_DIR/scripts/generate_dashboard.py --json > skill_data.json
   ```

4. If the user provides a custom `sessions.db` (e.g. copied from another machine), pass it with `--db`:
   ```
   uv run $SKILL_DIR/scripts/generate_dashboard.py --db /path/to/sessions.db --output /tmp/skill_audit.html
   ```
   When analyzing a foreign database, also pass `--skills-dir` if the skills directory differs from the local default, or omit it to skip installed-skills detection (the dashboard will still show all invoked skills from the DB).

5. Use the data to answer specific questions:
   - "Which skills should I remove?" — look at skills with 0 sessions and 0 invocations
   - "What's my most-used skill?" — sort by session count, not invocation count
   - "How much context am I wasting?" — compare always-on token cost vs usage

### Interpreting the dashboard

The dashboard shows several views:

- **Usage Funnel** — how many skills narrow from "installed" to "consistently used"
- **Sessions vs Invocations** — session spread is a better signal than raw count (a skill used in 7 sessions beats one used 700 times in 1 marathon session)
- **Rolling Usage Rate** — 10-session sliding window; skills below 10% sustained rate are candidates for removal
- **Context Budget** — token cost of always-on skill listings; each unused skill wastes ~30 tokens per session
- **Failure Modes** — why skills go unused (redundant with rules, too niche, or broken/hidden)

User arguments: $ARGUMENTS
