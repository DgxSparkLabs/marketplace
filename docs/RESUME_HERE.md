# Resume Here

**This is the first file to read when returning to this project after any break.** Don't read anything else first.

Updated 2026-05-24 after the DI refactor (dependency-injection architecture for the generator). Previous version documented the pre-refactor state.

---

## 30-Second TLDR

This repo (`DgxSparkLabs/marketplace`) is a **Claude Code plugin marketplace**. It ships skills, rules, commands, agents, hooks, MCP servers, LSP servers, monitors, output styles, and themes — 10 construct types total. The generator (`scripts/generate_manifest.py`) reads sources + `catalog.toml` and produces everything else. PR #1 is open against `main` and contains the full migration to native `/plugin marketplace add` compliance plus the DI refactor.

---

## You Are Here

```
Active branch:         feat/claude-plugin-compliance
Tip commit:            a872e69 (docs(readme): add table of contents)
Open PRs:              #1 at https://github.com/DgxSparkLabs/marketplace/pull/1 — MERGEABLE
Status:                EVERY WORK PHASE COMPLETE. Awaiting merge call.
Working directory:     C:\Users\devic\source\marketplace
Last session ended:    2026-05-24, after DI refactor + validation + README rewrite
```

**Cross-references for context-loading:**
- Project state (longer): [`../HANDOFF.md`](../HANDOFF.md)
- Architecture (full): [`PLAN_DI_REFACTOR.md`](./PLAN_DI_REFACTOR.md)
- Implementation report: [`DI_REFACTOR_REPORT.md`](./DI_REFACTOR_REPORT.md)
- Validation verdict: [`DI_REFACTOR_VALIDATION_REPORT.md`](./DI_REFACTOR_VALIDATION_REPORT.md)
- User-facing install/use: [`../README.md`](../README.md)

---

## Architecture (Post DI Refactor)

The generator is now a thin orchestrator over typed registries:

```
scripts/utils.py        — shared helpers (scan_source_dir, _load_plugin_json, etc.)
scripts/constructs.py   — 10 Construct classes (SkillConstruct, RuleConstruct, ...)
scripts/platforms.py    — 6 Platform classes (ClaudeCodePlatform, CodexPlatform, ...)
scripts/bundles.py      — Bundle dataclass + load_bundles + BundleMember
scripts/generate_manifest.py — orchestrator (~100 lines); 5 phases:
  Phase 1: individual plugins (construct.emit per source instance)
  Phase 2a: catalog bundles from catalog.toml [bundle.*]
  Phase 2b: code-generated catch-alls (bundle-<prefix>-all per construct)
  Phase 3: cross-platform mirrors (platform.emit per supported construct)
  Phase 4: Gemini extension manifest
  Phase 5: marketplace.json from in-memory entries (never re-reads filesystem)
catalog.toml            — bundle definitions ONLY (no [construct.*] or [skill_domain.*])
```

### Key architectural decisions

| # | Decision |
|---|----------|
| 15 | Construct protocol has TWO methods: `build_plugin_json` (pure) + `emit` (I/O) |
| 16 | Generated plugin path: `_generated/<prefix>-<name>/.claude-plugin/plugin.json` |
| 17 | marketplace.json built from in-memory entries — never re-read from filesystem |
| 18 | Example dirs renamed: `example-<construct>` → `example` (e.g., `skills/example/`) |
| 23 | Catch-all bundles code-generated (not catalog-declared) |
| 24 | `members_from_construct` field removed entirely from Bundle schema |
| 25 | Reserved bundle names: `<prefix>-all`; `load_bundles` raises ValueError if catalog defines them |

Full 25-decision table in [`docs/PLAN_DI_REFACTOR.md`](./PLAN_DI_REFACTOR.md) Locked Decisions section.

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

Examples are `example/` (not `example-<construct>/` — renamed in this refactor).

---

## Plugin Naming

```
Individual:     <prefix>-<name>           e.g., skill-telegram-notify
Catalog bundle: bundle-<bundle-name>      e.g., bundle-communication-skills
Catch-all:      bundle-<prefix>-all       e.g., bundle-skill-all
```

Notable renames from pre-refactor:
- `example-mcp` → `mcp-example`
- `example-skill` → `skill-example`
- `skills-communication` → `bundle-communication-skills`
- `rules-all` → `bundle-rule-all`
- etc.

---

## Next Concrete Actions (in priority order)

1. **Review and merge PR #1** — `gh pr merge 1 --merge` (or `--squash`/`--rebase`). Everything is on `feat/claude-plugin-compliance`: migration + multi-platform validation + DI refactor + README. Validator already verified all 25 locked decisions implemented; CI green on the tip commit. This is the ONLY remaining action.

2. **(Optional) File the GitHub whitelist request** — [`CI_WHITELIST_REQUEST.md`](./CI_WHITELIST_REQUEST.md) text is drafted, BUT [`ORG_POLICY_INVESTIGATION.md`](./ORG_POLICY_INVESTIGATION.md) found no policy ever existed (transient infrastructure event). Submit only if a similar `conclusion=failure, 0 jobs, duration <5s` recurrence is observed.

3. **(Optional) Maintenance** — as Claude Code's plugin spec evolves (e.g., native rule install ships), retire the `activate.sh` workaround. See [`RULE_FORMAT.md`](./RULE_FORMAT.md).

---

## Project Glossary

| Term | Meaning here |
|------|--------------|
| **marketplace** | A curated index of installable Claude Code plugins, declared in `.claude-plugin/marketplace.json`. Ours is named `dgxsparklabs-marketplace`. |
| **plugin** | A directory containing `.claude-plugin/plugin.json` plus construct content. |
| **construct** | One of 10 Claude Code plugin construct types: skill, rule, command, agent, hook, mcp, lsp, monitor, output-style, theme. |
| **Construct class** | A Python class in `scripts/constructs.py` implementing the Construct protocol. |
| **Platform class** | A Python class in `scripts/platforms.py` implementing the Platform protocol. |
| **bundle** | A dep-only plugin whose job is to declare dependencies on other plugins. Two kinds: catalog bundles (in `catalog.toml`) and code-generated catch-alls (one per construct). |
| **catch-all bundle** | `bundle-<prefix>-all` — code-generated by Phase 2b of the generator. Contains every instance of one construct type. NOT declared in catalog.toml. |
| **mirror** | An auto-generated directory under `.codex/`, `.gemini/`, `.cursor/`, `.windsurf/`, or `.devin/` that copies our generated content into the layout each non-Claude-Code CLI expects. |
| **generator** | `scripts/generate_manifest.py` — thin orchestrator. Reads sources + catalog.toml; produces everything else. |
| **activate.sh** | Per-rule plugin shell script that symlinks (or copies on Windows) the rule file into `.claude/rules/`. Workaround for the lack of a `rules` field in Claude Code's plugin spec. |
| **compat workflow** | A `.github/workflows/compat-<construct>.yml` file that verifies our marketplace works for that construct across applicable platforms. |
| **wave** | Implementation phase in the validation plan. Wave 4 = Codex/Gemini promoted from advisory after whitelist granted. |

---

## Reading Order (with time budgets)

| Time | Read | Why |
|------|------|-----|
| 90s | This file | Get oriented |
| 5min | `docs/PLAN_DI_REFACTOR.md` Locked Decisions table | The 25 locked decisions for the DI refactor |
| 10min | `docs/CONSTRUCT_TYPES.md` + `docs/ADDING_A_CONSTRUCT.md` | What the marketplace ships + contribution workflow |
| 20min | `docs/PLATFORM_VALIDATION_CICD_PLAN.md` Section 4 | 25 locked validation CI decisions |
| 30min | `docs/PLAN_DI_REFACTOR.md` (full) + `docs/PLATFORM_INSPECTION_CATALOG.md` | Full DI architecture + empirical CLI catalog |

---

## Dead Ends (Don't Re-litigate)

Same as before plus:

- **`members_from_construct` field in catalog.toml** — removed (decision #24). Catch-alls are code-generated, not catalog-declared.
- **`[bundle.<prefix>-all]` in catalog.toml** — reserved names; `load_bundles` raises ValueError.
- **`example-<construct>` directory naming** — renamed to `example/` (decision #18). Don't revert.
- **Hardcoding plugin count (e.g., `== 81`)** — the test suite uses a computed formula now (NICE 1 fix).

---

## When You Forget Everything

Re-read this file. Then:

1. What to do next → "Next Concrete Actions" above
2. Why a decision was made → `docs/PLAN_DI_REFACTOR.md` Locked Decisions table
3. About to repeat a mistake → "Dead Ends" above
4. Don't recognize a term → "Project Glossary" above
5. Need full architecture → `docs/PLAN_DI_REFACTOR.md` + `docs/PLATFORM_VALIDATION_CICD_PLAN.md`
6. Implementing a new construct or bundle → `docs/ADDING_A_CONSTRUCT.md`
