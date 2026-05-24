# Agent Instructions

This is a Claude Code plugin marketplace. Not a software project — no build system, no package manager. Identity, version, and license live in `MARKETPLACE.toml`; bundle tagging lives in `catalog.toml`; everything else is either source content (under `<construct>/<name>/`) or auto-generated from those two files by `scripts/generate_manifest.py`.

## Where to find things

- `README.md` — user-facing install + Quick Start.
- `HANDOFF.md` — long-form project state tracker (5 completed phases, layout, next steps).
- `docs/RESUME_HERE.md` — 30-second re-entry orientation.
- `CONTRIBUTING.md` — contributor workflow + conventions + output discipline (the canonical "how do I work in this repo" doc — see it before duplicating content here).
- `docs/ARCHITECTURE.md` — generator architecture: Construct + Platform protocols, six phases.
- `docs/PLATFORMS.md` — per-platform install/support reference.
- `docs/ADDING_A_CONSTRUCT.md` — the single contributor walkthrough for all 10 construct types.
- `docs/CONSTRUCT_TYPES.md` — reference table for the 10 constructs.

For project-wide conventions and contributor discipline, see `CONTRIBUTING.md`.

This file (`AGENTS.md`) is the per-project AI-agent rule set: only project-specific conventions live here. Generic discipline content (verification ladder, blast radius, document lifecycle, output discipline, autonomous persistence, etc.) used to be duplicated here; it now lives in `CONTRIBUTING.md` under "Output discipline (...)" and the contributor's user-global content. Don't re-import generic rules into this file — keep it project-scoped.

## Conventions (project-specific)

- Directory names: **kebab-case**
- Script filenames: **snake_case** for Python, **kebab-case** allowed for shell scripts
- Python scripts: PEP 723 inline metadata, runnable via `uv run` (never `pip`, see Python UV below)
- Shell scripts: shebang + `set -euo pipefail`
- Never commit secrets
- Do not add project-level config (`pyproject.toml`, `package.json`, etc.) at root
- Do not mix skill and rule formats in one directory
- New verification rounds get their own `docs/VERIFICATION_<YYYY-MM>/` subdirectory

## Testing

Run the test suite to validate all skills, rules, manifests, and generator drift:

```bash
uv run tests/test_marketplace.py        # all 52 tests
uv run tests/test_marketplace.py -v     # verbose
uv run tests/test_marketplace.py -k rule  # only rule tests
```

The test suite checks: directory structure, YAML frontmatter, catalog consistency, PEP 723 metadata, shell script safety, manifest schema, per-platform per-plugin manifest emission, mirror dir hygiene (no leaked `.claude-plugin/`), kebab-case naming, and secret scanning. Always run the tests before submitting changes.

Run the CI workflow locally with [act](https://github.com/nektos/act) and Docker:

```
./tests/run-ci-local.sh          # run the full GitHub Actions workflow locally
./tests/run-ci-local.sh -n       # dry-run (no container)
```

For full per-platform act verification (Codex/Gemini/Cursor/Claude install + enumeration in Docker), use `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/reproduce.ps1` — see `CONTRIBUTING.md` section "Running act-based verification".

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

The repo's own `rules/no-ai-credit/` rule documents this for downstream users; keep that rule and this section in sync.

## Writing Rules — Keep Them Concise

Rules consume agent context in every session. Verbose rules dilute attention and waste context budget.

- **Aim for actionable checklists, not documentation.** If a rule reads like an essay, it's too long.
- **Every line should be an instruction the agent can act on.** Remove explanations of *why* — agents need *what* and *when*.
- **Consolidate** — 5 crisp bullet points beat 40 lines of prose.
- Rules installed to multiple targets appear multiple times in agent context. Use `--format agents` to install to a single target.
- No code execution. Rules are passive instructions, not scripts. If you need to run code, make it a skill instead.

## Pitfalls Discipline

Maintain `PITFALLS.md` at the repo root. This is the knowledge base of things that went wrong and how they were fixed. (Pre-1.0 entries archived at `docs/archive/pre-1.0-pitfalls.md`.)

### Before complex work

- Check `PITFALLS.md` for entries related to the area you're touching.
- Search git log for relevant fixes: `git log --oneline --grep="<keyword>"`.
- If a past pitfall is relevant, factor it into your approach before writing code.

### After fixing a bug

- Add an entry: **symptom** (what you observed), **cause** (root cause), **fix** (what resolved it), **commit** (reference).
- Keep entries concise — 2-4 lines each.

### Promotion

- If a pitfall recurs across projects, promote it to a user-global rule.
- If a pitfall can be prevented structurally (test, hook, validation), add the guardrail and note it in the entry.

## Python UV

ALWAYS use `uv`. NEVER use `pip`, `pip install`, `virtualenv`, `venv`, `pyenv`, `conda`, or `poetry`. This is non-negotiable for any Python work in this repo.

- **Scripts:** PEP 723 inline metadata + `uv run script.py`
- **Projects:** `uv init`, `uv add`, `uv sync`, `uv run`
- **Virtualenvs:** `uv venv` (never `python -m venv`)
- **Global tools:** `uv tool install` (never `pip install --user` or `pipx`)
- This repo has **no project-level Python deps** (no `pyproject.toml`, no `uv.lock`). Every script declares its own dependencies via PEP 723 inline metadata and runs via `uv run script.py`. Do not add a project-level `pyproject.toml`.
