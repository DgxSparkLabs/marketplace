# example-lsp

Reference plugin for the **LSP server** (Language Server Protocol) construct type. Copy this directory to scaffold your own.

## What it does

Registers an LSP server for markdown files using [marksman](https://github.com/artempyanykh/marksman). Claude Code uses LSP signals (hover info, definitions, diagnostics) when working on files with matching extensions.

Install:
```
/plugin install example-lsp@dgxsparklabs-marketplace
```

Prerequisite: marksman must be installed on the system (`brew install marksman` or download from the project's releases). This plugin only registers the server — it does not install it.

## File-by-file walkthrough

```
example-lsp/
├── .claude-plugin/plugin.json     ← manifest with "lspServers": "./lsp-config.json"
├── lsp-config.json                ← server definitions
└── README.md
```

### `lsp-config.json`

A JSON file with an `lspServers` object. Each key is the server name. Each value declares:

- `command` — the LSP server executable
- `args` — startup arguments
- `fileExtensions` — which file types trigger this server

Multiple plugins can register different LSP servers for different file types. Claude Code routes each file to the matching server.

## When to use LSP

LSP servers give Claude type information, definitions, and diagnostics for a language. Use when:
- Working on a project that benefits from compile/type signals
- The language has a mature LSP available
- You want Claude to "see" errors before running build

For pure prose or scripting work where type info adds no value, skip LSP and rely on skills/hooks for guidance.

## To make your own LSP plugin from this template

1. `cp -r examples/example-lsp lsp-servers/my-lsp`
2. Edit `.claude-plugin/plugin.json` and `lsp-config.json`.
3. Pick the LSP server for your language (typescript-language-server, pyright, gopls, rust-analyzer, etc.).
4. List the file extensions that should trigger the server.
5. `uv run scripts/generate_manifest.py` and commit.

See `docs/ADDING_AN_LSP_SERVER.md` for the full config schema.
