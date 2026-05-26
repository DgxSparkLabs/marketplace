# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""End-of-session audit: check docs, commits, and readiness for the next agent."""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def run_git(args: list[str], cwd: str) -> str | None:
    """Run a git command and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["git"] + args, capture_output=True, text=True, cwd=cwd, timeout=10,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def check_uncommitted(project_dir: str) -> dict:
    """Check for uncommitted changes."""
    status = run_git(["status", "--porcelain"], project_dir)
    if status is None:
        return {"name": "uncommitted_changes", "status": "SKIP", "detail": "Not a git repository"}
    if status:
        count = len(status.splitlines())
        return {"name": "uncommitted_changes", "status": "FAIL", "detail": f"{count} uncommitted file(s)"}
    return {"name": "uncommitted_changes", "status": "PASS", "detail": "Clean working tree"}


def check_file_exists(project_dir: str, filename: str) -> dict:
    """Check if a documentation file exists."""
    path = os.path.join(project_dir, filename)
    if os.path.isfile(path):
        return {"name": f"{filename}_exists", "status": "PASS", "detail": f"{filename} present"}
    return {"name": f"{filename}_exists", "status": "WARN", "detail": f"{filename} not found"}


def check_handoff_freshness(project_dir: str) -> dict:
    """Check if HANDOFF.md was modified more recently than the last commit."""
    handoff_path = os.path.join(project_dir, "HANDOFF.md")
    if not os.path.isfile(handoff_path):
        return {"name": "handoff_freshness", "status": "FAIL", "detail": "HANDOFF.md does not exist"}

    # Get last commit timestamp
    commit_ts = run_git(["log", "-1", "--format=%ct"], project_dir)
    if commit_ts is None:
        return {"name": "handoff_freshness", "status": "SKIP", "detail": "No git commits"}

    try:
        last_commit = int(commit_ts)
    except ValueError:
        return {"name": "handoff_freshness", "status": "SKIP", "detail": "Could not parse commit timestamp"}

    handoff_mtime = os.path.getmtime(handoff_path)

    if handoff_mtime >= last_commit:
        return {"name": "handoff_freshness", "status": "PASS", "detail": "HANDOFF.md is up to date"}
    else:
        age = datetime.now(timezone.utc).timestamp() - handoff_mtime
        hours = int(age / 3600)
        if hours > 0:
            return {"name": "handoff_freshness", "status": "WARN", "detail": f"HANDOFF.md last modified {hours}h ago"}
        minutes = max(1, int(age / 60))
        return {"name": "handoff_freshness", "status": "WARN", "detail": f"HANDOFF.md last modified {minutes}m ago"}


def main():
    parser = argparse.ArgumentParser(description="End-of-session handoff readiness audit")
    parser.add_argument("--dir", default=".", help="Project directory (default: cwd)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.dir)
    if not os.path.isdir(project_dir):
        print(f"Error: directory does not exist: {project_dir}", file=sys.stderr)
        sys.exit(1)

    checks = [
        check_uncommitted(project_dir),
        check_handoff_freshness(project_dir),
        check_file_exists(project_dir, "HANDOFF.md"),
        check_file_exists(project_dir, "PITFALLS.md"),
        check_file_exists(project_dir, "CHANGELOG.md"),
    ]

    if args.json_output:
        print(json.dumps({"project": project_dir, "checks": checks}, indent=2))
        return

    print(f"Session wrapup audit: {project_dir}")
    print()

    fails = 0
    warns = 0
    for check in checks:
        status = check["status"]
        icon = {"PASS": "OK", "FAIL": "!!", "WARN": "??", "SKIP": "--"}[status]
        print(f"  [{icon}] {check['detail']}")
        if status == "FAIL":
            fails += 1
        elif status == "WARN":
            warns += 1

    print()
    if fails > 0:
        print(f"Result: {fails} issue(s) to fix before ending session.")
        sys.exit(1)
    elif warns > 0:
        print(f"Result: All clear, {warns} advisory item(s).")
    else:
        print("Result: Project is ready for handoff.")


if __name__ == "__main__":
    main()
