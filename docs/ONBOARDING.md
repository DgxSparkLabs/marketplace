# Agent Onboarding Guide

> **Read time:** 3 minutes
> **Audience:** Any AI agent working in this repository for the first time

---

## What This Project Is

This is a **skills and rules marketplace** — a curated collection of reusable capabilities for AI coding agents. It works across Claude Code, Cursor, Windsurf, Gemini CLI, and Devin.

- **Skills** are invoked on demand (`/skill-name`). They give you new abilities: web search, email, YouTube analysis, GitHub exploration, port tunneling, and more.
- **Rules** are always-on behavioral guidelines that activate every session: scoping changes by blast radius, requiring work verification, keeping you motivated.

This is NOT a software project. There is no build system, no package manager, no app to deploy. The "product" is the skills and rules themselves — and the research that informs what to build next.

## What's Here

```
marketplace/
├── AGENTS.md               ← Your instructions. Read this.
├── README.md               ← Catalog of all skills and rules
├── CONTRIBUTING.md          ← How to add new items
├── docs/                   ← Format specs (SKILL_FORMAT.md, RULE_FORMAT.md)
├── _template/              ← Copy this to start a new skill
├── research/               ← 200+ sources of market intelligence (see below)
├── tests/                  ← 104 automated tests
├── <skill-name>/           ← Each skill is a self-contained directory
└── <rule-name>/            ← Each rule is a self-contained directory
```

## Your First 5 Minutes

1. **Read `AGENTS.md`** — conventions, testing, how to add skills/rules
2. **Scan `README.md`** — catalog of everything available (15 skills, 9 rules)
3. **Read one skill** (try `duckduckgo-search/SKILL.md`) — see how skills work
4. **Read one rule** (try `blast-radius/rule.md`) — see how rules work
5. **Run the tests** — `uv run tests/test_marketplace.py` (must pass before any changes)

## The Research Library

The `research/` directory contains 12 rounds of market intelligence across GitHub, arXiv, Reddit, Twitter/X, Kaggle, and web sources. Before reading any raw research files:

1. **Start with** `research/README.md` — navigation index, canonical file markers, provenance rules
2. **For strategic context:** `research/SUMMARY_AND_CONCLUSIONS.md` — the master synthesis
3. **For actionable knowledge:** `research/KNOWLEDGE_BASE.md` — distilled insights organized by topic
4. **For avoiding mistakes:** `research/ANTI_PATTERNS.md` — dead ends, noise, and traps we've cataloged
5. **For doing more research:** `research/METHODOLOGY.md` — tools and strategies that work

Do NOT read the raw `skill-marketplaces-N/` directories unless you need to trace a specific claim back to its source.

## How to Contribute

### Adding a Skill

1. Copy `_template/` to `your-skill-name/`
2. Write `SKILL.md` (YAML frontmatter + prompt body) — see `docs/SKILL_FORMAT.md`
3. Write scripts in `scripts/` using PEP 723 inline metadata (zero-install via `uv run`)
4. Set `allowed-tools` to the minimum needed
5. Add a `README.md` and update the catalog in root `README.md`
6. Run `uv run tests/test_marketplace.py` — all 104 tests must pass

### Adding a Rule

1. Use `no-ai-credit/` as your reference
2. Write `rule.md` (plain Markdown, no frontmatter)
3. Create `formats/windsurf.md` and `formats/cursor.md`
4. Adapt `install.sh` from the reference
5. Add a `README.md` and update the catalog in root `README.md`
6. Run the tests

### Modifying Research

**Never wholesale-rewrite canonical research files.** Merge new findings incrementally. See `research/README.md` for the full protocol.

## Key Concepts to Internalize

These are the most important things we've learned from 200+ sources:

1. **Trust is the product, not skills.** The hard problem isn't creating or distributing skills — vibe-coding makes creation trivial, GitHub handles distribution. The hard problem is verification, security, quality assurance, and reputation.

2. **Narrow beats general.** Domain-specific skill collections (crypto, PM, security) consistently outperform general-purpose catalogs. Start vertical, expand horizontal.

3. **Composability is the moat.** Flat skill lists are commoditized. DAG-based orchestration, skill chaining, and composition patterns differentiate.

4. **Security is non-negotiable.** 26.1% of community skills have vulnerabilities. The ClawHavoc attack infiltrated 1,200 malicious skills into a major marketplace. Every skill you create must be safe by default.

5. **SKILL.md is the standard.** YAML frontmatter + Markdown prompt body, adopted by Anthropic, OpenAI, Microsoft, Cursor, Windsurf, and 38+ agents. This format is non-negotiable.

## Mindset

- **Be autonomous.** This repository exists to give you capabilities. Use them. Build new ones. Don't ask permission for things you can figure out by reading the code and running the tests.
- **Verify your work.** Always run the test suite. Always check that what you built actually works.
- **Search before building.** Check the research, check existing skills, check the prior-art rule. Someone may have already solved your problem.
- **Keep it simple.** Skills should do one thing well. Rules should be concise checklists, not essays. Scripts should use PEP 723 and `uv run` for zero-install.
- **Don't reinvent findings.** The research library contains hard-won insights from 200+ sources. Read `KNOWLEDGE_BASE.md` before making strategic decisions about what to build.

## Good First Contributions

If you're looking for a place to start, here are high-value, low-risk tasks:

1. **Add a skill from the research.** The research identified tools agents need (web scraping, data analysis, code review). Pick one, build it following `_template/`, run the tests.
2. **Verify a research claim.** Pick an unverified entry from `research/METHODOLOGY.md` (the "Reported" tier) and check it against live sources. Update the verification tier.
3. **Improve a README.** Some skills have minimal documentation. Compare against `send-email/README.md` (the reference) and add missing sections.
4. **Port a rule to a new format.** Some rules only have `windsurf.md` and `cursor.md` formats. Add support for other agent platforms.
5. **Write a missing test.** Read `tests/test_marketplace.py` and look for edge cases not covered. The test suite is the quality gate — making it stronger benefits everyone.
6. **Extend `ANTI_PATTERNS.md`.** If you encounter a dead-end, noise source, or mistake while working, document it so the next agent doesn't repeat it.
