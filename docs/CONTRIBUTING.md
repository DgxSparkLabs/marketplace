---
date: 2026-07-25
purpose: the one-folder contribution contract, local gate, conventions
status: live
---

# Contributing

The contract: **you touch `src/skills/` only; CI owns everything generated.** A contribution is a skill folder and nothing else — no manifest edits, no generator runs, no version bumps.

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) if you want to run the local gate (macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh` · Windows: `irm https://astral.sh/uv/install.ps1 | iex`)
- The `claude` CLI if you want the final validate step locally (optional — CI runs it regardless)

## Adding a skill

1. Create the folder — scaffold (`uv run scripts/new_construct.py skill my-skill`) or by hand:
   - **Solo layout**: `src/skills/my-skill/SKILL.md` (frontmatter `name:` + `description:` required)
   - **Multi layout**: `src/skills/my-plugin/skills/<skill-name>/SKILL.md` per skill, plus an operator-authored one-liner in `src/skills/my-plugin/.claude-plugin/plugin.json` (`description` — the ONLY allowed key; anything else fails validation)
2. Follow the naming rules (CI-enforced, full rationale in issue #19): kebab-case everywhere, folder name ≤ 32 chars, multi-layout folder name must equal frontmatter `name:`.
3. Commit and push / open a PR. That's it — same-repo PRs and pushes to main get manifests regenerated and committed by `regen-bot`; fork PRs are checked by the drift gate (run `uv run scripts/generate_manifest.py` and commit the output, or use `scripts/regen.sh`/`.ps1`).

## The local gate (optional but recommended)

```bash
uv run scripts/tasks.py verify
```

Runs, in order: `validate_source.py` (structure + naming standard) → drift check → the test suites (`test_marketplace`, `test_tooling` — with a nonzero-test-count assertion) → `claude plugin validate ./`. All must pass; CI runs the same steps.

## Conventions

- kebab-case names; Python is PEP 723 + `uv run` (never `pip`); shell scripts use `set -euo pipefail`.
- PR-only to `main`; feature branches push freely.
- No AI co-author attribution in commits.
- Never hand-edit `_generated/`, `.claude-plugin/`, or `docs/INVENTORY.md` — regenerated from scratch every run.
- After fixing any bug worth remembering, add a `PITFALLS.md` entry.

## Testing notes

- `tests/test_marketplace.py` — source layout, generated-output invariants, naming composition (issue #19 N3/N5), drift, secrets scan.
- `tests/test_tooling.py` — `validate_source.py` (including adversarial fixtures per rule) and the scaffolder.
- Verify a new guard by making it FAIL once (`docs/LESSONS.md` lesson 1); a guard only ever seen green proves nothing.
