# Adding an MCP Server

MCP servers expose tools, resources, and prompts to Claude over the Model Context Protocol. Use them for stateful services (database, API session, headless browser, search index).

For the file structure, read [`mcp-servers/example-mcp/README.md`](../mcp-servers/example-mcp/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   cp -r mcp-servers/example-mcp mcp-servers/my-mcp
   ```

2. **Edit**:
   - `mcp-servers/my-mcp/.claude-plugin/plugin.json` — set `name` to `mcp-my-mcp`.
   - `mcp-servers/my-mcp/mcp-config.json` — declare the MCP server(s) under the `mcpServers` object. Each server has `command`, `args`, and optionally `env`.

3. **Test the MCP server standalone** before installing — `uvx your-server`, `npx your-server`, etc. should start and speak MCP over stdio.

4. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate mcp-servers/my-mcp
   ```

5. **Commit**.

## Wrapping an existing MCP server

Most MCP plugins wrap an existing server published to PyPI or npm. The `command`/`args` just invoke it:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uvx",
      "args": ["the-server-package"]
    }
  }
}
```

This avoids needing to maintain your own MCP server code.

## Install path after merge

```
/plugin install mcp-my-mcp@dgxsparklabs-marketplace
```

Tools provided by the server become available as `mcp__my-server__<tool-name>`.

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [Anthropic MCP documentation](https://docs.anthropic.com/claude/docs/mcp) — protocol spec
- [`mcp-servers/example-mcp/README.md`](../mcp-servers/example-mcp/README.md)
