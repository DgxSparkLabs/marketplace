# example-output-style

Reference plugin for the **output style** construct type. Copy this directory to scaffold your own.

## What it does

Ships an output style named `Lab Notebook Voice` that, when selected, makes Claude write responses in a measured, citation-focused style. Not force-applied — users opt in via Claude Code's output style picker.

Install:
```
/plugin install example-output-style@marketplace
```

Then in Claude Code, switch to the style via `/output-style Lab Notebook Voice` (or similar — depends on UI).

## File-by-file walkthrough

```
example-output-style/
├── .claude-plugin/plugin.json         ← manifest with "outputStyles": "./output-styles"
├── output-styles/
│   └── lab-notebook-voice.md          ← the style itself
└── README.md
```

### `output-styles/<name>.md`

YAML frontmatter declares metadata:

- `name` — human-readable name (shown in the picker).
- `description` — one-line summary.
- `keep-coding-instructions: true` — preserves Claude's default code-task behavior alongside the style overlay.
- `force-for-plugin: true` (NOT set in this example) — when set, the style auto-applies whenever the plugin is enabled, without user selection. Useful for shipping team-wide conventions. Only one force-for-plugin style can be active at once.

The body is markdown — it becomes part of Claude's system prompt when the style is active.

## When to use an output style

- **Voice/tone adjustments** — "respond like a peer reviewer", "write like documentation".
- **Format constraints** — "always end with a Next: step", "always include code citations".
- **Always-on team conventions** — set `force-for-plugin: true` to apply automatically.

For project-specific conventions, a CLAUDE.md or rule is usually a better fit. For tone/format that applies across all projects, output styles are right.

## To make your own output style from this template

1. `cp -r examples/example-output-style output-styles/my-style`
2. Edit `.claude-plugin/plugin.json` and the style markdown file.
3. Decide: user-selectable (no `force-for-plugin`) or auto-applied (`force-for-plugin: true`)?
4. `uv run scripts/generate_manifest.py` and commit.

See `docs/ADDING_AN_OUTPUT_STYLE.md` for the full frontmatter spec.
