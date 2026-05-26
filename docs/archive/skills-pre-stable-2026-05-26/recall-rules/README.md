# recall-rules

Re-read global rules and thinking framework to realign mid-session. Loads all agent rules files from global and project-level locations.

## Setup

No external dependencies or API keys needed.

## Usage

```
/recall-rules
```

The skill scans for rules files across all supported agent platforms (Devin CLI, Claude Code, Cursor, Windsurf) and reads them into context.

### What It Reads

| Location | Platform |
|----------|----------|
| `~/.config/devin/AGENTS.md` | Devin CLI (global) |
| `~/.config/devin/CRAFT.md` | Devin CLI (thinking framework) |
| `~/.claude/CLAUDE.md` | Claude Code (global) |
| `AGENTS.md` / `CLAUDE.md` | Project-level |
| `.cursor/rules/*.md` | Cursor (project) |
| `.windsurf/rules/*.md` | Windsurf (project) |

### When to Use

- **Session start** — load operating instructions before doing anything
- **Mid-session drift** — when work quality drops or you're cutting corners
- **Project switch** — when moving between projects in the same session
- **User prompt** — when the user says "slow down", "check yourself", or similar

## As an Agent Skill

```bash
cp -r recall-rules/ ~/.config/devin/skills/recall-rules/
```

The skill is both user-triggered (`/recall-rules`) and model-triggered. The agent can invoke it autonomously when it detects it may be drifting from established rules.
