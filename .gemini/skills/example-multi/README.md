# skill-example

A working reference plugin demonstrating the **multi-skill layout** for the skill construct. One plugin ships two skills side-by-side: `notebook` and `status`. Copy this directory and modify to scaffold your own multi-skill plugin.

## What it does

After install + enable, the plugin exposes two slash commands:

| Slash form | What it does |
|---|---|
| `/dgxsparklabs-skill-example:notebook <topic>` | Prints a short markdown block tagged as a lab-notebook status update |
| `/dgxsparklabs-skill-example:status` | Prints `df -h .` for the current directory plus a UTC timestamp |

The bare flat forms `/notebook` and `/status` also resolve.

## Install

```
claude plugin install skill-example@dgxsparklabs-marketplace --scope project
claude plugin enable  skill-example@dgxsparklabs-marketplace
```

Install and enable are SEPARATE steps. If you skip enable, Claude reports "Plugin not found in any editable settings scope."

## File-by-file walkthrough

```
skills/example/
├── .claude-plugin/
│   └── plugin.json          ← plugin manifest; name "dgxsparklabs-skill-example", marketplace description
├── skills/
│   ├── notebook/SKILL.md    ← the "notebook" skill; frontmatter name: notebook
│   └── status/SKILL.md      ← the "status" skill;   frontmatter name: status
└── README.md                ← you are here
```

### `.claude-plugin/plugin.json`

Operator-authored. The generator reads:

- `name` — plugin identifier; must be `dgxsparklabs-skill-example` (kebab-case, `<brand>-<construct.prefix>-<plugin-dir-name>`). Don't typo the brand prefix; copy from any other plugin's plugin.json.
- `description` — the marketplace-listing one-liner shown in `claude plugin list --available`.

The generator overwrites `version` and `author` from `MARKETPLACE.toml`; you can omit those locally.

### `skills/<skill>/SKILL.md`

One SKILL.md per skill, each in its own subdir. The directory name (`notebook`, `status`) does NOT have to match the frontmatter `name:` — but having them match keeps things readable.

Per-skill frontmatter:

- `name` — slash-component suffix. `/dgxsparklabs-skill-example:notebook` ← this `notebook`.
- `description` — slash-autocomplete tooltip (distinct from the plugin-level description above).
- `argument-hint` — placeholder text shown after the command name.
- `allowed-tools` — restricts which tools the skill can call. Be minimal.

The body (everything after the closing `---`) is the prompt Claude runs when the skill fires.

## To make your own multi-skill plugin from this template

1. Copy this directory: `cp -r skills/example skills/<your-plugin>`
2. Edit `.claude-plugin/plugin.json` — replace `dgxsparklabs-skill-example` with `dgxsparklabs-skill-<your-plugin>` and rewrite the description.
3. Rename / add / delete `skills/<skill>/SKILL.md` files as needed. Each child dir needs its own SKILL.md.
4. Add your plugin to a `[bundle.*]` member list in `catalog.toml` (or skip — bundles are optional).
5. `uv run scripts/generate_manifest.py`
6. `uv run tests/test_marketplace.py`
7. Commit.

## Solo (single-skill) layout

If your plugin has only one skill, prefer the **solo layout** instead. See `skills/example-single/` for the canonical example. Both layouts coexist in this marketplace; pick by which fits.

## Related

- Full naming convention + the three contributor patterns (solo, multi-instance, bundle): `docs/ADDING_A_CONSTRUCT.md`
- Other example plugins demonstrating different construct types: `agents/example/`, `commands/example/`, `hooks/example/`, etc.
- The single-skill counterpart: `skills/example-single/`
