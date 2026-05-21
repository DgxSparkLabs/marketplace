# Adding an Agent

Agents are sub-agent personas with their own system prompt and scoped tool access. Use them when you want Claude to take on a distinct persona for a task (peer reviewer, security auditor, technical writer).

For the file structure, read [`examples/example-agent/README.md`](../examples/example-agent/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   mkdir -p agents
   cp -r examples/example-agent agents/my-agent
   ```

2. **Edit**:
   - `agents/my-agent/.claude-plugin/plugin.json` — set `name` to `agent-my-agent`.
   - `agents/my-agent/agents/my-agent.md` — rename inner file, write the agent's system prompt in the body. Use YAML frontmatter for `name`, `description`, optional `tools` to restrict tool access.

3. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate agents/my-agent
   ```

4. **Commit**.

## Auto-discovery

Claude Code auto-discovers `agents/*.md` files inside any plugin directory. You do **not** need to declare an `agents` field in `plugin.json`. (You can override the default location with `"agents": ["./custom/path"]` if needed.)

## Install path after merge

```
/plugin install agent-my-agent@marketplace
```

Invoke via Claude Code's agent picker or `--agent my-agent`.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- Agent vs. skill vs. command guidance: see [`examples/example-agent/README.md`](../examples/example-agent/README.md)
