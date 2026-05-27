# Objective checklist — multi-instance-capable plugins (Claude-only)

A boolean checklist for verifying the implementation is complete and correct. Every item is independently verifiable with a one-line command or file inspection. Mark items `[x]` only when the verification command actually passes.

## Code changes

- [ ] **`scripts/constructs.py` `_base_plugin_shape` f-string flipped** to `f"{brand}-{construct.prefix}-{name}"`
  - **Verify**: `grep -n 'name.*f.*brand.*construct.prefix.*{name}' scripts/constructs.py` returns a hit
  - **Counter-verify**: `grep -n 'construct.category}' scripts/constructs.py` returns NO hits in `_base_plugin_shape`

- [ ] **`SkillConstruct.build_plugin_json` has layout-detection branch**
  - **Verify**: function reads root SKILL.md presence + skills/ subdir presence; raises ValueError on both-or-neither; sets `"skills": ["./"]` for single-skill case and `"skills": ["./skills/"]` for multi-skill case
  - **Test command**: `grep -A 30 'def build_plugin_json' scripts/constructs.py | grep -E 'root_skill|skills_subdir|ValueError|has_root|has_subdir'` returns 5+ hits

- [ ] **`scripts/utils.py` exports `_read_source_plugin_description` helper**
  - **Verify**: `grep -n 'def _read_source_plugin_description' scripts/utils.py` returns one hit
  - **Counter-verify**: function signature accepts `(src_plugin_dir, fallback)` and reads `<src>/.claude-plugin/plugin.json` `description` field

- [ ] **`scripts/platforms.py` has 6 NOTE comments tagging non-Claude paths as multi-instance-unverified**
  - **Verify**: `grep -c 'multi-instance.*UNVERIFIED\|multi-instance.*not yet verified\|multi-instance source layout' scripts/platforms.py` returns 6 or more
  - **Counter-verify**: no actual code changes in `CursorPlatform.build_plugin_json`, `CodexPlatform.build_plugin_json`, or any non-Claude `emit()` methods

- [ ] **`scripts/generate_manifest.py` unchanged from `3275049`** (no code changes needed; `_make_marketplace_entry` already reads `plugin_dir.name`)
  - **Verify**: `git diff 3275049 -- scripts/generate_manifest.py` returns empty

## Source content changes

- [ ] **`skills/example/SKILL.md` deleted** (old root-level single-skill content)
  - **Verify**: `test ! -f skills/example/SKILL.md && echo OK`

- [ ] **`skills/example/.claude-plugin/plugin.json` exists with correct shape**
  - **Verify**: `jq '.name' skills/example/.claude-plugin/plugin.json` returns `"dgxsparklabs-skill-example"` AND `jq '.description' ...` returns a non-empty string

- [ ] **`skills/example/skills/notebook/SKILL.md` exists with frontmatter `name: notebook`**
  - **Verify**: `head -3 skills/example/skills/notebook/SKILL.md | grep -E '^name: notebook$'` returns a hit

- [ ] **`skills/example/skills/status/SKILL.md` exists with frontmatter `name: status`**
  - **Verify**: `head -3 skills/example/skills/status/SKILL.md | grep -E '^name: status$'` returns a hit

- [ ] **`skills/example/README.md` describes both skills + the multi-skill layout**
  - **Verify**: `grep -E 'notebook|status' skills/example/README.md | wc -l` returns 2 or more

- [ ] **`skills/example-single/.claude-plugin/plugin.json` exists with correct shape**
  - **Verify**: `jq '.name' skills/example-single/.claude-plugin/plugin.json` returns `"dgxsparklabs-skill-example-single"`

- [ ] **`skills/example-single/SKILL.md` exists with frontmatter `name: hello`**
  - **Verify**: `head -3 skills/example-single/SKILL.md | grep -E '^name: hello$'` returns a hit

- [ ] **`skills/example-single/README.md` describes the single-skill layout**
  - **Verify**: `test -f skills/example-single/README.md`

- [ ] **`catalog.toml` `bundle.examples` includes `skill:example-single` member**
  - **Verify**: `grep '"skill:example-single"' catalog.toml` returns a hit

## Generator output (post-regeneration)

- [ ] **Generator runs clean**: `uv run scripts/generate_manifest.py` exits 0 and reports 11 plugin entries
  - **Verify**: count "Generated 11 plugin entries" in output

- [ ] **`.claude-plugin/marketplace.json` has 11 plugin entries**
  - **Verify**: `jq '.plugins | length' .claude-plugin/marketplace.json` returns 11

- [ ] **`_generated/skill-example/.claude-plugin/plugin.json`** has `name: "dgxsparklabs-skill-example"` and `skills: ["./skills/"]`
  - **Verify**: `jq '.name + " " + (.skills | tostring)' _generated/skill-example/.claude-plugin/plugin.json` returns `"dgxsparklabs-skill-example [\"./skills/\"]"`

- [ ] **`_generated/skill-example-single/.claude-plugin/plugin.json`** has `name: "dgxsparklabs-skill-example-single"` and `skills: ["./"]`
  - **Verify**: `jq '.name + " " + (.skills | tostring)' _generated/skill-example-single/.claude-plugin/plugin.json` returns `"dgxsparklabs-skill-example-single [\"./\"]"`

- [ ] **`_generated/skill-example/skills/notebook/SKILL.md` and `.../skills/status/SKILL.md` both exist** (byte-copied from source)
  - **Verify**: `ls _generated/skill-example/skills/ | wc -l` returns 2

- [ ] **`_generated/skill-example-single/SKILL.md` exists** (byte-copied from source)
  - **Verify**: `test -f _generated/skill-example-single/SKILL.md`

- [ ] **Drift check is clean**
  - **Verify**: `uv run scripts/generate_manifest.py --check` exits 0 (no drift between source + generated)

## Test changes

- [ ] **`test_individual_plugin_name_is_unique_brand_namespace` renamed + updated** (was `test_individual_plugin_name_is_brand_namespace` under Path A)
  - **Verify**: `grep 'def test_individual_plugin_name_is_unique_brand_namespace' tests/test_marketplace.py` returns a hit
  - **Counter-verify**: `grep 'def test_individual_plugin_name_is_brand_namespace' tests/test_marketplace.py` returns NO hits

- [ ] **`test_skill_plugin_layouts` exists**
  - **Verify**: `grep 'def test_skill_plugin_layouts' tests/test_marketplace.py` returns a hit AND test asserts both `["./skills/"]` for `skill-example` and `["./"]` for `skill-example-single`

- [ ] **`test_mcp_server_keys_unique_across_plugins` exists**
  - **Verify**: `grep 'def test_mcp_server_keys_unique_across_plugins' tests/test_marketplace.py` returns a hit

- [ ] **Marketplace-count formula updated to 11**
  - **Verify**: `grep -B 2 -A 2 'individuals + catalog_bundles' tests/test_marketplace.py` shows the formula matches 10 + 1 = 11

- [ ] **All marketplace tests pass**
  - **Verify**: `uv run tests/test_marketplace.py 2>&1 | tail -3` shows `OK` and non-zero test count

- [ ] **All schema-fitness tests pass**
  - **Verify**: `uv run tests/test_schema_fitness.py 2>&1 | tail -3` shows `OK` and 21 tests

## Doc cascade

- [ ] **`docs/ADDING_A_CONSTRUCT.md` updated**: Trace section rewritten for new model + three-recipe section present
  - **Verify**: `grep -c 'Pattern 1\|Pattern 2\|Pattern 3\|dgxsparklabs-skill-' docs/ADDING_A_CONSTRUCT.md` returns 5+ hits
  - **Counter-verify**: no remaining `lab-notebook` references in the trace section (was the Path A worked example)

- [ ] **`docs/TEST_YOURSELF.md` updated**: Claude reference card under new model
  - **Verify**: `grep '/dgxsparklabs-skill-example:notebook\|/dgxsparklabs-skill-example:status\|/dgxsparklabs-skill-example-single:hello' docs/TEST_YOURSELF.md` returns 3+ hits

- [ ] **`docs/USER_GUIDE.md` slash-command table updated** with new prefix shapes
  - **Verify**: `grep 'dgxsparklabs-skill-' docs/USER_GUIDE.md` returns a hit

- [ ] **`docs/PLATFORMS.md` has multi-instance-unverified banner for non-Claude platforms**
  - **Verify**: `grep -i 'multi-instance.*unverified\|paused.*platform QA' docs/PLATFORMS.md` returns a hit

- [ ] **`docs/CONSTRUCT_TYPES.md` notes multi-instance capability for skill**
  - **Verify**: `grep -i 'multi-instance\|multi-skill' docs/CONSTRUCT_TYPES.md` returns a hit

- [ ] **`README.md` updated**: install count 11, new slash forms, simpler grep fallback before jq filter
  - **Verify**: `grep 'dgxsparklabs-skill-example' README.md` returns a hit AND `grep '11 plugin' README.md` returns a hit

- [ ] **`docs/RESUME_HERE.md` updated** for new naming pattern
  - **Verify**: `grep 'dgxsparklabs-skill-\|brand-prefix' docs/RESUME_HERE.md` returns a hit

- [ ] **`CHANGELOG.md` has entry titled multi-instance-capable layout (Claude-only)**
  - **Verify**: `head -30 CHANGELOG.md | grep -i 'multi-instance.*claude-only\|multi-instance.*pause'` returns a hit
  - **Counter-verify**: entry explicitly mentions what's paused (non-Claude verification) AND the follow-up roadmap items

## ROADMAP updates

- [ ] **ROADMAP.md has items #37-#42** (one per non-Claude platform multi-instance verification follow-up)
  - **Verify**: `grep -E '^\| 3[7-9]|^\| 4[0-2]' docs/ROADMAP.md | wc -l` returns 6 or more

## Hermetic Docker verification (optional but recommended)

- [ ] **`/dgxsparklabs-skill-example:notebook` resolves** via the body-dumper stub
  - **Verify**: from inside qa-claude container with stub running, body-dumper log captures the slash form

- [ ] **`/dgxsparklabs-skill-example:status` resolves** via the body-dumper stub
  - **Verify**: same as above for status

- [ ] **`/dgxsparklabs-skill-example-single:hello` resolves** via the body-dumper stub
  - **Verify**: same as above for hello

- [ ] **`claude plugin details dgxsparklabs-skill-example` lists BOTH `notebook` and `status` as components**
  - **Verify**: command output contains both skill names (this is the regression check for Path A's "first-installed-wins" collapse)

## Git + PR state

- [ ] **STATE.md updated** to reflect end-of-implementation
  - **Verify**: `head -20 STATE.md | grep -i 'multi-instance\|path d\|claude-only'` returns a hit

- [ ] **One commit on `chore/housekeeping-and-roadmap` branch** with message `refactor(skills): multi-instance-capable layout (Claude-only); revert Path A; pause non-Claude verification`
  - **Verify**: `git log -1 --pretty=%s` returns the message above

- [ ] **No AI co-author attribution in commit message**
  - **Verify**: `git log -1 --pretty=%B | grep -i 'Co-Authored-By\|Generated with\|Created by\|Built with'` returns NO hits

- [ ] **Commit pushed to remote**
  - **Verify**: `git log origin/chore/housekeeping-and-roadmap..HEAD` returns empty

- [ ] **PR #10 has 13 commits total**
  - **Verify**: `gh pr view 10 --json commits --jq '.commits | length'` returns 13

## Done state — what success looks like

When every box above is checked:

1. PR #10 has 13 commits, the last reverts Path A and lands multi-instance for Claude.
2. The example marketplace ships 11 plugins (was 10): the two skill plugins side-by-side teach contributors both layouts.
3. The slash form `/dgxsparklabs-skill-example:notebook` (or `:status`, or `/dgxsparklabs-skill-example-single:hello`) resolves on the hermetic Claude stub.
4. The `claude plugin details dgxsparklabs-skill-example` lookup works per-plugin (Path A's collapse is gone).
5. The 5 non-Claude platforms continue to emit per their existing code; their multi-instance behavior is acknowledged unverified via NOTE comments + ROADMAP follow-ups #37-#42.
6. Docs in 10 files have been updated to reflect the new model with the new slash forms.
7. CHANGELOG explicitly explains the Path A revert + the Claude-only scope decision.

PR #10 is then ready to merge. The next session's first task is the Cursor IDE QA cycle (ROADMAP item #9), which will produce the empirical evidence to unblock follow-up #37.
