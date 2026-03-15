---
name: youtube-search
description: Search YouTube for technical videos, tutorials, and talks on a topic
argument-hint: "<topic>"
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

# YouTube Search

Find the best YouTube videos, tutorials, conference talks, and technical content for a given topic. Results are ranked by technical relevance — longer, tutorial-style, deep-dive content surfaces first.

## Step 1 — Search

Run the search script with the user's topic:

```
uv run youtube-search/scripts/search_youtube.py $ARGUMENTS
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--max-results N` | Maximum results (default: 10) |
| `-r`, `--region CODE` | Region code, e.g. `us-en`, `wt-wt` (default: `wt-wt`) |
| `-t`, `--time {d,w,m,y}` | Time range: day, week, month, year |
| `--json` | Output as JSON |
| `--scores` | Show technical relevance scores |

## Step 2 — Present results

Review the results and present them to the user as a curated list:

1. **Highlight the top picks** — call out the 2-3 most relevant videos with a sentence on why each is worth watching (e.g. "full 2-hour course", "conference talk from the library author", "step-by-step build from scratch").
2. **List the rest** — show remaining results with title, channel, duration, and URL.
3. **Suggest next steps** — if the user wants to go deeper into a specific video, recommend using the `youtube-wisdom` skill to fetch and analyze its transcript.

### Tailoring the search

- For **broad topics** (e.g. "Kubernetes"), add qualifiers: `uv run youtube-search/scripts/search_youtube.py "Kubernetes" -n 15`
- For **recent content**, use time filters: `-t w` for past week, `-t m` for past month
- If results seem weak, try **rephrasing** — e.g. "React server components deep dive" instead of just "React".

## Step 3 — Deep dive (optional)

If the user asks to learn more about a specific video from the results, use the `youtube-wisdom` skill:

```
uv run youtube-wisdom/scripts/fetch_transcript.py "<video-url>"
```

Then analyze the transcript to extract key insights, actionable takeaways, and notable quotes.

## Error handling

- If no results are found, try broadening the query or removing overly specific terms.
- If the script fails, retry once. If it still fails, report the error to the user.
- The search uses DuckDuckGo — no API key needed.

User arguments: $ARGUMENTS
