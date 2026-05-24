# example-theme

Reference plugin for the **theme** construct type. Copy this directory to scaffold your own.

## What it does

Ships a UI theme named `Lab Notebook` with a muted, paper-toned palette (Solarized Light derivatives). Users select it via Claude Code's `/theme` picker.

Install:
```
/plugin install example-theme@dgxsparklabs-marketplace
```

> Themes are an experimental construct. The plugin.json field is `experimental.themes`, reflecting that the API may change.

## File-by-file walkthrough

```
example-theme/
├── .claude-plugin/plugin.json     ← manifest with "experimental.themes": "./themes"
├── themes/
│   └── lab-notebook.json          ← the theme itself
└── README.md
```

### `themes/<name>.json`

A JSON file declaring color tokens. The exact schema is in flux as themes mature in Claude Code; consult the latest docs before shipping. This example uses a minimal token set (`background`, `foreground`, `accent`, `warning`, `error`, `success`, `muted`) suitable for most terminal UIs.

## When to use a theme plugin

- You want to distribute a team color scheme.
- You want to pair UI styling with other plugin components (e.g., a theme that complements a specific output style).

For personal taste tweaks, the built-in `/theme` picker and config file is usually enough — no plugin needed.

## To make your own theme from this template

1. `cp -r examples/example-theme themes/my-theme`
2. Edit `.claude-plugin/plugin.json` and the theme JSON.
3. Test in Claude Code — check contrast and readability in your terminal.
4. `uv run scripts/generate_manifest.py` and commit.

See `docs/ADDING_A_THEME.md` for the full token schema. Themes are experimental; the field naming may change.
