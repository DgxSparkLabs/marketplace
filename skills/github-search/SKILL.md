---
name: github-search
description: Search GitHub for repositories, prior art, and implementation inspiration
argument-hint: "<query>"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
    - Exec(gh)
    - Write(agent-fetched/**)
triggers:
  - user
  - model
---

# GitHub Search

Search GitHub for existing projects, libraries, and implementations relevant to the task at hand. Use this before building something from scratch — there's almost always prior art worth learning from.

## Usage

```
uv run $SKILL_DIR/scripts/search.py <query> [options]
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

### Prerequisites

The `gh` CLI must be installed and authenticated (`gh auth login`).

## Output files

Results are automatically saved to `agent-fetched/github-search/` relative to the current working directory. Files are named `<timestamp>_<query>.txt` (or `.json` with `--json`).

- **Large results (>500 chars):** Only the file path and size are printed to stdout. Use `read` to view the file.
- **Small results (<=500 chars):** Content is printed to stdout normally.

## Instructions

### When to use this skill

Invoke this skill **before implementing any non-trivial feature**. If you're about to write something that might already exist — a parser, a protocol handler, a CLI tool, a data pipeline — search GitHub first. Prior art saves time and often reveals edge cases you wouldn't have thought of.

### Step 1: Search wide

Run the search with the core concept you're about to implement. Frame the query around **what it does**, not what you're building:

```
uv run $SKILL_DIR/scripts/search.py "websocket server framework" -l python
```

If results are sparse, try:
- Broader terms (e.g. "websocket" instead of "websocket server framework")
- Removing the language filter
- Sorting by `best-match` instead of `stars`
- Searching for the underlying technique (e.g. "raft consensus" instead of "distributed database")

### Step 2: Triage — pick which repos to explore

You now have up to 20 results with names, descriptions, stars, languages, and topics. **Do not read all 20.** Select **3-6 repos** to actually explore, based on these criteria (in priority order):

1. **Stars + activity signal quality.** A repo with 5k+ stars and recent updates is battle-tested. But don't ignore small gems — a 50-star repo with a perfect description match can be more useful than a 10k-star kitchen sink.
2. **Description relevance.** The description should match your actual problem, not just share keywords. A "minimal websocket library" is more useful than a "full-stack web framework" when you need websockets.
3. **Language match.** Prefer repos in the same language as your project. Cross-language repos are still useful for understanding algorithms and architecture, but prioritize same-language for actual code patterns.
4. **Recency.** Prefer repos updated in the last year. Abandoned repos may have outdated patterns, broken deps, or security issues. Check the "updated" field.
5. **Scope fit.** Prefer focused libraries/tools over monorepos or frameworks. A single-purpose repo is easier to learn from than digging through a massive project.
6. **License compatibility.** Note the license. MIT/Apache/BSD are safe to draw inspiration from. GPL/AGPL may have implications. No license means all rights reserved.

### Step 3: Explore selected repos

For each selected repo, use `gh` and the web scraper to understand it:

```bash
# Read the README (fastest way to understand what it does)
gh repo view <owner>/<repo>

# Browse the file structure
gh api repos/<owner>/<repo>/git/trees/HEAD --jq '.tree[].path'

# Read specific source files
gh api repos/<owner>/<repo>/contents/<path> --jq '.content' | base64 -d
```

Explore in parallel when possible. Focus on:
- **README** — what problem does it solve, how is it architected
- **Entry point / main module** — how is the core logic structured
- **Tests** — what edge cases do they handle
- **Issues** — what problems have users hit (these are the gotchas you'll face too)

### Step 4: Synthesize findings

Present what you found to inform the implementation:

- **What exists** — list the most relevant repos with one-line summaries
- **Key patterns** — common architectural approaches across projects (e.g. "all 4 repos use an event loop with a queue-based dispatcher")
- **Reusable code** — specific libraries or modules worth depending on directly instead of reimplementing
- **Gotchas** — common issues from READMEs and issue trackers
- **Recommendation** — whether to use an existing library, fork one, or build from scratch (and why)

### Error handling

- If `gh` is not installed or not authenticated, tell the user to run `gh auth login`.
- If the search returns no results, broaden the query or try different keywords.
- If a repo's README can't be fetched, note it and move on.

User arguments: $ARGUMENTS
