# Adding a Theme

> **Experimental construct.** The plugin.json field is `experimental.themes`, reflecting that the API may change.

Themes ship UI color palettes for Claude Code. Use them to distribute team color schemes or to pair with other plugins (e.g., a theme that complements a specific output style).

For the file structure, read [`themes/example-theme/README.md`](../themes/example-theme/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   cp -r themes/example-theme themes/my-theme
   ```

2. **Edit**:
   - `themes/my-theme/.claude-plugin/plugin.json` — set `name` to `theme-my-theme`.
   - `themes/my-theme/themes/my-theme.json` — declare the color tokens. The schema is in flux; consult Claude Code's latest docs.

3. **Test in your terminal** — check contrast and readability in both light and dark backgrounds.

4. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate themes/my-theme
   ```

5. **Commit**.

## Install path after merge

```
/plugin install theme-my-theme@dgxsparklabs-marketplace
```

Then select via `/theme My Theme`.

## When to use a theme plugin

- Distributing a team color scheme.
- Pairing UI styling with other plugin components.

For personal taste tweaks, the built-in `/theme` picker is usually enough — no plugin needed.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`themes/example-theme/README.md`](../themes/example-theme/README.md)
