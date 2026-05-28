# output-style-example-multi

Reference plugin demonstrating the **multi-style layout**: one plugin ships three output styles (`Lab Notebook Voice`, `Concise Engineer`, `Tutoring`) in one `output-styles/` subdir.

## Selecting a style

```
/output-style Lab Notebook Voice
/output-style Concise Engineer
/output-style Tutoring
```

The argument is the frontmatter `name:` field of the style, NOT the plugin name. Switching styles takes effect on the next `/clear`.

## When to choose multi over single

Pick multi when you want to ship a family of voices users can A/B against (e.g. for different audiences). Pick single (`src/output-styles/example-single/`) when you have exactly one canonical voice.

## File walkthrough

```
src/output-styles/example-multi/
├── .claude-plugin/plugin.json
├── output-styles/                       ← each .md is one style; frontmatter `name:` is the slash argument
│   ├── lab-notebook-voice.md
│   ├── concise-engineer.md
│   └── tutoring.md
└── README.md
```

## Related

- Single counterpart: `src/output-styles/example-single/`
- Adding your own output-style plugin: `docs/ADDING_A_CONSTRUCT.md`
