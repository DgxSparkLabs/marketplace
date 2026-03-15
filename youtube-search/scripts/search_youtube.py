# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ddgs>=7.0.0",
# ]
# ///
"""Search YouTube for technical videos and tutorials via DuckDuckGo."""

from __future__ import annotations

import argparse
import json
import sys
import textwrap


def parse_duration(raw: str | None) -> int | None:
    """Parse a duration string like '12:34' or '1:02:30' into total seconds."""
    if not raw:
        return None
    parts = raw.strip().split(":")
    try:
        parts = [int(p) for p in parts]
    except ValueError:
        return None
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return None


def fmt_published(raw: str | None) -> str:
    """Extract just the date from an ISO timestamp like '2026-01-27T14:39:28.0000000'."""
    if not raw:
        return ""
    return raw.split("T")[0]


def technical_score(result: dict) -> float:
    """Score a result higher if it looks technical/tutorial-like."""
    score = 0.0
    title = (result.get("title") or "").lower()
    desc = (result.get("description") or result.get("body") or "").lower()
    text = f"{title} {desc}"

    strong_signals = [
        "tutorial", "explained", "deep dive", "how to", "from scratch",
        "step by step", "crash course", "full course", "masterclass",
        "advanced", "internals", "under the hood", "architecture",
        "system design", "implementation", "walkthrough", "hands-on",
        "live coding", "code review", "tech talk", "conference",
    ]
    weak_signals = [
        "beginner", "introduction", "intro to", "getting started",
        "basics", "overview", "guide", "demo", "example",
        "programming", "developer", "engineering", "coding",
    ]
    negative_signals = [
        "shorts", "reaction", "vlog", "unboxing", "haul",
        "meme", "funny", "prank", "tiktok", "compilation",
    ]

    for signal in strong_signals:
        if signal in text:
            score += 2.0
    for signal in weak_signals:
        if signal in text:
            score += 0.5
    for signal in negative_signals:
        if signal in text:
            score -= 3.0

    # Prefer longer videos (more substance)
    dur = parse_duration(result.get("duration"))
    if dur is not None:
        if dur >= 1800:       # 30+ min
            score += 3.0
        elif dur >= 600:      # 10+ min
            score += 2.0
        elif dur >= 180:      # 3+ min
            score += 1.0
        elif dur < 60:        # shorts
            score -= 2.0

    # Boost videos with high view counts (battle-tested content)
    stats = result.get("statistics") or {}
    views = stats.get("viewCount")
    if views is not None:
        try:
            views = int(views)
        except (ValueError, TypeError):
            views = 0
        if views >= 500_000:
            score += 2.0
        elif views >= 100_000:
            score += 1.5
        elif views >= 10_000:
            score += 1.0

    return score


def search_videos(
    query: str,
    *,
    max_results: int = 10,
    region: str = "wt-wt",
    time_range: str | None = None,
) -> list[dict]:
    """Search for YouTube videos using DuckDuckGo video search."""
    from ddgs import DDGS

    ddgs = DDGS()
    raw = list(ddgs.videos(
        f"{query} site:youtube.com",
        region=region,
        timelimit=time_range,
        max_results=max_results * 3,  # fetch extra so we can filter/rank
    ))

    # Keep only YouTube results
    videos = [
        r for r in raw
        if "youtube.com" in (r.get("content") or "") or "youtu.be" in (r.get("content") or "")
    ]

    # Score and sort by technical relevance
    for v in videos:
        v["_score"] = technical_score(v)
    videos.sort(key=lambda v: v["_score"], reverse=True)

    return videos[:max_results]


def search_text_fallback(
    query: str,
    *,
    max_results: int = 10,
    region: str = "wt-wt",
    time_range: str | None = None,
) -> list[dict]:
    """Fallback: text search scoped to youtube.com."""
    from ddgs import DDGS

    ddgs = DDGS()
    raw = list(ddgs.text(
        f"site:youtube.com {query}",
        region=region,
        timelimit=time_range,
        max_results=max_results * 2,
    ))

    results = []
    for r in raw:
        href = r.get("href", "")
        if "youtube.com/watch" not in href and "youtu.be" not in href:
            continue
        results.append({
            "title": r.get("title", ""),
            "content": href,
            "description": r.get("body", ""),
            "uploader": "",
            "duration": "",
            "_score": technical_score({
                "title": r.get("title", ""),
                "description": r.get("body", ""),
            }),
        })

    results.sort(key=lambda v: v["_score"], reverse=True)
    return results[:max_results]


def format_results(videos: list[dict], *, show_scores: bool = False) -> str:
    """Format video results as readable text."""
    if not videos:
        return "No YouTube videos found."

    lines: list[str] = []
    for i, v in enumerate(videos, 1):
        title = v.get("title", "Unknown")
        url = v.get("content", v.get("href", ""))
        desc = v.get("description", v.get("body", ""))
        uploader = v.get("uploader", "")
        duration = v.get("duration", "")
        published = fmt_published(v.get("published", ""))

        meta_parts = []
        if duration:
            meta_parts.append(duration)
        if uploader:
            meta_parts.append(uploader)
        if published:
            meta_parts.append(published)
        meta = " | ".join(meta_parts)

        lines.append(f"[{i}] {title}")
        lines.append(f"    {url}")
        if meta:
            lines.append(f"    {meta}")
        if desc:
            wrapped = textwrap.fill(
                desc, width=90,
                initial_indent="    ", subsequent_indent="    ",
            )
            lines.append(wrapped)
        if show_scores:
            lines.append(f"    [score: {v.get('_score', 0):.1f}]")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search YouTube for technical videos and tutorials",
    )
    parser.add_argument("query", nargs="+", help="Search query / topic")
    parser.add_argument(
        "-n", "--max-results",
        type=int, default=10,
        help="Maximum results to return (default: 10)",
    )
    parser.add_argument(
        "-r", "--region",
        default="wt-wt",
        help="Region code, e.g. us-en, uk-en, wt-wt for global (default: wt-wt)",
    )
    parser.add_argument(
        "-t", "--time",
        choices=["d", "w", "m", "y"],
        default=None,
        help="Time range: d=day, w=week, m=month, y=year",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "--scores",
        action="store_true",
        help="Show technical relevance scores",
    )

    args = parser.parse_args()
    query = " ".join(args.query)

    try:
        videos = search_videos(
            query,
            max_results=args.max_results,
            region=args.region,
            time_range=args.time,
        )

        # If video search returns too few, supplement with text search
        if len(videos) < args.max_results // 2:
            seen = {v.get("content", "") for v in videos}
            fallback = search_text_fallback(
                query,
                max_results=args.max_results,
                region=args.region,
                time_range=args.time,
            )
            for fb in fallback:
                if fb.get("content", "") not in seen:
                    videos.append(fb)
                    seen.add(fb.get("content", ""))
            videos.sort(key=lambda v: v.get("_score", 0), reverse=True)
            videos = videos[:args.max_results]

        if args.json:
            # Strip internal scoring field for clean output
            clean = [{k: v for k, v in vid.items() if not k.startswith("_")} for vid in videos]
            print(json.dumps(clean, indent=2, ensure_ascii=False))
        else:
            print(format_results(videos, show_scores=args.scores))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
