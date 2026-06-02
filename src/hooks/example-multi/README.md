# hook-example-multi

Reference plugin demonstrating the **multi-event hook layout**: one plugin's `hooks/hooks.json` handles all nine Claude hook events.

## Events covered

- `SessionStart`, `SessionEnd` — session lifecycle bookends.
- `UserPromptSubmit` — fires on every user prompt; also injects a `[Lab Notebook context: ...]` line into the prompt.
- `PreToolUse`, `PostToolUse` — fire before/after tool calls; matched on `Write|Edit`.
- `Notification` — fires when Claude wants to alert the user (e.g. tool-permission prompts).
- `Stop`, `SubagentStop` — fire when the assistant or a sub-agent ends a turn.
- `PreCompact` — fires before Claude compacts conversation history.

## A "debug example" — every handler logs its stdin payload

These hooks are written as **debug references**: each handler reads the hook's JSON
payload from **stdin** (`p="$(cat)"`) and appends a timestamped marker **plus that
full payload** to `/tmp/hook-fired-<event>.log`. So the sentinel isn't just "it
fired" — it's a record of *exactly what Claude sends each event*, which is the
single most useful thing to know when writing your own hook.

> **Read the payload from stdin, not the environment.** A common mistake (which an
> earlier version of this example made) is to read `${CLAUDE_TOOL_NAME}` from the
> environment — it is **not populated**. The tool name, tool input, file paths,
> session id, etc. all arrive as JSON on **stdin**. The `PreToolUse` sentinel makes
> this concrete, e.g.:
> ```json
> {"hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":".../clean.py","old_string":"...","new_string":"..."},"tool_use_id":"toolu_...","cwd":"...","session_id":"..."}
> ```

## Verification

```
ls /tmp/hook-fired-*.log
cat /tmp/hook-fired-pretooluse.log        # marker line + the full JSON payload
# pretty-print the payloads if you have jq:
grep -v ' fired$' /tmp/hook-fired-pretooluse.log | jq .
```

After running a Claude session, each fired event produces a sentinel file containing a UTC timestamp + marker line followed by the verbatim JSON payload.

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
