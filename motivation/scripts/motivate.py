# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Completeness checker: report what's actually unfinished.

Checks git status, HANDOFF.md freshness, test artifacts, and prints
a concrete list of what remains. Replaces the old pep-talk motivator
with state-based feedback.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: str | None = None) -> tuple[int, str]:
    """Run a command, return (exit_code, stdout)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10, cwd=cwd)
        return r.returncode, r.stdout.strip()
    except Exception:
        return -1, ""


def check_git(cwd: str) -> list[str]:
    """Check for uncommitted changes."""
    issues = []
    rc, out = run(["git", "status", "--porcelain"], cwd=cwd)
    if rc != 0:
        return ["Not a git repository"]
    if out:
        lines = out.strip().split("\n")
        modified = [ln for ln in lines if ln.startswith(" M") or ln.startswith("M ")]
        untracked = [ln for ln in lines if ln.startswith("??")]
        staged = [ln for ln in lines if ln[0] in "ACDMR" and ln[1] == " "]
        if modified:
            issues.append(f"{len(modified)} modified file(s) not staged")
        if untracked:
            issues.append(f"{len(untracked)} untracked file(s)")
        if staged:
            issues.append(f"{len(staged)} staged but uncommitted file(s)")
    return issues


def check_handoff(cwd: str) -> list[str]:
    """Check if HANDOFF.md exists and is recent."""
    issues = []
    handoff = Path(cwd) / "HANDOFF.md"
    if not handoff.exists():
        issues.append("HANDOFF.md does not exist")
        return issues

    # Check if HANDOFF.md was modified more recently than the last commit
    rc, last_commit_time = run(
        ["git", "log", "-1", "--format=%ct", "--", "HANDOFF.md"], cwd=cwd
    )
    rc2, head_time = run(["git", "log", "-1", "--format=%ct"], cwd=cwd)
    if rc == 0 and rc2 == 0 and last_commit_time and head_time:
        if int(head_time) - int(last_commit_time) > 3600:
            issues.append(
                "HANDOFF.md has not been updated in the last commit(s) — "
                "may be stale"
            )
    return issues


def check_tests(cwd: str) -> list[str]:
    """Check for test runner and recent test results."""
    issues = []
    # Look for common test runner locations
    runners = [
        Path(cwd) / "test" / "run_tests.sh",
        Path(cwd) / "tests" / "run_tests.sh",
        Path(cwd) / "shim" / "test" / "run_tests.sh",
    ]
    has_runner = any(r.exists() for r in runners)
    if not has_runner:
        issues.append("No test runner found (test/run_tests.sh)")
    return issues


def check_build(cwd: str) -> list[str]:
    """Check if build artifacts exist."""
    issues = []
    build_dirs = [
        Path(cwd) / "build",
        Path(cwd) / "shim" / "build",
    ]
    has_build = any(d.exists() for d in build_dirs)
    build_files = ["Makefile", "CMakeLists.txt", "Cargo.toml", "package.json"]
    has_build_system = any((Path(cwd) / f).exists() for f in build_files) or any(
        (Path(cwd) / "shim" / f).exists() for f in build_files
    )

    if has_build_system and not has_build:
        issues.append("Build system found but no build directory — run the build")
    return issues


def main() -> None:
    as_json = "--json" in sys.argv
    cwd = os.getcwd()

    checks = {
        "git": check_git(cwd),
        "handoff": check_handoff(cwd),
        "tests": check_tests(cwd),
        "build": check_build(cwd),
    }

    total_issues = sum(len(v) for v in checks.values())

    if as_json:
        print(json.dumps({
            "complete": total_issues == 0,
            "issues": checks,
            "total_issues": total_issues,
        }, indent=2))
        return

    print("=" * 60)
    print("COMPLETENESS CHECK")
    print("=" * 60)
    print()

    if total_issues == 0:
        print("  All clear. Nothing obviously incomplete.")
        print()
        print("  Double-check:")
        print("  - Are all todo items marked complete?")
        print("  - Did you run the test suite?")
        print("  - Is HANDOFF.md accurate?")
    else:
        print(f"  {total_issues} issue(s) found:\n")
        for category, issues in checks.items():
            if issues:
                for issue in issues:
                    print(f"  [{category}] {issue}")
        print()
        print("  Fix these before declaring done.")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
