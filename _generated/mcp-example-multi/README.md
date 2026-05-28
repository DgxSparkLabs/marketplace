# mcp-example-multi

Reference plugin demonstrating the **multi-server MCP layout**: one plugin ships three MCP servers (`fetch`, `sequential-thinking`, `filesystem`) in one `mcp-config.json`.

## Tool form

Each server's tools surface in Claude as `mcp__dgxsparklabs-mcp-example-multi__<server>__<tool>`. The three servers above are illustrative — each maps to a canonical upstream MCP package.

## When to choose multi over single

Pick multi when you have multiple MCP servers you want to ship as one plugin (often a toolbox theme). Pick single (`src/mcp-servers/example-single/`) when you have exactly one server.

## File walkthrough

```
src/mcp-servers/example-multi/
├── .claude-plugin/plugin.json    ← `mcpServers` field points at the config file
├── mcp-config.json               ← top-level `mcpServers` map with one entry per server
└── README.md
```

## Cross-plugin server-key collisions

Two MCP plugins both defining a server keyed `fetch` would shadow each other in Claude's tool list. The test `test_mcp_server_keys_unique_across_plugins` catches this; prefer plugin-scoped keys when adding your own (e.g. `git-helpers-fetch`).

## Related

- Single counterpart: `src/mcp-servers/example-single/`
- Adding your own MCP plugin: `docs/ADDING_A_CONSTRUCT.md`
