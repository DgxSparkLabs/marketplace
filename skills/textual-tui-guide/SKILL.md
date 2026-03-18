---
name: textual-tui-guide
description: "Build rich terminal UIs with Python Textual — layouts, widgets, modals, styling"
argument-hint: "[description of the TUI to build]"
allowed-tools:
  - exec
  - read
  - edit
  - grep
  - glob
permissions:
  allow:
    - Exec(uv run)
triggers:
  - user
  - model
---

# Textual TUI Guide

Build polished terminal user interfaces with Python's Textual framework. This skill covers layout, widgets, modals, styling, key bindings, and data flow — everything needed to create interactive CLI tools that feel like real applications.

## When to use this

Use this skill when:
- The user wants to build an interactive terminal UI (not just a CLI with argparse)
- The task involves selection lists, forms, previews, multi-panel layouts, or modal dialogs
- Someone says "TUI", "terminal app", "interactive installer", "menu", or "dashboard"
- The user wants something that looks good in the terminal

## Quick start

Textual apps are single-file Python scripts runnable with `uv run` via PEP 723 inline metadata:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["textual>=1.0.0"]
# ///
```

Run with: `uv run my_tui.py`

To scaffold a new TUI project from a working skeleton, run:

```bash
uv run textual-tui-guide/scripts/scaffold_tui.py <output-path> [--name "App Name"]
```

This generates a single-file TUI with a two-panel layout, selection list, preview panel, modal dialogs, status bar, and keybindings — ready to customize.

## Architecture

Every Textual TUI follows this pattern:

```
App (top level)
├── compose()        → declares the widget tree
├── CSS              → class variable with Textual CSS
├── BINDINGS         → keyboard shortcuts
├── on_mount()       → runs after widgets are rendered
├── ModalScreen(s)   → overlay dialogs
└── event handlers   → @on() decorators for widget events
```

### The compose pattern

`compose()` is a generator that yields widgets. Use `with` blocks for containers:

```python
def compose(self) -> ComposeResult:
    yield Header(show_clock=False)
    with Horizontal(id="main"):
        with VerticalScroll(id="left"):
            yield SelectionList(...)
        with Vertical(id="right"):
            yield Static("Preview here", id="preview")
    yield Footer()
```

Key rules:
- `yield` places a widget. `with` nests widgets inside a container.
- Give widgets `id=` for CSS targeting and `self.query_one("#id", Type)` lookups.
- Use `classes=` for reusable style groups.

### Layout with CSS

Textual uses a CSS dialect (not browser CSS). Core layout properties:

```css
/* Two-panel split */
#left  { width: 2fr; }
#right { width: 1fr; }

/* Stack children vertically (default) or horizontally */
#container { layout: horizontal; }

/* Scrollable panels */
VerticalScroll { overflow-y: auto; }
```

Sizing: `fr` (fractional), `%`, fixed integers, `auto`, `1fr` (fill remaining).

### Widgets to know

| Widget | Use for |
|--------|---------|
| `Static` | Text display, labels, status bars |
| `SelectionList` | Checkboxes with values |
| `Collapsible` | Expandable/collapsible sections |
| `Header` / `Footer` | App chrome with key hints |
| `Button` | Clickable actions |
| `Markdown` | Rich markdown rendering |
| `Input` | Text input fields |
| `DataTable` | Tabular data |

### SelectionList (the workhorse)

```python
from textual.widgets import SelectionList
from textual.widgets.selection_list import Selection
from rich.text import Text

# Rich-formatted labels with values
label = Text.from_markup("[bold]item-name[/]  [dim]description[/]")
selections = [
    Selection(label, "item-value", initial_state=True),   # checked
    Selection(label2, "item-value2", initial_state=False), # unchecked
]
yield SelectionList(*selections, id="my-list")

# Reading selections
sl = self.query_one("#my-list", SelectionList)
selected_values = list(sl.selected)        # list of values
highlighted_idx = sl.highlighted           # current cursor index
option = sl.get_option_at_index(idx)       # get specific option
```

### Collapsible sections

```python
# Nested: top-level collapsible containing sub-collapsibles
with Collapsible(title="SECTION HEADER", collapsed=False, id="section-id", classes="top-level"):
    with Collapsible(title="Sub-group — description  (3/5)", collapsed=False):
        yield SelectionList(...)
```

### Modal screens

Three-step pattern: define, push, handle callback.

```python
class ConfirmScreen(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, message: str):
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static(self._message, id="modal-body")
            with Horizontal(id="modal-actions"):
                yield Button("OK", variant="success", id="confirm-yes")
                yield Button("Cancel", variant="default", id="confirm-no")

    @on(Button.Pressed, "#confirm-yes")
    def confirm(self, _event) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#confirm-no")
    def cancel(self, _event=None) -> None:
        self.dismiss(False)

    def action_cancel(self) -> None:
        self.dismiss(False)

# Push it from the main app:
def handle_result(confirmed: bool | None) -> None:
    if confirmed:
        self.do_the_thing()

self.push_screen(ConfirmScreen("Are you sure?"), callback=handle_result)
```

Modal types:
- `ModalScreen[bool]` — returns True/False (confirm/cancel)
- `ModalScreen[str]` — returns a string value
- `ModalScreen` (no type) — fire-and-forget, dismiss with no return

### Event handling

```python
from textual import on

# React to selection changes
@on(SelectionList.SelectionToggled)
def _on_toggle(self, _event) -> None:
    self._update_status_bar()

# React to cursor movement (update preview)
@on(SelectionList.SelectionHighlighted)
def _on_highlight(self, event) -> None:
    value = event.selection.value
    # update preview panel based on value

# React to button presses (scoped by ID)
@on(Button.Pressed, "#my-button")
def handle_click(self, _event) -> None:
    ...
```

### Key bindings

```python
class MyApp(App):
    BINDINGS = [
        Binding("q", "quit_app", "Quit"),
        Binding("p", "preview", "Preview"),
        Binding("i", "do_install", "Install"),
        Binding("a", "select_all", "All"),
        Binding("space", "toggle", "Toggle", show=False),  # hidden from footer
    ]

    def action_quit_app(self) -> None:
        self.exit()

    def action_preview(self) -> None:
        # Binding "p" calls action_preview automatically
        ...
```

The Footer widget automatically shows visible bindings.

### Styling cheat sheet

```css
/* Theme variables (adapt to user's terminal theme) */
background: $surface;       /* main background */
color: $text;               /* main text */
color: $text-muted;         /* secondary text */
color: $primary;            /* accent color */
background: $panel;         /* panel/bar background */
color: $success;            /* green for success states */

/* Direct colors (when theme vars aren't enough) */
color: dodgerblue;
color: mediumpurple;
color: red;
color: yellow;

/* Text styles */
text-style: bold;
text-style: italic;
text-style: bold reverse;   /* highlighted/focused state */

/* Borders */
border: round $primary 30%;    /* rounded, semi-transparent */
border: heavy $success;        /* thick solid border for modals */

/* Remove default widget chrome */
SelectionList { border: none; background: transparent; }

/* Pseudo-classes */
Widget:hover  { color: $primary; }
Widget:focus  { text-style: bold; }

/* Targeting children */
Collapsible.top-level > CollapsibleTitle { text-style: bold; color: dodgerblue; }
```

### Status bar pattern

```python
yield Static("0 items selected", id="status-bar")

def _update_status_bar(self) -> None:
    count = sum(len(sl.selected) for sl in self.query(SelectionList))
    bar = self.query_one("#status-bar", Static)
    bar.update(f"[bold green]{count}[/bold green] items selected")
```

### Querying widgets

```python
# By ID + type
preview = self.query_one("#preview-body", Static)

# All of a type
for sl in self.query(SelectionList):
    ...

# With try/except for optional widgets
try:
    widget = self.query_one("#maybe-exists", Static)
except Exception:
    pass
```

## Data flow pattern

For TUIs that manage selectable items with metadata:

1. **Store metadata in a dict** keyed by selection value:
   ```python
   self._item_metadata: dict[str, dict] = {}
   # When building selections:
   self._item_metadata["item:name"] = {"type": "rule", "name": "...", "installed": True, ...}
   ```

2. **Use prefixed values** to distinguish item types:
   ```python
   Selection(label, "mcp:fetch")    # MCP server
   Selection(label, "rule:blast")   # Rule
   Selection(label, "skill:email")  # Skill
   ```

3. **Gather selections** by iterating all SelectionLists:
   ```python
   for sl in self.query(SelectionList):
       for val in sl.selected:
           if val.startswith("mcp:"):
               selected_mcps.append(val.split(":", 1)[1])
   ```

## Reference

For a complete annotated cookbook with production-tested patterns (CSS reference, modal patterns, event handling, full app lifecycle, animated widgets), read the bundled reference:

```
@skills/textual-tui-guide/references/patterns.md
```

## Animated widgets

Subclass `Static` and use `set_interval` + `self.update()` for live-updating content:

```python
import math, colorsys

class AnimatedBanner(Static):
    def on_mount(self):
        self._angle = 0.0
        self._render_frame()
        self.set_interval(1 / 12, self._tick)  # 12 FPS

    def _tick(self):
        self._angle += 0.05
        self._render_frame()

    def _render_frame(self):
        # Compute content from self._angle, then:
        self.update(markup_string, layout=False)  # layout=False: dimensions are fixed by CSS
```

Fix banner height in CSS to prevent layout jitter: `#banner { height: 10; }`

### Smooth color gradients with HSV

Use `colorsys.hsv_to_rgb` + Rich's `rgb(r,g,b)` for smooth animated colors instead of jumping between named colors:

```python
hue = (self._angle * 0.08 + row / total_rows * 0.6) % 1.0
r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
color = f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"
line = f"[bold {color}]{content}[/]"
```

## Overriding widget keybindings

To reclaim a key from a built-in widget (e.g., free Space from CollapsibleTitle):

```python
from textual.widgets._collapsible import CollapsibleTitle
CollapsibleTitle.BINDINGS = [Binding("enter", "toggle", "Toggle")]
# Now Space is free for your own bindings
```

## Screenshot fix

Textual's built-in screenshot saves to `~/Downloads/` which may not exist. Override to ensure the directory exists:

```python
def action_screenshot(self, filename=None, path=None):
    (Path.home() / "Downloads").mkdir(parents=True, exist_ok=True)
    super().action_screenshot(filename, path)
```

## Common pitfalls

- **Forgot `id=`**: Can't query widgets without an ID. Always set `id=` on anything you'll reference later.
- **SelectionList height**: Set `height: auto; max-height: 20;` in CSS or it may collapse to zero or overflow.
- **Yielding inside `with`**: You must `yield` inside `with Container():` blocks — the context manager captures yielded widgets as children.
- **VerticalScroll focus**: Set `can_focus = False` on scroll containers so Tab skips them and goes to interactive widgets.
- **Modal return types**: `ModalScreen[bool]` needs `self.dismiss(True/False)`. Forgetting the type parameter means callbacks get `None`.
- **Rich markup in SelectionList**: Use `Text.from_markup()` for labels, not raw strings with `[bold]` tags.
- **Animation layout jitter**: Use fixed `height` in CSS for animated widgets; `auto` causes layout recalc every frame.
- **Animation rendering corruption**: `Static.update()` defaults to `layout=True`, which triggers a full layout recalculation on every call. For animated widgets with fixed CSS dimensions, always pass `layout=False` — e.g. `self.update(content, layout=False)`. Without this, repeated layout passes can cause the compositor to miscalculate dirty regions, leading to braille/color artifacts bleeding into adjacent widgets over time.
- **Named color jumps**: Use `rgb()` via HSV interpolation for smooth gradients; named color palettes look choppy when cycling.
- **Screenshot fails silently**: `~/Downloads` may not exist on headless/server systems — always mkdir first.

User arguments: $ARGUMENTS
