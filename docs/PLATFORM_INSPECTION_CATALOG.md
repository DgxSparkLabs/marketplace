# Platform Inspection Catalog

This catalog is the **executable specification** for multi-platform CI/CD validation. Each row is a verified auth-free CLI command that introspects what a platform sees from our marketplace. CI workflows transcribe these rows into assertions: install our marketplace → run the cataloged command → match expected output.

If a platform's command surface changes (deprecation, rename, new flag), this catalog gets the edit and the corresponding CI step gets the matching edit. No spec drift between docs and tests.

**Verification date:** 2026-05-22 (empirical evidence from local execution + the `exp/cli-empirical-discovery` branch's CI runs).
**Verification methodology:** Every command in every table was executed in this session or in the sub-agent's CI runs. Outputs are quoted verbatim where short; ellipsized where long. Auth-free claims are verified by actual execution without API keys, not inferred from docs.

---

## Index — Cross-Platform Coverage Matrix

Which platform exposes a CLI command to introspect each construct type:

| Construct | Claude Code | Codex | Gemini | Cursor | Windsurf | Devin |
|-----------|:-----------:|:-----:|:------:|:------:|:--------:|:-----:|
| skill | `claude plugin list` | — | `gemini skills list [--all]` | — no CLI | — no CLI | `devin skills list` |
| rule | — (file-only) | n/a (uses AGENTS.md) | n/a (uses GEMINI.md) | — no CLI | — no CLI | `devin rules list` |
| command | `claude plugin list` | — | — | — | — | — |
| agent | `claude plugin list` | — | — | — | — | — |
| hook | `claude plugin list` | — | only `gemini hooks migrate` | — | — | — |
| mcp | `claude plugin list` | `codex mcp list` | `gemini mcp list` | — | — | `devin mcp list` |
| extension | n/a | n/a | `gemini extensions list` | — | — | n/a |
| monitor | `claude plugin list` | — | — | — | — | — |
| output style | `claude plugin list` | — | — | — | — | — |
| theme | `claude plugin list` | — | — | — | — | — |
| marketplace add | `claude plugin marketplace add owner/repo` | `codex plugin marketplace add <source>` | — (per-construct install only) | n/a | n/a | n/a |
| validate cmd | `claude plugin validate <path>` | — | `gemini extensions validate <path>` (needs `gemini-extension.json`) | — | — | — |

**Legend:** `command` = CLI command exists, auth-free, verified | `—` = no CLI command at this depth | `n/a` = construct concept doesn't apply to this platform.

---

## Match Mode Convention

CI workflows transcribe each catalog row into one of four assertion shapes. Every row's "after-install output" cell implicitly uses **`grep` substring match** of the bolded or backticked key phrase shown, unless the row explicitly declares another mode. Implementing agents follow this contract; deviations require an explicit Match mode override per row.

| Match mode | Assertion shape | When to use |
|------------|----------------|-------------|
| `exit-code-only` | `<command>; [ $? -eq 0 ]` | Command must complete without error; output content is not checked |
| `grep <substring>` (default) | `<command> \| grep -F '<substring>'` | A specific phrase must appear in the output (most common) |
| `regex <pattern>` | `<command> \| grep -E '<pattern>'` | Output structure matters more than exact text (e.g., version numbers, paths) |
| `exact-diff` | `<command> > tmp; diff <(echo '<expected>') tmp` | Byte-exact match required (rare; useful for stable JSON outputs) |

Default for every command in this catalog: **`exit-code-only` for `--version` / `--help`-type commands; `grep <substring>` for list/inspection commands.** Per-row overrides documented inline where they apply.

---

## Platform 1: Claude Code

**CLI binary:** `claude` (`claude --version` reports current Code release)
**Install:** Bundled with Claude Code application
**Auth model:** Auth-free for `plugin` subcommands; auth-required for chat sessions

### Auth-free inspection commands

| Command | Inspects | Exit code | Output format | Empty-state output | After-install output |
|---------|----------|-----------|---------------|--------------------|--------------------- |
| `claude plugin list` | Installed plugins across scopes | 0 | text table | `No plugins installed. Use \`claude plugin install\` to install a plugin.` | `Installed plugins:\n  ❯ skill-telegram-notify@dgxsparklabs-marketplace\n    Version: 1.0.0\n    Scope: project\n    Status: ✔ enabled` |
| `claude plugin list --json` | Same, machine-readable | 0 | JSON | `{"installed": [], "available": [...]}` | `{"installed": [{"name":"skill-...","marketplaceName":"dgxsparklabs-marketplace",...}], "available": [...]}` |
| `claude plugin list --json --available` | Installed + all available | 0 | JSON | All marketplaces' plugins | Same plus our 71 entries |
| `claude plugin marketplace list` | Configured marketplaces | 0 | text | `claude-plugins-official` only | adds `dgxsparklabs-marketplace` row with `Source: Directory (...)` |
| `claude plugin validate <path>` | Plugin manifest correctness | 0 (or 1 on errors) | text + warnings | n/a | `✔ Validation passed` or `✔ Validation passed with warnings` |
| `claude plugin details <name>` | Plugin component inventory | 0 if installed | text | `Plugin "..." not found.` | Component table + projected token cost |

### Auth-gated commands (excluded from CI)

| Command | Why auth required |
|---------|-------------------|
| `claude` (interactive) | Starts a chat session |
| `claude -p "..."` | Non-interactive prompt to model |

### Marketplace/plugin registration behavior

- `claude plugin marketplace add owner/repo` — accepts GitHub shortform, full HTTPS URL, or local path
- `claude plugin marketplace add "$(pwd)"` — registers local directory; our marketplace registers as `dgxsparklabs-marketplace`
- Our format is **native** for Claude Code (designed for it)

### Per-construct visibility after install

| Construct | Detection method | Expected output |
|-----------|------------------|-----------------|
| skill | `claude plugin install skill-X@dgxsparklabs-marketplace` → `claude plugin list` | shows installed entry |
| skill bundle | `claude plugin install skills-X@dgxsparklabs-marketplace` | output reports `(+ N dependency: ...)` auto-installing members |
| rule | `claude plugin install rule-X@dgxsparklabs-marketplace` → run plugin's `activate.sh` | symlinks/copies into `.claude/rules/` |
| MCP | Plugin manifest's `mcpServers` field; `claude plugin details` shows MCP entries | confirmed via `details` output |

### Workspace/trust/sandbox quirks

- No workspace trust dialog for `plugin` subcommands (read-only/install-only)
- Cache path: `~/.claude/plugins/cache/<marketplace-name>/<plugin>/<version>/`
- `.orphaned_at` marker files indicate plugins pending cleanup

### Cleanup commands

| Command | Effect |
|---------|--------|
| `claude plugin uninstall <name> --scope project` | Removes one plugin |
| `claude plugin prune --scope project -y` | Removes orphaned auto-installed dependencies |
| `claude plugin marketplace remove <name>` | Unregisters marketplace |

---

## Platform 2: Codex (OpenAI)

**CLI binary:** `codex` (`codex-cli 0.130.0` verified 2026-05-22)
**Install:** `npm install -g @openai/codex`
**Auth model:** Auth-free for inspection/management subcommands; OPENAI_API_KEY required for chat/exec/review

> **CI WARNING:** GitHub Actions blocks workflows that reference `@openai/codex` at the org/repo level (verified empirically — 0-second failures across 12+ variants on this org). Codex Tier 2 CI requires a self-hosted runner or local-only verification path.

### Auth-free inspection commands

| Command | Inspects | Exit code | Output format | Empty-state output | After-install output |
|---------|----------|-----------|---------------|--------------------|--------------------- |
| `codex --version` | Binary version | 0 | single string | `codex-cli 0.130.0` | same |
| `codex --help` | All subcommands | 0 | text | 21 commands listed | same |
| `codex mcp list` | MCP servers from `~/.codex/config.toml` | 0 | text | `No MCP servers configured yet. Try \`codex mcp add my-tool -- my-command\`.` | each registered MCP with name/cmd/args |
| `codex mcp get <name>` | One MCP server detail, supports `--json` | 0 if exists; non-0 if not | text or JSON | `error: MCP server '<name>' not found` | full server config |
| `codex features list` | Feature flag table (stage + state) | 0 | text columns | 80+ rows of `feature_name  stage  bool` | same (feature catalog is binary-bundled) |
| `codex login status` | Auth state | 0 | text | `Not logged in.` or `Logged in as <user>` | same |
| `codex plugin marketplace add <source>` | Register marketplace source | 0 | text | n/a | `Added marketplace 'dgxsparklabs-marketplace' from <path>.\nInstalled marketplace root: <path>` |
| `codex plugin marketplace upgrade [name]` | Refresh registered marketplace | 0 | text | (no marketplaces) | re-fetches plugin manifests |
| `codex plugin marketplace remove <name>` | Unregister | 0 | text | (none) | `Removed marketplace '<name>'.` |
| `codex debug models --bundled` | Built-in model catalog | 0 | JSON | (always populated) | model list as JSON |
| `codex debug prompt-input` | Render the model-visible prompt list | 0 | JSON | n/a | structured prompt JSON |

### Auth-gated commands (excluded from CI)

| Command | Why auth required |
|---------|-------------------|
| `codex` (interactive) | Starts model session |
| `codex exec "..."` | Non-interactive prompt |
| `codex review` | Code review against model |
| `codex cloud` | Codex Cloud API |
| `codex login` | OAuth/API key flow |

### Marketplace/plugin registration behavior

- `codex plugin marketplace add` accepts: `owner/repo[@ref]`, HTTPS URLs, SSH URLs, **local marketplace root directories**
- Registers in `~/.codex/config.toml` under `[marketplaces.<name>]`
- **Format compatibility:** Codex registers our marketplace successfully (read our `.claude-plugin/marketplace.json` and stored under `dgxsparklabs-marketplace`)
- **Plugin format mismatch:** Codex looks for `.codex-plugin/plugin.json` inside each plugin directory; our `.claude-plugin/plugin.json` is NOT detected as a Codex plugin
- **Codex plugin manifest is richer** — includes `apps`, `interface` (with `displayName`, `category`, `composerIcon`, `developerName`, `defaultPrompt`), `policy` (with `installation`, `authentication`), `keywords`, `license`
- Codex's own bundled marketplace lives at `~/.codex/.tmp/plugins/.agents/plugins/marketplace.json` with the canonical format

### Per-construct visibility

| Construct | Detection method | Expected behavior |
|-----------|------------------|-------------------|
| skill | `codex` has no skills subcommand; skills concept is via `AGENTS.md` | unsupported as a discrete command |
| rule | Read from `AGENTS.md`, `.cursor/rules/*.md`, `.windsurf/rules/*.md` | inferred from filesystem, no CLI to list |
| mcp | `codex mcp list` | our `example-mcp` config not auto-imported; user would `codex mcp add` manually |
| plugin | `codex plugin marketplace list` doesn't exist (only `add/upgrade/remove`); inspection is via `cat ~/.codex/config.toml` | registered marketplaces appear in TOML |

### Workspace/trust/sandbox quirks

- Codex marks projects as `trust_level = "trusted"` in `~/.codex/config.toml` after first interactive session
- Sandbox modes: `read-only`, `workspace-write`, `danger-full-access` (`-s` flag)
- `--dangerously-bypass-approvals-and-sandbox` exists for CI use

### Cleanup commands

| Command | Effect |
|---------|--------|
| `codex plugin marketplace remove <name>` | Unregister marketplace |
| `rm -rf ~/.codex/.tmp/plugins/` | Clear extracted plugin cache (manual) |
| `npm uninstall -g @openai/codex` | Remove CLI binary |

---

## Platform 3: Gemini (Google)

**CLI binary:** `gemini` (`gemini 0.42.0` verified 2026-05-22)
**Install:** `npm install -g @google/gemini-cli`
**Auth model:** Mixed — most management subcommands auth-free; top-level flags like `--list-extensions` (different from `gemini extensions list`!) require auth; all chat/inference requires `GEMINI_API_KEY` / `GOOGLE_GENAI_USE_VERTEXAI` / `GOOGLE_GENAI_USE_GCA`

> **CI WARNING:** Same GitHub Actions org-level block as Codex applies to `@google/gemini-cli`. CI Tier 2 needs self-hosted runner or local-only path.

### Auth-free inspection commands

| Command | Inspects | Exit code | Output format | Empty-state output | After-install output |
|---------|----------|-----------|---------------|--------------------|--------------------- |
| `gemini --version` | Binary version | 0 | single string | `0.42.0` | same |
| `gemini --help` | Subcommand surface | 0 | text | 5 main subcommands + many flags | same |
| `gemini skills list` | Discovered skills (project + user + built-in) | 0 | text | `No skills discovered.` | enumerated skills with location + status |
| `gemini skills list --all` | Same + built-in/disabled | 0 | text | At minimum `skill-creator [Enabled] [Built-in]` | additional discovered skills |
| `gemini extensions list` | Installed extensions | 0 | text | `No extensions installed.` | extension entries with name + version |
| `gemini mcp list` | Configured MCP servers | 0 | text | `No MCP servers configured.` | each server with command + status |
| `gemini skills enable <name>` / `disable <name>` | Toggle skill | 0 | text | (skill not found error) | updates `~/.gemini/settings.json` |
| `gemini extensions enable <name>` / `disable <name>` | Toggle extension | 0 | text | (not found) | updates settings |
| `gemini extensions validate <path>` | Validate extension manifest | 0 if valid, 1 if invalid | text + errors | n/a | `Configuration file not found at <path>/gemini-extension.json` (if missing) or validation report |

### Auth-gated commands (excluded from CI)

| Command | Why auth required |
|---------|-------------------|
| `gemini` (interactive) | Starts model session |
| `gemini -p "..."` | Non-interactive prompt |
| `gemini --list-extensions` (top-level flag) | Returns `EXIT 41 — Auth method required` (different from `gemini extensions list` subcommand!) |
| `gemini extensions install <git-url>` | Network + repo fetch |

**Important asymmetry:** `gemini --list-extensions` (flag) requires auth, but `gemini extensions list` (subcommand) does NOT. Always prefer the subcommand form in CI.

### Marketplace/plugin registration behavior

- **No marketplace concept** — Gemini installs skills/extensions individually via `gemini skills install <source>` or `gemini extensions install <source>`
- `gemini skills install <local-path>` — verified to detect our marketplace's SKILL.md format: `Searching for skills in ...\Installing agent skill(s) from ...\* telegram-notify: <description>\(Source: ...\SKILL.md) (3 items in directory)`
- Install destination: `C:\Users\<user>\.gemini\skills\<skill-name>\`
- **Format compatibility:** Our SKILL.md format is **directly detected** by Gemini's skill installer (verified — the install confirmation prompt appeared with our skill metadata)
- `gemini extensions validate <path>` requires `gemini-extension.json` — that's Gemini's extension manifest format (which we don't ship)
- `gemini skills link <path>` — symlink mode for local-dev iteration (updates reflect immediately)

### Per-construct visibility

| Construct | Detection method | Expected behavior |
|-----------|------------------|-------------------|
| skill | `gemini skills install <local-skill-dir>` then `gemini skills list` | our skill should appear; format is compatible |
| rule | Read from `GEMINI.md` and `AGENTS.md`; no `gemini rules list` exists | inferred from filesystem |
| mcp | `gemini mcp add` then `gemini mcp list` | manageable via CLI |
| extension | `gemini extensions install <local-extension-dir>` requires `gemini-extension.json` | NOT compatible with our format unless we add the manifest |
| hook | `gemini hooks migrate` (Claude Code → Gemini converter) | Gemini understands Claude Code hook format and can convert |

### Workspace/trust/sandbox quirks

- `gemini skills list` reports: `Skipping project agents due to untrusted folder. To enable, ensure that the project root is trusted.` — workspace trust must be configured for project-level skill discovery
- Approval modes: `default`, `auto_edit`, `yolo`, `plan` (`--approval-mode` flag)
- `--skip-trust` flag bypasses workspace trust for the session

### Cleanup commands

| Command | Effect |
|---------|--------|
| `gemini skills uninstall <name> [--scope]` | Remove a skill |
| `gemini extensions uninstall <name>` | Remove an extension |
| `gemini mcp remove <name>` | Unregister an MCP server |
| `npm uninstall -g @google/gemini-cli` | Remove CLI binary |

---

## Platform 4: Cursor

**CLI binary:** None (verified — installer URL serves IDE/GUI only)
**Install:** N/A (no headless CLI exists)
**Auth model:** N/A

> **Verification methodology:** Tested empirically by the `exp/cli-empirical-discovery` sub-agent. The `https://cursor.com/install` URL returns a bash script titled "Cursor Agent Installer," but execution installs the Electron GUI application. No `cursor` or `agent` binary lands in PATH on headless Linux. No npm packages exist (`@cursor-ai/cli`, `@cursor/cli`, `cursor-cli` — all empty). Confirmed by 12+ install attempt variants in CI logs.

### Auth-free inspection commands

| Command | Inspects | Status |
|---------|----------|--------|
| (none documented or installable) | — | — no CLI exists |

### Auth-gated commands

| Command | Status |
|---------|--------|
| (none — Cursor is IDE-only) | — |

### Marketplace/plugin registration behavior

- **No marketplace concept** — Cursor reads `.cursor/rules/*.mdc` files at IDE open
- Format: `.mdc` files with YAML frontmatter (`description`, `globs`, `alwaysApply`)
- **Our format compatibility:** Generator writes `.cursor/rules/<name>.md` — Cursor docs say `.mdc` is canonical; `.md` is also accepted but loses UI/validator support
- **Third-party validator (verified 2026-05-22):** `cursor-doctor@1.11.0` (npm, by `nedcodes`, MIT-licensed, zero deps). Usage: `npx --yes cursor-doctor@1.11.0 scan .cursor/rules/`. The `scan` operation is free; `fix` operation has a 3-uses-per-session free tier (Pro for unlimited). For CI validation we only need `scan`, which is fully auth-free. Available subcommands: `scan` (default), `fix`, `fix --preview`, `lint`, `badge`.

### Per-construct visibility

| Construct | Detection method | Expected behavior |
|-----------|------------------|-------------------|
| rule | File presence in `.cursor/rules/`; validate via `npx cursor-doctor` | format-only validation |
| skill | (no Cursor skills concept) | n/a |

### Workspace/trust/sandbox quirks

- N/A (no CLI to configure)

### Cleanup commands

| Command | Effect |
|---------|--------|
| (none — no installation occurs) | — |

---

## Platform 5: Windsurf

**CLI binary:** None (verified — zero CLI presence across all package ecosystems)
**Install:** N/A
**Auth model:** N/A

> **Verification methodology:** Sub-agent CI runs verified: no npm package (the existing `windsurf@0.0.1` is an unrelated name-squatter — a terminal-cursor utility by an unaffiliated author), no pip package, no snap, no apt, no GitHub releases under `codeium-ai/windsurf` or similar. Windsurf is IDE-only. The `windsurf` shell command (if present) just opens files in the IDE.
>
> **Note:** Cognition acquired Windsurf in July 2025; "Devin Local Agent" now ships bundled in Windsurf Enterprise. The `devin` CLI authenticates via Windsurf accounts.

### Auth-free inspection commands

| Command | Inspects | Status |
|---------|----------|--------|
| (none exists) | — | — no CLI |

### Auth-gated commands

| Command | Status |
|---------|--------|
| (none) | — |

### Marketplace/plugin registration behavior

- **No marketplace concept** — Windsurf reads `.windsurf/rules/*.md` at IDE open
- Format: `.md` files with required `trigger:` frontmatter field (`always_on`, `model_decision`, `glob`, `manual`)
- Body limit: 12,000 characters per file
- **Our format compatibility:** Generator writes `.windsurf/rules/<name>.md` with `trigger: always_on` per docs — format-correct, no CLI to verify

### Per-construct visibility

| Construct | Detection method | Expected behavior |
|-----------|------------------|-------------------|
| rule | File presence in `.windsurf/rules/`; format validation via stdlib YAML parser | format-only validation |
| skill | (no Windsurf skills concept) | n/a |

### Workspace/trust/sandbox quirks

- N/A (no CLI to configure)

### Cleanup commands

| Command | Effect |
|---------|--------|
| (none) | — |

---

## Platform 6: Devin (Cognition)

**CLI binary:** `devin` (`devin 2026.5.6-10 (87ae95e)` verified 2026-05-22 in `exp/cli-empirical-discovery` CI run 26260259130)
**Install:** `curl -fsSL https://cli.devin.ai/install.sh | bash`
**Auth model:** Auth-free for `skills list`, `rules list`, `mcp list`, `skills paths`, `rules paths`, `auth status`, `--version`, `--help`; Windsurf account login required for sessions/cloud/auth login

> **Installer quirk:** The install script tries an interactive setup wizard that fails in non-TTY environments — `curl ... | bash` exits 1 in CI, but the binary is correctly installed at `~/.local/bin/devin`. Wrap with `|| true` in CI.

### Auth-free inspection commands

| Command | Inspects | Exit code | Output format | Empty-state output | After-install output |
|---------|----------|-----------|---------------|--------------------|--------------------- |
| `devin --version` | Binary version | 0 | text | `devin 2026.5.6-10 (87ae95e)` | same |
| `devin auth status` | Auth state | 0 | text | `Not logged in.\nCredentials: <path>` | same (auth-free even when unauthenticated) |
| `devin skills list` | Available skills (project + user) | 0 | text | (none if no skills found) | enumerated skills with slash-command name, file path, description |
| `devin skills paths` | Where skills are loaded from | 0 | text | list of scan paths | `.devin/skills/`, `~/.config/devin/skills/`, project-relative paths |
| `devin skills show <name>` | One skill's content | 0 | text | (not found error) | formatted SKILL.md content |
| `devin rules list` | Available rules with provider tags | 0 | text | (none) | rules tagged `Cursor`, `Windsurf`, `Standard` |
| `devin rules paths` | Where rules are loaded from | 0 | text | list | `.windsurf/rules/*.md`, `.cursor/rules/*.md`, `.cursorrules`, `AGENTS.md` |
| `devin rules show <name>` | One rule's content | 0 | text | (not found) | formatted rule content |
| `devin mcp list` | Configured MCP servers | 0 | text | `No MCP servers configured` | each registered MCP |
| `devin mcp get <name>` | One MCP server detail | 0 if exists | text | (not found) | full config |

### Auth-gated commands (excluded from CI)

| Command | Why auth required |
|---------|-------------------|
| `devin` (interactive) | Starts Devin session |
| `devin auth login` | Windsurf OAuth flow |
| `devin cloud drs *` | Cloud DRS API |

### Marketplace/plugin registration behavior

- **No marketplace concept** in Devin — there's no `devin plugin marketplace add`
- Devin discovers content from filesystem at session start:
  - Skills: `.devin/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md`
  - Rules: `AGENTS.md` (primary), `.cursor/rules/*.md` (compat), `.windsurf/rules/*.md` (compat)
- **Our format compatibility:** Excellent — Devin **natively reads our cross-platform mirror directories** (`.cursor/rules/`, `.windsurf/rules/`) without configuration. Our `.devin/skills/` mirror works directly. This is the strongest cross-platform validation surface we have.

### Per-construct visibility

| Construct | Detection method | Expected output |
|-----------|------------------|-----------------|
| skill | `devin skills list` from project root with `.devin/skills/` present | each skill listed with slash-command name + description |
| rule | `devin rules list` from project root with `.cursor/rules/` or `.windsurf/rules/` present | rules tagged by provider; our 21 rules visible after generator runs |
| mcp | `devin mcp list` after `devin mcp add` (user or project scope) | each registered MCP |

### Workspace/trust/sandbox quirks

- Devin reads from indexed cloud repos AND local clones simultaneously
- `~/.config/devin/config.json` enables/disables Cursor/Windsurf rule format reading
- `devin auth login` says **"Log in to Windsurf"** — Devin is internally a Codeium/Windsurf product

### Cleanup commands

| Command | Effect |
|---------|--------|
| (Devin doesn't install our content — it reads filesystem live) | nothing to uninstall |
| `rm ~/.local/bin/devin` | Remove CLI binary |

---

## Summary — Validation Strength Per Platform

| Platform | CLI-driven Tier 2 possible? | Strongest available proof | CI viability |
|----------|----------------------------|---------------------------|--------------|
| Claude Code | ✅ Full | `claude plugin install` + `list` + `validate` per-plugin | ✅ In CI today |
| Devin | ✅ Full (skills + rules + mcp) | `devin skills list` + `devin rules list` after our generator runs | ⚠️ CI install works (with `|| true`) — verified by sub-agent |
| Codex | ⚠️ Partial (mcp + marketplace registration) | `codex plugin marketplace add <local>` + `codex mcp list` | ❌ Blocked by GitHub Actions org policy; local-only |
| Gemini | ⚠️ Partial (skill install detects our format; mcp + extensions list) | `gemini skills install <local-skill-dir>` (dry-run via Y/n cancel) + `gemini mcp list` + `gemini extensions list` | ❌ Blocked by GitHub Actions org policy; local-only |
| Cursor | ❌ None — no CLI exists | `npx cursor-doctor scan` (third-party, format-only) | ✅ Free in CI |
| Windsurf | ❌ None — no CLI exists | Custom YAML frontmatter parser (stdlib) | ✅ Free in CI |

---

## Notes for the CI/CD Design Phase

This catalog drives the next document (`docs/PLATFORM_VALIDATION_CICD_PLAN.md`, to be written). Each row in the auth-free inspection tables above becomes a CI assertion of the shape:

```
1. Install platform CLI (or skip job entirely if blocked/not available)
2. Register/install our marketplace artifact for this platform
3. Run <command from catalog>
4. Assert exit code matches catalog's expected
5. Assert output matches catalog's "after-install output" column
6. Cleanup
```

CI workflows that map directly to catalog rows produce minimum-friction maintenance: when a platform deprecates a command, the catalog row is removed, the CI assertion is removed, and they stay in sync.

Platforms with no auth-free CLI (Cursor, Windsurf) fall back to format-only validators (frontmatter parsing, file-presence checks). The catalog records this explicitly as "no CLI exists" rather than leaving it ambiguous.
