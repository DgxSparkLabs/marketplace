# /// script
# requires-python = ">=3.11"
# dependencies = ["textual>=1.0.0"]
# ///
"""
Marketplace interactive installer — install and uninstall agent tools.

Usage:
    uv run install.py                    # interactive mode
    uv run install.py --uninstall        # uninstall mode
    uv run install.py --global           # install to global config (default)
    uv run install.py --project          # install to project-level config
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import shutil
import sys
from pathlib import Path

# ── Platform Definitions ────────────────────────────────────────────────────

PLATFORMS = {
    "devin": {
        "label": "Devin CLI",
        "global": {
            "config": Path.home() / ".config" / "devin" / "config.json",
            "rules": Path.home() / ".config" / "devin" / "AGENTS.md",
            "skills": Path.home() / ".config" / "devin" / "skills",
        },
        "project": {
            "config": Path(".devin") / "config.json",
            "rules": Path("AGENTS.md"),
            "skills": Path(".devin") / "skills",
        },
        "rule_fmt": "agents",
    },
    "claude-code": {
        "label": "Claude Code",
        "global": {
            "config": Path.home() / ".claude" / "settings.json",
            "rules": Path.home() / ".claude" / "CLAUDE.md",
            "skills": None,
        },
        "project": {
            "config": Path(".claude") / "settings.local.json",
            "rules": Path("CLAUDE.md"),
            "skills": None,
        },
        "rule_fmt": "agents",
    },
    "cursor": {
        "label": "Cursor",
        "global": {
            "config": Path.home() / ".cursor" / "mcp.json",
            "rules": Path.home() / ".cursor" / "rules",
            "skills": None,
        },
        "project": {
            "config": Path(".cursor") / "mcp.json",
            "rules": Path(".cursor") / "rules",
            "skills": None,
        },
        "rule_fmt": "cursor",
    },
    "windsurf": {
        "label": "Windsurf",
        "global": {
            "config": Path.home() / ".codeium" / "windsurf" / "mcp_config.json",
            "rules": Path.home() / ".windsurf" / "rules",
            "skills": Path.home() / ".windsurf" / "skills",
        },
        "project": {
            "config": Path(".windsurf") / "mcp.json",
            "rules": Path(".windsurf") / "rules",
            "skills": Path(".windsurf") / "skills",
        },
        "rule_fmt": "windsurf",
    },
}

MCP_SERVERS = {
    "fetch": {
        "description": "Fetch web pages and return content",
        "config": {"command": "uvx", "args": ["mcp-server-fetch"]},
    },
    "github": {
        "description": "GitHub API — issues, PRs, repos, search",
        "config": {"command": "npx", "args": ["-y", "@github/mcp-server"]},
    },
    "playwright": {
        "description": "Browser automation for web testing",
        "config": {"command": "npx", "args": ["-y", "@playwright/mcp-server"]},
    },
    "filesystem": {
        "description": "Read/write/search local files",
        "config": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path.home())]},
    },
    "sqlite": {
        "description": "Query and manage SQLite databases",
        "config": {"command": "uvx", "args": ["mcp-server-sqlite"]},
    },
    "brave-search": {
        "description": "Web search via Brave Search API",
        "config": {"command": "npx", "args": ["-y", "@anthropic/mcp-server-brave-search"]},
    },
    "memory": {
        "description": "Persistent knowledge graph memory",
        "config": {"command": "npx", "args": ["-y", "@anthropic/mcp-server-memory"]},
    },
}

# ── Category Families ───────────────────────────────────────────────────────
# To add a new skill or rule to the installer, just add its name to the
# appropriate family below.  Items not listed go into "Other".

RULE_FAMILIES = {
    "Quality & Verification": {
        "icon": "\u2714",
        "description": "Enforce code quality, testing, and review standards",
        "members": ["blast-radius", "prior-art", "verification-ladder", "verify-your-work"],
    },
    "Documentation & Progress": {
        "icon": "\U0001f4dd",
        "description": "Track work, document decisions, maintain project history",
        "members": ["document-lifecycle", "document-progress"],
    },
    "Workflow & Process": {
        "icon": "\u2699",
        "description": "Shape how agents approach and execute tasks",
        "members": ["continuous-improvement", "improve-the-process", "stay-motivated", "task-formation"],
    },
    "Environment & Conventions": {
        "icon": "\U0001f527",
        "description": "Technical environment rules and output conventions",
        "members": ["no-ai-credit", "python-uv"],
    },
    "Notifications": {
        "icon": "\U0001f514",
        "description": "Alert you when important events happen",
        "members": ["telegram-on-complete"],
    },
}

SKILL_FAMILIES = {
    "Search & Research": {
        "icon": "\U0001f50d",
        "description": "Find information across web, code repos, and video",
        "members": ["duckduckgo-search", "github-search", "web-scraper", "youtube-search", "youtube-wisdom"],
    },
    "Communication": {
        "icon": "\u2709",
        "description": "Send emails, messages, and notifications",
        "members": ["send-email", "telegram-notify"],
    },
    "DevOps & Infrastructure": {
        "icon": "\U0001f680",
        "description": "Run CI locally, expose ports, manage tunnels",
        "members": ["act-runner", "expose-port", "ssh-tunnel"],
    },
    "Productivity & Meta": {
        "icon": "\u2b50",
        "description": "Session management, handoffs, and skill development",
        "members": ["motivation", "session-history", "structured-handoff", "skill-creator", "sync-rules", "textual-tui-guide"],
    },
    "AI & External Services": {
        "icon": "\U0001f916",
        "description": "Connect to AI models and cloud APIs",
        "members": ["gemini-chat", "google-drive-reader"],
    },
}

# Skills unchecked by default in install mode (require API keys or complex setup)
SKILLS_DISABLED_BY_DEFAULT = {"web-scraper", "expose-port", "gemini-chat", "google-drive-reader"}


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
    if fmt == "agents":
        # Rules appended to a single file
        if target.exists():
            content = target.read_text()
            # Read actual heading from rule.md instead of guessing from dir name
            rule_path = find_marketplace() / "rules" / rule_name / "rule.md"
            if rule_path.exists():
                for line in rule_path.read_text().splitlines():
                    if line.startswith("## "):
                        return line[3:].strip() in content
            # Fallback: check if dir name appears in any ## heading
            return f"## {rule_name}" in content.lower().replace(" ", "-")
        return False
    else:
        # Rules as separate .md files in a directory
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
    rules = []
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
    skills = []
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
        with open(target, "a") as f:
            # Only add separator newline if file already has content
            if target.exists() and target.stat().st_size > 0:
                f.write("\n")
            f.write(content)
        return "installed"
    else:
        src = rule["path"] / "formats" / f"{fmt}.md"
        if not src.exists():
            return f"no {fmt} format"
        target.mkdir(parents=True, exist_ok=True)
        dest = target / f"{rule['name']}.md"
        # Skip if already identical
        if dest.exists() and dest.read_text() == src.read_text():
            return "already installed"
        shutil.copy2(src, dest)
        return "installed"


def uninstall_rule(rule: dict, pid: str, paths: dict) -> str:
    fmt = PLATFORMS[pid]["rule_fmt"]
    target = paths["rules"]

    if fmt == "agents":
        if not target.exists():
            return "not found"
        content = target.read_text()
        rule_content = (rule["path"] / "rule.md").read_text().strip()
        # Try to find and remove the rule block
        title = ""
        for line in rule_content.splitlines():
            if line.startswith("## "):
                title = line.strip()
                break
        if not title or title not in content:
            return "not installed"
        # Remove from the next occurrence of the heading to the next ## heading or EOF
        lines = content.splitlines(keepends=True)
        new_lines = []
        skipping = False
        for line in lines:
            if line.strip() == title:
                skipping = True
                # Also remove a leading blank line
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


# ── UI Helpers ──────────────────────────────────────────────────────────────

def status_badge(installed: bool) -> str:
    return "[green]installed[/green]" if installed else "[dim]not installed[/dim]"


def action_badge(result: str) -> str:
    if result in ("installed", "removed"):
        return f"[green]{result}[/green]"
    if result in ("already installed", "not installed", "not found"):
        return f"[dim]{result}[/dim]"
    return f"[yellow]{result}[/yellow]"


def show_platform_table(platforms: dict, scope: str):
    from rich.console import Console
    from rich.table import Table
    from rich import box
    console = Console()
    table = Table(box=box.ROUNDED, title="Detected Platforms", title_style="bold cyan",
                  border_style="cyan", padding=(0, 1))
    table.add_column("Platform", style="bold")
    table.add_column("Status")
    table.add_column("Config")
    for pid, info in PLATFORMS.items():
        if pid in platforms:
            cfg = info[scope]["config"]
            exists = "config found" if cfg.exists() else "dir exists"
            table.add_row(info["label"], f"[green]{exists}[/green]", str(cfg))
        else:
            table.add_row(info["label"], "[dim]not detected[/dim]", "")
    console.print(table)
    console.print()


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

/* Modal screens */
ConfirmScreen, PreviewScreen, ResultsScreen {
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
"""

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
    "  [bold bright_cyan]╔═╗ ╦╔═ ╦ ╦   ╦   ╔═╗[/]",
    "  [bold cyan]╚═╗ ╠╩╗ ║ ║   ║   ╚═╗[/]",
    "  [bold deep_sky_blue1]╚═╝ ╩ ╩ ╩ ╩═╝ ╩═╝ ╚═╝[/]",
    "",
    "  [bold medium_purple1]╔╦╗ ╔═╗ ╦═╗ ╦╔═ ╔═╗ ╔╦╗[/]",
    "  [bold medium_purple1]║║║ ╠═╣ ╠╦╝ ╠╩╗ ║╣   ║[/]",
    "  [bold blue]╩ ╩ ╩ ╩ ╩╚═ ╩ ╩ ╚═╝  ╩[/]",
    "  [dim]──────────────────────────[/]",
    "  [bold deep_sky_blue1]✦[/] [bold white]Agent Tools Installer[/] [bold deep_sky_blue1]✦[/]",
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


# ── TUI App ─────────────────────────────────────────────────────────────────

def main():
    from textual import on
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Horizontal, Vertical, VerticalScroll
    from textual.screen import ModalScreen
    from textual.widgets import (
        Button, Collapsible, Footer, Header,
        Markdown, SelectionList, Static,
    )
    from textual.widgets.selection_list import Selection
    from rich.text import Text

    # ── Animated 3D wireframe banner ──
    class AnimatedBanner(Static):
        """Spinning wireframe cube + octahedron rendered in braille."""
        _GW, _GH = 50, 40  # pixel grid → 25 braille chars × 10 lines

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
    # Enter still collapses/expands.
    try:
        from textual.widgets._collapsible import CollapsibleTitle
        CollapsibleTitle.BINDINGS = [Binding("enter", "toggle", "Toggle")]
    except ImportError:
        pass

    parser = argparse.ArgumentParser(description="Marketplace interactive installer")
    parser.add_argument("--global", dest="scope", action="store_const", const="global", default="global")
    parser.add_argument("--project", dest="scope", action="store_const", const="project")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall mode")
    args = parser.parse_args()
    scope = args.scope
    install_mode = not args.uninstall
    mode_verb = "Install" if install_mode else "Uninstall"

    platforms = detect_platforms()
    if not platforms:
        from rich.console import Console
        Console().print("[red]No agent platforms detected.[/red]")
        sys.exit(1)

    marketplace = find_marketplace()
    all_rules = scan_rules(marketplace)
    all_skills = scan_skills(marketplace)

    primary_pid = list(platforms.keys())[0]
    primary_paths = PLATFORMS[primary_pid][scope]
    primary_mcps = read_mcp_servers(primary_paths["config"])

    rule_families = _categorize_items(all_rules, RULE_FAMILIES)
    skill_families = _categorize_items(all_skills, SKILL_FAMILIES)

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
                    yield Button("Close [Esc]", variant="default", classes="modal-btn btn-close", id="preview-close")

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
                yield Static(f"[bold dodger_blue2]\u2500\u2500 Confirm {self._mode_label} \u2500\u2500[/]", id="modal-title")
                yield Static(self._summary, id="modal-body")
                with Horizontal(id="modal-actions"):
                    yield Button(f"{self._mode_label}", variant="success", classes="modal-btn btn-install", id="confirm-yes")
                    yield Button("Cancel", variant="default", classes="modal-btn btn-cancel", id="confirm-no")

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
        BINDINGS = [Binding("escape", "dismiss_screen", "Done"), Binding("enter", "dismiss_screen", "Done")]

        def __init__(self, results_text: str):
            super().__init__()
            self._results = results_text

        def compose(self) -> ComposeResult:
            with Vertical(id="results-dialog"):
                yield Static("[bold green]\u2500\u2500 Results \u2500\u2500[/]", id="modal-title")
                yield VerticalScroll(Static(self._results), id="modal-body")
                with Horizontal(id="modal-actions"):
                    yield Button("Done [Enter]", variant="success", classes="modal-btn btn-done", id="results-done")

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
            Binding("space", "toggle_section", "Toggle", show=False),
        ]

        def __init__(self):
            super().__init__()
            self._item_metadata: dict[str, dict] = {}

        def action_screenshot(self, filename=None, path=None):
            """Ensure download dir exists before taking a screenshot."""
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
                        "Use [bold]Space[/bold] on a section header to\n"
                        "toggle all items in that group.\n"
                        "Use [bold]Tab[/bold] to move between sections.\n"
                        "Use [bold]Enter[/bold] to collapse/expand.\n"
                        "Use [bold]I[/bold] to install selected items.[/dim]",
                        id="preview-body",
                    )
            yield Static(
                f"[bold]{mode_verb} mode \u2502 {scope} scope \u2502 "
                f"0 items selected[/]",
                id="status-bar",
            )
            yield Footer()

        def on_mount(self) -> None:
            """Focus the first SelectionList so arrow keys work immediately."""
            try:
                first_sl = self.query_one("#sl-platforms", SelectionList)
                first_sl.focus()
            except Exception:
                pass

        def _build_left_panel(self):
            """Generator helper that yields all widgets for the left panel."""
            # ── Platforms ──
            plat_selections = []
            for pid, info in platforms.items():
                cfg = info[scope]["config"]
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
            with Collapsible(
                title="\u2588\u2588 PLATFORMS",
                collapsed=False,
                id="section-platforms",
                classes="section-collapsible",
            ):
                yield SelectionList(*plat_selections, id="sl-platforms")

            # ── MCP Servers ──
            mcp_selections = []
            for name, srv in MCP_SERVERS.items():
                is_inst = name in primary_mcps
                indicator = "[green]\u25cf[/] " if is_inst else "[dim]\u25cb[/] "
                label = Text.from_markup(
                    f"{indicator}[bold]{name}[/]  [dim]{srv['description']}[/]"
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
            with Collapsible(
                title="\u2588\u2588 MCP SERVERS  \u2014  External tool connections",
                collapsed=False,
                id="section-mcps",
                classes="section-collapsible",
            ):
                yield SelectionList(*mcp_selections, id="sl-mcps")

            # ── Rules ──
            with Collapsible(
                title="\u2588\u2588 RULES  \u2014  Always-on agent behaviors",
                collapsed=False,
                id="section-rules",
                classes="section-collapsible",
            ):
                for fname, fdata in rule_families.items():
                    if not fdata["items"]:
                        continue
                    icon = fdata.get("icon", "\u2022")
                    sel_count = 0
                    family_selections = []
                    for item in fdata["items"]:
                        is_inst = is_rule_installed(primary_pid, item["name"], primary_paths)
                        indicator = "[green]\u25cf[/] " if is_inst else "[dim]\u25cb[/] "
                        label = Text.from_markup(
                            f"{indicator}[bold]{item['name']}[/]  [dim]{item['description']}[/]"
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
                    slug = fname.lower().replace(" ", "-").replace("&", "and")
                    with Collapsible(
                        title=f"{icon}  {fname}  \u2014  {fdata['description']}  ({sel_count}/{len(fdata['items'])})",
                        collapsed=False,
                    ):
                        yield SelectionList(
                            *family_selections,
                            id=f"sl-rules-{slug}",
                        )

            # ── Skills ──
            with Collapsible(
                title="\u2588\u2588 SKILLS  \u2014  On-demand /skill-name commands",
                collapsed=False,
                id="section-skills",
                classes="section-collapsible",
            ):
                for fname, fdata in skill_families.items():
                    if not fdata["items"]:
                        continue
                    icon = fdata.get("icon", "\u2022")
                    sel_count = 0
                    family_selections = []
                    for item in fdata["items"]:
                        is_inst = is_skill_installed(item["name"], primary_paths)
                        indicator = "[green]\u25cf[/] " if is_inst else "[dim]\u25cb[/] "
                        label = Text.from_markup(
                            f"{indicator}[bold]{item['name']}[/]  [dim]{item['description']}[/]"
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
                    slug = fname.lower().replace(" ", "-").replace("&", "and")
                    with Collapsible(
                        title=f"{icon}  {fname}  \u2014  {fdata['description']}  ({sel_count}/{len(fdata['items'])})",
                        collapsed=False,
                    ):
                        yield SelectionList(
                            *family_selections,
                            id=f"sl-skills-{slug}",
                        )

        def _get_all_selection_lists(self) -> list:
            """Get all SelectionList widgets."""
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
            bar = self.query_one("#status-bar", Static)
            bar.update(
                f"[bold]{mode_verb} mode \u2502 {scope} scope \u2502 "
                f"[bold green]{count}[/bold green] items selected[/]"
            )

        @on(SelectionList.SelectionToggled)
        def _on_toggle(self, _event) -> None:
            self._update_status_bar()

        @on(SelectionList.SelectionHighlighted)
        def _on_highlight(self, event) -> None:
            """Update the preview panel when cursor moves."""
            if event.selection is None:
                return
            value = event.selection.value
            meta = self._item_metadata.get(value, {})
            if not meta:
                return
            name = meta.get("name", "")
            desc = meta.get("description", "")
            item_type = meta.get("type", "")
            installed = meta.get("installed", False)
            inst_str = "[green]installed[/]" if installed else "[dim]not installed[/]"

            lines = [
                f"[bold]{name}[/]",
                "",
                f"{desc}",
                "",
                f"[dim]Status:[/] {inst_str}",
                f"[dim]Type:[/] {item_type}",
            ]
            if item_type == "mcp":
                lines.append(f"\n[dim]Config:[/]\n{meta.get('config', '')}")
            if item_type == "rule":
                fmts = meta.get("formats", [])
                if fmts:
                    lines.append(f"[dim]Formats:[/] {', '.join(fmts)}")
            lines.append(
                "\n[dim]Press [bold]P[/bold] to view full content[/]"
            )
            preview = self.query_one("#preview-body", Static)
            preview.update("\n".join(lines))

        def action_quit_app(self) -> None:
            self.exit()

        def action_preview(self) -> None:
            """Show full SKILL.md or rule.md in a modal."""
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
            name = meta.get("name", value)
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
            """Get SelectionLists based on what's focused.

            - Focused on a SelectionList → just that list
            - Focused on a CollapsibleTitle → all lists inside that Collapsible
            - Otherwise → empty
            """
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
            """Space on a CollapsibleTitle toggles all selections in it."""
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

        def action_do_install(self) -> None:
            """Gather selections and show confirmation."""
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

            summary_lines = [
                f"[bold]Action:[/] [bold dodger_blue2]{mode_verb}[/]",
                f"[bold]Scope:[/] {scope}",
                f"[bold]Platforms:[/] {', '.join(PLATFORMS[p]['label'] for p in selected_platforms)}",
                "",
                f"[bold]MCP Servers:[/] {len(selected_mcps)}",
            ]
            for m in selected_mcps:
                summary_lines.append(f"  \u2022 {m}")
            summary_lines.append(f"\n[bold]Rules:[/] {len(selected_rules)}")
            for r in selected_rules:
                summary_lines.append(f"  \u2022 {r}")
            summary_lines.append(f"\n[bold]Skills:[/] {len(selected_skills)}")
            for s in selected_skills:
                summary_lines.append(f"  \u2022 {s}")
            summary_lines.append(f"\n[bold]Total:[/] {total} items")

            def handle_confirm(confirmed: bool | None) -> None:
                if confirmed:
                    self._execute_install(
                        selected_platforms, selected_mcps,
                        selected_rules, selected_skills,
                    )

            self.push_screen(
                ConfirmScreen("\n".join(summary_lines), mode_verb),
                callback=handle_confirm,
            )

        def _execute_install(
            self,
            selected_platforms: list[str],
            selected_mcps: list[str],
            selected_rules: list[str],
            selected_skills: list[str],
        ) -> None:
            rules_by_name = {r["name"]: r for r in all_rules}
            skills_by_name = {s["name"]: s for s in all_skills}

            result_lines = []
            total_count = 0

            for pid in selected_platforms:
                info = PLATFORMS[pid]
                paths = info[scope]
                plabel = info["label"]

                for name in selected_mcps:
                    if install_mode:
                        res = install_mcp(name, MCP_SERVERS[name], paths["config"])
                    else:
                        res = uninstall_mcp(name, paths["config"])
                    color = "green" if res in ("installed", "removed") else "dim"
                    result_lines.append(
                        f"  [{color}]\u2502[/] {plabel:<14s} [bold]MCP[/]    {name:<24s} [{color}]{res}[/]"
                    )
                    total_count += 1

                for name in selected_rules:
                    rule = rules_by_name.get(name)
                    if not rule:
                        continue
                    if install_mode:
                        res = install_rule(rule, pid, paths)
                    else:
                        res = uninstall_rule(rule, pid, paths)
                    color = "green" if res in ("installed", "removed") else "dim"
                    result_lines.append(
                        f"  [{color}]\u2502[/] {plabel:<14s} [bold]Rule[/]   {name:<24s} [{color}]{res}[/]"
                    )
                    total_count += 1

                skills_dir = paths.get("skills")
                for name in selected_skills:
                    skill = skills_by_name.get(name)
                    if not skill:
                        continue
                    if install_mode:
                        res = install_skill(skill, skills_dir)
                    else:
                        res = uninstall_skill(name, skills_dir)
                    color = "green" if res in ("installed", "removed") else "dim"
                    result_lines.append(
                        f"  [{color}]\u2502[/] {plabel:<14s} [bold]Skill[/]  {name:<24s} [{color}]{res}[/]"
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
