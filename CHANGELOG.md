# Changelog

## 2026-05-25 — Platform emission bug fixes from QA round

Hands-on QA verification of the platform-feature-routing refactor (merged at `a86cb86`) surfaced several format mismatches where our emitted manifests passed drift checks (byte-identical to committed output) but did not match the platforms' actual loader contracts. This PR fixes the diagnosed bugs and adds a new schema-fitness test category to catch this class of bug at CI time going forward.

### Fixed

- **Cursor skill plugin popup** — `CursorPlatform.build_plugin_json` now emits `description`, `version`, and a `skills` pointer for `SkillConstruct` plugins. Previously emitted only `{"name": ...}`, causing Cursor's display layer to render mangled metadata (version, git SHA, duplicated description) in the slash-command popup (commit `e7f0b65`, per `cursor.com/docs/reference/plugins`, 2026-05-25).
- **Gemini sub-agent `tools` field** — now emitted as a YAML array per `geminicli.com/docs/core/subagents/` (2026-05-25); previously a comma-separated string. The shape mismatch caused Gemini's `/agents` discovery to silently skip our sub-agents (commit `e53afed`).
- **Windsurf hook event names** — now translated from Claude PascalCase (`UserPromptSubmit`, …) to Windsurf snake_case (`pre_user_prompt`, …) per `docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25), and the doubly-nested `hooks.<event>[].hooks[]` source shape is flattened to Windsurf's flat per-entry shape. Conservative mapping — ambiguous Claude events (e.g. `PreToolUse`, which Windsurf splits into four sub-events) are dropped rather than guessed (commit `4e63a4e`).
- **Cursor hook emission** — new `HookConstruct` branch in `CursorPlatform.emit` produces `.cursor/hooks.json` in Cursor's flat schema (`version: 1`, camelCase event names, flattened per-entry structure) per `cursor.com/docs/agent/hooks` (2026-05-25). Previously the per-plugin `.cursor-plugin/plugin.json` "hooks" pointer resolved to an un-converted Claude-shape file and Cursor silently ignored it (closest analog for `UserPromptSubmit` is `beforeSubmitPrompt`, verified against three working community plugins).
- **Gemini hook event names** — now translated to Gemini's documented PascalCase vocabulary (`UserPromptSubmit` → `BeforeModel`, etc.) per `geminicli.com/docs/hooks/reference/` (2026-05-25). The nested file shape is structurally identical to Claude's (verified against the working `sandipchitale/hooklog` extension), so only the vocabulary is rewritten.
- **CRLF/LF drift on Windows** — generator's `write_text` calls now pass `newline=""` so regenerated files match committed LF bytes (commit chain landing alongside the refactor). Fixes two previously-flaky tests (`test_check_succeeds`, `test_agents_plugins_marketplace_byte_identical`) on Windows.

### Added

- `scripts/converters/event_name_mapping.py` — shared table of Claude → {Cursor, Gemini, Windsurf} hook event-name translations. Per-platform tables (`CLAUDE_TO_CURSOR_EVENTS`, `CLAUDE_TO_GEMINI_EVENTS`, `CLAUDE_TO_WINDSURF_EVENTS`) plus `map_event(event, platform)` lookup. Each converter imports from here so the mapping for any given Claude event lives in exactly one place.
- `scripts/converters/hooks_to_cursor.py` — Claude-shape → Cursor flat-schema converter (adds `version: 1`, renames events, flattens entries).
- `scripts/converters/hooks_to_gemini.py` — Claude → Gemini hook event-name rewrite (same nested structure; only vocabulary differs).
- `tests/test_schema_fitness.py` — validates emitted per-platform manifests against reference JSON Schemas captured directly from the platforms' docs. Coverage: Cursor `SkillConstruct` plugin.json, Gemini `AgentConstruct` frontmatter, Windsurf hooks event names + shape, Cursor hooks shape + `version` presence, Gemini hooks event-name vocabulary. Uses an inline ~30-line JSON Schema subset validator to avoid adding a runtime `jsonschema` dependency. Initial: 9 tests; this PR brings it to 15.
- `docs/TEST_YOURSELF.md` — 53 per-construct × per-platform hands-on operator-QA cells (up from ~5 in the prior revision). Comprehensive verification doc covering all 6 platforms + the `agents` CLI; flags 8 specific UNKNOWN-method gaps for the next research round.
- `docs/research/qa-bug-fixes-2026-05/` — research artifacts that diagnosed the bugs fixed in this PR: `RESEARCH.md` (32 KB, two-round investigation + empirical verification), `logs/` (community-plugin manifests + hermetic install probe outputs for Codex and Gemini).

### Known limitations (NOT fixed in this PR)

- **Codex sub-agent install** — `.codex/agents/<name>.toml` emission is kept (forward-looking) but does not currently install. Per `developers.openai.com/codex/plugins/build` (2026-05-25), Codex's plugin.json schema has only `skills`, `mcpServers`, `apps`, `hooks` — no `agents` field exists. Empirical probe (`docs/research/qa-bug-fixes-2026-05/logs/codex-probe-output.log`) confirms `codex plugin add` installs the plugin's source `agent.md` but does NOT copy our generated `.codex/agents/notebook-reviewer.toml` into any path Codex discovers at runtime (`~/.codex/agents/` is never created). The install pathway for plugin-shipped sub-agents appears to not yet be implemented upstream. Our TOML emission remains in place for the day Codex adds support; until then, Codex users can install sub-agents by manually copying the TOML to `~/.codex/agents/notebook-reviewer.toml`.
- 8 specific UNKNOWN-method gaps are flagged in `docs/TEST_YOURSELF.md` for the next research round (Codex hook listing, Gemini hook listing, Cursor command/hook/MCP enumeration, Cursor CLI dispatch, Windsurf hook triggers, `agents` CLI default spray policy, LSP/Monitor/OutputStyle/Theme observability).

### Tests

- `tests/test_marketplace.py` — 78 tests (unchanged in this arc).
- `tests/test_schema_fitness.py` — 15 tests (up from 9 in the prior commit `c10cb45`).
- Total: 93 (up from 87 in the baseline immediately before this PR; 67 in `main`).

---

## 2026-05-25 — Platform feature routing refactor

Surveyed every platform's native capabilities (Cursor 2.4 sub-agents, Codex sub-agents TOML, Gemini hooks/agents, Windsurf hooks) and discovered the generator was under-emitting against documented APIs. This refactor (a) retires two dead skill mirrors, (b) expands per-platform `supports` sets to cover sub-agents on Cursor + Gemini + Codex and hooks on Cursor + Gemini + Windsurf and commands/MCP on Cursor, (c) adds a forward-looking `.agents/rules/` mirror and `.agents/plugins/marketplace.json` (Codex canonical path), and (d) introduces an `agents` CLI shim for Class B platforms.

### Retired (breaking — no migration helper per D-7)

- `.codex/skills/` mirror tree (27 directories) — Codex installs plugins via `_generated/<plugin>/.codex-plugin/plugin.json`, not the repo-root skill mirror (verified hermetic act run Q-A1 PASS).
- `.devin/skills/` mirror tree (27 directories) — Devin enumerates `.agents/skills/` natively (verified hermetic act run Q-B1: 27 skills enumerated post-retirement).
- Migration: nothing required for users — content remains available at `.agents/skills/` and via per-plugin manifests.

### Added — per-platform emission

- **Cursor sub-agents** at `.cursor/agents/<name>.md` (`CursorPlatform.supports += {AgentConstruct}`); per-plugin `.cursor-plugin/plugin.json` now includes `agents`, `commands`, `hooks`, `mcpServers` fields for agent/command/hook/MCP plugins (per `cursor.com/docs/reference/plugins`, 2026-05-25).
- **Gemini sub-agents** at `.gemini/agents/<name>.md` (`GeminiPlatform.supports += {AgentConstruct}`) and **Gemini hooks** at `.gemini/hooks/hooks.json` (`+= {HookConstruct}`) per `geminicli.com/docs/extensions/reference/` (2026-05-25).
- **Codex sub-agents** at `.codex/agents/<name>.toml` (`CodexPlatform.supports += {AgentConstruct}`) per `developers.openai.com/codex/subagents/` (2026-05-25). Source format stays Claude-style markdown with YAML frontmatter (D-16); conversion happens at emit time via `scripts/converters/md_to_toml.py`.
- **Windsurf hooks** at `.windsurf/hooks.json` (`WindsurfPlatform.supports += {HookConstruct}`) per `docs.windsurf.com/windsurf/cascade/hooks` (2026-05-25).
- **`.agents/rules/<name>.md`** forward-looking convergence (`AgentsPlatform.supports += {RuleConstruct}`) — no platform reads it today (verified Q-R1/Q-R2) but Cursor 2.7+ and Windsurf 2.0 are credible adopters.

### Added — generator infrastructure

- **Phase 5.5**: emit `.agents/plugins/marketplace.json` (byte-identical copy of `.claude-plugin/marketplace.json`) — Codex's canonical marketplace path per `developers.openai.com/codex/plugins/build` (2026-05-25). Both paths remain valid; we now serve both.
- **`scripts/converters/md_to_toml.py`** — Claude-md → Codex-TOML translator for sub-agent emission.

### Added — `agents` CLI shim (`scripts/agents_cli/`)

- New CLI providing Claude-equivalent install UX for Class B platforms (Windsurf, Devin, Cursor CLI). Subcommands: `install`, `uninstall`, `list`, `list --available`, `upgrade`, `upgrade --all`, `info`, `marketplace add|list|remove`, `--version`, `--help`.
- `--scope project|user` semantics: project = `./.agents/<construct>/` + per-platform paths; user = `~/.agents/<construct>/` only (per D-6).
- `--agents-only` strict mode skips per-platform spray (D-13 Option C).
- Content source: `git clone` (per D-4).
- Install location: `~/.local/bin/agents` (POSIX) / `$env:LOCALAPPDATA\agents\bin\agents.ps1` (Windows) (per D-17).
- One-liner installers at repo root: `install.sh` (POSIX) and `install.ps1` (Windows).

### Documentation

- `docs/PLATFORMS.md`, `docs/ARCHITECTURE.md`, `docs/RULE_FORMAT.md` aligned with new per-platform support matrix.
- `docs/RULE_FORMAT.md:117` removed stale `.devin/rules/` claim (the generator never emitted that path).
- `rules/*/README.md` (21 files) — dropped `.devin/rules/` references.
- `README.md` — added `agents` CLI install section and a row to the GitHub-direct-install table.

### Tests

- `tests/test_marketplace.py` — 67 tests passing (unchanged in this refactor's Units 7-9; Units 0-6 already extended it).
- `tests/test_agents_cli.py` (new, 25 tests) — CLI argparse, dispatch, path resolution, install/uninstall round-trip, --agents-only verification.

### CI

- Extended `compat-agent.yml`, `compat-hook.yml`, `compat-command.yml`, `compat-mcp.yml` with `cursor-emission` / `gemini-emission` / `codex-emission` / `windsurf-emission` filesystem assertion jobs.
- New `compat-agents-cli.yml` — install.sh → `agents install skill-example --scope project` round-trip on ubuntu-latest, plus advisory windows-latest install.ps1 smoke.

---

## 2026-05-24 — Phase 5 cross-platform native install compliance (merged: bfb476d)

Verification round exposed that the README documented install commands that didn't fully work on Codex / Gemini / Windsurf / Cursor. Fixed by emitting per-platform per-plugin manifests and root-level entry-point manifests so each platform's native installer succeeds.

### Added

- `AgentsPlatform` (7th `Platform` class in `scripts/platforms.py`) — emits `.agents/skills/<name>/` as a cross-platform skill mirror that Windsurf Cascade, Cursor, and Devin all discover natively.
- Per-plugin native manifests, gated on `platform.supports`:
  - `_generated/<plugin>/.codex-plugin/plugin.json` per Codex-supported plugin
  - `_generated/<plugin>/.cursor-plugin/plugin.json` per Cursor-supported plugin
- Root-level entry-point manifests:
  - `gemini-extension.json` at repo root for `gemini extensions install <github-url> --consent`
  - `.cursor-plugin/marketplace.json` at repo root (49 plugin entries) for Cursor team-marketplace import
- New generator phases: Phase 1.5 (per-plugin per-platform manifests), Phase 4.5 (root Gemini extension), Phase 6 (root Cursor marketplace).
- Extended `Platform` protocol with `build_plugin_json(construct, name) -> dict`.
- CI assertions in `compat-marketplace-add.yml` (Codex enumeration + install; Claude install + list) and a new `gemini-github-url-install` job in `compat-extension.yml`. End-to-end registration → enumeration → install → use verified for Claude/Codex/Gemini.
- 18 new tests in `tests/test_marketplace.py` (52 total now, up from 34).
- Full audit trail in `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/` (SUMMARY, empirical_act_verification, cursor research, implementation report, validation, README rewrite preview + report, act workflows, container logs, `reproduce.ps1`).

### Changed

- Plan: `docs/archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md` (v2) — 4 locked decisions (A1 per-plugin manifests, B2 supports-gated emission, C1 root-level entry-point manifests, Q2 `.agents/skills/` convergence dir).
- README rewritten with per-platform install + GitHub-direct-install support matrix (every command appears as VERIFIED-PASS in `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md`).
- Mirror dir hygiene: `shutil.copytree` ignore patterns exclude cross-platform manifest dirs.

---

## 2026-05-24 — Phase 4 dependency-injection refactor of the generator

Restructured `scripts/generate_manifest.py` from a procedural per-construct script (~600 lines of special cases) into a strategy-pattern architecture. No user-visible install behavior change; the refactor unlocked Phase 5's per-platform manifest emission.

### Added

- `scripts/constructs.py` — 10 typed `Construct` classes (Skill, Rule, Command, Agent, Hook, MCPServer, LSPServer, Monitor, OutputStyle, Theme). Each implements the `Construct` protocol (`prefix`, `source_directory`, `category`, `build_plugin_json`, `emit`). Registered in a `CONSTRUCTS` dict — adding an 11th construct = one new class + one registry entry.
- `scripts/platforms.py` — initially 6 typed `Platform` classes (Claude, Codex, Gemini, Cursor, Windsurf, Devin); Phase 5 added a 7th (`AgentsPlatform`). Each declares a `supports` set and implements `emit`.
- `scripts/bundles.py` — `Bundle` dataclass + loader for `catalog.toml`.
- `scripts/utils.py` — shared helpers (kebab-case validation, plugin-name derivation, etc.).
- `scripts/generate_manifest.py` — reduced to a thin 5-phase orchestrator (was a monolith).

### Changed

- Construct example directories: `examples/example-<type>/` → `<construct>/example/` (Phase 3 restructure, finalized by DI refactor decision #18). Examples now live next to their source siblings instead of in a separate `examples/` tree.
- `catalog.toml` is now bundles-only (no construct-type config, no platform config). Construct definitions live in code via `CONSTRUCTS`; platform definitions live in `PLATFORMS`.
- Plugin naming convention formalized: `<prefix>-<instance-name>` for individual plugins, `bundle-<bundle-name>` for catalog bundles, `bundle-<prefix>-all` for code-generated catch-alls (reserved names — can't be declared in `catalog.toml`).
- Test suite rewritten/extended for the DI architecture; baseline 34 tests for this phase.

### Documentation

- 25 locked decisions captured in `docs/archive/di-refactor/PLAN_DI_REFACTOR.md` (v3) with v1/v2 reviewer critiques alongside.
- Implementation evidence in `docs/archive/di-refactor/DI_REFACTOR_REPORT.md`; validation in `docs/archive/di-refactor/DI_REFACTOR_VALIDATION_REPORT.md`.
- 11 separate `docs/ADDING_*.md` per-construct tutorials consolidated into one `docs/ADDING_A_CONSTRUCT.md` (decision #10).

---

## 2026-05-22 — v1.0.0 Claude Code plugin compliance

Major migration. The marketplace is now natively installable via Claude Code's `/plugin marketplace add DgxSparkLabs/marketplace`.

### Added

- `.claude-plugin/marketplace.json` — root manifest with 71 plugin entries: 26 individual skills, 8 skill-domain bundles, 21 individual rules, 5 rule-domain bundles, 1 rules-all catch-all, 10 example reference plugins.
- `MARKETPLACE.toml` — single source of truth for owner / version / license / repo URL. All generated manifests inherit from this; renames or version bumps are one-line edits.
- `catalog.toml` restructured around `[construct.*]` definitions and `[skill_domain.*]` / `[rule_domain.*]` tagging.
- `scripts/generate_manifest.py` — the engine. Produces `_generated/skill-<name>/`, `_generated/rule-<name>/`, dependency-only bundle plugins, and cross-platform mirrors. Supports `--check` mode for CI drift detection.
- 10 example reference plugins in `examples/` (one per Claude Code construct type). Each is both a working installable plugin and a tutorial reference.
- 12 contributor tutorials in `docs/`: `CONSTRUCT_TYPES.md` plus eleven `ADDING_*.md` files.
- Planning dossier: `docs/archive/phase-1-compliance/GOAL_PLUGIN_COMPLIANCE.md`, `docs/archive/phase-1-compliance/PLAN_PLUGIN_COMPLIANCE.md`, `docs/archive/phase-1-compliance/INVESTIGATION_PLUGIN_DEPENDENCIES.md`, `docs/archive/phase-1-compliance/IMPLEMENTING_AGENT_PROMPT.md`.
- Cross-platform mirrors (auto-generated, committed): `.codex/skills/`, `.gemini/skills/`, `.cursor/rules/`, `.windsurf/rules/`, `.devin/skills/`, `.devin/rules/`.
- `activate-installed-rules.sh` at repo root — bulk-symlinks every installed rule plugin into `.claude/rules/`.
- CI step that validates manifest sync via `generate_manifest.py --check`.

### Removed

- `install.py` (85 KB Textual TUI) — replaced by native `/plugin marketplace add`.
- `scripts/install.sh` (curl bootstrap) — replaced by native `/plugin marketplace add`.
- `scripts/install-rule.sh` — replaced by per-plugin `activate.sh` generated by the engine.
- `rules/<name>/install.sh` × 21 — replaced by per-plugin `activate.sh`.
- `pyproject.toml` and `uv.lock` — no project-level Python dependencies remain (the generator uses PEP 723 inline metadata).
- `_template/` — replaced by `examples/example-<type>/` directories as the contributor starting templates.

### Changed

- GitHub organization: `ForkYoraiLevi/marketplace` → `DgxSparkLabs/marketplace`. All install URLs updated.
- Test suite rewritten (1854 lines → ~360 lines) for the post-migration architecture. Now validates: TOML config integrity, catalog tagging cross-checks, example completeness, generator drift, manifest schema, activate.sh shape, mirror coverage, kebab-case naming, secret scan.

### Migration notes

- **`curl ... | bash` users**: the old install URL now returns 404. Switch to `/plugin marketplace add DgxSparkLabs/marketplace` in a Claude Code session.
- **Devin / Cursor / Windsurf users**: `git clone` the repo and point your tool at the matching mirror directory.
- **Rule users**: rules now ship as plugins. After install, run the plugin's `activate.sh` (or the repo-root bulk helper) to symlink into `.claude/rules/`. See `docs/archive/phase-1-compliance/INVESTIGATION_PLUGIN_DEPENDENCIES.md`.

### Verified empirically

The dependency-only bundle architecture requires Claude Code to auto-install plugin dependencies. Verified — `claude plugin install` reports `"(+ N dependency: <name>)"`. Full experiment and decision matrix in `docs/archive/phase-1-compliance/INVESTIGATION_PLUGIN_DEPENDENCIES.md`.

---

## 2026-03-22

### Enable Devin CLI global rules support

Devin CLI now loads `~/.config/devin/AGENTS.md` as global rules. Updated `catalog.toml` to set `global_rules = "~/.config/devin/AGENTS.md"` for the Devin platform. This removes the workspace-only forcing for Devin rules — users can now install rules globally or per-workspace, matching the behavior of Claude Code, Cursor, and Windsurf.

## 2026-03-19

### Banner K glyph fix (f5043c8)

Corrected the K letter in SKILLS and MARKET banner text. The previous fix (`404b181`) changed K from looking like R (`╦═╗`) to `╦ ╦`, but that read as H (two parallel verticals). Now uses `╦╔═` — the canonical form from the `calvin_s` pyfiglet font — which properly shows the upper diagonal arm of the K.

### Installer bug fixes (404b181)

Fixed four user-reported issues: K glyph in banner looked like R (changed to open-top form), path completion dropdown was hard-capped at 20 results (removed cap, increased visible height), installed marker only checked primary platform (now checks all detected platforms), and confirm dialog showed all global rules as workspace-only when any platform forced workspace (now shows in global section with a note about which platforms redirect to workspace).

### Installer bug fixes (d6f254a)

Fixed crash on missing catalog.toml (IndexError on empty PLATFORMS), duplicate items in confirm dialog summary, install_rule race condition (exists check after open), and added 5 uncategorized skills/rules to catalog.toml families.

### Installer upgrade (9edc9de)

Major installer rewrite: externalized configuration to catalog.toml, added per-item scope toggle (S key), workspace paths section with autocomplete and directory picker, MarketplaceList with click-to-focus behavior, platform-aware scope forcing (Devin rules auto-redirect to workspace), scope validation, and empty-state notices.
