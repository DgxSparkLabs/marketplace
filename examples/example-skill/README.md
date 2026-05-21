# example-skill

A working reference plugin demonstrating the **skill** construct type. Copy this directory and modify to scaffold your own skill plugin.

## What it does

When invoked as `/example-skill <topic>`, it prints a short markdown block tagged as a lab notebook status update.

Install:
```
/plugin install example-skill@marketplace
```

Invoke:
```
/example-skill onboarding
```

## File-by-file walkthrough

```
example-skill/
├── .claude-plugin/
│   └── plugin.json    ← plugin manifest (Claude Code reads this)
├── SKILL.md           ← the skill itself (Claude reads this when invoked)
└── README.md          ← human-facing tutorial (you are here)
```

### `.claude-plugin/plugin.json`

Required for the plugin to be installable via `/plugin install`. Key fields:

- `name` — must match the skill name in `SKILL.md` frontmatter. Must be kebab-case (`lowercase-with-hyphens`).
- `version` — semantic version. Bump when shipping changes.
- `skills: ["./"]` — tells Claude Code that the SKILL.md lives in the same directory as the plugin manifest. For a skill in a subdirectory, use `["./skills"]` or specific paths.
- `author` must be an object `{ "name": "...", "url": "..." }`, not a string.

### `SKILL.md`

The actual skill. The YAML frontmatter declares metadata Claude Code uses to surface the skill in slash-command completions and to scope its tool access:

- `name` and `description` — what users see when typing `/`.
- `argument-hint` — placeholder text shown after the command name.
- `allowed-tools` — restricts which tools the skill can call. Be minimal — only list what the skill genuinely needs. Lists `Bash` (for the timestamp) and `Read` (just because most skills end up reading files; remove if yours doesn't).

The body (everything after the closing `---`) is the prompt Claude sees when the skill fires. Use imperatives: "Compose a block...", "Print it..."

`$ARGUMENTS` is substituted with everything the user typed after the slash command.

## To make your own skill from this template

1. Copy this directory: `cp -r examples/example-skill skills/my-skill`
2. Rename `my-skill` to whatever you want (kebab-case).
3. Edit `.claude-plugin/plugin.json` — update `name`, `description`, `homepage`, `keywords`.
4. Edit `SKILL.md` — replace the frontmatter and body with your skill's content. See `docs/ADDING_A_SKILL.md` for full conventions.
5. Add your skill name to a domain in `catalog.toml` under `[skill_domain.<domain>]`.
6. Run `uv run scripts/generate_manifest.py` to refresh manifests.
7. Commit.

## Related

- Full skill specification: `docs/SKILL_FORMAT.md`
- Other example plugins demonstrating different construct types: `examples/example-*`
- Real skills shipped by this marketplace: `skills/`
