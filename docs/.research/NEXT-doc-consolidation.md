---
date: 2026-06-03
purpose: jump-start brief + tiered plan for the post-v1.0.0 documentation consolidation
audience: a fresh agent picking this up from a clean clone of `main` (no prior session context)
status: active / pending — archive this file (with the rest of docs/.research/) when the task is done
---

# Plan: Consolidate & tidy the docs for a clean v1.0.0 repo

## Read this first (you are a fresh agent on a fresh clone)

- **Where the project is:** `v1.0.0` is published. `main` is the release; CI is green (14 workflows on the branch, 15 on the main push). The marketplace installs via `claude plugin marketplace add DgxSparkLabs/marketplace`. Ships **reference/example** plugins only — production skills/rules are archived (re-add is ROADMAP #16–#18, out of scope here).
- **Read order to orient (all in this clone):** `docs/RESUME_HERE.md` → `docs/LESSONS.md` (hard-won working rules — read before any generator/CI/move) → `HANDOFF.md` + `STATE.md` (state) → `PITFALLS.md` (bug→fix log) → this file.
- **Non-negotiable conventions** (full list in `CONTRIBUTING.md` / `AGENTS.md`): no AI attribution in commits/PRs/files (overrides any default footer); `uv` only (never pip); **PR-only to `main`** (branch, PR, merge); preserve history with `git mv`, don't delete-and-recreate.
- **Verify before you push:** `uv run tasks.py verify` (drift-check + 4 suites + `claude plugin validate`). For CI, run a job locally first: `act -j <job> -W .github/workflows/<wf>.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest -s GITHUB_TOKEN="$(gh auth token)"` (the `-s GITHUB_TOKEN` is required).

## 1. Objective

- Make the documentation tree navigable from a fresh clone: one obvious entry point, a canonical reference set, and **no "active research" folders still holding settled work**.
- Archive (don't delete) cold/settled material with `git mv`; hard-delete only true orphans.
- Refresh the entry docs so a newcomer isn't misled by pre-`v1.0.0` state.

**Definition of Done** (observable):
- `docs/.research/` and `docs/research/` no longer hold settled work — settled arcs moved under `docs/archive/` (history preserved; `git log --follow` traces a moved file).
- The two orphans (`docs/archive/pr1-body.md`, `docs/archive/ONBOARDING.md`) are gone (ONBOARDING only after confirming it duplicates `RESUME_HERE.md`).
- No dangling doc links: `grep -rn "](.*/research/" docs/ *.md` and a link check find nothing pointing at moved/removed files; the stale `rules/no-ai-credit/` path references are fixed.
- `HANDOFF.md`, `STATE.md`, `RESUME_HERE.md` state "v1.0.0 published" and point at the current canonical docs.
- `uv run scripts/generate_manifest.py --check` is still clean (no `src/`, `_generated/`, or mirror files moved) and CI is green.
- A reviewer reading only `RESUME_HERE.md` can find every canonical doc and this plan.

**Open questions** (decide before executing — they change the file moves):
- **OQ1 — root `research/` (tracked market-intelligence, ~80 files / ~30k lines):** archive it to `docs/archive/research-market-intel-2026-05/`, or keep it at repo root? It is cold and not load-bearing for the marketplace; recommend archiving. *(Note the separate gitignored `docs/research/research/` stash — leave it; a fresh clone never sees it.)*
- **OQ2 — delete vs archive the orphans:** convention is archive-not-delete, but `pr1-body.md` (a merged PR's body) and `ONBOARDING.md` (apparent `RESUME_HERE` dup) are genuine garbage. Hard-delete, or sink deeper into `docs/archive/`? Recommend delete.
- **OQ3 — `docs/TEST_YOURSELF.md` (2751 lines):** it is multi-platform and its non-Claude sections are stale post-Claude-first. Trim/split now (keeping `docs/CLAUDE_QA_RUNBOOK.md` as the Claude path), or defer and just mark the stale sections? Recommend defer → ROADMAP.

## 2. Approach

**Strategy: a docs-only `git mv` + de-drift pass — content moves to `docs/archive/`, the entry docs get refreshed, and zero `src/`/`_generated/`/mirror bytes are touched (so the generator and drift gate are untouched).**

Why this shape:
- The repo's own lifecycle rule is *cold→hot→cold*: settled work belongs in `docs/archive/`, not `docs/.research/` (pending) — the task is just enforcing that after the release.
- `git mv` keeps `--follow` history, which is the whole reason to move-not-recreate.
- Keeping it strictly docs-only means `--check` stays green by construction; the risk is only broken **links**, which a grep sweep catches.

Mechanics that matter:
- **Two confusingly-named dirs** collapse: `docs/.research/` (dot, 2 settled QA notes) and `docs/research/` (no dot, 4 settled arcs + the gitignored stash). Move both settled sets into `docs/archive/<arc>/`; the distinction goes away.
- **Link integrity:** after each move, `grep -rn "<old-path>" docs/ *.md README.md` and fix references. The biggest link sources are `README.md` ("Deep Dives"), `RESUME_HERE.md`, `HANDOFF.md`.
- **Dangling rule refs:** `CONTRIBUTING.md`/`AGENTS.md` reference `rules/no-ai-credit/`, which lives only in `docs/archive/rules-pre-stable-2026-05-26/`. Point the references at the archived path or restate the rule inline.
- **Entry-doc trim:** `HANDOFF.md` stacks dated session banners; move the historical ones into `CHANGELOG.md` (append-only) and keep `HANDOFF.md` to current state.

**Scope IN:**
- `docs/.research/`, `docs/research/` (non-stash), root `research/` (per OQ1), the two archive orphans.
- Refresh `HANDOFF.md`, `STATE.md`, `RESUME_HERE.md`; fix dangling links/refs; update `README.md` Deep-Dives index.

**Scope OUT:**
- `src/`, `_generated/`, `.claude-plugin/`, `.cursor/`, `.gemini/`, `.codex/`, `.windsurf/`, `.devin/`, `.agents/`, `scripts/`, `tests/` — out because moving generated/source/mirror files breaks the generator + drift gate; this is docs-only.
- Re-adding the archived production skills/rules — out → ROADMAP #16–#18.
- Deep rewrite of `TEST_YOURSELF.md` — out (OQ3) → ROADMAP / follow-up.
- Per-platform QA cycles — out → ROADMAP #9–#14.

**Delivery:** one branch off `main` (`docs/consolidation`), one PR, merge after CI green. Solo. Run `act` on `ci.yml` + `compat-validate.yml` locally first (doc-only ⇒ trivially green, but proves no link/test broke).

## 3. Per-change overview (file-level)

### 3.1 Archive settled research (`git mv` → `docs/archive/`)
- `docs/.research/CONTINUATION-construct-tmux-verification.md` and `docs/.research/driving-claude-code-tui-controller-2026-06-01.md` → `docs/archive/claude-tmux-qa-2026-06/`.
- `docs/research/multi-instance-claude-only-2026-05-27/` → `docs/archive/` (the refactor it planned landed: Path A reverted, single/multi shipped).
- `docs/research/naming-conventions-2026-05-26/`, `docs/research/shared-namespace-2026-05-27/`, `docs/research/qa-bug-fixes-2026-05/` → `docs/archive/` (decisions all landed).
- Leave the gitignored `docs/research/research/` stash alone.

### 3.2 Root `research/` (OQ1)
- If archiving: `git mv research docs/archive/research-market-intel-2026-05` (one move of the whole tree). Verify the `.gitignore` `research/raw_*`/`research/nb*` patterns are re-pointed or dropped if the dir no longer exists at root.

### 3.3 Remove orphans
- `git rm docs/archive/pr1-body.md`.
- Confirm `docs/archive/ONBOARDING.md` ⊆ `docs/RESUME_HERE.md`, then `git rm` it (else fold any unique content into RESUME_HERE first).

### 3.4 Refresh entry docs
- `HANDOFF.md`: status → "v1.0.0 published (main @ <sha>), CI green"; move stale dated banners to `CHANGELOG.md`; fix `rules/no-ai-credit/` ref.
- `STATE.md`: add a short "v1.0.0 published" entry; it currently ends mid-publish.
- `docs/RESUME_HERE.md`: 30-second status → v1.0.0; ensure links resolve post-move; keep the "Next task" pointer to this plan until the task starts.
- `README.md`: Deep-Dives index → repoint any links into moved dirs; add `docs/LESSONS.md` + `docs/INVENTORY.md`.

### 3.5 This plan
- When the task is complete, `git mv docs/.research/NEXT-doc-consolidation.md docs/archive/<arc>/` (it is itself "settled" once executed) and drop the RESUME_HERE pointer.

## 4. Implementer guide

### Step 1 — branch + baseline
```bash
git checkout main && git pull
git checkout -b docs/consolidation
uv run scripts/generate_manifest.py --check   # baseline: clean
```
Checkpoint: `--check` prints "OK: generated content matches committed content."

### Step 2 — the moves (decide OQ1/OQ2 first)
```bash
mkdir -p docs/archive/claude-tmux-qa-2026-06
git mv docs/.research/*.md docs/archive/claude-tmux-qa-2026-06/
git mv docs/research/multi-instance-claude-only-2026-05-27 docs/archive/
git mv docs/research/naming-conventions-2026-05-26 docs/archive/
git mv docs/research/shared-namespace-2026-05-27   docs/archive/
git mv docs/research/qa-bug-fixes-2026-05           docs/archive/
# OQ1 = archive root research/:
git mv research docs/archive/research-market-intel-2026-05
# OQ2 = delete orphans:
git rm docs/archive/pr1-body.md docs/archive/ONBOARDING.md
```
Checkpoint: `git status` shows only renames/deletions under `docs/` (+ root `research/`); nothing under `src/`/`_generated/`/mirrors.

### Step 3 — fix links & refs (the only real risk)
```bash
# Find references to moved/removed paths and fix each:
grep -rn "\.research/\|docs/research/\|](.*research/\|rules/no-ai-credit/\|pr1-body\|ONBOARDING" \
  README.md HANDOFF.md STATE.md AGENTS.md CONTRIBUTING.md docs/*.md
```
Edit each hit to the new `docs/archive/...` location (or remove). `rules/no-ai-credit/` → `docs/archive/rules-pre-stable-2026-05-26/no-ai-credit/` (or restate inline).
Checkpoint: the grep returns no live (non-archive) references to moved files.

### Step 4 — refresh entry docs (§3.4)
Edit `HANDOFF.md` / `STATE.md` / `RESUME_HERE.md` / `README.md` per §3.4. No AI attribution.
Checkpoint: `RESUME_HERE.md` names every canonical doc and resolves; opening it cold tells you the project is at v1.0.0.

### Step 5 — verify & ship
```bash
uv run tasks.py verify        # --check clean + 4 suites + validate
act -j test -W .github/workflows/ci.yml -P ubuntu-latest=catthehacker/ubuntu:act-latest -s GITHUB_TOKEN="$(gh auth token)"
git add -A && git commit -m "docs: consolidate + archive settled material for a clean v1.0.0 tree"
git push -u origin docs/consolidation
gh pr create --base main --fill
# after CI green:
gh pr merge --merge
```
Checkpoint: PR CI all green; `main` clone shows a tidy `docs/` with no live `.research`/`research` work-in-progress dirs.

### Canonical docs to KEEP (do not move)
Root: `README`, `HANDOFF`, `PITFALLS`, `STATE`, `CHANGELOG`, `AGENTS`, `CONTRIBUTING`, `VAULT-RULES`, `LICENSE`, `CODE_OF_CONDUCT`, `SECURITY`, `RELEASING`.
`docs/`: `RESUME_HERE`, `LESSONS`, `INVENTORY`, `ARCHITECTURE`, `PLATFORMS`, `ADDING_A_CONSTRUCT`, `CONSTRUCT_TYPES`, `USER_GUIDE`, `SKILL_FORMAT`, `RULE_FORMAT`, `ROADMAP`, `TEST_YOURSELF`, `CLAUDE_QA_RUNBOOK`.
`docs/archive/*` (incl. `skills-pre-stable-*` / `rules-pre-stable-*` — those are the production content to RE-ADD per ROADMAP, not deletable history).
