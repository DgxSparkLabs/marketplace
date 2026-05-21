#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
generate_manifest.py — produce all generated marketplace content from sources.

Reads:
  - MARKETPLACE.toml            (identity: owner, repo URL, version, license)
  - catalog.toml                (construct types + domain tagging)
  - skills/<name>/              (skill source content)
  - rules/<name>/               (rule source content + format mirrors)
  - examples/<name>/            (example reference plugins, included in manifest)

Writes:
  - .claude-plugin/marketplace.json
  - _generated/skill-<name>/    (per-skill plugin wrapper)
  - _generated/rule-<name>/     (per-rule plugin wrapper + activate.sh)
  - _generated/skills-<domain>/ (dep-only skill bundle plugin)
  - _generated/rules-<domain>/  (dep-only rule bundle plugin)
  - _generated/rules-all/       (catch-all rule bundle plugin)
  - .codex/skills/, .gemini/skills/, .cursor/rules/, .windsurf/rules/,
    .devin/rules/, .devin/skills/  (cross-platform mirrors)

Usage:
  uv run scripts/generate_manifest.py            # write everything
  uv run scripts/generate_manifest.py --check    # exit non-zero if output differs
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tomllib
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_TOML = REPO_ROOT / "MARKETPLACE.toml"
CATALOG_TOML = REPO_ROOT / "catalog.toml"
SKILLS_DIR = REPO_ROOT / "skills"
RULES_DIR = REPO_ROOT / "rules"
EXAMPLES_DIR = REPO_ROOT / "examples"
GENERATED_DIR = REPO_ROOT / "_generated"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"

# Cross-platform mirror roots
MIRRORS = {
    "codex":    REPO_ROOT / ".codex",
    "gemini":   REPO_ROOT / ".gemini",
    "cursor":   REPO_ROOT / ".cursor",
    "windsurf": REPO_ROOT / ".windsurf",
    "devin":    REPO_ROOT / ".devin",
}

ACTIVATE_SH_TEMPLATE = """\
#!/usr/bin/env bash
# activate.sh — symlink (or copy on platforms without symlink support)
# this plugin's rule file(s) into the project's .claude/rules/.
# Run once after installing this plugin.
#
# Usage:
#   bash <path>/activate.sh                   # default target: .claude/rules
#   bash <path>/activate.sh <rules-dir>       # custom target
#
# On Linux/macOS: creates symlinks so plugin updates auto-propagate.
# On Windows (Git Bash, MSYS) without symlink privileges: falls back
# to file copy. After a plugin update, re-run activate.sh to refresh.
set -euo pipefail

RULES_DIR="${1:-.claude/rules}"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$RULES_DIR"
mode="symlinked"
for rule in "$PLUGIN_DIR/rules"/*.md; do
  [ -e "$rule" ] || continue
  target="$RULES_DIR/$(basename "$rule")"
  rm -f "$target"
  if ln -s "$rule" "$target" 2>/dev/null && [ -L "$target" ]; then
    :  # real symlink created
  else
    # Symlink unsupported on this platform; fall back to copy.
    cp -f "$rule" "$target"
    mode="copied"
  fi
done
echo "$mode rule(s) into $RULES_DIR. Claude Code will load them at next session start."
if [ "$mode" = "copied" ]; then
  echo "Note: copies, not symlinks (your platform doesn't allow symlinks here)."
  echo "      Re-run activate.sh after a plugin update to refresh."
fi
"""


# ───────────────────────── loaders + helpers ─────────────────────────────────

def load_toml(path: Path) -> dict[str, Any]:
    with open(path, "rb") as f:
        return tomllib.load(f)


def parse_frontmatter(path: Path) -> dict[str, str]:
    """Extract simple key:value pairs from a markdown YAML frontmatter block."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fm_text = text[4:end]
    result: dict[str, str] = {}
    for raw in fm_text.splitlines():
        if not raw or raw.startswith("#") or raw.startswith(" ") or raw.startswith("\t"):
            continue
        if ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def make_author(mp: dict) -> dict[str, str]:
    return {"name": mp["owner"]["name"], "url": mp["owner"]["url"]}


def make_plugin_json(
    *,
    name: str,
    description: str,
    mp: dict,
    extra_keys: dict | None = None,
    rel_homepage: str | None = None,
) -> dict:
    """Construct a plugin.json dict with marketplace-inherited identity."""
    rel_homepage = rel_homepage or f"_generated/{name}"
    out = {
        "name": name,
        "description": description,
        "version": mp["marketplace"]["version"],
        "author": make_author(mp),
        "homepage": f"{mp['repository']['url']}/tree/main/{rel_homepage}",
        "repository": mp["repository"]["url"],
        "license": mp["repository"]["license"],
    }
    if extra_keys:
        out.update(extra_keys)
    return out


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str, *, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)


# ───────────────────────── source enumeration ────────────────────────────────

def list_skills() -> list[Path]:
    return sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


def list_rules() -> list[Path]:
    return sorted(d for d in RULES_DIR.iterdir() if d.is_dir() and (d / "rule.md").exists())


def list_examples() -> list[Path]:
    if not EXAMPLES_DIR.exists():
        return []
    return sorted(d for d in EXAMPLES_DIR.iterdir() if d.is_dir() and (d / ".claude-plugin" / "plugin.json").exists())


# ───────────────────────── generators ────────────────────────────────────────

def gen_skill_plugins(mp: dict) -> list[dict]:
    """For each skill in skills/, generate _generated/skill-<name>/. Return manifest entries."""
    entries = []
    for skill_dir in list_skills():
        name = skill_dir.name
        plugin_name = f"skill-{name}"
        target = GENERATED_DIR / plugin_name
        if target.exists():
            shutil.rmtree(target)
        # Copy skill content (SKILL.md, scripts/, references/, setup.sh, README.md, ...)
        shutil.copytree(skill_dir, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        # Add plugin.json
        fm = parse_frontmatter(target / "SKILL.md")
        description = fm.get("description", name)
        plugin = make_plugin_json(
            name=plugin_name,
            description=description,
            mp=mp,
            extra_keys={"skills": ["./"], "keywords": ["skill", name]},
        )
        write_json(target / ".claude-plugin" / "plugin.json", plugin)
        entries.append({
            "name": plugin_name,
            "source": f"./_generated/{plugin_name}",
            "description": description,
            "version": mp["marketplace"]["version"],
            "author": make_author(mp),
            "category": "skill",
        })
    return entries


def gen_rule_plugins(mp: dict) -> list[dict]:
    """For each rule in rules/, generate _generated/rule-<name>/ with rules/<name>.md + activate.sh."""
    entries = []
    for rule_dir in list_rules():
        name = rule_dir.name
        plugin_name = f"rule-{name}"
        target = GENERATED_DIR / plugin_name
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        # Copy rule body into rules/<name>.md (activate.sh expects rules/*.md)
        (target / "rules").mkdir()
        shutil.copy(rule_dir / "rule.md", target / "rules" / f"{name}.md")
        # Bundle the README if present (helpful for users browsing the cache)
        if (rule_dir / "README.md").exists():
            shutil.copy(rule_dir / "README.md", target / "README.md")
        # activate.sh
        write_text(target / "activate.sh", ACTIVATE_SH_TEMPLATE, executable=True)
        # plugin.json
        description = f"Always-on rule: {name}. Install, then run activate.sh to symlink into .claude/rules/."
        plugin = make_plugin_json(
            name=plugin_name,
            description=description,
            mp=mp,
            extra_keys={"keywords": ["rule", name]},
        )
        write_json(target / ".claude-plugin" / "plugin.json", plugin)
        entries.append({
            "name": plugin_name,
            "source": f"./_generated/{plugin_name}",
            "description": description,
            "version": mp["marketplace"]["version"],
            "author": make_author(mp),
            "category": "rule",
        })
    return entries


def gen_skill_bundles(mp: dict, cat: dict) -> list[dict]:
    """For each skill_domain, generate _generated/skills-<domain>/ as dep-only plugin."""
    entries = []
    for dname, dconf in cat.get("skill_domain", {}).items():
        plugin_name = f"skills-{dname}"
        target = GENERATED_DIR / plugin_name
        if target.exists():
            shutil.rmtree(target)
        deps = [f"skill-{m}" for m in dconf.get("members", [])]
        description = dconf.get("description", dname)
        plugin = make_plugin_json(
            name=plugin_name,
            description=description,
            mp=mp,
            extra_keys={
                "dependencies": deps,
                "keywords": ["bundle", "skills", dname],
            },
        )
        write_json(target / ".claude-plugin" / "plugin.json", plugin)
        entries.append({
            "name": plugin_name,
            "source": f"./_generated/{plugin_name}",
            "description": description,
            "version": mp["marketplace"]["version"],
            "author": make_author(mp),
            "category": "skill-bundle",
        })
    return entries


def gen_rule_bundles(mp: dict, cat: dict) -> list[dict]:
    """For each rule_domain, generate _generated/rules-<domain>/ as dep-only plugin."""
    entries = []
    for dname, dconf in cat.get("rule_domain", {}).items():
        plugin_name = f"rules-{dname}"
        target = GENERATED_DIR / plugin_name
        if target.exists():
            shutil.rmtree(target)
        deps = [f"rule-{m}" for m in dconf.get("members", [])]
        description = dconf.get("description", dname) + " (auto-installs member rule plugins; each requires activate.sh to apply)"
        plugin = make_plugin_json(
            name=plugin_name,
            description=description,
            mp=mp,
            extra_keys={
                "dependencies": deps,
                "keywords": ["bundle", "rules", dname],
            },
        )
        write_json(target / ".claude-plugin" / "plugin.json", plugin)
        entries.append({
            "name": plugin_name,
            "source": f"./_generated/{plugin_name}",
            "description": description,
            "version": mp["marketplace"]["version"],
            "author": make_author(mp),
            "category": "rule-bundle",
        })
    return entries


def gen_rules_all(mp: dict) -> dict:
    """Catch-all bundle depending on every individual rule plugin."""
    plugin_name = "rules-all"
    target = GENERATED_DIR / plugin_name
    if target.exists():
        shutil.rmtree(target)
    deps = [f"rule-{r.name}" for r in list_rules()]
    description = "Every rule in this marketplace, bundled. Auto-installs all rule plugins; each requires activate.sh to apply, or use activate-installed-rules.sh at the repo root."
    plugin = make_plugin_json(
        name=plugin_name,
        description=description,
        mp=mp,
        extra_keys={
            "dependencies": deps,
            "keywords": ["bundle", "rules", "all"],
        },
    )
    write_json(target / ".claude-plugin" / "plugin.json", plugin)
    return {
        "name": plugin_name,
        "source": f"./_generated/{plugin_name}",
        "description": description,
        "version": mp["marketplace"]["version"],
        "author": make_author(mp),
        "category": "rule-bundle",
    }


def gen_example_entries(mp: dict) -> list[dict]:
    """Examples already contain their own .claude-plugin/plugin.json. Just index them."""
    entries = []
    for ex_dir in list_examples():
        pj = json.loads((ex_dir / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        entries.append({
            "name": pj["name"],
            "source": f"./examples/{ex_dir.name}",
            "description": pj.get("description", ex_dir.name),
            "version": pj.get("version", mp["marketplace"]["version"]),
            "author": pj.get("author", make_author(mp)),
            "category": "example",
        })
    return entries


def gen_marketplace_json(mp: dict, all_entries: list[dict]) -> None:
    data = {
        "name": mp["marketplace"]["name"],
        "owner": mp["owner"],
        "description": mp["marketplace"]["description"],
        "homepage": mp["repository"]["homepage"],
        "repository": mp["repository"]["url"],
        "metadata": {
            "description": mp["marketplace"]["description"],
            "version": mp["marketplace"]["version"],
        },
        "plugins": all_entries,
    }
    write_json(MARKETPLACE_JSON, data)


def gen_cross_platform_mirrors() -> None:
    """Materialize directories users on non-Claude-Code platforms can point at directly."""
    # Wipe all mirror roots to start clean
    for path in MIRRORS.values():
        if path.exists():
            shutil.rmtree(path)

    # Skill mirrors: copy each skills/<name>/ into .codex/skills/<name>/, .gemini/skills/<name>/, .devin/skills/<name>/
    for platform in ("codex", "gemini", "devin"):
        target_root = MIRRORS[platform] / "skills"
        target_root.mkdir(parents=True, exist_ok=True)
        for skill_dir in list_skills():
            shutil.copytree(
                skill_dir,
                target_root / skill_dir.name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )

    # Rule mirrors for cursor + windsurf: copy each rule's formats/<platform>.md → .<platform>/rules/<name>.md
    for platform in ("cursor", "windsurf"):
        target_root = MIRRORS[platform] / "rules"
        target_root.mkdir(parents=True, exist_ok=True)
        for rule_dir in list_rules():
            fmt_file = rule_dir / "formats" / f"{platform}.md"
            if fmt_file.exists():
                shutil.copy(fmt_file, target_root / f"{rule_dir.name}.md")
            else:
                # Fallback: copy the plain rule.md
                shutil.copy(rule_dir / "rule.md", target_root / f"{rule_dir.name}.md")

    # Devin gets rules appended via AGENTS.md format (just copy the raw rule.md files for now)
    devin_rules = MIRRORS["devin"] / "rules"
    devin_rules.mkdir(parents=True, exist_ok=True)
    for rule_dir in list_rules():
        shutil.copy(rule_dir / "rule.md", devin_rules / f"{rule_dir.name}.md")


# ───────────────────────── --check mode ──────────────────────────────────────

def snapshot_tree(root: Path) -> dict[str, bytes]:
    """Return {relative_path_str: content_bytes} for every file under root."""
    if not root.exists():
        return {}
    out: dict[str, bytes] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(REPO_ROOT))] = p.read_bytes()
    return out


def check_drift() -> int:
    """Snapshot current outputs, regenerate to a temp tree, diff. Return exit code."""
    import tempfile

    # Snapshot current state
    targets = [GENERATED_DIR, MARKETPLACE_JSON.parent] + list(MIRRORS.values())
    before: dict[str, bytes] = {}
    for t in targets:
        before.update(snapshot_tree(t))

    # Regenerate to actual locations (we'll diff after)
    write_all()

    after: dict[str, bytes] = {}
    for t in targets:
        after.update(snapshot_tree(t))

    if before == after:
        print("OK: generated content matches committed content.")
        return 0

    # Report differences
    missing = sorted(set(before) - set(after))
    added = sorted(set(after) - set(before))
    changed = sorted(p for p in (set(before) & set(after)) if before[p] != after[p])

    print("DRIFT detected. Run `uv run scripts/generate_manifest.py` and commit the result.")
    for p in missing:
        print(f"  removed:  {p}")
    for p in added:
        print(f"  added:    {p}")
    for p in changed:
        print(f"  changed:  {p}")
    return 1


# ───────────────────────── orchestration ─────────────────────────────────────

def write_all() -> None:
    mp = load_toml(MARKETPLACE_TOML)
    cat = load_toml(CATALOG_TOML)

    # Clear and regenerate the _generated/ tree completely
    if GENERATED_DIR.exists():
        shutil.rmtree(GENERATED_DIR)
    GENERATED_DIR.mkdir()

    # Build per-construct outputs and collect manifest entries
    entries: list[dict] = []
    entries += gen_skill_plugins(mp)
    entries += gen_rule_plugins(mp)
    entries += gen_skill_bundles(mp, cat)
    entries += gen_rule_bundles(mp, cat)
    entries.append(gen_rules_all(mp))
    entries += gen_example_entries(mp)

    # Sort entries for deterministic output: category first, then name
    entries.sort(key=lambda e: (e.get("category", ""), e["name"]))

    gen_marketplace_json(mp, entries)
    gen_cross_platform_mirrors()

    print(f"Generated {len(entries)} plugin entries in marketplace.json")
    print(f"  Skills:        {sum(1 for e in entries if e['category'] == 'skill')}")
    print(f"  Skill bundles: {sum(1 for e in entries if e['category'] == 'skill-bundle')}")
    print(f"  Rules:         {sum(1 for e in entries if e['category'] == 'rule')}")
    print(f"  Rule bundles:  {sum(1 for e in entries if e['category'] == 'rule-bundle')}")
    print(f"  Examples:      {sum(1 for e in entries if e['category'] == 'example')}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Exit non-zero if generated content differs from what's already committed")
    args = parser.parse_args()

    if args.check:
        return check_drift()
    write_all()
    return 0


if __name__ == "__main__":
    sys.exit(main())
