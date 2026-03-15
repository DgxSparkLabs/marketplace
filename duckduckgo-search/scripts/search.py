# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ddgs>=7.0.0",
# ]
# ///
"""Search DuckDuckGo and return results as structured text or JSON."""

from __future__ import annotations

import argparse
import json
import sys
import textwrap


def search(
    query: str,
    *,
    max_results: int = 5,
    region: str = "wt-wt",
    time_range: str | None = None,
    output_json: bool = False,
) -> str:
    from ddgs import DDGS

    ddgs = DDGS()
    results = list(
        ddgs.text(
            query,
            region=region,
            timelimit=time_range,
            max_results=max_results,
        )
    )

    if not results:
        return "No results found."

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Search DuckDuckGo")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument(
        "-n", "--max-results",
        type=int,
        default=5,
        help="Maximum number of results (default: 5)",
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
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
