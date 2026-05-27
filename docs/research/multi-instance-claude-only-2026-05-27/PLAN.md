# Multi-instance-capable plugins (Claude-only scope) — execution plan

## TL;DR

**What ships**: skill plugins can contain multiple skills via a `skills/<skill-name>/SKILL.md` subdirectory layout. Two source-side example plugins demonstrate the patterns side-by-side: `skills/example/` (multi-skill, two skills) and `skills/example-single/` (single-skill, one skill). All plugin.json `name` fields revert to unique brand-prefixed form `dgxsparklabs-skill-<plugin>` (Path A's shared namespace is undone).

**What's paused**: cross-platform verification on Cursor, Codex, Gemini, Windsurf, Devin, and the `.agents/` shim. The non-Claude paths in `scripts/platforms.py` continue to emit (architecture unchanged) but are NOT verified to work correctly with multi-skill source layouts. Source-code NOTE comments tag each non-Claude `emit()` method as "multi-instance unverified; see ROADMAP #9-#14." Future re-enabling per-platform is a localized edit to that platform's class, not a generator redesign.

**Operator UX (no change for installs)**:

```
claude plugin install skill-example@dgxsparklabs-marketplace --scope project
claude plugin enable  skill-example@dgxsparklabs-marketplace

# In Claude session:
/dgxsparklabs-skill-example:notebook
/dgxsparklabs-skill-example:status
/dgxsparklabs-skill-example-single:hello
```

**Contributor UX (three recipes)**:

| Pattern | Use when | Source layout |
|---|---|---|
| **Solo plugin** | One skill, no thematic siblings | `skills/<plugin>/SKILL.md` at plugin root |
| **Multi-instance plugin** | Multiple skills under one theme | `skills/<plugin>/skills/<skill-A>/SKILL.md` + `<skill-B>/SKILL.md` etc. |
| **Catalog bundle** | Group plugins of DIFFERENT construct types | Add `[bundle.*]` entry to `catalog.toml` |

## Locked decisions

1. **plugin.json `name` field**: `f"{brand}-{construct.prefix}-{source_dir_name}"` — e.g., `dgxsparklabs-skill-example`. Unique per plugin. Reverts Path A's shared-namespace pattern.
2. **Two skill example plugins**: `skill-example` (multi, 2 skills: notebook + status) + `skill-example-single` (single, 1 skill: hello).
3. **Cross-platform scope**: CLAUDE ONLY. Non-Claude per-platform paths continue to emit but are unverified under multi-skill source layouts. Architecture preserved so later per-platform fixes are localized.

---

## Code changes

### 1. `scripts/constructs.py` — `_base_plugin_shape` revert Path A

```python
# CURRENT (line ~91, Path A):
"name": f"{brand}-{construct.category}",

# AFTER:
"name": f"{brand}-{construct.prefix}-{name}",
```

Single-line f-string flip. The `name` parameter is already in scope (it's the source-directory name).

### 2. `scripts/constructs.py` — `SkillConstruct.build_plugin_json` layout detection

Replace the current method (around lines 117-123) with:

```python
def build_plugin_json(self, name: str) -> dict:
    base = _base_plugin_shape(self, name)
    src = self.source_directory / name
    root_skill = src / "SKILL.md"
    skills_subdir = src / "skills"

    has_root = root_skill.exists()
    has_subdir = skills_subdir.is_dir() and any(
        (d / "SKILL.md").exists() for d in skills_subdir.iterdir() if d.is_dir()
    )

    if has_root and has_subdir:
        raise ValueError(
            f"Source plugin {src} contains BOTH a root SKILL.md AND a "
            f"skills/ subdir with skill children. Pick one layout: either "
            f"move the root SKILL.md into skills/<name>/ or remove the "
            f"skills/ subdir."
        )
    if not has_root and not has_subdir:
        raise ValueError(
            f"Source plugin {src} contains neither a root SKILL.md "
            f"(single-skill layout) nor a skills/<name>/SKILL.md subdir "
            f"(multi-skill layout). Create one or the other."
        )

    # Description comes from the plugin-level .claude-plugin/plugin.json
    # (operator-authored, separate from any per-skill SKILL.md frontmatter).
    base["description"] = _read_source_plugin_description(src, name)
    base["skills"] = ["./"] if has_root else ["./skills/"]
    base["keywords"] = ["skill", name]
    return base
```

### 3. `scripts/utils.py` — new helper `_read_source_plugin_description`

```python
def _read_source_plugin_description(src_plugin_dir: Path, fallback: str) -> str:
    """Read the plugin-level description from <src>/.claude-plugin/plugin.json.

    This is the marketplace-listing one-liner, distinct from per-component
    descriptions (which live in each SKILL.md frontmatter for skills, or
    each agent .md frontmatter for sub-agents, etc.).

    Falls back to `fallback` (typically the plugin directory name) if the
    source plugin.json is missing or has no description field.
    """
    src_pj_path = src_plugin_dir / ".claude-plugin" / "plugin.json"
    if not src_pj_path.exists():
        return fallback
    try:
        data = json.loads(src_pj_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback
    return data.get("description", fallback)
```

### 4. `scripts/generate_manifest.py` — no changes needed

`_make_marketplace_entry` already uses `plugin_dir.name` (line 74) which is `f"{construct.prefix}-{source_dir_name}"` per Phase 1 line 152. Install command names stay unchanged.

### 5. `scripts/platforms.py` — comment-only changes for non-Claude paths

Add a `# NOTE: multi-instance source layout (skills/<skill>/SKILL.md under plugin) NOT YET VERIFIED on this platform. The current shutil.copytree produces a nested mirror that may not be discoverable by downstream consumers. See ROADMAP #9-#14 for per-platform follow-up.` to:

- `CursorPlatform.build_plugin_json` (above line 388 where `"skills"` is hardcoded)
- `CodexPlatform.build_plugin_json` (above line 198)
- `GeminiPlatform.emit` (above line 223 for the SkillConstruct branch)
- `WindsurfPlatform.emit` (above the SkillConstruct branch if present)
- `DevinPlatform.emit` (above the SkillConstruct branch if present)
- `AgentsPlatform.emit` (above line 509 SkillConstruct branch)

No code changes — these are documentation/discoverability anchors for the future implementer.

---

## Test changes (`tests/test_marketplace.py`)

### Rename existing test

Path A landed it as `test_individual_plugin_name_is_brand_namespace`. Rename + update expected value:

```python
def test_individual_plugin_name_is_unique_brand_namespace(self):
    """Each plugin's _generated/<plugin>/.claude-plugin/plugin.json `name` field
    is `<brand>-<construct.prefix>-<source-dir-name>` — unique per plugin."""
    from utils import _marketplace_name
    mp_name = _marketplace_name()
    brand = mp_name.removesuffix("-marketplace") if mp_name.endswith("-marketplace") else mp_name

    for construct in CONSTRUCTS.values():
        if type(construct) not in ClaudeCodePlatform.supports:
            continue
        for source_name in scan_source_dir(construct.source_directory):
            expected = f"{brand}-{construct.prefix}-{source_name}"
            plugin_path = REPO_ROOT / "_generated" / f"{construct.prefix}-{source_name}" / ".claude-plugin" / "plugin.json"
            with self.subTest(construct=construct.prefix, name=source_name):
                data = json.loads(plugin_path.read_text(encoding="utf-8"))
                self.assertEqual(data["name"], expected)
```

### New test — skill plugin layouts

```python
def test_skill_plugin_layouts(self):
    """Verify both example skill plugins emit the correct `skills` field."""
    # Multi-skill plugin
    multi_pj = REPO_ROOT / "_generated" / "skill-example" / ".claude-plugin" / "plugin.json"
    multi_data = json.loads(multi_pj.read_text(encoding="utf-8"))
    self.assertEqual(multi_data["skills"], ["./skills/"])
    self.assertTrue((REPO_ROOT / "_generated" / "skill-example" / "skills" / "notebook" / "SKILL.md").exists())
    self.assertTrue((REPO_ROOT / "_generated" / "skill-example" / "skills" / "status" / "SKILL.md").exists())

    # Single-skill plugin
    single_pj = REPO_ROOT / "_generated" / "skill-example-single" / ".claude-plugin" / "plugin.json"
    single_data = json.loads(single_pj.read_text(encoding="utf-8"))
    self.assertEqual(single_data["skills"], ["./"])
    self.assertTrue((REPO_ROOT / "_generated" / "skill-example-single" / "SKILL.md").exists())
```

### New test — MCP server-key cross-plugin uniqueness

```python
def test_mcp_server_keys_unique_across_plugins(self):
    """No two MCP plugins may share a top-level `mcpServers` key (e.g.,
    two plugins both defining `mcpServers.fetch`). Without this check,
    Claude's tool list would silently shadow one plugin's tool with the
    other's via `mcp__<plugin>__fetch__*` collision in the model's view.
    Recommended convention: name server keys to incorporate the plugin
    name (e.g., `git-helpers-fetch` instead of bare `fetch`)."""
    seen = {}  # key -> source plugin name
    for source_name in scan_source_dir(REPO_ROOT / "mcp-servers"):
        config_path = REPO_ROOT / "mcp-servers" / source_name / "mcp-config.json"
        if not config_path.exists():
            continue
        data = json.loads(config_path.read_text(encoding="utf-8"))
        for key in data.get("mcpServers", {}).keys():
            with self.subTest(server_key=key, plugin=source_name):
                self.assertNotIn(
                    key, seen,
                    f"MCP server key '{key}' duplicated across plugins: "
                    f"{seen.get(key, '?')} and {source_name}. Rename one "
                    f"to incorporate the plugin name."
                )
                seen[key] = source_name
```

### Update marketplace-count test

```python
# Marketplace entry count formula:
# = individuals + catalog bundles
# Individuals: 9 example plugins (Claude-supported) — rule is excluded
# After this plan: skill ships TWO source plugins (example + example-single),
# so individuals becomes 10 (was 9).
# Catalog bundles: 1 (bundle.examples)
# Total: 11 (was 10)
expected = individuals + catalog_bundles  # 10 + 1 = 11
```

### Drop test

`test_bundle_cannot_use_reserved_catchall_name` was already removed in commit `24f30bf`. No further changes to catch-all-related tests.

### Skill-name uniqueness — NOT a global test

Each per-skill mirror dir (`.gemini/skills/`, `.windsurf/skills/`, etc.) is keyed by the SOURCE PLUGIN DIRECTORY name (not the SKILL.md frontmatter `name:`), so collisions between two source plugins both having a skill named `commit` don't actually happen at the mirror level today. A global SKILL.md-name uniqueness test is NOT added. This decision supersedes earlier plan iterations that proposed it.

---

## Source content changes

### `skills/example/` — reorganize into multi-skill layout

**Delete**:
- `skills/example/SKILL.md` (the current root-level SKILL.md with `name: lab-notebook`)

**Create**:
- `skills/example/.claude-plugin/plugin.json` — operator-authored:
  ```json
  {
    "name": "dgxsparklabs-skill-example",
    "description": "Two reference skills demonstrating the multi-skill plugin layout."
  }
  ```
- `skills/example/skills/notebook/SKILL.md` — frontmatter `name: notebook`, body adapted from current SKILL.md (prints today's lab-notebook header)
- `skills/example/skills/status/SKILL.md` — frontmatter `name: status`, body that prints `df -h .` + UTC timestamp (NEW content; ~20 lines)

**Update**:
- `skills/example/README.md` — describe both skills + the multi-skill layout

### `skills/example-single/` — NEW single-skill example plugin (1 SKILL.md only)

**Create directory** `skills/example-single/` with:
- `skills/example-single/.claude-plugin/plugin.json`:
  ```json
  {
    "name": "dgxsparklabs-skill-example-single",
    "description": "One reference skill demonstrating the single-skill plugin layout."
  }
  ```
- `skills/example-single/SKILL.md` — frontmatter `name: hello`, body that prints a minimal greeting (~10 lines)
- `skills/example-single/README.md` — describe the single-skill layout, when to use it instead of multi-skill

**Total new source content**: 5 new files (2 plugin.json, 2 SKILL.md, 1 README), 1 update (existing README), 1 delete (old SKILL.md). The third skill the operator decision called for is the `status` skill under `skills/example/skills/status/`.

### `catalog.toml`

Add one line to `bundle.examples` members:

```toml
[bundle.examples]
members = [
  "skill:example",
  "skill:example-single",  # NEW
  "rule:example",
  "command:example",
  "agent:example",
  "hook:example",
  "mcp:example",
  "lsp:example",
  "monitor:example",
  "output-style:example",
  "theme:example",
]
```

---

## What's deferred (not in this commit)

Explicit list — these are NOT TO BE DONE in this PR:

1. Per-skill mirror flattening in `AgentsPlatform.emit`, `GeminiPlatform.emit`, `WindsurfPlatform.emit`, `DevinPlatform.emit` — the current `shutil.copytree` produces a nested mirror under multi-skill source layouts that downstream platforms may not discover. Acknowledged debt; tagged with NOTE comments per step 5 above.
2. `CursorPlatform.build_plugin_json` reading source plugin.json — currently hardcodes `"skills": "./"`; under multi-skill source layouts this produces a wrong manifest. Acknowledged debt; tagged with NOTE comment.
3. Empirical Docker verification on Cursor / Codex / Gemini / Windsurf / Devin / `.agents/` shim — all deferred to roadmap items #9-#14 (the platform QA cycles).
4. Layout-detection logic extended to other dir-scan constructs (command, agent, output-style, theme) — even though Claude's spec supports multi-instance for these too, our generator stays single-instance per plugin for now. Documented as available capability in CONTRIBUTING but not exercised by the example set.

---

## ROADMAP updates

Add follow-up tasks (one per non-Claude platform) under "Infrastructure follow-ups":

| # | Task | Status |
|---|---|---|
| 37 | Verify Cursor IDE consumes multi-skill source layouts correctly; fix `CursorPlatform.build_plugin_json` to read source plugin.json `skills` field | `[BLOCKED]` blocker: roadmap #9 (Cursor IDE QA cycle) |
| 38 | Verify Codex consumes multi-skill source layouts correctly | `[BLOCKED]` blocker: roadmap #10 |
| 39 | Per-skill mirror flattening in Gemini (`scripts/platforms.py` GeminiPlatform.emit) | `[BLOCKED]` blocker: roadmap #11 |
| 40 | Per-skill mirror flattening in Windsurf | `[BLOCKED]` blocker: roadmap #12 |
| 41 | Per-skill mirror flattening in Devin | `[BLOCKED]` blocker: roadmap #13 |
| 42 | Per-skill mirror flattening in `.agents/` shim (consumed by Cursor CLI + Windsurf + Devin) | `[BLOCKED]` blocker: roadmap #14 |

---

## Doc changes

### Active docs to update (full or major-section rewrite)

| File | Change |
|---|---|
| `docs/ADDING_A_CONSTRUCT.md` | Rewrite "Trace each fragment to its source" under the new model (the slash form is `/dgxsparklabs-skill-<plugin>:<skill-name>`). Add the three-recipe section (Pattern 1 solo, Pattern 2 multi, Pattern 3 catalog). Drop the Path A shared-namespace explanation. Address the 4 onboarding gaps the fresh-eyes review flagged: brand-prefix-without-typos hint, plugin-vs-component decision tree, allowed-tools guidance, description-fields distinction. |
| `docs/TEST_YOURSELF.md` | Update Claude reference card under new model. Replace `/dgxsparklabs-skill:lab-notebook` with `/dgxsparklabs-skill-example:notebook` + `/dgxsparklabs-skill-example:status`. Add cell for `skill-example-single`. Mark non-Claude per-construct cells as "(unverified under multi-instance source layouts — see ROADMAP #37-#42)." |
| `docs/USER_GUIDE.md` | Update slash-command namespacing table. Update bundle section for 11-entry count. |
| `docs/PLATFORMS.md` | Add top-of-doc banner: "Non-Claude platforms in active QA cycles; multi-instance source layouts unverified outside Claude." Pointer to roadmap follow-ups. |
| `docs/CONSTRUCT_TYPES.md` | Add note: skill is multi-instance-capable per plugin; other dir-scan constructs (command, agent, output-style, theme) support multi-instance in Claude's spec but our generator stays single-instance until needed. |
| `README.md` | Update quick-start; add jq-filter browse command + simpler `grep` fallback. Update install count to 11 plugin entries. |
| `docs/RESUME_HERE.md` | Plugin-naming section updated for new pattern. |
| `CHANGELOG.md` | Entry titled "Skills: multi-instance-capable plugin layout (Claude-only scope); revert Path A; pause cross-platform verification until QA cycles." |
| `skills/example/README.md` | Rewrite for the two-skill multi-instance demonstration. |
| `skills/example-single/README.md` | NEW — describe single-skill layout, when to choose it. |

### README quick-start (drop into `README.md`)

```markdown
## Quick Start — Claude Code

Register the marketplace and install. The bundle-examples plugin auto-installs every reference example (one per construct type, plus the two skill examples):

    claude plugin marketplace add DgxSparkLabs/marketplace
    claude plugin install bundle-examples@dgxsparklabs-marketplace --scope project

Or install one at a time. Install + enable are SEPARATE steps:

    claude plugin install skill-example@dgxsparklabs-marketplace --scope project
    claude plugin enable  skill-example@dgxsparklabs-marketplace

(If you skip enable, Claude says "Plugin not found in any editable settings scope.")

Browse what's installable, filtered to this marketplace:

    claude plugin list --available | grep dgxsparklabs

For machine-readable output use jq:

    claude plugin list --json --available \
      | jq --arg mp "dgxsparklabs-marketplace" \
           '[.. | objects | select(.marketplaceName? == $mp)]'

Invoke. Every plugin's slash form follows the pattern `/dgxsparklabs-<construct>-<plugin>:<component>`:

| Installed plugin | Slash form | What it does |
|---|---|---|
| `skill-example` | `/dgxsparklabs-skill-example:notebook` | Today's lab-notebook header |
| `skill-example` | `/dgxsparklabs-skill-example:status` | Disk usage + UTC timestamp |
| `skill-example-single` | `/dgxsparklabs-skill-example-single:hello` | Minimal greeting |
| `command-example` | `/dgxsparklabs-command-example:hello` | Formatted lab-notebook entry |
| `agent-example` | `/agents` → pick `dgxsparklabs-agent-example:notebook-reviewer` | Sub-agent: skeptical peer review |
| `output-style-example` | `/output-style Lab Notebook Voice` | Switch reply voice |
| `theme-example` | `/theme Lab Notebook` | Switch terminal colors |

Skills have a flat-form shortcut: just `/notebook`, `/status`, or `/hello` — Claude resolves them through the same namespace. Use the qualified form when autocomplete is ambiguous.
```

### CONTRIBUTING quick-start (drop into `docs/ADDING_A_CONSTRUCT.md`)

```markdown
## Quick Start — adding a new plugin

Three patterns. Pick one.

### Pattern 1 — solo skill (or command, agent, etc.)

For a one-off skill that doesn't belong with thematic siblings.

    mkdir -p skills/my-thing/.claude-plugin

    cat > skills/my-thing/.claude-plugin/plugin.json <<EOF
    { "name": "dgxsparklabs-skill-my-thing",
      "description": "One-line description for the marketplace listing." }
    EOF

    cat > skills/my-thing/SKILL.md <<EOF
    ---
    name: do-the-thing
    description: One-line tooltip shown in the slash autocomplete dropdown.
    allowed-tools: [Bash, Read]
    ---
    Body of the skill prompt. Use \$ARGUMENTS for the user's input.
    EOF

    uv run scripts/generate_manifest.py
    uv run tests/test_marketplace.py

Slash form: `/dgxsparklabs-skill-my-thing:do-the-thing`. Bare flat form: `/do-the-thing`.

### Pattern 2 — multi-instance plugin

For multiple skills under one theme.

    mkdir -p skills/git-helpers/{.claude-plugin,skills/{quick-commit,branch-summary,safe-rebase}}

    cat > skills/git-helpers/.claude-plugin/plugin.json <<EOF
    { "name": "dgxsparklabs-skill-git-helpers",
      "description": "Three skills for fast, safe git workflows." }
    EOF

    cat > skills/git-helpers/skills/quick-commit/SKILL.md <<EOF
    ---
    name: quick-commit
    description: Stage modified files and commit with a one-line message.
    allowed-tools: [Bash]
    ---
    Read git status, compose a conventional commit message, stage, commit.
    EOF
    # ... repeat for branch-summary and safe-rebase

    uv run scripts/generate_manifest.py

The plugin name is the CATEGORY (`git-helpers`); skill names are ACTIONS (`quick-commit`, `branch-summary`, `safe-rebase`). One install brings all three.

### Pattern 3 — catalog bundle

For grouping plugins of DIFFERENT construct types.

    # Edit catalog.toml directly; bundles are dep-only, no source dir needed

    cat >> catalog.toml <<'EOF'

    [bundle.onboarding-pack]
    description = "Skill, hook, and rule a new contributor should install first."
    members = [
      "skill:welcome-tour",
      "hook:new-prompt-helper",
      "rule:onboarding-guidance",
    ]
    EOF

    uv run scripts/generate_manifest.py

Plugin name: `bundle-onboarding-pack`. Install with one command, Claude auto-installs all members.

### Decision tree

```
Are you grouping multiple ACTIONS of one construct type under a theme?
  └─ YES → Pattern 2 (multi-instance plugin)

Are you grouping plugins across DIFFERENT construct types?
  └─ YES → Pattern 3 (catalog bundle)

Otherwise:
  └─ Pattern 1 (solo plugin)
```

### Naming rules

1. **Plugin directory name** (`my-thing` in Pattern 1) = kebab-case, semantic, describes the CATEGORY. The brand prefix `dgxsparklabs-skill-` is added automatically by the generator — do not include it in the directory name.
2. **Component name** in frontmatter (`do-the-thing`) = kebab-case verb or noun describing the SPECIFIC ACTION. Don't repeat the plugin name (avoid `/skill-git-helpers:git-commit`; use `:commit`).
3. **Don't typo the brand prefix** — copy from any existing plugin's `.claude-plugin/plugin.json`. The prefix is always derived from `MARKETPLACE.toml` with `-marketplace` stripped.

### Two description fields, two destinations

- `<plugin>/.claude-plugin/plugin.json` `description` → shown in the marketplace listing (`claude plugin list --available`)
- `SKILL.md` frontmatter `description` → shown in Claude's slash autocomplete tooltip

### Test + commit

    uv run scripts/generate_manifest.py
    uv run tests/test_marketplace.py
    uv run tests/test_schema_fitness.py

    git add . && git commit -m "feat(skill-<plugin>): <one-line>"

Never include AI co-author attribution in commit messages (rules/no-ai-credit/).
```

---

## Verification recipe

1. **Generator**:
   ```bash
   uv run scripts/generate_manifest.py
   ```
   Must produce drift-clean output (`scripts/generate_manifest.py --check` exits 0).

2. **Tests**:
   ```bash
   uv run tests/test_marketplace.py
   uv run tests/test_schema_fitness.py
   ```
   Both green. 77+ marketplace tests, 21 schema-fitness tests.

3. **Empirical Claude verification** (hermetic Docker):
   ```bash
   docker run --rm -d --name claude-stub \
     -v "$PWD/.stub-logs:/var/log/stub" claude-stub
   docker run --rm -it --name qa-claude \
     --network container:claude-stub \
     -v "$PWD:/workspace/marketplace" -w /workspace/marketplace \
     -e ANTHROPIC_BASE_URL=http://127.0.0.1:8089 \
     -e ANTHROPIC_AUTH_TOKEN=stub \
     node:20 bash
   ```
   Inside qa-claude:
   ```bash
   npm install -g @anthropic-ai/claude-code
   curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH="$HOME/.local/bin:$PATH"

   claude plugin marketplace add /workspace/marketplace
   claude plugin install skill-example@dgxsparklabs-marketplace --scope project
   claude plugin enable  skill-example@dgxsparklabs-marketplace
   claude plugin install skill-example-single@dgxsparklabs-marketplace --scope project
   claude plugin enable  skill-example-single@dgxsparklabs-marketplace

   echo "/dgxsparklabs-skill-example:notebook" | claude --print
   echo "/dgxsparklabs-skill-example:status"   | claude --print
   echo "/dgxsparklabs-skill-example-single:hello" | claude --print
   ```
   Then on host:
   ```bash
   grep -F "dgxsparklabs-skill-example:notebook" .stub-logs/stub-bodies.log
   grep -F "dgxsparklabs-skill-example:status"   .stub-logs/stub-bodies.log
   grep -F "dgxsparklabs-skill-example-single:hello" .stub-logs/stub-bodies.log
   ```
   All three greps must match.

4. **Per-plugin details query** (regression check for Path A's collapse fix):
   ```bash
   claude plugin details dgxsparklabs-skill-example
   ```
   Must list BOTH `notebook` AND `status` as components. (Under Path A this collapsed to one.)

5. **Non-Claude verification** — **EXPLICITLY DEFERRED**. Do not block this PR on Cursor / Codex / Gemini / Windsurf / Devin verification. Those land in their own QA cycles per ROADMAP #9-#14.

---

## Rollout

One commit on PR #10:

`refactor(skills): multi-instance-capable layout (Claude-only); revert Path A; pause non-Claude verification`

Contains:
- Code: `_base_plugin_shape` f-string flip; `SkillConstruct.build_plugin_json` layout-detection branch; `_read_source_plugin_description` helper in utils
- Comments: NOTE tags on 6 non-Claude `emit()`/`build_plugin_json()` methods in `scripts/platforms.py`
- Source content: `skills/example/` reorganized to multi-skill (notebook + status); NEW `skills/example-single/` (hello)
- Catalog: `bundle.examples` adds `skill:example-single` member
- Tests: rename + update `test_individual_plugin_name_is_unique_brand_namespace`; new `test_skill_plugin_layouts`; new `test_mcp_server_keys_unique_across_plugins`; marketplace-count formula updated
- Regenerated `_generated/` outputs
- Doc cascade (10 files updated per "Active docs to update" table above)
- ROADMAP: 6 new follow-up tasks (#37-#42) for per-platform multi-instance verification

CHANGELOG entry must explicitly state:
- What's verified (Claude path; hermetic stub PASSES on all three slash invocations)
- What's paused (the 5 non-Claude platforms; emission continues, correctness unverified)
- Where the follow-up is tracked (ROADMAP #9-#14 platform QA cycles → #37-#42 per-platform fixes)

After this commit lands, PR #10 (13 commits total) is ready to merge.
