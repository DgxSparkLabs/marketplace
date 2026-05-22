# Resume Here

**This is the first file to read when returning to this project after any break.** Don't read anything else first.

Written 2026-05-22 at the close of a long working session that completed the migration and designed (but did not yet implement) the multi-platform validation feature. If you're picking this up cold, the next ~3 minutes of reading get you back to where the previous session left off.

---

## 30-Second TLDR

This repo (`DgxSparkLabs/marketplace`) is a **Claude Code plugin marketplace**. The previous session migrated it from a custom Textual TUI installer to native `/plugin marketplace add DgxSparkLabs/marketplace` compliance, then designed the CI/CD validation layer that will verify the marketplace works across six AI-coding-CLI platforms (Claude Code, Codex, Gemini CLI, Cursor, Windsurf, Devin). PR #1 is open with both the migration and the validation design — the validation **implementation** is the next phase and has not started.

---

## You Are Here

```
Active branch:         feat/claude-plugin-compliance
Last commit:           8584dc5 ("docs: second-pass reviewer fixes — drop stale compat-rule.yml reference + minor")
Open PR:               #1 at https://github.com/DgxSparkLabs/marketplace/pull/1
Status:                Migration done; validation design locked; validation implementation NOT STARTED
Working directory:     C:\Users\devic\source\marketplace
Other relevant branch: exp/cli-empirical-discovery (sub-agent's empirical research, contains CI logs)
```

The PR contains everything: the migration (TUI removed, native /plugin compliance achieved) and the validation design (planning docs only — no compat workflow files yet).

---

## Next Concrete Actions (in priority order)

1. **File the GitHub whitelist request** — independent of all other work. Copy-paste the body from `docs/CI_WHITELIST_REQUEST.md` into https://support.github.com/contact. Ask GitHub to permit `@openai/codex` and `@google/gemini-cli` in our org's Actions. Update the doc's "After-the-fact tracking" section with the ticket number once filed. This can happen any time; it doesn't block engineering.

2. **Get PR #1 reviewed and merged** — contains the migration plus all design documents for the future validation work. Once merged, anyone cloning main has the full planning dossier.

3. **Start multi-platform validation implementation** — spawn an implementer agent on a new branch `feat/multi-platform-validation`. The brief is the planning docs themselves. Expected effort: ~15–20 hours across 4 waves per `docs/PLATFORM_VALIDATION_CICD_PLAN.md` Section 8.

If you only have time for one action and want to make forward progress: file the whitelist request. It's the only one with an external dependency (GitHub's response time).

---

## Reading Order (with time budgets)

| Time | Read | Why |
|------|------|-----|
| 90s | This file | Get oriented |
| 3min | `docs/IMPLEMENTING_AGENT_PROMPT.md` | Understand what an implementer agent gets handed |
| 5min | `docs/GOAL_PLUGIN_COMPLIANCE.md` + `docs/PLATFORM_VALIDATION_CICD_PLAN.md` Section 4 (decisions table) | Success criteria + the 20 locked design decisions |
| 10min | `README.md` + `docs/CONSTRUCT_TYPES.md` | What the marketplace ships + the construct vocabulary |
| 20min | `docs/PLAN_PLUGIN_COMPLIANCE.md` + `docs/PLATFORM_INSPECTION_CATALOG.md` + `docs/PLATFORM_VALIDATION_CICD_PLAN.md` (full) | Architecture + empirical CLI catalog + full validation design |
| 30+min | `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` + `docs/CI_WHITELIST_REQUEST.md` + `AGENTS.md` + `HANDOFF.md` + `CHANGELOG.md` | Empirical investigation outcomes + open requests + conventions + change history |

For implementing, the implementing agent should start with the 5-minute tier and reach Section 4 of `PLATFORM_VALIDATION_CICD_PLAN.md` — that's where the 20 locked decisions are. Everything below that is supporting reference.

---

## Project Glossary

Terms in this project have specific meanings. The same word might mean something different elsewhere.

| Term | Meaning here |
|------|--------------|
| **marketplace** | A curated index of installable Claude Code plugins, declared in `.claude-plugin/marketplace.json`. Our marketplace is named `dgxsparklabs-marketplace`. |
| **plugin** | A directory containing `.claude-plugin/plugin.json` plus the content it ships (skill, command, agent, hook, mcp config, etc.). |
| **construct** | One of 10 Claude Code plugin construct types: skill, rule, command, agent, hook, mcp, lsp, monitor, output style, theme. |
| **mirror** | An auto-generated directory under `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, or `.devin/` that copies our generated content into the directory layout each non-Claude-Code CLI expects. |
| **generator** | `scripts/generate_manifest.py` — reads `MARKETPLACE.toml`, `catalog.toml`, `skills/`, `rules/`, `examples/`, produces everything else (`_generated/`, mirrors, `.claude-plugin/marketplace.json`). |
| **inspection command** | An auth-free CLI command that lists or describes locally-loaded content without invoking the model — e.g., `codex mcp list`, `gemini skills list`, `devin rules list`. |
| **auth-free** | A CLI command that runs without an API key, OAuth login, or paid auth. Often inspection-type commands. |
| **catalog tagging** | The `[skill_domain.X]` and `[rule_domain.X]` sections in `catalog.toml` that group constructs into bundles. |
| **domain bundle** | A plugin (e.g., `skills-communication`) whose only job is to declare dependencies on other plugins, so users can install a curated set with one command. |
| **compat workflow** | A `.github/workflows/compat-<construct>.yml` file that verifies our marketplace works for that construct across applicable platforms. Designed but not yet implemented. |
| **match mode** | The shape of a CI assertion against a catalog command's output: `exit-code-only`, `grep <substring>`, `regex <pattern>`, or `exact-diff`. Declared per catalog row. |
| **the trio** | Shorthand for the three core planning docs: `GOAL_PLUGIN_COMPLIANCE.md` + `PLAN_PLUGIN_COMPLIANCE.md` + `INVESTIGATION_PLUGIN_DEPENDENCIES.md`. |
| **the catalog** | Shorthand for `docs/PLATFORM_INSPECTION_CATALOG.md` — the executable spec for CI assertions. |
| **the validation plan** | Shorthand for `docs/PLATFORM_VALIDATION_CICD_PLAN.md` — the CI/CD design. |
| **the migration** | The work that took the marketplace from TUI installer to native /plugin marketplace add. Now complete. |
| **the validation** | The work that will add multi-platform CI/CD verification. Design complete, implementation not started. |
| **blocked platforms** | Codex and Gemini. Their npm packages (`@openai/codex`, `@google/gemini-cli`) are blocked at the GitHub Actions org policy level. CI cannot install them currently. |
| **wave** | Implementation phase in the validation plan. Wave 1 = Claude-only workflows. Wave 2 = free-in-CI matrix workflows. Wave 3 = blocked-platform advisory + local-dev fallback. Wave 4 = promotion after whitelist arrives. |
| **continue-on-error** | The YAML idiom (`continue-on-error: true` at job level) that makes Codex/Gemini failures advisory: they're visible in the PR UI but don't block merge. |
| **template fixture** | `examples/example-<construct>/` — the canonical reference plugins. Used as test subjects for compat workflows. Stable contract: don't rename or delete without updating the workflow. |
| **`activate.sh`** | Per-rule plugin shell script that symlinks (or copies on Windows) the rule file into `.claude/rules/`. Workaround for the lack of a `rules` field in Claude Code's plugin spec. |

---

## Top Decisions with Rationale

The full 20-decision table is in `docs/PLATFORM_VALIDATION_CICD_PLAN.md` Section 4. The ones below are the ten most consequential — the ones that, if reversed, would change the architecture substantially.

| # | Decision | Why |
|---|----------|-----|
| 1 | **Per-construct workflows, not per-platform** | A new construct type = one new workflow file. A new platform = a matrix entry to N existing workflows. Matches the marketplace's domain model (construct is the primary axis). |
| 2 | **Required for non-blocked platforms; advisory for blocked (Codex, Gemini) via `continue-on-error: true`** | GitHub Actions blocks the Codex/Gemini npm packages at org policy level. Honest failure surfacing without blocking PR merges. |
| 3 | **No gating variable for blocked platforms** | The CLI install attempt itself is the gate. When GitHub lifts the block (or whitelist arrives), workflows start passing on the next run with zero code changes. Beats a `vars.X_WHITELIST_GRANTED` toggle that nobody would remember to flip. |
| 4 | **`compat-rule.yml` does NOT exist** | Rules aren't installable via plugins on any platform. They use the `activate.sh` symlink workaround for Claude. Rule format validation lives in `tests/test_marketplace.py` instead. |
| 5 | **Per-row Match Mode column in the catalog** | Without explicit match modes, 11 workflows would invent 11 ways to compare command output. Per-row commitment prevents drift. Default is `grep <substring>`; explicit override per row when needed. |
| 6 | **Each compat workflow runs `generate_manifest.py --write` as first step** | Workflows are self-contained: they regenerate `_generated/` fresh from sources rather than trusting the committed tree. Isolates compat failures from generator drift. |
| 7 | **Float to `@latest` for npm-installed CLIs (Codex, Gemini)** | Catches real-world CLI changes immediately. Pinning lies about reproducibility — the CLI changes upstream regardless of our pin. Per the platform-breakage policy (#7 in the table), a breakage blocks release until catalog + assertions are updated. |
| 8 | **Standard composite action contract** | Every `setup-<platform>/action.yml` takes `inputs.version` (default `'latest'`) and emits `outputs.installed` (boolean). Uniform shape across all 5 setup actions. |
| 9 | **Per-job test isolation, not per-step** | Each matrix cell on a fresh `ubuntu-latest` runner. Higher CI cost but no risk of one platform's CLI install polluting another's environment. Cleanup discipline becomes less load-bearing. |
| 10 | **Triggers: PR to main + push to main + push to feat/** + workflow_dispatch** | Catches issues at PR time AND on feature-branch commits. Manual dispatch available for ad-hoc verification. Comprehensive but not so noisy as to drown the runner pool. |

---

## Dead Ends — What We Tried That Didn't Work

Avoid re-litigating these. Each is one or more hours of conversation that ended in "no."

| Idea | Why we rejected it |
|------|-------------------|
| **Web research for current CLI surfaces** | Docs from December 2025 were stale by May 2026 for fast-moving CLIs (`gemini skills` subcommand existed but no research surfaced it). Switched to empirical CI + local exploration. |
| **Council of 6 specialist agents** to review the design | Theatrical / overkill for the scope. Reviewer push-back collapsed it to 1 platform researcher + 1 devil's advocate. |
| **Hooks-based rules validation** (UserPromptSubmit hook per rule) | Clunky pattern that the user correctly called "stupid." Rules aren't installable as plugins on any platform; format validation in the test suite is the right primitive. |
| **`force-for-plugin: true` output styles for rules** | Single-winner (only one can apply at a time). Doesn't compose across multiple installed rule plugins. |
| **`vars.CODEX_WHITELIST_GRANTED` gating mechanism** | Adds a state variable nobody would remember to flip. `continue-on-error: true` alone makes the workflow advisory; when the block lifts, the install just succeeds. Zero ceremony. |
| **Soft-deprecation of the TUI installer** | User wanted full removal in the migration branch, not a deprecation period. Single PR ships the breaking change with migration notes. |
| **Per-platform workflow organization** | Was the initial framing. User reframed to per-construct ("new construct = one workflow; new platform = matrix row in N workflows"). Cleaner. |
| **Trying to install `@openai/codex` / `@google/gemini-cli` in GitHub Actions** | Blocked at the org policy level (0-second failures across 12+ variants). Local exploration is the empirical fallback; whitelist request is the long-term unblock. |
| **Pinning CLI versions in CI** | Decided against — pinning lies about reproducibility because the upstream CLI evolves regardless. Float to `@latest` and let the platform-breakage policy handle change. |
| **Caching CLI installs across CI runs** | Deferred to Wave 1/2 implementation. Empirical decision: measure first, optimize if CI minutes become a problem. |

---

## Methods That Worked

Patterns to reuse. These shaped how this session reached convergence.

- **Spawn a reviewer agent after locking decisions** — second-opinion review catches blind spots the locked-in author misses. We did this twice; both caught real issues.
- **`AskUserQuestion` with 3 explicit options + a Recommended marker** — concrete picks beat open-ended prose. Most decisions took less than 30 seconds once posed as choices with defaults.
- **Empirical CI exploration on a research branch** — when stale docs distrust, push experiment workflows to a throwaway branch and let CI logs be the evidence. `exp/cli-empirical-discovery` has the logs.
- **Local CLI exploration when CI is blocked** — GitHub Actions can't install everything; the local dev machine can. Two complementary empirical vantage points.
- **Per-decision iteration cycle** — reviewer flags ambiguity → AskUserQuestion → doc edit → next reviewer pass. Three rounds converged on a clean design.
- **Catalog-as-executable-spec** — `PLATFORM_INSPECTION_CATALOG.md` rows transcribe 1:1 into CI assertions. Catalog + workflow stay synchronized because one drives the other.
- **Single source of truth for identity** — `MARKETPLACE.toml` is the only place where owner / repo URL / version / license live. Generated manifests inherit from there. Renames or version bumps are one-line edits.
- **Construct-axis organization** — when in doubt, organize by what's being shipped (skill, rule, command…), not by what's consuming it (Claude, Codex, Gemini…).
- **"If it fails it fails" gating** — for blocked external dependencies, the failure itself is the gate. No state variable, no toggle, no promotion ceremony.

---

## Active Branches and Their State

| Branch | Purpose | Status |
|--------|---------|--------|
| `main` | Production | Current; doesn't yet have the migration |
| `feat/claude-plugin-compliance` | Migration + validation design | All work; PR #1 open; ready to merge |
| `exp/cli-empirical-discovery` | Sub-agent's empirical CLI research | Contains CI experiment workflows + per-platform findings docs; not for production merge |
| `feat/multi-platform-validation` | The implementation of the validation design | **DOES NOT EXIST YET.** This is where the implementer agent will work |

---

## Task List Snapshot

```
#1–#13  ✅ Migration work (catalog, generator, examples, mirrors, deprecation, tests, docs, e2e verification, PR open)
#14     ✅ GitHub whitelist request drafted (docs/CI_WHITELIST_REQUEST.md — ready to file)
#15     ✅ First reviewer pass complete (14 items flagged)
#16     ✅ Critique iteration cycle complete (3 decision rounds + 2 reviewer passes → clean)
#17     ⏳ Multi-platform validation implementation — waiting to start
```

---

## When You Forget Everything

Re-read this file. Then:

1. If you need WHAT to do next → "Next Concrete Actions" section above
2. If you need WHY a decision was made → "Top Decisions with Rationale" section
3. If you're about to repeat a mistake → "Dead Ends" section
4. If you don't recognize a term → "Project Glossary"
5. If you need full architecture → `docs/PLAN_PLUGIN_COMPLIANCE.md` + `docs/PLATFORM_VALIDATION_CICD_PLAN.md`
6. If you're the implementer → `docs/IMPLEMENTING_AGENT_PROMPT.md` is the brief

The work from May 2026 was deliberate. Each decision recorded here was made with at least one round of review. When in doubt, trust the locked decisions over fresh intuition — the rationale is documented; the alternatives were considered and rejected.

If anything seems wrong, the planning docs aren't the bug — start by reading carefully. The architecture earned its complexity through deliberate iteration; reverting it without going through the same depth of review will introduce the dead ends listed above.
