# Changelog

## 2026-03-19

### Installer bug fixes (404b181)

Fixed four user-reported issues: K glyph in banner looked like R (changed to open-top form), path completion dropdown was hard-capped at 20 results (removed cap, increased visible height), installed marker only checked primary platform (now checks all detected platforms), and confirm dialog showed all global rules as workspace-only when any platform forced workspace (now shows in global section with a note about which platforms redirect to workspace).

### Installer bug fixes (d6f254a)

Fixed crash on missing catalog.toml (IndexError on empty PLATFORMS), duplicate items in confirm dialog summary, install_rule race condition (exists check after open), and added 5 uncategorized skills/rules to catalog.toml families.

### Installer upgrade (9edc9de)

Major installer rewrite: externalized configuration to catalog.toml, added per-item scope toggle (S key), workspace paths section with autocomplete and directory picker, MarketplaceList with click-to-focus behavior, platform-aware scope forcing (Devin rules auto-redirect to workspace), scope validation, and empty-state notices.
