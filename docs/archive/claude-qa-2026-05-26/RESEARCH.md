---
date: 2026-05-26
purpose: research-for-claude-qa-fixes
arc: claude/qa-and-user-guide
status: draft-for-discussion
operator-qa-date: 2026-05-26
docs-fetch-date: 2026-05-26
---

# Claude QA Findings — Research and Recommendations

A diagnosis pass for the nine findings the operator surfaced during Docker QA on 2026-05-26. Each finding pairs Claude's canonical doc behavior (fetched 2026-05-26 from `code.claude.com/docs/en/...`) with the current source/generated state and produces an actionable fix the implementer can apply mechanically. Source-of-truth files cited as `path:line` ranges; doc claims cited as URL + fetch date.

## TL;DR

- **Six confirmed bugs**, all mechanical fixes: marketplace.json missing `description`; `lsp-example` wraps the LSP server config under a redundant `lspServers` key AND uses the wrong field name (`fileExtensions` vs `extensionToLanguage`); `monitor-example` ships an object-with-named-keys instead of an array; `theme-example` uses an invented `{name, description, colors}` schema (Claude wants `{name, base, overrides}`); `hook-example` fires correctly but emits a `[Lab Notebook context: ...]` line to stdout which `UserPromptSubmit` injects as context (operator-invisible by design — the symptom is a verification gap, not a hook failure); `mcp-example` needs a `uv` prerequisite documented.
- **Three investigation answers, all decisive**:
  - **Rules are NOT a Claude plugin component.** The official component list (`code.claude.com/docs/en/plugins-reference#plugin-components-reference`, 2026-05-26) is: Skills, Agents, Hooks, MCP servers, LSP servers, Monitors, Themes, Output Styles. Claude reads rules from `.claude/rules/*.md` (memory subsystem). **Verdict: remove `RuleConstruct` from `ClaudeCodePlatform.supports` and stop emitting `_generated/rule-<name>/`.**
  - **Slash command namespacing is mandatory** and there is no flatten mechanism. Per `code.claude.com/docs/en/plugins` (2026-05-26): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name. To change the namespace prefix, update the `name` field in `plugin.json`."* Renaming plugins to shorter forms is the only lever. The `/example-skill` operator observation is misread: that's the skill name being the same word as the plugin name suffix, not a flat invocation.
  - **Output-style activation IS observable**: it's persisted to `.claude/settings.local.json` under `"outputStyle": "<Name>"` (per `code.claude.com/docs/en/output-styles`, 2026-05-26), and the picker confirms after `/clear`. Validation method: pick style → `/clear` → ask for a code summary → expect lab-notebook prose markers from the SKILL.md spec.
- **The single most impactful finding** is the rule deprecation verdict (Finding 8). It changes `ClaudeCodePlatform.supports`, removes 22 stranded `_generated/rule-<name>/` plugin directories from the marketplace listing for Claude consumers, and unblocks the verified-working end-to-end state. Discuss this first.

## Finding 1 — marketplace.json description warning

### Symptom (operator's observation)

```
claude plugin validate /workspace/marketplace/
⚠ Found 1 warning:
  ❯ description: No marketplace description provided. Adding a description helps users understand what this marketplace offers
✔ Validation passed with warnings
```

### Claude's expected schema

Per `code.claude.com/docs/en/plugin-marketplaces#marketplace-schema` (fetched 2026-05-26):

> ### Optional fields
> | `description` | string | Brief marketplace description |
> | `version`     | string | Marketplace manifest version |

And per `code.claude.com/docs/en/plugins-reference#unrecognized-fields` (fetched 2026-05-26):

> Pass `--strict` to treat warnings as errors. Use it in CI to catch a misspelled field name or a field left over from another tool's manifest before publishing, even though the plugin would load at runtime.

So `description` is a **top-level optional field of marketplace.json itself**, not inside a per-plugin entry, and not nested under `metadata` (though `metadata.description` is accepted for backward compatibility per the same doc).

### Current state

`.claude-plugin/marketplace.json:1-7` — the top-level object has `name`, `owner`, `plugins`, but no `description`. Each plugin entry has its own `description` (e.g. line 11), which satisfies the per-plugin field but not the marketplace-level field.

### Root cause

The marketplace generator (`scripts/generator.py` or equivalent — see also `scripts/utils.py::_marketplace_description`, which is already used by `GeminiPlatform.emit_extension_manifest` at `scripts/platforms.py:280`) computes a description for Gemini's extension manifest but never injects it into the Claude marketplace.json output.

### Recommended fix

Add a top-level `description` to `.claude-plugin/marketplace.json` between `owner` and `plugins`:

```json
{
  "name": "dgxsparklabs-marketplace",
  "owner": { "name": "DgxSparkLabs", "url": "https://github.com/DgxSparkLabs" },
  "description": "Cross-platform AI agent skills, rules, and reference plugins for Claude Code, Codex, Gemini, Cursor, Windsurf, and Devin.",
  "plugins": [ ... ]
}
```

Implementation: have the generator write `description: _marketplace_description()` into the marketplace.json top-level dict before emitting. The helper already exists in `scripts/utils.py` and is consumed by `GeminiPlatform.emit_extension_manifest` (`scripts/platforms.py:280`), so this is a 1-line dict-key addition to whichever phase writes `marketplace.json`.

### CI check recommendation

The QA step is already aware of `--strict`. Add to the Claude CI workflow:

```bash
claude plugin validate . --strict
```

`--strict` per the docs *"treats warnings as errors"*, which catches both this case and any future unrecognized-field drift. If `--strict` is not yet supported in the CI Claude version, fall back to grepping the non-strict output:

```bash
out=$(claude plugin validate .)
echo "$out"
if echo "$out" | grep -q 'warning'; then echo "ERROR: warnings present"; exit 1; fi
```

This can fold into the existing test-suite shell harness — no new commit needed if the marketplace.json edit lands alongside the CI tweak.

## Finding 2 — lsp-example manifest schema is broken

### Symptom (operator's observation)

```
1 error:
  Invalid LSP server config for "./lsp-config.json": [
    { "expected": "string", "code": "invalid_type", "path": ["lspServers", "command"], ... },
    { "expected": "record", "code": "invalid_type", "path": ["lspServers", "extensionToLanguage"], ... },
    { "code": "unrecognized_keys", "keys": ["example-markdown"], "path": ["lspServers"], ... }
  ]
```

### Claude's expected schema

Per `code.claude.com/docs/en/plugins-reference#lsp-servers` (fetched 2026-05-26), the `.lsp.json` file format is:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

**Top-level keys ARE the language-server identifiers.** There is no outer `lspServers` wrapper in the standalone `.lsp.json` file. The outer `lspServers` wrapper only appears when the config is *inlined into plugin.json*:

```json
{
  "name": "my-plugin",
  "lspServers": { "go": { "command": "gopls", ... } }
}
```

**Required fields per server:** `command` (string), `extensionToLanguage` (record of `.ext` → `language-id`). Note: `extensionToLanguage`, NOT `fileExtensions`.

The canonical filename is `.lsp.json` at plugin root (not `lsp-config.json`), per the file locations table in the same doc.

### Current state

Source: `lsp-servers/example/lsp-config.json:1-9`:
```json
{
  "lspServers": {
    "example-markdown": {
      "command": "marksman",
      "args": ["server"],
      "fileExtensions": [".md"]    // ← wrong field name
    }
  }
}
```

Generated: `_generated/lsp-example/lsp-config.json:1-9` — identical (verbatim copy).

Generated plugin.json: `_generated/lsp-example/.claude-plugin/plugin.json:9` — `"lspServers": "./lsp-config.json"` (correct: a string path pointer to the standalone file).

### Root cause

Two compounding bugs in `lsp-servers/example/lsp-config.json`:

1. **Wrong wrapping**: The file is a standalone `.lsp.json` (referenced as `./lsp-config.json` from plugin.json's `lspServers` field). Standalone `.lsp.json` files have language IDs as top-level keys. We wrapped them under an extra `lspServers` key — that's the schema shape for the *inline* variant.
2. **Wrong field name**: `fileExtensions: [".md"]` is invented. The Claude spec uses `extensionToLanguage: { ".md": "markdown" }` — an object mapping `.ext` → language identifier.

The validator's three errors map cleanly:
- `path: ["lspServers", "command"] expected string received undefined` — because the validator descends `lspServers.example-markdown` looking for `command`, but the top-level key it found is `example-markdown`, not the expected language-id with `command` directly under it
- `path: ["lspServers", "extensionToLanguage"] expected record received undefined` — same descent path, no `extensionToLanguage`
- `unrecognized_keys: ["example-markdown"]` — when the validator treats the outer dict as `lspServers` map, the value under `example-markdown` is a server-config object, but the validator expected language IDs at that level

### Recommended fix

Rewrite `lsp-servers/example/lsp-config.json` to match Claude's spec:

```json
{
  "markdown": {
    "command": "marksman",
    "args": ["server"],
    "extensionToLanguage": {
      ".md": "markdown"
    }
  }
}
```

Optionally rename the file to `.lsp.json` and update `lsp-servers/example/.claude-plugin/plugin.json:14` (`"lspServers": "./lsp-config.json"`) to `"lspServers": "./.lsp.json"` — but the current path-via-string is valid per the schema (`lspServers` accepts `string | array | object`), so keeping `lsp-config.json` as the filename is acceptable.

`scripts/constructs.py::LSPConstruct.build_plugin_json` (lines 295-302) currently passes the source `lspServers` value through verbatim, so no code change is needed there once the source file is corrected. The generated file `_generated/lsp-example/lsp-config.json` will be a verbatim copy of the source post-`emit`, so this single edit fixes both source and generated states.

If the marksman binary isn't realistic for QA hosts, switching to a generic example is fine — e.g. use `gopls`+`.go` from the doc as the canonical example to mirror Claude's own docs exactly.

## Finding 3 — monitor-example JSON shape error (array vs object)

### Symptom (operator's observation)

```
1 error:
  Failed to load monitors from /workspace/marketplace/_generated/monitor-example/monitors/monitors.json: [
    { "expected": "array", "code": "invalid_type", "path": [], "message": "Invalid input: expected array, received object" }
  ]
```

### Claude's expected schema

Per `code.claude.com/docs/en/plugins-reference#monitors` (fetched 2026-05-26):

> **Format**: JSON array of monitor entries
>
> ```json
> [
>   {
>     "name": "deploy-status",
>     "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh ${user_config.api_endpoint}",
>     "description": "Deployment status changes"
>   },
>   {
>     "name": "error-log",
>     "command": "tail -F ./logs/error.log",
>     "description": "Application error log",
>     "when": "on-skill-invoke:debug"
>   }
> ]
> ```
>
> **Required fields**: `name`, `command`, `description`.
> **Optional fields**: `when` (`"always"` default, or `"on-skill-invoke:<skill>"`).

The top-level value is an **array of monitor objects**. Each monitor object has `name`/`command`/`description`. No `args`, no `intervalSeconds` — long-running shell commands deliver each stdout line as a notification (so polling-style scripts use a loop inside `command`, and one-shot snapshots don't fit the schema as-is).

### Current state

Source: `monitors/example/monitors/monitors.json:1-10`:
```json
{
  "monitors": {
    "example-disk": {
      "command": "df",
      "args": ["-h", "."],
      "intervalSeconds": 300,
      "description": "Sample disk usage every 5 minutes and surface to Claude on demand."
    }
  }
}
```

Generated: `_generated/monitor-example/monitors/monitors.json:1-10` — identical verbatim copy.

Plugin manifest at `_generated/monitor-example/.claude-plugin/plugin.json:10` correctly points `experimental.monitors: ./monitors/monitors.json` (a path to the standalone file).

### Root cause

The source JSON uses an outer `{"monitors": {...}}` wrapper with named entries, mirroring the LSP file's structure. That's not the monitors schema — monitors are a flat top-level array. Additionally, `args` is not a top-level monitor field (the entire shell command lives in `command`), and `intervalSeconds` is not a documented field — polling is expressed by wrapping the command in `while sleep 300; do ...; done`.

### Recommended fix

Rewrite `monitors/example/monitors/monitors.json` to a top-level array with three monitor fields:

```json
[
  {
    "name": "example-disk",
    "command": "while sleep 300; do df -h . | tail -n +2; done",
    "description": "Sample disk usage every 5 minutes and surface to Claude as notifications."
  }
]
```

The polling pattern is correct: each `df -h .` invocation prints lines to stdout; the monitor delivers each line as a notification. `sleep 300` enforces the 5-minute interval. For a one-shot "current disk state" delivered once at session start, drop the loop:

```json
[
  {
    "name": "example-disk",
    "command": "df -h . | tail -n +2",
    "description": "Report current disk usage once at session start."
  }
]
```

Either form is schema-valid; the operator should pick the one that matches the demo's intent. Recommend the second (one-shot) since it produces a single visible notification and is easier to verify hands-on.

No code change is needed in `scripts/constructs.py::MonitorConstruct.emit` (lines 330-337) — it does a `shutil.copytree` of the source dir, so fixing the source file fixes the generated file on next regenerate.

## Finding 4 — theme-example not actually distinct from default

### Symptom (operator's observation)

> "Lab Notebook (from theme-example) — this theme seems to be 1:1 with the Dark mode default theme?"

### Claude's expected schema

Per `code.claude.com/docs/en/plugins-reference#themes` (fetched 2026-05-26):

> A theme is a JSON file in `themes/` with a `base` preset and a sparse `overrides` map of color tokens.
>
> ```json
> {
>   "name": "Dracula",
>   "base": "dark",
>   "overrides": {
>     "claude": "#bd93f9",
>     "error": "#ff5555",
>     "success": "#50fa7b"
>   }
> }
> ```
>
> Selecting a plugin theme persists `custom:<plugin-name>:<slug>` in the user's config.

**Required fields**: `name`, `base`, `overrides`. `base` accepts a Claude preset name (`"dark"`, `"light"`, etc. — the doc shows `"dark"` and references "built-in presets"; the exact list isn't enumerated in the plugins-reference but `dark`/`light` are implied). `overrides` is a sparse object — only the tokens you want to change. Theme is experimental, so the manifest pointer is `experimental.themes`.

### Current state

Source: `themes/example/themes/lab-notebook.json:1-13`:
```json
{
  "name": "Lab Notebook",
  "description": "Muted, paper-toned theme suited to long reading sessions. Reference example only.",
  "colors": {
    "background": "#fdf6e3",
    "foreground": "#586e75",
    "accent": "#268bd2",
    "warning": "#cb4b16",
    "error": "#dc322f",
    "success": "#859900",
    "muted": "#93a1a1"
  }
}
```

Generated: `_generated/theme-example/themes/lab-notebook.json` — identical verbatim copy. Plugin.json correctly emits `experimental.themes: ./themes` (a directory pointer — the schema accepts string|array).

### Root cause

The theme file uses an invented schema: `{name, description, colors: {...}}`. Claude's loader expects `{name, base, overrides: {...}}`. Unrecognized top-level fields (`description`, `colors`) are ignored per the plugins-reference's *"Unrecognized fields"* rule. Without `base`, Claude probably falls back to the loaded default (likely "dark" or the user's previously selected theme), explaining the operator's "1:1 with Dark mode default" observation. The user's `colors.background: #fdf6e3` (Solarized Light cream) never reaches the renderer because `colors` is not a recognized key.

Note: the source file uses Solarized-palette hex values; visually this would clearly diverge from default-dark if it were being applied. The fact that it doesn't visibly differ is the proof that the loader is silently rejecting the unrecognized keys.

### Recommended fix

Rewrite `themes/example/themes/lab-notebook.json` to the canonical schema. Use `base: "light"` (paper-toned theme) and put the distinctive colors in `overrides`:

```json
{
  "name": "Lab Notebook",
  "base": "light",
  "overrides": {
    "claude": "#268bd2",
    "error": "#dc322f",
    "success": "#859900"
  }
}
```

Keep the override set small — the doc emphasizes "sparse overrides". If `base: "light"` provides the cream background already, no `background` override is needed; if a distinct paper-tone is desired, add `"background": "#fdf6e3"` once the actual override key name is confirmed in a live `/theme` test (the plugins-reference doesn't enumerate every override key; the `claude`/`error`/`success` keys shown in the Dracula example are the documented examples).

**Verification after fix**: in `/theme` menu, the Lab Notebook entry should show a *light* color preview vs the default dark; selecting it should visibly change the foreground/background. If the live test shows the override keys don't include `background` (i.e. only foreground-text tokens are overridable), this becomes an explicit limitation — the example then highlights the contrast between Claude-customizable tokens and locked tokens.

No code change in `scripts/constructs.py::ThemeConstruct.emit` (lines 380-387) — verbatim copy is correct once the source is fixed.

## Finding 5 — hook-example not firing + needs full hook-type coverage

### Symptom (operator's observation)

> "hook-example did not seem to do anything. also we need a example per each hook type that's available for Claude not just `UserPromptSubmit`"

### Claude's expected hook schema

Per `code.claude.com/docs/en/plugins-reference#hooks` and `code.claude.com/docs/en/hooks` (both fetched 2026-05-26), the canonical hooks.json shape is:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh" }
        ]
      }
    ]
  }
}
```

**Required per hook entry**: `type` (one of `command`, `http`, `mcp_tool`, `prompt`, `agent`), plus the type-specific required field (`command` for command hooks, `url` for http, etc.).

### Current state (file:line)

Source: `hooks/example/hooks/hooks.json:1-15`:
```json
{
  "description": "Reference example hook. Prepends a timestamp marker to every user prompt so Claude sees session context.",
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "printf '[Lab Notebook context: timestamp=%s]\\n' \"$(date -u +%FT%TZ)\""
          }
        ]
      }
    ]
  }
}
```

Generated: `_generated/hook-example/hooks/hooks.json` — verbatim copy. Plugin.json correctly omits the `hooks` field (auto-discovery from `hooks/hooks.json`); description is propagated.

### Root cause analysis (why doesn't it fire?)

The hook *is firing*. The schema is valid: `type: command` with a `command` string, nested under `hooks.UserPromptSubmit[].hooks[]`. What the operator sees as "not doing anything" is a verification gap, not a hook failure:

Per `code.claude.com/docs/en/hooks` (fetched 2026-05-26), under "UserPromptSubmit: Context Injection":

> For `UserPromptSubmit`, plain text written to stdout with exit code 0 is **automatically added as context** and visible to Claude.

So the `printf '[Lab Notebook context: timestamp=...]'` output is being silently merged into the prompt that Claude sees — there is no visible terminal echo on the operator side. The hook works; the operator can't tell because the side effect (context injection) doesn't render in the operator's UI. There is no built-in indicator like "hook fired".

To verify, the operator would need either:
- Run `claude --debug` (per `code.claude.com/docs/en/hooks` "Method 2: Debug Mode"), which logs hook output
- Change the hook to a side-effect-visible form (e.g. `tee` to a logfile)
- Use `/hooks` in-session to see configured hooks (`code.claude.com/docs/en/hooks` "Method 3")
- Use the `statusMessage` field on the hook entry, which shows a spinner string while the hook runs (`code.claude.com/docs/en/hooks`)

### All Claude hook types

Per `code.claude.com/docs/en/plugins-reference#hooks` (fetched 2026-05-26), the full list:

| Event | When it fires |
|---|---|
| `SessionStart` | Session begins or resumes |
| `Setup` | `--init-only` / `--init` / `--maintenance` in `-p` mode |
| `UserPromptSubmit` | User submits a prompt, before Claude processes it |
| `UserPromptExpansion` | A typed command expands into a prompt |
| `PreToolUse` | Before a tool call executes (can block) |
| `PermissionRequest` | When a permission dialog appears |
| `PermissionDenied` | Tool call denied by auto-mode classifier |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `PostToolBatch` | After a batch of parallel tool calls resolves |
| `Notification` | When Claude Code sends a notification |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent finishes |
| `TaskCreated` | TaskCreate fires |
| `TaskCompleted` | Task marked completed |
| `Stop` | Claude finishes responding |
| `StopFailure` | Turn ends due to API error |
| `TeammateIdle` | Agent-team teammate about to go idle |
| `InstructionsLoaded` | CLAUDE.md or `.claude/rules/*.md` loaded into context |
| `ConfigChange` | Configuration file changes mid-session |
| `CwdChanged` | Working directory changes |
| `FileChanged` | Watched file changes on disk |
| `WorktreeCreate` | Worktree being created |
| `WorktreeRemove` | Worktree being removed |
| `PreCompact` | Before context compaction |
| `PostCompact` | After context compaction |
| `Elicitation` | MCP server requests user input |
| `ElicitationResult` | After user responds to MCP elicitation |
| `SessionEnd` | Session terminates |

**Hook types** (the `type` field of an individual hook entry): `command`, `http`, `mcp_tool`, `prompt`, `agent`.

### Recommended fix

Two changes:

1. **Make the existing `UserPromptSubmit` hook observably side-effecting** so an operator can verify "hook fired" without reading debug logs. Change `hooks/example/hooks/hooks.json` to also write a logfile:

```json
{
  "description": "Reference example hook. On every user prompt, injects a timestamp marker as context AND appends a line to /tmp/hook-fired-userprompt.log.",
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "ts=\"$(date -u +%FT%TZ)\"; printf '[Lab Notebook context: timestamp=%s]\\n' \"$ts\"; printf '%s userPromptSubmit fired\\n' \"$ts\" >> /tmp/hook-fired-userprompt.log"
          }
        ]
      }
    ]
  }
}
```

   The first `printf` (to stdout) still injects context. The second (to a logfile) gives the operator a verifiable side effect: `tail -f /tmp/hook-fired-userprompt.log` shows lines accumulating as prompts are submitted.

2. **Add additional hook example variants** so each major hook type has a runnable demo. Recommend a curated subset rather than all 29 events (full coverage adds noise; operators want representative examples). Suggested set:

| Event | Demo command (side-effect visible) | Why this event |
|---|---|---|
| `SessionStart` | `printf '%s session-start\n' "$(date -u +%FT%TZ)" >> /tmp/hook-fired-sessionstart.log` | Confirms boot-time hook works |
| `UserPromptSubmit` | (above) | Confirms per-turn hook |
| `PreToolUse` (matcher `Write\|Edit`) | `printf '%s preTool %s\n' "$(date -u +%FT%TZ)" "$CLAUDE_TOOL_NAME" >> /tmp/hook-fired-pretool.log` | Confirms tool-event hook + matcher |
| `PostToolUse` (matcher `Write\|Edit`) | same shape | Mirrors PreToolUse |
| `Stop` | `printf '%s stop\n' "$(date -u +%FT%TZ)" >> /tmp/hook-fired-stop.log` | Confirms response-end hook |
| `SessionEnd` | `printf '%s session-end\n' "$(date -u +%FT%TZ)" >> /tmp/hook-fired-sessionend.log` | Confirms shutdown hook |

These six cover session lifecycle (start, end), per-turn (UserPromptSubmit, Stop), and tool lifecycle (Pre/PostToolUse with matcher) — the categorical breadth without exhaustive listing.

Two implementation options:
- **Single hook-example with all six events in one hooks.json** — concrete, immediately discoverable, but mixed (operators picking only one might not want all six).
- **Six separate plugins** (`hook-example-session-start`, `hook-example-pre-tool-use`, etc.) — clearer separation but explodes the marketplace listing.

Recommend the **single hooks.json approach** for the example plugin. The example is meant to teach the schema, not to be a la carte-installable production hooks. The hooks.json with six events demonstrates matcher syntax, the difference between session/tool/turn events, and how to chain multiple events in one file.

### Recommended hook-type coverage

The list above (6 events) covers four of the five `type` values: all six use `type: command`. To demonstrate the other types, add three optional variants either inline or as separate plugins:

- `type: http` example using `Notification` event: POST event JSON to `http://localhost:8000/hook` (operator runs a netcat listener as the side-effect observation)
- `type: prompt` example using `PreToolUse(Bash)`: prompt an LLM to evaluate the command (operator observes the conversation message stream — these are explicit per `code.claude.com/docs/en/hooks`)
- `type: mcp_tool` example: deferred — requires a running MCP server, which adds setup complexity to the example. Document the schema in the README, not as a runnable demo.

### Verification method per hook type

Add to `docs/TEST_YOURSELF.md` Claude section a "Hook verification" subsection with one line per event:

| Event | Action | Expected observation |
|---|---|---|
| `SessionStart` | Start a new session in the workspace | `tail /tmp/hook-fired-sessionstart.log` shows a new line with the session-start timestamp |
| `UserPromptSubmit` | Type any prompt in Claude | `/tmp/hook-fired-userprompt.log` gets a new line; debug-mode output includes the injected `[Lab Notebook context: ...]` line |
| `PreToolUse` (matcher Write\|Edit) | Ask Claude to edit a file | `/tmp/hook-fired-pretool.log` gets a `preTool Write` (or `preTool Edit`) entry |
| `PostToolUse` (matcher Write\|Edit) | Same — successful edit | `/tmp/hook-fired-posttool.log` line right after the PreToolUse |
| `Stop` | Wait for Claude to finish responding | `/tmp/hook-fired-stop.log` gets a line per assistant turn |
| `SessionEnd` | Exit the session (`Ctrl+D` or `/exit`) | `/tmp/hook-fired-sessionend.log` gets the final line |

## Finding 6 — mcp-example uv prerequisite

### Symptom (operator's observation)

```
# without uv:
plugin:mcp-example:example-fetch: uvx mcp-server-fetch - ✗ Failed to connect
# with uv:
plugin:mcp-example:example-fetch: uvx mcp-server-fetch - ✓ Connected
```

### Claude's expected MCP shape

Per `code.claude.com/docs/en/plugins-reference#mcp-servers` (fetched 2026-05-26), an MCP server entry takes `command` + `args` + optional `env`/`cwd`. There's no concept of "auto-install prereqs" — the binary the `command` field names must exist on the host PATH. The doc explicitly notes for the LSP analogue, *"You must install the language server binary separately"*; the same constraint applies to MCP commands.

### Current state

Source: `mcp-servers/example/mcp-config.json:1-8`:
```json
{
  "mcpServers": {
    "example-fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

Generated: `_generated/mcp-example/mcp-config.json` — identical. Plugin.json points `mcpServers: ./mcp-config.json` correctly.

### Root cause

The example uses `uvx`, a CLI shipped with `uv`. If `uv` isn't installed on the host, `uvx` isn't on PATH and the MCP server can't start. This is correct behavior — the marketplace example just doesn't document its dependency.

### Recommended fix

Recommend **option (a) — document the `uv` prerequisite** rather than swapping to a no-prereq alternative. Rationale:

1. The marketplace itself already requires `uv` (the generator scripts use `# /// script` PEP-723 inline metadata + uv to run, per `scripts/platforms.py:1-5`). So a contributor cloning the marketplace already has `uv`. Adding an MCP example that uses `uvx` is consistent with our existing tooling baseline.
2. `uvx` is the documented pattern in the official MCP docs (`modelcontextprotocol.io/quickstart`) for running Python-based MCP servers without polluting global Python.
3. Alternative options would push the user to install Node (`npx`-based MCP servers), which is a strictly larger dependency surface than `uv`.

Concretely:

1. Edit `mcp-servers/example/README.md` to add a "Prerequisites" section pointing to `https://github.com/astral-sh/uv` install instructions.
2. Edit `_generated/mcp-example/README.md` (which is auto-generated from the source README per `scripts/constructs.py::MCPConstruct.emit`'s `shutil.copytree` at lines 278-285) to propagate the same.
3. Optionally add a `SessionStart` hook that detects missing `uvx` and prints a helpful error message. This is a stretch goal — most operators will install `uv` once and not see the message again. Skip unless the implementer has bandwidth.

Folding into a larger commit: yes — this is a 5-line README addition; fold it into the example-fixes commit alongside Findings 1-5.

## Finding 7 — slash command namespacing investigation

### What we observed

The operator listed four invocation patterns from a session with the marketplace installed:

- `/example-skill` — looks flat
- `/command-example:example-command` — `<plugin-name>:<component-name>` namespaced
- `agent-example:notebook-reviewer` — same pattern
- `plugin:mcp-example:example-fetch` — three-level

### Claude's namespacing convention

Per `code.claude.com/docs/en/plugins` (fetched 2026-05-26):

> **Why namespacing?** Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name.
>
> To change the namespace prefix, update the `name` field in `plugin.json`.

And from the "Standalone vs Plugins" table on the same page:

| Approach | Skill names | Best for |
|---|---|---|
| **Standalone** (`.claude/` directory) | `/hello` | Personal workflows |
| **Plugins** | `/plugin-name:hello` | Sharing with teammates |

And from `code.claude.com/docs/en/skills` (fetched 2026-05-26):

> Plugin skills use a `plugin-name:skill-name` namespace, so they cannot conflict with other levels.

**There is no flatten mechanism.** The only lever is the plugin's `name` field — which determines the prefix verbatim. The doc says *"To change the namespace prefix, update the `name` field in plugin.json"* — i.e. the prefix IS the plugin name.

For the `/example-skill` case the operator observed: this is `/<plugin-name>:<skill-name>` where the plugin is named `skill-example` and the skill is named `example-skill`. Wait — that would give `/skill-example:example-skill`. Let me re-read: `_generated/skill-example/.claude-plugin/plugin.json:9` declares the plugin name as `skill-example`, and `skills/example/SKILL.md:2` has `name: example-skill`. So the invocation should be `/skill-example:example-skill`. The operator's `/example-skill` observation must be a misread — likely they typed the skill name and Claude resolved it from autocomplete (the slash menu shows just the skill name component, but the actual invocation is still `/skill-example:example-skill`).

This needs hands-on verification: the operator should type `/` in Claude and look at what the autocomplete dropdown shows vs what gets resolved on Enter. If the dropdown shows `/example-skill` but the resolved invocation is `/skill-example:example-skill`, that's UI sugar, not a flatten feature.

### Per-construct invocation rules

Per `code.claude.com/docs/en/plugins-reference` (fetched 2026-05-26), the manifest-schema "name" section:

> This name is used for namespacing components. For example, in the UI, the agent `agent-creator` for the plugin with name `plugin-dev` will appear as `plugin-dev:agent-creator`.

Cross-referenced with `code.claude.com/docs/en/discover-plugins` (fetched 2026-05-26):

> Plugin skills are namespaced by the plugin name, so **commit-commands** provides skills like `/commit-commands:commit`.

| Construct | Invocation pattern | Source citation |
|---|---|---|
| Skill | `/<plugin-name>:<skill-name>` | plugins.md, skills.md |
| Command (legacy flat .md in `commands/`) | `/<plugin-name>:<file-stem>` (skills are the unified name now; `commands/` files are an alias) | skills.md "Custom commands have been merged into skills" |
| Agent | `<plugin-name>:<agent-name>` (no `/` prefix — appears in `/agents` UI) | plugins-reference.md |
| MCP tool | `mcp__<plugin-name>__<tool-name>` or surfaced as `plugin:<plugin-name>:<tool>` in CLI listings (hook matcher format vs CLI display) | hooks.md, plugins-reference.md |

So the operator's `plugin:mcp-example:example-fetch` is the CLI listing format. In hook matchers and tool-list context, MCP tools appear as `mcp__<plugin>__<tool>` (per `code.claude.com/docs/en/hooks`'s matcher examples). The `plugin:<plugin>:<tool>` prefix is a display convention in `claude plugin details` / `/plugin` UI surfaces, not the matcher form.

### Options (accept / rename / flatten)

- **(a) Accept the convention**: leave everything as-is and document the namespacing rules in `docs/PLATFORMS.md` Claude section + `docs/TEST_YOURSELF.md`. Zero code change. Operators learn the pattern by reading docs once.
- **(b) Rename our example plugins to shorter forms**: change plugin names from `skill-example` → `skl-ex`, `command-example` → `cmd-ex`, `agent-example` → `agt-ex`, etc. This produces `/skl-ex:example-skill`, `/cmd-ex:example-command`. Slightly tighter. But Claude's own convention (in the doc) uses `my-first-plugin:hello`, `commit-commands:commit` — they don't shorten. Following the doc's idiom is better.
- **(c) Flatten mechanism (`prefix: ""`)**: investigated. **Does not exist.** The plugins-reference manifest schema is fully enumerated and contains no `prefix`, `namespace`, or alias-suppression field. The only way to influence the prefix is renaming the plugin (option b).

### Recommendation

**Option (a) — accept the convention, document it.** Add to `docs/PLATFORMS.md` Claude section a "Naming conventions" subsection that lists the four invocation patterns above. Add to `docs/TEST_YOURSELF.md` Claude section a one-line per-construct "How to invoke" reminder so operators know what to type.

For `bundle-*` plugins, namespacing is the same — `/bundle-skill-all:<skill-name>` — but bundles install their contents under each contained plugin's namespace via dependency resolution (per `code.claude.com/docs/en/plugins-reference#dependencies`). The bundle wrapper itself doesn't introduce a new prefix level; users still call `/skill-act-runner:act-runner` (or whatever the contained plugin's namespace is) even when installed via a bundle. This is worth a callout in PLATFORMS.md.

No source code changes. No plugin renames.

## Finding 8 — Claude plugin rule deprecation verdict

### Claude's official component list

Per `code.claude.com/docs/en/plugins-reference#plugin-components-reference` (fetched 2026-05-26):

> A **plugin** is a self-contained directory of components that extends Claude Code with custom functionality. Plugin components include skills, agents, hooks, MCP servers, LSP servers, and monitors.

And the components-reference section header enumerates: Skills, Agents, Hooks, MCP servers, LSP servers, Monitors, Themes. The `experimental` block adds Themes and Monitors. The `plugin-manifest-schema` "Component path fields" table lists: `skills`, `commands`, `agents`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`, `experimental.themes`, `experimental.monitors`. No `rules`.

### Is rule a Claude plugin component?

**NO.** Rules are not a Claude plugin component. They are a *memory* feature.

Per `code.claude.com/docs/en/memory#organize-rules-with-claude-rules` (fetched 2026-05-26):

> For larger projects, you can organize instructions into multiple files using the `.claude/rules/` directory. ... All `.md` files are discovered recursively, so you can organize rules into subdirectories like `frontend/` or `backend/`.
>
> Place markdown files in your project's `.claude/rules/` directory. Each file should cover one topic, with a descriptive filename like `testing.md` or `api-design.md`.
>
> Rules without [`paths` frontmatter] are loaded at launch with the same priority as `.claude/CLAUDE.md`.

User-level rules:

> Personal rules in `~/.claude/rules/` apply to every project on your machine.

So Claude consumes rules in three ways:
1. Project rules: `<project>/.claude/rules/**/*.md` — loaded at session start
2. User rules: `~/.claude/rules/**/*.md` — loaded at session start
3. Path-scoped rules: rules with `paths:` frontmatter — loaded when matching files are opened

The relevant hook event is `InstructionsLoaded` (per the hook events table above), which fires whenever a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. This is observable evidence that rules-as-files-in-`.claude/rules/` is the canonical mechanism.

The plugin `activate.sh` we ship today (per `scripts/constructs.py::ACTIVATE_SH_TEMPLATE` lines 72-109) symlinks the rule into `.claude/rules/`. That's the right place — but the way we arrive there (install a plugin → run activate.sh) is awkward. The plugin is a one-shot wrapper around `cp` + `ln -s`. The actual rule-consumption mechanism (Claude reading `.claude/rules/*.md`) doesn't need a plugin layer at all.

### Verdict

**DEPRECATE rule emission to Claude.** Remove `RuleConstruct` from `ClaudeCodePlatform.supports`. Rationale:

1. Rules aren't a Claude plugin component (per official doc enumeration).
2. The current `_generated/rule-<name>/` plugins exist solely to symlink files into `.claude/rules/` via activate.sh — that's not a real plugin, it's a copy script wrapped in plugin metadata.
3. Each of the 22 rule plugins clutters `marketplace.json` (22 entries) and contributes always-on token cost via Claude's `plugin details` token estimation (per `code.claude.com/docs/en/plugins-reference#plugin-details`).
4. Operators on Claude who want our rules can `git clone` the marketplace and symlink/copy `rules/<name>/rule.md` to their `~/.claude/rules/` directly. We can document this in `docs/PLATFORMS.md` Claude section.

### What to do with the rule files

**Keep source `rules/<name>/`**. Cursor and Windsurf consume them via `CursorPlatform` (lines 314-324) and `WindsurfPlatform` (lines 408-417) emissions to `.cursor/rules/<name>.md` and `.windsurf/rules/<name>.md`. AgentsPlatform also emits them to `.agents/rules/<name>.md` (per `D-12` decision in `platforms.py:484-507`). Those emissions remain valid — the rules are real, just not surfaced as Claude *plugins*.

**Stop emitting `_generated/rule-<name>/`**. This is the directory containing `.claude-plugin/plugin.json` + `activate.sh` + `rules/<name>.md` for Claude. Once `RuleConstruct` is removed from `ClaudeCodePlatform.supports`, the generator's Phase 1.5 (plugin manifest emission) skips it, and the marketplace.json plugin-list emission can also skip rule entries.

**Add a "Claude rules" section to `docs/PLATFORMS.md`** with the manual install:

```bash
# In a Claude-using project:
mkdir -p .claude/rules
ln -s "$(pwd)/rules/blast-radius/rule.md" .claude/rules/blast-radius.md
# or copy for portability:
cp rules/blast-radius/rule.md .claude/rules/blast-radius.md
```

User-scope variant: replace `.claude/rules` with `~/.claude/rules`.

This is a 3-line install vs the prior "install plugin → run activate.sh" two-step. Net simplification.

### What to remove from ClaudeCodePlatform.supports

In `scripts/platforms.py:115-119`:

```python
supports: set[type[Construct]] = {
    SkillConstruct, RuleConstruct, CommandConstruct, AgentConstruct,
    HookConstruct, MCPConstruct, LSPConstruct, MonitorConstruct,
    OutputStyleConstruct, ThemeConstruct,
}
```

Change to:

```python
supports: set[type[Construct]] = {
    SkillConstruct, CommandConstruct, AgentConstruct,
    HookConstruct, MCPConstruct, LSPConstruct, MonitorConstruct,
    OutputStyleConstruct, ThemeConstruct,
}
```

This single edit ripples: Phase 1.5 skips `RuleConstruct` for Claude (no `_generated/rule-*/` plugin.json written for the Claude side), and the marketplace.json plugin-list emission (which checks `type(construct) in ClaudeCodePlatform.supports`) drops all 22 rule-* entries. Implementer note: also check whether the marketplace plugins-list emission in `scripts/generator.py` (not read but referenced) iterates `CONSTRUCTS` directly or filters by `ClaudeCodePlatform.supports`; if it iterates directly, the rule entries need to be filtered out by a separate explicit check.

Update `docs/ARCHITECTURE.md` and `docs/PLATFORMS.md` Claude sections to reflect the new supports set. Add a migration note: existing Claude users who installed `rule-<name>` plugins via `/plugin install` should `/plugin uninstall rule-<name>@dgxsparklabs-marketplace` to clean up; new install instructions point to the symlink/copy method instead.

## Finding 9 — output-style activation observability

### Symptom (operator's observation)

> "output-style-example: Lab Notebook Voice — It seems to be a pickable option from the menu but I don't know if it applied it, how can I determine for sure it works?"

### How Claude exposes active output style

Per `code.claude.com/docs/en/output-styles` (fetched 2026-05-26):

> Run `/config` and select **Output style** to pick a style from a menu. Your selection is saved to `.claude/settings.local.json` at the [local project level](/en/settings).
>
> To set a style without the menu, edit the `outputStyle` field directly in a settings file:
>
> ```json
> { "outputStyle": "Explanatory" }
> ```
>
> Output style is part of the system prompt, which Claude Code reads once at session start. Changes take effect after `/clear` or a new session.

Also from the same doc:

> Output styles directly modify Claude Code's system prompt.
> - All output styles have their own custom instructions added to the end of the system prompt.
> - All output styles trigger reminders for Claude to adhere to the output style instructions during the conversation.

And for plugin-shipped styles specifically (per `code.claude.com/docs/en/plugins-reference#output-styles`, which is brief — the canonical reference is `code.claude.com/docs/en/output-styles`), styles in a plugin's `output-styles/` directory appear in the `/config → Output style` menu alongside built-in and user-level styles.

### Current state

Source: `output-styles/example/output-styles/lab-notebook-voice.md:1-20`:
```yaml
---
name: Lab Notebook Voice
description: Writes responses in a measured, citation-focused lab notebook voice. Reference example showing the output-style format. Not force-applied — users select it explicitly.
keep-coding-instructions: true
---

## Voice
Respond in the voice of a scientific lab notebook entry:
- State facts plainly with measurements and units.
- Cite the source whenever you assert something the user could verify (file path, line number, URL, paper DOI).
- ...
End answers with one line tagged `Next:` proposing the immediate next checkable step.
```

The source frontmatter and content are schema-valid. Generated copy: `_generated/output-style-example/output-styles/lab-notebook-voice.md` (verbatim per `OutputStyleConstruct.emit`).

### Validation method

To prove the style is applied (vs default), an operator runs this exact sequence:

1. **Before**: Open the Claude project with the marketplace installed but no output style set. Confirm by running:
   ```bash
   cat .claude/settings.local.json
   ```
   Expect: no `outputStyle` key (or `"outputStyle": "Default"`).

2. **Select the style**: In the Claude session, type `/config`, navigate to **Output style**, and pick "Lab Notebook Voice".

3. **Verify persistence**: After selection:
   ```bash
   cat .claude/settings.local.json
   ```
   Expect: a key `"outputStyle": "Lab Notebook Voice"` (the `name` from the SKILL.md frontmatter).

4. **Apply by clearing**: Type `/clear` in Claude to force a fresh session that re-reads the system prompt.

5. **Test the behavioral change**: Ask Claude a small task that exercises the style's distinctive markers:
   ```
   Explain what the `_base_plugin_shape` function in scripts/constructs.py does.
   ```

6. **Observe**: The response should exhibit lab-notebook prose markers from the SKILL.md spec:
   - Plain factual sentences with units/specifics (file paths, line numbers, etc.) — the spec says *"Cite the source whenever you assert something the user could verify (file path, line number, URL, paper DOI)"*
   - No hedging language unless flagged as uncertainty
   - A final line tagged `Next:` — the spec ends with *"End answers with one line tagged `Next:` proposing the immediate next checkable step."*

7. **Compare to default**: To strongly confirm: in a separate clean session, set `outputStyle: "Default"`, ask the same question, and observe that the response has none of the lab-notebook markers (no `Next:` line, more conversational tone, etc.).

The `Next:` line is the cleanest binary signal: present → Lab Notebook Voice is active; absent → it's not. This is hands-on, operator-runnable, and produces a definitive yes/no.

If the persistence check (step 3) shows no `outputStyle` in settings.local.json after picking from `/config`, that's a *new* Claude bug to file — not a marketplace bug, since our SKILL.md is schema-valid.

## Appendix A — Validation methods for non-obvious behaviors

Per the goal-hook directive: "for things that are not obvious why they happen design a set of validations and include them into the claude section of TEST_YOURSELF.md". This appendix collects hands-on operator-runnable validation methods for the implementer to add to the Claude section of `docs/TEST_YOURSELF.md`. Each step says "do X, observe Y" — no file-existence checks.

| # | Finding | Action | Expected observation |
|---|---|---|---|
| 1 | F1 — marketplace description | Run `claude plugin validate ./ --strict` from repo root | Exit code 0, "Validation passed", no warnings |
| 2 | F2 — lsp schema | After fix: open Claude in a `.md` repo with `lsp-example` installed. Open or edit a `.md` file. | Claude surfaces marksman diagnostics (e.g. broken-link or heading warnings) inline; `/plugin` Errors tab shows no LSP errors |
| 3 | F3 — monitors | Install `monitor-example`, start a session. Watch the bottom-status / task panel during the first 30 seconds | A notification appears with the disk usage summary, sourced from `example-disk` monitor (one-shot variant) |
| 4 | F4 — theme | Run `/theme`, pick "Lab Notebook", confirm with Enter | Editor visibly switches to a light/paper-toned palette (foreground darkens, background lightens). `cat ~/.claude/settings.json \| grep theme` shows `custom:theme-example:lab-notebook` |
| 5a | F5 — UserPromptSubmit hook fires | After fix lands: with `hook-example` installed, type any prompt. Then in another terminal: `tail /tmp/hook-fired-userprompt.log` | New line with timestamp and `userPromptSubmit fired` |
| 5b | F5 — SessionStart hook | Restart Claude in the project. Then: `tail /tmp/hook-fired-sessionstart.log` | New line with start-time timestamp |
| 5c | F5 — PreToolUse hook + matcher | Ask Claude to edit any file. Then: `tail /tmp/hook-fired-pretool.log` | Line with `preTool Edit` or `preTool Write` |
| 5d | F5 — PostToolUse hook | After the edit completes: `tail /tmp/hook-fired-posttool.log` | Mirror line immediately after the PreToolUse one |
| 5e | F5 — Stop hook | After Claude finishes a response: `tail /tmp/hook-fired-stop.log` | New line per assistant turn |
| 5f | F5 — SessionEnd hook | Exit Claude (`/exit` or `Ctrl+D`). Then: `tail /tmp/hook-fired-sessionend.log` | Final line with session-end timestamp |
| 6 | F6 — uv prereq | On a fresh host: try `claude plugin install mcp-example@dgxsparklabs-marketplace`. Then `/plugin` Errors tab | Without uv: error "Failed to connect, uvx not found". After `curl -LsSf https://astral.sh/uv/install.sh \| sh`: connects. |
| 7a | F7 — skill namespacing | Type `/` in Claude with skill-example installed. Read the autocomplete dropdown | Entry appears as `/skill-example:example-skill` (or shortened in UI; the actual invocation is the namespaced form) |
| 7b | F7 — agent namespacing | Run `/agents` with agent-example installed | Entry appears as `agent-example:notebook-reviewer` |
| 7c | F7 — MCP tool namespacing | Ask Claude to fetch a URL with mcp-example installed. Watch `claude --debug` tool name in the log | Tool name appears as `mcp__mcp-example__example-fetch` (hook-matcher form) or `plugin:mcp-example:example-fetch` (display form) |
| 8 | F8 — rule deprecation, post-fix | Run `claude plugin list --available --json \| jq '.available \| map(.name) \| map(select(startswith("rule-"))) \| length'` | `0` — no rule-* plugins listed for Claude after deprecation |
| 9 | F9 — output style applied | Pick "Lab Notebook Voice" via `/config`. `/clear`. Ask Claude: "Explain `_base_plugin_shape` in scripts/constructs.py." | Response ends with a line tagged `Next:`, cites file paths and line numbers, avoids hedging. `cat .claude/settings.local.json \| jq .outputStyle` returns `"Lab Notebook Voice"`. |

## Appendix B — Doc URLs we relied on

All fetched 2026-05-26 unless noted:

- `https://code.claude.com/docs/en/plugins` — namespacing rules, plugin structure overview, mandatory `/plugin-name:skill-name` invocation
- `https://code.claude.com/docs/en/plugins-reference` — full component schemas (skills, agents, hooks, MCP, LSP, monitors, themes, output-styles), manifest schema, namespacing rule on the `name` field
- `https://code.claude.com/docs/en/plugin-marketplaces` — marketplace.json schema, top-level `description` field, `--strict` validate flag
- `https://code.claude.com/docs/en/discover-plugins` — slash-command invocation patterns for installed plugins (`/commit-commands:commit` example)
- `https://code.claude.com/docs/en/skills` — namespacing for skill invocation, single-skill plugins, autoplay rules, frontmatter reference
- `https://code.claude.com/docs/en/hooks` — full hooks shape, UserPromptSubmit context-injection semantics, verification methods (`claude --debug`, `/hooks`, transcript inspection, statusMessage)
- `https://code.claude.com/docs/en/output-styles` — `/config` activation flow, `outputStyle` field in settings.local.json, `force-for-plugin` flag, how styles modify system prompt
- `https://code.claude.com/docs/en/memory` — rule discovery via `.claude/rules/*.md`, `InstructionsLoaded` hook event, project vs user vs managed scopes

### 404s noted

- `https://code.claude.com/docs/en/themes` — returned 404 on 2026-05-26 fetch. Theme schema instead came from `code.claude.com/docs/en/plugins-reference#themes` (the components-reference section, which has the full schema).

## Open questions

1. **Theme override key set is not enumerated**. The plugins-reference shows `claude`, `error`, `success` as override-key examples, plus an implication that `background`/`foreground` might be overridable. The full set isn't documented. After the F4 fix lands, an empirical pass picking the Lab Notebook theme and varying which override keys are present should produce the canonical list. This is a follow-up doc-empiricism task, not a blocker.

2. **Bundles and namespace inheritance**. Per F7 commentary: bundles install their contained plugins as dependencies. The bundle plugin itself has its own name (e.g. `bundle-skill-all`), but the namespace for installed contents is each contained plugin's own name (e.g. `/skill-act-runner:act-runner`). This is inferred from the dependencies+namespacing semantics in `code.claude.com/docs/en/plugin-dependencies` (not directly fetched in this pass). Verify hands-on: install `bundle-skill-all`, then check `/` autocomplete to see whether contained skills appear under their own plugin namespaces or under `bundle-skill-all:*`. Defer to a separate QA step.

3. **MCP tool naming convention** has two surface forms: `mcp__<plugin>__<tool>` in hook matchers vs `plugin:<plugin>:<tool>` in CLI listings. The plugins-reference doesn't make this distinction explicit. Both forms are observed in our QA traces; the `mcp__` form is documented in hooks.md and the `plugin:` form is documented in tool-listing outputs. Worth documenting both in PLATFORMS.md but not a bug.

## Bonus findings — additional issues surfaced during this research

1. **`activate.sh` is now orphaned for Claude**. After F8's rule deprecation, the `activate.sh` template in `scripts/constructs.py:72-109` only runs in the Cursor/Windsurf/Agents paths (which already symlink rules via their own emit branches at `platforms.py:315-323, 408-416, 505-512`). The template isn't called by any of those — they call `shutil.copy` directly. So the `activate.sh` we emit today is dead code after F8 lands. Recommend removing the template from `RuleConstruct.emit` (lines 153-173) entirely, since the rule-as-Claude-plugin path is the only consumer.

2. **`mcp-example`'s plugin.json description vs source plugin.json description redundancy**. `scripts/constructs.py::MCPConstruct.build_plugin_json` (lines 268-276) loads the source's `.claude-plugin/plugin.json` and reuses its `description`. This works but creates two sources of truth for the description: the source plugin.json and the source mcp-config.json. The hooks pattern (read description from hooks.json) is similar. Consider unifying: always read description from the construct's primary content file (mcp-config.json's parent, hooks.json), not from a parallel `.claude-plugin/plugin.json` that mirrors the generated one. Minor cleanliness issue; not blocking.

3. **`HookConstruct.build_plugin_json` doesn't write the `hooks` pointer field**. `scripts/constructs.py:240-251` returns a plugin.json with `name`, `version`, `author`, `description` — no `hooks` field. The plugins-reference says hooks at `hooks/hooks.json` are auto-discovered, so omitting the field is correct. Note in code comments. (Already noted in the source code comment lines 249-250.) Worth confirming with an explicit `claude plugin validate` pass after F5 lands that the auto-discovery works.

4. **`AgentConstruct.build_plugin_json` similarly omits the `agents` field** (lines 210-223), with comment confirming "Claude Code reads agents from the plugin's agents/ subdir automatically. No `agents` field is needed in plugin.json (the spec doesn't define one)." This is correct per plugins-reference's "Path behavior rules" — but worth a re-check: the plugins-reference manifest schema DOES list `agents` as a component path field ("string|array — Custom agent files (replaces default `agents/`)"). It's optional — if you don't set it, the default `agents/` is scanned. We rely on the default. Good as-is.

5. **`OutputStyleConstruct.build_plugin_json` writes `outputStyles: "./output-styles"`** (line 351), pointing at the directory. Per plugins-reference, this is correct (`outputStyles: string|array`). Verified.

6. **Code paths reference `docs/research/qa-bug-fixes-2026-05/RESEARCH.md` from several `platforms.py` comments** (lines 224, 253, 346, 430). That's a prior QA pass. Our pass (`docs/research/claude-qa-2026-05-26/RESEARCH.md`) is the next-iteration parallel. Worth a future cross-link from the implementer's commit message so future readers can trace both passes.
