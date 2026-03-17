# web-scraper

Fetch any web page and extract its main content as clean, readable text — no HTML noise, no nav bars, no cookie banners.

Uses [trafilatura](https://github.com/adbar/trafilatura) for general content extraction, with custom parsers for Reddit.

## Usage

Invoke as a skill:

```
/web-scraper https://example.com/article
```

Or run the script directly:

```bash
uv run web-scraper/scripts/scrape.py https://example.com/article
uv run web-scraper/scripts/scrape.py https://example.com/article --links --json
uv run web-scraper/scripts/scrape.py https://reddit.com/r/programming/top/?t=week
```

## Options

| Flag | Description |
|------|-------------|
| `--links` | Preserve hyperlinks in output |
| `--images` | Include image references |
| `--no-tables` | Exclude tables |
| `--no-metadata` | Only return content body |
| `--language XX` | Filter to a target language |
| `--json` | Output as structured JSON |

## Reddit support

Reddit URLs get special handling via old.reddit.com HTML parsing (no API key needed):

- **Listing pages** — returns numbered posts with scores, comment counts, and links
- **Post pages** — returns title, body/link, and all comments with text

## Limitations

- JavaScript-rendered SPAs won't work (trafilatura fetches static HTML)
- Paywalled content returns only what's visible without login
- Some sites block automated requests via user-agent filtering

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r web-scraper/ ~/.config/devin/skills/web-scraper/
# or: cp -r web-scraper/ ~/.windsurf/skills/web-scraper/

# Project-specific
cp -r web-scraper/ /path/to/project/.devin/skills/web-scraper/
```

Then invoke with `/web-scraper` in a session.
