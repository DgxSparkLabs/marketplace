# hook-example-multi

Reference plugin demonstrating the **multi-event hook layout**: one plugin's `hooks/hooks.json` handles all nine Claude hook events.

## Events covered

- `SessionStart`, `SessionEnd` — session lifecycle bookends.
- `UserPromptSubmit` — fires on every user prompt; also injects a `[Lab Notebook context: ...]` line into the prompt.
- `PreToolUse`, `PostToolUse` — fire before/after tool calls; matched on `Write|Edit`.
- `Notification` — fires when Claude wants to alert the user (e.g. tool-permission prompts).
- `Stop`, `SubagentStop` — fire when the assistant or a sub-agent ends a turn.
- `PreCompact` — fires before Claude compacts conversation history.

## Verification

```
ls /tmp/hook-fired-*.log
```

After running a Claude session, each fired event produces a sentinel file with a UTC timestamp line.

## When to choose multi over per-event

Pick multi when you want one plugin that covers the full lifecycle. Pick a per-event plugin (e.g. `src/hooks/example-userpromptsubmit/`) when you want to demonstrate or ship just one event.

## File walkthrough

```
src/hooks/example-multi/
├── .claude-plugin/plugin.json
├── hooks/hooks.json            ← top-level `hooks:` object keyed by event name; arrays of matchers + handlers
└── README.md
```

## Related

- Per-event counterparts: `src/hooks/example-<event>/` (one per event)
- Adding your own hook plugin: `docs/ADDING_A_CONSTRUCT.md`
