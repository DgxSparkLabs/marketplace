# monitor-example-multi

Reference plugin demonstrating the **multi-monitor layout**: one plugin ships three monitors (`disk-usage`, `memory-usage`, `git-status`) in one `monitors.json` array.

## Behavior

Each monitor runs its `command` once at session start. The output is surfaced to Claude as observation context.

## When to choose multi over single

Pick multi when you have multiple thematically related observations to surface at session start (e.g. an "environment health" toolbox). Pick single (`src/monitors/example-single/`) when you have exactly one.

## File walkthrough

```
src/monitors/example-multi/
├── .claude-plugin/plugin.json
├── monitors/monitors.json      ← top-level array; one object per monitor with {name, command, description}
└── README.md
```

## Related

- Single counterpart: `src/monitors/example-single/`
- Adding your own monitor plugin: `docs/ADDING_A_CONSTRUCT.md`
