# Agent Instructions

This is a skills and rules marketplace. Not a software project — no build system, no package manager.

**New here?** Read `docs/ONBOARDING.md` for a 3-minute orientation. For market intelligence, start with `research/KNOWLEDGE_BASE.md`.

Skills live under `skills/` and rules under `rules/`.
- Has `SKILL.md` → skill
- Has `rule.md` + `install.sh` → rule

## Layout

```
marketplace/
├── catalog.toml                # TUI installer configuration (platforms, families, MCP)
├── docs/
│   ├── SKILL_FORMAT.md         # Full SKILL.md spec
│   └── RULE_FORMAT.md          # Full rule spec
├── _template/                  # Starter for new skills
├── rules/
│   └── no-ai-credit/           # Reference rule
├── skills/
│   └── send-email/             # Reference skill
└── ...
```

## Adding a Skill

Use `_template/` as a starter. Full spec in `docs/SKILL_FORMAT.md`.

```
my-skill/
├── SKILL.md            # Required
├── README.md           # Required
├── scripts/            # Optional
├── setup.sh            # Optional — prerequisite installer
└── references/         # Optional
```

- Python scripts must use PEP 723 inline metadata (`uv run` with zero install)
- Always set `allowed-tools` to minimum needed
- Update the **Skills** table in root `README.md` (alphabetical)

## Adding a Rule

Use `rules/no-ai-credit/` as a reference. Full spec in `docs/RULE_FORMAT.md`.

```
my-rule/
├── rule.md             # Required — plain Markdown, no frontmatter
├── README.md           # Required
├── install.sh          # Required — supports --global and --format
└── formats/
    ├── windsurf.md     # trigger: always_on
    └── cursor.md       # alwaysApply: true
```

- Copy and adapt `rules/no-ai-credit/install.sh`
- Update the **Rules** table in root `README.md` (alphabetical)

## Conventions

- Directory names: **kebab-case**
- Script filenames: **snake_case** for Python, **kebab-case** allowed for shell scripts
- Python scripts: PEP 723, runnable via `uv run`
- Shell scripts: shebang + `set -euo pipefail`
- Never commit secrets
- Do not add project-level config (`pyproject.toml`, `package.json`, etc.) at root
- Do not mix skill and rule formats in one directory

## Testing

Run the test suite to validate all skills, rules, and install scripts:

```
uv run tests/test_marketplace.py        # all tests
uv run tests/test_marketplace.py -v     # verbose
uv run tests/test_marketplace.py -k rule  # only rule tests
```

The test suite checks: directory structure, YAML frontmatter, catalog consistency, PEP 723 metadata, shell script safety, install script behavior (--help, --global, idempotency), format file content parity, and secret scanning. Always run the tests before submitting changes.

Run the CI workflow locally with [act](https://github.com/nektos/act) and podman:

```
./tests/run-ci-local.sh          # run the full GitHub Actions workflow locally
./tests/run-ci-local.sh -n       # dry-run (no container)
```

## Marketplace Testing

Always run `uv run tests/test_marketplace.py` before declaring done.

## Research Directory

The `research/` directory contains 90+ files across 12 research rounds. Read `research/README.md` before modifying any research file.

**Critical rules:**

- **Canonical files** are the top-level `.md` files in `research/` (e.g., `arxiv_findings.md`, `github_findings.md`, `SUMMARY_AND_CONCLUSIONS.md`). These represent carefully consolidated findings across all rounds.
- **Never wholesale-rewrite a canonical file.** Merge new findings incrementally into the existing structure. Rewrites lose data — past attempts dropped 21 arXiv papers and 38 GitHub repos.
- **Archival rounds** live in `research/skill-marketplaces-N/`. These are raw research data, not authoritative. New rounds go in `skill-marketplaces-N+1/`.
- **Verify before citing.** Star counts and repo existence must be checked against live sources before adding to canonical files. Prior rounds contain unverified data.
- **Raw artifacts are gitignored.** Scrape dumps, notebook outputs, and batch results are excluded. Only curated analysis files are committed.
- **Note provenance.** When adding a data point, note which research round or source it came from.
- See `research/TASKS.md` for the current maintenance backlog.

## No AI Credit

Never attribute work to yourself or to any AI agent, tool, or assistant. This applies to every artifact you produce or modify.

- NEVER add "Co-Authored-By" lines referencing any AI agent or bot in git commits.
- NEVER add "Generated with", "Created by", "Built with", "Powered by", or similar AI attribution to git commits, PRs, code comments, documentation, READMEs, changelogs, or any other output.
- NEVER add badges, links, sections, or footnotes crediting an AI tool or agent.
- NEVER add file headers or authorship lines that reference an AI tool.
- NEVER include `noreply@` email addresses associated with AI bots in commits.
- Git commit messages must contain only the actual change description — no agent attribution of any kind.

Before completing any task, scan your output for:
- "Co-Authored-By" lines referencing any AI or bot
- "Generated with" / "Created by" / "Built with" / "Powered by" followed by an AI tool name
- Any mention of an AI agent name as an author or contributor
- Badges or links that credit an AI tool
- `noreply@` email addresses associated with AI bots

If any of these are present, remove them before finishing. No exceptions.

## Writing Rules — Keep Them Concise

Rules consume agent context in every session. Verbose rules dilute attention and waste context budget.

- **Aim for actionable checklists, not documentation.** If a rule reads like an essay, it's too long.
- **Every line should be an instruction the agent can act on.** Remove explanations of *why* — agents need *what* and *when*.
- **Consolidate** — 5 crisp bullet points beat 40 lines of prose.
- Rules installed to multiple targets appear multiple times in agent context. Use `--format agents` to install to a single target.
