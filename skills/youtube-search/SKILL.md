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

Find the best YouTube videos on a topic — tutorials, conference talks, deep dives, courses. The script pre-ranks results by technical relevance, but **you must still triage** before presenting.

## Usage

```
uv run youtube-search/scripts/search_youtube.py <query> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--max-results N` | Maximum results (default: 15) |
| `-r`, `--region CODE` | Region code, e.g. `us-en`, `wt-wt` (default: `wt-wt`) |
| `-t`, `--time {d,w,m,y}` | Time range: day, week, month, year |
| `--json` | Output as JSON |
| `--scores` | Show technical relevance scores (useful for debugging) |

## Instructions

### Step 1: Search wide

Run the search with the user's topic:

```
uv run youtube-search/scripts/search_youtube.py <query>
```

### Step 2: Triage — pick which videos to recommend

You now have up to 15 titles, channels, durations, and descriptions. **Do not just dump all 15.** Read them carefully and select **3-7 videos** to actually recommend based on these preferences (in priority order):

1. **Creator authority over production value.** Prefer videos from the library/framework author, a core contributor, a conference speaker who built the thing, or a respected educator. A low-production talk by the actual creator beats a polished video from a content mill.
2. **Technical depth over surface coverage.** A 45-min deep dive with code walkthrough beats a 5-min "Top 10 things about X". Look for signals like "deep dive", "internals", "from scratch", "implementation", "under the hood", "live coding" in titles and descriptions.
3. **Duration as signal.** Conference talks (30-60 min) and full courses (1+ hr) are usually high substance. Tutorials in the 10-30 min range are solid for focused topics. Videos under 5 min rarely have depth — skip them unless they're from an exceptional source (e.g. Fireship, 3Blue1Brown).
4. **Channel diversity.** Pick videos from different creators and perspectives. Don't recommend 4 videos from the same channel. Mix conference talks, independent tutorials, official channels, and community educators.
5. **Recency vs fundamentals.** For fast-moving topics (frameworks, AI, cloud), prefer recent content. For fundamentals (algorithms, OS internals, networking), older videos from great educators are often better than recent rehashes.
6. **Specificity to the query.** Match the video type to what the user needs. "How to build X" → hands-on tutorials. "What is X" → explainer/overview. "X best practices" → conference talks. "X vs Y" → comparison deep dives or benchmarks.
7. **Skip low-signal videos.** Skip results that are clearly clickbait, reaction/commentary videos, shorts compilations, or videos where the description is all affiliate links and no substance.

### Step 3: Present curated results

For each selected video, present:

- **Title** and **URL**
- **Why it's worth watching** — one sentence explaining what makes this pick valuable (e.g. "conference talk by the library author", "full 2-hour project build from scratch", "best visual explanation of the concept")
- **Duration** and **channel** for context

Group them: lead with the top 2-3 picks (with brief reasoning), then list the rest.

### Step 4: Deep dive (if the user wants to go deeper)

If the user asks to learn from a specific video, use the `youtube-wisdom` skill to fetch and analyze its transcript (requires the **youtube-wisdom** skill to be installed):

```
uv run youtube-wisdom/scripts/fetch_transcript.py "<video-url>"
```

Then extract: core thesis, key technical points, actionable takeaways, and notable quotes.

### Tailoring the search

- For **broad topics** (e.g. "Kubernetes"), add qualifiers to the query itself: "Kubernetes networking internals" or "Kubernetes production setup"
- For **recent content**, use time filters: `-t w` for past week, `-t m` for past month
- For **channel-specific searches**, just use the channel name as the query: "Fireship" or "0xSero"
- If results seem weak, try **rephrasing** — "React server components deep dive" instead of just "React"
- Run **multiple searches** with different angles if the first set doesn't fully cover the topic

### Error handling

- If the search returns no results, try rephrasing the query or broadening the terms.
- If the script fails, retry once. If it still fails, report the error to the user.
- The search uses DuckDuckGo — no API key needed.

User arguments: $ARGUMENTS
