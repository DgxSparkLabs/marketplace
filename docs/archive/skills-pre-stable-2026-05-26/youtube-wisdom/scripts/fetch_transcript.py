# /// script
# requires-python = ">=3.11"
# dependencies = ["youtube-transcript-api>=1.0.0"]
# ///
"""Fetch a YouTube video's transcript and metadata."""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime
from html import unescape
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats or a bare ID."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id


def fetch_title(video_id: str) -> str:
    """Fetch the video title from the YouTube page."""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        match = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
        if match:
            title = unescape(match.group(1)).replace(" - YouTube", "").strip()
            return title
    except Exception:
        pass
    return ""


def fetch_transcript(video_id: str, lang: str | None = None):
    """Fetch transcript, trying requested language first, then falling back."""
    api = YouTubeTranscriptApi()

    if lang:
        try:
            return api.fetch(video_id, languages=[lang])
        except Exception:
            pass

    # Try with English first
    try:
        return api.fetch(video_id, languages=["en"])
    except Exception:
        pass

    # Fall back: pick manually created over auto-generated
    try:
        transcript_list = api.list(video_id)
        for t in transcript_list:
            if not t.is_generated:
                return t.fetch()
        for t in transcript_list:
            return t.fetch()
    except Exception:
        pass

    # Last resort: let the API pick
    return api.fetch(video_id)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS."""
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _save_and_emit(output: str, skill_name: str, label: str, ext: str = ".txt") -> None:
    """Save output to agent-fetched/<skill_name>/ and print path or content."""
    slug = re.sub(r"[^\w\-.]", "_", label)[:80].strip("_")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("agent-fetched") / skill_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{ts}_{slug}{ext}"
    out_path.write_text(output, encoding="utf-8")
    if len(output) > 500:
        size_kb = len(output.encode("utf-8")) / 1024
        print(f"Results saved to {out_path} ({len(output):,} chars, {size_kb:.1f} KB)")
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--lang", help="Preferred transcript language code (e.g. en, es, fr)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    title = fetch_title(video_id)

    try:
        segments = fetch_transcript(video_id, args.lang)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.as_json:
        data = {
            "video_id": video_id,
            "title": title,
            "segments": [{"timestamp": s.start, "text": s.text} for s in segments],
        }
        output = json.dumps(data, ensure_ascii=False, indent=2)
        _save_and_emit(output, "youtube-wisdom", video_id, ".json")
    else:
        lines: list[str] = []
        if title:
            lines.append(f"# {title}\n")
        for segment in segments:
            ts = format_timestamp(segment.start)
            lines.append(f"[{ts}] {segment.text}")
        output = "\n".join(lines)
        _save_and_emit(output, "youtube-wisdom", video_id, ".txt")


if __name__ == "__main__":
    main()
