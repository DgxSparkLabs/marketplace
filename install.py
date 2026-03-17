# /// script
# requires-python = ">=3.11"
# dependencies = ["questionary", "rich"]
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
import json
import shutil
import sys
from pathlib import Path

import questionary
from prompt_toolkit.keys import Keys as PtKeys
from questionary import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# Key binding hints shown on interactive prompts
KEYS_CHECKBOX = "(Space: toggle, Enter: confirm, Esc: cancel)"
KEYS_CONFIRM = "(Enter: confirm, Esc: cancel)"


def _add_escape_binding(question: questionary.Question) -> questionary.Question:
    """Patch a questionary Question so that Escape cancels (same as Ctrl+C)."""
    kb = question.application.key_bindings
    # confirm prompts use _MergedKeyBindings which lacks .add() —
    # fall back to creating a fresh KeyBindings layer and merging it.
    if hasattr(kb, "add"):
        @kb.add(PtKeys.Escape, eager=True)
        def _escape(event):
            event.app.exit(exception=KeyboardInterrupt, style="class:aborting")
    else:
        from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
        extra = KeyBindings()

        @extra.add(PtKeys.Escape, eager=True)
        def _escape(event):
            event.app.exit(exception=KeyboardInterrupt, style="class:aborting")

        question.application.key_bindings = merge_key_bindings([kb, extra])

    return question

STYLE = Style([
    ("qmark", "fg:cyan bold"),
    ("question", "bold"),
    ("pointer", "fg:cyan bold"),
    ("highlighted", "fg:cyan bold"),
    ("selected", "fg:green"),
    ("separator", "fg:#808080"),
    ("instruction", "fg:#808080"),
    ("answer", "fg:green bold"),
])

# ── Platform Definitions ────────────────────────────────────────────────────

PLATFORMS = {
    "devin": {
        "label": "Devin CLI",
        "global": {
            "config": Path.home() / ".config" / "cognition" / "config.json",
            "rules": Path.home() / ".config" / "cognition" / "AGENTS.md",
            "skills": Path.home() / ".config" / "cognition" / "skills",
        },
        "project": {
            "config": Path(".cognition") / "config.json",
            "rules": Path("AGENTS.md"),
            "skills": Path(".cognition") / "skills",
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


def build_choices(items: list[dict], installed_check, *, install_mode: bool) -> list[questionary.Choice]:
    """Build checkbox choices with install status shown."""
    choices = []
    for item in items:
        is_inst = installed_check(item)
        label = f"{item['name']:<25s} {item['description'][:50]}"
        if install_mode:
            choices.append(questionary.Choice(label, value=item["name"], checked=not is_inst))
        else:
            choices.append(questionary.Choice(label, value=item["name"], checked=is_inst))
    return choices


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Marketplace interactive installer")
    parser.add_argument("--global", dest="scope", action="store_const", const="global", default="global")
    parser.add_argument("--project", dest="scope", action="store_const", const="project")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall mode")
    args = parser.parse_args()
    scope = args.scope

    mode = "uninstall" if args.uninstall else "install"
    mode_color = "red" if mode == "uninstall" else "cyan"
    mode_verb = "Uninstall" if mode == "uninstall" else "Install"
    mode_past = "uninstalled" if mode == "uninstall" else "installed"

    console.print(Panel.fit(
        f"[bold {mode_color}]Marketplace {mode_verb}er[/bold {mode_color}]\n"
        f"Select agent tools to {mode} ({scope} scope)",
        border_style=mode_color,
    ))
    console.print("[dim]Navigation: arrows to move, Space to toggle, Enter to confirm, Esc to cancel[/dim]")
    console.print()

    # ── Detect platforms ──
    platforms = detect_platforms()
    if not platforms:
        console.print("[red]No agent platforms detected.[/red]")
        sys.exit(1)
    show_platform_table(platforms, scope)

    platform_choices = _add_escape_binding(questionary.checkbox(
        "Which platforms?",
        choices=[questionary.Choice(info["label"], value=pid, checked=True)
                 for pid, info in platforms.items()],
        style=STYLE,
        instruction=KEYS_CHECKBOX,
    )).ask()
    if not platform_choices:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    if len(platform_choices) > 1 and mode == "install":
        # Check if multiple platforms would write rules the same agent reads
        agents_fmts = [pid for pid in platform_choices if PLATFORMS[pid]["rule_fmt"] == "agents"]
        if len(agents_fmts) > 1:
            labels = ", ".join(PLATFORMS[p]["label"] for p in agents_fmts)
            console.print(f"[yellow]Note:[/yellow] {labels} all use AGENTS.md format — "
                          "rules will be appended to separate files, no duplication.")
        else:
            console.print(
                f"[yellow]Note:[/yellow] Installing to {len(platform_choices)} platforms. "
                "If your agent reads from multiple sources (e.g. Devin reads AGENTS.md + "
                ".windsurf/ + .cursor/), rules may appear multiple times in context. "
                "Consider installing to one platform only."
            )
        console.print()

    # ── Scan marketplace ──
    marketplace = find_marketplace()
    rules = scan_rules(marketplace)
    skills = scan_skills(marketplace)

    # For status detection, use first selected platform
    primary_pid = platform_choices[0]
    primary_paths = PLATFORMS[primary_pid][scope]

    # ── MCP Servers ──
    console.print(f"\n[bold {mode_color}]MCP Servers[/bold {mode_color}]")
    primary_mcps = read_mcp_servers(primary_paths["config"])
    mcp_choices_list = []
    for name, srv in MCP_SERVERS.items():
        is_inst = name in primary_mcps
        marker = "\u2713 " if is_inst else "  "
        label = f"{marker}{name:<20s} {srv['description'][:50]}"
        if mode == "install":
            mcp_choices_list.append(questionary.Choice(label, value=name, checked=not is_inst))
        else:
            mcp_choices_list.append(questionary.Choice(label, value=name, checked=is_inst))

    mcp_choices = _add_escape_binding(questionary.checkbox(
        f"MCP servers to {mode}:",
        choices=mcp_choices_list,
        style=STYLE,
        instruction=KEYS_CHECKBOX,
    )).ask()
    if mcp_choices is None:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    # ── Rules ──
    console.print(f"\n[bold {mode_color}]Rules[/bold {mode_color}] [dim](always-on agent instructions)[/dim]")
    rule_choices_list = []
    for r in rules:
        is_inst = is_rule_installed(primary_pid, r["name"], primary_paths)
        marker = "\u2713 " if is_inst else "  "
        label = f"{marker}{r['name']:<25s} {r['description'][:45]}"
        if mode == "install":
            rule_choices_list.append(questionary.Choice(label, value=r["name"], checked=not is_inst))
        else:
            rule_choices_list.append(questionary.Choice(label, value=r["name"], checked=is_inst))

    rule_choices = _add_escape_binding(questionary.checkbox(
        f"Rules to {mode}:",
        choices=rule_choices_list,
        style=STYLE,
        instruction=KEYS_CHECKBOX,
    )).ask()
    if rule_choices is None:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    # ── Skills ──
    console.print(f"\n[bold {mode_color}]Skills[/bold {mode_color}] [dim](on-demand /skill-name commands)[/dim]")
    skill_choices_list = []
    for s in skills:
        is_inst = is_skill_installed(s["name"], primary_paths)
        marker = "\u2713 " if is_inst else "  "
        label = f"{marker}{s['name']:<25s} {s['description'][:45]}"
        if mode == "install":
            skill_choices_list.append(questionary.Choice(label, value=s["name"], checked=not is_inst))
        else:
            skill_choices_list.append(questionary.Choice(label, value=s["name"], checked=is_inst))

    skill_choices = _add_escape_binding(questionary.checkbox(
        f"Skills to {mode}:",
        choices=skill_choices_list,
        style=STYLE,
        instruction=KEYS_CHECKBOX,
    )).ask()
    if skill_choices is None:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    # ── Confirm ──
    total = len(mcp_choices) + len(rule_choices) + len(skill_choices)
    if total == 0:
        console.print("[yellow]Nothing selected.[/yellow]")
        return

    summary = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    summary.add_column(style="bold")
    summary.add_column()
    summary.add_row("Action", f"[bold {mode_color}]{mode_verb}[/bold {mode_color}]")
    summary.add_row("MCP servers", f"{len(mcp_choices)}")
    summary.add_row("Rules", f"{len(rule_choices)}")
    summary.add_row("Skills", f"{len(skill_choices)}")
    summary.add_row("Platforms", ", ".join(platform_choices))
    summary.add_row("Scope", scope)
    console.print(Panel(summary, title="Summary", border_style=mode_color))

    proceed = _add_escape_binding(questionary.confirm(
        f"Proceed with {mode}?", default=True, style=STYLE,
        instruction=KEYS_CONFIRM,
    )).ask()
    if not proceed:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    # ── Execute ──
    console.print()
    selected_rules = {r["name"]: r for r in rules if r["name"] in rule_choices}
    selected_skills = {s["name"]: s for s in skills if s["name"] in skill_choices}

    results_table = Table(box=box.ROUNDED, border_style=mode_color, padding=(0, 1),
                          title=f"{mode_verb}ation Results", title_style=f"bold {mode_color}")
    results_table.add_column("Platform", style="bold cyan")
    results_table.add_column("Type")
    results_table.add_column("Name")
    results_table.add_column("Result")

    for pid in platform_choices:
        info = PLATFORMS[pid]
        paths = info[scope]

        # MCP servers
        for name in mcp_choices:
            if mode == "install":
                res = install_mcp(name, MCP_SERVERS[name], paths["config"])
            else:
                res = uninstall_mcp(name, paths["config"])
            results_table.add_row(info["label"], "[green]MCP[/green]", name, action_badge(res))

        # Rules
        for name in rule_choices:
            rule = selected_rules[name]
            if mode == "install":
                res = install_rule(rule, pid, paths)
            else:
                res = uninstall_rule(rule, pid, paths)
            results_table.add_row(info["label"], "[yellow]Rule[/yellow]", name, action_badge(res))

        # Skills
        skills_dir = paths.get("skills")
        for name in skill_choices:
            if mode == "install":
                skill = selected_skills[name]
                res = install_skill(skill, skills_dir)
            else:
                res = uninstall_skill(name, skills_dir)
            results_table.add_row(info["label"], "[magenta]Skill[/magenta]", name, action_badge(res))

    console.print(results_table)
    console.print()
    console.print(Panel.fit(
        f"[bold green]Done![/bold green] {total} items {mode_past} across {len(platform_choices)} platform(s).\n"
        "Restart agent sessions to pick up changes.",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
