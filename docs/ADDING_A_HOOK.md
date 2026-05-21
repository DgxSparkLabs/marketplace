# Adding a Hook

Hooks fire on Claude Code lifecycle events (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `SubagentStop`). Use them for logging, enforcement, context injection, or notifications.

For the file structure, read [`examples/example-hook/README.md`](../examples/example-hook/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   mkdir -p hooks
   cp -r examples/example-hook hooks/my-hook
   ```

2. **Edit**:
   - `hooks/my-hook/.claude-plugin/plugin.json` — set `name` to `hook-my-hook`.
   - `hooks/my-hook/hooks/hooks.json` — declare your hook handlers. The file must use the `{ "description": ..., "hooks": { "<Event>": [...] } }` structure.

3. **Test your hook command standalone** before installing — if it errors or hangs in a regular shell, it will do the same when the hook fires.

4. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate hooks/my-hook
   ```

5. **Commit**.

## Auto-discovery

Claude Code auto-discovers `hooks/hooks.json` inside any plugin directory. No `hooks` field in `plugin.json` is needed.

## Hook event reference

- **`UserPromptSubmit`** — runs before Claude sees the user's prompt. Output (stdout for `command` type) is prepended to the prompt.
- **`PreToolUse`** — runs before a tool call. Optional `matcher` field scopes by tool name regex (e.g., `"Edit|Write"`). Can block via non-zero exit + stderr.
- **`PostToolUse`** — runs after a tool call completes.
- **`SessionStart`** — runs at session start.
- **`Stop`** / **`SubagentStop`** — runs when Claude or a sub-agent finishes. These are the only events that support `type: "prompt"` handlers.

## Install path after merge

```
/plugin install hook-my-hook@dgxsparklabs-marketplace
```

The hook fires automatically once enabled.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`examples/example-hook/README.md`](../examples/example-hook/README.md) — full format reference
