---
name: web-scraper
description: Fetch a web page and extract its main content as clean readable text
argument-hint: "<url>"
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

# Web Scraper

Fetch a web page and return its main content, stripped of navigation, ads, scripts, and boilerplate.

## Step 1: Fetch and extract

```
uv run $SKILL_DIR/scripts/scrape.py "$1"
```

### Options

- `--links` — preserve hyperlinks in the output
- `--images` — include image references
- `--no-tables` — exclude tables
- `--language en` — filter to a specific language
- `--json` — output structured JSON instead of plain text

For multiple URLs, run the command once per URL.

## Output files

Scraped content is automatically saved to `agent-fetched/web-scraper/` relative to the current working directory. Files are named `<timestamp>_<url-slug>.txt` (or `.json` with `--json`).

- **Large results (>500 chars):** Only the file path and size are printed to stdout. Use `read` to view the file.
- **Small results (<=500 chars):** Content is printed to stdout normally.

## Step 2: Present the content

Based on what the user asked for:

- **"Summarize this page"** — read the extracted content and provide a concise summary.
- **"What does this page say about X?"** — find and quote the relevant sections.
- **"Extract all links"** — re-run with `--links --json` and list them.
- **"Compare these pages"** — scrape each URL, then compare the content side by side.
- If the user just gave a URL with no instruction, present the title, metadata, and a brief summary, then ask what they'd like to know.

## Reddit support

Reddit URLs are handled specially — the script parses old.reddit.com HTML directly:

- **Listing pages** (subreddit, front page, /top, /hot, etc.) return a numbered list of posts with scores, comment counts, authors, and URLs.
- **Post pages** (/r/.../comments/...) return the post title, selftext or link URL, and all comments with author and body text.

This works without Reddit API credentials.

## Error handling

- If the script says "Failed to fetch", the URL may be behind authentication, geo-blocked, or down. Tell the user.
- If "No extractable content found", the page may be a SPA that requires JavaScript rendering. Explain this to the user — trafilatura works on static/server-rendered HTML.
- For paywalled sites, the extraction will typically get whatever content is visible without login.

## Guidelines

- Do not dump the entire extracted text to the user unless they ask for it. Summarize or answer their question.
- If the content is very long (>5000 words), summarize it section by section.
- Preserve the original structure (headings, lists) when presenting content.
- If the page is in a language the user didn't request, mention this.

User arguments: $ARGUMENTS
