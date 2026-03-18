# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Sync rules from global AI agent configs into a workspace.

Scans Devin, Claude Code, Cursor, and Windsurf global config directories,
deduplicates rules across agents by content similarity, and writes the
merged result into workspace rule files.

Usage:
    uv run sync-rules/scripts/sync_rules.py                     # scan only (dry run)
    uv run sync-rules/scripts/sync_rules.py --write agents       # write to AGENTS.md
    uv run sync-rules/scripts/sync_rules.py --write cursor       # write to .cursor/rules/
    uv run sync-rules/scripts/sync_rules.py --write windsurf     # write to .windsurf/rules/
    uv run sync-rules/scripts/sync_rules.py --write all          # write to all formats
    uv run sync-rules/scripts/sync_rules.py --agent devin        # only scan Devin globals
    uv run sync-rules/scripts/sync_rules.py --workspace /path    # target a specific directory
"""
from __future__ import annotations

import argparse
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path

GLOBAL_SOURCES = {
    "devin": {
        "label": "Devin CLI",
        "rules_path": Path.home() / ".config" / "devin" / "AGENTS.md",
        "format": "agents",
    },
    "claude-code": {
        "label": "Claude Code",
        "rules_path": Path.home() / ".claude" / "CLAUDE.md",
        "format": "agents",
    },
    "cursor": {
        "label": "Cursor",
        "rules_path": Path.home() / ".cursor" / "rules",
        "format": "cursor",
    },
    "windsurf": {
        "label": "Windsurf",
        "rules_path": Path.home() / ".windsurf" / "rules",
        "format": "windsurf",
    },
}

SIMILARITY_THRESHOLD = 0.75


# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_markdown_sections(text: str, source_agent: str, source_path: str) -> list[dict]:
    """Split a Markdown file into rules by ## headings."""
    rules: list[dict] = []
    current_name: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current_name and current_lines:
                content = "\n".join(current_lines).strip()
                if content:
                    rules.append({
                        "name": current_name,
                        "sources": [{"agent": source_agent, "path": source_path}],
                        "content": content,
                    })
            current_name = line[3:].strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)

    if current_name and current_lines:
        content = "\n".join(current_lines).strip()
        if content:
            rules.append({
                "name": current_name,
                "sources": [{"agent": source_agent, "path": source_path}],
                "content": content,
            })
    return rules


def strip_frontmatter(text: str) -> tuple[dict, str]:
    """Remove YAML frontmatter and return (metadata_dict, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text

    frontmatter_str = text[3:end].strip()
    body = text[end + 3:].strip()

    meta: dict[str, str] = {}
    for line in frontmatter_str.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip("\"'")
    return meta, body


def parse_rule_file(path: Path, source_agent: str) -> dict | None:
    """Parse a single .md rule file (Cursor or Windsurf format)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    if not text.strip():
        return None

    meta, body = strip_frontmatter(text)
    name = meta.get("description", path.stem)
    if len(name) > 80:
        name = path.stem

    return {
        "name": name or path.stem,
        "sources": [{"agent": source_agent, "path": str(path)}],
        "content": body,
    }


# ── Discovery ────────────────────────────────────────────────────────────────

def discover(agents: list[str] | None = None) -> list[dict]:
    """Discover all rules from global agent configs."""
    rules: list[dict] = []
    for agent_id, info in GLOBAL_SOURCES.items():
        if agents and agent_id not in agents:
            continue
        path = info["rules_path"]
        fmt = info["format"]

        if fmt == "agents":
            if path.is_file():
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError) as e:
                    print(f"Warning: Could not read {path}: {e}", file=sys.stderr)
                    continue
                rules.extend(parse_markdown_sections(text, agent_id, str(path)))
        else:
            if path.is_dir():
                for md_file in sorted(path.glob("*.md")):
                    rule = parse_rule_file(md_file, agent_id)
                    if rule:
                        rules.append(rule)
    return rules


# ── Deduplication ────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Collapse whitespace for comparison."""
    return " ".join(text.split()).lower()


def content_similarity(a: str, b: str) -> float:
    """Return 0-1 similarity ratio between two rule bodies."""
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def deduplicate(rules: list[dict]) -> list[dict]:
    """Merge rules that are duplicates across agents.

    Two rules are considered duplicates if their content similarity
    exceeds the threshold. When merged, the longest version is kept
    and all sources are combined.
    """
    groups: list[dict] = []
    for rule in rules:
        merged = False
        for group in groups:
            if content_similarity(rule["content"], group["content"]) >= SIMILARITY_THRESHOLD:
                # Keep the longer version as canonical
                if len(rule["content"]) > len(group["content"]):
                    group["content"] = rule["content"]
                group["sources"].extend(rule["sources"])
                # Prefer the more descriptive name
                if len(rule["name"]) > len(group["name"]):
                    group["name"] = rule["name"]
                merged = True
                break
        if not merged:
            groups.append({
                "name": rule["name"],
                "sources": list(rule["sources"]),
                "content": rule["content"],
            })
    return groups


# ── Workspace scanning ───────────────────────────────────────────────────────

def scan_workspace_rules(workspace: Path) -> list[dict]:
    """Find rules already present in workspace config files."""
    existing: list[dict] = []

    # AGENTS.md / CLAUDE.md (## sections)
    for name in ("AGENTS.md", "CLAUDE.md"):
        md_path = workspace / name
        if md_path.is_file():
            try:
                text = md_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for rule in parse_markdown_sections(text, f"workspace:{name}", str(md_path)):
                existing.append(rule)

    # .cursor/rules/ and .windsurf/rules/
    for dirname in (".cursor", ".windsurf"):
        rules_dir = workspace / dirname / "rules"
        if rules_dir.is_dir():
            for md_file in sorted(rules_dir.glob("*.md")):
                rule = parse_rule_file(md_file, f"workspace:{dirname}")
                if rule:
                    existing.append(rule)

    # .devin/ AGENTS.md
    devin_agents = workspace / ".devin" / "AGENTS.md"
    if devin_agents.is_file():
        try:
            text = devin_agents.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass
        else:
            for rule in parse_markdown_sections(text, "workspace:.devin", str(devin_agents)):
                existing.append(rule)

    return existing


def find_conflicts(incoming: list[dict], existing: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split incoming rules into new (no conflict) and conflicting (already in workspace).

    Returns (new_rules, conflicts) where each conflict has an extra
    'workspace_match' field pointing to the existing rule it overlaps with.
    """
    new_rules: list[dict] = []
    conflicts: list[dict] = []
    for rule in incoming:
        match = None
        for ex in existing:
            if content_similarity(rule["content"], ex["content"]) >= SIMILARITY_THRESHOLD:
                match = ex
                break
        if match:
            conflicts.append({**rule, "workspace_match": match})
        else:
            new_rules.append(rule)
    return new_rules, conflicts


# ── Writing ──────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """Turn a rule name into a kebab-case filename."""
    slug = name.lower().replace(" ", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-").strip("-")
    return slug or "rule"


def unique_path(dest: Path, taken: set[Path]) -> Path:
    """Return *dest* if unused, otherwise append -2, -3, ... until unique."""
    if dest not in taken:
        return dest
    stem, suffix = dest.stem, dest.suffix
    n = 2
    while True:
        candidate = dest.with_name(f"{stem}-{n}{suffix}")
        if candidate not in taken:
            return candidate
        n += 1


def yaml_escape(value: str) -> str:
    """Escape a string for use as a double-quoted YAML value."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def rule_description(rule: dict) -> str:
    """Extract a short description from a rule's content, safe for YAML frontmatter."""
    first_line = rule["content"].split("\n")[0].strip()
    desc = first_line[:77] + "..." if len(first_line) > 80 else first_line
    return yaml_escape(desc)


def write_agents_md(rules: list[dict], workspace: Path) -> Path:
    """Append rules to AGENTS.md."""
    target = workspace / "AGENTS.md"
    existing_text = ""
    if target.is_file():
        existing_text = target.read_text(encoding="utf-8")

    new_sections: list[str] = []
    for rule in rules:
        section = f"## {rule['name']}\n\n{rule['content']}"
        new_sections.append(section)

    addition = "\n\n".join(new_sections)
    if existing_text.strip():
        final = existing_text.rstrip() + "\n\n" + addition + "\n"
    else:
        final = addition + "\n"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(final, encoding="utf-8")
    return target


def write_cursor(rules: list[dict], workspace: Path) -> list[Path]:
    """Write rules as separate .md files to .cursor/rules/."""
    rules_dir = workspace / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    taken: set[Path] = set()
    paths: list[Path] = []
    for rule in rules:
        slug = slugify(rule["name"])
        dest = unique_path(rules_dir / f"{slug}.md", taken)
        taken.add(dest)
        desc = rule_description(rule)
        text = f"---\ndescription: \"{desc}\"\nalwaysApply: true\n---\n\n{rule['content']}\n"
        dest.write_text(text, encoding="utf-8")
        paths.append(dest)
    return paths


def write_windsurf(rules: list[dict], workspace: Path) -> list[Path]:
    """Write rules as separate .md files to .windsurf/rules/."""
    rules_dir = workspace / ".windsurf" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    taken: set[Path] = set()
    paths: list[Path] = []
    for rule in rules:
        slug = slugify(rule["name"])
        dest = unique_path(rules_dir / f"{slug}.md", taken)
        taken.add(dest)
        desc = rule_description(rule)
        text = f"---\ntrigger: always_on\ndescription: \"{desc}\"\n---\n\n{rule['content']}\n"
        dest.write_text(text, encoding="utf-8")
        paths.append(dest)
    return paths


WRITERS = {
    "agents": write_agents_md,
    "cursor": write_cursor,
    "windsurf": write_windsurf,
}


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Sync rules from global AI agent configs into a workspace."
    )
    parser.add_argument(
        "--agent", action="append", choices=list(GLOBAL_SOURCES.keys()),
        help="Filter source agents (repeatable). Default: all.",
    )
    parser.add_argument(
        "--write", choices=["agents", "cursor", "windsurf", "all"],
        help="Write rules to workspace in this format. Omit for dry-run scan.",
    )
    parser.add_argument(
        "--workspace", type=Path, default=Path.cwd(),
        help="Workspace directory (default: current directory).",
    )
    parser.add_argument(
        "--include-conflicts", action="store_true",
        help="Also write rules that conflict with existing workspace rules.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON instead of human-readable text.",
    )
    args = parser.parse_args()

    # Discover
    raw_rules = discover(agents=args.agent)
    if not raw_rules:
        agents_checked = args.agent or list(GLOBAL_SOURCES.keys())
        paths_checked = [str(GLOBAL_SOURCES[a]["rules_path"]) for a in agents_checked]
        if args.json:
            print(json.dumps({"rules": [], "paths_checked": paths_checked}, indent=2))
        else:
            print("No rules found in global configs.")
            print(f"Checked: {', '.join(paths_checked)}")
        return

    # Deduplicate across agents
    merged = deduplicate(raw_rules)

    # Check workspace for conflicts
    workspace_rules = scan_workspace_rules(args.workspace)
    new_rules, conflicts = find_conflicts(merged, workspace_rules)

    if args.json:
        output = {
            "discovered": len(raw_rules),
            "after_dedup": len(merged),
            "new": [{"name": r["name"], "sources": r["sources"]} for r in new_rules],
            "conflicts": [
                {
                    "name": c["name"],
                    "sources": c["sources"],
                    "workspace_match": c["workspace_match"]["name"],
                }
                for c in conflicts
            ],
        }
        if args.write:
            output["wrote_to"] = args.write
            output["rules_written"] = len(new_rules) + (len(conflicts) if args.include_conflicts else 0)
        print(json.dumps(output, indent=2))
    else:
        source_agents = sorted({s["agent"] for r in merged for s in r["sources"]})
        print(f"Found {len(raw_rules)} rules across {', '.join(source_agents)}")
        dedup_count = len(raw_rules) - len(merged)
        if dedup_count:
            print(f"Deduplicated {dedup_count} cross-agent duplicates -> {len(merged)} unique rules")
        print()

        if new_rules:
            print(f"New rules ({len(new_rules)}):")
            for r in new_rules:
                agents = ", ".join(s["agent"] for s in r["sources"])
                print(f"  + {r['name']}  (from {agents})")
        if conflicts:
            print(f"\nAlready in workspace ({len(conflicts)}):")
            for c in conflicts:
                agents = ", ".join(s["agent"] for s in c["sources"])
                print(f"  = {c['name']}  (from {agents}, matches workspace '{c['workspace_match']['name']}')")

    # Write if requested
    if args.write:
        to_write = list(new_rules)
        if args.include_conflicts:
            to_write.extend(conflicts)

        if not to_write:
            if not args.json:
                print("\nNothing to write — all rules already in workspace.")
            return

        formats = list(WRITERS.keys()) if args.write == "all" else [args.write]
        for fmt in formats:
            writer = WRITERS[fmt]
            result = writer(to_write, args.workspace)
            if not args.json:
                if isinstance(result, list):
                    print(f"\nWrote {len(result)} files to {fmt}:")
                    for p in result:
                        print(f"  {p}")
                else:
                    print(f"\nAppended {len(to_write)} rules to {result}")
    elif not args.json:
        print("\nDry run — pass --write <format> to sync rules into workspace.")


if __name__ == "__main__":
    main()
