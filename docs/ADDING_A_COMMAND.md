# Adding a Command

Commands are custom slash commands. Lighter than skills — single markdown file, user-invoked only.

For the file structure walkthrough, read [`commands/example-command/README.md`](../commands/example-command/README.md).

## Workflow

1. **Copy the example** as your starting template:
   ```bash
   cp -r commands/example-command commands/my-command
   ```

2. **Edit**:
   - `commands/my-command/.claude-plugin/plugin.json` — update `name` to `command-my-command`, `description`, `homepage`.
   - `commands/my-command/commands/my-command.md` — rename the inner file to match your command, write the prompt body in markdown. The filename becomes the slash-command name.

3. **Add to a domain in `catalog.toml`** (when command bundles are added; for now, individual commands install standalone).

4. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate commands/my-command
   ```

5. **Commit**.

## Install path after merge

```
/plugin install command-my-command@dgxsparklabs-marketplace
```

## When to use a command vs. a skill

- **Command**: one-shot prompt, deterministic, no `allowed-tools` restrictions, no model triggers.
- **Skill**: multi-step reasoning, scoped tool access, can be auto-invoked by Claude on contextual match.

When in doubt, start as a command. Promote to a skill if you need tool restrictions or model auto-invocation.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`ADDING_A_SKILL.md`](./ADDING_A_SKILL.md)
