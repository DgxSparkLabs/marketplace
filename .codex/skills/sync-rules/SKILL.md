---
name: sync-rules
description: Sync rules from global AI agent configs into the workspace
argument-hint: "[format]"
allowed-tools:
  - exec
  - Bash
  - read
  - Read
  - edit
  - Edit
  - glob
  - Glob
  - grep
  - Grep
permissions:
  allow:
    - Exec(uv run)
    - Read(**)
triggers:
  - user
  - model
---

# Sync Rules

Import rules from your global AI agent configurations into the current project.

Different AI agents store rules in different places — Devin uses `~/.config/devin/AGENTS.md`, Claude Code uses `~/.claude/CLAUDE.md`, Cursor and Windsurf keep separate files in `~/.cursor/rules/` and `~/.windsurf/rules/`. Over time you accumulate useful rules in these global configs, but they don't automatically carry over to new projects or to agents that lack global rule support. This skill bridges that gap: it scans all your global configs, deduplicates identical rules that appear in multiple agents, and writes the merged set into your workspace.

## The sync script

The script handles scanning, deduplication, conflict detection, and writing in one step:

```
uv run $SKILL_DIR/scripts/sync_rules.py                     # dry run — show what would sync
uv run $SKILL_DIR/scripts/sync_rules.py --write agents       # write to AGENTS.md
uv run $SKILL_DIR/scripts/sync_rules.py --write cursor       # write to .cursor/rules/
uv run $SKILL_DIR/scripts/sync_rules.py --write windsurf     # write to .windsurf/rules/
uv run $SKILL_DIR/scripts/sync_rules.py --write all          # all formats at once
uv run $SKILL_DIR/scripts/sync_rules.py --agent devin        # only scan Devin globals
uv run $SKILL_DIR/scripts/sync_rules.py --json               # structured output
```

### What the script does

1. **Scans** global configs for all installed agents (Devin, Claude Code, Cursor, Windsurf)
2. **Deduplicates** — if the same rule exists in multiple agents (e.g., "Blast Radius" in both Devin and Cursor), it keeps the longest version and tracks all sources
3. **Compares** against rules already in the workspace to find conflicts
4. **Writes** new rules into the chosen format, skipping rules that already exist in the workspace

Deduplication uses content similarity (not just name matching) so it catches rules that were slightly reformatted across agents.

### Options

- `--agent <name>` — filter to specific agents (repeatable: `--agent devin --agent cursor`)
- `--write <format>` — write rules to workspace (`agents`, `cursor`, `windsurf`, `all`). Without this flag, just prints what it found (dry run).
- `--workspace <path>` — target a different directory (default: current directory)
- `--include-conflicts` — also overwrite rules that already exist in workspace
- `--json` — output structured JSON instead of human-readable text

## Workflow

### Step 1: Dry run

Start with a dry run so the user sees what's available before anything changes:

```
uv run $SKILL_DIR/scripts/sync_rules.py
```

Show the user the output. It lists new rules (not yet in workspace) and rules that already exist. If rules were deduplicated across agents, it notes that too.

### Step 2: Confirm and write

Ask the user which format to write to. Suggest `agents` (AGENTS.md) as the default since it works with Devin and Claude Code. If the workspace already has `.cursor/rules/` or `.windsurf/rules/` directories, suggest `all` instead.

Then run with `--write`:

```
uv run $SKILL_DIR/scripts/sync_rules.py --write agents
```

### Step 3: Handle conflicts

If the user wants to overwrite existing rules, re-run with `--include-conflicts`. But warn them first — their workspace rules may have been customized for this project. Show them the diff between the global and workspace versions of any conflicting rule before proceeding.

### Output formats

**AGENTS.md**: Rules are appended as `## Heading` sections — works with Devin and Claude Code.

**Cursor**: Each rule becomes a separate `.cursor/rules/<slug>.md` file with frontmatter:
```yaml
---
description: "Short description"
alwaysApply: true
---
```

**Windsurf**: Each rule becomes a separate `.windsurf/rules/<slug>.md` file with frontmatter:
```yaml
---
trigger: always_on
description: "Short description"
---
```

User arguments: $ARGUMENTS
