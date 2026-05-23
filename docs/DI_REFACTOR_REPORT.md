# DI Refactor Report

**Branch:** `feat/claude-plugin-compliance`
**Commit:** 79caefb
**Date:** 2026-05-24

## What Changed

### Architecture

Replaced the monolithic `scripts/generate_manifest.py` (628 lines, 15 special-case functions) with a typed, polymorphic strategy-pattern architecture:

| File | Role | Lines |
|------|------|-------|
| `scripts/utils.py` | Shared helpers (`scan_source_dir`, `_load_plugin_json`, `_frontmatter`, `_marketplace_*`, `write_plugin_json`) | ~90 |
| `scripts/constructs.py` | 10 Construct classes + CONSTRUCTS registry | ~230 |
| `scripts/platforms.py` | 6 Platform classes + PLATFORMS registry | ~130 |
| `scripts/bundles.py` | Bundle + BundleMember dataclasses + `load_bundles` with validation | ~130 |
| `scripts/generate_manifest.py` | 5-phase orchestrator | ~120 |

The old generator had 15+ special-case functions. The new one has zero — all dispatch is polymorphic through the registries.

### Generator Phases

1. **Phase 1**: Individual construct plugins — `construct.emit(name, plugin_dir)` for every source instance
2. **Phase 2a**: Catalog bundles — `load_bundles(CATALOG, CONSTRUCTS)` then `_emit_bundle_plugin`
3. **Phase 2b**: Code-generated catch-alls — `bundle-<prefix>-all` per construct with sources
4. **Phase 3**: Cross-platform mirrors — `platform.emit(construct, name)` for each supported construct
5. **Phase 4**: Gemini extension manifest
6. **Phase 5**: Top-level `marketplace.json` from in-memory entries (never re-reads filesystem)

### catalog.toml

Before: 258 lines with `[construct.*]`, `[skill_domain.*]`, `[rule_domain.*]`, `[platform.*]` blocks.

After: ~110 lines with ONLY `[bundle.*]` blocks — 8 skill domain bundles, 5 rule domain bundles, 1 examples cross-construct bundle.

### Example Directory Renames (decision #18)

All 10 example directories renamed from `example-<construct>` to `example`:

| Before | After |
|--------|-------|
| `skills/example-skill/` | `skills/example/` |
| `rules/example-rule/` | `rules/example/` |
| `commands/example-command/` | `commands/example/` |
| `agents/example-agent/` | `agents/example/` |
| `hooks/example-hook/` | `hooks/example/` |
| `mcp-servers/example-mcp/` | `mcp-servers/example/` |
| `lsp-servers/example-lsp/` | `lsp-servers/example/` |
| `monitors/example-monitor/` | `monitors/example/` |
| `output-styles/example-output-style/` | `output-styles/example/` |
| `themes/example-theme/` | `themes/example/` |

### Compat Workflow Updates

7 compat workflows updated for renamed example plugins:
- `compat-mcp.yml`: `example-mcp` → `mcp-example`
- `compat-agent.yml`: `example-agent` → `agent-example`
- `compat-command.yml`: `example-command` → `command-example`
- `compat-hook.yml`: `example-hook` → `hook-example`
- `compat-monitor.yml`: `example-monitor` → `monitor-example`
- `compat-output-style.yml`: `example-output-style` → `output-style-example`
- `compat-theme.yml`: `example-theme` → `theme-example`

### Documentation

- Deleted 11 `docs/ADDING_*.md` files
- Created `docs/ADDING_A_CONSTRUCT.md` (single parameterized contribution guide)
- Updated `docs/CONSTRUCT_TYPES.md` (new architecture reference table)
- Updated `docs/RESUME_HERE.md` (post-refactor orientation)
- Added `docs/PLAN_DI_REFACTOR.md` + critique docs

### Test Suite

Deleted 6 stale tests that asserted on the old catalog schema (`[construct.*]`, `[skill_domain.*]`). Added 28 new tests. Final suite: 34 tests, all green.

New test classes:
- `TestSourceLayout` — uniform construct/example/kebab validation
- `TestGeneratedPlugins` — generated plugin paths and schemas
- `TestCatchAllBundles` — code-generated catch-all correctness
- `TestPlatformMirrors` — per-platform mirror assertions (Codex, Gemini, Cursor, Windsurf, Devin)
- `TestMarketplaceJson` — schema, sorting, completeness
- `TestNoOrphanedConstructs` — every instance in at least one bundle
- `TestBundleValidation` — reserved names, empty bundles, member syntax
- `TestConstructRegistry` — prefix uniqueness and kebab-case
- `TestPluginCount` — computed formula (not hardcoded)
- `TestMarketplaceToml` — catalog bundles-only assertion

---

## Plugin Name Snapshot Diff

Before (81 plugins) → After (81 plugins). Same total count; different names.

```diff
1,17c1,31
< "agents-examples"
< "commands-examples"
< "example-agent"
< "example-command"
< "example-hook"
< "example-lsp"
< "example-mcp"
< "example-monitor"
< "example-output-style"
< "example-rule"
< "example-skill"
< "example-theme"
< "hooks-examples"
< "lsps-examples"
< "mcps-examples"
< "monitors-examples"
< "output-styles-examples"
---
> "agent-example"
> "bundle-agent-all"
> "bundle-ai-services-skills"
> "bundle-code-analysis-skills"
> "bundle-command-all"
> "bundle-communication-skills"
> "bundle-devops-skills"
> "bundle-documentation-rules"
> "bundle-environment-rules"
> "bundle-examples"
> "bundle-hook-all"
> "bundle-lsp-all"
> "bundle-mcp-all"
> "bundle-meta-tooling-skills"
> "bundle-monitor-all"
> "bundle-notifications-rules"
> "bundle-output-style-all"
> "bundle-project-scaffolding-skills"
> "bundle-quality-rules"
> "bundle-rule-all"
> "bundle-search-research-skills"
> "bundle-session-management-skills"
> "bundle-skill-all"
> "bundle-theme-all"
> "bundle-workflow-rules"
> "command-example"
> "hook-example"
> "lsp-example"
> "mcp-example"
> "monitor-example"
> "output-style-example"
23a38
> "rule-example"
39,45d53
< "rules-all"
< "rules-documentation"
< "rules-environment"
< "rules-examples"
< "rules-notifications"
< "rules-quality"
< "rules-workflow"
49a58
> "skill-example"
72,81c81
< "skills-ai-services"
< "skills-code-analysis"
< "skills-communication"
< "skills-devops"
< "skills-examples"
< "skills-meta-tooling"
< "skills-project-scaffolding"
< "skills-search-research"
< "skills-session-management"
< "themes-examples"
---
> "theme-example"
```

### Summary of diff

**Removed (24 old names):**
- 10 `example-<construct>` individual plugins (renamed)
- 10 `<construct>s-examples` per-construct bundle plugins (replaced by `bundle-examples`)
- 4 `skills-<domain>` bundles (renamed to `bundle-<domain>-skills`)
- 5 `rules-<domain>` bundles (renamed to `bundle-<domain>-rules`)
- `rules-all` (renamed to `bundle-rule-all`)

**Added (25 new names):**
- 10 `<construct>-example` individual plugins (renames from above)
- 10 `bundle-<prefix>-all` catch-all bundles (code-generated, new)
- 8 `bundle-<domain>-skills` bundles (renames from `skills-<domain>`)
- 5 `bundle-<domain>-rules` bundles (renames from `rules-<domain>`)
- `bundle-examples` cross-construct bundle (new)
- `bundle-rule-all` (renamed from `rules-all`)

Real plugin names (skills like `skill-telegram-notify`, rules like `rule-no-ai-credit`) are **unchanged**.

---

## Local Test Results

```
Ran 34 tests in 6.756s
OK
```

All 34 tests pass. Drift check: `OK: generated content matches committed content.`

---

## Asymmetries Dissolved

| Letter | Asymmetry | Resolution |
|--------|-----------|------------|
| A | Examples filtered out then re-included via `gen_example_bundles()` | First-class bundle members; one code path |
| B | `gen_skill_bundles()` / `gen_rule_bundles()` as separate functions | One generic bundle generator |
| C | Skills/rules privileged in tests | Tests iterate `CONSTRUCTS.values()` uniformly |
| D | `rules-all` exists; `skills-all` doesn't | `bundle-<construct>-all` for every construct |
| E | Naming uses both `_` and `-` | Hyphens throughout |
| F | 11 near-duplicate ADDING_*.md docs | One parameterized doc + reference table |
| G | description field placement varies | Each Construct class knows where its description lives |
| H | Mirror generation only for skills/rules | `Platform.supports` declares which constructs each platform mirrors |
| K | Plugin.json field variation per construct | Each Construct class builds its own plugin.json shape |

---

## Surprises / Notes

1. **The example-rule directory didn't have `rule.md`** — it had a pre-built `rules/example-rule.md` (the old generated format). Added `rules/example/rule.md` as the canonical source file that `RuleConstruct.emit` copies.

2. **`.devin/rules/` mirror removed** — the previous generator emitted `.devin/rules/` (21 files). Per `docs/PLATFORM_INSPECTION_CATALOG.md` and the Devin empirical findings, Devin reads rules from `.cursor/rules/` and `.windsurf/rules/` natively. The Devin platform now correctly emits only `.devin/skills/` mirrors.

3. **Git rename detection is cosmetic** — git's heuristic similarity matching detected renames between deleted source files and new `_generated/` files. This is harmless; the actual file contents are correct. The heuristics produce visually noisy `git log --follow` output but don't affect correctness.

4. **CRLF warnings on Windows** — expected on Windows; git normalizes line endings on commit. No impact on cross-platform CI.

5. **81 plugin count preserved** — the refactor produced the same total count (81) despite the nomenclature changes. Individual construct counts shifted: rules went from 21 to 22 (example now included), skills went from 26 to 27.
