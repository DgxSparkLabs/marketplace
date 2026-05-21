# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Scaffold a new Textual TUI project.

Generates a single-file TUI with two-panel layout, selection list,
preview panel, modal dialogs, status bar, and keybindings.

Usage:
    uv run scaffold_tui.py output.py
    uv run scaffold_tui.py output.py --name "My Dashboard"
"""
from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATE = '''\
# /// script
# requires-python = ">=3.11"
# dependencies = ["textual>=1.0.0"]
# ///
"""
{title} — interactive terminal UI.

Usage:
    uv run {filename}
"""
from __future__ import annotations

import argparse
import sys

# ── Data ────────────────────────────────────────────────────────────────────

ITEMS = {{
    "Section A": {{
        "description": "First group of items",
        "members": [
            {{"name": "alpha", "description": "First item"}},
            {{"name": "beta", "description": "Second item"}},
            {{"name": "gamma", "description": "Third item"}},
        ],
    }},
    "Section B": {{
        "description": "Second group of items",
        "members": [
            {{"name": "delta", "description": "Fourth item"}},
            {{"name": "epsilon", "description": "Fifth item"}},
        ],
    }},
}}

# ── CSS ─────────────────────────────────────────────────────────────────────

APP_CSS = """
Screen {{ background: $surface; }}

#banner {{
    width: 100%; height: 1;
    content-align: center middle; text-align: center;
    background: $panel; color: $primary; text-style: bold;
}}

#main-area {{ height: 1fr; }}

#left-panel {{
    width: 2fr;
    border: round $primary 30%;
    padding: 0 1;
    overflow-y: auto;
}}

#right-panel {{
    width: 1fr;
    border: round $secondary 30%;
    padding: 1 1;
}}

SelectionList {{
    height: auto; max-height: 20;
    border: none; margin: 0 0 0 1; padding: 0;
    background: transparent;
}}

SelectionList:focus {{ border: none; }}
SelectionList > .selection-list--button {{ background: transparent; }}
SelectionList:focus > .selection-list--button-highlighted {{ background: $boost; }}
SelectionList > .selection-list--button-selected {{ color: $success; }}

Collapsible {{
    padding: 0 0 0 1; margin: 0;
    background: transparent; border: none;
}}

CollapsibleTitle {{
    padding: 0; color: $text-muted; text-style: italic;
    width: 100%; background: transparent;
}}

CollapsibleTitle:hover {{ color: $primary; text-style: bold italic; }}
CollapsibleTitle:focus {{ color: $primary; text-style: bold; }}

#preview-body {{ padding: 1 0; color: $text; }}

#status-bar {{
    dock: bottom; height: 1;
    background: $panel; color: $text-muted; text-align: center;
}}

Footer {{ background: $panel; }}
Footer > .footer--key {{ background: $surface; color: $primary; }}
Footer > .footer--description {{ color: $text-muted; }}

/* Modal screens */
ConfirmScreen, ResultsScreen {{ align: center middle; }}

#confirm-dialog {{
    width: 70; max-height: 80%;
    border: heavy $primary; background: $surface; padding: 1 2;
}}

#results-dialog {{
    width: 80%; max-height: 90%;
    border: heavy $success; background: $surface; padding: 1 2;
}}

#modal-title {{
    text-align: center; text-style: bold;
    color: $primary; width: 100%; padding: 0 0 1 0;
}}

#modal-body {{
    height: 1fr; overflow-y: auto; padding: 1 1; color: $text;
}}

#modal-actions {{
    height: 3; align: center middle;
    layout: horizontal; padding: 1 0 0 0;
}}

.modal-btn {{ margin: 0 2; }}
"""


# ── TUI ─────────────────────────────────────────────────────────────────────

def main():
    from textual import on
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Horizontal, Vertical, VerticalScroll
    from textual.screen import ModalScreen
    from textual.widgets import (
        Button, Collapsible, Footer, Header,
        SelectionList, Static,
    )
    from textual.widgets.selection_list import Selection
    from rich.text import Text

    # ── Confirm Modal ──
    class ConfirmScreen(ModalScreen[bool]):
        BINDINGS = [Binding("escape", "cancel", "Cancel")]

        def __init__(self, message: str):
            super().__init__()
            self._message = message

        def compose(self) -> ComposeResult:
            with Vertical(id="confirm-dialog"):
                yield Static("[bold]Confirm[/]", id="modal-title")
                yield Static(self._message, id="modal-body")
                with Horizontal(id="modal-actions"):
                    yield Button("OK", variant="success", classes="modal-btn", id="confirm-yes")
                    yield Button("Cancel", variant="default", classes="modal-btn", id="confirm-no")

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
                yield Static("[bold green]Results[/]", id="modal-title")
                yield VerticalScroll(Static(self._results), id="modal-body")
                with Horizontal(id="modal-actions"):
                    yield Button("Done [Enter]", variant="success", classes="modal-btn", id="results-done")

        @on(Button.Pressed, "#results-done")
        def done(self, _event) -> None:
            self.dismiss()

        def action_dismiss_screen(self) -> None:
            self.dismiss()

    # ── Main App ──
    class {app_class}(App):
        CSS = APP_CSS
        TITLE = "{title}"
        BINDINGS = [
            Binding("q", "quit_app", "Quit"),
            Binding("p", "preview", "Preview"),
            Binding("i", "do_action", "Go"),
            Binding("a", "select_all", "All"),
            Binding("n", "select_none", "None"),
        ]

        def __init__(self):
            super().__init__()
            self._metadata: dict[str, dict] = {{}}

        def compose(self) -> ComposeResult:
            yield Header(show_clock=False)
            yield Static(
                "[bold dodger_blue2]\\u2550\\u2550\\u2550[/] "
                "[bold white]{title}[/] "
                "[bold dodger_blue2]\\u2550\\u2550\\u2550[/]",
                id="banner",
            )
            with Horizontal(id="main-area"):
                left = VerticalScroll(id="left-panel")
                left.can_focus = False
                with left:
                    yield from self._build_left_panel()
                with Vertical(id="right-panel"):
                    yield Static(
                        "[bold]Preview[/]\\n\\n"
                        "[dim]Navigate with arrow keys.\\n"
                        "Space to toggle. P to preview.\\n"
                        "I to execute action.[/]",
                        id="preview-body",
                    )
            yield Static("[bold]0 items selected[/]", id="status-bar")
            yield Footer()

        def on_mount(self) -> None:
            try:
                first = list(self.query(SelectionList))[0]
                first.focus()
            except (IndexError, Exception):
                pass

        def _build_left_panel(self):
            for section_name, section in ITEMS.items():
                selections = []
                for item in section["members"]:
                    label = Text.from_markup(
                        f"[bold]{{item['name']}}[/]  [dim]{{item['description']}}[/]"
                    )
                    value = f"item:{{item['name']}}"
                    selections.append(Selection(label, value, initial_state=False))
                    self._metadata[value] = item

                slug = section_name.lower().replace(" ", "-")
                with Collapsible(
                    title=f"{{section_name}}  \\u2014  {{section['description']}}",
                    collapsed=False,
                ):
                    yield SelectionList(*selections, id=f"sl-{{slug}}")

        def _count_selected(self) -> int:
            return sum(len(sl.selected) for sl in self.query(SelectionList))

        def _update_status(self) -> None:
            count = self._count_selected()
            self.query_one("#status-bar", Static).update(
                f"[bold green]{{count}}[/bold green] items selected"
            )

        @on(SelectionList.SelectionToggled)
        def _on_toggle(self, _event) -> None:
            self._update_status()

        @on(SelectionList.SelectionHighlighted)
        def _on_highlight(self, event) -> None:
            if event.selection is None:
                return
            meta = self._metadata.get(event.selection.value, {{}})
            if not meta:
                return
            preview = self.query_one("#preview-body", Static)
            preview.update(
                f"[bold]{{meta.get('name', '')}}[/]\\n\\n"
                f"{{meta.get('description', '')}}\\n\\n"
                "[dim]Press P for full details[/]"
            )

        def action_quit_app(self) -> None:
            self.exit()

        def action_preview(self) -> None:
            focused = self.focused
            if not isinstance(focused, SelectionList):
                self.notify("Focus a list first", severity="warning")
                return
            idx = focused.highlighted
            if idx is None:
                return
            option = focused.get_option_at_index(idx)
            meta = self._metadata.get(option.value, {{}})
            name = meta.get("name", option.value)
            self.notify(f"Preview: {{name}}", severity="information")

        def action_select_all(self) -> None:
            focused = self.focused
            if isinstance(focused, SelectionList):
                focused.select_all()
                self._update_status()

        def action_select_none(self) -> None:
            focused = self.focused
            if isinstance(focused, SelectionList):
                focused.deselect_all()
                self._update_status()

        def action_do_action(self) -> None:
            selected = []
            for sl in self.query(SelectionList):
                for val in sl.selected:
                    if isinstance(val, str):
                        selected.append(val.split(":", 1)[1])

            if not selected:
                self.notify("Nothing selected", severity="warning")
                return

            summary = f"[bold]Selected {{len(selected)}} items:[/]\\n"
            for s in selected:
                summary += f"  \\u2022 {{s}}\\n"

            def handle_confirm(confirmed):
                if confirmed:
                    self._execute(selected)

            self.push_screen(ConfirmScreen(summary), callback=handle_confirm)

        def _execute(self, selected: list[str]) -> None:
            lines = []
            for name in selected:
                lines.append(f"  [green]\\u2714[/] {{name}}")
            results = f"[bold green]Done![/] Processed {{len(selected)}} items.\\n\\n" + "\\n".join(lines)
            self.push_screen(ResultsScreen(results), callback=lambda _: self.exit())

    app = {app_class}()
    app.run()


if __name__ == "__main__":
    main()
'''


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new Textual TUI project")
    parser.add_argument("output", help="Output file path (e.g., my_tui.py)")
    parser.add_argument("--name", default="My TUI", help="App title (default: 'My TUI')")
    args = parser.parse_args()

    output = Path(args.output)
    title = args.name
    filename = output.name
    # Convert title to PascalCase class name
    app_class = "".join(word.capitalize() for word in title.split()) + "App"

    content = TEMPLATE.format(
        title=title,
        filename=filename,
        app_class=app_class,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content)
    print(f"Created {output}")
    print(f"Run with: uv run {output}")


if __name__ == "__main__":
    main()
