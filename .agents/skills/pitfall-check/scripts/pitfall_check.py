# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Search PITFALLS.md and git log for known issues related to given keywords."""

import argparse
import os
import re
import subprocess


def search_pitfalls_file(pitfalls_path: str, keywords: list[str]) -> list[str]:
    """Search PITFALLS.md for entries containing any of the keywords."""
    if not os.path.isfile(pitfalls_path):
        return []

    with open(pitfalls_path) as f:
        content = f.read()

    # Split into entries by horizontal rule or heading
    entries = re.split(r'\n(?=---|\n##\s)', content)
    matches = []
    pattern = re.compile("|".join(re.escape(k) for k in keywords), re.IGNORECASE)

    for entry in entries:
        if pattern.search(entry):
            stripped = entry.strip()
            if stripped and not stripped.startswith("# ") and stripped != "---":
                matches.append(stripped)

    return matches


def search_git_log(project_dir: str, keywords: list[str], limit: int) -> list[str]:
    """Search git log for commits mentioning any of the keywords."""
    matches = []
    for keyword in keywords:
        try:
            result = subprocess.run(
                ["git", "log", f"--max-count={limit}", "--oneline",
                 f"--grep={keyword}", "-i"],
                capture_output=True, text=True, cwd=project_dir, timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.strip().splitlines():
                    if line not in matches:
                        matches.append(line)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    return matches


def main():
    parser = argparse.ArgumentParser(
        description="Search PITFALLS.md and git log for known issues"
    )
    parser.add_argument("keywords", nargs="+", help="Keywords to search for")
    parser.add_argument("--dir", default=".", help="Project directory (default: cwd)")
    parser.add_argument(
        "--git-log-limit", type=int, default=200,
        help="Max git log entries to search (default: 200)",
    )
    args = parser.parse_args()

    project_dir = os.path.abspath(args.dir)
    pitfalls_path = os.path.join(project_dir, "PITFALLS.md")

    print(f"Searching for: {', '.join(args.keywords)}")
    print(f"Project: {project_dir}")
    print()

    # Search PITFALLS.md
    pitfall_matches = search_pitfalls_file(pitfalls_path, args.keywords)
    if pitfall_matches:
        print(f"=== PITFALLS.md ({len(pitfall_matches)} match{'es' if len(pitfall_matches) != 1 else ''}) ===")
        print()
        for match in pitfall_matches:
            print(match)
            print()
    elif os.path.isfile(pitfalls_path):
        print("=== PITFALLS.md: no matches ===")
        print()
    else:
        print("=== PITFALLS.md: file not found ===")
        print()

    # Search git log
    git_matches = search_git_log(project_dir, args.keywords, args.git_log_limit)
    if git_matches:
        print(f"=== Git log ({len(git_matches)} match{'es' if len(git_matches) != 1 else ''}) ===")
        print()
        for match in git_matches:
            print(f"  {match}")
    else:
        print("=== Git log: no matches ===")

    # Summary
    total = len(pitfall_matches) + len(git_matches)
    if total == 0:
        print()
        print("No known pitfalls found. Proceed with normal caution.")
        print("Remember to add a PITFALLS.md entry if you discover an issue.")
    else:
        print()
        print(f"Found {total} related item{'s' if total != 1 else ''}. Review before proceeding.")


if __name__ == "__main__":
    main()
