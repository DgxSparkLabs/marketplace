# example-command

A working reference plugin demonstrating the **command** construct type. Copy this directory and modify to scaffold your own slash command plugin.

## What it does

When the user types `/example-command`, Claude runs the prompt in `commands/example-command.md` and prints a markdown block tagged as a fresh lab notebook page.

Install:
```
/plugin install example-command@marketplace
```

Invoke:
```
/example-command
```

## File-by-file walkthrough

```
example-command/
├── .claude-plugin/
│   └── plugin.json                 ← plugin manifest
├── commands/
│   └── example-command.md          ← the command itself (filename = command name)
└── README.md                       ← human-facing tutorial (you are here)
```

### `.claude-plugin/plugin.json`

Notable field: `"commands": ["./commands"]`. This tells Claude Code where the command markdown files live within the plugin. The directory name and the command filenames together determine what the user types — `commands/example-command.md` becomes `/example-command`.

### `commands/example-command.md`

The command file is markdown with optional YAML frontmatter:

- `description` — one-line summary shown in the slash-command picker.
- Body — the prompt Claude runs when the command is invoked.

Commands are like one-shot skills with no `name` field (filename serves as the name) and typically no argument hint. Commands are good for short, deterministic tasks; skills are better for multi-step domain expertise.

## Skills vs commands

- **Skill**: longer, supports `allowed-tools`, supports model auto-invocation via the `triggers` field, lives in a directory with its own scripts/references.
- **Command**: short markdown prompt, user-invoked only, simpler to write.

When in doubt, start as a command. Promote to a skill if you find yourself needing tool restrictions, scripts, or rich frontmatter.

## To make your own command from this template

1. Copy this directory: `cp -r examples/example-command commands/my-command`
2. Rename the directory and the command file inside `commands/` to your command name (kebab-case). The filename becomes the slash-command name.
3. Edit `.claude-plugin/plugin.json` — update `name`, `description`, `homepage`.
4. Edit the command markdown file with your command's behavior.
5. Run `uv run scripts/generate_manifest.py` to refresh manifests.
6. Commit.

## Related

- Slash command docs: see Claude Code official documentation
- Other example plugins: `examples/example-*`
- Skill vs. command decision guide: `docs/CONSTRUCT_TYPES.md`
