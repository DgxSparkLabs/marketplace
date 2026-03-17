# github-search

Search GitHub for repositories, prior art, and implementation inspiration before building from scratch. Requires the `gh` CLI.

## Setup

Install and authenticate the GitHub CLI:

```bash
# Install (if not already)
# See https://cli.github.com/

# Authenticate
gh auth login
```

## Usage

```bash
uv run github-search/scripts/search.py "your search query"
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--limit N` | Maximum number of results (default: 20) |
| `-l`, `--language LANG` | Filter by language (e.g. `python`, `rust`, `go`) |
| `-s`, `--sort ORDER` | Sort by: `stars`, `forks`, `updated`, `best-match` (default: `stars`) |
| `--min-stars N` | Minimum star count (default: 0) |
| `--topic TOPIC` | Filter by repository topic |
| `--json` | Output results as JSON |

### Examples

```bash
# Find Python websocket libraries
uv run github-search/scripts/search.py "websocket server" -l python

# Popular Rust CLI tools for inspiration
uv run github-search/scripts/search.py "command line tool" -l rust --min-stars 1000

# Recently updated Go HTTP frameworks
uv run github-search/scripts/search.py "http framework" -l go -s updated

# Search by topic
uv run github-search/scripts/search.py "state machine" --topic finite-automata

# JSON output for scripting
uv run github-search/scripts/search.py "markdown parser" --json
```

## As an Agent Skill

Install into Devin or any compatible agent:

```bash
cp -r github-search ~/.config/cognition/skills/github-search
```

Once installed, the agent can invoke it via `/github-search` or autonomously before implementing non-trivial features to find prior art and inspiration.
