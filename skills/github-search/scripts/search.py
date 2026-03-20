# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Search GitHub repositories for prior work and inspiration. Requires `gh` CLI."""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


JSON_FIELDS = "name,owner,description,stargazersCount,forksCount,language,license,updatedAt,url"


def _run_gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh failed: {result.stderr.strip()}")
    return result.stdout


def _relative_date(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        delta = datetime.now(dt.tzinfo) - dt
        if delta.days > 365:
            return f"{delta.days // 365}y ago"
        if delta.days > 30:
            return f"{delta.days // 30}mo ago"
        if delta.days > 0:
            return f"{delta.days}d ago"
        return "today"
    except Exception:
        return iso[:10]


def search_repos(
    query: str,
    *,
    limit: int = 20,
    language: str | None = None,
    sort: str = "stars",
    min_stars: int = 0,
    topic: str | None = None,
    output_json: bool = False,
) -> str:
    cmd = ["search", "repos", query, "--json", JSON_FIELDS, "-L", str(limit)]
    if sort:
        cmd += ["--sort", sort]
    if language:
        cmd += ["--language", language]
    if min_stars > 0:
        cmd += ["--stars", f">={min_stars}"]
    if topic:
        cmd += ["--topic", topic]

    raw = _run_gh(cmd)
    repos = json.loads(raw) if raw.strip() else []

    if not repos:
        return "No repositories found."

    if output_json:
        return json.dumps(repos, indent=2, ensure_ascii=False)

    lines: list[str] = []
    for i, r in enumerate(repos, 1):
        owner = r.get("owner", {}).get("login", "?")
        name = r.get("name", "?")
        stars = r.get("stargazersCount", 0)
        forks = r.get("forksCount", 0)
        lang = r.get("language", "") or ""
        desc = r.get("description", "") or ""
        url = r.get("url", "")
        updated = _relative_date(r.get("updatedAt", ""))
        license_name = ""
        li = r.get("license")
        if li and isinstance(li, dict):
            license_name = li.get("key", "") or ""
        elif isinstance(li, str):
            license_name = li

        meta_parts = []
        if stars:
            meta_parts.append(f"{stars:,} stars")
        if forks:
            meta_parts.append(f"{forks:,} forks")
        if lang:
            meta_parts.append(lang)
        if license_name:
            meta_parts.append(license_name)
        meta_parts.append(f"updated {updated}")
        meta = " | ".join(meta_parts)

        lines.append(f"[{i}] {owner}/{name}")
        lines.append(f"    {url}")
        lines.append(f"    {meta}")
        if desc:
            lines.append(f"    {desc}")
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
    parser = argparse.ArgumentParser(
        description="Search GitHub repositories for prior work",
    )
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=20,
        help="Maximum number of results (default: 20)",
    )
    parser.add_argument(
        "-l", "--language",
        default=None,
        help="Filter by programming language (e.g. python, rust, go)",
    )
    parser.add_argument(
        "-s", "--sort",
        choices=["stars", "forks", "updated", "best-match"],
        default="stars",
        help="Sort order (default: stars)",
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=0,
        help="Minimum number of stars (default: 0)",
    )
    parser.add_argument(
        "--topic",
        default=None,
        help="Filter by repository topic",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()
    query = " ".join(args.query)

    try:
        output = search_repos(
            query,
            limit=args.limit,
            language=args.language,
            sort=args.sort,
            min_stars=args.min_stars,
            topic=args.topic,
            output_json=args.json,
        )
        ext = ".json" if args.json else ".txt"
        _save_and_emit(output, "github-search", query, ext)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
