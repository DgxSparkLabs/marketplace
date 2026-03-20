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
    - Write(agent-fetched/**)
triggers:
  - user
  - model
---

# DuckDuckGo Search

Search DuckDuckGo from the command line and return clean, readable results.

## Prerequisites

The **web-scraper** skill must be installed alongside this skill (used in Step 3 to fetch full page content from search results).

## Usage

```
uv run $SKILL_DIR/scripts/search.py <query> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--max-results N` | Maximum number of results (default: 20) |
| `-r`, `--region CODE` | Region code, e.g. `us-en`, `uk-en`, `wt-wt` for global (default: `wt-wt`) |
| `-t`, `--time {d,w,m,y}` | Time range: `d`=day, `w`=week, `m`=month, `y`=year |
| `--json` | Output results as JSON |

## Output files

Results are automatically saved to `agent-fetched/duckduckgo-search/` relative to the current working directory. Files are named `<timestamp>_<query>.txt` (or `.json` with `--json`).

- **Large results (>500 chars):** Only the file path and size are printed to stdout. Use `read` to view the file.
- **Small results (<=500 chars):** Content is printed to stdout normally.

## Instructions

### Step 1: Search wide

Run the search with `-n 20` to get a broad set of results:

```
uv run $SKILL_DIR/scripts/search.py <query> -n 20
```

### Step 2: Triage — pick which results to scrape

You now have 20 titles, URLs, and snippets. **Do not scrape all 20.** Read the titles and snippets carefully and select **3-7 results** to actually scrape based on these preferences (in priority order):

1. **Primary sources over aggregators.** Prefer official docs, original blog posts, research papers, and manufacturer pages over SEO content farms, listicles, or news aggregators that just summarize other sources.
2. **Technical depth over marketing.** A benchmark review with actual numbers beats a press release or product announcement. Look for words like "review", "benchmark", "tested", "measured", "hands-on", "in-depth" in titles.
3. **Source diversity.** Pick results from different domains and perspectives. Don't scrape 4 articles from the same site. Mix independent reviewers, official sources, community forums, and technical blogs.
4. **Recency.** When multiple results cover the same ground, prefer the most recent one — it likely incorporates earlier findings. Check dates in snippets.
5. **Specificity to the query.** If the user asked about performance, prioritize benchmark articles. If they asked "what is X", prioritize overviews and official pages. Match the source type to the user's intent.
6. **Skip low-signal pages.** Skip results that are clearly paywalled, login-walled, video-only (YouTube), pure forums with no structured answer, or link aggregators (e.g. HackerNews, Reddit listing pages with no real content in the snippet).

### Step 3: Scrape selected results

Use the `web-scraper` skill to fetch the full content of each selected result. **Scrape all selected pages in parallel** — do not scrape them one at a time.

```
uv run $SKILL_DIR/../web-scraper/scripts/scrape.py "<url>"
```

### Step 4: Synthesize

Read all scraped content and produce a thorough answer:

- Lead with a direct answer to the user's question.
- Support claims with specifics from the sources (numbers, quotes, dates).
- Cite sources inline so the user knows where information comes from.
- Note any contradictions or disagreements between sources.
- If the scraped content doesn't fully answer the question, say what's missing.

### Error handling

- If the search returns no results, try rephrasing the query or broadening the terms.
- If the script fails, check network connectivity and retry once before reporting the error.
- If a scrape fails (paywall, blocking), skip it and note which source was inaccessible.
- When the query is ambiguous, prefer broader searches and let the user refine.

User arguments: $ARGUMENTS
