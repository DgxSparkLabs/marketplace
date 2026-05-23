# example-rule

A working reference plugin demonstrating the **rule** construct type. Copy this directory and modify to scaffold your own rule plugin.

## What it does

Ships an always-on behavioral rule that gets symlinked into Claude Code's `.claude/rules/` directory. Once activated, the rule's text is loaded into Claude's context at every session start.

Install:
```
/plugin install example-rule@dgxsparklabs-marketplace
```

Then activate (one-time):
```
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/example-rule/activate.sh
```

After that, Claude Code loads the rule automatically every session.

## Why two steps?

Claude Code's `/plugin install` does not natively install rules — there is no `rules` field in `plugin.json`. The workaround is to ship the rule file inside a plugin, then provide an `activate.sh` that symlinks it into `.claude/rules/`. Once symlinked, future plugin updates automatically propagate (the symlink points back into the plugin cache).

See `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` and `docs/PLAN_PLUGIN_COMPLIANCE.md` (the rules architecture section) for the full rationale.

## File-by-file walkthrough

```
example-rule/
├── .claude-plugin/
│   └── plugin.json        ← plugin manifest (Claude Code reads this)
├── rules/
│   └── example-rule.md    ← the actual rule body (symlinked into .claude/rules/)
├── activate.sh            ← one-shot helper that creates the symlink
└── README.md              ← human-facing tutorial (you are here)
```

### `.claude-plugin/plugin.json`

A minimal manifest. Notably **no `skills`, `commands`, `agents`, or other component fields** — the rule content is loaded via the `.claude/rules/` symlink, not via any plugin auto-discovery.

### `rules/example-rule.md`

The actual rule. Plain markdown. Short, imperative, focused on one behavior. The filename you choose here becomes the filename in `.claude/rules/` after activation.

### `activate.sh`

A small shell script that symlinks every `*.md` file in `rules/` into the target rules directory (`.claude/rules/` by default). Symlinks (not copies) so future plugin updates propagate.

If the project does not yet have `.claude/rules/`, the script creates it.

To activate into a different location (e.g., user-global rules at `~/.claude/rules/`):
```
bash activate.sh ~/.claude/rules
```

## To make your own rule from this template

1. Copy this directory: `cp -r examples/example-rule rules/my-rule`
2. Rename `my-rule` to whatever you want (kebab-case).
3. Edit `.claude-plugin/plugin.json` — update `name`, `description`, `homepage`, `keywords`.
4. Replace `rules/example-rule.md` with your rule body. Filename should match your rule name.
5. `activate.sh` does not need changes — it globs `*.md` from the `rules/` subdirectory.
6. Add your rule name to a domain in `catalog.toml` under `[rule_domain.<domain>]`.
7. Run `uv run scripts/generate_manifest.py` to refresh manifests.
8. Commit.

## Related

- Full rule format reference: `docs/RULE_FORMAT.md`
- Investigation of rule installation alternatives: `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`
- Other example plugins: `examples/example-*`
- Real rules shipped by this marketplace: `rules/`
- Repo-root bulk activator: `activate-installed-rules.sh` (symlinks every installed rule plugin's rules at once)
