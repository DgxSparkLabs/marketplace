# Multi-Platform Validation CI/CD Plan

This is the design for the CI/CD layer that verifies our marketplace works on every platform we ship a mirror for. It transcribes the rows in [`PLATFORM_INSPECTION_CATALOG.md`](./PLATFORM_INSPECTION_CATALOG.md) into automated assertions.

**Still planning.** No workflow files are committed yet. This document is the design that contributors will implement, review, and adjust before any `.github/workflows/compat-*.yml` ships.

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

Eleven `compat-*.yml` workflows, one per construct type. Some are single-platform (Claude-only constructs); some span 2–4 platforms.

| Workflow file | Construct covered | Matrix platforms | Required for merge? |
|---------------|------------------|------------------|--------------------|
| `compat-skill.yml` | skills | claude, devin, codex, gemini | claude + devin **required**; codex + gemini **advisory** |
| `compat-rule.yml` | rules | claude, cursor, windsurf, devin | claude + cursor + windsurf + devin **required** (all viable in CI) |
| `compat-command.yml` | commands | claude | **required** |
| `compat-agent.yml` | agents | claude | **required** |
| `compat-hook.yml` | hooks | claude, gemini (migration check only) | claude **required**; gemini **advisory** |
| `compat-mcp.yml` | MCP servers | claude, devin, codex, gemini | claude + devin **required**; codex + gemini **advisory** |
| `compat-extension.yml` | Gemini extensions | gemini | **advisory** (Gemini-only construct; blocked from GitHub Actions) |
| `compat-monitor.yml` | monitors | claude | **required** |
| `compat-output-style.yml` | output styles | claude | **required** |
| `compat-theme.yml` | themes | claude | **required** |
| `compat-marketplace-add.yml` | marketplace registration | claude, codex | claude **required**; codex **advisory** |

**Eleven workflows total.** Most are small (one platform); a few are matrix-rich (skills, rules, MCP).

---

## 4. All Locked Decisions Recap

Eight decisions are locked. The implementing agent picks these up as given.

| # | Decision | Chosen direction |
|---|----------|-----------------|
| 1 | Where to commit catalog + plan docs | `feat/claude-plugin-compliance` (merged with migration PR #1) |
| 2 | Required vs advisory for compat checks | Required for non-blocked platforms; advisory for blocked platforms |
| 3 | Workflow file structure | One workflow per construct capability, with platform matrix per workflow |
| 4 | Codex + Gemini blocked-in-CI strategy | Parallel tracks — GitHub support whitelist request + local-dev fallback scripts |
| 5 | Composite action location | In this repo, `.github/actions/setup-<platform>/` |
| 6 | Test isolation between platforms | Per-job isolation — each matrix cell on a fresh Ubuntu runner |
| 7 | Platform-breakage policy | Block release until catalog + assertions are updated in same PR |
| 8 | Advisory → required promotion path (post-whitelist) | Immediate promotion after one green CI run on `main` + branch protection update |

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

To avoid duplicating install logic across 11 workflows, each platform with a CLI gets a composite action:

```
.github/actions/
├── setup-claude/action.yml         # claude CLI (likely pre-installed in some runners)
├── setup-codex/action.yml          # npm install -g @openai/codex (skip-if-blocked logic)
├── setup-gemini/action.yml         # npm install -g @google/gemini-cli (skip-if-blocked logic)
├── setup-devin/action.yml          # curl install script with || true wrap
├── setup-cursor-doctor/action.yml  # npx cursor-doctor (no auth, no install global)
└── register-marketplace/action.yml # registers ./_generated as the local marketplace for whichever platform was set up
```

Workflows then:

```yaml
- uses: ./.github/actions/setup-claude
- uses: ./.github/actions/register-marketplace
  with:
    platform: claude
- run: claude plugin install skill-telegram-notify@dgxsparklabs-marketplace --scope project
- run: claude plugin list | grep skill-telegram-notify || exit 1
```

Composite actions encapsulate the platform-specific quirks (Devin's interactive installer needing `|| true`, Gemini's `--scope project` flag, Codex's `plugin marketplace add` syntax). The workflows themselves stay readable.

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

### 6.2 `compat-rule.yml`

**Construct:** rules
**Matrix platforms:** claude (advisory — rules use activate.sh, not pure plugin install), cursor, windsurf, devin

| Platform | Strategy |
|----------|----------|
| claude (advisory) | Install `rule-blast-radius@dgxsparklabs-marketplace`, then run cached `activate.sh`, verify symlink/copy in `.claude/rules/blast-radius.md` |
| cursor | `npx cursor-doctor scan .cursor/rules/` exit 0 + custom YAML parser asserting frontmatter has `description \| globs \| alwaysApply` |
| windsurf | Custom YAML parser asserting `trigger:` in `{always_on, model_decision, glob, manual}`, body ≤ 12,000 chars |
| devin | `devin rules list` output includes rules tagged `Cursor` and `Windsurf` (matching our generator-produced mirror files) |

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

The Codex and Gemini compat workflows (already drafted with the assertions, just gated on `if: ${{ vars.CODEX_WHITELIST_GRANTED == 'true' }}` or similar) flip from skipped to running. Their advisory status is promoted to required. No code changes to the workflows themselves — just toggling the gate.

If the whitelist is denied or doesn't arrive, the local-dev scripts remain the validation path indefinitely. The compat workflows stay as documented intent.

---

## 8. Implementation Phasing

**This branch (`feat/claude-plugin-compliance`):** the catalog + this plan ship as design docs. No `.github/workflows/compat-*.yml` files. PR #1 doesn't grow further.

**Follow-up PR #2 (`feat/multi-platform-validation`):**

| Wave | Scope | Files added | Effort |
|------|-------|-------------|--------|
| 1 | Composite actions + 6 single-platform Claude-only workflows | `.github/actions/setup-claude/`, `compat-command.yml`, `compat-agent.yml`, `compat-monitor.yml`, `compat-output-style.yml`, `compat-theme.yml`, `compat-marketplace-add.yml` (claude row only) | 4–6 hrs |
| 2 | Matrix workflows for free-in-CI platforms | `compat-skill.yml` (claude + devin), `compat-rule.yml` (4 platforms), `compat-mcp.yml` (claude + devin), `compat-hook.yml` (claude only initially), `setup-devin/`, `setup-cursor-doctor/` | 6–8 hrs |
| 3 | Codex + Gemini advisory rows in existing matrices + local fallback scripts | `setup-codex/`, `setup-gemini/`, `scripts/validate-codex-local.sh`, `scripts/validate-gemini-local.sh`, `LOCAL_DEVELOPMENT.md` update | 3–4 hrs |
| 4 | Whitelist follow-up — flip Codex/Gemini advisory → required when granted | one-line edits per workflow | 30 min |

**Total estimated effort:** ~15–20 hours of implementation work + the indeterminate whitelist process.

---

## 9. Remaining Open Questions

Three smaller questions deferred to implementation time (Wave 1/2 of the implementation PR):

1. **Composite action cache strategy.** npm installs are 5–10s each; multiplied across many workflows × platforms = significant CI cost. Should `setup-codex` etc. use `actions/cache` for `~/.npm` and the installed binary? Decide during Wave 1 by measuring actual runner cost.

2. **Devin CLI install cost in CI.** The `curl ... | bash` installer is large; consider caching the installed binary across runs. Decide during Wave 2 once the actual Devin workflow is being authored.

3. **Should `compat-marketplace-add.yml` also test Devin's filesystem-only "registration" (just verifying `devin rules list` sees our mirrors)?** Devin doesn't have a marketplace concept but its native cross-platform reading IS our cross-platform compatibility surface. Lean: yes, add a Devin row in advisory mode — but defer the call until Wave 2 since the related `compat-rule.yml` already covers `devin rules list` assertions.

These three are intentionally left for implementation-time empirical resolution rather than pre-committed to here.

### Resolved questions (moved to Section 4 above)

Five questions from the earlier draft of this section are now locked decisions and moved to Section 4: composite action publishing (in-repo), test isolation (per-job), platform-breakage policy (block release), promotion path (immediate after one green run), and the four decisions from the original Phase A round (branch, advisory, structure, whitelist).

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
