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
  - commands/, agents/, hooks/, mcp-servers/, lsp-servers/, monitors/,
    output-styles/, themes/     (other construct source directories)
    Each construct directory may contain example-<type>/ subdirectories
    (the reference fixtures) as well as real plugins.

Writes:
  - .claude-plugin/marketplace.json
  - _generated/skill-<name>/    (per-skill plugin wrapper)
  - _generated/rule-<name>/     (per-rule plugin wrapper + activate.sh)
  - _generated/skills-<domain>/ (dep-only skill bundle plugin)
  - _generated/rules-<domain>/  (dep-only rule bundle plugin)
  - _generated/rules-all/       (catch-all rule bundle plugin)
  - _generated/<construct>s-examples/  (dep-only example bundle for each construct)
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
GENERATED_DIR = REPO_ROOT / "_generated"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
GEMINI_EXTENSION_JSON = REPO_ROOT / ".gemini" / "gemini-extension.json"

# Cross-platform mirror roots
MIRRORS = {
    "codex":    REPO_ROOT / ".codex",
    "gemini":   REPO_ROOT / ".gemini",
    "cursor":   REPO_ROOT / ".cursor",
    "windsurf": REPO_ROOT / ".windsurf",
    "devin":    REPO_ROOT / ".devin",
}

# Map from catalog construct key → the domain table key in catalog.toml
# e.g. "output-style" uses "output_style_domain" (hyphens become underscores)
def _domain_table_key(construct_key: str) -> str:
    return construct_key.replace("-", "_") + "_domain"


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
    return sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists() and not d.name.startswith("example-"))


def list_rules() -> list[Path]:
    return sorted(d for d in RULES_DIR.iterdir() if d.is_dir() and (d / "rule.md").exists() and not d.name.startswith("example-"))


def list_examples_by_construct(cat: dict) -> dict[str, list[Path]]:
    """
    For each construct type defined in catalog.toml, look up the example directory
    path from [construct.<type>].example_directory and return a mapping:
      { construct_key: [Path, ...] }
    Each path is expected to have a .claude-plugin/plugin.json.
    """
    result: dict[str, list[Path]] = {}
    for ckey, cconf in cat.get("construct", {}).items():
        ex_dir_str = cconf.get("example_directory", "")
        if not ex_dir_str:
            result[ckey] = []
            continue
        ex_dir = REPO_ROOT / ex_dir_str
        if ex_dir.is_dir() and (ex_dir / ".claude-plugin" / "plugin.json").exists():
            result[ckey] = [ex_dir]
        else:
            result[ckey] = []
    return result


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
    """For each skill_domain (excluding 'examples'), generate _generated/skills-<domain>/ as dep-only plugin."""
    entries = []
    for dname, dconf in cat.get("skill_domain", {}).items():
        if dname == "examples":
            continue
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
    """For each rule_domain (excluding 'examples'), generate _generated/rules-<domain>/ as dep-only plugin."""
    entries = []
    for dname, dconf in cat.get("rule_domain", {}).items():
        if dname == "examples":
            continue
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


def gen_example_bundles(mp: dict, cat: dict) -> list[dict]:
    """
    For each [<construct>_domain.examples] entry in catalog.toml, emit:
      1. A manifest entry pointing at the native source directory for the example
         plugin (the example already has its own .claude-plugin/plugin.json).
      2. A dep-only bundle plugin _generated/<construct>s-examples/ that depends
         on the example plugin name.

    The example plugins live in their native construct folders (skills/example-skill/,
    rules/example-rule/, etc.) and already have their own .claude-plugin/plugin.json,
    so we index them directly rather than generating wrappers.
    """
    entries = []

    # Build a reverse map: construct_key -> source_directory from catalog
    construct_source: dict[str, str] = {}
    construct_prefix: dict[str, str] = {}
    construct_bundle_prefix: dict[str, str] = {}
    for ckey, cconf in cat.get("construct", {}).items():
        construct_source[ckey] = cconf.get("source_directory", "").rstrip("/")
        construct_prefix[ckey] = cconf.get("prefix_individual", f"{ckey}-")
        construct_bundle_prefix[ckey] = cconf.get("prefix_domain", f"{ckey}s-")

    # Iterate all construct keys and check for a <construct>_domain.examples table
    for ckey in cat.get("construct", {}):
        domain_table = _domain_table_key(ckey)
        domain_data = cat.get(domain_table, {})
        examples_domain = domain_data.get("examples")
        if not examples_domain:
            continue

        members = examples_domain.get("members", [])
        description = examples_domain.get("description", f"Reference example for {ckey}")
        src_dir_rel = construct_source.get(ckey, "")
        ind_prefix = construct_prefix.get(ckey, f"{ckey}-")
        bundle_prefix = construct_bundle_prefix.get(ckey, f"{ckey}s-")

        # Emit one manifest entry per example member (direct source reference)
        example_plugin_names = []
        for member in members:
            member_path = REPO_ROOT / src_dir_rel / member
            if not (member_path / ".claude-plugin" / "plugin.json").exists():
                continue
            pj = json.loads((member_path / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
            plugin_name = pj["name"]
            example_plugin_names.append(plugin_name)
            entries.append({
                "name": plugin_name,
                "source": f"./{src_dir_rel}/{member}",
                "description": pj.get("description", member),
                "version": pj.get("version", mp["marketplace"]["version"]),
                "author": pj.get("author", make_author(mp)),
                "category": "example",
            })

        # Emit one dep-only bundle plugin: <construct>s-examples
        if example_plugin_names:
            bundle_name = f"{bundle_prefix}examples"
            target = GENERATED_DIR / bundle_name
            if target.exists():
                shutil.rmtree(target)
            plugin = make_plugin_json(
                name=bundle_name,
                description=description,
                mp=mp,
                extra_keys={
                    "dependencies": example_plugin_names,
                    "keywords": ["bundle", "examples", ckey],
                },
            )
            write_json(target / ".claude-plugin" / "plugin.json", plugin)
            entries.append({
                "name": bundle_name,
                "source": f"./_generated/{bundle_name}",
                "description": description,
                "version": mp["marketplace"]["version"],
                "author": make_author(mp),
                "category": "example-bundle",
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


def gen_gemini_extension_json(mp: dict) -> None:
    """Produce .gemini/gemini-extension.json for gemini extensions validate.

    The gemini-extension.json format requires only `name` and `version`.
    We write it into .gemini/ (the existing Gemini mirror directory) so that
    generated content stays under the mirror dir rather than polluting repo root.
    The compat-extension.yml workflow runs: gemini extensions validate ./.gemini/

    Minimum required fields verified empirically with gemini 0.43.0 (2026-05-22):
      - name    (string)
      - version (string)
    Optional fields include description, mcpServers, skills, themes, etc.
    """
    data = {
        "name": mp["marketplace"]["name"],
        "version": mp["marketplace"]["version"],
        "description": mp["marketplace"]["description"],
    }
    write_json(GEMINI_EXTENSION_JSON, data)


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
    entries += gen_example_bundles(mp, cat)

    # Sort entries for deterministic output: category first, then name
    entries.sort(key=lambda e: (e.get("category", ""), e["name"]))

    gen_marketplace_json(mp, entries)
    gen_cross_platform_mirrors()
    gen_gemini_extension_json(mp)

    print(f"Generated {len(entries)} plugin entries in marketplace.json")
    print(f"  Skills:          {sum(1 for e in entries if e['category'] == 'skill')}")
    print(f"  Skill bundles:   {sum(1 for e in entries if e['category'] == 'skill-bundle')}")
    print(f"  Rules:           {sum(1 for e in entries if e['category'] == 'rule')}")
    print(f"  Rule bundles:    {sum(1 for e in entries if e['category'] == 'rule-bundle')}")
    print(f"  Examples:        {sum(1 for e in entries if e['category'] == 'example')}")
    print(f"  Example bundles: {sum(1 for e in entries if e['category'] == 'example-bundle')}")


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
