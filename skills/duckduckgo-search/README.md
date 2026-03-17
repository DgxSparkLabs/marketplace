# duckduckgo-search

Search DuckDuckGo from the command line and get clean, readable results. No API key required.

## Setup

No setup needed — the script uses DuckDuckGo's public search API.

## Usage

```bash
uv run duckduckgo-search/scripts/search.py "your search query"
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--max-results N` | Maximum number of results (default: 20) |
| `-r`, `--region CODE` | Region code, e.g. `us-en`, `uk-en`, `wt-wt` for global (default: `wt-wt`) |
| `-t`, `--time {d,w,m,y}` | Time range: `d`=day, `w`=week, `m`=month, `y`=year |
| `--json` | Output results as JSON |

### Examples

```bash
# Basic search
uv run duckduckgo-search/scripts/search.py "python asyncio tutorial"

# Top 10 results from the past week
uv run duckduckgo-search/scripts/search.py "rust vs go performance" -n 10 -t w

# JSON output
uv run duckduckgo-search/scripts/search.py "best static site generators" --json

# Region-specific search
uv run duckduckgo-search/scripts/search.py "local news" -r uk-en
```

## As an Agent Skill

Install into Devin or any compatible agent:

```bash
devin skills install duckduckgo-search
```

Once installed, the agent can invoke it via the `/duckduckgo-search` command or autonomously when it needs to search the web.
