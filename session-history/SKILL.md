---
name: session-history
description: Query past Devin CLI conversations from the local session database
argument-hint: "[search <query>] [list] [read <id>] [stats] [prompts]"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Session History

Query the local Devin CLI session database to recall past conversations,
search for topics discussed, and review what was done in previous sessions.

## Prerequisites

- **uv** installed
- Devin CLI sessions database at `~/.local/share/cognition/cli/sessions.db`

## Usage

### List recent sessions

```
uv run session-history/scripts/query_sessions.py list
uv run session-history/scripts/query_sessions.py list -n 10
```

### Search across all conversations

```
uv run session-history/scripts/query_sessions.py search "terraform"
uv run session-history/scripts/query_sessions.py search "API key" --role user
uv run session-history/scripts/query_sessions.py search "docker" -n 10
```

### Read a full conversation

```
uv run session-history/scripts/query_sessions.py read <session-id>
uv run session-history/scripts/query_sessions.py read <partial-id>
uv run session-history/scripts/query_sessions.py read <id> --max-length 5000
```

### Show database statistics

```
uv run session-history/scripts/query_sessions.py stats
```

### List recent user prompts

```
uv run session-history/scripts/query_sessions.py prompts
uv run session-history/scripts/query_sessions.py prompts "terraform" -n 10
```

### JSON output (all commands)

```
uv run session-history/scripts/query_sessions.py --json search "query"
uv run session-history/scripts/query_sessions.py --json stats
```

## Instructions

When the user asks about past conversations, what was discussed before, or
wants to recall something from a previous session:

1. Start with `search` if the user mentions a topic or keyword
2. Use `list` to show recent sessions if they want an overview
3. Use `read <id>` to pull up a specific conversation (supports partial IDs)
4. Use `prompts` to see what the user has asked across sessions
5. Use `stats` for a quick summary of the knowledge base

When the agent needs context from previous sessions (e.g., "we discussed this
before", "what did we decide about X"), search proactively to find relevant
history.

All commands support `--json` for structured output when piping to other tools.

User arguments: $ARGUMENTS
