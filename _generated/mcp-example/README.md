# example-mcp

Reference plugin for the **MCP server** (Model Context Protocol) construct type. Copy this directory to scaffold your own.

## What it does

Registers an MCP server named `example-fetch` that wraps `mcp-server-fetch` (the official fetch MCP, installed on demand via `uvx`). Once the plugin is enabled, the fetch tools become available in every session.

## Prerequisites

This example launches the MCP server with **`uvx mcp-server-fetch`**, so the host must have **[`uv`](https://github.com/astral-sh/uv)** installed and on `PATH`. Without it, Claude reports `plugin:mcp-example:example-fetch: uvx mcp-server-fetch - ✗ Failed to connect` after install.

Install `uv` once (any platform):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh        # macOS / Linux
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows PowerShell
```

After install, `uvx` becomes available — `uvx mcp-server-fetch` then downloads and runs the official fetch MCP on first invocation (no global Python install needed).

This is consistent with the marketplace's existing tooling baseline: `uv` is already required to run the generator (`scripts/generate_manifest.py` uses PEP 723 inline metadata).

## Install

```
/plugin install example-mcp@dgxsparklabs-marketplace
```

After install, MCP tools like `mcp__example-fetch__fetch` become available.

## File-by-file walkthrough

```
example-mcp/
├── .claude-plugin/plugin.json     ← manifest with "mcpServers": "./mcp-config.json"
├── mcp-config.json                ← server definitions
└── README.md
```

### `mcp-config.json`

A JSON file with an `mcpServers` object. Each key is a server name (becomes the prefix on tool names). Each value is the launch config:

- `command` — the executable
- `args` — array of arguments
- Optional: `env` — environment variables for the server process

The example uses `uvx mcp-server-fetch` — `uvx` runs Python packages without installing them globally. You can also use `npx`, a path to a local script, or any executable that speaks the MCP protocol over stdio.

## When to use MCP

MCP servers expose tools, resources, and prompts to Claude. Use MCP when:
- You need a stateful service (database, API session, headless browser).
- The capability is reusable across many skills/commands.
- There's an existing MCP server you can wrap (don't reinvent fetch, GitHub, etc.).

For simple one-off tools, a skill calling a script is lighter weight.

## To make your own MCP plugin from this template

1. `cp -r examples/example-mcp mcp-servers/my-mcp`
2. Edit `.claude-plugin/plugin.json` and `mcp-config.json`.
3. If wrapping an existing MCP server, just change `command` and `args`. If writing one, point `command` to your server script.
4. Test the server standalone first (`uvx your-server`) to confirm it speaks MCP correctly.
5. `uv run scripts/generate_manifest.py` and commit.

See `docs/ADDING_AN_MCP_SERVER.md` for the full launch-config schema.
