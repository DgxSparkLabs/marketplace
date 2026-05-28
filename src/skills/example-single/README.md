# skill-example-single

A working reference plugin demonstrating the **single-skill (solo) layout** for the skill construct. One plugin ships exactly one skill (`hello`) via a `SKILL.md` at the plugin root — no `skills/` subdir. Copy this directory to scaffold a one-off skill that doesn't belong with thematic siblings.

## What it does

After install + enable, the plugin exposes one slash command:

```
/dgxsparklabs-skill-example-single:hello
```

The bare flat form `/hello` also resolves.

## Install

```
claude plugin install skill-example-single@dgxsparklabs-marketplace --scope project
claude plugin enable  skill-example-single@dgxsparklabs-marketplace
```

## File-by-file walkthrough

```
skills/example-single/
├── .claude-plugin/
│   └── plugin.json   ← plugin manifest; name "dgxsparklabs-skill-example-single"
├── SKILL.md          ← the single skill (frontmatter name: hello, body is the skill prompt)
└── README.md         ← you are here
```

The generator detects "no `skills/` subdir + one root `SKILL.md`" and emits `skills: ["./"]` in the generated `plugin.json`. The multi-skill counterpart at `skills/example/` (with two SKILL.md files under `skills/<name>/`) emits `skills: ["./skills/"]` instead.

## When to choose this layout

- Your plugin ships **exactly one skill**.
- The skill is a one-off, not part of a thematic group (no obvious sibling skills you'd want to add later).
- You want the leanest possible source layout.

Pick the multi-skill layout (see `skills/example/`) instead when you have two-plus related skills that ship together — that way one `claude plugin install` lands them all.

## To make your own single-skill plugin from this template

1. Copy this directory: `cp -r skills/example-single skills/<your-plugin>`
2. Edit `.claude-plugin/plugin.json` — replace `dgxsparklabs-skill-example-single` with `dgxsparklabs-skill-<your-plugin>` and rewrite the description.
3. Edit `SKILL.md` — update frontmatter (`name`, `description`, `allowed-tools`) and rewrite the body.
4. Optionally add to a `[bundle.*]` in `catalog.toml`.
5. `uv run scripts/generate_manifest.py`
6. `uv run tests/test_marketplace.py`
7. Commit.

## Related

- The multi-skill counterpart: `skills/example/`
- Full naming convention + the three contributor patterns: `docs/ADDING_A_CONSTRUCT.md`
