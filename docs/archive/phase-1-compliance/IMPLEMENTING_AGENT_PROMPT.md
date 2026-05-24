# Implementing Agent Prompt

The prompt below is the handoff brief for the agent that will execute the `feat/claude-plugin-compliance` branch. Copy it verbatim into a fresh Claude Code session opened in this repository, or pipe it to the Agent tool with `subagent_type: claude`.

The prompt is deliberately short. Detail lives in the planning docs it points at — keep it that way. If architecture changes, update `GOAL_PLUGIN_COMPLIANCE.md` and `PLAN_PLUGIN_COMPLIANCE.md`, not this prompt.

---

## The prompt

```
You're picking up a Claude Code skills marketplace migration at
`C:\Users\devic\source\marketplace`. Verify you're on the branch
`feat/claude-plugin-compliance` (`git branch --show-current`) before
any other action.

## Mission

Migrate this marketplace from a curl-bootstrapped Textual TUI installer
to native Claude Code `/plugin marketplace add DgxSparkLabs/marketplace`
compliance. Support both individual and domain-bundle installs across
all 10 Claude Code construct types (skills, rules, commands, agents,
hooks, mcps, lsps, monitors, output styles, themes). Ship one
reference `example-*` plugin per construct type so future contributors
can copy-and-adapt instead of reading docs.

The TUI installer (`install.py` + `scripts/install.sh`) and all legacy
install scripts are DELETED in this branch — full removal, no
backwards-compat shim. The only install path after this branch merges
is `/plugin marketplace add` (or the auto-generated cross-platform
mirrors for non-Claude-Code tools).

## Required reading, in order, in full

Do not skim. The planning dossier is the contract.

1. `AGENTS.md` — project conventions (commit hygiene, no AI attribution,
   PEP 723 + uv discipline)
2. `docs/GOAL_PLUGIN_COMPLIANCE.md` — what done looks like
   (12 binary pass/fail criteria + explicit out-of-scope list)
3. `docs/PLAN_PLUGIN_COMPLIANCE.md` — full architecture, naming
   conventions, repository layout, task execution order, risks
4. `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` — the one open question
   gating bundle work; includes its own experiment and fallback design

After reading, run `TaskList` to see the 12 existing tasks.

## Task execution order

Locked in `PLAN_PLUGIN_COMPLIANCE.md`:

   #12 → #13 → #2 → #3 → #4 → #5 → #9 → #6 → #7 → #8 → #10

Task #12 first: rename `ForkYoraiLevi` → `DgxSparkLabs` everywhere
(simple but blocking — subsequent generated files inherit the URLs).

Task #13 second and blocking: empirically verify Claude Code's
dependency auto-install behavior per the experiment documented in
`docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md`. Append the outcome to
that file. If the outcome is anything other than "deps auto-install,"
apply Option 2 fallback (bundles ship `install-deps.sh`) when you reach
task #3.

## Discipline

- Mark each task `in_progress` BEFORE starting it, `completed`
  immediately when done. Never batch updates.
- Commit after every meaningful step. Never include AI co-author
  attribution in commit messages (see `rules/no-ai-credit/`).
- Run the test suite after each change: `uv run tests/test_marketplace.py`.
- When the planning docs don't cover a decision, surface a question
  rather than guessing. Do not expand scope on your own initiative.

## What is locked (do not re-litigate)

The Architecture and Repository Layout sections of
`PLAN_PLUGIN_COMPLIANCE.md` are decided. In particular:

- 8 skill domains; prefix naming (skill-/skills-, rule-/rules-, etc.)
- Dependency-only domain bundles, with Option 2 fallback if task #13
  proves dep auto-install does not work
- Path 2 rules architecture: rules ship as plugins but require a manual
  `activate.sh` symlink step after install
- 10 `example-*` reference plugins, one per construct type
- Cross-platform mirrors (`.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`)
  auto-generated and committed
- TUI installer + all legacy install scripts are DELETED in this branch
  (install.py, scripts/install.sh, scripts/install-rule.sh,
  rules/*/install.sh). No backwards-compat shim.
- SKILL.md frontmatter is unchanged. PEP 723 + `uv` scripts stay.

## What is out of scope

The OUT_OF_SCOPE section of `GOAL_PLUGIN_COMPLIANCE.md` is the source
of truth. Notably: do NOT migrate scripts off PEP 723, do NOT add new
skills or rules unrelated to the migration, do NOT fix the rule
duplication / contradiction issues from earlier reviews, do NOT ship a
backwards-compat shim for the deleted curl-bash install. If you spot
worthwhile out-of-scope work, file it in `PITFALLS.md` or as a new
task — do not expand this branch.

## Done condition

All 12 criteria in `docs/GOAL_PLUGIN_COMPLIANCE.md` pass. Then open a
PR to `main` whose description references the three planning docs and
explains the migration concisely — including the deletion of the TUI
and the new install path for existing users.
```

---

## How to use it

**Option A — Fresh Claude Code session (recommended for long execution):**
Open Claude Code in `C:\Users\devic\source\marketplace`. Paste the prompt as the first message. The agent reads its own `AGENTS.md` + the planning docs and begins. This is the right path for a multi-task workload like this branch.

**Option B — Sub-agent via the Agent tool:**
Use `subagent_type: claude` and the prompt above. Best for delegating execution while monitoring from another session. A sub-agent has its own context window and returns a single final summary — for a 12-task multi-day workload, Option A is better.

**Option C — Async background agent (Devin etc.):**
Same prompt works. The "verify you're on the branch" first sentence + explicit task order + "read these files in full" instructions are exactly what an async agent needs to self-orient.

## Why it's short

We deliberately did not embed task details, architecture, or success criteria into the prompt itself — every fact lives in one of the planning docs. The prompt's job is to point and constrain, not instruct. If architecture changes mid-stream, you update the planning docs and this prompt stays correct. If we inlined the architecture, every change would mean updating two places.

The prompt also explicitly says "do not re-litigate" and lists what's locked — this prevents the implementing agent from second-guessing decisions you've already made, which is the most common failure mode when handing off a partially-designed project to a fresh agent.
