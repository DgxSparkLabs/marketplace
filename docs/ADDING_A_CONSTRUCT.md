# Adding a New Plugin (Skill, Rule, Command, ...)

The marketplace supports 10 plugin construct types. The contribution workflow is identical for each — copy the example, edit the content, add to a bundle, regenerate, test, commit.

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

### The three layers — using `skill-example` / `lab-notebook` as the walked example

| Layer | Owner | How `skill-example` was made | How `lab-notebook` was made |
|---|---|---|---|
| **Marketplace name** | `MARKETPLACE.toml` `name = "dgxsparklabs-marketplace"` | — (this is the suffix `@dgxsparklabs-marketplace`, fixed for the whole repo) | — |
| **Plugin name** | The generator builds it as `<construct-prefix>-<source-dir-name>` | Construct prefix `skill` (defined in `scripts/constructs.py:SkillConstruct.prefix`) + source dir name `example` (from `skills/example/`). Yields `skill-example`. The generator overwrites the source `plugin.json` `name` field at emission so the cached plugin.json always matches. | — |
| **Component name** | The construct's content file | — | Skill `name:` field in `skills/example/SKILL.md` frontmatter. Operator-controlled — write whatever kebab-case word you want. For agents it's the frontmatter `name:` in `agents/<name>.md`; for commands it's the bare filename (e.g., `hello.md` → component `hello`); for MCP it's the server key in `mcp-config.json`. |

So when you run:

```bash
claude plugin install skill-example@dgxsparklabs-marketplace
```

The CLI looks up `skill-example` in the marketplace's `plugins[]` array, finds the source, installs it. Then in a Claude session:

```text
/skill-example:lab-notebook weather
```

`skill-example` resolves to the plugin's namespace (set by the generator from the source dir + prefix); `lab-notebook` resolves to the component (set by the SKILL.md frontmatter); `weather` is `$ARGUMENTS`.

### What this means when you add a new skill

You control TWO of the three layers:
- **Plugin name** is implicitly chosen when you pick the directory name. If you create `skills/foo-bar/`, the plugin will be `skill-foo-bar`. To rename later, rename the directory.
- **Component name** is explicit in the file. For a skill, set `name:` in SKILL.md frontmatter. Pick something short and semantic — don't repeat the directory name (avoid `/skill-foo-bar:foo-bar` doubled forms).

Then run `uv run scripts/generate_manifest.py` and Claude can see it.

Per [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) (fetched 2026-05-26): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name."* There is no flatten mechanism — the only lever is the plugin name (i.e., the directory name).

### Trace each fragment to its source — `claude plugin install skill-notify@dgxsparklabs-marketplace` byte by byte

The walked example: you've created `skills/notify/` with `SKILL.md` frontmatter `name: notify`. After `uv run scripts/generate_manifest.py`, the install command above and the invocation `/skill-notify:notify` both work. Every visible fragment maps to exactly one file:line below. `Ctrl+click` (or `git grep`) to follow.

| Fragment of the install/invocation | Defined at (file:line) | What that line does |
|---|---|---|
| `skill-` (the construct prefix) | [`scripts/constructs.py:73`](../scripts/constructs.py) — `prefix = "skill"` inside `class SkillConstruct` | Literal string assigned to the construct class. The other 9 prefixes are at lines 113 (rule), 150 (command), 179 (agent), 209 (hook), 237 (mcp), 264 (lsp), 288 (monitor), 314 (output-style), 338 (theme). |
| `notify` (the directory name half) | The filesystem — `skills/notify/` is a directory you created in step 1 of the contribution workflow above. The generator discovers it via [`scripts/utils.py:33-41`](../scripts/utils.py) — `scan_source_dir(source_dir)` returns `sorted(d.name for d in source_dir.iterdir() if d.is_dir())`. | Any kebab-case subdirectory of `skills/` becomes the second half of the plugin name. No central registry. |
| `skill-notify` (the combined plugin name) | Built at [`scripts/constructs.py:64`](../scripts/constructs.py) — `"name": f"{construct.prefix}-{name}"` inside `_base_plugin_shape`. Phase 1 of the generator wires it into the on-disk dir at [`scripts/generate_manifest.py:138`](../scripts/generate_manifest.py) — `plugin_dir = GENERATED / f"{construct.prefix}-{name}"`, then `:142` calls `construct.build_plugin_json(name)` which threads through `_base_plugin_shape`. | One concatenation, two places. The dir name `_generated/skill-notify/` and the `plugin.json` `name` field MUST agree (they do, because both come from the same f-string). |
| `@` (the separator) | Claude Code's CLI convention — not defined in this repo. Per [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) it's the syntax for scoping a plugin reference to a specific marketplace. | Plain string. The CLI parses `<plugin>@<marketplace>` and looks up the marketplace's plugin list. |
| `dgxsparklabs-marketplace` (the marketplace name) | [`MARKETPLACE.toml:12`](../MARKETPLACE.toml) — `name = "dgxsparklabs-marketplace"`. Read by [`scripts/utils.py:98-100`](../scripts/utils.py) `_marketplace_name()`. Written into `.claude-plugin/marketplace.json` `"name"` field at [`scripts/generate_manifest.py:76`](../scripts/generate_manifest.py) inside `_write_marketplace_json`. | Single source of truth — renaming the marketplace is a single-line edit at `MARKETPLACE.toml:12`. The `display_name` on line 13 is separate UI sugar; the install-time reference uses `name` only. |
| The `name:` field in `skills/notify/SKILL.md` frontmatter (becomes the slash component `notify`) | Written **directly by you** in `skills/notify/SKILL.md` line 2 — e.g., `name: notify`. The generator does NOT touch this field; `SkillConstruct.emit` at [`scripts/constructs.py:85-94`](../scripts/constructs.py) copies the whole SKILL.md verbatim via `shutil.copytree`. At install time Claude Code reads the cached `SKILL.md` and uses the frontmatter `name:` value as the slash component half. | Operator-owned, no generator round-trip. To change `/skill-notify:notify` → `/skill-notify:status`, edit one line in the source SKILL.md and re-run the generator. |

### How the same fragments end up in three separate files

If you want to see the wiring end-to-end without running the generator, here are the **on-disk files the generator produces** and the line in each where every fragment lands:

```
After `uv run scripts/generate_manifest.py` finishes:

  MARKETPLACE.toml:12                              "dgxsparklabs-marketplace"  ← edited by hand
                              │
                              ▼  read by _marketplace_name() at scripts/utils.py:98-100
                              │
  .claude-plugin/marketplace.json
    "name": "dgxsparklabs-marketplace"             ← top-level marketplace identity
    "plugins": [
      {
        "name": "skill-notify",                    ← entry from Phase 1 (scripts/generate_manifest.py:138-145)
        "source": "./_generated/skill-notify",
        "category": "skill",
        "description": "...",                      ← read from SKILL.md frontmatter (scripts/constructs.py:79-80)
        ...
      }
    ]

  _generated/skill-notify/.claude-plugin/plugin.json
    "name": "skill-notify"                         ← written by SkillConstruct.emit at scripts/constructs.py:85-94
                                                     via _base_plugin_shape at scripts/constructs.py:61-67

  _generated/skill-notify/SKILL.md  ← byte-copied from skills/notify/SKILL.md
    ---
    name: notify                                   ← OPERATOR-AUTHORED in skills/notify/SKILL.md line 2
    description: ...
    ---
```

When you run `claude plugin install skill-notify@dgxsparklabs-marketplace`:

1. CLI splits on `@` — left side is the plugin name, right side is the marketplace.
2. CLI looks up `dgxsparklabs-marketplace` in its registered marketplaces (from `claude plugin marketplace add`); finds the path to this repo's `.claude-plugin/marketplace.json`.
3. CLI finds the entry where `plugins[].name == "skill-notify"` and reads `source` (`./_generated/skill-notify`).
4. CLI copies `_generated/skill-notify/` to `~/.claude/plugins/cache/dgxsparklabs-marketplace/skill-notify/<version>/`.
5. After `claude plugin enable skill-notify@dgxsparklabs-marketplace`, the SKILL.md frontmatter `name: notify` becomes a registered skill in Claude's runtime.
6. `/skill-notify:notify` at the prompt resolves to that skill — `skill-notify` is the cached `plugin.json` `name` (Claude's namespace prefix); `notify` is the SKILL.md frontmatter `name`.

If any link in this chain breaks, the symptom changes deterministically:

| Broken link | Symptom |
|---|---|
| `skills/notify/` directory missing | `claude plugin install` errors `Plugin "skill-notify" not found in marketplace` |
| SKILL.md frontmatter `name:` missing or malformed | install succeeds; `/skill-notify:notify` returns `Unknown command` |
| `MARKETPLACE.toml` `name` field renamed mid-flight | `@dgxsparklabs-marketplace` references break across all 10 plugin installs at once |
| `_generated/skill-notify/` deleted (generator not re-run after source edit) | install succeeds against stale source; behavior reflects the prior content |

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
