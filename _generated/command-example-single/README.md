# command-example

A working reference plugin demonstrating the **command** construct type. Copy this directory and modify to scaffold your own slash command plugin.

## What it does

When the user types `/command-example:hello`, Claude runs the prompt in `commands/hello.md` and prints a markdown block tagged as a fresh lab notebook page.

Install:
```
/plugin install command-example@dgxsparklabs-marketplace
```

Invoke (Claude namespaces every slash command as `/<plugin-name>:<component-name>`):
```
/command-example:hello
```

See `docs/ADDING_A_CONSTRUCT.md` "Naming convention for slash command invocations" for why the component file is named `hello` rather than `example-command` — the latter doubled the `command-example` plugin prefix and produced the awkward `/command-example:example-command`.

## File-by-file walkthrough

```
command-example/
├── .claude-plugin/
│   └── plugin.json                 ← plugin manifest
├── commands/
│   └── hello.md                    ← the command itself (filename = command name)
└── README.md                       ← human-facing tutorial (you are here)
```

### `.claude-plugin/plugin.json`

Notable field: `"commands": ["./commands"]`. This tells Claude Code where the command markdown files live within the plugin. The directory name and the command filenames together determine what the user types — `commands/hello.md` becomes `/command-example:hello`.

### `commands/hello.md`

The command file is markdown with optional YAML frontmatter:

- `description` — one-line summary shown in the slash-command picker.
- Body — the prompt Claude runs when the command is invoked.

Commands are like one-shot skills with no `name` field (filename serves as the name) and typically no argument hint. Commands are good for short, deterministic tasks; skills are better for multi-step domain expertise.

## Skills vs commands

- **Skill**: longer, supports `allowed-tools`, supports model auto-invocation via the `triggers` field, lives in a directory with its own scripts/references.
- **Command**: short markdown prompt, user-invoked only, simpler to write.

When in doubt, start as a command. Promote to a skill if you find yourself needing tool restrictions, scripts, or rich frontmatter.

## To make your own command from this template

1. Copy this directory: `cp -r commands/example commands/<your-name>`
2. Rename the file(s) inside `commands/` to your command name (kebab-case). The filename becomes the component half of the namespaced invocation (`/command-<your-name>:<filename>`). Pick a short generic name that does not repeat the plugin prefix.
3. Edit `.claude-plugin/plugin.json` — update `name`, `description`, `homepage`.
4. Edit the command markdown file with your command's behavior.
5. Run `uv run scripts/generate_manifest.py` to refresh manifests.
6. Commit.

## Related

- Slash command docs: see Claude Code official documentation
- Other example plugins: `<construct>/example/` (each construct dir has an `example/`)
- Skill vs. command decision guide: `docs/CONSTRUCT_TYPES.md`
