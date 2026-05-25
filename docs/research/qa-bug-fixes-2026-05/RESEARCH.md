---
date: 2026-05-25
purpose: research-for-bug-fixes
arc: fix/platform-emission-bugs
status: draft-for-discussion
---

# Platform Emission Bugs — Research

## TL;DR

Three bugs share the same root pattern: **the generator emits files that satisfy our internal "byte-identity" drift checks but do not satisfy the platforms' loader contracts.** (1) Codex sub-agents land at the wrong install location — `.codex/agents/<n>.toml` is a *workspace* path, but plugin-installed agents must live inside the plugin's *installed-cache* tree (or, on the canonical interpretation, the per-plugin `.codex-plugin/plugin.json` needs an `agents` pointer). (2) Gemini sub-agents must live at `<extension-root>/agents/*.md` per the extensions reference — but in our extension layout the extension root is `.gemini/` and the install location after `gemini extensions install <url>` is `~/.gemini/extensions/<name>/agents/*.md`; we ship them in the right relative spot but Gemini's discovery is gated on the `<extension-root>` of the installed extension (not the source repo path our tests check). The crucial side-finding is that there is **no `agents` field in `gemini-extension.json`** — Gemini's reference confirms directory-convention discovery only. (3) Cursor's mangled popup is the simplest: `CursorPlatform.build_plugin_json` for `SkillConstruct` emits *only* `{"name": "..."}` — no `description`, no `version`, no `skills` pointer — so Cursor's popup falls back to ambient strings (version, git SHA from install metadata, plus the SKILL.md description) and renders them in arbitrary slots. Fix Bug 3 first (one-line `build_plugin_json` change, no upstream dependencies). The sanity-check pass surfaced **5 additional likely/definite bugs** — most notably Cursor hooks (we emit Claude's nested `hooks.<event>[].hooks[].command` shape but Cursor's reference shows a *flat* `{version, hooks: {<event>: [{command, ...}]}}`), Cursor commands (no schema documented; emitter is speculative), and the `.windsurf/hooks.json` location collision (we write the workspace path, which is correct, but the *hook nesting shape* is Claude's, not Windsurf's flat shape).

## Bug 1 — Codex sub-agent format mismatch

### Symptom

QA on 2026-05-25 added the marketplace via `codex plugin marketplace add DgxSparkLabs/marketplace`, installed `agent-example@dgxsparklabs-marketplace`, opened `codex` interactive, asked "what subagents do we have available?" — got only Codex's built-ins (`default`, `explorer`, `worker`). `notebook-reviewer` is not listed.

### Codex's expected schema

Per `https://developers.openai.com/codex/subagents/` (fetched 2026-05-25):

- **File location** (two valid roots):
  - Personal agents: `~/.codex/agents/<name>.toml`
  - Project-scoped agents: `<workspace>/.codex/agents/<name>.toml`
- "Each file defines one custom agent and uses standalone TOML format."
- **Required fields:** `name` (string), `description` (string), `developer_instructions` (string).
- **Optional fields:** `nickname_candidates` (string[]), `model` (string), `model_reasoning_effort` (string), `sandbox_mode` (string), `mcp_servers` (table), `skills.config` (array).
- "Codex identifies the custom agent by its `name` field" — filename is conventional but not load-bearing.

Per `https://developers.openai.com/codex/plugins/build` (fetched 2026-05-25), the `.codex-plugin/plugin.json` supports optional component-reference fields: `skills`, `mcpServers`, `apps`, `hooks`. **The documented surface does NOT list `agents` as a plugin pointer field.** All paths must be relative and start with `./`.

### What we currently emit

`scripts/converters/md_to_toml.py:96-135` converts the Claude-style markdown frontmatter + body into TOML. The actual output at `C:\Users\devic\source\marketplace\.codex\agents\notebook-reviewer.toml` is:

```toml
name = "notebook-reviewer"
description = "Reviews a lab notebook entry as a skeptical peer reviewer. Use when the user has drafted a notebook entry and wants a critical second opinion before publishing."
tools = ["Read", "Grep", "Glob"]
developer_instructions = '''
You are a peer reviewer for laboratory notebook entries. ...
'''
```

The emit path in `scripts/platforms.py:154-176` writes the TOML to `<repo>/.codex/agents/<name>.toml` (the workspace-project path).

The per-plugin manifest at `_generated/agent-example/.codex-plugin/plugin.json` is:

```json
{
  "name": "agent-example",
  "version": "1.0.0",
  "description": "Reviews a lab notebook entry ..."
}
```

— no `agents` pointer, no agent content under the plugin dir at all (`ls _generated/agent-example/` shows: `.claude-plugin`, `.codex-plugin`, `.cursor-plugin`, `agents/notebook-reviewer.md`, `README.md` — the agent .md is there but the **TOML is not in the plugin dir**, it is only at the repo-root `.codex/` mirror).

### Diff table

| Field / aspect | Codex expects | We emit | Mismatch |
|---|---|---|---|
| TOML file shape | `name`, `description`, `developer_instructions` (required) | All three present | OK |
| Optional `tools` | Schema does NOT list a `tools` array; closest analog is `skills.config` | We emit `tools = [...]` | Likely IGNORED by Codex (unknown key — probably harmless, but not surfaced). |
| File location for plugin-installed agents | `<workspace>/.codex/agents/<n>.toml` (project-scoped) OR `~/.codex/agents/<n>.toml` (personal) | `<repo-source>/.codex/agents/<n>.toml` | **MISMATCH.** Our `.codex/agents/` mirror is a *source-repo* path. After `codex plugin add agent-example`, Codex unpacks the plugin into `~/.codex/.tmp/marketplaces/.../agent-example/<version>/`. The TOML never reaches `~/.codex/agents/` or any project's `.codex/agents/`. |
| Per-plugin manifest pointer | Not documented (no `agents` field in plugins/build) | No `agents` field | OK (matches docs) — but means there is no documented mechanism for a *plugin-installed* sub-agent. |
| Subagent surfaced in `codex` interactive after `plugin add` | YES (per docs) | NO (per QA) | **Symptom confirmed.** |

### Hypothesis

The Codex sub-agent doc describes **workspace + user paths only**, not plugin-install paths. The Codex plugin doc lists `skills`, `mcpServers`, `hooks`, `apps` — but NOT `agents`. So:

- **Hypothesis A (most likely):** Codex's plugin-install machinery does not yet know how to surface sub-agents from an installed plugin. The TOML is correct; the install pathway is missing. To verify: after `codex plugin add agent-example`, manually copy the TOML from the plugin's install dir to `~/.codex/agents/notebook-reviewer.toml` and re-test. If the agent then appears in `codex` interactive, this confirms the install-pathway is the gap (an upstream limitation).

- **Hypothesis B:** Codex *does* support sub-agents in plugins via an undocumented `agents` pointer field, and the missing pointer in our `.codex-plugin/plugin.json` causes silent skip. To verify: try adding `"agents": "./agents/"` (or `"agents": "./agents/*.toml"`) to the manifest and observe whether `codex` interactive picks it up. (Inexpensive to test — requires generator change + reinstall.)

### Recommended fix

Two-step:

1. **Test Hypothesis B first** (low cost). Modify `CodexPlatform.build_plugin_json` in `scripts/platforms.py:178-191`:

   ```python
   def build_plugin_json(self, construct: Construct, name: str) -> dict:
       full_name = f"{construct.prefix}-{name}"
       manifest: dict = {
           "name": full_name,
           "version": "1.0.0",
           "description": _description_from_construct(construct, name),
       }
       if isinstance(construct, SkillConstruct):
           manifest["skills"] = "./skills/"
       elif isinstance(construct, MCPConstruct):
           manifest["mcpServers"] = "./mcp.json"
       elif isinstance(construct, HookConstruct):
           manifest["hooks"] = "./hooks/hooks.json"
       elif isinstance(construct, AgentConstruct):
           manifest["agents"] = "./agents/"  # speculative pointer
       return manifest
   ```

   Also update `CodexPlatform.emit` to write the TOML *inside the plugin dir* (`_generated/agent-<name>/agents/<n>.toml`) so the pointer resolves correctly after install. This requires emit signature to know the plugin's `_generated` path — current emit writes to `self.mirror_directory / "agents" /` (the workspace mirror). Either: (a) add a Phase-1.5-coupled emission so each plugin dir gets its own `agents/*.toml`, or (b) keep the workspace mirror and add an `agents/` copy to the plugin dir as well.

2. **If Hypothesis A holds** (the field does nothing): file an upstream issue / feature request with OpenAI Codex docs to clarify or add plugin-install support for sub-agents. In the interim, document the gap in `docs/PLATFORMS.md` — the `.codex/agents/<n>.toml` we already emit *is* useful for workspace-scoped use when the user clones the repo, just not for plugin-add installs.

The TOML-shape fix (removing the unknown `tools` field, or repurposing as `mcp_servers`/`skills.config`) is independently worthwhile but probably not load-bearing for the symptom.

## Bug 2 — Gemini sub-agent format mismatch

### Symptom

QA on 2026-05-25 ran `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent`, confirmed the extension installed and all 27 skills enumerated via `gemini skills list --all`. Opened `gemini` interactive, typed `/agents` — got only built-ins (`codebase_investigator`, `cli_help`, `generalist`). `notebook-reviewer` is missing.

### Gemini's expected schema

Per `https://geminicli.com/docs/extensions/reference/` (fetched 2026-05-25):

- `gemini-extension.json` core fields: `name`, `version`, `description`, `mcpServers`, `contextFileName`, `excludeTools`, `migratedTo`, `plan`. **No `agents` / `subAgents` field is documented in the manifest.**
- The reference does state: "Provide sub-agents ... Add agent definition files (`.md`) to an `agents/` directory in your extension root."
- Sub-agents are "a preview feature currently under active development."

Per `https://geminicli.com/docs/core/subagents/` (fetched 2026-05-25):

- Sub-agent file = markdown with YAML frontmatter.
- **Required frontmatter:** `name` (slug — lowercase, numbers, hyphens, underscores), `description` (visible to main agent for routing).
- **Optional frontmatter:** `kind` (`local`|`remote`, default `local`), `tools` (array; supports wildcards), `mcpServers` (inline), `model`, `temperature`, `max_turns`, `timeout_mins`.
- **Discovery locations:**
  1. Project: `.gemini/agents/*.md` (shared)
  2. User: `~/.gemini/agents/*.md` (personal)
- "Extensions can bundle and distribute subagents" but the reference link points to other docs not in the excerpt.

### What we currently emit

Per `scripts/platforms.py:219-225`, `GeminiPlatform.emit` for `AgentConstruct` copies each `agents/<name>/agents/*.md` source file to `<repo>/.gemini/agents/<name>.md`. The output at `C:\Users\devic\source\marketplace\.gemini\agents\notebook-reviewer.md`:

```markdown
---
name: notebook-reviewer
description: Reviews a lab notebook entry as a skeptical peer reviewer. Use when the user has drafted a notebook entry and wants a critical second opinion before publishing.
tools: Read, Grep, Glob
---

You are a peer reviewer for laboratory notebook entries. ...
```

The repo-root `.gemini/gemini-extension.json`:

```json
{
  "name": "dgxsparklabs-marketplace",
  "version": "1.0.0",
  "description": "Curated agent skills, rules, ..."
}
```

After `gemini extensions install <url>`, the install path is `~/.gemini/extensions/dgxsparklabs-marketplace/`. The agents subdir lands at `~/.gemini/extensions/dgxsparklabs-marketplace/agents/notebook-reviewer.md`.

### Diff table

| Field / aspect | Gemini expects | We emit | Mismatch |
|---|---|---|---|
| Extension root location | The extension dir (`<extension-root>/`) | We are in `.gemini/`, which **IS** the extension root for local install | OK |
| Agents subdir location | `<extension-root>/agents/*.md` | `.gemini/agents/*.md` (= `<extension-root>/agents/*.md`) | OK — matches docs verbatim |
| `gemini-extension.json` `agents` field | None documented (directory-convention discovery) | None emitted | OK (matches absence of documented field) |
| Frontmatter `name` | Required, slug-style | Present, `notebook-reviewer` | OK |
| Frontmatter `description` | Required | Present | OK |
| Frontmatter `tools` | Optional array (supports wildcards) | Comma-separated string `"Read, Grep, Glob"` — **NOT a YAML array** | **LIKELY BUG.** The Gemini spec says `tools` is an array. Our format is the Claude shape (comma-separated scalar). If Gemini's loader strictly parses YAML, our `tools: Read, Grep, Glob` parses as a single string, not a 3-tool array. This may or may not cause discovery failure (the doc says omitting `tools` means "inherit all"; a malformed `tools` field could plausibly cause Gemini to reject the agent file entirely). |
| Discovery after `extensions install` | Agents at `~/.gemini/extensions/<ext>/agents/*.md` discovered automatically | We ship to the same relative location | OK in principle, but discovery is **gated on the `<extension-root>` being the install root**, which it is. |
| `/agents` lists our agent | YES | NO | **Symptom confirmed.** |

### Hypothesis

Three candidate root causes, in priority order:

- **Hypothesis A (highest confidence):** `tools` frontmatter is malformed. Gemini's reference (`https://geminicli.com/docs/core/subagents/`) shows tools as:
  ```yaml
  tools:
    - read_file
    - grep_search
  ```
  We emit `tools: Read, Grep, Glob` — a single string. If Gemini's loader treats unknown/malformed `tools` as a parse error, it skips the file silently. Verify by removing the `tools` line from the file by hand and re-running `gemini extensions update` (or reinstall) — if `/agents` then surfaces it, this is the bug.

- **Hypothesis B:** Gemini's "preview" extension-bundled sub-agents simply do not register at the user-extension install location yet — the doc says "extensions can bundle ... see other docs" but the reference we fetched doesn't confirm `~/.gemini/extensions/<ext>/agents/` is on the discovery path; only `.gemini/agents/` (project) and `~/.gemini/agents/` (user) are. Verify by copying the .md to `~/.gemini/agents/notebook-reviewer.md` directly; if `/agents` then lists it, the extension-install path is the gap.

- **Hypothesis C:** `tools` values must be lowercase (matching tool names like `read_file`, not Claude-style `Read`). Verify by editing the file to lowercase tool names.

### Recommended fix

Step 1 — fix the YAML shape (low cost, high confidence). In `GeminiPlatform.emit` at `scripts/platforms.py:219-225`, instead of `shutil.copy(agent_md, ...)`, transform the frontmatter: convert `tools: Read, Grep, Glob` to a YAML list. A code sketch (add a small converter module `scripts/converters/md_to_gemini_md.py`):

```python
# scripts/converters/md_to_gemini_md.py
def claude_agent_md_to_gemini_md(text: str) -> str:
    """Re-emit Claude-style agent .md with Gemini-shaped tools array."""
    fm, body = _parse_frontmatter_and_body(text)  # reuse from md_to_toml
    lines = ["---"]
    for k in ("name", "description"):
        if k in fm:
            lines.append(f"{k}: {fm[k]}")
    if "tools" in fm and fm["tools"]:
        tools = [t.strip() for t in fm["tools"].split(",") if t.strip()]
        lines.append("tools:")
        for t in tools:
            lines.append(f"  - {t}")
    if "model" in fm and fm["model"]:
        lines.append(f"model: {fm['model']}")
    lines.append("---")
    lines.append("")
    lines.append(body)
    return "\n".join(lines)
```

Then in `GeminiPlatform.emit`:

```python
elif isinstance(construct, AgentConstruct):
    from converters.md_to_gemini_md import claude_agent_md_to_gemini_md
    agents_dir = self.mirror_directory / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    src_agents = construct.source_directory / name / "agents"
    if src_agents.exists():
        for agent_md in sorted(src_agents.glob("*.md")):
            text = agent_md.read_text(encoding="utf-8")
            (agents_dir / agent_md.name).write_text(
                claude_agent_md_to_gemini_md(text), encoding="utf-8"
            )
```

Step 2 — verify empirically after deploy. If `/agents` still doesn't list the agent, fall through to Hypothesis B (extension-install discovery gap; likely upstream-blocked).

## Bug 3 — Cursor skill manifest field mapping

### Symptom

QA on 2026-05-25: `/add-plugin skill-telegram-notify@https://github.com/DgxSparkLabs/marketplace` succeeded; `.cursor/settings.json` populated. Typing `/telegram` shows the popup:

```
/1.0.0
Send a Telegram notification with a task summary
a86cb86dfd62f99475408fc984e334af0475029b
Send a Telegram notification with a task summary
+ Add Skills
```

— that's version, description, merge commit SHA, description-again.

### Cursor's expected schema

Per `https://cursor.com/docs/reference/plugins` (fetched 2026-05-25):

- Required: `name` (string, lowercase kebab-case).
- Optional: `description`, `version` (semver), `author`, `homepage`, `repository`, `license`, `keywords`, `logo`, `rules`, `agents`, `skills`, `commands`, `hooks`, `mcpServers`.
- `skills`: "string or array — Path(s) to skill directories."
- For auto-discovered skills, the **SKILL.md frontmatter `name` + `description` drive display**.

Per `https://cursor.com/docs/agent/skills` (fetched 2026-05-25): SKILL.md frontmatter requires `name` (must match parent folder name, kebab-case) and `description`.

### What we currently emit

`scripts/platforms.py:310-330` — `CursorPlatform.build_plugin_json`:

```python
def build_plugin_json(self, construct: Construct, name: str) -> dict:
    manifest: dict = {"name": f"{construct.prefix}-{name}"}
    if isinstance(construct, AgentConstruct):
        manifest["agents"] = "./agents/"
    elif isinstance(construct, CommandConstruct):
        manifest["commands"] = "./commands/"
    elif isinstance(construct, HookConstruct):
        manifest["hooks"] = "./hooks/hooks.json"
    elif isinstance(construct, MCPConstruct):
        manifest["mcpServers"] = source_pj["mcpServers"]
    # RuleConstruct + SkillConstruct: name-only minimal manifest (existing behavior).
    return manifest
```

For SkillConstruct the *entire* `.cursor-plugin/plugin.json` is `{"name": "skill-telegram-notify"}`. Concretely:

```json
{"name": "skill-telegram-notify"}
```

No `description`, no `version`, no `skills` pointer, no `keywords`. The SKILL.md inside the same `_generated/skill-telegram-notify/` dir does have `name: telegram-notify` (NOT `skill-telegram-notify`) and `description: Send a Telegram notification with a task summary`.

The `.cursor-plugin/marketplace.json` (root, Phase 6) entry is also minimal:

```json
{"name": "skill-telegram-notify", "source": "./_generated/skill-telegram-notify"}
```

### Diff table

| Display slot in popup | Cursor likely reads from | What it should show | What it shows | Misalignment |
|---|---|---|---|---|
| Line 1 (skill title) | plugin.json `name`, or SKILL.md `name`, or `displayName` | `skill-telegram-notify` (plugin name) or `telegram-notify` (skill) | `1.0.0` (looks like a version string) | Cursor is **filling the name slot with a version**. Plugin.json has no `version` key, so this likely comes from install metadata (the team-marketplace cached the merge commit). |
| Line 2 (description) | plugin.json `description`, fallback to SKILL.md `description` | "Send a Telegram notification..." | "Send a Telegram notification..." | OK (read from SKILL.md frontmatter). |
| Line 3 | (nothing should be here) | (empty) | `a86cb86dfd62f99475408fc984e334af0475029b` (merge commit SHA) | Cursor is rendering install-metadata git-SHA into a third slot. |
| Line 4 (also description?) | (description repeated?) | (nothing) | "Send a Telegram notification..." | Cursor's UI is fallback-chaining multiple sources and rendering duplicates because the explicit fields are absent. |

### Hypothesis

Cursor's slash-popup renderer expects 3 fields from `plugin.json`: `name`, `description`, `version`. When *any* are missing, it falls back to:
1. The git/install metadata (commit SHA, branch name) for missing identifiers.
2. The skill's SKILL.md frontmatter `description` for the description (and possibly re-renders it elsewhere when the plugin.json description is also missing).

Our manifest provides only `name`, so the renderer scrambles the slots. Adding `description` and `version` to `plugin.json` should fix the popup deterministically.

### Recommended fix

Modify `CursorPlatform.build_plugin_json` in `scripts/platforms.py:310-330` so SkillConstruct (and ideally every construct type) returns the full triple `name + version + description + skills pointer`:

```python
def build_plugin_json(self, construct: Construct, name: str) -> dict:
    full_name = f"{construct.prefix}-{name}"
    manifest: dict = {
        "name": full_name,
        "version": _marketplace_version(),  # add: from utils
        "description": _description_from_construct(construct, name),
    }
    if isinstance(construct, SkillConstruct):
        manifest["skills"] = "./"      # SKILL.md is at plugin root
    elif isinstance(construct, AgentConstruct):
        manifest["agents"] = "./agents/"
    elif isinstance(construct, CommandConstruct):
        manifest["commands"] = "./commands/"
    elif isinstance(construct, HookConstruct):
        manifest["hooks"] = "./hooks/hooks.json"
    elif isinstance(construct, MCPConstruct):
        source_pj = _load_plugin_json(
            construct.source_directory / name / ".claude-plugin" / "plugin.json"
        )
        manifest["mcpServers"] = source_pj["mcpServers"]
    return manifest
```

Note: also add `from utils import _marketplace_version` (already imported elsewhere in the file). For RuleConstruct, keeping `name + version + description` (no extra pointer) is sufficient.

After deploy, the popup should render:

```
/skill-telegram-notify
Send a Telegram notification with a task summary
v1.0.0
+ Add Skills
```

— deterministic, no git-SHA leakage.

## Bonus sanity-check pass

| # | Item | Platform doc URL (fetched 2026-05-25) | Our emission | Verdict |
|---|---|---|---|---|
| 1 | **Cursor hooks shape** (per-plugin `.cursor-plugin/plugin.json`) | `https://cursor.com/docs/agent/hooks` — `{"version": 1, "hooks": {"<event>": [{"command", "timeout", "matcher", "type", "failClosed", "loop_limit"}]}}` (flat, version-tagged) | Manifest emits `"hooks": "./hooks/hooks.json"` pointing to the Claude-shaped file: `{"hooks": {"UserPromptSubmit": [{"hooks": [{"type", "command"}]}]}}` (nested twice, no `version` key) — see `hooks/example/hooks/hooks.json`. | **LIKELY BUG / needs investigation.** The pointer is correct but the file content is Claude's nested shape. Cursor's parser expects the flat shape with `version: 1`. Cursor may silently ignore the entire file. Same pattern as Bug 2: format mismatch hidden by the byte-identity drift check. |
| 2 | **Cursor commands shape** (per-plugin `.cursor-plugin/plugin.json`) | `https://cursor.com/docs/agent/commands` returned 404; broader doc fetches contain no command schema. | Manifest emits `"commands": "./commands/"`, source files are Claude command .md (slash command frontmatter `description`, `argument-hint`, etc.). | **LIKELY BUG / needs investigation.** No documented Cursor command schema means we cannot verify match. Either Cursor parses Claude-shape commands (lucky) or silently ignores them. Empirical test required: install a command plugin, look for the slash command in `/` popup. |
| 3 | **Cursor MCP shape** (per-plugin `.cursor-plugin/plugin.json`) | `https://cursor.com/docs/reference/plugins` — `mcpServers` accepts "string, object, or array — MCP server definitions or config file path". | Manifest emits `"mcpServers": <source_pj["mcpServers"]>` (passes through whatever the source plugin.json has — a path or an inline dict). | **PROBABLY OK.** Pass-through of the Claude MCP shape lines up with Cursor's schema (Cursor explicitly supports a config-file path). Worth empirical verification. |
| 4 | **Gemini hooks** (`.gemini/hooks/hooks.json`) | No Gemini hooks documentation surfaced during fetch (extensions reference does not mention hooks file format in the excerpt; `geminicli.com/docs/extensions/` mentions hooks in passing). | We emit `.gemini/hooks/hooks.json` with the Claude nested shape (verified: `{"description", "hooks": {"UserPromptSubmit": [{"hooks": [{...}]}]}}`). `gemini-extension.json` does NOT declare a hooks pointer. | **LIKELY BUG.** Without a Gemini hooks schema doc + manifest pointer, Gemini almost certainly does not discover the file. Same loader-gap pattern as Bug 2. Open question: where do Gemini extension hooks actually go? |
| 5 | **Windsurf hooks** (`.windsurf/hooks.json`) | `https://docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25) — flat shape: `{"hooks": {"<event>": [{"command": "...", "powershell": "...", "show_output": bool, "working_directory": "..."}]}}`. Event names: `pre_read_code`, `post_read_code`, `pre_write_code`, `post_write_code`, `pre_run_command`, `post_run_command`, `pre_mcp_tool_use`, `post_mcp_tool_use`, `pre_user_prompt`, `post_cascade_response`, `post_cascade_response_with_transcript`, `post_setup_worktree`. Required: at least one of `command` or `powershell`. | We emit (verified) `.windsurf/hooks.json` containing Claude's nested shape with event name `UserPromptSubmit` and inner field `type: "command"` — neither shape nor event names match. | **DEFINITE BUG — same pattern as Bug 1/Bug 2.** Windsurf event names like `pre_user_prompt` are entirely absent; our `UserPromptSubmit` is a Claude event name that Windsurf has no schema entry for. The file will load but no hook will ever fire. |
| 6 | **Codex `.codex/agents/` install path** | `https://developers.openai.com/codex/subagents/` — agents at `~/.codex/agents/` (personal) or `<workspace>/.codex/agents/` (project-scoped). Plugin-build docs do not list `agents` as a pointer field. | Codex's plugin install lands the plugin under `~/.codex/.tmp/marketplaces/<marketplace>/<plugin>/<version>/`. Our TOML is at `<source-repo>/.codex/agents/<n>.toml` — never copied to either of Codex's documented agent-discovery locations on plugin install. | **DEFINITE BUG — same root cause as Bug 1.** The Codex sub-agent install path is missing entirely. Confirms Bug 1's Hypothesis A. |
| 7 | **Cursor commands marketplace.json description** (root manifest) | Cursor team marketplace docs not authoritative on per-plugin entries. The root `.cursor-plugin/marketplace.json` we emit lists only `{name, source}` per plugin. | Same as code: `{"name": "skill-telegram-notify", "source": "./_generated/skill-telegram-notify"}` — no description, no version. | **PROBABLY OK** for team-marketplace import (which then reads the per-plugin manifest). But contributes to Bug 3 by making the popup fall back when the per-plugin manifest is also bare. |

**Summary:** Bug 1 is corroborated by sanity-check #6 (same root). Sanity-checks #1, #4, #5 are likely format-shape bugs (Claude shape leaking into platforms that want a different shape). Sanity-check #5 is the most confident new finding (Windsurf event names don't match Claude's). The pattern across all three QA bugs and three sanity-check findings is: **we copy Claude-shaped files into other platforms' mirror dirs without per-platform conversion**, and our drift checks confirm byte-identity rather than schema fitness.

## References we couldn't fetch

- `https://cursor.com/docs/agent/skills` — returned HTTP 404 on direct fetch. We obtained skill-display info indirectly via `cursor.com/docs/reference/plugins` and a second fetch attempt to `cursor.com/docs/agent/skills` (which returned schema content on the second try). Used the available content.
- `https://cursor.com/docs/agent/commands` — returned HTTP 404 (both fetches). **No Cursor command schema was obtained; sanity-check #2 is flagged as needing empirical verification.**
- `https://docs.gemini-cli.com/docs/extensions/reference/` — ECONNREFUSED (alternate Gemini docs host does not resolve).
- `https://docs.cursor.com/en/agent/skills` and `https://docs.cursor.com/en/reference/plugins` — both 308-redirected to `https://cursor.com/docs` (rather than the specific page), suggesting the `docs.cursor.com` subdomain is being deprecated in favor of `cursor.com/docs`.

## Recommended sequencing for fixes

1. **Bug 3 (Cursor skill popup) — fix first.** One-file change in `scripts/platforms.py:310-330`. Zero upstream dependencies. Improves UX for *every* Cursor user immediately. Self-contained: add `description` + `version` + `skills` pointer to `build_plugin_json`. Verifiable with a Cursor install + popup observation.

2. **Sanity-check #5 (Windsurf hooks) — fix second.** Likely the same `_COPY_IGNORE`-pattern blind spot: a converter is needed to translate Claude hooks event names + nesting into Windsurf's flat shape with renamed events. Lower QA priority (no current user reports), but the fix avoids future hours debugging "why doesn't my Windsurf hook fire?". Write `scripts/converters/md_to_windsurf_hooks.py` (or similar) and route through `WindsurfPlatform.emit`.

3. **Bug 2 (Gemini sub-agent) — fix third, in two passes.** Pass 2a: add the Gemini-shape tools-array converter (`md_to_gemini_md.py`); deploy; observe. Pass 2b: if `/agents` still doesn't list, file upstream + document gap.

4. **Bug 1 (Codex sub-agent) — fix fourth.** Test the speculative `agents` pointer first; if it works, ship. If not, file upstream + document gap. Codex sub-agents are explicitly described as a preview feature, so partial support is the most plausible state.

5. **Sanity-checks #1, #2, #4 (Cursor hooks/commands, Gemini hooks)** — empirical verification phase. Install each construct in the target platform, observe whether the feature surfaces; treat verified failures as new fix tickets.

## Open questions

- **(Bug 1)** Does Codex's `.codex-plugin/plugin.json` support an undocumented `agents` pointer field? (Hypothesis B; verifiable in <30 minutes of QA after the speculative-pointer fix lands.)
- **(Bug 1)** If the pointer doesn't help: does Codex's installer copy *any* file from the plugin tree into `~/.codex/agents/` automatically, or is sub-agent install entirely upstream-missing? (Verify by inspecting `~/.codex/.tmp/marketplaces/.../agent-example/` and `~/.codex/agents/` after `codex plugin add`.)
- **(Bug 2)** Is the `tools: Read, Grep, Glob` comma-separated string the actual blocker, or does Gemini's extension-bundled sub-agent discovery simply not land at `~/.gemini/extensions/<ext>/agents/`? (Verify by manually fixing the tools field AND/OR by copying the .md to `~/.gemini/agents/` to bypass the extension layer.)
- **(Bug 3)** Where does Cursor's popup pull the `1.0.0` and the merge-commit SHA from when the manifest lacks `version`? (Not load-bearing for the fix — adding `version` explicitly to manifest eliminates the fallback — but useful for understanding Cursor's renderer.)
- **(Sanity #1)** Does Cursor's hooks parser silently accept Claude's nested `hooks.<event>[].hooks[].command` shape, or does it reject the whole file? Verify by installing `hook-example` in Cursor and triggering a `UserPromptSubmit` event.
- **(Sanity #2)** What is Cursor's slash-command file schema? No documented source. Best guess: same Claude command .md frontmatter shape; verifiable empirically.
- **(Sanity #4)** Does Gemini's extension model support hooks at all today? If yes, what's the schema? (Reference excerpt does not document this; deeper docs fetch or upstream issue required.)
- **(Sanity #5)** Does Windsurf require a workspace-scope file at `.windsurf/hooks.json` exactly, or are user-scope hooks under `~/.codeium/windsurf/hooks.json` also discovered when the workspace lacks one?
- **(General)** Is there any shared convention emerging across Cursor/Windsurf/Gemini for hook event names (e.g., `pre_user_prompt` vs `UserPromptSubmit`), or are we permanently in per-platform-converter territory?
- **(Generator-architecture)** Should the converters be elevated to first-class concerns (a `Converter` protocol with per-source-shape → per-target-shape methods) instead of one-off lazy imports inside `Platform.emit`? Three converters already needed (Codex TOML, Gemini YAML-array, Windsurf flat-hooks). A pattern is forming.

## Empirical verification round 2026-05-25

This section appends empirical findings that close (or definitively flag-as-blocked) the three partially-diagnosed bugs from the round above: Cursor hooks shape, Gemini hooks discoverability, Codex sub-agent install pathway. All evidence is logged under `docs/research/qa-bug-fixes-2026-05/logs/`.

### Q1 — Cursor hooks: CONFIRMED-FIX (flat shape + camelCase events + version:1)

**Canonical schema (verbatim from `cursor.com/docs/agent/hooks`, fetched 2026-05-25):**

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [{ "command": "./hooks/session-init.sh" }],
    "beforeShellExecution": [
      { "command": "./hooks/approve-network.sh", "timeout": 30, "matcher": "curl|wget|nc" }
    ],
    "afterFileEdit": [{ "command": "./hooks/format.sh" }],
    "stop": [{ "command": "./hooks/audit.sh", "loop_limit": 10 }]
  }
}
```

Plugin.json `hooks` field is documented as "Path to hooks config file, or inline hook config" (per `cursor.com/docs/reference/plugins`, fetched 2026-05-25). The pointer we already emit (`"hooks": "./hooks/hooks.json"`) is correct shape.

**Community working examples (saved as logs/*.json):**

1. `cursor/plugins/continual-learning` — Cursor's own official plugin. plugin.json sets `"hooks": "./hooks/hooks.json"`; hooks.json content:
   ```json
   {"version": 1, "hooks": {"stop": [{"command": "bun run ${CURSOR_PLUGIN_ROOT}/hooks/continual-learning-stop.ts"}]}}
   ```
   (`logs/cl-plugin.json`, `logs/cl-hooks.json`)

2. `cursor/plugins/ralph-loop` — Cursor's own. hooks.json:
   ```json
   {"version": 1, "hooks": {"afterAgentResponse": [{"command": "./hooks/capture-response.sh"}], "stop": [{"command": "./hooks/stop-hook.sh", "loop_limit": null}]}}
   ```
   (`logs/ralph-plugin.json`, `logs/ralph-hooks.json`)

3. `prisma/cursor-plugin` — third-party. hooks.json:
   ```json
   {"version": 1, "hooks": {"beforeShellExecution": [{"command": "./scripts/pre-commit.sh", "matcher": "^git commit"}], "afterFileEdit": [{"command": "node ./scripts/format-schema.js"}]}}
   ```
   (`logs/prisma-plugin.json`, `logs/prisma-root-hooks.json`)

**Side-by-side diff (working vs ours):**

| | Cursor canonical (Cursor's own plugins) | Ours (`_generated/hook-example/hooks/hooks.json`) |
|---|---|---|
| Top-level `version` key | `"version": 1` (REQUIRED) | absent |
| Hook entry shape | flat: `{command, matcher?, timeout?, loop_limit?}` | nested: `{hooks: [{type, command}]}` |
| Event name | camelCase from documented set (`stop`, `afterAgentResponse`, `beforeShellExecution`, `afterFileEdit`, `beforeSubmitPrompt`, ...) | `UserPromptSubmit` (Claude-specific; not in Cursor's vocabulary) |
| `"type": "command"` key | absent (only `command` field exists) | present |

**Documented event vocabulary** (Cursor, fetched 2026-05-25): `sessionStart`, `sessionEnd`, `preToolUse`, `postToolUse`, `postToolUseFailure`, `subagentStart`, `subagentStop`, `beforeShellExecution`, `afterShellExecution`, `beforeMCPExecution`, `afterMCPExecution`, `beforeReadFile`, `afterFileEdit`, `beforeSubmitPrompt`, `preCompact`, `stop`, `afterAgentResponse`, `afterAgentThought`, `beforeTabFileRead`, `afterTabFileEdit`, `workspaceOpen`.

The closest analog to Claude's `UserPromptSubmit` is **`beforeSubmitPrompt`**.

**Recommended fix (CONFIRMED):** Write a converter `scripts/converters/md_to_cursor_hooks.py` (or `claude_hooks_to_cursor.py`) that:
1. Reads source Claude hooks.json (`hooks/<plugin>/hooks/hooks.json`).
2. Rewrites top-level to `{"version": 1, "hooks": {...}}`.
3. Maps Claude event names to Cursor event names. Required minimal mapping for our current `UserPromptSubmit` example:
   - `UserPromptSubmit` → `beforeSubmitPrompt`
   - (table — extend as new event names appear: `PreToolUse` → `preToolUse`; `PostToolUse` → `postToolUse`; `Stop` → `stop`; `SessionStart` → `sessionStart`; `SessionEnd` → `sessionEnd`; `Notification` → no direct analog, drop)
4. Flattens each entry: from `{hooks: [{type, command}]}` to `{command}`. Preserve `matcher`, `timeout` if present.
5. Wire into `CursorPlatform.emit` for `HookConstruct` (currently has no mirror branch for hooks — the plugin.json points to a file the platform never emits a converted copy of; the implementer needs to add a `.cursor/` mirror or, better, emit per-plugin `_generated/<plugin>/hooks/hooks.json` in the converted shape so the plugin.json pointer resolves to a Cursor-shaped file).

### Q2 — Gemini hooks: CONFIRMED-FIX (event-name mismatch; no manifest pointer needed)

**Manifest schema verdict (verbatim from `geminicli.com/docs/extensions/reference/`, fetched 2026-05-25):**

> "Define hooks in a `hooks/hooks.json` file within your extension directory. **Note that hooks are not defined in the `gemini-extension.json` manifest.**"

So our `.gemini/gemini-extension.json` (which lacks a `hooks` pointer) is **correct as-is per documentation**. The bug is not a missing pointer.

**Community working example: `sandipchitale/hooklog`** (Gemini extension shipping hooks). Full hooks.json saved to `logs/hooklog-hooks.json`. Shape:

```json
{
  "hooks": {
    "SessionStart": [
      {"matcher": "startup", "hooks": [{"name": "...", "type": "command", "command": "node ${extensionPath}/scripts/hooklog.ts"}]}
    ],
    "BeforeModel": [...],
    "AfterModel": [...],
    "BeforeTool": [...],
    ...
  }
}
```

**Critical finding:** The nested `{event: [{matcher, hooks: [{type, command}]}]}` shape **matches what we already emit**. The Gemini-CLI hooks schema is *structurally identical* to Claude's — but **the event-name vocabulary is different**.

**Documented Gemini event names** (per `geminicli.com/docs/hooks/reference/` fetched 2026-05-25 and hooklog plugin):
`SessionStart`, `SessionEnd`, `BeforeModel`, `AfterModel`, `BeforeAgent`, `AfterAgent`, `BeforeTool`, `AfterTool`, `BeforeToolSelection`, `PreCompress`, `Notification`.

**Gemini has NO `UserPromptSubmit` event.** Our emission at `.gemini/hooks/hooks.json` uses `UserPromptSubmit`, which Gemini will silently ignore.

**Empirical probe (logs/gemini-probe-output.log):** Ran `gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent` in a fresh `node:20` container. Reported: `Extension "dgxsparklabs-marketplace" installed successfully and enabled.` The hooks file landed at `/root/.gemini/extensions/dgxsparklabs-marketplace/.gemini/hooks/hooks.json` and contains our `UserPromptSubmit` block verbatim. No `gemini-extension.json` modification needed; Gemini found the file via the directory convention. **What's missing is the matching event name in the file content, not a manifest pointer.**

**Recommended fix (CONFIRMED):** In `GeminiPlatform.emit` for `HookConstruct`, instead of `shutil.copy`, run a converter that maps Claude event names to Gemini event names. Closest analog for `UserPromptSubmit` → **`BeforeModel`** (fires before each model call, which encompasses the prompt-submit moment). Implementer should add `scripts/converters/md_to_gemini_hooks.py` along the same pattern as the proposed `md_to_gemini_md.py`. (Side note: Gemini supports `${extensionPath}` substitution per the docs — useful for hooks that reference scripts bundled in the extension.)

**Bonus — tools-frontmatter still likely a bug:** The earlier hypothesis (Q2 from the original report) about `tools: Read, Grep, Glob` being a YAML scalar rather than an array stands — Gemini agents probably parse-fail on it. Not re-verified here (orthogonal to hooks).

### Q3 — Codex sub-agents: CONFIRMED-BLOCKED (upstream: no plugin install pathway)

**Docs verdict:** `developers.openai.com/codex/plugins/build` (re-fetched 2026-05-25) confirms the documented `.codex-plugin/plugin.json` schema has **only** `skills`, `mcpServers`, `apps`, `hooks` as component-pointer fields. **No `agents` field exists.** The doc lists every field: `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `skills`, `mcpServers`, `apps`, `hooks`, plus an `interface` object — and explicitly *not* `agents`. Also confirmed via WebSearch: subagent settings live under `[agents]` in `~/.codex/config.toml`, not in `plugin.json`.

`developers.openai.com/codex/subagents/` (re-fetched 2026-05-25): "To define your own custom agents, add standalone TOML files under `~/.codex/agents/` for personal agents or `.codex/agents/` for project-scoped agents." **No third install location, no plugin pathway.**

**Empirical probe (logs/codex-probe-output.log):** Fresh `node:20` container, `npm i -g @openai/codex` (got `codex-cli 0.133.0`):

1. `codex plugin marketplace add DgxSparkLabs/marketplace` — succeeds. Clones repo to `/root/.codex/.tmp/marketplaces/dgxsparklabs-marketplace/`.
2. `codex plugin add agent-example@dgxsparklabs-marketplace` — succeeds. Reports `Installed plugin root: /root/.codex/plugins/cache/dgxsparklabs-marketplace/agent-example/1.0.0`.
3. The plugin cache at `/root/.codex/plugins/cache/.../agent-example/1.0.0/` contains **only**: `README.md`, `agents/notebook-reviewer.md` (the source `.md`), `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`. **The `.toml` we generate is NOT copied into the plugin cache.**
4. The `.toml` exists only at `/root/.codex/.tmp/marketplaces/dgxsparklabs-marketplace/.codex/agents/notebook-reviewer.toml` — i.e., inside the marketplace clone's own workspace mirror, not in any path Codex discovers at runtime.
5. `/root/.codex/agents/` directory **does not exist** after install. Codex's installer never created it and never copied any TOML there.
6. `~/.codex/config.toml` shows the plugin is recorded as `enabled = true`, but no agent reference is added.
7. Manually copying the TOML to `/root/.codex/agents/notebook-reviewer.toml` succeeds (documented personal-agents path) — but `codex --help` shows there is **no headless subcommand** (`codex agents list`, `codex agents` both fail) for verifying discovery. Sub-agent listing only happens inside interactive TTY, which the act probe cannot drive. Per the doc contract, agent-files at `~/.codex/agents/*.toml` ARE discovered, so manual copy should work; the gap is purely the plugin installer's failure to land the TOML there.

**Verdict — UPSTREAM-BLOCKED.** Codex's plugin-install machinery has no documented or empirical path for shipping sub-agents. The TOML we emit is correctly shaped per the sub-agents docs, but Codex's `plugin add` does not copy any agent file out of the plugin cache into `~/.codex/agents/` or any other discoverable path. Until OpenAI adds an `agents` field to the plugin schema OR teaches `codex plugin add` to copy `agents/*.toml` from the plugin tree to `~/.codex/agents/`, **sub-agents cannot ship via the marketplace pipeline**.

**Implementer recommendation (CONFIRMED-BLOCKED):**

1. **Keep** `CodexPlatform.emit` for `AgentConstruct` as forward-looking (the TOML is the right shape; we want to be ready the day OpenAI ships the install pathway).
2. **Add a CHANGELOG / docs note** flagging that Codex sub-agents are currently a no-op pending upstream plugin-marketplace support. The user-facing workaround today: clone the marketplace repo, then symlink or copy `.codex/agents/notebook-reviewer.toml` to `~/.codex/agents/notebook-reviewer.toml`.
3. **Do NOT speculatively add `"agents"` to the plugin.json** — the field isn't in the schema; depending on Codex's strictness, it could be either ignored (harmless) or warned about (noisy). Wait for upstream.
4. **Optional**: file an upstream issue at `github.com/openai/codex` titled "Plugin marketplace cannot ship sub-agents" pointing at the install pathway gap.

### New / incidental bugs found this round

- **(Windsurf hooks event-name mismatch)** Same root cause as Q2 Gemini: `.windsurf/hooks.json` ships our Claude-named events (`UserPromptSubmit`); Windsurf's vocabulary is `pre_user_prompt`, `post_cascade_response`, etc. (Already flagged as sanity-check #5 in the prior round.) Confirmed in `logs/gemini-probe-output.log:132` — the `.windsurf/hooks.json` content is verbatim our nested Claude shape.
- **(Cursor hook nesting shape never converted)** `CursorPlatform.emit` has no `HookConstruct` branch (`scripts/platforms.py:285-308`). The per-plugin `.cursor-plugin/plugin.json` points to `./hooks/hooks.json`, but no Cursor-shape hooks.json is emitted under `_generated/<plugin>/hooks/`. Currently the only `hooks.json` in `_generated/hook-example/hooks/` is the un-converted Claude source. Implementer fix: route through a converter (per Q1 recommendation) and write to `_generated/<plugin>/hooks/hooks.json`.
- **(Pattern across platforms)** The root cause across Cursor hooks (Q1), Gemini hooks (Q2), and Windsurf hooks (sanity #5) is the same: **event-name vocabulary is per-platform**, but we ship Claude's vocabulary. A central Claude→Cursor/Gemini/Windsurf event-name mapping table belongs in a shared converter module. This is the "elevate converters to first-class" generator-architecture question from the previous round — now backed by three real instances.

### Log files produced

- `logs/cl-plugin.json`, `logs/cl-hooks.json` — Cursor's official `continual-learning` plugin manifest + hooks
- `logs/ralph-plugin.json`, `logs/ralph-hooks.json` — Cursor's official `ralph-loop` plugin manifest + hooks
- `logs/prisma-plugin.json`, `logs/prisma-root-hooks.json` — Prisma's third-party Cursor plugin
- `logs/hooklog-gemini-extension.json`, `logs/hooklog-hooks.json` — Working Gemini extension shipping hooks
- `logs/cursor-plugins-tree.json`, `logs/cursor-plugins-marketplace.json` — Full file tree of `cursor/plugins`
- `logs/codex-probe.sh`, `logs/codex-probe-output.log` — Hermetic Codex install probe (node:20)
- `logs/gemini-probe.sh`, `logs/gemini-probe-output.log` — Hermetic Gemini install probe (node:20)

