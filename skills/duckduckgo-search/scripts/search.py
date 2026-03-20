# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ddgs>=7.0.0",
# ]
# ///
"""Search DuckDuckGo and return results as structured text or JSON."""

import argparse
import json
import re
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path

MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 5]


def _fetch(
    query: str,
    *,
    max_results: int,
    region: str,
    time_range: str | None,
) -> list[dict]:
    from ddgs import DDGS

    ddgs = DDGS()
    return list(
        ddgs.text(
            query,
            region=region,
            timelimit=time_range,
            max_results=max_results,
        )
    )


def search(
    query: str,
    *,
    max_results: int = 20,
    region: str = "wt-wt",
    time_range: str | None = None,
    output_json: bool = False,
) -> str:
    results: list[dict] = []
    last_error: Exception | None = None

    for attempt in range(MAX_RETRIES):
        try:
            results = _fetch(
                query,
                max_results=max_results,
                region=region,
                time_range=time_range,
            )
            if results:
                break
            # Empty results may be transient throttling — retry
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAYS[attempt]
                print(f"No results (attempt {attempt + 1}/{MAX_RETRIES}), retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAYS[attempt]
                print(f"Error: {e} (attempt {attempt + 1}/{MAX_RETRIES}), retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)

    if not results:
        if last_error:
            return f"Search failed after {MAX_RETRIES} attempts. Last error: {last_error}"
        return "No results found after exhausting retries."

    if output_json:
        return json.dumps(results, indent=2, ensure_ascii=False)

    lines: list[str] = []
    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        href = r.get("href", "")
        body = r.get("body", "")
        lines.append(f"[{i}] {title}")
        lines.append(f"    {href}")
        if body:
            wrapped = textwrap.fill(body, width=90, initial_indent="    ", subsequent_indent="    ")
            lines.append(wrapped)
        lines.append("")
    return "\n".join(lines)


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Search DuckDuckGo")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument(
        "-n", "--max-results",
        type=int,
        default=20,
        help="Maximum number of results (default: 20)",
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
        help="Output results as JSON",
    )

    args = parser.parse_args()
    query = " ".join(args.query)

    try:
        output = search(
            query,
            max_results=args.max_results,
            region=args.region,
            time_range=args.time,
            output_json=args.json,
        )
        ext = ".json" if args.json else ".txt"
        _save_and_emit(output, "duckduckgo-search", query, ext)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
