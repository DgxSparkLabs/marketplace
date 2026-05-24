# Changelog

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
- Full audit trail in `docs/VERIFICATION_2026-05/` (SUMMARY, empirical_act_verification, cursor research, implementation report, validation, README rewrite preview + report, act workflows, container logs, `reproduce.ps1`).

### Changed

- Plan: `docs/PLAN_CROSS_PLATFORM_INSTALL_FIX.md` (v2) — 4 locked decisions (A1 per-plugin manifests, B2 supports-gated emission, C1 root-level entry-point manifests, Q2 `.agents/skills/` convergence dir).
- README rewritten with per-platform install + GitHub-direct-install support matrix (every command appears as VERIFIED-PASS in `docs/VERIFICATION_2026-05/empirical_act_verification.md`).
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

- 25 locked decisions captured in `docs/PLAN_DI_REFACTOR.md` (v3) with v1/v2 reviewer critiques alongside.
- Implementation evidence in `docs/DI_REFACTOR_REPORT.md`; validation in `docs/DI_REFACTOR_VALIDATION_REPORT.md`.
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
- Planning dossier: `docs/GOAL_PLUGIN_COMPLIANCE.md`, `docs/PLAN_PLUGIN_COMPLIANCE.md`, `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`, `docs/IMPLEMENTING_AGENT_PROMPT.md`.
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
- **Rule users**: rules now ship as plugins. After install, run the plugin's `activate.sh` (or the repo-root bulk helper) to symlink into `.claude/rules/`. See `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`.

### Verified empirically

The dependency-only bundle architecture requires Claude Code to auto-install plugin dependencies. Verified — `claude plugin install` reports `"(+ N dependency: <name>)"`. Full experiment and decision matrix in `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`.

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
