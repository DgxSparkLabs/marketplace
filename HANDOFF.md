# Handoff

## Current State

The marketplace is a skills and rules repository with a TUI installer (`install.py`) built on Textual. It supports 4 platforms: Devin CLI, Claude Code, Cursor, and Windsurf.

### Recent Changes

- **Installer upgrade** (`9edc9de`): Per-item scope toggle, workspace paths with autocomplete, catalog.toml externalization, MarketplaceList click behavior, platform-aware scope forcing (Devin rules forced to workspace).
- **Bug fixes** (`d6f254a`): Crash on empty catalog, duplicate confirm summary, install_rule race condition, uncategorized catalog items.
- **Bug fixes** (`404b181`): Banner K glyph, dropdown completion cap removed, installed marker checks all platforms, confirm summary shows correct scope breakdown.

### Key Architecture

- `catalog.toml` — all TUI configuration (platforms, MCP servers, families, defaults)
- `install.py` — single-file TUI app, PEP 723 inline deps (`textual>=1.0.0`)
- `_build_platforms()` converts TOML to runtime PLATFORMS dict; empty string `""` in TOML is falsy in Python, correctly becoming `None`
- `_execute_install()` handles per-platform scope forcing: if a platform has `global.rules = None`, rules are redirected to workspace scope
- Confirm dialog summary now shows items in user-chosen scope with a note about platforms that force workspace

### How to Build/Test

```bash
uv run install.py                    # run the TUI
uv run install.py --uninstall        # uninstall mode
uv run tests/test_marketplace.py     # 112 tests
uvx ruff check install.py            # lint
```

### What's Next

- The installed marker only checks global scope per platform. Workspace-installed items aren't reflected in the marker. This is a known limitation.
- The path autocomplete dropdown can now show all results, but very large directories may produce long lists. Consider lazy loading if this becomes an issue.
