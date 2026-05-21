# Adding a Rule

Rules are always-on behavioral guidelines loaded into every Claude session via `.claude/rules/`. Examples in this marketplace include `rule-blast-radius`, `rule-verify-your-work`, `rule-no-ai-credit`.

For the architectural rationale (why rules need a manual `activate.sh` step), see [`INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./INVESTIGATION_PLUGIN_DEPENDENCIES.md). For the file structure walkthrough, see [`examples/example-rule/README.md`](../examples/example-rule/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   cp -r examples/example-rule rules/my-rule
   ```

2. **Edit the rule body**:
   - `rules/my-rule/rule.md` — the actual rule text. Short, imperative, focused on one behavior. Keep it under ~200 lines so it doesn't bloat every session's context.
   - `rules/my-rule/README.md` — human-facing docs for the rule (what it enforces, when to use, examples).
   - `rules/my-rule/formats/cursor.md` and `rules/my-rule/formats/windsurf.md` — platform-specific rule formats for the cross-platform mirrors. Templates exist in any existing `rules/*/formats/` directory.

3. **Delete the example plugin.json and activate.sh wrappers** — your rule lives in `rules/`, not `examples/`. The generator will create the wrapper for you in `_generated/rule-my-rule/`.
   ```bash
   rm -rf rules/my-rule/.claude-plugin
   rm rules/my-rule/activate.sh
   ```

4. **Add to a domain in `catalog.toml`**:
   ```toml
   [rule_domain.<domain>]
   members = [..., "my-rule"]
   ```
   The rule becomes part of the corresponding `rules-<domain>` bundle and the `rules-all` catch-all.

5. **Regenerate manifests and mirrors**:
   ```bash
   uv run scripts/generate_manifest.py
   ```
   This creates `_generated/rule-my-rule/` with its own `activate.sh`, adds entries to `.claude-plugin/marketplace.json`, and copies the rule into `.cursor/rules/`, `.windsurf/rules/`, `.devin/rules/` using the platform-specific format files.

6. **Validate**:
   ```bash
   uv run tests/test_marketplace.py
   ```

7. **Commit**.

## Install path after merge

```bash
/plugin install rule-my-rule@marketplace
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-my-rule/activate.sh
```

Or via a bundle:

```bash
/plugin install rules-<domain>@marketplace
# Then symlink each rule (or use the repo-root bulk helper)
bash ~/.local/share/marketplace/activate-installed-rules.sh
```

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`RULE_FORMAT.md`](./RULE_FORMAT.md) — rule body spec + platform-specific format file conventions
- [`INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./INVESTIGATION_PLUGIN_DEPENDENCIES.md) — why the activate.sh step exists
- [`ADDING_A_DOMAIN_BUNDLE.md`](./ADDING_A_DOMAIN_BUNDLE.md)
