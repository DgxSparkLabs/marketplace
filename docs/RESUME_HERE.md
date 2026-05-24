# Resume Here

**This is the first file to read when returning to this project after any break.** Don't read anything else first.

Updated 2026-05-24 after the cross-platform native install fix (Phase 1 generator additions + Phase 2 README rewrite + CI all green in real GHA). Previous version documented the post-DI-refactor state before this round.

---

## 30-Second TLDR

This repo (`DgxSparkLabs/marketplace`) is a **multi-platform plugin marketplace** for Claude Code, Codex, Gemini, Cursor, Windsurf, and Devin. The generator emits **platform-native** per-plugin manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`) plus a shared `.agents/skills/` mirror — so each platform's native install command actually works end-to-end. PR #1 is open against `main`, all 11 CI workflows green, ready to merge.

---

## You Are Here

```
Active branch:         feat/claude-plugin-compliance
Tip commit:            70e55d6 (docs(readme): add GitHub-direct install support matrix + reframe opener)
Open PRs:              #1 at https://github.com/DgxSparkLabs/marketplace/pull/1 — MERGEABLE
CI status:             ALL 11 WORKFLOWS GREEN on 70e55d6 (including new Gemini GitHub URL install assertion)
Status:                Phase 1 + Phase 2 complete. End-to-end install proven for Claude/Codex/Gemini in real GHA. Awaiting merge call.
Working directory:     C:\Users\devic\source\marketplace
Last session ended:    2026-05-24, after cross-platform install fix verification + push to main awaited
```

**Cross-references for context-loading:**
- Project state (longer): [`../HANDOFF.md`](../HANDOFF.md)
- This round's plan + locked decisions: [`archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md`](./archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md)
- Ground-truth verification synthesis: [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md)
- Per-claim act evidence: [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md)
- Cursor (IDE + CLI) May 2026 research: [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/cursor.md)
- Implementer's commit-by-commit report: [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_REPORT.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_REPORT.md)
- Validator's APPROVED verdict: [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md)
- Phase 2 README rewrite report: [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/README_REWRITE_REPORT.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/README_REWRITE_REPORT.md)
- DI refactor (prior round): [`archive/di-refactor/PLAN_DI_REFACTOR.md`](./archive/di-refactor/PLAN_DI_REFACTOR.md)
- User-facing install/use: [`../README.md`](../README.md)

---

## Architecture (Post Cross-Platform Install Fix)

The generator now orchestrates **7 platforms** through **6 phases** plus per-plugin native-manifest emission:

```
scripts/utils.py        — shared helpers
scripts/constructs.py   — 10 Construct classes
scripts/platforms.py    — 7 Platform classes (Claude, Codex, Gemini, Cursor, Windsurf, Devin, AgentsPlatform)
                          + Platform.build_plugin_json(construct, name) protocol method
scripts/bundles.py      — Bundle dataclass + load_bundles
scripts/generate_manifest.py — orchestrator; 6 phases:
  Phase 1:   individual plugins (construct.emit per source instance, Claude-side)
  Phase 1.5: per-platform per-plugin manifests (supports-gated emission of
             .codex-plugin/plugin.json + .cursor-plugin/plugin.json)
  Phase 2a:  catalog bundles from catalog.toml [bundle.*]
  Phase 2b:  code-generated catch-alls (bundle-<prefix>-all)
  Phase 3:   cross-platform mirrors (platform.emit per supported construct,
             includes .agents/skills/ via AgentsPlatform)
  Phase 4:   Gemini extension manifest at .gemini/gemini-extension.json
  Phase 4.5: copy .gemini/gemini-extension.json to repo root (enables GitHub URL install)
  Phase 5:   marketplace.json from in-memory entries
  Phase 6:   .cursor-plugin/marketplace.json at repo root (enables Cursor team-import)
catalog.toml — bundle definitions ONLY
```

### Key architectural decisions (this round)

| # | Decision | Where |
|---|----------|-------|
| A1 | `AgentsPlatform` is a proper Platform class (not a special-case step) | [`archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md`](./archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md) |
| B2 | Per-plugin native manifests gated on `platform.supports` (e.g., theme plugins get no `.codex-plugin/` because ThemeConstruct ∉ CodexPlatform.supports) | Same |
| C1 | CI assertions + generator additions shipped in same PR (#1 expanded scope) | Same |
| Q2 | All work on `feat/claude-plugin-compliance`; no new branch | Same |

DI refactor decisions (prior round) still hold — see [`archive/di-refactor/PLAN_DI_REFACTOR.md`](./archive/di-refactor/PLAN_DI_REFACTOR.md) for the 25 there.

---

## What Each Platform Reads (post-Phase-1)

| Platform | Marketplace manifest | Per-plugin manifest | Skill content path | Rule content path |
|----------|---------------------|---------------------|--------------------|--------------------|
| Claude Code | `.claude-plugin/marketplace.json` | `_generated/<plugin>/.claude-plugin/plugin.json` | (via plugin install) | (via plugin install) |
| Codex | `.claude-plugin/marketplace.json` (legacy-compatible) or `.agents/plugins/marketplace.json` | `_generated/<plugin>/.codex-plugin/plugin.json` | `.codex/skills/` (mirror) | reads `AGENTS.md`, `.cursor/rules/`, `.windsurf/rules/` |
| Gemini | `gemini-extension.json` at repo root (for GitHub URL install) or `.gemini/gemini-extension.json` (for local install) | n/a (extensions, not plugins) | `.gemini/skills/` (mirror) | reads `GEMINI.md`, `AGENTS.md` |
| Cursor IDE | `.cursor-plugin/marketplace.json` (team-marketplace import) | `_generated/<plugin>/.cursor-plugin/plugin.json` | `.agents/skills/` (primary, per Cursor docs) | `.cursor/rules/` (auto-load) |
| Windsurf | n/a (no marketplace) | n/a (no CLI) | `.windsurf/skills/` AND `.agents/skills/` (both auto-discovered by Cascade) | `.windsurf/rules/` (auto-load) |
| Devin | n/a (no marketplace) | n/a (no CLI) | `.devin/skills/` AND `.agents/skills/` (both auto-discovered) | reads `.cursor/rules/`, `.windsurf/rules/`, `AGENTS.md` |

---

## Source Structure

```
skills/<name>/          — real skill content + skills/example/
rules/<name>/           — real rule content + rules/example/
commands/<name>/        — commands/example/ (only example today)
agents/<name>/          — agents/example/
hooks/<name>/           — hooks/example/
mcp-servers/<name>/     — mcp-servers/example/
lsp-servers/<name>/     — lsp-servers/example/
monitors/<name>/        — monitors/example/
output-styles/<name>/   — output-styles/example/
themes/<name>/          — themes/example/
```

Examples are `example/` (not `example-<construct>/`).

---

## Plugin Naming

```
Individual:     <prefix>-<name>           e.g., skill-telegram-notify
Catalog bundle: bundle-<bundle-name>      e.g., bundle-communication-skills
Catch-all:      bundle-<prefix>-all       e.g., bundle-skill-all
```

---

## Next Concrete Actions (in priority order)

1. **Merge PR #1** — CI all green on `70e55d6`; this is the only remaining gate. Options:
   - `gh pr merge 1 --squash` — collapses all commits into one (cleanest main history)
   - `gh pr merge 1 --merge` — preserves full commit history with a merge commit (most accurate audit trail)
   - `gh pr merge 1 --rebase` — replays commits linearly (clean linear history, rewrites SHAs)
   - User direction pending as of this writing.

2. **Post-merge follow-up commit (small)** — drop the `--ref feat/claude-plugin-compliance` footnotes from the README; the no-ref forms work post-merge for Codex/Gemini.

3. **(Optional) Verify C2 in real GHA post-merge** — `codex plugin marketplace add DgxSparkLabs/marketplace` (no ref) should now succeed against main. Either spot-test manually or add a one-shot CI job.

4. **(Optional) Maintenance** — retire `.devin/skills/` once Devin's `.agents/skills/` reading is confirmed live (Devin docs say yes; existing `devin skills paths` empirical from May 22 says yes).

---

## Project Glossary

| Term | Meaning here |
|------|--------------|
| **marketplace** | Curated index of installable plugins, declared in platform-native manifest at repo root. |
| **plugin** | A `_generated/<name>/` directory containing per-platform manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/` where applicable) plus construct content. |
| **construct** | One of 10 construct types: skill, rule, command, agent, hook, mcp, lsp, monitor, output-style, theme. |
| **Construct class** | A class in `scripts/constructs.py` implementing the Construct protocol. |
| **Platform class** | A class in `scripts/platforms.py` implementing the Platform protocol (which now includes `build_plugin_json` for per-plugin native manifests). |
| **bundle** | A dep-only plugin declaring dependencies on other plugins. Two kinds: catalog bundles (in `catalog.toml`) and code-generated catch-alls. |
| **catch-all bundle** | `bundle-<prefix>-all` — code-generated, NOT in catalog.toml. |
| **mirror** | An auto-generated directory under `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, `.devin/`, or `.agents/` that copies generated content to the layout each platform expects. |
| **`.agents/` standard** | Cross-platform skill (`.agents/skills/`) and plugin (`.agents/plugins/`) directory convention. Read by Windsurf, Cursor, Devin natively; Codex accepts `.claude-plugin/marketplace.json` as legacy-compatible. |
| **generator** | `scripts/generate_manifest.py` — 6-phase orchestrator. |
| **act-based verification** | Hermetic local-container CI runs via nektos/act for verification before pushing. Scaffolds at `docs/archive/phase-5-cross-platform-install/VERIFICATION_2026-05/workflows/`. |
| **compat workflow** | A `.github/workflows/compat-<construct>.yml` file verifying our marketplace works for that construct across applicable platforms. |

---

## Reading Order (with time budgets)

| Time | Read | Why |
|------|------|-----|
| 90s | This file | Get oriented |
| 5min | [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md) | Single-page ground truth: what works per platform |
| 10min | [`archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md`](./archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md) | This round's plan + locked decisions A1/B2/C1/Q2 |
| 15min | [`archive/di-refactor/PLAN_DI_REFACTOR.md`](./archive/di-refactor/PLAN_DI_REFACTOR.md) Locked Decisions table | 25 prior-round decisions still in force |
| 30min | Above + [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/empirical_act_verification.md) + [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/IMPLEMENTATION_VALIDATION.md) | Full architecture + per-claim evidence + validator's verdict |

---

## Dead Ends (Don't Re-litigate)

- **Codex per-plugin install with only `.claude-plugin/plugin.json`** — fails with `missing or invalid plugin.json`. Codex needs its own `.codex-plugin/plugin.json` (now emitted by Phase 1.5).
- **Gemini GitHub URL install with `gemini-extension.json` only in `.gemini/`** — fails because Gemini looks for it at the cloned repo root. Now also emitted at repo root by Phase 4.5.
- **Cursor binary name `cursor` in headless tests** — the headless CLI is `agent` (with `cursor-agent` as alias). Don't probe for `cursor --version`; probe for `agent --version`.
- **Codex marketplace shortform without `--ref` against main pre-merge** — fails because main lacks the manifest. Auto-resolves on PR #1 merge.
- **Per-plugin manifest emission unconditional across all platforms** — rejected via decision B2; emission is gated on `platform.supports`.
- **CI assertions that test only registration without enumeration/install** — caused real defects to go undetected for weeks; new assertions in `compat-marketplace-add.yml` and `compat-extension.yml` close this gap.
- **`members_from_construct` field in catalog.toml** — removed (DI refactor decision #24).
- **`[bundle.<prefix>-all]` in catalog.toml** — reserved names; `load_bundles` raises ValueError.
- **`example-<construct>` directory naming** — renamed to `example/` (DI refactor decision #18).
- **Hardcoding plugin count (e.g., `== 81`)** — test suite uses a computed formula.

---

## When You Forget Everything

Re-read this file. Then:

1. What to do next → "Next Concrete Actions" above
2. Why a decision was made → [`archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md`](./archive/phase-5-cross-platform-install/PLAN_CROSS_PLATFORM_INSTALL_FIX.md) or [`archive/di-refactor/PLAN_DI_REFACTOR.md`](./archive/di-refactor/PLAN_DI_REFACTOR.md)
3. About to repeat a mistake → "Dead Ends" above
4. Don't recognize a term → "Project Glossary" above
5. Need full ground-truth on what works → [`archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md`](./archive/phase-5-cross-platform-install/VERIFICATION_2026-05/SUMMARY.md)
6. Implementing a new construct or bundle → [`ADDING_A_CONSTRUCT.md`](./ADDING_A_CONSTRUCT.md)
