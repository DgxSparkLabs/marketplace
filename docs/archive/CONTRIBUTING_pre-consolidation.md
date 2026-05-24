# Contributing

Thanks for your interest in contributing to the marketplace.

The marketplace ships **plugins** for ten Claude Code construct types: skills, rules, commands, agents, hooks, MCP servers, LSP servers, monitors, output styles, and themes — plus **domain bundles** that auto-install a curated group of related plugins.

The fastest path to adding anything is **copy the matching `examples/example-<type>/` directory** and adapt. Each example is both a working installable plugin and a tutorial.

## Adding something — pick your construct

Detailed walkthroughs (each takes ~5 minutes to read):

| Construct type | Tutorial |
|----------------|----------|
| Skill | [`docs/ADDING_A_SKILL.md`](./docs/ADDING_A_SKILL.md) |
| Rule | [`docs/ADDING_A_RULE.md`](./docs/ADDING_A_RULE.md) |
| Command | [`docs/ADDING_A_COMMAND.md`](./docs/ADDING_A_COMMAND.md) |
| Agent | [`docs/ADDING_AN_AGENT.md`](./docs/ADDING_AN_AGENT.md) |
| Hook | [`docs/ADDING_A_HOOK.md`](./docs/ADDING_A_HOOK.md) |
| MCP server | [`docs/ADDING_AN_MCP_SERVER.md`](./docs/ADDING_AN_MCP_SERVER.md) |
| LSP server | [`docs/ADDING_AN_LSP_SERVER.md`](./docs/ADDING_AN_LSP_SERVER.md) |
| Monitor | [`docs/ADDING_A_MONITOR.md`](./docs/ADDING_A_MONITOR.md) |
| Output style | [`docs/ADDING_AN_OUTPUT_STYLE.md`](./docs/ADDING_AN_OUTPUT_STYLE.md) |
| Theme | [`docs/ADDING_A_THEME.md`](./docs/ADDING_A_THEME.md) |
| **Domain bundle** | [`docs/ADDING_A_DOMAIN_BUNDLE.md`](./docs/ADDING_A_DOMAIN_BUNDLE.md) |

For the construct-types overview and naming convention, see [`docs/CONSTRUCT_TYPES.md`](./docs/CONSTRUCT_TYPES.md).

## Architecture in one paragraph

Human-edited content lives in `skills/`, `rules/`, and `examples/`. Tagging lives in `catalog.toml` (which skill/rule belongs to which domain). The script `scripts/generate_manifest.py` consumes both plus `MARKETPLACE.toml` (single source for owner/version/license) and produces everything else: `.claude-plugin/marketplace.json`, per-plugin wrappers in `_generated/`, and cross-platform mirrors in `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`. CI fails any PR where generated content drifts from sources.

## The contributor checklist

For every PR:

1. **Edit source content only** — never edit `_generated/` or the cross-platform mirror directories. The generator overwrites them.
2. **Tag new skills/rules in `catalog.toml`** — every skill must belong to exactly one `[skill_domain.*]`; every rule must belong to exactly one `[rule_domain.*]`. The test suite enforces this.
3. **Regenerate** — `uv run scripts/generate_manifest.py`
4. **Test** — `uv run tests/test_marketplace.py` (must pass)
5. **Validate the plugin manifest** — `claude plugin validate <new-plugin-dir>` (if the `claude` CLI is available locally)
6. **Commit** with a clear conventional message. Do not include AI co-author attribution.

## Quality bar

- **Names are kebab-case.** Skill, rule, domain, and plugin names: lowercase letters, digits, hyphens only.
- **Author is an object.** `{ "name": "...", "url": "..." }`, never a string.
- **Paths start with `./`.** Marketplace.json `source` paths and `skills`/`commands`/`agents` arrays.
- **No hardcoded secrets.** Use environment variables for all credentials. The secret scanner in `tests/test_marketplace.py` will block obvious patterns.
- **Python scripts use PEP 723 + `uv run`.** Inline dependency metadata, no project-level `pyproject.toml`.
- **Shell scripts use `set -euo pipefail` and a shebang.**
- **One construct, one purpose.** Keep skills, rules, commands, and agents focused on a single concern.

## Submission

1. Fork the repository.
2. Create a branch: `feat/<short-description>`.
3. Make your changes (source + catalog.toml tagging only — let the generator handle the rest).
4. Run `uv run scripts/generate_manifest.py` and commit the generated output too.
5. Run `uv run tests/test_marketplace.py` — all 35+ tests must pass.
6. Open a PR to `main`. CI runs the generator with `--check` and the test suite.

## Related reading

- [`docs/CONSTRUCT_TYPES.md`](./docs/CONSTRUCT_TYPES.md) — what each construct is and when to use it
- [`AGENTS.md`](./AGENTS.md) — project conventions for AI agents
- [`docs/PLAN_PLUGIN_COMPLIANCE.md`](./docs/PLAN_PLUGIN_COMPLIANCE.md) — full architecture
- [`docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`](./docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md) — why bundles use the `dependencies` field
