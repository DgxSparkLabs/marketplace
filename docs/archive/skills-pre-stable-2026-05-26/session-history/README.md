# session-history

Query past Devin CLI conversations from the local session database. Search for topics, list sessions, read full conversations, and review prompt history.

## Setup

No external dependencies or API keys needed. The skill reads the local Devin CLI database at `~/.local/share/devin/cli/sessions.db`.

Requires:
- `uv` installed

## Usage

The script is self-contained with inline dependencies (PEP 723). No install step needed:

```bash
uv run session-history/scripts/query_sessions.py <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `list` | List recent sessions (most recent first) |
| `search <query>` | Full-text search across all user and assistant messages |
| `read <session-id>` | Read a full conversation (supports partial ID prefix) |
| `stats` | Show database statistics (sessions, messages, models) |
| `prompts [query]` | List recent user prompts, optionally filtered |

### Options

| Flag | Applies to | Description |
|------|-----------|-------------|
| `--json` | All | Output as JSON |
| `-n`, `--limit` | list, search, prompts | Max results to return |
| `--role user\|assistant` | search | Filter search by role |
| `--max-length N` | read | Max characters per message (default: 2000) |
| `--db PATH` | All | Custom database path |

### Examples

```bash
# List last 10 sessions
uv run session-history/scripts/query_sessions.py list -n 10

# Search for discussions about terraform
uv run session-history/scripts/query_sessions.py search "terraform"

# Search only in user messages
uv run session-history/scripts/query_sessions.py search "API key" --role user

# Read a specific session (partial ID works)
uv run session-history/scripts/query_sessions.py read 44571c7b

# Show stats about the knowledge base
uv run session-history/scripts/query_sessions.py stats

# List recent prompts matching a keyword
uv run session-history/scripts/query_sessions.py prompts "docker" -n 10

# JSON output for piping
uv run session-history/scripts/query_sessions.py --json search "deploy"
```

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r session-history/ ~/.config/devin/skills/session-history/

# Project-specific
cp -r session-history/ /path/to/project/.devin/skills/session-history/
```

Then invoke with `/session-history` in a session, or the agent can use it autonomously when past context is needed.
