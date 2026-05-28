# lsp-example-multi

Reference plugin demonstrating the **multi-LSP layout**: one plugin ships three Language Server configurations (`markdown`, `python`, `rust`) in one `lsp-config.json`.

## Illustrative only

The LSP binaries (`marksman`, `pyright-langserver`, `rust-analyzer`) are NOT bundled. Install them separately if you want the LSPs to actually attach. The config shape is the reference; the runtime depends on your host environment.

## When to choose multi over single

Pick multi when you have multiple language servers you want to ship as one plugin (e.g. a polyglot toolbox). Pick single (`src/lsp-servers/example-single/`) when you have exactly one.

## File walkthrough

```
src/lsp-servers/example-multi/
├── .claude-plugin/plugin.json    ← `lspServers` field points at the config file
├── lsp-config.json               ← one entry per language: command, args, extensionToLanguage map
└── README.md
```

## Related

- Single counterpart: `src/lsp-servers/example-single/`
- Adding your own LSP plugin: `docs/ADDING_A_CONSTRUCT.md`
