# Textual TUI Patterns — Reference

Annotated patterns extracted from the marketplace installer (`install.py`), a 1400+ line production TUI. Use this as a cookbook when building your own.

## Table of Contents

1. [File skeleton](#file-skeleton)
2. [App class structure](#app-class-structure)
3. [Two-panel layout](#two-panel-layout)
4. [Building dynamic content with generators](#building-dynamic-content-with-generators)
5. [Nested collapsible sections](#nested-collapsible-sections)
6. [Modal screen patterns](#modal-screen-patterns)
7. [Event-driven preview updates](#event-driven-preview-updates)
8. [Gathering and acting on selections](#gathering-and-acting-on-selections)
9. [Animated widgets](#animated-widgets)
10. [CSS reference](#css-reference)
11. [Platform fixes](#platform-fixes)
12. [Full app lifecycle](#full-app-lifecycle)

---

## File skeleton

Single-file TUI with PEP 723 inline deps — zero install, just `uv run app.py`:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["textual>=1.0.0"]
# ///
"""My TUI app."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

# Data definitions (dicts, constants) go here — keep them out of main()

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

    # Parse CLI args before creating the app
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="install")
    args = parser.parse_args()

    # Scan data, detect state, build lookup dicts
    items = load_items()

    class MyApp(App):
        CSS = "..."       # Textual CSS as a class variable
        TITLE = "My App"
        BINDINGS = [...]

        def compose(self) -> ComposeResult:
            ...

    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()
```

Why imports are inside `main()`: the `textual` import is heavy. Keeping it inside the function means the module can be imported for testing without triggering it.

---

## App class structure

```python
class MyApp(App):
    CSS = APP_CSS                    # CSS string (class var)
    TITLE = "My TUI"                # Shown in Header
    BINDINGS = [                     # Key shortcuts (shown in Footer)
        Binding("q", "quit_app", "Quit"),
        Binding("p", "preview", "Preview"),
        Binding("i", "do_action", "Install"),
        Binding("a", "select_all", "All"),
        Binding("n", "select_none", "None"),
    ]

    def __init__(self):
        super().__init__()
        self._metadata: dict[str, dict] = {}   # Store per-item info

    def compose(self) -> ComposeResult:
        """Declare the widget tree. Called once."""
        yield Header(show_clock=False)
        yield Static(BANNER, id="banner")
        with Horizontal(id="main"):
            left = VerticalScroll(id="left")
            left.can_focus = False              # Tab skips container, goes to children
            with left:
                yield from self._build_left()
            with Vertical(id="right"):
                yield Static("Preview", id="preview")
        yield Static("status", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Runs after compose. Focus the first interactive widget."""
        try:
            self.query_one("#first-list", SelectionList).focus()
        except Exception:
            pass

    # Action methods (called by Bindings)
    def action_quit_app(self) -> None:
        self.exit()
```

---

## Two-panel layout

The installer uses a 2:1 horizontal split — selection on the left, preview on the right:

```python
with Horizontal(id="main-area"):
    left = VerticalScroll(id="left-panel")
    left.can_focus = False
    with left:
        yield from self._build_left_panel()
    with Vertical(id="right-panel"):
        yield Static("...", id="preview-body")
```

CSS:
```css
#left-panel  { width: 2fr; border: round $primary 30%; overflow-y: auto; }
#right-panel { width: 1fr; border: round $secondary 30%; }
```

`VerticalScroll` gives the left panel automatic scrolling. Setting `can_focus = False` means Tab jumps directly to the SelectionList children.

---

## Building dynamic content with generators

The `_build_left_panel()` method is a generator that builds all left-panel content. This keeps `compose()` clean:

```python
def _build_left_panel(self):
    # Build Selection objects first, then yield the list
    selections = []
    for item in data:
        label = Text.from_markup(f"[bold]{item['name']}[/]  [dim]{item['desc']}[/]")
        selections.append(Selection(label, f"type:{item['name']}", initial_state=True))
        self._metadata[f"type:{item['name']}"] = item  # Store for later lookup
    
    with Collapsible(title="SECTION", collapsed=False, id="section-id"):
        yield SelectionList(*selections, id="sl-items")
```

The pattern is:
1. Build `Selection` objects in a list (with Rich-formatted labels)
2. Store metadata keyed by the selection value
3. Yield the `SelectionList` inside a layout container

---

## Nested collapsible sections

Two levels: top-level sections (Platforms, MCP, Rules, Skills) contain family-level sub-groups:

```python
# Top-level: bold colored header
with Collapsible(
    title="\u2588\u2588 RULES  \u2014  Always-on behaviors",
    collapsed=False,
    id="section-rules",
    classes="section-collapsible",
):
    # Family level: italic sub-headers with counts
    for family_name, family_data in families.items():
        selections = []
        count = 0
        for item in family_data["items"]:
            checked = not item["installed"]
            if checked:
                count += 1
            selections.append(Selection(label, value, initial_state=checked))
        
        with Collapsible(
            title=f"\u2714  {family_name}  ({count}/{len(family_data['items'])})",
            collapsed=False,
        ):
            yield SelectionList(*selections, id=f"sl-rules-{slug}")
```

CSS differentiates the levels:
```css
/* Family-level (inner) */
CollapsibleTitle { color: $text-muted; text-style: italic; }

/* Section-level (outer) */
Collapsible.section-collapsible > CollapsibleTitle {
    text-style: bold; color: dodgerblue;
}
```

---

## Modal screen patterns

Three modal types cover most needs:

### Confirm (returns bool)

```python
class ConfirmScreen(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, message: str):
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Static(self._message, id="modal-body")
            with Horizontal(id="modal-actions"):
                yield Button("OK", variant="success", id="yes")
                yield Button("Cancel", variant="default", id="no")

    @on(Button.Pressed, "#yes")
    def confirm(self, _) -> None: self.dismiss(True)

    @on(Button.Pressed, "#no")
    def cancel(self, _=None) -> None: self.dismiss(False)

    def action_cancel(self) -> None: self.dismiss(False)
```

Push with callback:
```python
def handle(confirmed):
    if confirmed:
        self.do_it()

self.push_screen(ConfirmScreen("Proceed?"), callback=handle)
```

### Preview (read-only, Markdown)

```python
class PreviewScreen(ModalScreen):
    BINDINGS = [Binding("escape", "dismiss", "Close")]

    def __init__(self, title: str, content: str):
        super().__init__()
        self._title = title
        self._content = content

    def compose(self) -> ComposeResult:
        with Vertical(id="preview-dialog"):
            yield Static(f"[bold]{self._title}[/]", id="modal-title")
            yield VerticalScroll(Markdown(self._content), id="modal-body")
            with Horizontal(id="modal-actions"):
                yield Button("Close [Esc]", id="close")

    @on(Button.Pressed, "#close")
    def close(self, _) -> None: self.dismiss()
```

### Results (read-only, exits app on dismiss)

```python
class ResultsScreen(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss_screen", "Done"),
        Binding("enter", "dismiss_screen", "Done"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="results-dialog"):
            yield Static("[bold green]Results[/]", id="modal-title")
            yield VerticalScroll(Static(self._results), id="modal-body")
            with Horizontal(id="modal-actions"):
                yield Button("Done [Enter]", variant="success", id="done")

    @on(Button.Pressed, "#done")
    def done(self, _) -> None: self.dismiss()

    def action_dismiss_screen(self) -> None: self.dismiss()

# Push with exit callback:
self.push_screen(ResultsScreen(text), callback=lambda _: self.exit())
```

---

## Event-driven preview updates

Two events drive the right panel:

```python
@on(SelectionList.SelectionHighlighted)
def _on_highlight(self, event) -> None:
    """User moved cursor — update preview."""
    if event.selection is None:
        return
    value = event.selection.value          # e.g. "rule:blast-radius"
    meta = self._metadata.get(value, {})
    
    lines = [
        f"[bold]{meta['name']}[/]",
        f"{meta['description']}",
        f"[dim]Status:[/] {'installed' if meta['installed'] else 'not installed'}",
        "\n[dim]Press P to view full content[/]",
    ]
    self.query_one("#preview-body", Static).update("\n".join(lines))

@on(SelectionList.SelectionToggled)
def _on_toggle(self, _event) -> None:
    """User toggled a checkbox — update count."""
    count = sum(len(sl.selected) for sl in self.query(SelectionList) if sl.id != "sl-platforms")
    self.query_one("#status-bar", Static).update(f"[bold green]{count}[/] selected")
```

---

## Gathering and acting on selections

Use prefixed values to distinguish item types across multiple SelectionLists:

```python
def action_do_install(self) -> None:
    mcps, rules, skills = [], [], []
    for sl in self.query(SelectionList):
        if sl.id == "sl-platforms":
            continue
        for val in sl.selected:
            if val.startswith("mcp:"):
                mcps.append(val.split(":", 1)[1])
            elif val.startswith("rule:"):
                rules.append(val.split(":", 1)[1])
            elif val.startswith("skill:"):
                skills.append(val.split(":", 1)[1])
    
    if not (mcps or rules or skills):
        self.notify("Nothing selected", severity="warning")
        return
    
    # Build summary → push ConfirmScreen → execute on confirm
```

---

## CSS reference

Complete CSS from the installer, annotated:

```css
/* App background */
Screen { background: $surface; }

/* Top banner — fixed height for animated content */
#banner {
    width: 100%; height: 10;
    content-align: center middle; text-align: left;
    background: $panel; color: $primary; padding: 0 2;
}

/* Main content fills remaining space */
#main-area { height: 1fr; }

/* Two-panel split */
#left-panel  { width: 2fr; border: round $primary 30%; padding: 0 1; overflow-y: auto; }
#right-panel { width: 1fr; border: round $secondary 30%; padding: 1 1; }

/* SelectionList: transparent, minimal chrome */
SelectionList {
    height: auto; max-height: 20;
    border: none; margin: 0 0 0 1; padding: 0;
    background: transparent;
}
SelectionList:focus { border: none; }
SelectionList > .selection-list--button { background: transparent; }
SelectionList:focus > .selection-list--button-highlighted { background: $boost; }
SelectionList > .selection-list--button-selected { color: $success; }

/* Collapsible: transparent, compact */
Collapsible { padding: 0 0 0 1; margin: 0; background: transparent; border: none; }
CollapsibleTitle { padding: 0; color: $text-muted; text-style: italic; }
CollapsibleTitle:hover { color: $primary; text-style: bold italic; }
CollapsibleTitle:focus { color: $primary; text-style: bold; }

/* Top-level section collapsibles */
Collapsible.section-collapsible { padding: 0; margin: 1 0 0 0; }
Collapsible.section-collapsible > CollapsibleTitle { text-style: bold; }
Collapsible.section-collapsible > CollapsibleTitle:focus { text-style: bold reverse; }

/* Section colors */
#section-platforms > CollapsibleTitle { color: dodgerblue; }
#section-mcps > CollapsibleTitle { color: red; }
#section-rules > CollapsibleTitle { color: yellow; }
#section-skills > CollapsibleTitle { color: mediumpurple; }

/* Status bar docked to bottom */
#status-bar {
    dock: bottom; height: 1;
    background: $panel; color: $text-muted; text-align: center;
}

/* Footer key hints */
Footer { background: $panel; }
Footer > .footer--key { background: $surface; color: $primary; }
Footer > .footer--description { color: $text-muted; }

/* Modal screens: centered overlay */
ConfirmScreen, PreviewScreen, ResultsScreen { align: center middle; }

/* Modal dialogs */
#confirm-dialog { width: 70; max-height: 80%; border: heavy $primary; padding: 1 2; }
#preview-dialog { width: 90%; height: 90%; border: heavy $secondary; padding: 1 2; }
#results-dialog { width: 80%; max-height: 90%; border: heavy $success; padding: 1 2; }

/* Modal layout */
#modal-title { text-align: center; text-style: bold; color: $primary; width: 100%; }
#modal-body { height: 1fr; overflow-y: auto; padding: 1 1; }
#modal-actions { height: 3; align: center middle; layout: horizontal; }

/* Buttons */
.modal-btn { margin: 0 2; }
.btn-install { background: $success; text-style: bold; }
.btn-cancel { background: $surface; }
.btn-done { background: $success; text-style: bold; }
```

---

## Full app lifecycle

1. **Parse args** — CLI flags control mode (install/uninstall), scope (global/project)
2. **Detect state** — scan filesystem, read configs, build data dicts
3. **Build app** — `compose()` creates widget tree, `_build_left_panel()` populates dynamic content
4. **User navigates** — `SelectionHighlighted` updates preview, `SelectionToggled` updates count
5. **User acts** — keybinding triggers `action_do_install()`, gathers selections
6. **Confirm** — `ConfirmScreen` shows summary, returns bool via callback
7. **Execute** — loop over selections, call install/uninstall functions, collect results
8. **Report** — `ResultsScreen` shows outcome, exits app on dismiss
