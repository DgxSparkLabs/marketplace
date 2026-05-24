# Goal — Claude Code Plugin Compliance

**Branch:** `feat/claude-plugin-compliance`
**Status:** Planning complete. Execution not yet started.

---

## Goal (one paragraph)

Make this marketplace installable through Claude Code's native `/plugin marketplace add DgxSparkLabs/marketplace` command, with first-class support for both **individual** and **domain-bundle** installs across **all ten** Claude Code plugin construct types (skills, rules, commands, agents, hooks, MCP servers, LSP servers, monitors, output styles, themes). Ship a reference `example-*` plugin per construct type so contributors can copy-and-adapt rather than read docs.

---

## Success Criteria (each is a binary pass/fail)

A reviewer can run each check below and get a yes/no.

| # | Criterion | How to verify |
|---|-----------|---------------|
| 1 | `/plugin marketplace add DgxSparkLabs/marketplace` succeeds in a fresh Claude Code session | Run the command, confirm no error |
| 2 | Individual skill install works | `/plugin install skill-telegram-notify@dgxsparklabs-marketplace` then invoke `/telegram-notify` |
| 3 | Domain skill bundle install works | `/plugin install skills-communication@dgxsparklabs-marketplace` results in all member skills being installed (directly or via `install-deps.sh` per task #13 outcome) |
| 4 | Individual rule install + activation works | `/plugin install rule-blast-radius@dgxsparklabs-marketplace` then `bash <cache>/rule-blast-radius/activate.sh` symlinks rule into `.claude/rules/` |
| 5 | Bulk rule install + activation works | `/plugin install rules-all@dgxsparklabs-marketplace` + activate script applies all 21 rules |
| 6 | Ten example plugins exist and install | One `example-*` plugin per construct type (skill, rule, command, agent, hook, mcp, lsp, monitor, output-style, theme); each installs without error |
| 7 | Cross-platform mirrors exist | `.codex/skills/`, `.gemini/skills/`, `.cursor/rules/`, `.windsurf/rules/` directories committed and populated |
| 8 | Test suite passes | `uv run tests/test_marketplace.py` exits 0 |
| 9 | Manifests stay in sync via CI | `uv run scripts/generate_manifest.py --check` exits 0 in GitHub Actions |
| 10 | README leads with the new install path | First install instruction is `/plugin marketplace add DgxSparkLabs/marketplace` |
| 11 | Complete contributor tutorial set exists | `docs/CONSTRUCT_TYPES.md` + 11 `docs/ADDING_*.md` files cover every construct type and domain bundles |
| 12 | TUI is fully removed | `install.py` and `scripts/install.sh` are deleted from the branch; no references remain in `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, tests, or docs; the only install path is `/plugin marketplace add DgxSparkLabs/marketplace` (or the auto-generated cross-platform mirrors for non-Claude-Code tools) |

**Done = all 12 boxes ticked. Anything less is not done.**

---

## Out of Scope (explicitly NOT in this branch)

- Backwards-compatible install shim for users on the old `curl ... | bash` path (we link to migration notes in CHANGELOG.md instead; no stub script is shipped)
- Migrating Python scripts away from PEP 723 / `uv` (this is our differentiator vs. stdlib-only marketplaces)
- Adding new skills or rules unrelated to the migration
- Changing SKILL.md frontmatter format (Claude Code-native fields stay)
- Fixing the rule duplication/contradiction issues surfaced in earlier reviews (separate work)
- Implementing rule installation as a native plugin field (Anthropic must add support first)
