# Multi-Platform Validation Implementation Brief

The brief to hand to a sub-agent that will implement the multi-platform CI/CD validation feature designed during the May 2026 working session. The design is fully locked across 20 decisions; this brief points the implementer at the canonical planning artifacts and constrains scope so they execute the locked design rather than re-design it.

Copy-paste the section "The Prompt" below into a sub-agent invocation. Recommended: `general-purpose` or `claude` subagent type, `sonnet` model, foreground (so progress is visible) or background (so it runs while you do other things).

---

## The Prompt

```
You're implementing the multi-platform CI/CD validation feature for the
DgxSparkLabs/marketplace project. The design is fully locked — your job
is execution, not design.

## Your starting point

- Working directory: `C:\Users\devic\source\marketplace`
- Start by creating a new branch: `feat/multi-platform-validation` off
  `main` (or off `feat/claude-plugin-compliance` if PR #1 hasn't merged
  yet — the design docs are on that branch). Confirm the branch with
  `git branch --show-current` before any other action.

## Required reading, in order, in full

Do not skim. The planning dossier is the contract; the design is locked
through three rounds of reviewer-driven refinement. Do not re-litigate
locked decisions.

1. `docs/RESUME_HERE.md` — 30-second TLDR, project glossary, the 10 top
   decisions with rationale, and the dead-ends table (with "trigger to
   watch for" column for the patterns to avoid).
2. `docs/PLATFORM_VALIDATION_CICD_PLAN.md` — the CI/CD design. Section
   3 (workflow inventory), Section 4 (all 20 locked decisions), Section
   5 (composite action contracts), Section 6 (per-workflow specs),
   Section 7 (Codex/Gemini strategy), Section 8 (implementation
   phasing).
3. `docs/PLATFORM_INSPECTION_CATALOG.md` — empirical CLI commands per
   platform. The Match Mode Convention section is critical: each row's
   "after-install output" is matched per the row's declared mode.
4. `docs/IMPLEMENTING_AGENT_PROMPT.md` (for context on how the prior
   implementer was briefed for the migration — same project conventions
   apply to this work).

## Your mission

Implement what the validation plan describes. Specifically, deliver:

- **Ten `.github/workflows/compat-*.yml` files** per the inventory in
  PLATFORM_VALIDATION_CICD_PLAN.md Section 3:
  `compat-skill.yml`, `compat-command.yml`, `compat-agent.yml`,
  `compat-hook.yml`, `compat-mcp.yml`, `compat-extension.yml`,
  `compat-monitor.yml`, `compat-output-style.yml`, `compat-theme.yml`,
  `compat-marketplace-add.yml`.

  Each workflow has the shape specified in Section 6 (per-workflow
  specs) with assertions transcribed 1:1 from the matching catalog rows
  in PLATFORM_INSPECTION_CATALOG.md. Match modes per the catalog.

- **Five composite actions** under `.github/actions/` per
  PLATFORM_VALIDATION_CICD_PLAN.md Section 5:
  `setup-claude/`, `setup-codex/`, `setup-gemini/`, `setup-devin/`,
  `setup-cursor-doctor/`. All follow the standard contract:
  `inputs.version` (default `'latest'`) + `outputs.installed` boolean.

- **Two local-dev fallback scripts** for the platforms blocked from
  GitHub Actions (Codex, Gemini) per Section 7:
  `scripts/validate-codex-local.sh`, `scripts/validate-gemini-local.sh`.
  Contributors with the CLIs installed locally can run these to
  validate before opening PRs.

## Locked decisions (do not re-litigate)

Read all 20 in PLATFORM_VALIDATION_CICD_PLAN.md Section 4. The most
load-bearing for implementation:

- Each compat workflow runs `uv run scripts/generate_manifest.py
  --write` as its first step (decision #13) — regenerates `_generated/`
  fresh from sources; do NOT trust the committed tree.
- Triggers: `on: pull_request` to `main` + `on: push` to `main` +
  `feat/**` + `workflow_dispatch` (decision #12).
- Concurrency block on every workflow: `concurrency: { group:
  '${{ github.workflow }}-${{ github.ref }}', cancel-in-progress: true }`
  (decision #19).
- Per-job runner isolation: each matrix cell on a fresh `ubuntu-latest`
  (decision #6).
- Codex/Gemini matrix entries have `continue-on-error: true` at the
  JOB level (decision #10). This makes them advisory; they will fail at
  install time because GitHub Actions blocks `@openai/codex` and
  `@google/gemini-cli` at the org policy level (verified empirically).
  When the block lifts (whitelist arrives), they will start passing on
  the next CI run with zero code changes. Do NOT add a
  `vars.CODEX_WHITELIST_GRANTED` toggle or any gating variable
  (decision #16).
- CLI versions: float to `@latest` for npm-installed CLIs (decision
  #14). Do NOT pin to specific versions in setup actions.
- Devin assertions: explicit `working-directory: ${{ github.workspace }}`
  + `grep -i` (decision #15).
- Output match modes per the catalog's per-row "Match Mode" column
  (decision #9).
- No defensive `remove-if-exists` for marketplace re-registration —
  trust runner ephemerality (decision #18).

## Out of scope (do not do)

- Do NOT create `compat-rule.yml` (decision #11 — rules aren't
  installable via plugins; rule format validation lives in
  `tests/test_marketplace.py`).
- Do NOT redesign the workflow organization to per-platform
  (decision #1 — the locked design is per-construct with platform
  matrix per workflow).
- Do NOT add caching strategies preemptively (Section 9 — deferred to
  empirical resolution during implementation; measure first).
- Do NOT propose new construct types or platforms.
- Do NOT touch the migration architecture (PR #1 territory).
- Do NOT propose alternatives to the 20 locked decisions. If you find
  ambiguity that the locked decisions don't resolve, surface it as a
  question; do not silently guess.

## Discipline

- Use TaskCreate to break the implementation into trackable tasks.
  Suggested decomposition mirrors the Wave 1–4 phasing in Section 8.
- Mark each task `in_progress` before starting, `completed` immediately
  when done. Never batch updates.
- Commit after each meaningful step. Use clear conventional commit
  messages. NEVER include AI co-author attribution (see
  `rules/no-ai-credit/`).
- Run `uv run tests/test_marketplace.py` after each change.
- Run `uv run scripts/generate_manifest.py --check` periodically to
  ensure no drift in `_generated/`.
- When you encounter design ambiguity, surface it as an
  `AskUserQuestion` with 3 explicit options + a Recommended marker. Do
  not guess.

## Methods to use (these worked in the design phase, reuse them)

- Catalog-as-executable-spec: every CI assertion comes from a catalog
  row. No catalog row → no assertion.
- Empirical verification over docs: if you wonder whether a CLI
  command behaves a certain way, install it locally and run it.
- AskUserQuestion with 3 options + Recommended for any ambiguity.

## What "done" looks like

A successful PR (`feat/multi-platform-validation` → `main`) containing:

- 10 `compat-*.yml` workflows
- 5 composite actions
- 2 local-dev validation scripts
- Documentation updates (the existing planning docs reference these
  workflows; verify the references resolve to real files)
- All workflows verified to either pass or fail as designed (Codex/
  Gemini fail at install on github.com; that failure is the advisory
  signal per decision #10)
- Tests pass (`uv run tests/test_marketplace.py`)
- Manifest drift check passes (`uv run scripts/generate_manifest.py
  --check`)

Estimated effort: 15–20 hours per the phasing in Section 8.

## When to ask the user

The user wants to be involved when:

- The locked decisions don't unambiguously answer a question you face
  during implementation
- You discover a real bug or inconsistency in the planning docs (vs.
  the empirical CLI surface)
- You finish a Wave and want a checkpoint before starting the next
- You hit a blocker that needs a decision

Pose all of these as `AskUserQuestion` calls with 3 explicit options.

## When NOT to ask the user

The user does not want to be involved when:

- A locked decision answers the question (just follow the decision)
- A NICE-level deferred question (Section 9 of the validation plan)
  comes up in a context where you can resolve it empirically (measure
  and decide; document your choice in a commit message)
- You hit a routine implementation question that doesn't affect
  architecture
- You want to re-litigate any locked decision (just don't — surface
  the underlying concern instead, framed as "this assumption may not
  hold because X" rather than "let's revisit decision Y")

## First action

After reading the four required-reading files in full:

1. Create branch `feat/multi-platform-validation` off the appropriate
   base.
2. Use TaskCreate to break Wave 1 of Section 8 into ~5 trackable tasks.
3. Mark the first task `in_progress`.
4. Begin implementation.

Good luck. The design earned its complexity through deliberate
iteration; trust the locked decisions and execute.
```

---

## Notes for Whoever Spawns This Agent

- The brief is self-contained. Don't preface it with additional context — the agent's job is to find context on disk, not from you.
- If this is being spawned post-compaction, the durable artifacts on disk are what matters; the chat history is not.
- Run it with `run_in_background: true` if you want to do other things while it works (~15–20 hour task, but it'll commit in small steps you can monitor via `git log`).
- Reasonable check-in cadence: after each Wave commits, verify the wave's scope matches Section 8 expectations.
