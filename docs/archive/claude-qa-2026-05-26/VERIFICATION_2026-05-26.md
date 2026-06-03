---
date: 2026-05-26
purpose: hermetic-Docker-verification-of-claude-qa-fixes
arc: claude/qa-and-user-guide
status: complete
container: node:20
claude-version: 2.1.150
branch-sha: 35fdadb3790edb8ed96a56b032bae58bd5a257bf
---

# Claude QA Verification — Docker Hermetic Round 2026-05-26

## TL;DR

- **All 9 findings (F1-F9) PASS** on the hermetically-verifiable checks. Zero failures, zero residual schema warnings or errors.
- **General install/list flow PASSES end-to-end without auth**: `marketplace add`, `marketplace list`, `plugin list`, `plugin install`, `plugin list` (post-install), `plugin disable`, `plugin enable`, `plugin uninstall`, `marketplace remove` — every command exits 0 with sensible output. This means the install-chain cells the spec hedged as auth-blocked actually run unauthed.
- **4 cells partially SKIPPED-DUE-TO-AUTH** for their interactive aspects only: F4 visual theme distinctness, F5 actual hook firing observation, F7 actual `/` invocation in a session, F9 actual output-style activation. The underlying schema/file fixes for all four passed hermetically; only the in-session UX confirmation requires an authed interactive Claude.
- Container `qa-claude-verify` cleaned up; 17 log files captured at `docs/research/claude-qa-2026-05-26/verification-logs/`.

## Container environment

- Image: `node:20` (ephemeral, named `qa-claude-verify`)
- Inside-container install: `apt-get install -y git jq`, then `npm install -g @anthropic-ai/claude-code`
- `claude --version` → `2.1.150 (Claude Code)`
- Clone: `git clone --branch claude/qa-and-user-guide --depth 1 https://github.com/DgxSparkLabs/marketplace.git /workspace/marketplace`
- HEAD SHA: `35fdadb3790edb8ed96a56b032bae58bd5a257bf` (matches latest commit on `claude/qa-and-user-guide` at clone time: `docs(changelog): add 2026-05-26 entry for Claude QA + user guide`)
- Verification timestamp: 2026-05-25 (run-day) for the 2026-05-26-dated arc

## Per-cell verdicts

### F1 — Marketplace description warning resolved

- **Command**: `claude plugin validate ./`
- **Log**: `verification-logs/F1-validate-marketplace.log`
- **Exit**: 0
- **Output**:
  ```
  Validating marketplace manifest: /workspace/marketplace/.claude-plugin/marketplace.json

  ✔ Validation passed
  ```
- **Verdict**: **PASS** — zero warnings, zero errors. The original `description: No marketplace description provided` warning is gone. `MARKETPLACE.toml` carries the description, and the generated `.claude-plugin/marketplace.json` propagates it (confirmed by the validator's silence on the field).

### F2 — LSP example schema

- **Command**: `claude plugin validate _generated/lsp-example/`
- **Log**: `verification-logs/F2-validate-lsp.log`
- **Exit**: 0
- **Output**:
  ```
  Validating plugin manifest: /workspace/marketplace/_generated/lsp-example/.claude-plugin/plugin.json

  ✔ Validation passed
  ```
- **Verdict**: **PASS** — no schema errors about `lspServers.command` or `extensionToLanguage`. Pre-fix this cell would have failed with three validator errors per the F2 symptom block; post-fix the validator is silent.

### F3 — Monitor example shape

- **Command**: `claude plugin validate _generated/monitor-example/`
- **Log**: `verification-logs/F3-validate-monitor.log`
- **Exit**: 0
- **Output**: `✔ Validation passed`
- **Verdict**: **PASS** — no "expected array received object" error.

### F4 — Theme example schema

- **Command (hermetic)**: `claude plugin validate _generated/theme-example/`
- **Log**: `verification-logs/F4-validate-theme.log`
- **Exit**: 0
- **Output**: `✔ Validation passed`
- **Verdict**: **PASS-SCHEMA / SKIPPED-AUTH-FOR-VISUAL**
  - Schema correctness verified hermetically.
  - Visual distinctness from default Dark mode requires an interactive authed Claude session to pick the theme via `/theme` and observe colors changing. Deferred to hands-on.

### F5 — Hook example schema + coverage

- **Hermetic check 1 (schema)**: `claude plugin validate _generated/hook-example/` — Exit 0, `✔ Validation passed`. Log: `verification-logs/F5-validate-hook.log`.
- **Hermetic check 2 (event coverage)**: parsed `hooks/example/hooks/hooks.json` — all 6 required event types present: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SessionEnd`.
- **Hermetic check 3 (per-type sentinels)**: parsed all hook commands — each writes to a distinct `/tmp/hook-fired-<type>.log` sentinel:
  - `/tmp/hook-fired-sessionstart.log`
  - `/tmp/hook-fired-userpromptsubmit.log`
  - `/tmp/hook-fired-pretooluse.log`
  - `/tmp/hook-fired-posttooluse.log`
  - `/tmp/hook-fired-stop.log`
  - `/tmp/hook-fired-sessionend.log`
- Log: `verification-logs/F5-hook-json-content.log`
- **Verdict**: **PASS-SCHEMA-AND-COVERAGE / SKIPPED-AUTH-FOR-FIRING-OBSERVATION**
  - Actual hook firing in an interactive Claude session is deferred to hands-on (sentinel-file tail check).

### F6 — MCP example uv prerequisite documented

- **Check**: `mcp-servers/example/README.md` exists and mentions `uv`.
- **Log**: `verification-logs/F6-mcp-readme.log`
- **Evidence**: README has a "## Prerequisites" section that says:
  > This example launches the MCP server with **`uvx mcp-server-fetch`**, so the host must have **[`uv`](https://github.com/astral-sh/uv)** installed and on `PATH`. Without it, Claude reports `plugin:mcp-example:example-fetch: uvx mcp-server-fetch - ✗ Failed to connect` after install.
  >
  > Install `uv` once (any platform):
  >
  > `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS / Linux)
  > `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)
- **Verdict**: **PASS** — prerequisite is prominently documented with install commands for both POSIX and Windows hosts.

### F7 — Slash command namespacing

- **Hermetic check**: validate manifest emissions for `skill-example`, `command-example`, `agent-example`, `mcp-example` and confirm their `name` fields match the namespacing prefix the cell would invoke.
- **Log**: `verification-logs/F7-namespacing-manifests.log`
- **Evidence**: All four manifests have correct `name` fields (`skill-example`, `command-example`, `agent-example`, `mcp-example`) — so the namespaced invocations resolve as `/skill-example:example-skill`, `/command-example:example-command`, `agent-example:notebook-reviewer`, `mcp__mcp-example__example-fetch`. All four pass `claude plugin validate`.
- **Verdict**: **PASS-MANIFEST / SKIPPED-AUTH-FOR-INVOCATION**
  - Actual `/` autocomplete observation and `/agents` panel inspection require an interactive authed session. Deferred to hands-on.

### F8 — Claude rule deprecation

- **Hermetic check 1**: `find _generated -path "*rule-*" -name "plugin.json" -path "*/.claude-plugin/*" | wc -l` → **0** (no Claude rule manifests emitted)
- **Hermetic check 2**: `find _generated -name "activate.sh" | wc -l` → **0** (no `activate.sh` files anywhere)
- **Hermetic check 3**: `claude plugin marketplace add /workspace/marketplace && claude plugin list --available --json | jq '.available[].name' | grep -c '^rule-'` → **0** (no `rule-*` plugins surface in Claude's marketplace listing)
- **Hermetic check 4**: `claude plugin list --available --json | jq '.available[].name' | grep bundle-quality-rules` → **empty** (cascading deprecation worked)
- **Bonus evidence**: total Claude-visible plugins from marketplace = **53** (matches `.claude-plugin/marketplace.json` plugin count); **18 bundle-* plugins** remain (the non-Claude-rule bundles).
- **Bonus observation**: 22 `_generated/rule-*` directories still exist on disk, but they only contain `.cursor-plugin/`, `README.md`, and `rules/` subdirs — no Claude `.claude-plugin/` directory. So the source is preserved for Cursor/Windsurf/Agents emission, but Claude sees nothing.
- **Logs**: `verification-logs/F8-rule-deprecation.log`, `verification-logs/F8b-rule-dirs-listing.log`, `verification-logs/F8c-plugin-list-rules.log`, `verification-logs/F8d-plugin-list-available.log`
- **Verdict**: **PASS** — full deprecation per all four hermetic counts.

### F9 — Output style activation observability

- **Hermetic check**: `output-styles/example/output-styles/lab-notebook-voice.md` exists with correct frontmatter.
- **Log**: `verification-logs/F9-output-style-file.log`
- **Evidence**: file exists; frontmatter has `name: Lab Notebook Voice`, `description: ...`, `keep-coding-instructions: true`; body has the `## Voice` and `## Format` sections with the lab-notebook prose markers (Cite source, no hedging, `Next:` line spec).
- **Verdict**: **PASS-FILE-EXISTS / SKIPPED-AUTH-FOR-ACTIVATION**
  - Actual `/config → Output style` picker, `/clear`, behavioral observation require an interactive authed session. Deferred to hands-on.

### Install/List flow (general marketplace ops)

- **Logs**: `verification-logs/IF-install-flow-1-3.log`, `verification-logs/IF-install-flow-4-5.log`, `verification-logs/IF-install-flow-6-9.log`

| Step | Command | Outcome | Verdict |
|---|---|---|---|
| 1 | `claude plugin marketplace add /workspace/marketplace` | `✔ Successfully added marketplace: dgxsparklabs-marketplace` | PASS |
| 2 | `claude plugin marketplace list` | shows `dgxsparklabs-marketplace` with source path | PASS |
| 3 | `claude plugin list` | "No plugins installed" (correct — none yet) | PASS |
| 4 | `claude plugin install skill-example@dgxsparklabs-marketplace --scope project` | `✔ Successfully installed plugin: skill-example` | PASS |
| 5 | `claude plugin list` | shows `skill-example` v1.0.0, scope project, status enabled | PASS |
| 6 | `claude plugin disable skill-example` | `✔ Successfully disabled plugin: skill-example` | PASS |
| 7 | `claude plugin enable skill-example` | `✔ Successfully enabled plugin: skill-example` | PASS |
| 8 | `claude plugin uninstall skill-example --scope project` | `✔ Successfully uninstalled plugin: skill-example` | PASS |
| 9 | `claude plugin marketplace remove dgxsparklabs-marketplace` | `✔ Successfully removed marketplace` | PASS |

**Important auth finding**: the install/disable/enable/uninstall chain ran **without any auth prompt** on Claude CLI 2.1.150. The spec hedged these cells as potentially auth-blocked (`SKIPPED-AUTH-CHAIN`). They are NOT auth-blocked — only the interactive in-session `/` invocations / `/theme` / `/config` / hook-firing-from-prompt cells require an authed interactive Claude. Plugin lifecycle management is fully scriptable in headless containers.

## Cells SKIPPED due to auth requirement

| Cell | What requires auth | Recommended hands-on test |
|---|---|---|
| F4 (visual) | Picking the theme + observing palette change | Open authed Claude in workspace, install `theme-example`, run `/theme`, pick "Lab Notebook", confirm with Enter, observe foreground/background change |
| F5 (firing) | Triggering hooks from inside a session | After `claude plugin install hook-example`, start session, submit a prompt, then in another shell `tail /tmp/hook-fired-userpromptsubmit.log` (and the other 5 sentinel files for each event variant) |
| F7a (skill invocation) | `/` autocomplete in session | Install `skill-example`, type `/` in session, observe `/skill-example:example-skill` resolves correctly |
| F7b (agent invocation) | `/agents` panel in session | Install `agent-example`, run `/agents`, observe `agent-example:notebook-reviewer` entry |
| F7c (MCP tool naming) | Tool name in `claude --debug` output | Install `mcp-example` + `uv`, ask Claude to fetch a URL, watch debug log for `mcp__mcp-example__example-fetch` |
| F9 (activation) | `/config → Output style` picker + behavioral response markers | Install `output-style-example`, `/config → Output style → Lab Notebook Voice`, `/clear`, ask "Explain `_base_plugin_shape` in scripts/constructs.py", observe `Next:` line and citation markers; A/B against default style |

## Summary

- **Hermetic cells PASS**: 9 / 9 findings (F1, F2, F3, F4 schema, F5 schema+coverage, F6, F7 manifests, F8, F9 file-exists) + 9 / 9 install-flow steps.
- **Hermetic cells FAIL**: 0.
- **Cells with auth-deferred sub-aspects**: 4 (F4 visual, F5 firing, F7 invocation, F9 activation). Each has a passing hermetic check; only the in-session UX confirmation remains for hands-on.
- **Newly surfaced bugs**: none.
- **Notable observation (not a bug)**: 22 `_generated/rule-*` source directories still exist on disk after F8's deprecation, but they correctly contain no Claude `.claude-plugin/plugin.json` and no `activate.sh` — they only hold `.cursor-plugin/`, `README.md`, `rules/` for the non-Claude platform emissions. This matches the F8 design intent ("Keep source `rules/<name>/`. Cursor and Windsurf consume them").

## Next steps

PR #6 is ready for human review and merge **after** the auth-required hands-on cells (F4 visual, F5 firing, F7 invocation, F9 activation) are confirmed by a human-driven interactive Claude session. No code changes required; all schema and structural fixes are verified end-to-end in Docker.

If a hands-on tester wants the fastest minimum-viable validation:

1. `claude plugin install hook-example` + submit one prompt + `tail /tmp/hook-fired-userpromptsubmit.log` (proves F5 end-to-end with one observation).
2. `claude plugin install theme-example` + `/theme` + pick Lab Notebook (proves F4 visual).
3. `claude plugin install output-style-example` + `/config → Output style → Lab Notebook Voice` + `/clear` + ask the prompt from the cell (proves F9 activation).
4. Type `/` with `skill-example` installed (proves F7 namespacing).

Four interactive cells, ~5 minutes of human time. Everything else is already proven hermetic.
