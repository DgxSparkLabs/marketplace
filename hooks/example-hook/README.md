# example-hook

Reference plugin for the **hook** construct type. Copy this directory to scaffold your own.

## What it does

Installs a `UserPromptSubmit` hook that prepends a timestamp marker to every prompt the user sends. Claude sees it; the user does not. Demonstrates the hook output-prepend pattern.

Install:
```
/plugin install example-hook@dgxsparklabs-marketplace
```

After install, every prompt you type gets a `[Lab Notebook context: timestamp=...]` line prepended invisibly.

## File-by-file walkthrough

```
example-hook/
├── .claude-plugin/plugin.json    ← minimal manifest (no "hooks" field needed)
├── hooks/
│   └── hooks.json                ← hook configuration (auto-discovered)
└── README.md
```

**Auto-discovery:** Claude Code automatically picks up `hooks/hooks.json` in the plugin root — you do NOT need to declare a `hooks` field in `plugin.json`. The file at `hooks/hooks.json` is discovered by convention.

### `hooks/hooks.json` structure

The outer object has two keys:

- `description` — what the hook does (shown in plugin details)
- `hooks` — object mapping lifecycle events to handler arrays

Lifecycle events include `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `SubagentStop`, etc. Each handler is one of:

- `type: "command"` — runs a shell command; stdout becomes the hook's contribution to context (for input-stage hooks like `UserPromptSubmit`)
- `type: "http"` — POSTs the event to a URL; response body becomes the contribution
- `type: "prompt"` — only valid for `Stop` and `SubagentStop` events

The optional `matcher` field on a handler block scopes it (e.g., `"matcher": "Edit|Write|MultiEdit"` for PreToolUse hooks that only fire on those specific tools).

Multiple plugins can register hooks for the same event — they all fire and their outputs compose.

## Hooks vs everything else

Hooks are for **side-effecting at lifecycle moments** (log, enforce, inject context). If you need behavior that lives between prompts and tool calls, hooks are right. For behavioral guidance Claude follows, use rules. For domain expertise, use skills.

## To make your own hook from this template

1. `cp -r examples/example-hook hooks/my-hook`
2. Edit `.claude-plugin/plugin.json` and `hooks/hooks.json`.
3. Test the shell command standalone first — if it fails or hangs, the hook will too.
4. `uv run scripts/generate_manifest.py` and commit.

See `docs/ADDING_A_HOOK.md` for the full list of supported events and field semantics.
