# Adding a Skill

Skills are on-demand domain expertise invoked via slash command. Examples in this marketplace include `skill-telegram-notify`, `skill-github-search`, `skill-web-scraper`.

For the file-by-file walkthrough of skill structure, read [`skills/example-skill/README.md`](../skills/example-skill/README.md).

## Workflow

1. **Copy the example** as your starting template:
   ```bash
   cp -r skills/example-skill skills/my-skill
   ```
   `my-skill` must be kebab-case.

2. **Edit the skill's content**:
   - `skills/my-skill/SKILL.md` — replace frontmatter (`name`, `description`, `argument-hint`, `allowed-tools`) and the body with your skill's instructions
   - Add `scripts/`, `references/`, `setup.sh` etc. if your skill needs them. Python scripts must use PEP 723 inline metadata and run via `uv run`.

3. **Delete the example plugin.json wrapper** — your skill lives in `skills/`, not `examples/`. The generator will create the wrapper for you in `_generated/skill-my-skill/`.
   ```bash
   rm -rf skills/my-skill/.claude-plugin
   rm skills/my-skill/README.md   # optional — keep if your skill needs human-facing docs beyond SKILL.md
   ```

4. **Add to a domain in `catalog.toml`**:
   ```toml
   [skill_domain.<domain>]
   # ... existing members ...
   members = [..., "my-skill"]
   ```
   The skill becomes part of the corresponding `skills-<domain>` bundle.

5. **Regenerate manifests and mirrors**:
   ```bash
   uv run scripts/generate_manifest.py
   ```
   This creates `_generated/skill-my-skill/` (the wrapper plugin), adds an entry to `.claude-plugin/marketplace.json`, and copies the skill into `.codex/skills/`, `.gemini/skills/`, `.devin/skills/`.

6. **Validate**:
   ```bash
   uv run tests/test_marketplace.py
   claude plugin validate _generated/skill-my-skill
   ```

7. **Commit** with an atomic message describing what the skill does. Do not include AI co-author attribution.

## Install path after merge

```
/plugin install skill-my-skill@dgxsparklabs-marketplace
```

Or via a bundle that includes it:

```
/plugin install skills-<domain>@dgxsparklabs-marketplace
```

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md) — index of all construct types
- [`SKILL_FORMAT.md`](./SKILL_FORMAT.md) — full SKILL.md spec (frontmatter fields, allowed-tools, triggers)
- [`ADDING_A_DOMAIN_BUNDLE.md`](./ADDING_A_DOMAIN_BUNDLE.md) — how domain tagging produces bundles
