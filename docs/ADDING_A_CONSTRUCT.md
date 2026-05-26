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

3. **Add to a bundle in `catalog.toml`** (existing or new):
   ```toml
   [bundle.my-domain-skills]
   description = "My domain skills"
   members = ["skill:my-skill", "skill:existing-skill"]
   ```
   The plugin also automatically appears in the code-generated `bundle-<prefix>-all` catch-all.

4. **Regenerate**:
   ```bash
   uv run scripts/generate_manifest.py
   ```
   This creates `_generated/<prefix>-<your-name>/`, adds the entry to `.claude-plugin/marketplace.json`, and updates all cross-platform mirrors.

5. **Test**:
   ```bash
   uv run tests/test_marketplace.py
   uv run tests/test_schema_fitness.py
   ```

6. **Validate**: run `claude plugin validate _generated/<your-prefix>-<your-name>` for your new plugin and `claude plugin validate ./` for the marketplace as a whole. Both must produce zero warnings — CI gates on this. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md#running-claude-plugin-validate) for the full validate workflow, common warnings, and how the CI gate is wired.

7. **Commit** with a conventional commit message. No AI co-author attribution (`rules/no-ai-credit/`).

## Naming convention for slash command invocations

Three distinct layers participate in every install command and every slash invocation. Understanding which layer owns which segment of a name prevents the awkward duplication that the `2026-05-26` minimal-stable-state refactor cleaned up.

### The three layers

| Layer            | Owner                          | Example                          | Where it appears                                    |
|------------------|--------------------------------|----------------------------------|-----------------------------------------------------|
| **Marketplace**  | `MARKETPLACE.toml` `name` field| `dgxsparklabs-marketplace`       | The `@<marketplace>` suffix in install commands     |
| **Plugin**       | Source dir + construct prefix  | `command-example`                | The `<plugin-name>` half of slash namespacing       |
| **Component**    | File inside the plugin         | `hello` (from `commands/hello.md`)| The `<component>` half after the `:`               |

Put together, the install command is `/plugin install <plugin>@<marketplace>` and the invocation is `/<plugin>:<component>`. For the reference example: install is `/plugin install command-example@dgxsparklabs-marketplace`; invocation is `/command-example:hello`.

Per [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) (fetched 2026-05-26): *"Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name."* There is no flatten mechanism — the only lever is the plugin name. The component half is always derived from the file name (commands, output styles, themes) or the frontmatter `name` field (skills, agents).

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

**Reserved names**: `<prefix>-all` (e.g., `skill-all`, `rule-all`) are code-generated catch-all bundles and cannot be declared in `catalog.toml`. The generator owns these names.

## Install path after merge

```bash
# Individual plugin
/plugin install <prefix>-<your-name>@dgxsparklabs-marketplace

# Via a domain bundle
/plugin install bundle-<domain>-skills@dgxsparklabs-marketplace

# Via the catch-all (install everything of one construct type)
/plugin install bundle-<prefix>-all@dgxsparklabs-marketplace
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
