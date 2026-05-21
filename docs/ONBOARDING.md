# Agent Onboarding Guide

> **Read time:** 3 minutes
> **Audience:** Any AI agent or human contributor working in this repository for the first time

---

## What This Project Is

This is a **Claude Code plugin marketplace** — a curated collection of skills, rules, and reference example plugins, packaged for native `/plugin marketplace add` install. It also ships auto-generated mirrors for Devin, Cursor, Windsurf, Codex CLI, and Gemini CLI.

- **Skills** = on-demand capabilities invoked with `/skill-name` (26 skills)
- **Rules** = always-on behavioral guidelines loaded every session via `.claude/rules/` (21 rules)
- **Examples** = 10 reference plugins (one per Claude Code construct type) in `examples/`
- **Research** = 250+ sources across 12 rounds of market intelligence

This is NOT a software project. The product is the plugins themselves.

## What's Here

```
marketplace/
├── MARKETPLACE.toml                  ← Single source for owner / version / license
├── catalog.toml                      ← Construct types + skill/rule domain tagging
├── .claude-plugin/marketplace.json   ← Generated root manifest (71 plugin entries)
├── skills/                           ← Source skill content (26 skills)
├── rules/                            ← Source rule content (21 rules)
├── examples/                         ← 10 example-* reference plugins
├── _generated/                       ← Generated plugin wrappers + bundles + rules-all
├── .codex/, .gemini/, .cursor/, .windsurf/, .devin/   ← Cross-platform mirrors
├── scripts/generate_manifest.py      ← The engine that produces everything generated
├── activate-installed-rules.sh       ← Bulk helper for symlinking installed rule plugins
├── tests/test_marketplace.py         ← Test suite (35+ tests)
├── docs/                             ← Format specs, tutorials, architecture docs
├── research/                         ← 250+ market intelligence sources
├── AGENTS.md                         ← Your instructions if you're an AI agent
└── CONTRIBUTING.md                   ← How to add a new plugin
```

## Your First 5 Minutes

1. **Read `AGENTS.md`** — conventions, generator workflow, no-AI-credit requirement.
2. **Skim `README.md`** — catalog of all 71 installable plugins.
3. **Read `docs/CONSTRUCT_TYPES.md`** — what each construct type is.
4. **Look at one `examples/example-skill/`** — the canonical pattern for adding new content.
5. **Run the tests**: `uv run tests/test_marketplace.py` (must pass before any change).

## Install Path

```bash
# In a Claude Code session:
/plugin marketplace add DgxSparkLabs/marketplace

# Then install whatever you need:
/plugin install skill-telegram-notify@marketplace        # individual skill
/plugin install skills-communication@marketplace         # domain bundle
/plugin install rule-blast-radius@marketplace            # individual rule
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-blast-radius/activate.sh

# Bulk-activate all installed rule plugins at once:
bash ~/.local/share/marketplace/activate-installed-rules.sh
```

For Devin / Cursor / Windsurf / Codex CLI / Gemini CLI: `git clone` the repo and point your tool at the appropriate mirror directory (`.devin/`, `.cursor/`, etc.).

## How to Contribute

The fastest path is **copy the matching `examples/example-<type>/` directory** and adapt. Each construct type has a step-by-step tutorial:

| Construct type | Tutorial |
|----------------|----------|
| Skill | [`docs/ADDING_A_SKILL.md`](./ADDING_A_SKILL.md) |
| Rule | [`docs/ADDING_A_RULE.md`](./ADDING_A_RULE.md) |
| Domain bundle | [`docs/ADDING_A_DOMAIN_BUNDLE.md`](./ADDING_A_DOMAIN_BUNDLE.md) |
| Anything else | see [`docs/CONSTRUCT_TYPES.md`](./CONSTRUCT_TYPES.md) for the full list |

Workflow (every contribution):

1. Edit source content in `skills/`, `rules/`, or `examples/`.
2. If adding a new skill/rule, tag it in `catalog.toml`.
3. Run `uv run scripts/generate_manifest.py`.
4. Run `uv run tests/test_marketplace.py`.
5. Commit. **No AI co-author attribution.** (See `rules/no-ai-credit/`.)

## The Research Library

The `research/` directory contains 12 rounds of market intelligence across GitHub, arXiv, Reddit, Twitter/X, Kaggle, and web sources. Before reading any raw research files:

1. **Start with** `research/README.md` — navigation index, canonical file markers, provenance rules.
2. **For strategic context:** `research/SUMMARY_AND_CONCLUSIONS.md` — the master synthesis.
3. **For actionable knowledge:** `research/KNOWLEDGE_BASE.md` — distilled insights organized by topic.
4. **For avoiding mistakes:** `research/ANTI_PATTERNS.md` — dead ends, noise, and traps we've cataloged.

Do NOT read raw `skill-marketplaces-N/` directories unless tracing a specific claim back to its source.

## Key Concepts to Internalize

1. **Trust is the product, not skills.** The hard problem isn't creating or distributing skills — it's verification, security, and reputation.

2. **Narrow beats general.** Domain-specific skill collections outperform general-purpose catalogs.

3. **Composability is the moat.** Flat skill lists are commoditized. Domain bundles, agent composition, and skill chaining differentiate.

4. **Security is non-negotiable.** ~26% of community skills have known vulnerabilities. Every plugin must be safe by default.

5. **`SKILL.md` is the open standard.** YAML frontmatter + Markdown prompt body, adopted by Anthropic, OpenAI, Microsoft, Cursor, Windsurf, and 38+ agents.

## Mindset

- **Be autonomous.** Read the code, run the tests, figure things out. Don't ask permission for what you can verify yourself.
- **Verify your work.** Always run the test suite. Always confirm what you built actually works.
- **Search before building.** Check existing skills, the research library, and prior art.
- **Keep it simple.** Skills do one thing well. Rules are concise checklists, not essays. Scripts use PEP 723 and `uv run` for zero-install.
- **Source of truth, not duplicates.** Edit `skills/`, `rules/`, `examples/`, or `catalog.toml` — never `_generated/` or the cross-platform mirrors.

## Good First Contributions

1. **Add a missing skill.** Check `research/KNOWLEDGE_BASE.md` for tools agents commonly need.
2. **Add a new rule.** Look at the rule reviews surfaced in `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` and earlier discussions.
3. **Improve a README.** Some skill READMEs are minimal. Use `skills/send-email/README.md` as a reference.
4. **Add a tutorial that helped you.** If you learn something while contributing, document it.
5. **Extend the test suite.** Read `tests/test_marketplace.py` and add coverage for cases not yet tested.
