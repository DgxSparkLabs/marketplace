---
date: 2026-05-24
purpose: how to add things, test, follow conventions
status: live
---

# Contributing

This is the canonical contributor doc. For the step-by-step "how do I add a skill / rule / hook / ...?" walkthrough, the authoritative file is [[ADDING_A_CONSTRUCT]] — this doc covers the broader workflow (quickstart, testing, conventions, output discipline). Hub-and-spoke: when this file mentions adding a construct type, it points at [[ADDING_A_CONSTRUCT]] rather than duplicating the steps.

## Quickstart

```bash
# 1. Clone
git clone https://github.com/DgxSparkLabs/marketplace
cd marketplace

# 2. Install uv (Python's modern dep manager — required; we don't use pip)
# macOS/Linux:    curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PS):   irm https://astral.sh/uv/install.ps1 | iex

# 3. Run the test suite (should all pass)
uv run scripts/tasks.py test            # runs all four suites at once

# 4. Regenerate manifests + mirrors from sources
uv run scripts/generate_manifest.py

# 5. View the generated outputs
ls _generated/                          # per-plugin wrappers (one per construct + bundles)
cat .claude-plugin/marketplace.json     # top-level manifest (plugin count: see docs/INVENTORY.md, generated/authoritative)
ls .agents/skills/                      # cross-platform skill mirror (Windsurf/Cursor/Devin)
```

No project-level Python deps. Every script declares its own dependencies via PEP 723 inline metadata and runs via `uv run script.py`.

## Adding things

### Add a new skill

Copy `src/skills/example-single/` to `src/skills/<your-skill-name>/`, edit the `SKILL.md` frontmatter and body, then regenerate. The full step-by-step is in [[ADDING_A_CONSTRUCT]]; the frontmatter field reference is in [[SKILL_FORMAT]].

### Add a new rule

Copy `src/rules/example/` to `src/rules/<your-rule-name>/`, edit `rule.md` (and the `formats/` files for Cursor/Windsurf if needed), regenerate. See [[ADDING_A_CONSTRUCT]] for the workflow and [[RULE_FORMAT]] for the multi-format spec (rule.md + Windsurf + Cursor + AGENTS.md).

### Add a new MCP server / hook / agent / etc.

Same pattern — copy `src/<construct>/<name>/`, edit, regenerate. The full per-construct table (source dir, example template, description source) is in [[CONSTRUCT_TYPES]]; the workflow is identical for all 10 construct types per [[ADDING_A_CONSTRUCT]].

### Add a new construct type

Adding an 11th construct type means writing a new class in `scripts/constructs.py` implementing the `Construct` protocol (`prefix`, `source_directory`, `category`, `build_plugin_json`, `emit`) and registering it in the `CONSTRUCTS` dict. Then declare `supports` membership in any `Platform` class that should host it (see [[ARCHITECTURE#The two protocols]]). Phase 1 picks up the new construct automatically; Phase 1.5 emits per-platform manifests via the `supports` gate. No generator-loop changes needed.

### Add a new platform

Adding a new platform means writing a new class in `scripts/platforms.py` implementing the `Platform` protocol (`name`, `mirror_directory`, `supports`, `emit`, `build_plugin_json`) and registering it in the `PLATFORMS` dict. Phase 1.5 emits per-plugin manifests automatically wherever `type(construct) in platform.supports`; Phase 3 calls `platform.emit` for every supported construct instance. See [[ARCHITECTURE#The seven platform classes]] for shape examples (especially `AgentsPlatform` as the simplest case).

## Submission flow

When you're ready to contribute changes back upstream:

1. **Fork the repository** on GitHub (outside contributors need a fork; team members with write access can skip this).
2. **Create a branch** from `main`: `git checkout -b your-branch-name`.
3. **Make your changes** per the [[#Adding things]] section above.
4. **Regenerate and check for drift**: `uv run scripts/generate_manifest.py --check`. This must exit 0.
5. **Validate generated plugin manifests** (see [[#Running `claude plugin validate`]] below): `claude plugin validate _generated/<your-plugin>` for each plugin you added or changed, AND `claude plugin validate ./` for the marketplace as a whole. Both must produce zero warnings — CI gates on this via `.github/workflows/compat-validate.yml`.
6. **Run the test suite**: `uv run scripts/tasks.py test` (runs all four suites — `test_marketplace`, `test_schema_fitness`, `test_agents_cli`, `test_tooling`). All must exit 0.
7. **Open a PR** against `main`. See the [[#PR-only flow (never push to main)]] convention below.

## Testing

### Running the test suite

```bash
uv run scripts/tasks.py test            # all four suites at once (recommended)
uv run tests/test_marketplace.py        # marketplace tests
uv run tests/test_schema_fitness.py     # platform-schema-fitness tests
uv run tests/test_agents_cli.py         # agents-cli tests
uv run tests/test_tooling.py            # contributor-tooling tests
uv run tests/test_marketplace.py -v     # verbose
uv run tests/test_marketplace.py -k rule  # only rule-related tests
```

Tests live in four files:

- `tests/test_marketplace.py`: directory structure, YAML frontmatter parity, catalog consistency, generator drift, manifest schema, per-platform per-plugin manifest emission, mirror dir hygiene (no leaked `.claude-plugin/`), secret scanning.
- `tests/test_schema_fitness.py`: per-platform schema fitness — validates emitted manifests against reference JSON Schemas captured directly from each platform's docs (Cursor `SkillConstruct` plugin.json, Gemini `AgentConstruct` frontmatter, Windsurf hooks event names + shape, Cursor hooks shape + `version` presence, Gemini hooks event-name vocabulary, marketplace.json description presence, LSP / monitor / theme / hook example schemas).
- `tests/test_agents_cli.py`: the agents-CLI surface.
- `tests/test_tooling.py`: the contributor tooling — `new_construct.py` scaffolder and `validate_source.py` pre-commit check.

Always run all four before committing (or just `uv run scripts/tasks.py test`).

The drift gate (`uv run scripts/generate_manifest.py --check`) runs in CI and exits 1 if regenerated output differs from committed output. Run it before pushing if you've changed anything under `scripts/`, `src/<construct>/`, or `src/MARKETPLACE.toml`/`src/catalog.toml`.

### Running `claude plugin validate`

This marketplace gates CI on `claude plugin validate ./` producing zero warnings (per `.github/workflows/compat-validate.yml`, added 2026-05-26). Contributors should run validate locally before pushing to catch warnings and errors the byte-identical drift check is blind to.

**What it does**:

```bash
# Validate the entire marketplace (top-level marketplace.json + every per-plugin manifest)
claude plugin validate ./

# Validate one specific plugin
claude plugin validate _generated/skill-my-skill
```

Per [code.claude.com/docs/en/plugins-reference#unrecognized-fields](https://code.claude.com/docs/en/plugins-reference#unrecognized-fields) (fetched 2026-05-26), Claude's validator catches misspelled field names, fields left over from other tools' manifests, and other schema-shape problems. `--strict` promotes any warning to an error (CI uses a portable equivalent: grep the output for `warning|error` and fail).

**When to run it**:

- After adding a new plugin (any construct type).
- After editing any `src/<construct>/<plugin>/.claude-plugin/plugin.json`, `src/MARKETPLACE.toml` description, or any source file the generator inlines into `_generated/<plugin>/.claude-plugin/plugin.json`.
- Before opening or updating a PR — CI will fail if your changes introduce any warning or error.

**How CI enforces it**:

The `.github/workflows/compat-validate.yml` workflow runs on every PR and push to `main`. It:

1. Regenerates manifests from sources (`uv run scripts/generate_manifest.py`).
2. Installs the Claude CLI via `./.github/actions/setup-claude`.
3. Runs `claude plugin validate ./` and fails the build if the output contains any warning or error (case-insensitive grep).

If CI fails here but the drift check passed, the offending file is one of: top-level `.claude-plugin/marketplace.json` (e.g., missing `description`), an inlined per-plugin `plugin.json` field name typo, or an unrecognized field the validator does not expect. Run validate locally to see the exact warning message; fix at source; regenerate; re-validate.

**Common warnings and how to fix them**:

| Warning | Cause | Fix |
|---|---|---|
| `description: No marketplace description provided` | Top-level `description` missing from `marketplace.json` | Add a `description` field to `src/MARKETPLACE.toml` — the generator propagates it to the top-level `.claude-plugin/marketplace.json`. |
| `Unrecognized field "<name>"` in a `plugin.json` | Typo or stale field name | Compare against the [Claude plugin manifest schema](https://code.claude.com/docs/en/plugins-reference#manifest-schema); fix at the source file the generator copies. |
| LSP / monitor / theme / hook schema errors | Source content uses an invented schema shape | See `docs/archive/claude-qa-2026-05-26/RESEARCH.md` Findings 2-5 for canonical schemas with examples. |

### Running act-based verification

For hermetic local-container CI re-verification before pushing:

```powershell
# From repo root (Windows PowerShell)
docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/reproduce.ps1
```

The script runs four verification workflows (`verify-codex.yml`, `verify-gemini.yml`, `verify-cursor.yml`, `verify-claude.yml`) via nektos/act 0.2.63+ in Docker containers. Each workflow's full stdout/stderr lands in `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/logs/verify-<platform>-run.log`; per-claim snippets are extracted to `logs/<ID>.txt`. Prerequisites: act + Docker Desktop + the `catthehacker/ubuntu:act-latest` image pulled. See the script for the full command sequence.

## Conventions

### No AI co-author attribution in commits

Never attribute work to any AI agent, tool, or assistant in commits, PRs, code comments, documentation, READMEs, changelogs, or any other output. No "Co-Authored-By" lines referencing an AI/bot. No "Generated with", "Created by", "Built with", "Powered by" followed by an AI tool name. No `noreply@` email addresses for AI bots. The repo's own [`no-ai-credit`](archive/rules-pre-stable-2026-05-26/no-ai-credit/) rule (archived pending re-add per ROADMAP #16–18) documents this; check for and remove any such lines before finishing a task.

### PR-only flow (never push to main)

`main` is protected. All changes go through PRs. The branch policy at `HANDOFF.md` keeps a record of which branch each phase shipped on. The Phase 5 work shipped on `feat/claude-plugin-compliance` and was merged to `main` at `bfb476d`. Follow-up cleanup typically gets its own branch (e.g., `docs/post-merge-cleanup`).

### Use uv, not pip

ALWAYS use `uv`. NEVER use `pip`, `pip install`, `virtualenv`, `venv`, `pyenv`, `conda`, or `poetry`.

- Scripts: PEP 723 inline metadata + `uv run script.py`
- Projects: `uv init`, `uv add`, `uv sync`, `uv run`
- Virtualenvs: `uv venv` (never `python -m venv`)
- Global tools: `uv tool install` (never `pip install --user` or `pipx`)

Python 3.11+ (we use `match`, `Protocol[runtime_checkable]`, etc.). Shell scripts need `set -euo pipefail` and a shebang.

### Obsidian vault conventions

This repo is also an Obsidian vault. When you write `.md` files:

- `[[Note]]` — link for *further reading*. Each link should mean something; don't link every mention of a word.
- `[[Note#Heading]]` — section-level link.
- `![[Note]]` / `![[Note#Heading]]` — transclude when content is needed *in place*. Use sparingly.
- `#tag` (nested `#topic/sub` welcome) — group by topic. lowercase, singular.
- Frontmatter properties — for facts *about* the note (status, type, date). Use these instead of tags for anything typed.
- Folders — group by type, not topic. A file has many tags but one location.

### Output discipline (no emojis unless asked, no narration without artifacts)

The user explicitly distrusts narration-without-artifacts. The work product is the file on disk, not the chat summary. Some specific rules carried into the project from the user's global discipline:

- **Verify your work.** Run the code. If it produces output, inspect it. If it has side effects, confirm they occurred. Never say "should work" — say "verified, here's the evidence."
- **State what was tested and what remains untested.** Pause for what only the user can provide (API keys, OAuth, policy decisions). Everything else, figure it out yourself.
- **Redirect verbose commands to files.** Use `command > output.log 2>&1` for anything that produces more than a screenful. Never pipe long output into your context. Extract with targeted reads (`tail`, `grep`).
- **Diagnose failures from the end.** `tail -n 50 output.log` gets you the stack trace; do not read from the top.
- **Never use `tee` for long-running commands.** It floods context with the same output you saved to disk.
- **Delete temporary output files when done.** Log files are diagnostic tools, not artifacts.
- **Blast-radius estimation.** Before any change: how many files? (>5 = break it up.) How complex? Can you revert cleanly? Small atomic changes, one commit one purpose.
- **Simple > clever.** Removing code that preserves results is always a win. Marginal gains do not justify ugly complexity. Every line you add must be read, maintained, and debugged by the next agent — earn each line.
- **Revert on failure.** Commit a known-good state before experimenting. Define "better" before changing code. If the metric didn't improve, `git reset --hard HEAD` and try a different angle. Three tries without improvement → abandon and pivot.
- **Document lifecycle.** Three tiers, no more. Rules in `AGENTS.md` (conventions; max ~200 lines; no changelogs). Reference in `HANDOFF.md` (current state; updated in-place after behavior-changing commits). History in `CHANGELOG.md` (append-only).
- **Autonomous persistence.** Don't pause to ask "should I keep going?" The human may be away. Only pause for what you genuinely cannot provide yourself.

For the longer-form versions of these rules (Verification Ladder, Improve the Process, Session Resilience, Stay Motivated, Task Formation, Continuous Improvement), see the user-global excerpts imported into [`AGENTS.md`](../AGENTS.md) — they apply project-wide and are not duplicated here.

### Writing rules — keep them concise

Rules consume agent context in every session. Verbose rules dilute attention and waste context budget.

- Aim for actionable checklists, not documentation. If a rule reads like an essay, it's too long.
- Every line should be an instruction the agent can act on. Remove explanations of *why* — agents need *what* and *when*.
- Consolidate — 5 crisp bullet points beat 40 lines of prose.
- No code execution. Rules are passive instructions, not scripts. If you need to run code, make it a skill instead.

## References

- [[HANDOFF]] — long-form project state tracker
- [[README]] — user-facing entry point (install + Quick Start)
- [[ARCHITECTURE]] — generator architecture (Construct + Platform protocols, generation phases)
- [[ARCHITECTURE#Things worth knowing]] — system invariants worth knowing when contributing (bundle dependency auto-install, kebab-case validation, mirror hygiene)
- [[PLATFORMS]] — per-platform install/support reference
- [[ADDING_A_CONSTRUCT]] — primary contributor walkthrough
- [[CONSTRUCT_TYPES]] — 10-construct reference table
- [[RULE_FORMAT]] — rule format spec (rule.md + Windsurf + Cursor + AGENTS.md)
- [[SKILL_FORMAT]] — SKILL.md frontmatter and body spec

---

*Last updated: 2026-06-03.*
