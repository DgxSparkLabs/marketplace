# /// script
# requires-python = ">=3.10"
# ///
"""Scan a codebase for mechanical code health issues.

Reports: large files, duplicate definition names, high-density files,
generic file names, and CODEBASE.md status.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Patterns that indicate a named definition in common languages
DEFINITION_PATTERNS = [
    # TypeScript / JavaScript
    (re.compile(r"^\s*(?:export\s+)?type\s+(\w+)", re.MULTILINE), "type"),
    (re.compile(r"^\s*(?:export\s+)?interface\s+(\w+)", re.MULTILINE), "interface"),
    (re.compile(r"^\s*(?:export\s+)?enum\s+(\w+)", re.MULTILINE), "enum"),
    (re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*[=:]", re.MULTILINE), "const"),
    (re.compile(r"^\s*(?:export\s+)?(?:function|async\s+function)\s+(\w+)", re.MULTILINE), "function"),
    # Python
    (re.compile(r"^class\s+(\w+)", re.MULTILINE), "class"),
    (re.compile(r"^def\s+(\w+)", re.MULTILINE), "function"),
    (re.compile(r"^(\w+)\s*=\s*", re.MULTILINE), "const"),
    # Rust
    (re.compile(r"^\s*(?:pub\s+)?struct\s+(\w+)", re.MULTILINE), "struct"),
    (re.compile(r"^\s*(?:pub\s+)?enum\s+(\w+)", re.MULTILINE), "enum"),
    (re.compile(r"^\s*(?:pub\s+)?fn\s+(\w+)", re.MULTILINE), "function"),
    # Go
    (re.compile(r"^type\s+(\w+)\s+struct", re.MULTILINE), "struct"),
    (re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)", re.MULTILINE), "function"),
]

SKIP_DIRS = frozenset({
    "node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build",
    ".next", ".nuxt", "coverage", ".tox", ".mypy_cache", ".pytest_cache",
    "vendor", "target", ".cargo", "pkg", "bin", "obj", ".svelte-kit",
    ".turbo", ".cache", ".parcel-cache",
})

CODE_EXTENSIONS = frozenset({
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".rs", ".go", ".java", ".kt", ".kts",
    ".c", ".cpp", ".h", ".hpp", ".cs",
    ".rb", ".php", ".swift", ".scala",
    ".lua", ".sh", ".bash", ".zsh", ".svelte", ".vue",
})

GENERIC_NAMES = frozenset({
    "utils", "util", "helpers", "helper", "misc", "common", "stuff",
    "shared", "lib", "tools", "functions", "methods", "index",
})

# Short common names that aren't meaningful duplicates
TRIVIAL_NAMES = frozenset({
    "i", "j", "k", "x", "y", "z", "e", "f", "n", "s", "t", "v",
    "id", "ok", "fn", "cb", "el", "db", "fs", "os", "re", "io",
    "key", "val", "err", "req", "res", "msg", "buf", "ctx", "cfg",
    "len", "max", "min", "sum", "map", "set", "get", "put", "run",
    "log", "cmd", "env", "cwd", "pid", "uid", "gid", "url", "uri",
    "args", "opts", "data", "name", "path", "self", "this", "init",
    "main", "test", "type", "item", "node", "list", "root", "home",
    "app", "cli", "api", "row", "col", "pos", "end", "src", "dst",
    "tmp", "old", "new", "out", "ret", "idx", "num", "str", "int",
    "bool", "true", "false", "none", "null", "void",
})


def should_skip(name: str) -> bool:
    """Skip directory or file."""
    return name.startswith(".") or name in SKIP_DIRS


def get_tracked_files(root: Path) -> list[Path] | None:
    """Get git-tracked files. Returns None if not a git repo."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            cwd=root,
            timeout=30,
        )
        if result.returncode != 0:
            return None
        return [root / line for line in result.stdout.splitlines() if line]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def collect_files(root: Path) -> list[tuple[Path, str]]:
    """Collect code files to scan. Uses git ls-files if available, else walks."""
    tracked = get_tracked_files(root)

    if tracked is not None:
        # Git-aware: only scan tracked files (respects .gitignore)
        results = []
        for fpath in tracked:
            if fpath.suffix.lower() in CODE_EXTENSIONS and fpath.is_file():
                results.append((fpath, str(fpath.relative_to(root))))
        return sorted(results, key=lambda x: x[1])

    # Fallback: walk with skip list
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not should_skip(d))
        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() in CODE_EXTENSIONS:
                results.append((fpath, str(fpath.relative_to(root))))
    return results


def scan_directory(root: Path, max_lines: int = 300) -> dict:
    """Scan codebase and return structured findings."""
    large_files = []
    definitions: dict[str, list] = defaultdict(list)
    high_density = []
    generic_names = []
    dirs_seen: set[str] = set()

    files = collect_files(root)

    for fpath, rel_path in files:
        # Collect directories
        parent = str(fpath.relative_to(root).parent)
        if parent != ".":
            dirs_seen.add(parent)

        stem = fpath.stem.lower()
        if stem in GENERIC_NAMES:
            generic_names.append(rel_path)

        try:
            content = fpath.read_text(errors="replace")
            line_count = len(content.splitlines())
        except OSError:
            continue

        if line_count > max_lines:
            large_files.append({"path": rel_path, "lines": line_count})

        def_count = 0
        for pattern, kind in DEFINITION_PATTERNS:
            for match in pattern.finditer(content):
                name = match.group(1)
                if len(name) <= 3 or name in TRIVIAL_NAMES or name.startswith("_"):
                    continue
                line_num = content[: match.start()].count("\n") + 1
                definitions[name].append(
                    {"path": rel_path, "line": line_num, "kind": kind}
                )
                def_count += 1

        if def_count > 20:
            high_density.append(
                {"path": rel_path, "definitions": def_count, "lines": line_count}
            )

    # Filter to definitions appearing in multiple distinct files
    duplicates = {}
    for name, locs in definitions.items():
        unique_files = set(loc["path"] for loc in locs)
        if len(unique_files) > 1:
            duplicates[name] = locs

    codebase_md = root / "CODEBASE.md"

    # Documentation health checks
    readme = root / "README.md"
    readme_lines = 0
    if readme.exists():
        try:
            readme_lines = len(readme.read_text(errors="replace").splitlines())
        except OSError:
            pass

    docs_dir = root / "docs"
    doc_files = []
    orphaned_docs = []
    if docs_dir.is_dir():
        # Find all markdown files in docs/
        for doc in sorted(docs_dir.rglob("*.md")):
            rel = str(doc.relative_to(root))
            doc_files.append(rel)

        # Check which docs are linked from README or other docs
        if readme.exists():
            try:
                all_doc_content = readme.read_text(errors="replace")
            except OSError:
                all_doc_content = ""
            for doc in docs_dir.rglob("*.md"):
                try:
                    all_doc_content += "\n" + doc.read_text(errors="replace")
                except OSError:
                    pass
            for rel in doc_files:
                # Check if the file is referenced by name anywhere
                fname = Path(rel).name
                if fname not in all_doc_content and rel not in all_doc_content:
                    orphaned_docs.append(rel)

    return {
        "duplicates": duplicates,
        "large_files": sorted(large_files, key=lambda x: -x["lines"]),
        "high_density": sorted(high_density, key=lambda x: -x["definitions"]),
        "generic_names": sorted(generic_names),
        "directory_tree": sorted(dirs_seen),
        "codebase_md_exists": codebase_md.exists(),
        "codebase_md_size": codebase_md.stat().st_size if codebase_md.exists() else 0,
        "readme_exists": readme.exists(),
        "readme_lines": readme_lines,
        "docs_dir_exists": docs_dir.is_dir(),
        "doc_files": doc_files,
        "orphaned_docs": orphaned_docs,
    }


def print_text_report(findings: dict, root: Path) -> None:
    """Print human-readable report."""
    print(f"# Code Health Scan: {root.name}\n")

    dupes = findings["duplicates"]
    if dupes:
        print(f"## Duplicate Definitions ({len(dupes)} names in multiple files)\n")
        for name in sorted(dupes, key=lambda n: -len(dupes[n])):
            locs = dupes[name]
            files = sorted(set(f"{loc['path']}:{loc['line']} ({loc['kind']})" for loc in locs))
            print(f"- **{name}** ({len(files)} locations)")
            for f in files:
                print(f"  - {f}")
        print()
    else:
        print("## Duplicate Definitions\nNone found.\n")

    if findings["large_files"]:
        print(f"## Large Files ({len(findings['large_files'])} over threshold)\n")
        for f in findings["large_files"]:
            print(f"- **{f['path']}** — {f['lines']} lines")
        print()

    if findings["high_density"]:
        print("## High Definition Density\n")
        for f in findings["high_density"]:
            print(
                f"- **{f['path']}** — {f['definitions']} definitions in {f['lines']} lines"
            )
        print()

    if findings["generic_names"]:
        print("## Generic File Names\n")
        for p in findings["generic_names"]:
            print(f"- {p}")
        print()

    print("## Directory Structure (top 3 levels)\n")
    for d in findings["directory_tree"]:
        depth = d.count(os.sep)
        if depth < 3:
            indent = "  " * depth
            print(f"{indent}- {Path(d).name}/")
    print()

    # Documentation health
    doc_issues = []
    if not findings["readme_exists"]:
        doc_issues.append("README.md: **MISSING**")
    elif findings["readme_lines"] > 100:
        doc_issues.append(
            f"README.md: {findings['readme_lines']} lines — consider trimming "
            "to a TL;DR and moving details to docs/"
        )
    if not findings["docs_dir_exists"]:
        doc_issues.append("docs/ directory: **MISSING** — no detailed guides")
    else:
        count = len(findings["doc_files"])
        doc_issues.append(f"docs/ directory: {count} file{'s' if count != 1 else ''}")
    if findings["orphaned_docs"]:
        doc_issues.append(
            f"Orphaned docs (not linked from any other doc): "
            f"{len(findings['orphaned_docs'])}"
        )
        for p in findings["orphaned_docs"]:
            doc_issues.append(f"  - {p}")

    if doc_issues:
        print("## Documentation Health\n")
        for issue in doc_issues:
            print(f"- {issue}")
        print()

    print("## Summary\n")
    print(f"- Duplicate definition names: {len(dupes)}")
    print(f"- Files over threshold: {len(findings['large_files'])}")
    print(f"- High-density files: {len(findings['high_density'])}")
    print(f"- Generic-named files: {len(findings['generic_names'])}")

    if findings["codebase_md_exists"]:
        print(
            f"- CODEBASE.md: exists ({findings['codebase_md_size']} bytes)"
        )
    else:
        print(
            "- CODEBASE.md: **MISSING** — create one to document module "
            "boundaries and shared types"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan codebase for maintainability issues"
    )
    parser.add_argument(
        "directory", nargs="?", default=".", help="Directory to scan (default: .)"
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=300,
        help="Line threshold for large files (default: 300)",
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output as JSON"
    )
    args = parser.parse_args()

    root = Path(args.directory).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    findings = scan_directory(root, args.max_lines)

    if args.json_output:
        json.dump(findings, sys.stdout, indent=2)
        print()
    else:
        print_text_report(findings, root)


if __name__ == "__main__":
    main()
