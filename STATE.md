# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions), `PITFALLS.md` (specific bug→fix entries), and `docs/LESSONS.md` (working-practice lessons for the next agent — read before any generator/CI/layout change).

## Session — 2026-06-03 (stable/PR-friendly implementation)

**Goal:** land the in-flight tree and move toward a Claude-first stable release.

### Landed

- Committed the untracked in-flight sources: `example_lsp.py` plus two `mcp_logging_proxy.py`, and regenerated output. `.claude/` stays ignored (operator's local config).
- Fixed the agents CLI to resolve sources under `src/` — `tests/test_agents_cli.py` now passes 25/25.
- Added a generated, drift-checked `docs/INVENTORY.md` (FR-12) as the authoritative plugin-entry list; fixed `snapshot_tree` to cover file targets.

- Relaxed the bundle-membership gate: a construct is installable without catalog-bundle membership (bundles are optional curation now); removed `test_every_construct_in_at_least_one_bundle`.
- Added `scripts/regen.{sh,ps1}` and `.github/workflows/regen-bot.yml` (auto-regenerate + commit on same-repo PR branches; forks fall back to the drift gate).
- Release scaffolding: `LICENSE` (MIT), PR/issue templates, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CODEOWNERS` (commented template), `RELEASING.md`, `.github/dependabot.yml`. Version is already `1.0.0`.
- CI (`ci.yml`) now runs all four suites (`test_marketplace`, `test_schema_fitness`, `test_agents_cli`, `test_tooling`); fixed stale plugin names in `compat-headless-claude.yml` (left advisory per its promotion plan).
- Contributor tooling: `scripts/new_construct.py`, `scripts/validate_source.py` (+ `.pre-commit-config.yaml`), `tasks.py`, with `tests/test_tooling.py` (10 tests).

### Verified

- `uv run tasks.py verify` → drift-clean + all four suites + `claude plugin validate ./` "Validation passed".
- Fresh `git clone` reproduces byte-identical (`--check` clean) and runs all four suites green.
- North-star drop-in proven: `new_construct.py skill <name>` → regenerate → entry appears in `marketplace.json` + `docs/INVENTORY.md` with NO `catalog.toml` edit.
- **Branch pushed; all 14 CI workflows green** on the tip (incl. all 9 per-construct compat workflows after fixing their post-reorg staleness — see `PITFALLS.md`). Validated locally with `act` first.

### Owner's remaining manual steps (not done autonomously)

- The branch is pushed and its PR is green end-to-end — review and merge to `main`.
- After merge, tag `v1.0.0` (see `RELEASING.md`).
- Optional: set the `CODEOWNERS` handle; promote `compat-headless-claude.yml` to required after an observed green run.

### Out of scope (per plan section 4.4 / ROADMAP)

- 6-platform QA parity (#9–#14) and multi-instance fixes (#37–#42); re-adding archived real content (#16–#18); PE-4 pinning example MCP/LSP versions.

## Session end — 2026-05-28 (afternoon)

**Branch:** `chore/housekeeping-and-roadmap` (PR #10, 15 commits after this one)
**Tip commit (about to push):** symmetric single/multi example set + `src/` reorg + 15 review-finding fixes
**Working tree:** clean except `.claude/` untracked (operator's local Claude config)

## What this session shipped

Three-part refactor in one commit per the plan at `~/.claude/plans/okay-this-is-a-cuddly-rain.md`:

### Part 1: Symmetric single/multi example set

- Every Claude-supported construct now demonstrates both layouts via paired `example-single/` + `example-multi/` source plugins.
- Renamed `src/skills/example/` → `src/skills/example-multi/` for naming symmetry with the existing `example-single`.
- Created paired `example-single` + `example-multi` for command, agent, mcp, lsp, monitor, output-style, theme.
- Hooks expanded to 9 per-event reference plugins (`example-userpromptsubmit/`, `example-pretooluse/`, `example-posttooluse/`, `example-notification/`, `example-stop/`, `example-subagentstop/`, `example-sessionstart/`, `example-sessionend/`, `example-precompact/`) plus one `example-multi/` covering all nine events.
- Rule stays at one example dir (not a Claude plugin component per F8).

### Part 2: `src/` reorganization

- Ten construct source dirs (`skills/`, `rules/`, `commands/`, `agents/`, `hooks/`, `mcp-servers/`, `lsp-servers/`, `monitors/`, `output-styles/`, `themes/`) moved from repo root to `src/`.
- Two operator-authored TOMLs (`MARKETPLACE.toml`, `catalog.toml`) moved alongside into `src/`.
- Used `git mv` so `git log --follow` traces history through the move.
- Updated 10 `source_directory` lines in `scripts/constructs.py` to point at `REPO_ROOT / "src" / "<dir>"`.
- Updated 2 path constants in `scripts/utils.py`: `MARKETPLACE_TOML`, `CATALOG`.
- `scripts/` stayed at root; `tests/`, `docs/`, `.github/` likewise.

### Part 3: 15 code-review fixes from commit 649b398 audit

- All 15 findings landed. CI workflow break (`compat-agents-cli.yml`), Codex/Cursor hardcoded manifest paths, doc cascade gap (TEST_YOURSELF, claude-stub README), helper symmetry across constructs, dict.get null swallowing, exception widening, junk-dir filter, narrowed `_description_from_construct` except, parameterized `test_skill_plugin_layouts`, split solo-vs-multi mirror tests, rewrote `_make_marketplace_entry` docstring.
- The one DEFERRED finding (#12, `.agents/.gemini/` mirror nesting) stays on ROADMAP #42/#39. NOTE comments remain in `scripts/platforms.py`.

## Marketplace shape post-implementation

- **27 plugin entries** in `.claude-plugin/marketplace.json` (was 11):
  - skill: 2 (example-single, example-multi)
  - command/agent/mcp/lsp/monitor/output-style/theme: 2 each = 14
  - hook: 10 (9 per-event + example-multi)
  - Subtotal Claude-supported individuals: 26
  - Plus 1 catalog bundle (`bundle-examples`, now with 26 members).
- Rule emits 1 source plugin (not in Claude marketplace per F8; still surfaces on Cursor/Codex/Windsurf).
- All non-bundle Claude `plugin.json` `name` fields are unique-per-plugin in the shape `dgxsparklabs-<construct.prefix>-<plugin>`.

## Tests state

- `uv run tests/test_marketplace.py` — **80 tests pass** (was 79; +1 new `test_per_event_hook_plugins_exist`).
- `uv run tests/test_schema_fitness.py` — **21 tests pass**.
- `uv run scripts/generate_manifest.py --check` — drift-clean.

## What's still paused (not blocking PR #10 merge)

- 6 platform QA cycles (Cursor IDE, Cursor CLI, Gemini, Windsurf, Devin, `.agents/` shim) — ROADMAP #9-#14.
- 6 multi-instance verification follow-ups — ROADMAP #37-#42, each blocked on the matching QA cycle.
- The mirror-nesting issue (`.agents/skills/<plugin>/skills/<skill>/SKILL.md`) is now affecting more plugins post-expansion; per-platform fixes land in ROADMAP #42/#39.
- F4 visual theme — interactive verification, operator-only.

## Critical-rules adherence

- No AI co-author attribution in the commit message (per `docs/archive/rules-pre-stable-2026-05-26/no-ai-credit/`).
- No direct push to `main` — PR #10 only.
- Stayed within plan scope: did not touch non-Claude per-platform mirror flattening (deferred); did not move `scripts/` (the user's clarity goal is achieved by `src/` containing source content).
