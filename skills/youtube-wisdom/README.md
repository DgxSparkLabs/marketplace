# youtube-wisdom

Extract structured knowledge from YouTube videos — key points, insights, actionable takeaways, and conclusions.

Fetches the transcript (no API key needed) and analyzes it as a knowledge source, not a summary.

## Setup

Install [uv](https://docs.astral.sh/uv/) if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

No API keys required. Transcripts are fetched directly from YouTube.

## Usage

### As a script

```bash
# Fetch transcript only
uv run youtube-wisdom/scripts/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Preferred language
uv run youtube-wisdom/scripts/fetch_transcript.py "https://youtu.be/VIDEO_ID" --lang en

# JSON output
uv run youtube-wisdom/scripts/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --json
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `url` | Yes | YouTube URL or video ID |
| `--lang` | No | Preferred transcript language code (e.g. `en`, `es`) |
| `--json` | No | Output as JSON instead of timestamped text |

### As an agent skill

```bash
# Global
cp -r youtube-wisdom/ ~/.config/cognition/skills/youtube-wisdom/
# or: cp -r youtube-wisdom/ ~/.windsurf/skills/youtube-wisdom/

# Project-specific
cp -r youtube-wisdom/ .cognition/skills/youtube-wisdom/
```

Then invoke with:

```
/youtube-wisdom https://www.youtube.com/watch?v=VIDEO_ID
```

The agent will fetch the transcript and produce structured knowledge extraction: core thesis, key points with timestamps, insights, actionable takeaways, conclusions, and notable quotes.

## Limitations

- Only works with videos that have captions/transcripts (most do)
- Auto-generated captions may have transcription errors
- Very long videos produce large transcripts
