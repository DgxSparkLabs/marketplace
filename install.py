# /// script
# requires-python = ">=3.11"
# dependencies = ["textual>=1.0.0"]
# ///
"""
Marketplace interactive installer — install and uninstall agent tools.

Usage:
    uv run install.py                    # interactive mode
    uv run install.py --uninstall        # uninstall mode
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import os
import shutil
import tomllib
from pathlib import Path

# ── Catalog Loader ──────────────────────────────────────────────────────────
# All TUI configuration lives in catalog.toml next to this script.

def _load_catalog() -> dict:
    """Load catalog.toml from the marketplace root."""
    path = Path(__file__).parent.resolve() / "catalog.toml"
    if not path.exists():
        return {}
    with open(path, "rb") as f:
        return tomllib.load(f)


def _build_platforms(catalog: dict) -> dict:
    """Convert catalog TOML platforms into the runtime PLATFORMS dict."""
    platforms = {}
    for pid, p in catalog.get("platforms", {}).items():
        platforms[pid] = {
            "label": p["label"],
            "global": {
                "config": Path(p["global_config"]).expanduser(),
                "rules": Path(p["global_rules"]).expanduser() if p.get("global_rules") else None,
                "skills": Path(p["global_skills"]).expanduser() if p.get("global_skills") else None,
            },
            "project": {
                "config": Path(p["project_config"]),
                "rules": Path(p["project_rules"]),
                "skills": Path(p["project_skills"]) if p.get("project_skills") else None,
            },
            "rule_fmt": p["rule_format"],
        }
    return platforms


def _build_mcp_servers(catalog: dict) -> dict:
    """Convert catalog TOML mcp_servers into the runtime dict."""
    servers = {}
    for name, s in catalog.get("mcp_servers", {}).items():
        servers[name] = {
            "description": s.get("description", ""),
            "config": s.get("config", {}),
        }
    return servers


def _build_families(catalog: dict, key: str) -> dict:
    """Convert catalog TOML families (skill_families / rule_families)."""
    families = {}
    for fname, f in catalog.get(key, {}).items():
        families[fname] = {
            "icon": f.get("icon", "\u2022"),
            "description": f.get("description", ""),
            "members": f.get("members", []),
        }
    return families


_CATALOG = _load_catalog()
PLATFORMS = _build_platforms(_CATALOG)
MCP_SERVERS = _build_mcp_servers(_CATALOG)
SKILL_FAMILIES = _build_families(_CATALOG, "skill_families")
RULE_FAMILIES = _build_families(_CATALOG, "rule_families")
SKILLS_DISABLED_BY_DEFAULT: set[str] = set(_CATALOG.get("skills_disabled_by_default", []))
WORKSPACE_SCOPE_DEFAULTS: set[str] = set(_CATALOG.get("workspace_scope_defaults", []))


# ── Detection Helpers ───────────────────────────────────────────────────────

def detect_platforms() -> dict[str, dict]:
    found = {}
    for pid, info in PLATFORMS.items():
        if info["global"]["config"].parent.exists():
            found[pid] = info
    return found


def read_mcp_servers(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    try:
        data = json.loads(config_path.read_text())
        return data.get("mcpServers", {})
    except (json.JSONDecodeError, KeyError):
        return {}


def is_rule_installed(pid: str, rule_name: str, paths: dict) -> bool:
    fmt = PLATFORMS[pid]["rule_fmt"]
    target = paths["rules"]
    if not target:
        return False
    if fmt == "agents":
        if target.exists():
            content = target.read_text()
            rule_path = find_marketplace() / "rules" / rule_name / "rule.md"
            if rule_path.exists():
                for line in rule_path.read_text().splitlines():
                    if line.startswith("## "):
                        return line[3:].strip() in content
            return f"## {rule_name}" in content.lower().replace(" ", "-")
        return False
    else:
        return target.is_dir() and (target / f"{rule_name}.md").exists()


def is_skill_installed(skill_name: str, paths: dict) -> bool:
    skills_dir = paths.get("skills")
    if not skills_dir:
        return False
    return (skills_dir / skill_name).is_dir()


# ── Scan Marketplace ────────────────────────────────────────────────────────

def find_marketplace() -> Path:
    """Find marketplace root — script lives inside it."""
    return Path(__file__).parent.resolve()


def scan_rules(marketplace: Path) -> list[dict]:
    rules: list[dict] = []
    rules_dir = marketplace / "rules"
    if not rules_dir.is_dir():
        return rules
    for d in sorted(rules_dir.iterdir()):
        if not d.is_dir() or not (d / "rule.md").exists() or d.name.startswith(("_", ".")):
            continue
        desc = ""
        readme = d / "README.md"
        if readme.exists():
            for line in readme.read_text().splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith(("#", "!", "[", "|", "-", "```")):
                    desc = stripped[:80]
                    break
        formats_dir = d / "formats"
        fmts = []
        if formats_dir.is_dir():
            fmts = [f.stem for f in formats_dir.iterdir() if f.suffix == ".md"]
        rules.append({"name": d.name, "description": desc, "path": d, "formats": fmts})
    return rules


def scan_skills(marketplace: Path) -> list[dict]:
    skills: list[dict] = []
    skills_dir = marketplace / "skills"
    if not skills_dir.is_dir():
        return skills
    for d in sorted(skills_dir.iterdir()):
        if not d.is_dir() or not (d / "SKILL.md").exists() or d.name.startswith(("_", ".")):
            continue
        desc = ""
        for line in (d / "SKILL.md").read_text().splitlines():
            if line.strip().startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip("\"'")[:80]
                break
        skills.append({"name": d.name, "description": desc, "path": d})
    return skills


# ── Install Logic ───────────────────────────────────────────────────────────

def install_mcp(name: str, server: dict, config_path: Path) -> str:
    existing = {}
    if config_path.exists():
        try:
            existing = json.loads(config_path.read_text())
        except json.JSONDecodeError:
            existing = {}
    servers = existing.setdefault("mcpServers", {})
    if name in servers:
        return "already installed"
    servers[name] = server["config"]
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(existing, indent=2) + "\n")
    return "installed"


def uninstall_mcp(name: str, config_path: Path) -> str:
    if not config_path.exists():
        return "not found"
    try:
        data = json.loads(config_path.read_text())
    except json.JSONDecodeError:
        return "config unreadable"
    servers = data.get("mcpServers", {})
    if name not in servers:
        return "not installed"
    del servers[name]
    config_path.write_text(json.dumps(data, indent=2) + "\n")
    return "removed"


def install_rule(rule: dict, pid: str, paths: dict) -> str:
    fmt = PLATFORMS[pid]["rule_fmt"]
    target = paths["rules"]
    if not target:
        return "not supported"

    if fmt == "agents":
        content = (rule["path"] / "rule.md").read_text()
        title = ""
        for line in content.splitlines():
            if line.startswith("## "):
                title = line[3:].strip()
                break
        if target.exists() and title and title in target.read_text():
            return "already installed"
        target.parent.mkdir(parents=True, exist_ok=True)
        needs_separator = target.exists() and target.stat().st_size > 0
        with open(target, "a") as f:
            if needs_separator:
                f.write("\n")
            f.write(content)
        return "installed"
    else:
        src = rule["path"] / "formats" / f"{fmt}.md"
        if not src.exists():
            return f"no {fmt} format"
        target.mkdir(parents=True, exist_ok=True)
        dest = target / f"{rule['name']}.md"
        if dest.exists() and dest.read_text() == src.read_text():
            return "already installed"
        shutil.copy2(src, dest)
        return "installed"


def uninstall_rule(rule: dict, pid: str, paths: dict) -> str:
    fmt = PLATFORMS[pid]["rule_fmt"]
    target = paths["rules"]
    if not target:
        return "not supported"

    if fmt == "agents":
        if not target.exists():
            return "not found"
        content = target.read_text()
        rule_content = (rule["path"] / "rule.md").read_text().strip()
        title = ""
        for line in rule_content.splitlines():
            if line.startswith("## "):
                title = line.strip()
                break
        if not title or title not in content:
            return "not installed"
        lines = content.splitlines(keepends=True)
        new_lines: list[str] = []
        skipping = False
        for line in lines:
            if line.strip() == title:
                skipping = True
                if new_lines and new_lines[-1].strip() == "":
                    new_lines.pop()
                continue
            if skipping and line.startswith("## "):
                skipping = False
            if not skipping:
                new_lines.append(line)
        target.write_text("".join(new_lines))
        return "removed"
    else:
        rule_file = target / f"{rule['name']}.md"
        if not rule_file.exists():
            return "not installed"
        rule_file.unlink()
        return "removed"


def install_skill(skill: dict, skills_dir: Path) -> str:
    if not skills_dir:
        return "not supported"
    skills_dir.mkdir(parents=True, exist_ok=True)
    dest = skills_dir / skill["name"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(skill["path"], dest)
    return "installed"


def uninstall_skill(skill_name: str, skills_dir: Path) -> str:
    if not skills_dir:
        return "not supported"
    dest = skills_dir / skill_name
    if not dest.exists():
        return "not installed"
    shutil.rmtree(dest)
    return "removed"


# ── Path Resolution ─────────────────────────────────────────────────────────

def resolve_paths(pid: str, scope: str, workspace_dir: str | None = None) -> dict:
    """Get install paths for a platform, resolving workspace paths."""
    info = PLATFORMS[pid]
    if scope == "global":
        return dict(info["global"])
    if workspace_dir:
        base = Path(workspace_dir).expanduser().resolve()
    else:
        base = Path.cwd()
    project = {}
    for key, val in info["project"].items():
        project[key] = base / val if val else None
    return project


def _resolve_user_path(path_str: str) -> Path:
    """Resolve a user-typed path, handling ~, ., .., and symlinks."""
    if not path_str:
        return Path.cwd()
    return Path(path_str).expanduser().resolve()


# ── UI Helpers ──────────────────────────────────────────────────────────────

def status_badge(installed: bool) -> str:
    return "[green]installed[/green]" if installed else "[dim]not installed[/dim]"


def action_badge(result: str) -> str:
    if result in ("installed", "removed"):
        return f"[green]{result}[/green]"
    if result in ("already installed", "not installed", "not found"):
        return f"[dim]{result}[/dim]"
    return f"[yellow]{result}[/yellow]"


# ── TUI ─────────────────────────────────────────────────────────────────────

APP_CSS = """
Screen {
    background: $surface;
}

#banner {
    width: 100%;
    height: 10;
    content-align: center middle;
    text-align: left;
    padding: 0 2;
    background: $panel;
    color: $primary;
}

#main-area {
    height: 1fr;
    margin: 0;
}

#left-panel {
    width: 2fr;
    border: round $primary 30%;
    padding: 0 1;
    background: $surface;
    overflow-y: auto;
}

#right-panel {
    width: 1fr;
    border: round $secondary 30%;
    padding: 1 1;
    background: $surface;
}

SelectionList {
    height: auto;
    max-height: 20;
    border: none;
    margin: 0 0 0 1;
    padding: 0;
    background: transparent;
}

SelectionList:focus {
    border: none;
}

SelectionList > .selection-list--button {
    background: transparent;
}

SelectionList:focus > .selection-list--button-highlighted {
    background: $boost;
}

SelectionList > .selection-list--button-highlighted {
    background: $surface;
}

SelectionList > .selection-list--button-selected {
    color: $success;
}

Collapsible {
    padding: 0 0 0 1;
    margin: 0;
    background: transparent;
    border: none;
}

CollapsibleTitle {
    padding: 0;
    color: $text-muted;
    text-style: italic;
    width: 100%;
    background: transparent;
}

CollapsibleTitle:hover {
    color: $primary;
    text-style: bold italic;
}

CollapsibleTitle:focus {
    color: $primary;
    text-style: bold;
}

Collapsible.section-collapsible {
    padding: 0;
    margin: 1 0 0 0;
}

Collapsible.section-collapsible > CollapsibleTitle {
    text-style: bold;
    padding: 0;
    background: transparent;
}

#section-platforms > CollapsibleTitle {
    color: dodgerblue;
}

#section-scope > CollapsibleTitle {
    color: green;
}

#section-mcps > CollapsibleTitle {
    color: red;
}

#section-rules > CollapsibleTitle {
    color: yellow;
}

#section-skills > CollapsibleTitle {
    color: mediumpurple;
}

Collapsible.section-collapsible > CollapsibleTitle:hover {
    text-style: bold;
}

Collapsible.section-collapsible > CollapsibleTitle:focus {
    text-style: bold reverse;
}

#preview-body {
    padding: 1 0;
    color: $text;
}

#status-bar {
    dock: bottom;
    height: 1;
    background: $panel;
    color: $text-muted;
    text-align: center;
    padding: 0 2;
}

Footer {
    background: $panel;
}

Footer > .footer--key {
    background: $surface;
    color: $primary;
}

Footer > .footer--description {
    color: $text-muted;
}

/* Workspace entries */
#workspace-paths-label {
    margin: 0 0 0 2;
    color: $text-muted;
}

#workspace-entries {
    height: auto;
    margin: 0;
}

.ws-row {
    height: auto;
    margin: 0 0 0 2;
    width: 100%;
}

.ws-path-input {
    width: 1fr;
}

.path-input-box {
    height: auto;
    width: 1fr;
}

.path-input-box Input {
    width: 100%;
}

.path-dropdown {
    height: auto;
    max-height: 16;
    display: none;
    border: tall $primary 40%;
    background: $surface;
    padding: 0;
    margin: 0;
    scrollbar-size: 1 1;
}

.path-dropdown.visible {
    display: block;
}

.path-dropdown:focus {
    border: tall $primary;
}

.ws-browse-btn {
    width: auto;
    min-width: 10;
    margin: 0 0 0 1;
}

.ws-remove-btn {
    width: auto;
    min-width: 5;
    margin: 0 0 0 1;
    color: $error;
}

#ws-add-btn {
    margin: 1 0 0 2;
    width: auto;
}

/* Modal screens */
ConfirmScreen, PreviewScreen, ResultsScreen, PathPickerScreen {
    align: center middle;
}

#confirm-dialog {
    width: 70;
    max-height: 80%;
    border: heavy $primary;
    background: $surface;
    padding: 1 2;
}

#preview-dialog {
    width: 90%;
    height: 90%;
    border: heavy $secondary;
    background: $surface;
    padding: 1 2;
}

#results-dialog {
    width: 80%;
    max-height: 90%;
    border: heavy $success;
    background: $surface;
    padding: 1 2;
}

#path-picker-dialog {
    width: 80%;
    height: 70%;
    border: heavy $primary;
    background: $surface;
    padding: 1 2;
}

#path-tree {
    height: 1fr;
    margin: 1 0;
}

#modal-title {
    text-align: center;
    text-style: bold;
    padding: 0 0 1 0;
    color: $primary;
    width: 100%;
}

#modal-body {
    height: 1fr;
    overflow-y: auto;
    padding: 1 1;
    color: $text;
}

#modal-actions {
    height: 3;
    align: center middle;
    layout: horizontal;
    padding: 1 0 0 0;
}

.modal-btn {
    margin: 0 2;
}

.btn-install {
    background: $success;
    color: $text;
    text-style: bold;
}

.btn-install:hover {
    background: $success-darken-1;
}

.btn-cancel {
    background: $surface;
    color: $text;
}

.btn-cancel:hover {
    background: $panel;
}

.btn-close {
    background: $surface;
    color: $text;
}

.btn-done {
    background: $success;
    color: $text;
    text-style: bold;
}

.empty-notice {
    margin: 1 0 0 2;
    color: $text-muted;
    text-style: italic;
}
"""

# ── 3D Wireframe Data ───────────────────────────────────────────────────────

_CUBE_V = [
    (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
    (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1),
]
_CUBE_E = [
    (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
    (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7),
]
_OCT_V = [
    (1.4, 0, 0), (-1.4, 0, 0), (0, 1.4, 0),
    (0, -1.4, 0), (0, 0, 1.4), (0, 0, -1.4),
]
_OCT_E = [
    (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3),
    (1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5),
]
_BRAILLE = [
    (0, 0, 0x01), (1, 0, 0x02), (2, 0, 0x04), (3, 0, 0x40),
    (0, 1, 0x08), (1, 1, 0x10), (2, 1, 0x20), (3, 1, 0x80),
]
_GEO_TEXT = [
    "",
    "  [bold bright_cyan]\u2554\u2550\u2557 \u2566 \u2566 \u2566 \u2566   \u2566   \u2554\u2550\u2557[/]",
    "  [bold cyan]\u255a\u2550\u2557 \u2560\u2569\u2557 \u2551 \u2551   \u2551   \u255a\u2550\u2557[/]",
    "  [bold deep_sky_blue1]\u255a\u2550\u255d \u2569 \u2569 \u2569 \u2569\u2550\u255d \u2569\u2550\u255d \u255a\u2550\u255d[/]",
    "",
    "  [bold medium_purple1]\u2554\u2566\u2557 \u2554\u2550\u2557 \u2566\u2550\u2557 \u2566 \u2566 \u2554\u2550\u2557 \u2554\u2566\u2557[/]",
    "  [bold medium_purple1]\u2551\u2551\u2551 \u2560\u2550\u2563 \u2560\u2566\u255d \u2560\u2569\u2557 \u2551\u2563   \u2551[/]",
    "  [bold blue]\u2569 \u2569 \u2569 \u2569 \u2569\u255a\u2550 \u2569 \u2569 \u255a\u2550\u255d  \u2569[/]",
    "  [dim]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500[/]",
    "  [bold deep_sky_blue1]\u2726[/] [bold white]Agent Tools Installer[/] [bold deep_sky_blue1]\u2726[/]",
]


def _categorize_items(items: list[dict], families: dict) -> dict:
    """Assign items to their family groups. Uncategorized go to 'Other'."""
    member_map = {}
    for fname, fdata in families.items():
        for m in fdata["members"]:
            member_map[m] = fname

    result = {fname: {**fdata, "items": []} for fname, fdata in families.items()}
    other_items = []
    for item in items:
        family = member_map.get(item["name"])
        if family and family in result:
            result[family]["items"].append(item)
        else:
            other_items.append(item)

    if other_items:
        result["Other"] = {
            "icon": "\u2022",
            "description": "Uncategorized items",
            "members": [],
            "items": other_items,
        }
    return result


def _read_item_content(item: dict, item_type: str) -> str:
    """Read the full content of a skill or rule for preview."""
    path = item.get("path")
    if not path:
        return "No content available."
    if item_type == "skill":
        skill_md = path / "SKILL.md"
        if skill_md.exists():
            return skill_md.read_text()
    elif item_type == "rule":
        rule_md = path / "rule.md"
        if rule_md.exists():
            return rule_md.read_text()
        readme = path / "README.md"
        if readme.exists():
            return readme.read_text()
    return "No content available."


# ── Path Autocomplete ───────────────────────────────────────────────────────

def _get_path_completions(partial: str) -> list[str]:
    """Return directory completions for a partial path string."""
    if not partial:
        return []
    uses_tilde = partial.startswith("~")
    home_str = str(Path.home())
    try:
        expanded = str(Path(partial).expanduser()) if uses_tilde else partial
    except RuntimeError:
        return []
    p = Path(expanded)
    try:
        if p.is_dir():
            parent = p.resolve()
            prefix = ""
        else:
            parent = p.parent.resolve()
            prefix = p.name
        if not parent.is_dir():
            return []
        entries: list[str] = []
        if not prefix:
            current = str(parent) + os.sep
            if uses_tilde and current.startswith(home_str):
                current = "~" + current[len(home_str):]
            entries.append(current)
        for child in sorted(parent.iterdir()):
            if child.name.startswith("."):
                continue
            if not child.is_dir():
                continue
            if prefix and not child.name.startswith(prefix):
                continue
            resolved = str(child.resolve()) + os.sep
            if uses_tilde and resolved.startswith(home_str):
                resolved = "~" + resolved[len(home_str):]
            entries.append(resolved)
        return entries
    except PermissionError:
        return []


# ── TUI App ─────────────────────────────────────────────────────────────────

def main():
    from textual import on
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Horizontal, Vertical, VerticalScroll
    from textual.screen import ModalScreen
    from textual.widgets import (
        Button, Collapsible, DirectoryTree, Footer, Header, Input,
        Markdown, OptionList, SelectionList, Static,
    )
    from textual.widgets.selection_list import Selection
    from rich.text import Text

    # ── Characters forbidden in a single path ──
    _PATH_REJECT = set(",;|\t\n\r")

    # ── Click-to-focus SelectionList ──
    class MarketplaceList(SelectionList):
        """First click on a new item only highlights it; second click or
        Enter/Space toggles selection."""

        _mouse_down_idx: int | None = None
        _is_mouse_toggle: bool = False

        def on_mouse_down(self, event) -> None:
            self._mouse_down_idx = self.highlighted
            self._is_mouse_toggle = True

        def _toggle_highlighted_selection(self) -> None:
            if self._is_mouse_toggle:
                self._is_mouse_toggle = False
                if self._mouse_down_idx != self.highlighted:
                    return
            super()._toggle_highlighted_selection()

    # ── Path input with dropdown autocomplete ──
    class PathInput(Vertical):
        """Input + dropdown OptionList for filesystem path completions.

        Design: focus never leaves the Input.  Arrow keys drive the
        dropdown highlight programmatically so there are no focus-
        transfer issues.  The dropdown is purely visual.
        """

        DEFAULT_CSS = """
        PathInput { height: auto; }
        """

        def __init__(self, entry_id: str, value: str = "", **kwargs):
            super().__init__(classes="path-input-box", **kwargs)
            self._entry_id = entry_id
            self._initial = value
            self._accepting = False

        def compose(self) -> ComposeResult:
            yield Input(
                value=self._initial,
                placeholder="Enter workspace path, e.g. ~/my-project",
                id=f"ws-input-{self._entry_id}",
                classes="ws-path-input",
            )
            ol = OptionList(id=f"ws-dd-{self._entry_id}", classes="path-dropdown")
            ol.can_focus = False
            yield ol

        @property
        def input(self) -> Input:
            return self.query_one(f"#ws-input-{self._entry_id}", Input)

        @property
        def dropdown(self) -> OptionList:
            return self.query_one(f"#ws-dd-{self._entry_id}", OptionList)

        @property
        def value(self) -> str:
            return self.input.value

        @value.setter
        def value(self, v: str) -> None:
            self._accepting = True
            self.input.value = v
            self.input.action_end()
            self._accepting = False

        def _refresh_dropdown(self, text: str) -> None:
            dd = self.dropdown
            dd.clear_options()
            completions = _get_path_completions(text)
            if not completions:
                dd.remove_class("visible")
                return
            for c in completions:
                dd.add_option(c)
            dd.highlighted = 0
            dd.add_class("visible")

        def _hide_dropdown(self) -> None:
            self.dropdown.remove_class("visible")

        @property
        def _dd_visible(self) -> bool:
            return self.dropdown.has_class("visible")

        def _accept_highlighted(self) -> None:
            dd = self.dropdown
            idx = dd.highlighted
            if idx is None:
                self._hide_dropdown()
                return
            try:
                opt = dd.get_option_at_index(idx)
            except Exception:
                self._hide_dropdown()
                return
            path = str(opt.prompt)
            self._accepting = True
            self.input.value = path
            self.input.action_end()
            self._accepting = False
            self._refresh_dropdown(path)

        def _move_highlight(self, delta: int) -> None:
            dd = self.dropdown
            if not self._dd_visible:
                return
            idx = dd.highlighted
            if idx is None:
                dd.highlighted = 0
                return
            new = idx + delta
            if new < 0 or new >= dd.option_count:
                return
            dd.highlighted = new
            dd.scroll_to_highlight()

        @on(Input.Changed)
        def _on_input_changed(self, event: Input.Changed) -> None:
            if self._accepting:
                return
            cleaned = "".join(c for c in event.value if c not in _PATH_REJECT)
            if cleaned != event.value:
                self._accepting = True
                self.input.value = cleaned
                self.input.action_end()
                self._accepting = False
            self._refresh_dropdown(cleaned)

        @on(OptionList.OptionSelected)
        def _on_dd_selected(self, event) -> None:
            self._accept_highlighted()
            self.input.focus()

        @on(Input.Submitted)
        def _on_input_submitted(self, event) -> None:
            if self._dd_visible:
                self._accept_highlighted()
                event.prevent_default()
                event.stop()

        def on_key(self, event) -> None:
            if not self._dd_visible:
                if event.key == "down":
                    self._refresh_dropdown(self.input.value)
                    event.prevent_default()
                    event.stop()
                return

            if event.key == "down":
                self._move_highlight(1)
                event.prevent_default()
                event.stop()
            elif event.key == "up":
                dd = self.dropdown
                if dd.highlighted is not None and dd.highlighted == 0:
                    self._hide_dropdown()
                else:
                    self._move_highlight(-1)
                event.prevent_default()
                event.stop()
            elif event.key == "escape":
                self._hide_dropdown()
                event.prevent_default()
                event.stop()
            elif event.key == "tab":
                self._accept_highlighted()
                event.prevent_default()
                event.stop()
            elif event.key == "enter":
                self._accept_highlighted()
                event.prevent_default()
                event.stop()

    # ── Directory-only tree for path picker ──
    class DirOnlyTree(DirectoryTree):
        """DirectoryTree that only shows directories, not files."""

        def filter_paths(self, paths):
            return [p for p in paths if p.is_dir()]

    # ── Animated 3D wireframe banner ──
    class AnimatedBanner(Static):
        """Spinning wireframe cube + octahedron rendered in braille."""
        _GW, _GH = 50, 40

        def on_mount(self):
            self._a = 0.0
            self._render_geo()
            self.set_interval(1 / 12, self._tick)

        def _tick(self):
            self._a += 0.05
            self._render_geo()

        @staticmethod
        def _line(g, x0, y0, x1, y1, W, H):
            dx, dy = abs(x1 - x0), abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            e = dx - dy
            while True:
                if 0 <= x0 < W and 0 <= y0 < H:
                    g[y0][x0] = True
                if x0 == x1 and y0 == y1:
                    break
                e2 = 2 * e
                if e2 > -dy:
                    e -= dy
                    x0 += sx
                if e2 < dx:
                    e += dx
                    y0 += sy

        def _render_geo(self):
            W, H = self._GW, self._GH
            g = [[False] * W for _ in range(H)]
            a = self._a
            ca, sa = math.cos(a), math.sin(a)
            cb, sb = math.cos(a * 0.7), math.sin(a * 0.7)

            def xf(x, y, z):
                x2 = x * ca - z * sa
                z2 = x * sa + z * ca
                y2 = y * cb - z2 * sb
                z3 = y * sb + z2 * cb
                return x2, y2, z3

            def pj(x, y, z):
                f = 4.0
                s = f / (z + f)
                return int(W / 2 + x * s * W / 5), int(H / 2 + y * s * H / 5)

            for edges, verts in [(_CUBE_E, _CUBE_V), (_OCT_E, _OCT_V)]:
                for i, j in edges:
                    p1, p2 = pj(*xf(*verts[i])), pj(*xf(*verts[j]))
                    self._line(g, *p1, *p2, W, H)

            blines = []
            for y in range(0, H, 4):
                row = ""
                for x in range(0, W, 2):
                    v = 0x2800
                    for dy, dx, bit in _BRAILLE:
                        if y + dy < H and x + dx < W and g[y + dy][x + dx]:
                            v |= bit
                    row += chr(v)
                blines.append(row)

            parts = []
            n = len(blines)
            for i, bl in enumerate(blines):
                hue = (a * 0.08 + i / n * 0.6) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
                rgb = f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"
                t = _GEO_TEXT[i] if i < len(_GEO_TEXT) else ""
                parts.append(f"[bold {rgb}]{bl}[/]{t}")
            self.update("\n".join(parts), layout=False)

    # Free up Space on CollapsibleTitle for section-level selection toggle.
    try:
        from textual.widgets._collapsible import CollapsibleTitle
        CollapsibleTitle.BINDINGS = [Binding("enter", "toggle", "Toggle")]
    except ImportError:
        pass

    parser = argparse.ArgumentParser(description="Marketplace interactive installer")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall mode")
    args = parser.parse_args()
    install_mode = not args.uninstall
    mode_verb = "Install" if install_mode else "Uninstall"

    platforms = detect_platforms()

    marketplace = find_marketplace()
    all_rules = scan_rules(marketplace)
    all_skills = scan_skills(marketplace)

    if not platforms and not PLATFORMS:
        from rich.console import Console
        Console().print(
            "[red]Error: No platforms configured.[/red]\n"
            "Ensure catalog.toml exists and has a [platforms] section."
        )
        raise SystemExit(1)
    primary_pid = list(platforms.keys())[0] if platforms else list(PLATFORMS.keys())[0]
    primary_paths = PLATFORMS[primary_pid]["global"]
    primary_mcps = read_mcp_servers(primary_paths["config"]) if platforms else {}

    def _is_rule_installed_any(rule_name: str) -> bool:
        """Check if a rule is installed on ANY detected platform (global scope)."""
        for pid in platforms:
            paths = PLATFORMS[pid]["global"]
            if is_rule_installed(pid, rule_name, paths):
                return True
        return False

    def _is_skill_installed_any(skill_name: str) -> bool:
        """Check if a skill is installed on ANY detected platform (global scope)."""
        for pid in platforms:
            paths = PLATFORMS[pid]["global"]
            if is_skill_installed(skill_name, paths):
                return True
        return False

    rule_families = _categorize_items(all_rules, RULE_FAMILIES)
    skill_families = _categorize_items(all_skills, SKILL_FAMILIES)

    # ── Path Picker Modal ──
    class PathPickerScreen(ModalScreen[str | None]):
        BINDINGS = [Binding("escape", "cancel", "Cancel")]

        def __init__(self, start_path: str = ""):
            super().__init__()
            self._start = start_path or str(Path.home())

        def compose(self) -> ComposeResult:
            with Vertical(id="path-picker-dialog"):
                yield Static(
                    "[bold dodger_blue2]\u2500\u2500 Select Workspace Directory \u2500\u2500[/]",
                    id="modal-title",
                )
                yield DirOnlyTree(self._start, id="path-tree")
                with Horizontal(id="modal-actions"):
                    yield Button("Select", variant="success",
                                 classes="modal-btn btn-install", id="path-select")
                    yield Button("Cancel", variant="default",
                                 classes="modal-btn btn-cancel", id="path-cancel")

        @on(Button.Pressed, "#path-select")
        def _select(self, _event) -> None:
            tree = self.query_one("#path-tree", DirOnlyTree)
            node = tree.cursor_node
            if node and node.data:
                p = node.data if isinstance(node.data, Path) else getattr(node.data, "path", None)
                if p and Path(p).is_dir():
                    self.dismiss(str(Path(p).resolve()))
                    return
            self.notify("Select a directory first", severity="warning")

        @on(Button.Pressed, "#path-cancel")
        def _cancel(self, _event=None) -> None:
            self.dismiss(None)

        def action_cancel(self) -> None:
            self.dismiss(None)

    # ── Preview Modal ──
    class PreviewScreen(ModalScreen):
        BINDINGS = [Binding("escape", "dismiss", "Close")]

        def __init__(self, title: str, content: str):
            super().__init__()
            self._title = title
            self._content = content

        def compose(self) -> ComposeResult:
            with Vertical(id="preview-dialog"):
                yield Static(
                    f"[bold medium_purple1]\u2500\u2500 {self._title} \u2500\u2500[/]",
                    id="modal-title",
                )
                yield VerticalScroll(
                    Markdown(self._content, id="preview-md"),
                    id="modal-body",
                )
                with Horizontal(id="modal-actions"):
                    yield Button("Close [Esc]", variant="default",
                                 classes="modal-btn btn-close", id="preview-close")

        @on(Button.Pressed, "#preview-close")
        def close(self, _event) -> None:
            self.dismiss()

    # ── Confirm Modal ──
    class ConfirmScreen(ModalScreen[bool]):
        BINDINGS = [Binding("escape", "cancel", "Cancel")]

        def __init__(self, summary_text: str, mode_label: str):
            super().__init__()
            self._summary = summary_text
            self._mode_label = mode_label

        def compose(self) -> ComposeResult:
            with Vertical(id="confirm-dialog"):
                yield Static(
                    f"[bold dodger_blue2]\u2500\u2500 Confirm {self._mode_label} \u2500\u2500[/]",
                    id="modal-title",
                )
                yield Static(self._summary, id="modal-body")
                with Horizontal(id="modal-actions"):
                    yield Button(f"{self._mode_label}", variant="success",
                                 classes="modal-btn btn-install", id="confirm-yes")
                    yield Button("Cancel", variant="default",
                                 classes="modal-btn btn-cancel", id="confirm-no")

        @on(Button.Pressed, "#confirm-yes")
        def confirm(self, _event) -> None:
            self.dismiss(True)

        @on(Button.Pressed, "#confirm-no")
        def cancel(self, _event=None) -> None:
            self.dismiss(False)

        def action_cancel(self) -> None:
            self.dismiss(False)

    # ── Results Modal ──
    class ResultsScreen(ModalScreen):
        BINDINGS = [
            Binding("escape", "dismiss_screen", "Done"),
            Binding("enter", "dismiss_screen", "Done"),
        ]

        def __init__(self, results_text: str):
            super().__init__()
            self._results = results_text

        def compose(self) -> ComposeResult:
            with Vertical(id="results-dialog"):
                yield Static("[bold green]\u2500\u2500 Results \u2500\u2500[/]", id="modal-title")
                yield VerticalScroll(Static(self._results), id="modal-body")
                with Horizontal(id="modal-actions"):
                    yield Button("Done [Enter]", variant="success",
                                 classes="modal-btn btn-done", id="results-done")

        @on(Button.Pressed, "#results-done")
        def done(self, _event) -> None:
            self.dismiss()

        def action_dismiss_screen(self) -> None:
            self.dismiss()

    # ── Main App ──
    class MarketplaceApp(App):
        CSS = APP_CSS
        TITLE = "Skills Marketplace"
        BINDINGS = [
            Binding("q", "quit_app", "Quit"),
            Binding("p", "preview", "Show Me"),
            Binding("i", "do_install", f"{mode_verb}"),
            Binding("a", "select_all", "All"),
            Binding("n", "select_none", "None"),
            Binding("s", "toggle_scope", "Scope"),
            Binding("space", "toggle_section", "Toggle", show=False),
        ]

        def __init__(self):
            super().__init__()
            self._item_metadata: dict[str, dict] = {}
            self._item_scopes: dict[str, str] = {}
            self._ws_counter = 0

        def action_screenshot(self, filename=None, path=None):
            dl = Path.home() / "Downloads"
            dl.mkdir(parents=True, exist_ok=True)
            super().action_screenshot(filename, path)

        def compose(self) -> ComposeResult:
            yield Header(show_clock=False)
            yield AnimatedBanner(id="banner")
            with Horizontal(id="main-area"):
                left = VerticalScroll(id="left-panel")
                left.can_focus = False
                with left:
                    yield from self._build_left_panel()
                with Vertical(id="right-panel"):
                    yield Static(
                        "[bold medium_purple1]Preview[/]\n\n"
                        "[dim]Navigate to any item and press "
                        "[bold]P[/bold] to show its full content.\n\n"
                        "Use [bold]Space[/bold] to toggle selections.\n"
                        "Use [bold]S[/bold] to toggle scope (global/workspace).\n"
                        "Use [bold]Tab[/bold] to move between sections.\n"
                        "Use [bold]Enter[/bold] to collapse/expand.\n"
                        "Use [bold]I[/bold] to install selected items.[/dim]",
                        id="preview-body",
                    )
            yield Static(
                f"[bold]{mode_verb} mode \u2502 "
                f"0 items selected \u2502 0 workspace-scoped[/]",
                id="status-bar",
            )
            yield Footer()

        def on_mount(self) -> None:
            self._mount_workspace_row()
            try:
                first_sl = self.query_one("#sl-platforms", SelectionList)
                first_sl.focus()
            except Exception:
                pass

        def _mount_workspace_row(self, path: str = "") -> None:
            self._ws_counter += 1
            entry_id = str(self._ws_counter)
            try:
                container = self.query_one("#workspace-entries", Vertical)
            except Exception:
                return
            row = Horizontal(
                PathInput(entry_id, value=path),
                Button("Browse", id=f"ws-browse-{entry_id}", classes="ws-browse-btn"),
                Button("\u2715", id=f"ws-remove-{entry_id}", classes="ws-remove-btn"),
                id=f"ws-row-{entry_id}",
                classes="ws-row",
            )
            container.mount(row)

        def _get_workspace_paths(self) -> list[str]:
            paths = []
            try:
                for inp in self.query(".ws-path-input"):
                    if isinstance(inp, Input) and inp.value.strip():
                        resolved = str(_resolve_user_path(inp.value.strip()))
                        if resolved not in paths:
                            paths.append(resolved)
            except Exception:
                pass
            return paths

        def _build_left_panel(self):
            # ── Platforms ──
            plat_selections = []
            if platforms:
                for pid, info in platforms.items():
                    cfg = info["global"]["config"]
                    detected = cfg.exists()
                    indicator = "[green]\u25cf[/] " if detected else "[dim]\u25cb[/] "
                    status = "[green]config found[/]" if detected else "[dim]dir exists[/]"
                    label = Text.from_markup(
                        f"{indicator}[bold]{info['label']}[/]  {status}"
                    )
                    plat_selections.append(
                        Selection(label, pid, initial_state=True)
                    )
                    self._item_metadata[pid] = {
                        "type": "platform", "name": info["label"],
                        "description": f"Config: {cfg}\nDetected: {'yes' if detected else 'no'}",
                    }
            else:
                for pid, info in PLATFORMS.items():
                    cfg = info["global"]["config"]
                    indicator = "[dim]\u25cb[/] "
                    label = Text.from_markup(
                        f"{indicator}[bold]{info['label']}[/]  [dim]not detected[/]"
                    )
                    plat_selections.append(
                        Selection(label, pid, initial_state=True)
                    )
                    self._item_metadata[pid] = {
                        "type": "platform", "name": info["label"],
                        "description": f"Config: {cfg}\nDetected: no",
                    }

            with Collapsible(
                title="\u2588\u2588 PLATFORMS",
                collapsed=False,
                id="section-platforms",
                classes="section-collapsible",
            ):
                yield MarketplaceList(*plat_selections, id="sl-platforms")

            # ── Workspace Paths ──
            with Collapsible(
                title="\u2588\u2588 WORKSPACE PATHS  \u2014 For [W] scoped items",
                collapsed=False,
                id="section-scope",
                classes="section-collapsible",
            ):
                yield Static(
                    "[dim]Items marked [W] install here. Toggle scope with S key. Tab accepts suggestion.[/]",
                    id="workspace-paths-label",
                )
                yield Vertical(id="workspace-entries")
                yield Button("+ Add Workspace Path", id="ws-add-btn", variant="default")

            # ── MCP Servers ──
            mcp_selections = []
            for name, srv in MCP_SERVERS.items():
                is_inst = name in primary_mcps
                indicator = "[green]\u25cf[/] " if is_inst else "[dim]\u25cb[/] "
                scope_tag = "[W]" if name in WORKSPACE_SCOPE_DEFAULTS else "[G]"
                label = Text.from_markup(
                    f"{indicator}[dim]{scope_tag}[/] [bold]{name}[/]  [dim]{srv['description']}[/]"
                )
                default_checked = (not is_inst) if install_mode else is_inst
                mcp_selections.append(
                    Selection(label, f"mcp:{name}", initial_state=default_checked)
                )
                self._item_metadata[f"mcp:{name}"] = {
                    "type": "mcp", "name": name,
                    "description": srv["description"],
                    "installed": is_inst,
                    "config": json.dumps(srv["config"], indent=2),
                }
                self._item_scopes[f"mcp:{name}"] = "workspace" if name in WORKSPACE_SCOPE_DEFAULTS else "global"
            with Collapsible(
                title="\u2588\u2588 MCP SERVERS  \u2014  External tool connections",
                collapsed=False,
                id="section-mcps",
                classes="section-collapsible",
            ):
                if mcp_selections:
                    yield MarketplaceList(*mcp_selections, id="sl-mcps")
                else:
                    yield Static(
                        "[dim italic]No MCP servers configured. Add entries to catalog.toml.[/]",
                        classes="empty-notice",
                    )

            # ── Rules ──
            has_rules = any(fdata["items"] for fdata in rule_families.values())
            with Collapsible(
                title="\u2588\u2588 RULES  \u2014  Always-on agent behaviors",
                collapsed=False,
                id="section-rules",
                classes="section-collapsible",
            ):
                if not has_rules:
                    yield Static(
                        "[dim italic]No rules yet. Add rules under rules/ to see them here.[/]",
                        classes="empty-notice",
                    )
                for fname, fdata in rule_families.items():
                    if not fdata["items"]:
                        continue
                    icon = fdata.get("icon", "\u2022")
                    sel_count = 0
                    family_selections = []
                    for item in fdata["items"]:
                        is_inst = _is_rule_installed_any(item["name"]) if platforms else False
                        indicator = "[green]\u25cf[/] " if is_inst else "[dim]\u25cb[/] "
                        default_scope = "workspace" if item["name"] in WORKSPACE_SCOPE_DEFAULTS else "global"
                        scope_tag = "[W]" if default_scope == "workspace" else "[G]"
                        label = Text.from_markup(
                            f"{indicator}[dim]{scope_tag}[/] [bold]{item['name']}[/]  [dim]{item['description']}[/]"
                        )
                        default_checked = (not is_inst) if install_mode else is_inst
                        if default_checked:
                            sel_count += 1
                        family_selections.append(
                            Selection(label, f"rule:{item['name']}", initial_state=default_checked)
                        )
                        self._item_metadata[f"rule:{item['name']}"] = {
                            "type": "rule", "name": item["name"],
                            "description": item["description"],
                            "installed": is_inst,
                            "formats": item.get("formats", []),
                            "path": item["path"],
                        }
                        self._item_scopes[f"rule:{item['name']}"] = default_scope
                    slug = fname.lower().replace(" ", "-").replace("&", "and")
                    with Collapsible(
                        title=f"{icon}  {fname}  \u2014  {fdata['description']}  ({sel_count}/{len(fdata['items'])})",
                        collapsed=False,
                    ):
                        yield MarketplaceList(
                            *family_selections,
                            id=f"sl-rules-{slug}",
                        )

            # ── Skills ──
            has_skills = any(fdata["items"] for fdata in skill_families.values())
            with Collapsible(
                title="\u2588\u2588 SKILLS  \u2014  On-demand /skill-name commands",
                collapsed=False,
                id="section-skills",
                classes="section-collapsible",
            ):
                if not has_skills:
                    yield Static(
                        "[dim italic]No skills yet. Add skills under skills/ to see them here.[/]",
                        classes="empty-notice",
                    )
                for fname, fdata in skill_families.items():
                    if not fdata["items"]:
                        continue
                    icon = fdata.get("icon", "\u2022")
                    sel_count = 0
                    family_selections = []
                    for item in fdata["items"]:
                        is_inst = _is_skill_installed_any(item["name"]) if platforms else False
                        indicator = "[green]\u25cf[/] " if is_inst else "[dim]\u25cb[/] "
                        default_scope = "workspace" if item["name"] in WORKSPACE_SCOPE_DEFAULTS else "global"
                        scope_tag = "[W]" if default_scope == "workspace" else "[G]"
                        label = Text.from_markup(
                            f"{indicator}[dim]{scope_tag}[/] [bold]{item['name']}[/]  [dim]{item['description']}[/]"
                        )
                        if install_mode:
                            default_checked = False if item["name"] in SKILLS_DISABLED_BY_DEFAULT else (not is_inst)
                        else:
                            default_checked = is_inst
                        if default_checked:
                            sel_count += 1
                        family_selections.append(
                            Selection(label, f"skill:{item['name']}", initial_state=default_checked)
                        )
                        self._item_metadata[f"skill:{item['name']}"] = {
                            "type": "skill", "name": item["name"],
                            "description": item["description"],
                            "installed": is_inst,
                            "path": item["path"],
                        }
                        self._item_scopes[f"skill:{item['name']}"] = default_scope
                    slug = fname.lower().replace(" ", "-").replace("&", "and")
                    with Collapsible(
                        title=f"{icon}  {fname}  \u2014  {fdata['description']}  ({sel_count}/{len(fdata['items'])})",
                        collapsed=False,
                    ):
                        yield MarketplaceList(
                            *family_selections,
                            id=f"sl-skills-{slug}",
                        )

        def _get_all_selection_lists(self) -> list:
            try:
                return list(self.query(SelectionList))
            except Exception:
                return []

        def _count_selected(self) -> int:
            total = 0
            for sl in self._get_all_selection_lists():
                if sl.id == "sl-platforms":
                    continue
                total += len(sl.selected)
            return total

        def _update_status_bar(self) -> None:
            count = self._count_selected()
            ws_count = sum(1 for s in self._item_scopes.values() if s == "workspace")
            bar = self.query_one("#status-bar", Static)
            bar.update(
                f"[bold]{mode_verb} mode \u2502 "
                f"[bold green]{count}[/bold green] items selected \u2502 "
                f"{ws_count} workspace-scoped[/]"
            )

        @on(SelectionList.SelectionToggled)
        def _on_toggle(self, _event) -> None:
            self._update_status_bar()

        def watch_focused(self, focused) -> None:
            if not isinstance(focused, SelectionList):
                return
            idx = focused.highlighted
            if idx is None:
                if focused.option_count > 0:
                    focused.highlighted = 0
                    idx = 0
                else:
                    return
            try:
                option = focused.get_option_at_index(idx)
            except Exception:
                return
            self._on_highlight_refresh(option.value)

        @on(SelectionList.SelectionHighlighted)
        def _on_highlight(self, event) -> None:
            if event.selection is None:
                return
            self._on_highlight_refresh(event.selection.value)

        def _on_highlight_refresh(self, value: str) -> None:
            meta = self._item_metadata.get(value, {})
            if not meta:
                return
            name = meta.get("name", "")
            desc = meta.get("description", "")
            item_type = meta.get("type", "")
            installed = meta.get("installed", False)
            inst_str = "[green]installed[/]" if installed else "[dim]not installed[/]"
            scope = self._item_scopes.get(value, "global")
            scope_str = f"[bold green]{scope}[/]" if scope == "global" else f"[bold yellow]{scope}[/]"
            lines = [
                f"[bold]{name}[/]",
                "",
                f"{desc}",
                "",
                f"[dim]Status:[/] {inst_str}",
                f"[dim]Type:[/] {item_type}",
                f"[dim]Scope:[/] {scope_str}",
            ]
            if item_type == "mcp":
                lines.append(f"\n[dim]Config:[/]\n{meta.get('config', '')}")
            if item_type == "rule":
                fmts = meta.get("formats", [])
                if fmts:
                    lines.append(f"[dim]Formats:[/] {', '.join(fmts)}")
            lines.append(
                "\n[dim]Press [bold]P[/bold] to view full content\n"
                "Press [bold]S[/bold] to toggle scope[/]"
            )
            try:
                preview = self.query_one("#preview-body", Static)
                preview.update("\n".join(lines))
            except Exception:
                pass

        # ── Workspace path handlers ──

        @on(Button.Pressed, "#ws-add-btn")
        def _on_add_workspace(self, _event) -> None:
            self._mount_workspace_row()

        @on(Button.Pressed, ".ws-remove-btn")
        def _on_remove_workspace(self, event) -> None:
            entry_id = event.button.id.replace("ws-remove-", "")
            try:
                rows = list(self.query(".ws-row"))
                if len(rows) <= 1:
                    self.notify("At least one workspace path is required", severity="warning")
                    return
                row = self.query_one(f"#ws-row-{entry_id}")
                row.remove()
            except Exception:
                pass

        @on(Button.Pressed, ".ws-browse-btn")
        def _on_browse_workspace(self, event) -> None:
            entry_id = event.button.id.replace("ws-browse-", "")
            try:
                input_widget = self.query_one(f"#ws-input-{entry_id}", Input)
            except Exception:
                return
            current = input_widget.value.strip()
            start = str(_resolve_user_path(current)) if current else str(Path.home())

            def _on_path_selected(path: str | None) -> None:
                if path:
                    input_widget.value = path
            self.push_screen(PathPickerScreen(start), callback=_on_path_selected)

        def action_quit_app(self) -> None:
            self.exit()

        def action_preview(self) -> None:
            focused = self.focused
            if not isinstance(focused, SelectionList):
                self.notify("Focus a selection list first", severity="warning")
                return
            idx = focused.highlighted
            if idx is None:
                return
            option = focused.get_option_at_index(idx)
            value = option.value
            meta = self._item_metadata.get(value, {})
            if not meta:
                return
            name = str(meta.get("name", value))
            item_type = meta.get("type", "")
            if item_type in ("skill", "rule") and "path" in meta:
                item_dict = {"path": meta["path"]}
                content = _read_item_content(item_dict, item_type)
            elif item_type == "mcp":
                content = (
                    f"# {name}\n\n"
                    f"{meta.get('description', '')}\n\n"
                    f"## Configuration\n\n```json\n{meta.get('config', '')}\n```"
                )
            else:
                content = f"# {name}\n\n{meta.get('description', '')}"
            self.push_screen(PreviewScreen(name, content))

        def _selection_lists_in_scope(self) -> list:
            focused = self.focused
            if isinstance(focused, SelectionList):
                return [focused]
            if focused is not None and type(focused).__name__ == "CollapsibleTitle":
                parent = focused.parent
                if parent is not None and isinstance(parent, Collapsible):
                    try:
                        return list(parent.query(SelectionList))
                    except Exception:
                        pass
            return []

        def action_select_all(self) -> None:
            for sl in self._selection_lists_in_scope():
                sl.select_all()
            self._update_status_bar()

        def action_select_none(self) -> None:
            for sl in self._selection_lists_in_scope():
                sl.deselect_all()
            self._update_status_bar()

        def action_toggle_section(self) -> None:
            focused = self.focused
            if focused is None:
                return
            if type(focused).__name__ != "CollapsibleTitle":
                return
            parent = focused.parent
            if parent is None or not isinstance(parent, Collapsible):
                return
            try:
                sls = list(parent.query(SelectionList))
            except Exception:
                return
            if not sls:
                return
            all_selected = all(
                len(sl.selected) == sl.option_count for sl in sls
            )
            for sl in sls:
                if all_selected:
                    sl.deselect_all()
                else:
                    sl.select_all()
            self._update_status_bar()

        def action_toggle_scope(self) -> None:
            focused = self.focused
            if not isinstance(focused, SelectionList):
                self.notify("Focus a selection list item to toggle scope", severity="warning")
                return
            idx = focused.highlighted
            if idx is None:
                return
            option = focused.get_option_at_index(idx)
            value = option.value
            if value in self._item_scopes:
                current = self._item_scopes[value]
                new_scope = "workspace" if current == "global" else "global"
                self._item_scopes[value] = new_scope
                meta = self._item_metadata.get(value, {})
                name = meta.get("name", value)
                desc = meta.get("description", "")
                installed = meta.get("installed", False)
                indicator = "[green]\u25cf[/] " if installed else "[dim]\u25cb[/] "
                scope_tag = "[W]" if new_scope == "workspace" else "[G]"
                new_label = Text.from_markup(
                    f"{indicator}[dim]{scope_tag}[/] [bold]{name}[/]  [dim]{desc}[/]"
                )
                try:
                    focused.replace_option_prompt_at_index(idx, new_label)
                except Exception:
                    pass
                self.notify(f"{name}: scope \u2192 {new_scope}", severity="information")
                self._on_highlight_refresh(value)
                self._update_status_bar()

        def action_do_install(self) -> None:
            plat_list = self.query_one("#sl-platforms", SelectionList)
            selected_platforms = list(plat_list.selected)
            if not selected_platforms:
                self.notify("Select at least one platform", severity="warning")
                return

            selected_mcps = []
            selected_rules = []
            selected_skills = []
            for sl in self._get_all_selection_lists():
                if sl.id == "sl-platforms":
                    continue
                for val in sl.selected:
                    if isinstance(val, str):
                        if val.startswith("mcp:"):
                            selected_mcps.append(val.split(":", 1)[1])
                        elif val.startswith("rule:"):
                            selected_rules.append(val.split(":", 1)[1])
                        elif val.startswith("skill:"):
                            selected_skills.append(val.split(":", 1)[1])

            total = len(selected_mcps) + len(selected_rules) + len(selected_skills)
            if total == 0:
                self.notify("Nothing selected", severity="warning")
                return

            # Determine if workspace paths are needed:
            # 1) Any item explicitly [W]
            # 2) Any selected platform lacks global rules AND rules are selected
            has_explicit_ws = any(
                self._item_scopes.get(f"mcp:{n}", "global") == "workspace"
                for n in selected_mcps
            ) or any(
                self._item_scopes.get(f"rule:{n}", "global") == "workspace"
                for n in selected_rules
            ) or any(
                self._item_scopes.get(f"skill:{n}", "global") == "workspace"
                for n in selected_skills
            )
            has_forced_ws = selected_rules and any(
                PLATFORMS[pid]["global"].get("rules") is None
                for pid in selected_platforms if pid in PLATFORMS
            )
            needs_ws = has_explicit_ws or has_forced_ws

            ws_paths = self._get_workspace_paths()
            if needs_ws:
                if not ws_paths:
                    self.notify(
                        "Enter at least one workspace path for workspace-scoped items",
                        severity="error",
                    )
                    return
                for wp in ws_paths:
                    p = Path(wp)
                    if not p.exists():
                        self.notify(f"Workspace path does not exist: {wp}", severity="error")
                        return
                    if not p.is_dir():
                        self.notify(f"Workspace path is not a directory: {wp}", severity="error")
                        return

            plat_labels = [
                PLATFORMS[p]["label"] for p in selected_platforms if p in PLATFORMS
            ]

            # Group items by scope for summary
            global_items: list[str] = []
            workspace_items_list: list[str] = []
            for m in selected_mcps:
                key = f"mcp:{m}"
                scope = self._item_scopes.get(key, "global")
                (workspace_items_list if scope == "workspace" else global_items).append(f"MCP: {m}")
            for r in selected_rules:
                key = f"rule:{r}"
                scope = self._item_scopes.get(key, "global")
                if scope == "workspace":
                    workspace_items_list.append(f"Rule: {r}")
                else:
                    global_items.append(f"Rule: {r}")
            for s in selected_skills:
                key = f"skill:{s}"
                scope = self._item_scopes.get(key, "global")
                (workspace_items_list if scope == "workspace" else global_items).append(f"Skill: {s}")

            # Identify platforms that force rules to workspace
            forced_ws_labels = [
                PLATFORMS[pid]["label"]
                for pid in selected_platforms
                if pid in PLATFORMS and PLATFORMS[pid]["global"].get("rules") is None
            ] if has_forced_ws else []

            summary_lines = [
                f"[bold]Action:[/] [bold dodger_blue2]{mode_verb}[/]",
                f"[bold]Platforms:[/] {', '.join(plat_labels)}",
            ]
            if global_items:
                summary_lines.append(f"\n[bold]Global scope[/] ({len(global_items)} items):")
                for item in global_items:
                    summary_lines.append(f"  \u2022 {item}")
            if forced_ws_labels and selected_rules:
                summary_lines.append(
                    f"\n[dim]Note: {', '.join(forced_ws_labels)} will install rules "
                    f"to workspace (no global rules support)[/]"
                )
            if workspace_items_list:
                wp_display = ", ".join(ws_paths) if ws_paths else "(none)"
                summary_lines.append(
                    f"\n[bold]Workspace scope[/] \u2192 {wp_display} ({len(workspace_items_list)} items):"
                )
                for item in workspace_items_list:
                    summary_lines.append(f"  \u2022 {item}")
            summary_lines.append(f"\n[bold]Total:[/] {total} items")

            def handle_confirm(confirmed: bool | None) -> None:
                if confirmed:
                    self._execute_install(
                        selected_platforms, selected_mcps,
                        selected_rules, selected_skills, ws_paths,
                    )

            self.push_screen(
                ConfirmScreen("\n".join(summary_lines), mode_verb),
                callback=handle_confirm,
            )

        def _get_install_targets(
            self, pid: str, scope: str, ws_paths: list[str],
        ) -> list[tuple[dict, str]]:
            if scope == "global":
                return [(resolve_paths(pid, "global"), "global")]
            return [
                (resolve_paths(pid, "workspace", wp), f"workspace: {wp}")
                for wp in ws_paths
            ]

        def _execute_install(
            self,
            selected_platforms: list[str],
            selected_mcps: list[str],
            selected_rules: list[str],
            selected_skills: list[str],
            ws_paths: list[str],
        ) -> None:
            rules_by_name = {r["name"]: r for r in all_rules}
            skills_by_name = {s["name"]: s for s in all_skills}

            result_lines = []
            total_count = 0

            for pid in selected_platforms:
                info = PLATFORMS[pid]
                plabel = info["label"]
                no_global_rules = info["global"].get("rules") is None

                for name in selected_mcps:
                    key = f"mcp:{name}"
                    scope = self._item_scopes.get(key, "global")
                    for paths, target_label in self._get_install_targets(pid, scope, ws_paths):
                        if install_mode:
                            res = install_mcp(name, MCP_SERVERS[name], paths["config"])
                        else:
                            res = uninstall_mcp(name, paths["config"])
                        color = "green" if res in ("installed", "removed") else "dim"
                        result_lines.append(
                            f"  [{color}]\u2502[/] {plabel:<14s} [bold]MCP[/]    {name:<24s} [{color}]{res}[/] ({target_label})"
                        )
                        total_count += 1

                for name in selected_rules:
                    rule = rules_by_name.get(name)
                    if not rule:
                        continue
                    key = f"rule:{name}"
                    scope = self._item_scopes.get(key, "global")
                    # Platform override: force workspace if platform lacks global rules
                    effective_scope = "workspace" if (scope == "global" and no_global_rules) else scope
                    for paths, target_label in self._get_install_targets(pid, effective_scope, ws_paths):
                        if install_mode:
                            res = install_rule(rule, pid, paths)
                        else:
                            res = uninstall_rule(rule, pid, paths)
                        color = "green" if res in ("installed", "removed") else "dim"
                        result_lines.append(
                            f"  [{color}]\u2502[/] {plabel:<14s} [bold]Rule[/]   {name:<24s} [{color}]{res}[/] ({target_label})"
                        )
                        total_count += 1

                for name in selected_skills:
                    skill = skills_by_name.get(name)
                    if not skill:
                        continue
                    key = f"skill:{name}"
                    scope = self._item_scopes.get(key, "global")
                    for paths, target_label in self._get_install_targets(pid, scope, ws_paths):
                        skills_dir = paths.get("skills")
                        if not skills_dir:
                            continue
                        if install_mode:
                            res = install_skill(skill, skills_dir)
                        else:
                            res = uninstall_skill(name, skills_dir)
                        color = "green" if res in ("installed", "removed") else "dim"
                        result_lines.append(
                            f"  [{color}]\u2502[/] {plabel:<14s} [bold]Skill[/]  {name:<24s} [{color}]{res}[/] ({target_label})"
                        )
                        total_count += 1

            past = "installed" if install_mode else "uninstalled"
            header = (
                f"[bold green]\u2714 Done![/] {total_count} items {past} "
                f"across {len(selected_platforms)} platform(s).\n"
                "[dim]Restart agent sessions to pick up changes.[/]\n"
            )
            results_text = header + "\n" + "\n".join(result_lines)
            self.push_screen(ResultsScreen(results_text), callback=lambda _: self.exit())

    app = MarketplaceApp()
    app.run()


if __name__ == "__main__":
    main()
