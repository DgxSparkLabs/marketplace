---
name: youtube-wisdom
description: Extract key knowledge from a YouTube video transcript
argument-hint: "<youtube-url>"
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

# YouTube Wisdom

Extract structured knowledge from a YouTube video.

## Step 1: Fetch the transcript

```
uv run $SKILL_DIR/scripts/fetch_transcript.py "$1"
```

If that fails, try with `--lang en`. If transcripts are disabled or unavailable, tell the user.

## Output files

Transcripts are automatically saved to `agent-fetched/youtube-wisdom/` relative to the current working directory. Files are named `<timestamp>_<video-id>.txt` (or `.json` with `--json`).

- **Large results (>500 chars):** Only the file path and size are printed to stdout. Use `read` to view the file.
- **Small results (<=500 chars):** Content is printed to stdout normally.

## Step 2: Analyze

Read the full transcript carefully. This is not entertainment — treat it as a knowledge source. Extract the following:

### Output format

**Title:** (video title)

**Core thesis:** One sentence — what is the speaker's central argument or message?

**Key points:**
- Numbered list of the main ideas presented, in the order they appear. Each point should be a complete thought, not a fragment. Include the timestamp where the point is made.

**Insights:**
- Ideas that are novel, non-obvious, or challenge conventional thinking. These are the things someone would miss by skimming.

**Actionable takeaways:**
- Concrete things the viewer can do, apply, or change based on this content. Be specific.

**Conclusions:**
- How the speaker wraps up. What final position do they land on?

**Notable quotes:**
- Direct quotes that capture key ideas concisely. Include timestamps.

## Guidelines

- Do not pad with filler. If a section has nothing meaningful, omit it.
- Prefer the speaker's own language and framing over paraphrasing.
- If the video is a tutorial or how-to, focus the takeaways on the specific steps and techniques.
- If the video is a debate or interview, capture both sides.
- If the video is a lecture, emphasize the conceptual framework and key definitions.
- For long videos, group key points by topic or section if there's a natural structure.

User arguments: $ARGUMENTS
