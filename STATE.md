# STATE

> Live within-session truth. Pair with `HANDOFF.md` (between-sessions) and `PITFALLS.md` (cross-session lessons).

## Session end — 2026-05-28

**Branch:** `chore/housekeeping-and-roadmap` (PR #10, 13 commits after this one)
**Main tip:** `4b00faa` — PR #9 squash-merged
**Working tree:** clean except `.claude/` untracked (operator's local Claude config)

## What this session shipped

Implemented the **multi-instance-capable plugins (Claude-only)** refactor — Path D — per [`docs/research/multi-instance-claude-only-2026-05-27/PLAN.md`](docs/research/multi-instance-claude-only-2026-05-27/PLAN.md). One commit on PR #10. Path A (`d641f92`, 2026-05-27) was reverted; Claude `plugin.json` `name` fields are now unique-per-plugin in shape `<brand>-<construct.prefix>-<source-dir>`.

### Code changes

- `scripts/constructs.py` — `_base_plugin_shape` flipped to `f"{brand}-{construct.prefix}-{name}"`. `SkillConstruct.build_plugin_json` gained a layout-detection branch: solo (`SKILL.md` at plugin root → `skills: ["./"]`) or multi (`skills/<skill>/SKILL.md` → `skills: ["./skills/"]`). Both-or-neither layouts raise `ValueError`.
- `scripts/utils.py` — new `_read_source_plugin_description(src_plugin_dir, fallback)` helper for reading the plugin-level marketplace-listing description.
- `scripts/platforms.py` — six NOTE comments tagging non-Claude Skill paths as `multi-instance source layout UNVERIFIED` (Cursor, Codex, Gemini, Windsurf, Devin, `.agents/` shim). Code unchanged on those platforms.

### Source content changes

- `skills/example/` — reorganized to multi-skill layout. Two skills now: `skills/notebook/SKILL.md` (lab-notebook body from the old root `SKILL.md`) + `skills/status/SKILL.md` (new ~20 lines for `df -h .` + UTC). Plus operator-authored `.claude-plugin/plugin.json`. Rewrote `README.md`.
- `skills/example-single/` — NEW solo-layout reference plugin. One skill (`name: hello`).
- `catalog.toml` — `bundle.examples` adds `skill:example-single`.

### Test changes (`tests/test_marketplace.py`)

- Renamed + updated `test_individual_plugin_name_is_unique_brand_namespace` (was `_is_brand_namespace`).
- New `test_skill_plugin_layouts` — asserts both `["./skills/"]` and `["./"]` shapes from the two canonical examples.
- New `test_mcp_server_keys_unique_across_plugins` — cross-plugin MCP server-key collision check.
- Marketplace-count formula updated to `10 + 1 = 11`.
- `test_agents_skills_mirror_exists` and `test_gemini_skills_mirror_and_extension_manifest` relaxed to accept either solo (`<plugin>/SKILL.md`) or multi (`<plugin>/skills/<x>/SKILL.md`) shape — the bytes-on-disk part of the contract.

### Doc cascade (10 files)

`README.md`, `docs/ADDING_A_CONSTRUCT.md`, `docs/TEST_YOURSELF.md`, `docs/USER_GUIDE.md`, `docs/PLATFORMS.md`, `docs/CONSTRUCT_TYPES.md`, `docs/RESUME_HERE.md`, `CHANGELOG.md`, plus the two skill plugin READMEs (`skills/example/README.md` rewritten; `skills/example-single/README.md` new). The pattern is the same in each: drop Path A's shared-namespace language, document the new `<brand>-<prefix>-<plugin>` unique slash form, flag non-Claude paths as multi-instance-unverified, point at ROADMAP #37-#42.

### ROADMAP

Items #37-#42 (per-platform multi-instance verification follow-ups, one per non-Claude platform) were prepped in the prior session-end commit `5ae8619`; no further changes this session.

## Tests state

- `uv run tests/test_marketplace.py` — **79 tests pass** (was 77; +2 for the two new tests).
- `uv run tests/test_schema_fitness.py` — **21 tests pass**.
- `uv run scripts/generate_manifest.py --check` — drift-clean.

## End-of-implementation marketplace shape

- **11 plugin entries** in `.claude-plugin/marketplace.json` (was 10):
  - 10 individual Claude-supported plugins (one per construct, plus the second skill example)
  - 1 catalog bundle (`bundle-examples`, now with 11 members including `skill:example-single`)
- All non-bundle Claude `plugin.json` `name` fields are unique-per-plugin in shape `dgxsparklabs-<construct.prefix>-<plugin>` (e.g. `dgxsparklabs-skill-example`, `dgxsparklabs-command-example`).
- All slash forms follow `/dgxsparklabs-<construct.prefix>-<plugin>:<component>` — e.g. `/dgxsparklabs-skill-example:notebook`, `/dgxsparklabs-skill-example-single:hello`.

## What's still paused (not blocking PR #10 merge)

- 6 platform QA cycles (Cursor IDE, Cursor CLI, Gemini, Windsurf, Devin, `.agents/` shim) — roadmap #9-#14.
- 6 multi-instance verification follow-ups (one per non-Claude platform) — roadmap #37-#42, each blocked on the matching QA cycle.
- F4 visual theme — interactive verification, operator-only (#15).

## Critical-rules adherence

- No AI co-author attribution in the commit message (per `rules/no-ai-credit/`).
- No direct push to `main` — PR #10 only.
- Stayed within Claude-only scope. Non-Claude per-platform `emit()` / `build_plugin_json` methods got NOTE comments only; no per-skill mirror flattening; no source-plugin.json reading in `CursorPlatform.build_plugin_json`. All deferred per the plan's "What's deferred" section.
