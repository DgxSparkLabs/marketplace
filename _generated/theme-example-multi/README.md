# theme-example-multi

Reference plugin demonstrating the **multi-theme layout**: one plugin ships three terminal themes (`Lab Notebook`, `Nord`, `Solarized Dark`) in one `themes/` subdir.

## Selecting a theme

```
/theme Lab Notebook
/theme Nord
/theme Solarized Dark
```

The argument is the JSON `name:` field of the theme, NOT the plugin name.

## When to choose multi over single

Pick multi when you want to ship a family of related themes (light/dark variants of one palette, or a color-blind-safe set). Pick single (`src/themes/example-single/`) when you have exactly one theme.

## File walkthrough

```
src/themes/example-multi/
├── .claude-plugin/plugin.json
├── themes/                       ← one JSON per theme; top-level `name:` is the slash argument
│   ├── lab-notebook.json
│   ├── nord.json
│   └── solarized-dark.json
└── README.md
```

## Related

- Single counterpart: `src/themes/example-single/`
- Adding your own theme plugin: `docs/ADDING_A_CONSTRUCT.md`
