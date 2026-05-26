# sync-rules

Import rules from global AI agent configurations (Devin, Claude Code, Cursor, Windsurf) into the current workspace — deduplicated and merged across agents.

## Why

You accumulate rules across multiple agents over time. When you start a new project, or want a specific project to follow the same conventions, you need a way to pull those rules in without manually copying and reformatting. This skill scans all your global configs, deduplicates rules that appear in multiple agents (even if slightly reformatted), and writes the merged set into whatever workspace format you need.

## Setup

No API keys or services needed. Just `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage

### Dry run (see what's available)

```bash
uv run sync-rules/scripts/sync_rules.py
```

### Write to workspace

```bash
uv run sync-rules/scripts/sync_rules.py --write agents     # AGENTS.md
uv run sync-rules/scripts/sync_rules.py --write cursor      # .cursor/rules/
uv run sync-rules/scripts/sync_rules.py --write windsurf    # .windsurf/rules/
uv run sync-rules/scripts/sync_rules.py --write all         # all formats
```

### Filter by source agent

```bash
uv run sync-rules/scripts/sync_rules.py --agent devin
uv run sync-rules/scripts/sync_rules.py --agent cursor --agent windsurf
```

### As an Agent Skill

```
/sync-rules              # scan and sync all
/sync-rules agents       # sync to AGENTS.md
/sync-rules cursor       # sync to .cursor/rules/
```

## Global Config Locations

| Agent | Path | Format |
|-------|------|--------|
| Devin CLI | `~/.config/devin/AGENTS.md` | Markdown sections |
| Claude Code | `~/.claude/CLAUDE.md` | Markdown sections |
| Cursor | `~/.cursor/rules/*.md` | Files with YAML frontmatter |
| Windsurf | `~/.windsurf/rules/*.md` | Files with YAML frontmatter |

## How Deduplication Works

Rules are compared by content similarity, not just name. If you have "Blast Radius" in Devin's global config and a slightly different version in Cursor's, the script recognizes them as the same rule. It keeps the longest version and tracks all sources so you know where it came from.
