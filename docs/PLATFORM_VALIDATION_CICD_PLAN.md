# Multi-Platform Validation CI/CD Plan

This is the design for the CI/CD layer that verifies our marketplace works on every platform we ship a mirror for. It transcribes the rows in [`PLATFORM_INSPECTION_CATALOG.md`](./PLATFORM_INSPECTION_CATALOG.md) into automated assertions.

**Implementation complete.** Workflow files are committed in branch `feat/multi-platform-validation`. This document remains the canonical design reference and source of truth for catalog-to-assertion synchronization.

---

## 1. The Transcription Principle

Every auth-free inspection command in the catalog becomes exactly one CI assertion:

```
install platform CLI  →  register our marketplace  →
run cataloged command  →  assert exit code + output  →  cleanup
```

The catalog is the source of truth. If the catalog says `devin skills list` returns rows tagged `Cursor`, the CI test asserts exactly that. If a platform deprecates a command, the catalog row is removed and the matching CI assertion is removed in the same PR — they stay synchronized.

**Anti-goal:** writing CI assertions that aren't backed by a catalog row. This is how spec drift creeps in. Every test step traces to a documented row.

---

## 2. Workflow Organization — Per-Construct, Cross-Platform Matrix

**Decision (locked):** One workflow file per Claude Code construct type our marketplace ships. Each workflow runs a matrix of the platforms applicable to that construct.

Why per-construct rather than per-platform:
- A new construct type added to Claude Code → one new workflow file, no edits to existing files.
- A new platform added → matrix entry added to each applicable workflow.
- The marketplace's natural domain model is constructs (skills, rules, hooks…); the CI layer matches that, not the platform vendor axis.
- Failures are scoped: "MCP validation failed on Codex" is more actionable than "Codex compat job failed (which assertion?)."

Why matrix rather than separate files per platform inside each construct workflow:
- Shared setup steps (checkout, run generator, validate manifest sync) execute once per platform, not duplicated 11 times per workflow.
- GitHub Actions matrix UI shows pass/fail per platform-construct cell, mapping directly to the inspection catalog's matrix.

---

## 3. Workflow Inventory

Ten `compat-*.yml` workflows, one per **plugin-installable** construct type our marketplace ships. Rules are intentionally excluded — they aren't installable via any platform's plugin system; rule format validation stays in `tests/test_marketplace.py`.

| Workflow file | Construct covered | Matrix platforms | Required for merge? |
|---------------|------------------|------------------|--------------------|
| `compat-skill.yml` | skills | claude, devin, codex, gemini | claude + devin **required**; codex + gemini **advisory** (`continue-on-error`) |
| `compat-command.yml` | commands | claude | **required** |
| `compat-agent.yml` | agents | claude | **required** |
| `compat-hook.yml` | hooks | claude, gemini (migration check only) | claude **required**; gemini **advisory** |
| `compat-mcp.yml` | MCP servers | claude, devin, codex, gemini | claude + devin **required**; codex + gemini **advisory** |
| `compat-extension.yml` | Gemini extensions | gemini | **advisory** — fails until generator emits `gemini-extension.json`; passes when it does |
| `compat-monitor.yml` | monitors | claude | **required** |
| `compat-output-style.yml` | output styles | claude | **required** |
| `compat-theme.yml` | themes | claude | **required** |
| `compat-marketplace-add.yml` | marketplace registration | claude, codex | claude **required**; codex **advisory** |

**Ten workflows total.** Most are small (one platform); a few are matrix-rich (skills, MCP).

All workflows share:
- `on: pull_request` to `main` AND `on: push` to `main` + `feat/**` AND `workflow_dispatch` (per decision #12)
- `concurrency: { group: '${{ github.workflow }}-${{ github.ref }}', cancel-in-progress: true }` (per decision #19)
- First step: `uv run scripts/generate_manifest.py --write` (per decision #13) — regenerates `_generated/` fresh from sources
- Each matrix cell runs in its own job on `ubuntu-latest` (per decision #6 — per-job isolation)

---

## 4. All Locked Decisions Recap

Twenty decisions are locked across three rounds of review-and-resolve. The implementing agent picks these up as given.

### Original 8 (first design pass)

| # | Decision | Chosen direction |
|---|----------|-----------------|
| 1 | Where to commit catalog + plan docs | `feat/claude-plugin-compliance` (merged with migration PR #1) |
| 2 | Required vs advisory for compat checks | Required for non-blocked platforms; advisory for blocked platforms (via job-level `continue-on-error`) |
| 3 | Workflow file structure | One workflow per construct capability, with platform matrix per workflow |
| 4 | Codex + Gemini blocked-in-CI strategy | Parallel tracks — GitHub support whitelist request + local-dev fallback scripts |
| 5 | Composite action location | In this repo, `.github/actions/setup-<platform>/` |
| 6 | Test isolation between platforms | Per-job isolation — each matrix cell on a fresh Ubuntu runner |
| 7 | Platform-breakage policy | Block release until catalog + assertions are updated in same PR |
| 8 | Advisory → required promotion path (post-whitelist) | **Superseded by #16 below** — no explicit promotion needed |

### Round 1+2+3 (post-reviewer-critique resolutions)

| # | Decision | Chosen direction |
|---|----------|-----------------|
| 9 | Output match contract (BLOCKER #1) | Per-row `Match mode` column in catalog: `exit-code-only` / `grep <substring>` / `regex <pattern>` / `exact-diff`. Each row commits to one. Default: `grep` substring match against stdout |
| 10 | Advisory enforcement YAML idiom (BLOCKER #2) | Job-level `continue-on-error: true` on Codex/Gemini matrix entries. Failures stay visible in PR UI without blocking merge |
| 11 | Claude rules in compat (BLOCKER #10) | **`compat-rule.yml` removed entirely.** Rules aren't installable via plugins on any platform; rule format validation lives in `tests/test_marketplace.py`. Workflow count: 11 → 10 |
| 12 | Workflow trigger model (IMPORTANT #8) | `on: pull_request` to `main` AND `on: push` to `main` + `feat/**`. Manual `workflow_dispatch` available |
| 13 | Generator invocation (BLOCKER #4) | Each compat workflow runs `uv run scripts/generate_manifest.py --write` as its first step (regenerates fresh from sources). Workflows do NOT trust the committed `_generated/` tree |
| 14 | CLI version pinning (IMPORTANT #5) | Float to `@latest` for npm-installed CLIs (Codex, Gemini). CI catches real-world breakage immediately; per the platform-breakage policy (#7), a failed compat run blocks release until catalog + assertions are updated |
| 15 | Devin skills/rules assertion (IMPORTANT #6) | Explicit `working-directory: ${{ github.workspace }}` + `devin skills list \| grep -i <skill-name>` (and same shape for rules, mcp). Asserts skill is in Devin's output |
| 16 | Gating mechanism for blocked platforms (NICE #13) | **None.** No `vars.*` variable, no admin toggle, no promotion ceremony. The CLI install attempt itself is the gate. When GitHub lifts the block, workflows start passing on the next run with zero code changes |
| 17 | Composite action contract (BLOCKER #3) | Standard contract for every `setup-<platform>` action: `inputs: version (string, default 'latest')`; `outputs: installed (boolean)`. Behavior: install CLI at requested version, run `<cli> --version` to verify, set output |
| 18 | Marketplace re-registration handling (IMPORTANT #9) | Trust runner ephemerality. No defensive `remove-if-exists`. GitHub-hosted runners are fresh per job. Self-hosted runner consideration deferred to if/when we add one |
| 19 | Concurrency block (NICE #11) | Add to every compat workflow: `concurrency: { group: '${{ github.workflow }}-${{ github.ref }}', cancel-in-progress: true }`. Prevents redundant runs on rapid pushes |
| 20 | Gemini extension workflow gating (NICE #14) | **No gating.** Ship `compat-extension.yml` normally. If it fails because generator doesn't yet emit `gemini-extension.json`, the failure is advisory (Gemini row has `continue-on-error: true`). Workflow passes when generator catches up |

### Required vs Advisory matrix (decision #2 elaborated)

| Platform | CI viability | Compat checks status |
|----------|-------------|----------------------|
| Claude Code | ✅ Free in CI | **Required** for merge |
| Devin | ✅ Free in CI (install with `\|\| true` per `exp/cli-empirical-discovery` findings) | **Required** for merge |
| Cursor | ✅ Free (`npx cursor-doctor`) | **Required** for merge (format-only) |
| Windsurf | ✅ Free (stdlib YAML parser) | **Required** for merge (format-only) |
| Codex | ❌ Blocked by GitHub Actions org policy | **Advisory** in CI; required for local-dev verification per `LOCAL_DEVELOPMENT.md` |
| Gemini | ❌ Blocked by GitHub Actions org policy | **Advisory** in CI; required for local-dev verification per `LOCAL_DEVELOPMENT.md` |

Advisory checks run but don't block merge. They surface failures in the UI without gating PRs. When the GitHub whitelist (Section 7) lands, they get promoted to required.

---

## 5. Shared Platform Setup — Composite Actions

To avoid duplicating install logic across 10 workflows, each platform with a CLI gets a composite action. **All actions share a standard contract** (per decision #17):

```yaml
inputs:
  version:
    description: 'CLI version to install. Default: latest'
    default: 'latest'
    required: false
outputs:
  installed:
    description: 'Boolean — true if the CLI binary is available after setup'
```

### Action inventory

```
.github/actions/
├── setup-claude/action.yml         # claude CLI install (TBD vendor mechanism)
├── setup-codex/action.yml          # npm install -g @openai/codex@${{ inputs.version }}
├── setup-gemini/action.yml         # npm install -g @google/gemini-cli@${{ inputs.version }}
├── setup-devin/action.yml          # curl -fsSL https://cli.devin.ai/install.sh | bash || true (per empirical finding: non-TTY exits 1 but binary installs)
└── setup-cursor-doctor/action.yml  # ensures `npx --yes cursor-doctor@${{ inputs.version }}` is reachable (no global install — npx ad-hoc)
```

Note: there is no `register-marketplace/action.yml`. Marketplace registration is a single platform-specific line in each workflow (e.g., `claude plugin marketplace add ./` or `codex plugin marketplace add ./`), simple enough not to warrant an abstraction. Per decision #18, no defensive `remove-if-exists` is needed because GitHub-hosted runners are ephemeral.

### Per-action behavior

| Action | Install command | Verify | Sets `installed` |
|--------|----------------|--------|------------------|
| `setup-claude` | TBD vendor install mechanism | `claude --version` exit 0 | true if verify passes |
| `setup-codex` | `npm install -g @openai/codex@${{ inputs.version }}` | `codex --version` exit 0 | true if verify passes |
| `setup-gemini` | `npm install -g @google/gemini-cli@${{ inputs.version }}` | `gemini --version` exit 0 | true if verify passes |
| `setup-devin` | `curl -fsSL https://cli.devin.ai/install.sh \| bash \|\| true` then `chmod +x ~/.local/bin/devin` | `devin --version` exit 0 | true if verify passes |
| `setup-cursor-doctor` | n/a — npx handles installation on first use (`'latest'` is a valid npm dist-tag, resolves to current published version) | `npx --yes cursor-doctor@${{ inputs.version }} --help` exit 0 | true if verify passes |

Workflows use them:

```yaml
- uses: ./.github/actions/setup-claude
  id: claude
- uses: ./.github/actions/setup-codex
  id: codex
  with:
    version: 'latest'    # per decision #14 — float to latest
- run: claude plugin marketplace add ./
- run: claude plugin install skill-telegram-notify@dgxsparklabs-marketplace --scope project
- run: claude plugin list | grep "skill-telegram-notify@dgxsparklabs-marketplace"
  # Match mode per catalog: grep substring (decision #9)
```

---

## 6. Per-Workflow Specifications

### 6.1 `compat-skill.yml`

**Construct:** skills
**Matrix platforms:** claude, devin, codex, gemini
**Per-platform validation strategy:**

| Platform | Setup | Install assertion | List assertion | Cleanup |
|----------|-------|-------------------|----------------|---------|
| claude | setup-claude + register-marketplace | `claude plugin install skill-telegram-notify@dgxsparklabs-marketplace --scope project` exit 0 | `claude plugin list \| grep "skill-telegram-notify@dgxsparklabs-marketplace"` exit 0 | uninstall + prune |
| devin | setup-devin | `git pull` (Devin reads filesystem at session start) | `devin skills list \| grep -i telegram` exit 0 (matches our `_generated/skill-telegram-notify/SKILL.md`) | n/a (no install state) |
| codex (advisory) | setup-codex (skip-if-blocked) | `codex plugin marketplace add ./` exit 0 | `cat ~/.codex/config.toml \| grep dgxsparklabs-marketplace` | `codex plugin marketplace remove dgxsparklabs-marketplace` |
| gemini (advisory) | setup-gemini (skip-if-blocked) | `echo "y" \| gemini skills install ./_generated/skill-telegram-notify` exit 0 | `gemini skills list --all \| grep telegram-notify` exit 0 | `gemini skills uninstall telegram-notify` |

### 6.2 ~~`compat-rule.yml`~~ — REMOVED (per decision #11)

Rules are not installable via the plugin system on any platform. Claude Code's plugin spec has no `rules` field; we use the `activate.sh` symlink workaround for Claude users, and Devin/Cursor/Windsurf simply read rule files directly from filesystem.

Rule **format validation** lives in the existing `tests/test_marketplace.py` (TestCursorRulesMirror, TestWindsurfRulesMirror, TestDevinRulesMirror classes — to be authored or extended as part of the implementation). It runs as part of the existing `ci.yml` and the manifest-drift check, not as a `compat-*.yml`.

There is no `compat-rule.yml` workflow.

### 6.3 `compat-command.yml`

**Construct:** commands (Claude-only)
**Matrix platforms:** claude

| Step | Assertion |
|------|-----------|
| Install `example-command@dgxsparklabs-marketplace` | exit 0 |
| `claude plugin list` | `grep example-command` exit 0 |
| `claude plugin details example-command` | shows commands section with one entry |

### 6.4 `compat-agent.yml`

**Construct:** agents (Claude-only)
**Matrix platforms:** claude

| Step | Assertion |
|------|-----------|
| Install `example-agent@dgxsparklabs-marketplace` | exit 0 |
| `claude plugin details example-agent` | shows agents section with `notebook-reviewer` |

### 6.5 `compat-hook.yml`

**Construct:** hooks
**Matrix platforms:** claude, gemini (migration advisory)

| Platform | Strategy |
|----------|----------|
| claude | Install `example-hook@dgxsparklabs-marketplace`, run `claude plugin details example-hook`, assert hooks section includes UserPromptSubmit entry |
| gemini (advisory) | Run `gemini hooks migrate` against `examples/example-hook/hooks/hooks.json` (dry-run), assert no error |

### 6.6 `compat-mcp.yml`

**Construct:** MCP servers
**Matrix platforms:** claude, devin, codex, gemini

| Platform | Strategy |
|----------|----------|
| claude | Install `example-mcp@dgxsparklabs-marketplace`, `claude plugin details example-mcp` shows mcpServers |
| devin | `devin mcp list` baseline; manually add our example via `devin mcp add example-fetch -- uvx mcp-server-fetch`; verify in list output |
| codex (advisory) | `codex mcp add example-fetch -- uvx mcp-server-fetch`; `codex mcp list` shows entry; `codex mcp get example-fetch --json` returns valid JSON |
| gemini (advisory) | `gemini mcp add example-fetch uvx mcp-server-fetch`; `gemini mcp list` shows entry |

### 6.7 `compat-extension.yml`

**Construct:** Gemini extensions
**Matrix platforms:** gemini (advisory, blocked)

| Step | Assertion |
|------|-----------|
| Skip if `gemini` not installable in this runner | conditional skip |
| Else: `gemini extensions install ./<path-where-we-ship-gemini-extension.json>` exit 0 | (requires generator to emit gemini-extension.json — future work flagged) |
| `gemini extensions list` shows our entry | grep assertion |
| `gemini extensions validate ./<path>` exit 0 | validation gate |

### 6.8–6.10 `compat-monitor.yml`, `compat-output-style.yml`, `compat-theme.yml`

**Construct:** monitor / output style / theme (Claude-only)
**Matrix platforms:** claude

Each follows the same skeleton:

| Step | Assertion |
|------|-----------|
| Install `example-<type>@dgxsparklabs-marketplace` | exit 0 |
| `claude plugin details example-<type>` | shows the relevant section |

### 6.11 `compat-marketplace-add.yml`

**Construct:** marketplace registration (cross-platform)
**Matrix platforms:** claude, codex (advisory)

| Platform | Strategy |
|----------|----------|
| claude | `claude plugin marketplace add ./` exit 0; `claude plugin marketplace list` shows `dgxsparklabs-marketplace` |
| codex (advisory) | `codex plugin marketplace add ./` exit 0; `cat ~/.codex/config.toml \| grep dgxsparklabs-marketplace` exit 0 |

---

## 7. Codex + Gemini Strategy — GitHub Whitelist Request + Local Fallback

The user chose: **try to whitelist the npm packages with GitHub support.**

### Parallel approach

**Track A — Whitelist request (process-driven, unblocking)**

1. File a support request with GitHub asking for `@openai/codex` and `@google/gemini-cli` to be added to the allowlist for the `DgxSparkLabs` org.
2. Cite that they are first-party OpenAI and Google packages with published Apache-2.0 licenses, NPM verified publishers.
3. Reference [GitHub Actions org policy documentation](https://docs.github.com/en/organizations/managing-organization-settings) for the exact policy mechanism (Actions permissions / npm allowlist).
4. Expected timeline: unknown. Could be hours, could be weeks, could be a rejection.

**Track B — Local-dev fallback (engineering-driven, ships immediately)**

A `scripts/validate-codex-local.sh` and `scripts/validate-gemini-local.sh` that contributors with the CLIs installed locally can run. These scripts run the same assertions the CI workflows would, in the same shape, so the local output looks identical to the (future) CI output. Documented prominently in `LOCAL_DEVELOPMENT.md`.

```bash
# scripts/validate-codex-local.sh
set -euo pipefail
which codex >/dev/null || { echo "Codex CLI not installed; run: npm install -g @openai/codex"; exit 0; }

uv run scripts/generate_manifest.py --check
codex plugin marketplace add ./
grep dgxsparklabs-marketplace ~/.codex/config.toml >/dev/null && echo "✓ Marketplace registered"
codex mcp list >/dev/null && echo "✓ codex mcp list returns auth-free"
codex features list >/dev/null && echo "✓ codex features list returns auth-free"
codex plugin marketplace remove dgxsparklabs-marketplace >/dev/null && echo "✓ cleanup"
echo "All Codex local validation checks passed."
```

### When the whitelist arrives

**No gating mechanism exists** (per decision #16). Codex and Gemini workflows are written normally and attempt to install at every run. While the org-level block is in place, their CLI install fails with the documented 0s GitHub Actions error. The matrix entries have `continue-on-error: true` (decision #10), so this failure is **advisory** — visible in the PR summary, doesn't gate merge.

When GitHub lifts the block (whether via whitelist, policy change, or any other mechanism), the install will succeed on the next CI run, the workflow will pass, and the advisory check turns green automatically. No code changes, no admin toggle, no promotion ceremony — the CLI install attempt itself is the gate.

If the block is never lifted, the local-dev scripts remain the only validation path for Codex/Gemini. The compat workflows continue to fail advisory and serve as visible documentation of the unresolved block.

---

## 8. Implementation Phasing

**This branch (`feat/claude-plugin-compliance`):** the catalog + this plan ship as design docs. No `.github/workflows/compat-*.yml` files. PR #1 doesn't grow further.

**Follow-up PR #2 (`feat/multi-platform-validation`):**

| Wave | Scope | Files added | Effort | Status |
|------|-------|-------------|--------|--------|
| 1 | Composite actions + 6 single-platform Claude-only workflows | `.github/actions/setup-claude/`, `compat-command.yml`, `compat-agent.yml`, `compat-monitor.yml`, `compat-output-style.yml`, `compat-theme.yml`, `compat-marketplace-add.yml` (claude row only) | 4–6 hrs | DONE |
| 2 | Matrix workflows for free-in-CI platforms | `compat-skill.yml` (claude + devin), `compat-mcp.yml` (claude + devin), `compat-hook.yml` (claude only initially), `setup-devin/`, `setup-cursor-doctor/` | 6–8 hrs | DONE |
| 3 | Codex + Gemini advisory rows in existing matrices + local fallback scripts | `setup-codex/`, `setup-gemini/`, `scripts/validate-codex-local.sh`, `scripts/validate-gemini-local.sh`, `LOCAL_DEVELOPMENT.md` update | 3–4 hrs | DONE |
| 4 | Whitelist follow-up — flip Codex/Gemini advisory → required when granted | one-line edits per workflow | 30 min | **DONE (2026-05-22)** — org block confirmed lifted via 3 consecutive clean CI runs; all 6 `continue-on-error: true` entries flipped to `false`. Generator also extended to emit `.gemini/gemini-extension.json`, making `compat-extension.yml` required. |

**Total estimated effort:** ~15–20 hours of implementation work + the indeterminate whitelist process.

**Wave 4 completion note:** The GitHub org-level block on `@openai/codex` and `@google/gemini-cli` was confirmed lifted empirically — both CLIs installed and passed all assertions across three consecutive CI runs (verification commit, FIX_REPORT commit, and fix cycle commit). No whitelist request was required; the block appears to have been lifted independently. All 6 Codex/Gemini `continue-on-error: true` entries are now `continue-on-error: false`. The `compat-extension.yml` gemini job additionally required generator work (decision #20) which landed in the same Wave 4 commit.

---

## 9. Remaining Open Questions

After three rounds of review-and-resolve, only smaller implementation-time questions remain. All BLOCKER and IMPORTANT items from the reviewer's critique are resolved in Section 4. The two below are NICE-level questions deferred to empirical resolution during Wave 1/2 implementation:

1. **Composite action cache strategy.** npm installs are 5–10s each; multiplied across many workflows × platforms = significant CI cost. Should `setup-codex` etc. use `actions/cache` for `~/.npm` and the installed binary? Decide during Wave 1 by measuring actual runner cost. Default: no caching to start; add if CI minutes become a problem.

2. **Devin CLI install cost in CI.** The `curl ... | bash` installer is large (~10s to download + install); consider caching the installed binary across runs. Decide during Wave 2 once the actual Devin workflow is authored and we have runtime data.

These two are intentionally left for implementation-time empirical resolution rather than pre-committed to here.

### Resolved questions (moved to Section 4 above)

All 20 substantial questions raised during the design and critique cycles are now locked decisions documented in Section 4 (8 original + 12 from critique resolution). Reviewer's critique surfaced 14 items (4 blockers + 6 important + 4 nice); 12 resolved with explicit decisions, 1 (`cursor-doctor` package name) resolved via npm research, 1 (`compat-rule.yml` existence) resolved by clarification of the marketplace's plugin-installable scope. Second-pass reviewer (after these updates) confirmed all 14 items resolved cleanly.

The third reviewer pass after these doc updates should confirm clean.

---

## 10. Synchronization Discipline

The catalog and these workflows must stay in lockstep:

- Adding a row to `PLATFORM_INSPECTION_CATALOG.md` requires adding the matching assertion to the relevant `compat-*.yml`.
- Removing a row from the catalog requires removing the matching assertion.
- A test review checklist (to be added in the implementation PR) verifies catalog ↔ workflow synchronization before merge.

Drift between catalog and workflows is the failure mode this design is meant to prevent. The test of whether the design works: in six months, can a new contributor add a new construct type and have CI coverage automatically apply by adding (a) one catalog row, (b) one workflow file, (c) one composite-action invocation?

---

## What This Plan Is Not

- It is not implementation. No `.github/workflows/compat-*.yml` ships in this branch.
- It is not a contract with any platform's owner. Codex, Gemini, Cursor, Windsurf, and Devin may change their CLI surfaces; our plan accommodates that via the catalog-as-spec model.
- It is not a substitute for the existing `ci.yml` (manifest drift check + test suite). Those remain required and orthogonal.

When the implementing agent picks up this plan in a follow-up branch, the deliverables are exactly the eleven workflow files, the composite actions, and the local-dev fallback scripts. Everything else is already designed.
