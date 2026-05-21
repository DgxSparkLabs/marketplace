# Adding an Output Style

Output styles modify Claude's system prompt — adjust voice, format, or behavior. Two modes:

- **User-selectable**: the user picks the style via `/output-style` (default).
- **Force-applied**: set `force-for-plugin: true` in frontmatter to auto-apply whenever the plugin is enabled (Anthropic's official `explanatory-output-style` plugin uses this).

Only **one** force-applied output style can be active at a time. If multiple plugins try, the first loaded wins.

For the file structure, read [`examples/example-output-style/README.md`](../examples/example-output-style/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   mkdir -p output-styles
   cp -r examples/example-output-style output-styles/my-style
   ```

2. **Edit**:
   - `output-styles/my-style/.claude-plugin/plugin.json` — set `name` to `output-style-my-style`.
   - `output-styles/my-style/output-styles/my-style.md` — rename inner file, set `name`, `description`. Add `force-for-plugin: true` if always-applied. Add `keep-coding-instructions: true` to preserve Claude's default code-task behavior alongside your overlay.

3. **Write the style body in markdown** — this becomes part of Claude's system prompt when the style is active. Be specific about voice, format, and constraints.

4. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate output-styles/my-style
   ```

5. **Commit**.

## When to use force-for-plugin

- Team-wide always-on conventions that should apply across all sessions.
- Pairing a style with a domain-specific plugin (e.g., a "scientific writing" plugin that auto-applies a citation-focused output style).

For per-project preferences, use a CLAUDE.md or a rule. Force-applied output styles are best for cross-cutting behavioral conventions that affect *every* response regardless of project.

## Install path after merge

```
/plugin install output-style-my-style@dgxsparklabs-marketplace
```

Then select via `/output-style My Style` — or, if `force-for-plugin: true`, it activates automatically.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`examples/example-output-style/README.md`](../examples/example-output-style/README.md)
