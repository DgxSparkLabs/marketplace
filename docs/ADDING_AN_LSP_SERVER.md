# Adding an LSP Server

LSP servers give Claude type information, definitions, and diagnostics for a language. Use them when working in a project that benefits from compile/type signals.

For the file structure, read [`examples/example-lsp/README.md`](../examples/example-lsp/README.md).

## Workflow

1. **Copy the example**:
   ```bash
   mkdir -p lsp-servers
   cp -r examples/example-lsp lsp-servers/my-lsp
   ```

2. **Edit**:
   - `lsp-servers/my-lsp/.claude-plugin/plugin.json` — set `name` to `lsp-my-lsp`.
   - `lsp-servers/my-lsp/lsp-config.json` — declare the server under `lspServers`. Each entry has `command`, `args`, and `fileExtensions`.

3. **Confirm the LSP binary is installable** on the target platform. The plugin registers the server; it does not install the binary itself. Document install instructions in the README.

4. **Regenerate and validate**:
   ```bash
   uv run scripts/generate_manifest.py
   uv run tests/test_marketplace.py
   claude plugin validate lsp-servers/my-lsp
   ```

5. **Commit**.

## Picking an LSP server

| Language | Common LSP server |
|----------|------------------|
| TypeScript / JavaScript | typescript-language-server |
| Python | pyright |
| Go | gopls |
| Rust | rust-analyzer |
| Markdown | marksman |
| YAML | yaml-language-server |

Multiple plugins can register different LSP servers for different file extensions. Claude Code routes each file to the matching server.

## Install path after merge

```
/plugin install lsp-my-lsp@marketplace
```

## Related docs

- [`CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md)
- [`examples/example-lsp/README.md`](../examples/example-lsp/README.md)
