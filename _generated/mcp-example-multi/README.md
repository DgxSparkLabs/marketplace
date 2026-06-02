# mcp-example-multi

Reference plugin demonstrating the **multi-server MCP layout**: one plugin ships three MCP servers (`fetch`, `sequential-thinking`, `filesystem`) in one `mcp-config.json`.

## Tool form

Each server's tools surface in Claude as `mcp__dgxsparklabs-mcp-example-multi__<server>__<tool>`. The three servers above are illustrative — each maps to a canonical upstream MCP package.

## A "debug example" — every server runs behind a logging proxy

Each entry in `mcp-config.json` does **not** launch the upstream server directly.
It launches `mcp_logging_proxy.py` (bundled, stdlib-only, run via `uv run`), which
spawns the real server and **tees the newline-delimited JSON-RPC stream in both
directions** to `${TMPDIR:-/tmp}/mcp_proxy_<server>.log`. This is the MCP analog of
the LSP input log — so you can *see* exactly what the client sends (`->`) and the
server replies (`<-`): the `initialize` handshake, `tools/list` schemas, and every
`tools/call` with its arguments and result. Watch it live:

```bash
tail -f /tmp/mcp_proxy_fetch.log
```

The proxy only forwards bytes line-by-line, so it cannot corrupt the protocol — the
real server's behavior is unchanged. To run a server *without* logging, drop the
`mcp_logging_proxy.py --name <x> --` prefix from its `args` and call the server
command directly.

> **Note — `filesystem` fails to connect** in some images: the upstream
> `@modelcontextprotocol/server-filesystem` npx package throws
> `ERR_MODULE_NOT_FOUND` for `zod` (a packaging bug, not a config issue). `fetch`
> and `sequential-thinking` connect normally. The proxy log shows the failing
> server's `initialize` going out with no reply — itself a useful debug signature.

## When to choose multi over single

Pick multi when you have multiple MCP servers you want to ship as one plugin (often a toolbox theme). Pick single (`src/mcp-servers/example-single/`) when you have exactly one server.

## File walkthrough

```
src/mcp-servers/example-multi/
├── .claude-plugin/plugin.json    ← `mcpServers` field points at the config file
├── mcp-config.json               ← top-level `mcpServers` map; each entry runs the upstream server via mcp_logging_proxy.py
├── mcp_logging_proxy.py          ← bundled stdio JSON-RPC logging proxy (stdlib only; ${CLAUDE_PLUGIN_ROOT}/...)
└── README.md
```

## Cross-plugin server-key collisions

Two MCP plugins both defining a server keyed `fetch` would shadow each other in Claude's tool list. The test `test_mcp_server_keys_unique_across_plugins` catches this; prefer plugin-scoped keys when adding your own (e.g. `git-helpers-fetch`).

## Related

- Single counterpart: `src/mcp-servers/example-single/`
- Adding your own MCP plugin: `docs/ADDING_A_CONSTRUCT.md`
