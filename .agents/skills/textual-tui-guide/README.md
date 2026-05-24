# textual-tui-guide

Build rich terminal user interfaces with Python's Textual framework. Covers layouts, widgets, modals, styling, key bindings, and data flow patterns.

## What's included

- **SKILL.md** — Complete guide to Textual TUI architecture: compose pattern, CSS, widgets, modals, events, data flow
- **references/patterns.md** — Annotated cookbook extracted from a production 1200-line TUI (the marketplace installer)
- **scripts/scaffold_tui.py** — Generates a working TUI skeleton you can customize

## Usage

### Scaffold a new TUI

```bash
uv run textual-tui-guide/scripts/scaffold_tui.py my_app.py --name "My Dashboard"
uv run my_app.py
```

The generated file is a single self-contained Python script with PEP 723 inline dependencies. It includes:

- Two-panel layout (selection + preview)
- Collapsible sections with selection lists
- Confirm and results modal dialogs
- Status bar with live selection count
- Keyboard shortcuts (q/p/i/a/n)
- Event-driven preview updates

### As a reference

Read the SKILL.md for a compact guide, or `references/patterns.md` for the full annotated cookbook with CSS reference and modal patterns.

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r textual-tui-guide/ ~/.config/devin/skills/textual-tui-guide/

# Project-specific
cp -r textual-tui-guide/ /path/to/project/.devin/skills/textual-tui-guide/
```

Then invoke with `/textual-tui-guide` in a session, or let the agent use it automatically when building terminal UIs.
