## Summary

Three combined features, originally planned as separate PRs but merged here under
the "1 PR" finalization strategy:

1. **Plugin marketplace compliance migration** — replaces the curl-bootstrapped
   Textual TUI installer with native Claude Code `/plugin marketplace add
   DgxSparkLabs/marketplace`. 81 plugin entries: 26 skills + 8 skill-domain
   bundles + 21 rules + 6 rule-domain bundles + 10 examples (native locations)
   + 10 example-bundle plugins.

2. **Multi-platform validation CI** — 10 compat-*.yml workflows + 5 composite
   actions in `.github/actions/setup-<platform>/` + 2 local-dev fallback
   scripts. Validates that every plugin-installable construct works on
   Claude Code, Devin, Codex, Gemini (Cursor + Windsurf intentionally
   excluded — no headless CLI). Generator extended to emit
   `.gemini/gemini-extension.json` for Gemini extension validation.

3. **Native construct folders (Option D restructure)** — examples now live in
   their construct's native folder instead of a separate `examples/` directory.
   8 new top-level source folders added: `commands/`, `agents/`, `hooks/`,
   `mcp-servers/`, `lsp-servers/`, `monitors/`, `output-styles/`, `themes/`.
   Each construct's `example-<type>/` lives directly inside it.

## Reading order (for reviewers)

Fast orientation (90s): `docs/RESUME_HERE.md`

Full design dossier:
- `docs/GOAL_PLUGIN_COMPLIANCE.md` — 12 binary success criteria (migration)
- `docs/PLAN_PLUGIN_COMPLIANCE.md` — migration architecture
- `docs/INVESTIGATION_PLUGIN_DEPENDENCIES.md` — empirical dep auto-install proof
- `docs/PLATFORM_INSPECTION_CATALOG.md` — executable spec, every CI assertion
- `docs/PLATFORM_VALIDATION_CICD_PLAN.md` — CI design + 20 locked decisions
- `docs/ORG_POLICY_INVESTIGATION.md` — root-cause analysis for the transient
  Codex/Gemini install failure (with canary signature for future recurrence)
- `docs/RESTRUCTURE_REPORT.md` — Option D restructure summary

Verification artifacts (cycle history, useful if reviewing assertion choices):
- `docs/VERIFICATION_REPORT.md` — first CI cycle (1 required failure found)
- `docs/FIX_REPORT.md` — fix cycle (1 required + 2 advisory fixes + catalog updates)
- `docs/FINALIZATION_REPORT.md` — Wave 4 promotion + generator extension + clean CI

## What's installable after merge

```bash
/plugin marketplace add DgxSparkLabs/marketplace

# Individual skill
/plugin install skill-telegram-notify@dgxsparklabs-marketplace

# Domain bundle (auto-installs every member)
/plugin install skills-communication@dgxsparklabs-marketplace

# Individual rule + activation symlink
/plugin install rule-blast-radius@dgxsparklabs-marketplace
bash ~/.claude/plugins/cache/dgxsparklabs-marketplace/rule-blast-radius/<v>/activate.sh

# All rules bundle + bulk activator
/plugin install rules-all@dgxsparklabs-marketplace
bash <repo>/activate-installed-rules.sh

# Reference example plugins (in their native construct folders)
/plugin install example-skill@dgxsparklabs-marketplace
/plugin install example-command@dgxsparklabs-marketplace
# ... and so on for each of the 10 construct types

# Example bundles (install the reference example for a construct type)
/plugin install skills-examples@dgxsparklabs-marketplace
/plugin install commands-examples@dgxsparklabs-marketplace
```

For Devin / Cursor / Windsurf / Codex CLI / Gemini CLI: `git clone` and point
at the auto-generated mirrors (`.devin/`, `.cursor/`, `.windsurf/`, `.codex/`,
`.gemini/`).

## Contributing a new plugin

Each construct's example now lives in its native folder — copy it in place:

```bash
cp -r skills/example-skill skills/my-new-skill
cp -r commands/example-command commands/my-new-command
cp -r agents/example-agent agents/my-new-agent
# ... etc.
```

See `docs/ADDING_A_SKILL.md`, `docs/ADDING_A_RULE.md`, and the other
`docs/ADDING_*.md` files for full per-construct workflows.

## Breaking changes

- **Deleted:** `install.py` (TUI), `scripts/install.sh` (curl bootstrap),
  `scripts/install-rule.sh`, `rules/<name>/install.sh` × 21, `pyproject.toml`,
  `uv.lock`, `_template/`.
- **Moved:** `examples/example-<type>/` → `<type-folder>/example-<type>/`.
  Any external link to `examples/` paths (e.g., in compat workflows) should
  be updated to the new native paths.
- **`curl ... | bash` users** will get a 404 after merge — switch to
  `/plugin marketplace add DgxSparkLabs/marketplace`.

## Validation CI

Workflows (all 10 compat-*.yml required after Wave 4 promotion; zero advisory):

- `compat-skill.yml` — Claude + Devin + Codex + Gemini
- `compat-command.yml`, `compat-agent.yml`, `compat-monitor.yml`,
  `compat-output-style.yml`, `compat-theme.yml` — Claude only
- `compat-hook.yml` — Claude only (Gemini hook migration is destructive,
  no non-destructive assertion path — documented in catalog)
- `compat-mcp.yml` — Claude + Devin + Codex + Gemini
- `compat-extension.yml` — Gemini (full install + validate + list + uninstall)
- `compat-marketplace-add.yml` — Claude + Codex

Composite actions: `setup-claude/`, `setup-codex/`, `setup-gemini/`,
`setup-devin/`, `setup-cursor-doctor/` — all follow the standard contract:
`inputs.version` (default `'latest'`) + `outputs.installed` boolean.

Local-dev fallbacks: `scripts/validate-codex-local.sh`,
`scripts/validate-gemini-local.sh` — preserved for contributors whose CI is
restricted; run the same assertions locally.

## Test plan

Migration (manual, verified locally on Windows Git Bash):
- [x] `uv run scripts/generate_manifest.py --check` passes
- [x] `uv run tests/test_marketplace.py` — 55 tests, all green
- [x] CI passes the explicit `--check` step and the test suite
- [x] `claude plugin marketplace add <fork-url>` registers as
      `dgxsparklabs-marketplace`
- [x] Individual skill install + invocation works
- [x] Domain bundle auto-installs member skills
- [x] Individual rule install + `activate.sh` symlinks (with Windows-safe
      copy fallback)
- [x] Rules-all bundle + bulk activator symlinks every rule

Native construct folder restructure (verified locally):
- [x] All 10 example plugins `git mv`'d to native folders; `examples/` removed
- [x] 8 new top-level construct folders created and visible in repo root
- [x] `catalog.toml` updated: all `example_directory` fields + 10 new
      `[<construct>_domain.examples]` sections
- [x] Generator produces 81 entries: 10 new example-bundle plugins
- [x] 55 tests all pass (15 new tests added, 1 obsolete test replaced)
- [x] Drift check clean

Validation CI (automated, verified across 3 clean CI runs on the integration branch):
- [x] All 10 compat workflows pass on the integration branch
- [x] Wave 4 promotion holds — Codex/Gemini required, not advisory
- [x] Generator emits `.gemini/gemini-extension.json` consumable by
      `gemini extensions validate`
- [ ] All 10 compat workflows pass on `feat/claude-plugin-compliance` after
      the merge (currently in flight)
