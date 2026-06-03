#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""validate_source.py — fast, friendly checks on construct sources (FR-13).

Runs at author time (and as a pre-commit hook) so a malformed source is caught
before the slower generate / --check / `claude plugin validate` cycle. Checks,
for each given path (default: all of src/):

  - every *.md with YAML frontmatter has a non-empty `description:`
  - every *.json parses
  - every ${CLAUDE_PLUGIN_ROOT}/<file> reference inside a *.json points at a
    file that exists in the plugin dir (catches the "config references a missing
    script" class — e.g. an lsp-config.json pointing at an untracked .py)
  - construct instance directory names are kebab-case

Usage:
    uv run scripts/validate_source.py [path ...]
Exit 0 if clean, 1 if any problem is found.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import SRC, _frontmatter  # noqa: E402

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PLUGIN_ROOT_REF = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"'\s]+)")
CONSTRUCT_DIRS = {
    "skills", "rules", "commands", "agents", "hooks", "mcp-servers",
    "lsp-servers", "monitors", "output-styles", "themes",
}


def _check_md(path: Path, problems: list[str]) -> None:
    fm = _frontmatter(path)
    if not fm:
        return  # plain markdown (e.g. README) - nothing to check
    # Require 'description' (the marketplace-listing one-liner). 'name' is NOT
    # required: commands derive their name from the filename stem, so requiring
    # it would false-positive on every command .md.
    if not fm.get("description"):
        problems.append(f"{path}: frontmatter missing or empty 'description'")


def _check_json(path: Path, problems: list[str]) -> None:
    try:
        text = path.read_text(encoding="utf-8-sig")
        json.loads(text)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        problems.append(f"{path}: invalid JSON ({exc})")
        return
    for m in PLUGIN_ROOT_REF.finditer(text):
        ref = m.group(1)
        if not (path.parent / ref).exists():
            problems.append(
                f"{path}: references ${{CLAUDE_PLUGIN_ROOT}}/{ref} "
                f"but {path.parent / ref} does not exist"
            )


def _iter_files(root: Path):
    if root.is_file():
        yield root
    elif root.is_dir():
        yield from (p for p in root.rglob("*") if p.is_file())


def _iter_instance_dirs(root: Path):
    """Yield directories that are an instance under a construct dir (.../<construct>/<name>)."""
    candidates = [root] if root.is_dir() else []
    if root.is_dir():
        candidates += [d for d in root.rglob("*") if d.is_dir()]
    for d in candidates:
        if d.parent.name in CONSTRUCT_DIRS:
            yield d


def validate(paths: list[Path]) -> list[str]:
    problems: list[str] = []
    for root in paths:
        if not root.exists():
            problems.append(f"{root}: path does not exist")
            continue
        for f in _iter_files(root):
            if f.name == "__pycache__" or f.suffix == ".pyc":
                continue
            if f.suffix == ".md":
                _check_md(f, problems)
            elif f.suffix == ".json":
                _check_json(f, problems)
        for d in _iter_instance_dirs(root):
            if not KEBAB.match(d.name):
                problems.append(f"{d}: instance directory name is not kebab-case")
    return problems


def main(argv: list[str]) -> int:
    paths = [Path(a).resolve() for a in argv] if argv else [SRC]
    problems = validate(paths)
    if problems:
        for p in problems:
            print(f"  FAIL: {p}", file=sys.stderr)
        print(f"\n{len(problems)} problem(s) found.", file=sys.stderr)
        return 1
    scanned = ", ".join(p.name for p in paths)
    print(f"source OK ({scanned})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
