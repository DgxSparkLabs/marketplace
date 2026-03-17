# youtube-search

Search YouTube for technical videos, tutorials, conference talks, and educational content on any topic. Results are ranked by technical relevance — longer, tutorial-style, deep-dive content is prioritized over shorts and entertainment.

## How it works

Uses DuckDuckGo's video search (scoped to YouTube) to find videos, then ranks them with a technical relevance heuristic that considers:

- **Content signals** — titles/descriptions mentioning "tutorial", "deep dive", "from scratch", "conference talk", etc. score higher
- **Duration** — longer videos (10+ min) are preferred; shorts are penalized
- **Negative signals** — reaction videos, vlogs, memes, etc. are deprioritized

Falls back to DuckDuckGo text search (`site:youtube.com`) if video search returns sparse results.

## Setup

No setup needed — uses DuckDuckGo's public API. No API key required.

## Usage

```bash
# Search for videos on a topic
uv run youtube-search/scripts/search_youtube.py "async Python"

# Limit to 5 results
uv run youtube-search/scripts/search_youtube.py "Rust ownership" -n 5

# Only recent videos (past month)
uv run youtube-search/scripts/search_youtube.py "LLM agents" -t m

# JSON output
uv run youtube-search/scripts/search_youtube.py "system design" --json

# Show relevance scores
uv run youtube-search/scripts/search_youtube.py "WebAssembly" --scores
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--max-results N` | Maximum number of results (default: 15) |
| `-r`, `--region CODE` | Region code, e.g. `us-en`, `uk-en`, `wt-wt` for global (default: `wt-wt`) |
| `-t`, `--time {d,w,m,y}` | Time range: `d`=day, `w`=week, `m`=month, `y`=year |
| `--json` | Output results as JSON |
| `--scores` | Show technical relevance scores |

## Pairs well with

- **youtube-wisdom** — once you find a promising video, use youtube-wisdom to fetch and analyze its transcript
- **duckduckgo-search** — for broader web searches beyond YouTube

## As an Agent Skill

Install into Devin or any compatible agent:

```bash
devin skills install youtube-search
```

Once installed, the agent can invoke it via `/youtube-search <topic>` or autonomously when it needs to find tutorial content.
