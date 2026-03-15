---
name: duckduckgo-search
description: Search DuckDuckGo and return results as structured text
argument-hint: "<query>"
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

# DuckDuckGo Search

Search DuckDuckGo from the command line and return clean, readable results.

## Usage

```
uv run duckduckgo-search/scripts/search.py <query> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--max-results N` | Maximum number of results (default: 5) |
| `-r`, `--region CODE` | Region code, e.g. `us-en`, `uk-en`, `wt-wt` for global (default: `wt-wt`) |
| `-t`, `--time {d,w,m,y}` | Time range: `d`=day, `w`=week, `m`=month, `y`=year |
| `--json` | Output results as JSON |

## Instructions

1. Run the search command with the user's query.
2. Review the results and present a concise summary to the user.
3. If the user asks for more detail on a specific result, use the `web-scraper` skill to fetch the full page content.
4. When the query is ambiguous, prefer broader searches and let the user refine.

### Error handling

- If the search returns no results, try rephrasing the query or broadening the terms.
- If the script fails, check network connectivity and retry once before reporting the error.

User arguments: $ARGUMENTS
