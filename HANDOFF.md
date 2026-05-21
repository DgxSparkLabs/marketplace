# Handoff

> **Branch `feat/claude-plugin-compliance`** — migration to Claude Code native `/plugin marketplace add` complete. 11 of 12 tasks done; task #10 (end-to-end install verification + open PR to main) is the only remaining work. Read `docs/GOAL_PLUGIN_COMPLIANCE.md` for the success criteria, `docs/PLAN_PLUGIN_COMPLIANCE.md` for the architecture.

## What This Is

A **Claude Code plugin marketplace** for AI coding agents. Natively installable via `/plugin marketplace add DgxSparkLabs/marketplace`, with auto-generated mirrors for Devin CLI, Cursor, Windsurf, Codex CLI, and Gemini CLI.

- 26 skills (`skills/<name>/`)
- 21 rules (`rules/<name>/`)
- 10 example reference plugins (`examples/example-<type>/`)
- 71 plugin entries total in `.claude-plugin/marketplace.json` (26 individual skills + 8 skill-domain bundles + 21 individual rules + 5 rule-domain bundles + 1 rules-all + 10 examples)
- 250+ research sources across 12 rounds in `research/`

## How to Build / Test

```bash
uv run scripts/generate_manifest.py            # regenerate _generated/ + cross-platform mirrors
uv run scripts/generate_manifest.py --check    # CI gate: drift-detection mode
uv run tests/test_marketplace.py               # 35+ tests, must all pass
uv run tests/test_marketplace.py -v            # verbose
claude plugin validate _generated/skill-<name> # validate a single plugin manifest
```

**Always regenerate and re-run tests before committing.** CI does both as separate steps so failures are clearly distinguishable.

## Project Layout

```
marketplace/
├── MARKETPLACE.toml                    Single source for identity (owner, version, license)
├── catalog.toml                        Construct-type definitions + skill/rule domain tagging
├── .claude-plugin/marketplace.json     Generated root manifest
├── skills/                             Source content
├── rules/                              Source content
├── examples/                           10 reference plugins (one per construct type)
├── _generated/                         Per-plugin wrappers + bundles
├── .codex/  .gemini/  .cursor/  .windsurf/  .devin/   Cross-platform mirrors
├── activate-installed-rules.sh         Bulk helper for rule activation
├── scripts/generate_manifest.py        The engine
├── tests/test_marketplace.py           Test suite
├── docs/                               Format specs, contributor tutorials, architecture
└── research/                           Market intelligence (read research/README.md first)
```

## Architecture Summary

- **Sources of truth**: `MARKETPLACE.toml`, `catalog.toml`, and the source content under `skills/`, `rules/`, `examples/`. Humans edit these.
- **Generated**: everything in `_generated/`, `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`, and `.claude-plugin/marketplace.json`. The generator produces these from the sources.
- **Skill or rule bundles** (`skills-<domain>`, `rules-<domain>`, `rules-all`) are content-free plugins whose `plugin.json` declares only `dependencies`. Claude Code auto-installs the dependencies — verified empirically; see `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`.
- **Rules** are installed via `/plugin install` then activated by running the plugin's `activate.sh`, which symlinks the rule file into `.claude/rules/`. Required because Claude Code's plugin system does not yet ship a native `rules` field.

## Conventions

- Names: kebab-case for everything (skills, rules, domains, plugin names).
- Python scripts: PEP 723 inline metadata, `uv run`.
- Shell scripts: shebang + `set -euo pipefail`.
- No project-level Python deps (no `pyproject.toml` at root).
- `author` in plugin.json is always an object `{ "name": "...", "url": "..." }`, never a string.
- `source` paths in marketplace.json start with `./`.
- Commit messages have no AI co-author attribution (see `rules/no-ai-credit/`).

## Adding Skills / Rules / Anything

Copy `examples/example-<type>/` and adapt. Each construct type has a tutorial in `docs/ADDING_*.md`; for the index, see `docs/CONSTRUCT_TYPES.md`.

General workflow:
1. Edit source content.
2. If skill or rule: add to a domain in `catalog.toml`.
3. `uv run scripts/generate_manifest.py`.
4. `uv run tests/test_marketplace.py`.
5. Commit.

## What's Next

- **Task #10**: End-to-end install verification + open PR to `main`. Manually verify in a fresh Claude Code session that `/plugin marketplace add DgxSparkLabs/marketplace`, `/plugin install skill-telegram-notify@marketplace`, `/plugin install skills-communication@marketplace`, `/plugin install rule-blast-radius@marketplace` + activate, and `/plugin install rules-all@marketplace` + bulk activate all work as documented.
- **After merge**: research backlog (T6 / T7 / T10 in `research/TASKS.md`).
- **Future**: native `rules` field if Anthropic adds it (would remove the activate.sh step). See `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` for the open feature request reference.

## Known Limitations

- Rule activation is a manual step (`activate.sh`). No native plugin-installable rules in Claude Code yet.
- Generator regenerates `_generated/` and mirrors from scratch each run — fast (~1s) but means hand-edits there are always lost.
- Cross-platform mirrors are best-effort. Platform-specific tooling (Cursor's `.mdc` files, Codex's plugin spec, etc.) may evolve faster than this repo tracks.
