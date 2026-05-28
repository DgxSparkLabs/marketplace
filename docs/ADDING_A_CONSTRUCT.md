# Adding a New Plugin (Skill, Rule, Command, ...)

The marketplace supports 10 plugin construct types. The contribution workflow is identical for each — copy the example, edit the content, add to a bundle, regenerate, test, commit.

## Quick start — three patterns, pick one

### Pattern 1 — solo skill (or command, agent, etc.)

For a one-off skill that doesn't belong with thematic siblings.

```bash
mkdir -p src/skills/my-thing/.claude-plugin

cat > src/skills/my-thing/.claude-plugin/plugin.json <<'EOF'
{
  "name": "dgxsparklabs-skill-my-thing",
  "description": "One-line description for the marketplace listing."
}
EOF

cat > src/skills/my-thing/SKILL.md <<'EOF'
---
name: do-the-thing
description: One-line tooltip shown in the slash autocomplete dropdown.
allowed-tools: [Bash, Read]
---
Body of the skill prompt. Use $ARGUMENTS for the user's input.
EOF

uv run scripts/generate_manifest.py
uv run tests/test_marketplace.py
```

Slash form: `/dgxsparklabs-skill-my-thing:do-the-thing`. Bare flat form: `/do-the-thing`.

Canonical reference: [`src/skills/example-single/`](../src/skills/example-single/).

### Pattern 2 — multi-instance plugin

For multiple skills under one theme. One install brings all of them.

```bash
mkdir -p src/skills/git-helpers/{.claude-plugin,skills/{quick-commit,branch-summary,safe-rebase}}

cat > src/skills/git-helpers/.claude-plugin/plugin.json <<'EOF'
{
  "name": "dgxsparklabs-skill-git-helpers",
  "description": "Three skills for fast, safe git workflows."
}
EOF

cat > src/skills/git-helpers/skills/quick-commit/SKILL.md <<'EOF'
---
name: quick-commit
description: Stage modified files and commit with a one-line message.
allowed-tools: [Bash]
---
Read git status, compose a conventional commit message, stage, commit.
EOF
# ... repeat for branch-summary and safe-rebase

uv run scripts/generate_manifest.py
```

Plugin name is the **category** (`git-helpers`); each child skill name is an **action** (`quick-commit`, `branch-summary`, `safe-rebase`). Slash forms: `/dgxsparklabs-skill-git-helpers:quick-commit`, etc.

Canonical reference: [`src/skills/example-multi/`](../src/skills/example-multi/) (two skills: `notebook`, `status`).

### Pattern 3 — catalog bundle

For grouping plugins of DIFFERENT construct types. Bundles are dep-only: no source dir, just a `catalog.toml` entry.

```bash
cat >> src/catalog.toml <<'EOF'

[bundle.onboarding-pack]
description = "Skill, hook, and rule a new contributor should install first."
members = [
  "skill:welcome-tour",
  "hook:new-prompt-helper",
  "rule:onboarding-guidance",
]
EOF

uv run scripts/generate_manifest.py
```

Plugin name: `bundle-onboarding-pack`. Install with one command — Claude auto-installs all member plugins as dependencies.

Canonical reference: `[bundle.examples]` in [`src/catalog.toml`](../src/catalog.toml).

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
3. **Don't typo the brand prefix.** It is always `<MARKETPLACE.toml name without -marketplace>-<construct.prefix>-<your-plugin>`. Copy from any existing plugin's `.claude-plugin/plugin.json` if you're unsure — if you typo the brand prefix in the source-side plugin.json, the generator will silently override it (the `name` field is computed), but the description will be the only thing read from your file, so a typo in `name` is harmless. The slash form is derived from the GENERATED plugin.json, not the source-side file.

### Two description fields, two destinations

Two distinct concerns, two distinct files. Don't confuse them:

| Field | File | Shown in |
|---|---|---|
| Plugin-level `description` | `<plugin>/.claude-plugin/plugin.json` | Marketplace listing (`claude plugin list --available`) |
| Per-component `description` | `SKILL.md` (or `<cmd>.md`, `<agent>.md`) frontmatter | Claude's slash-autocomplete tooltip |

For Pattern 2 (multi-skill), the plugin-level description summarizes the theme; each per-skill description is the specific action.

For Pattern 1 (solo), it can feel redundant — write a short plugin-level description for the marketplace listing, and a longer per-skill description for the autocomplete tooltip.

### Test + commit

```bash
uv run scripts/generate_manifest.py
uv run tests/test_marketplace.py
uv run tests/test_schema_fitness.py

git add . && git commit -m "feat(skill-<plugin>): <one-line>"
```

Never include AI co-author attribution in commit messages (see [`rules/no-ai-credit/`](../rules/no-ai-credit/)).

---

## Per-construct quick reference

| Construct    | Source folder     | Example template          | Description source       |
|--------------|-------------------|---------------------------|--------------------------|
| skill        | `skills/`         | `skills/example/`         | `SKILL.md` frontmatter   |
| rule         | `rules/`          | `rules/example/`          | (auto-generated)         |
| command      | `commands/`       | `commands/example/`       | `commands/*.md` frontmatter |
| agent        | `agents/`         | `agents/example/`         | `agents/*.md` frontmatter |
| hook         | `hooks/`          | `hooks/example/`          | `hooks/hooks.json`       |
| mcp          | `mcp-servers/`    | `mcp-servers/example/`    | `.claude-plugin/plugin.json` |
| lsp          | `lsp-servers/`    | `lsp-servers/example/`    | `.claude-plugin/plugin.json` |
| monitor      | `monitors/`       | `monitors/example/`       | `.claude-plugin/plugin.json` |
| output-style | `output-styles/`  | `output-styles/example/`  | `.claude-plugin/plugin.json` |
| theme        | `themes/`         | `themes/example/`         | `.claude-plugin/plugin.json` |

## Steps

1. **Copy the example template** for your construct type:
   ```bash
   cp -r <source-folder>/example/ <source-folder>/<your-name>/
   ```
   `<your-name>` must be kebab-case (e.g., `my-skill`, `no-profanity`, `claude-bot`).

2. **Edit the copied content** following the construct's convention:
   - **skill**: Update `SKILL.md` frontmatter (`name`, `description`, `argument-hint`, `allowed-tools`) and the body
   - **rule**: Update `rule.md` with the always-on behavioral guideline
   - **command**: Update `commands/<name>.md` with the slash command
   - **agent**: Update `agents/<name>.md` with the sub-agent persona
   - **hook**: Update `hooks/hooks.json` with event handlers
   - **mcp/lsp/monitor/output-style/theme**: Update `.claude-plugin/plugin.json` + the construct-specific config file

3. **Add to a bundle in `catalog.toml`** (existing or new) — required so the test `test_every_construct_in_at_least_one_bundle` stays green:
   ```toml
   [bundle.my-domain-skills]
   description = "My domain skills"
   members = ["skill:my-skill", "skill:existing-skill"]
   ```
   (Per-construct catch-all bundles like `bundle-skill-all` were retired 2026-05-27 — the catalog is now the only place that groups plugins.)

4. **Regenerate** — this is the one command that makes Claude (or any other platform) see your new plugin:
   ```bash
   uv run scripts/generate_manifest.py
   ```
   It walks `skills/`, `agents/`, ... finds your new dir, builds the per-plugin manifest, adds the entry to `.claude-plugin/marketplace.json`, and updates every cross-platform mirror. Without this step, your new skill is invisible to `claude plugin list --available` even after committing.

5. **Test**:
   ```bash
   uv run tests/test_marketplace.py
   uv run tests/test_schema_fitness.py
   ```

6. **Validate**: run `claude plugin validate _generated/<your-prefix>-<your-name>` for your new plugin and `claude plugin validate ./` for the marketplace as a whole. Both must produce zero warnings — CI gates on this. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md#running-claude-plugin-validate) for the full validate workflow, common warnings, and how the CI gate is wired.

7. **Commit** with a conventional commit message. No AI co-author attribution (`rules/no-ai-credit/`).

## Where do the names come from? (read this if any name surprises you)

Three distinct layers participate in every install command and every slash invocation. **Each layer is owned by a different file, and that's the only thing controlling that segment of the name.**

### The three layers — using `skill-example` / `notebook` as the walked example

| Layer | Owner | How `skill-example` was made | How `notebook` was made |
|---|---|---|---|
| **Marketplace name** | `MARKETPLACE.toml` `name = "dgxsparklabs-marketplace"` | — (this is the suffix `@dgxsparklabs-marketplace`, fixed for the whole repo) | — |
| **Plugin name** | The generator builds it as `<construct.prefix>-<source-dir-name>` | Construct prefix `skill` (defined in `scripts/constructs.py:SkillConstruct.prefix`) + source dir name `example` (from `skills/example/`). Yields `skill-example`. | — |
| **Component name** | The construct's content file | — | Skill `name:` field in `skills/example/skills/notebook/SKILL.md` frontmatter. Operator-controlled — write whatever kebab-case word you want. For agents it's the frontmatter `name:` in `agents/<name>.md`; for commands it's the bare filename (e.g., `hello.md` → component `hello`); for MCP it's the server key in `mcp-config.json`. |

So when you run:

```bash
claude plugin install skill-example@dgxsparklabs-marketplace
```

The CLI looks up `skill-example` in the marketplace's `plugins[]` array, finds the source, installs it. Then in a Claude session:

```text
/dgxsparklabs-skill-example:notebook weather
```

`dgxsparklabs-skill-example` resolves to the plugin's unique slash namespace (set by the generator from `<brand>-<construct.prefix>-<source-dir>`); `notebook` resolves to the component (set by the SKILL.md frontmatter); `weather` is `$ARGUMENTS`.

### What this means when you add a new skill

You control TWO of the three layers:
- **Plugin name** is implicitly chosen when you pick the directory name. If you create `skills/foo-bar/`, the plugin will be `skill-foo-bar` at install time and `/dgxsparklabs-skill-foo-bar:<component>` at slash time. To rename later, rename the directory.
- **Component name** is explicit in the file. For a skill, set `name:` in SKILL.md frontmatter. Pick something short and semantic — don't repeat the directory name (avoid `/dgxsparklabs-skill-foo-bar:foo-bar` doubled forms).

Then run `uv run scripts/generate_manifest.py` and Claude can see it.

Per [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) (fetched 2026-05-26): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name."* There is no flatten mechanism that drops the namespace — Claude rewrites the bare flat form `/hello` to the qualified form internally.

### Trace each fragment to its source — `claude plugin install skill-example@dgxsparklabs-marketplace` byte by byte

The walked example: the marketplace already ships `skills/example/` as a multi-skill plugin (with `skills/notebook/SKILL.md` and `skills/status/SKILL.md` underneath). After `uv run scripts/generate_manifest.py`, the install command above works and the invocations become `/dgxsparklabs-skill-example:notebook` and `/dgxsparklabs-skill-example:status`. Every visible fragment maps to exactly one file:line below. `Ctrl+click` (or `git grep`) to follow.

**Architectural note** (post-2026-05-28): the **install-time name** (`skill-example` in the install command) and the **slash-namespace name** (`dgxsparklabs-skill-example` in the invocation) are two separate fields, but both incorporate the source-directory name and are unique per plugin. An earlier short-lived experiment ("Path A", `d641f92`, 2026-05-27) collapsed multiple plugins of one construct into a shared slash namespace `/dgxsparklabs-skill:` — that was reverted on 2026-05-28 because `claude plugin details` could only show one plugin's components under the shared name. See [`docs/research/multi-instance-claude-only-2026-05-27/PLAN.md`](research/multi-instance-claude-only-2026-05-27/PLAN.md) for the revert rationale.

| Fragment | Defined at | What it does |
|---|---|---|
| `skill-` (the **install** construct prefix) | `scripts/constructs.py` — `prefix = "skill"` inside `class SkillConstruct` | Literal string. Used by the generator to build the `_generated/<plugin>/` directory name and the marketplace.json `plugins[].name` entry. Each of the 10 construct classes has its own `prefix` attribute. |
| `example` (the directory name) | Filesystem — `skills/example/` is the directory. Discovered by `scripts/utils.py` `scan_source_dir`. | Any kebab-case subdir of `skills/` becomes a candidate plugin. No central registry. |
| `skill-example` (install-time plugin name) | Composed in `scripts/generate_manifest.py` — `plugin_dir = GENERATED / f"{construct.prefix}-{name}"`. The directory NAME is what `_make_marketplace_entry` reads via `plugin_dir.name` to populate `marketplace.json` `plugins[].name`. | One f-string. The on-disk dir `_generated/skill-example/` and the marketplace entry `name` are guaranteed to match. |
| `@` (separator) | Claude CLI convention. Per [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins). | Splits `<plugin>@<marketplace>` at install time. |
| `dgxsparklabs-marketplace` (marketplace identity) | `MARKETPLACE.toml` `name = "dgxsparklabs-marketplace"`. Read by `_marketplace_name()` in `scripts/utils.py`. Written into `.claude-plugin/marketplace.json` top-level `"name"` field. | Single source of truth. Renaming the marketplace is one-line edit. |
| `dgxsparklabs-` (the **slash** brand prefix) | Derived in `scripts/constructs.py` `_base_plugin_shape` — `mp_name.removesuffix("-marketplace")` strips the trailing `-marketplace` from MARKETPLACE.toml's `name` to produce `dgxsparklabs`. | One line. To re-brand a fork, change MARKETPLACE.toml and the brand prefix follows automatically. |
| `dgxsparklabs-skill-example` (the unique plugin slash namespace) | Composed at `scripts/constructs.py` `_base_plugin_shape` — `"name": f"{brand}-{construct.prefix}-{name}"`. Written into `_generated/skill-example/.claude-plugin/plugin.json` `"name"` field by `SkillConstruct.emit`. | **One name per plugin** — unique. `claude plugin details dgxsparklabs-skill-example` resolves to this single plugin and lists all of its components. |
| `:` (separator) | Claude convention. Per [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`)."* | Splits `<plugin-json-name>:<skill-name>` at slash-resolution time. |
| `notebook` / `status` (the slash component) | The `name:` field in `skills/example/skills/notebook/SKILL.md` (and `.../status/SKILL.md`) frontmatter — operator-written. `SkillConstruct.emit` copies the SKILL.md files verbatim via `shutil.copytree`. At install time Claude reads each cached SKILL.md and uses the frontmatter `name:` value as the slash component. | Operator-owned, no generator round-trip. To rename `/dgxsparklabs-skill-example:notebook` → `/dgxsparklabs-skill-example:journal`, edit one line in the source SKILL.md and re-run the generator. |

### How the same fragments end up in three separate files

```
After `uv run scripts/generate_manifest.py` finishes:

  MARKETPLACE.toml                                 "dgxsparklabs-marketplace"  ← edited by hand
                              │
                              ▼  read by _marketplace_name() in scripts/utils.py
                              │
        ┌─────────────────────┴─────────────────────┐
        │ used as marketplace identity              │ stripped of "-marketplace" for brand
        ▼                                           ▼
  .claude-plugin/marketplace.json              "dgxsparklabs" (the brand prefix)
    "name": "dgxsparklabs-marketplace"               │
    "plugins": [                                     │ + construct.prefix ("skill") + source-dir-name ("example")
      {                                              ▼
        "name": "skill-example",               "dgxsparklabs-skill-example"
        "source": "./_generated/skill-example",(slash namespace — unique per plugin)
        "category": "skill",                         │
        "description": "...",                        ▼
        ...                                  _generated/skill-example/.claude-plugin/plugin.json
      },                                       "name": "dgxsparklabs-skill-example"
      { "name": "skill-example-single", ... }, "skills": ["./skills/"]
      ...
    ]                                                │
                                                     ▼
                                             _generated/skill-example/skills/notebook/SKILL.md
                                               ---
                                               name: notebook   ← YOU wrote this in skills/example/skills/notebook/SKILL.md:2
                                               description: ...
                                               ---
                                             _generated/skill-example/skills/status/SKILL.md
                                               ---
                                               name: status     ← second skill in the same plugin (multi-skill layout)
                                               description: ...
                                               ---
```

When you run `claude plugin install skill-example@dgxsparklabs-marketplace`:

1. CLI splits on `@` — left side `skill-example` is the plugin name, right side `dgxsparklabs-marketplace` is the marketplace identity.
2. CLI looks up `dgxsparklabs-marketplace` in registered marketplaces (from `claude plugin marketplace add`); finds the path to this repo's `.claude-plugin/marketplace.json`.
3. CLI finds the entry where `plugins[].name == "skill-example"` and reads `source` (`./_generated/skill-example`).
4. CLI copies `_generated/skill-example/` to `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-example/<version>/`.
5. After `claude plugin enable skill-example@dgxsparklabs-marketplace`, the cached `plugin.json` `name: dgxsparklabs-skill-example` registers as the plugin's slash namespace; both SKILL.md files register as components under it (`notebook` and `status`).
6. `/dgxsparklabs-skill-example:notebook` and `/dgxsparklabs-skill-example:status` at the prompt both resolve. The bare flat forms `/notebook` and `/status` also resolve (Claude internally rewrites to the qualified form).

If any link in this chain breaks, the symptom changes deterministically:

| Broken link | Symptom |
|---|---|
| `skills/example/` directory missing | `claude plugin install` errors `Plugin "skill-example" not found in marketplace` |
| SKILL.md frontmatter `name:` missing or malformed | install succeeds; `/dgxsparklabs-skill-example:notebook` returns `Unknown command` |
| `MARKETPLACE.toml` `name` field renamed mid-flight | `@dgxsparklabs-marketplace` references break AND the brand prefix changes for every plugin |
| `_generated/skill-example/` deleted (generator not re-run after source edit) | install succeeds against stale source; behavior reflects the prior content |
| Source plugin BOTH has root SKILL.md AND `skills/<x>/SKILL.md` subdirs | Generator raises `ValueError` from `SkillConstruct.build_plugin_json` — pick one layout |

### The duplication pitfall

If the component file's name repeats the plugin's prefix, the invocation reads twice:

| Plugin            | Component file              | Invocation                                | Verdict           |
|-------------------|-----------------------------|-------------------------------------------|-------------------|
| `command-example` | `commands/example-command.md` | `/command-example:example-command`      | Awkward — `example`/`command` appear twice |
| `command-example` | `commands/hello.md`         | `/command-example:hello`                  | Clean              |
| `skill-telegram-notify` | `SKILL.md` `name: telegram-notify` | `/skill-telegram-notify:telegram-notify` | Awkward     |
| `skill-telegram-notify` | `SKILL.md` `name: notify`         | `/skill-telegram-notify:notify`        | Clean              |

The duplication is invisible at the source-directory level (each layer's name is fine in isolation) and only surfaces in the rendered slash form. Read it aloud as a sanity check.

### Rule of thumb

1. Do not repeat words across the plugin name and the component file name.
2. Pick short, generic names for examples (`hello`, `voice`, `ping`).
3. If the invocation reads awkwardly, rename one of the two — usually the component is easier to rename than the plugin.
4. MCP plugins have an extra layer: the server key inside `mcp-config.json` (our choice) becomes the second namespace segment in the resulting `mcp__<plugin>__<server>__<tool>` invocation. Align it with the plugin name family — e.g., `mcp-example` plugin → server key `example` → tool `mcp__mcp-example__example__fetch`. The underlying npm tool name (`mcp-server-fetch`) is fixed by the external package but only appears in `args`, never in the invocation.

## Adding a new bundle

Bundles are declared in `catalog.toml`. Each bundle is a dep-only plugin that installs a curated set of other plugins.

```toml
[bundle.my-domain-skills]
description = "Skills for my domain"
members = [
  "skill:foo",
  "skill:bar",
  "bundle:existing-bundle",  # bundles can reference other bundles
]
```

Plugin name: `bundle-my-domain-skills@dgxsparklabs-marketplace`.

(Per-construct catch-all bundles like `bundle-skill-all` were retired 2026-05-27. The catalog may now use any name including the old `<prefix>-all` form if you want it back for a specific construct.)

## Install path after merge

```bash
# Individual plugin
/plugin install <prefix>-<your-name>@dgxsparklabs-marketplace

# Via a domain bundle
/plugin install bundle-<domain>-skills@dgxsparklabs-marketplace
```

**Rules are not a Claude plugin component** (per `code.claude.com/docs/en/plugins-reference#plugin-components-reference`, 2026-05-26). For Claude, install rules into the memory subsystem by symlinking or copying into `.claude/rules/`:
```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/my-rule/rule.md" .claude/rules/my-rule.md
# Or copy for portability:
cp rules/my-rule/rule.md .claude/rules/my-rule.md
```
Cursor / Windsurf / Codex / Gemini still install rule plugins via their respective marketplaces — only Claude's plugin path was retired. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

## Architecture context

- `scripts/constructs.py` — the 10 Construct classes. Each knows how to build plugin.json and emit the generated plugin directory.
- `scripts/platforms.py` — the 7 Platform classes (Claude, Codex, Gemini, Cursor, Windsurf, Devin, Agents). Each knows which constructs it mirrors and how.
- `scripts/bundles.py` — Bundle loader/parser for `catalog.toml`.
- `scripts/utils.py` — shared helpers.
- `scripts/generate_manifest.py` — thin orchestrator (~100 lines). Adding a new construct type requires only a new class in `constructs.py` and an entry in `CONSTRUCTS`.
- `catalog.toml` — bundle definitions only. No construct-type config, no platform config.

See [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md) for the full reference table.
