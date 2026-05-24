# Restructure Report — Option D (Native Construct Folders)

Date: 2026-05-23
Branch: feat/claude-plugin-compliance
Commit: d7a046d

---

## 1. Summary

Examples now live in their construct's native folder, not in a separate
`examples/` directory. This is "Option D — examples domain bundle."

**What was moved:**

| Old path | New path |
|----------|----------|
| `examples/example-skill/` | `skills/example-skill/` |
| `examples/example-rule/` | `rules/example-rule/` |
| `examples/example-command/` | `commands/example-command/` |
| `examples/example-agent/` | `agents/example-agent/` |
| `examples/example-hook/` | `hooks/example-hook/` |
| `examples/example-mcp/` | `mcp-servers/example-mcp/` |
| `examples/example-lsp/` | `lsp-servers/example-lsp/` |
| `examples/example-monitor/` | `monitors/example-monitor/` |
| `examples/example-output-style/` | `output-styles/example-output-style/` |
| `examples/example-theme/` | `themes/example-theme/` |

All moves used `git mv` so git tracks them as renames. The `examples/`
directory was removed (empty after all moves).

**What was added:**

8 new top-level source directories:
`commands/`, `agents/`, `hooks/`, `mcp-servers/`, `lsp-servers/`,
`monitors/`, `output-styles/`, `themes/`

10 new `[<construct>_domain.examples]` entries in `catalog.toml`.

10 new `_generated/<construct>s-examples/` dep-only bundle plugins.

---

## 2. Catalog Changes

**`example_directory` fields** — all 10 `[construct.*]` blocks updated:

```toml
# Before (example):
[construct.skill]
example_directory = "examples/example-skill/"

# After:
[construct.skill]
example_directory = "skills/example-skill/"
```

Same pattern applied to all 10 construct types (rule, command, agent,
hook, mcp, lsp, monitor, output-style, theme).

**New `[<construct>_domain.examples]` sections** — one per construct:

```toml
[skill_domain.examples]
description = "Reference example skill ..."
members = ["example-skill"]

[rule_domain.examples]
description = "Reference example rule ..."
members = ["example-rule"]

# ... (command_domain.examples, agent_domain.examples, hook_domain.examples,
#      mcp_domain.examples, lsp_domain.examples, monitor_domain.examples,
#      output_style_domain.examples, theme_domain.examples)
```

Note: multi-word constructs use underscore convention in the domain key
(`output_style_domain`, not `output-style_domain`).

---

## 3. Generator Changes

**File:** `scripts/generate_manifest.py`

**Removed:**
- `EXAMPLES_DIR` constant (examples no longer live in a single directory)
- `list_examples()` function (replaced by per-construct enumeration)
- `gen_example_entries()` function (replaced by `gen_example_bundles()`)

**Modified:**
- `list_skills()` and `list_rules()` now exclude `example-*` directories to
  prevent examples from being treated as real skills/rules
- `gen_skill_bundles()` and `gen_rule_bundles()` now skip `dname == "examples"`
  to avoid emitting a standalone `skills-examples` via the old bundle path
  (it is emitted by `gen_example_bundles()` instead, with the right category)

**Added:**
- `_domain_table_key(construct_key)` helper — converts construct keys to
  domain table names (e.g., `"output-style"` → `"output_style_domain"`)
- `gen_example_bundles(mp, cat)` — the main new function:
  1. Iterates all construct types in `catalog.toml`
  2. For each, looks up `[<construct>_domain.examples]`
  3. Emits one `"example"` category manifest entry per member, pointing at
     the native source directory (e.g., `./skills/example-skill`)
  4. Emits one `"example-bundle"` category manifest entry for the dep-only
     plugin `_generated/<construct>s-examples/`

**Updated `write_all()` summary output** to include `Example bundles` line.

---

## 4. Test Changes

**File:** `tests/test_marketplace.py`

**Removed:**
- `EXAMPLES_DIR = REPO_ROOT / "examples"` constant
- `list_examples()` function (replaced by `list_examples_native()`)
- `test_examples_dir_exists` (replaced by `test_examples_not_in_separate_dir`)

**Added constants:**
- `CONSTRUCT_DIRS` dict mapping 8 new folder names to Paths
- `CONSTRUCT_EXAMPLES` dict mapping construct folder → expected example name

**New tests in `TestSourceLayout`:**
- `test_commands_dir_exists`, `test_agents_dir_exists`, `test_hooks_dir_exists`,
  `test_mcp_servers_dir_exists`, `test_lsp_servers_dir_exists`,
  `test_monitors_dir_exists`, `test_output_styles_dir_exists`,
  `test_themes_dir_exists` (8 new dir assertions)
- `test_examples_not_in_separate_dir` (asserts `examples/` does NOT exist)
- `test_each_construct_dir_has_its_example` (every native dir has its example)

**New tests in `TestConfigFiles`:**
- `test_catalog_has_all_ten_construct_types`
- `test_catalog_has_examples_domain_for_each_construct`
- `test_examples_domain_members_exist_in_source_dirs`

**New tests in `TestExamples`:**
- `test_examples_live_in_native_dirs_not_examples_folder`
- Updated `list_examples()` → `list_examples_native()` calls

**New tests in `TestGeneratedManifests`:**
- `test_example_bundle_plugins_exist`
- `test_example_bundle_plugins_have_dependencies`
- Updated `test_plugin_count`: 71 → 81

**Updated skill/rule domain tests:**
- `test_every_skill_in_one_domain` and `test_every_rule_in_one_domain` now
  skip `dname == "examples"` to avoid false orphan detection

**Total: 55 tests (up from 40), all passing.**

---

## 5. Plugin Count

| Category | Count |
|----------|-------|
| Skills (individual) | 26 |
| Skill bundles | 8 |
| Rules (individual) | 21 |
| Rule bundles (domains) | 5 |
| rules-all | 1 |
| Examples (individual, direct source ref) | 10 |
| Example bundles | 10 |
| **Total** | **81** |

Previous total: 71. Delta: +10 (the 10 new example-bundle plugins; the 10
individual example entries now point at native source paths instead of the
old `examples/` path, so the count is the same).

---

## 6. CI Verification

The commit `d7a046d` triggered CI on two events: `push` and `pull_request`.

**PR trigger (pull_request) — all 11 workflows:**

| Workflow | Result |
|----------|--------|
| CI (test suite + drift check) | success |
| Compat — Skill (Claude + Devin + Codex + Gemini) | success |
| Compat — Command (Claude) | success |
| Compat — Agent (Claude) | success |
| Compat — Hook (Claude + Gemini migration check) | success |
| Compat — MCP Server (Claude + Devin + Codex + Gemini) | success |
| Compat — Monitor (Claude) | success |
| Compat — Output Style (Claude) | success |
| Compat — Theme (Claude) | success |
| Compat — Gemini Extension | success |
| Compat — Marketplace Add (Claude + Codex) | success |

**Push trigger — 2 of 11 failed with infrastructure errors:**

- `compat-output-style` (run 26337338221): "Bad credentials" on `setup-uv@v4`.
  Not a code failure — transient GitHub Actions credential error.
- `compat-hook` (run 26337338225): "fatal: could not read Username for
  'https://github.com'" during `actions/checkout@v4`. Same root cause —
  transient CI infrastructure error, not a code failure.

Both failures reproduced on the same timestamp batch (16:05:03–04Z) and
are clearly infrastructure-side, not result of the restructure changes.
The PR trigger runs for the exact same commit SHA all passed.

---

## 7. PR Description Update

PR #1 description updated via `gh pr edit 1 --body-file docs/pr1-body.md`.

Changes made to the PR description:
- Updated plugin count in summary: 71 → 81
- Added feature #3: "Native construct folders (Option D restructure)"
- Updated "What's installable after merge" to include example plugin
  and example-bundle install examples
- Added "Contributing a new plugin" section with new `cp -r` in-place workflow
- Updated "Breaking changes" to note the example path moves
- Updated test plan plugin count: 40 tests → 55 tests
- Added restructure verification checklist items

---

## 8. Surprises

**Generator `list_skills()` + `list_rules()` needed example exclusion.**
After moving `example-skill` into `skills/`, it was being picked up as a
real skill (it has a `SKILL.md`). Added `not d.name.startswith("example-")`
filter. Same for `list_rules()`. Without this, the generator would have
emitted a `skill-example-skill` plugin wrapper and tried to add `example-skill`
to `rules-all`, both wrong.

**`skill_domain.examples` / `rule_domain.examples` needed special-casing in
bundle generators.** `gen_skill_bundles()` iterates `skill_domain.*` and the
new `examples` domain would have produced a `skills-examples` bundle via the
old code path (with `skill-example-skill` as a dependency — wrong). Added
`if dname == "examples": continue` guard so the examples domain is handled
exclusively by `gen_example_bundles()`.

**Two push-trigger CI failures were infrastructure errors, not code failures.**
Both failed at `actions/checkout@v4` / `setup-uv@v4` with credential errors
in the same ~1s window, indicating a transient GitHub Actions issue. The PR
trigger runs for the identical commit SHA all passed. No code changes needed.

**`ADDING_A_COMMAND.md` had a stale note** about `commands/` not existing
("create one if it doesn't exist") and an explicit `mkdir -p commands`. Both
removed — `commands/` now exists as a tracked directory containing
`example-command/`.
