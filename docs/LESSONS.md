---
date: 2026-06-03
purpose: hard-won lessons for the next agent — read before touching the generator, CI, or doing any layout/name change
audience: future agents + contributors
status: live
---

# Lessons for the next agent

Distilled from the 2026-06-03 stabilization session (made the marketplace releasable + PR-friendly and got all 14 CI workflows green). These are the things that cost us time so they don't cost you yours. Pair with `PITFALLS.md` (specific bug→fix entries) and `HANDOFF.md` (state).

## 1. Verify by making it FAIL, not just pass

A check that only ever prints green proves nothing. Two real bugs this session were invisible until forced to fail:

- The drift gate (`generate_manifest.py --check`) silently did **not** guard `docs/INVENTORY.md` or `gemini-extension.json` — `snapshot_tree` used `root.rglob("*")`, which yields nothing for a *file* path. Found only by appending junk to the file and confirming `--check` *should* exit 1 (it didn't).
- `validate_source.py` "works" — but the proof is feeding it a malformed source and seeing exit 1, plus a missing `${CLAUDE_PLUGIN_ROOT}` reference and watching it flag that.

Rule: for every guard you add, run the adversarial case once. "Unfalsified" ≠ "proven."

## 2. A layout/name change has a blast radius far beyond the generator

The `src/` reorg + single/multi rename (`cd7a7d8`) was "handled by the generator" — yet it silently broke **four** places nobody tracked: the `agents` CLI handlers (`scripts/agents_cli/constructs/*.py` still pointed at top-level dirs), **9 compat CI workflows** (installed pre-rename plugin names), `compat-headless-claude.yml`, and a pile of docs/counts.

Rule: after any layout or published-name change, grep the **whole repo** — not just `scripts/` — for the old names: `grep -rn "<construct>-example" .github/ scripts/ docs/`. Assume nothing auto-propagated.

## 3. Unit tests ≠ CI ≠ reality

`uv run tasks.py verify` was fully green while 9 GitHub workflows were red. The suites validate the generator and the `agents` CLI against a **local checkout**; they never install the **published** plugin by name and never drive the Codex/Gemini/Devin CLIs. Those are different claims.

Rule: anything touching published plugin names or a platform CLI must be exercised by the real workflow bytes — locally via `act`, then on GitHub. See lesson 4.

## 4. The `act` recipe that works in this repo

```bash
act -j <job> -W .github/workflows/<wf>.yml \
    -P ubuntu-latest=catthehacker/ubuntu:act-latest \
    -s GITHUB_TOKEN="$(gh auth token)"
```

- The `-s GITHUB_TOKEN` is **required** — without it `astral-sh/setup-uv` dies with `Parameter token or opts.auth is required`. That error is an `act`-environment issue, not your code.
- The runner image is already cached locally; first run otherwise pulls ~2 GB.
- Use `-j <job>` to run a single job (e.g. `-j claude`) and skip the Codex/Gemini/Devin jobs that need CLIs `act` can't easily provide. The Claude jobs + the drift/validate jobs DO run under `act`.

## 5. CLI behavior drifts silently — probe, don't trust docs

Real surprises this arc, all version-specific (Claude CLI 2.1.159–2.1.161):

- `claude plugin details <install-name>` stopped resolving the **bare** install name — it needs `<install-name>@dgxsparklabs-marketplace` (or the namespaced `dgxsparklabs-<install-name>`).
- There is no `/output-style` slash command (it's under `/config`).
- Hook payloads come from **stdin**, not `${CLAUDE_TOOL_NAME}` (which is unset).

Rule: probe the live CLI for the exact behavior + version (`claude --version`), and treat old logs/docs as hypotheses. Record the version next to any behavioral claim.

## 6. Don't trust a subagent's diagnosis on the load-bearing claim

Subagents are great for breadth, but verify the one fact the whole plan rests on yourself. This session: a Plan agent asserted the bundle-membership test *gated availability* (it doesn't — Phase 1 emits the marketplace entry unconditionally), and under-diagnosed the `agents-cli` failure as "stale test names" when it was a real shipped bug across every handler. Read the code for the crux.

## 7. Identity is config-driven — rebrand in one file

The `<brand>-` prefix on every slash namespace / `plugin.json` `name` is derived in `scripts/constructs.py` as `brand = marketplace_name.removesuffix("-marketplace")`, where the name comes from `src/MARKETPLACE.toml`. So a fork rebrands by editing `src/MARKETPLACE.toml` (name, owner, repo URL) + regenerating — **don't hardcode brand strings**. (Human-facing literals — README install commands, `install.sh` `REPO_URL` default, a couple of CI greps — still need a find/replace; a `rebrand` helper would be a nice future addition.)

## 8. Project conventions that override defaults

- **No AI attribution, ever** (`rules/no-ai-credit/`): no `Co-Authored-By`, no "Generated with". This **overrides** the harness's default commit footer. Commit as the human git user; the CI regen-bot uses a non-AI identity (`marketplace-generator`).
- **`uv` only** — never `pip`. Scripts use PEP 723 inline metadata + `uv run`.
- **PR-only to `main`**; feature branches are fine to push.
- **Counts live in `docs/INVENTORY.md`** (generated + drift-checked). Never hardcode a plugin/test count in prose — point at the file.

## 9. Generated output is committed AND consumed from a clone

Cursor/Windsurf/Devin read the mirror dirs (`.cursor/`, `.windsurf/`, `.agents/`) directly from a clone, so the mirrors **must** stay committed and the fresh-clone-reproduces gate (FR-3) is real. The session's #1 release-blocker was exactly this class: a committed `lsp-config.json` referencing an **untracked** `example_lsp.py` — works locally, broken on every fresh clone. `validate_source.py` now catches "config references a missing file."

## 10. The contributor happy-path (and the one for you)

```bash
uv run scripts/new_construct.py <type> <name>   # scaffold from the example
# edit the copied files
uv run tasks.py verify                           # --check + 4 suites + claude plugin validate
git add . && git commit && open a PR             # NO catalog.toml edit needed
```

Same-repo PRs get manifests regenerated + committed by `.github/workflows/regen-bot.yml`. Forks run `scripts/regen.{sh,ps1}` and commit the output (the drift gate enforces it). Install pre-commit: `pre-commit install`.

## 11. Ignore the `example-lsp` diagnostics on files you edit

The `⚠ example-lsp marker — file analyzed …` line that fires on every file is the marketplace's **own** bundled LSP plugin reacting (it's installed in this environment) — proof the construct works, not an error. Its `undefined name 'scope'/'exc'` warnings are **false positives** (the toy stdlib server doesn't understand function params or `except … as exc`). Don't chase them.
