---
date: 2026-06-03
purpose: ready-to-paste launch prompt for a fresh agent picking up the documentation-consolidation task
audience: the maintainer launching the next agent
status: active / pending — archive with the rest of docs/.research/ when the consolidation task lands
---

# Launch prompt — doc-consolidation rookie agent

Paste the block below to a fresh agent working from a clean clone of `main`. It orients them and then
hands off to the task brief [`NEXT-doc-consolidation.md`](NEXT-doc-consolidation.md), which is the
agent's source of truth.

```text
You are picking up the DgxSparkLabs marketplace project at v1.0.0 (just published). You have a
FRESH CLONE of `main` and no prior context. Your task: the documentation consolidation / cleanup pass.

ORIENT FIRST — read in this order, all already in your clone:
  1. docs/RESUME_HERE.md  — 30-sec status + repo layout; it points you onward.
  2. docs/LESSONS.md       — the traps that cost the last session most. READ THIS BEFORE you touch
                             the generator, CI, or move any file.
  3. docs/.research/NEXT-doc-consolidation.md — YOUR TASK BRIEF: a tiered plan with the exact
                             file-level moves, the `git mv` commands, verification, and three open
                             questions. This is your source of truth — follow it.
  4. Skim HANDOFF.md, STATE.md, PITFALLS.md for state + bug history.

WHAT THE TASK IS (detail in the brief): make the docs tree navigable from a fresh clone — archive
settled/cold material into docs/archive/ (with `git mv`, preserving history), remove two true orphans,
refresh the entry docs (HANDOFF / STATE / RESUME_HERE) for v1.0.0, and fix dangling links. It is DOCS-ONLY.

BEFORE MOVING ANYTHING, resolve the three open questions with me (they decide which files move):
  OQ1 — archive the tracked root research/ market-intel (~80 files) or keep it at root?
  OQ2 — hard-delete vs archive the orphans (docs/archive/pr1-body.md, docs/archive/ONBOARDING.md)?
  OQ3 — trim docs/TEST_YOURSELF.md now (Claude-first) or defer?
They're spelled out in the brief with recommendations.

HARD RULES (full list in CONTRIBUTING.md / AGENTS.md — do not violate):
  - DOCS-ONLY. Do NOT edit src/, _generated/, the platform mirror dirs (.cursor/, .gemini/, .codex/,
    .windsurf/, .devin/, .agents/), or scripts/ — moving generated/source files breaks the generator
    and the drift gate. If you think you must, STOP and ask.
  - NO AI attribution anywhere (no Co-Authored-By, no "Generated with"). Commit as the human git user.
  - `uv` only (never pip). PR-ONLY to `main` — branch, PR, merge; never push to main.
  - Use `git mv` to move (preserves `--follow` history); never delete-and-recreate.
  - The brief lives in docs/.research/, which this task archives — move it LAST, and drop the
    RESUME_HERE "Next task" pointer when done.

VERIFY BEFORE EVERY PUSH:
  - `uv run tasks.py verify`  (drift-check + 4 test suites + `claude plugin validate ./`)
  - One CI job locally:
    `act -j test -W .github/workflows/ci.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest -s GITHUB_TOKEN="$(gh auth token)"`
    (the `-s GITHUB_TOKEN` is REQUIRED, or setup-uv errors with "Parameter token … required")
  - After the moves, sweep for broken links and fix each hit:
    `grep -rn "research/\|pr1-body\|ONBOARDING\|rules/no-ai-credit/" README.md HANDOFF.md STATE.md AGENTS.md CONTRIBUTING.md docs/*.md`

DONE WHEN (the brief's "Definition of Done" is authoritative): docs/ has no active-research folder still
holding settled work; the orphans are gone; no dangling links; entry docs say "v1.0.0 published";
`--check` clean and CI green on your PR; and someone can clone → RESUME_HERE → your work with zero
extra context.

Work autonomously. Only stop to (a) get my answers to OQ1–OQ3, and (b) anything you genuinely can't
decide (a destructive call, a policy choice). Start by reading the four docs above, then come back with
your proposed OQ answers + a short execution order BEFORE you move any files.
```
