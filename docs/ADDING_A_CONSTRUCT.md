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
   ```

6. **Commit** with a conventional commit message. No AI co-author attribution (`rules/no-ai-credit/`).

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

**Rules require an extra step** after install (Claude Code limitation — rules aren't installable natively):
```bash
/plugin install rule-my-rule@dgxsparklabs-marketplace
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-my-rule/activate.sh
```

## Architecture context

- `scripts/constructs.py` — the 10 Construct classes. Each knows how to build plugin.json and emit the generated plugin directory.
- `scripts/platforms.py` — the 7 Platform classes (Claude, Codex, Gemini, Cursor, Windsurf, Devin, Agents). Each knows which constructs it mirrors and how.
- `scripts/bundles.py` — Bundle loader/parser for `catalog.toml`.
- `scripts/utils.py` — shared helpers.
- `scripts/generate_manifest.py` — thin orchestrator (~100 lines). Adding a new construct type requires only a new class in `constructs.py` and an entry in `CONSTRUCTS`.
- `catalog.toml` — bundle definitions only. No construct-type config, no platform config.

See [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md) for the full reference table.
