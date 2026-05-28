# command-example-multi

Reference plugin demonstrating the **multi-command layout**: one plugin ships three slash commands (`hello`, `goodbye`, `ping`) under a single `commands/` subdir.

## Slash forms (after install + enable)

- `/dgxsparklabs-command-example-multi:hello` — lab-notebook header
- `/dgxsparklabs-command-example-multi:goodbye` — lab-notebook footer
- `/dgxsparklabs-command-example-multi:ping` — minimal liveness check

## When to choose multi over single

Pick multi when you have multiple thematically related commands you want to ship together — one install brings them all. Pick single (see `src/commands/example-single/`) when your plugin has exactly one command.

## File walkthrough

```
src/commands/example-multi/
├── .claude-plugin/plugin.json   ← name + marketplace-listing description
├── commands/
│   ├── hello.md                 ← one file per command; frontmatter `description:` becomes the autocomplete tooltip
│   ├── goodbye.md
│   └── ping.md
└── README.md                    ← you are here
```

## Related

- Single counterpart: `src/commands/example-single/`
- Adding your own command plugin: `docs/ADDING_A_CONSTRUCT.md`
