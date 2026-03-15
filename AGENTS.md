# Agent Instructions

This is a skills and rules marketplace. Not a software project — no build system, no package manager.

Each top-level directory (except `docs/`, `_template/`, dotfiles) is a skill or rule.
- Has `SKILL.md` → skill
- Has `rule.md` + `install.sh` → rule

## Layout

```
marketplace/
├── docs/
│   ├── SKILL_FORMAT.md         # Full SKILL.md spec
│   └── RULE_FORMAT.md          # Full rule spec
├── _template/                  # Starter for new skills
├── no-ai-credit/               # Reference rule
├── send-email/                 # Reference skill
└── <new-item>/
```

## Adding a Skill

Use `_template/` as a starter. Full spec in `docs/SKILL_FORMAT.md`.

```
my-skill/
├── SKILL.md            # Required
├── README.md           # Required
├── scripts/            # Optional
├── setup.sh            # Optional — prerequisite installer
└── references/         # Optional
```

- Python scripts must use PEP 723 inline metadata (`uv run` with zero install)
- Always set `allowed-tools` to minimum needed
- Update the **Skills** table in root `README.md` (alphabetical)

## Adding a Rule

Use `no-ai-credit/` as a reference. Full spec in `docs/RULE_FORMAT.md`.

```
my-rule/
├── rule.md             # Required — plain Markdown, no frontmatter
├── README.md           # Required
├── install.sh          # Required — supports --global and --format
└── formats/
    ├── windsurf.md     # trigger: always_on
    └── cursor.md       # alwaysApply: true
```

- Copy and adapt `no-ai-credit/install.sh`
- Update the **Rules** table in root `README.md` (alphabetical)

## Conventions

- Directory names: **kebab-case**
- Script filenames: **snake_case** for Python, **kebab-case** allowed for shell scripts
- Python scripts: PEP 723, runnable via `uv run`
- Shell scripts: shebang + `set -euo pipefail`
- Never commit secrets
- Do not add project-level config (`pyproject.toml`, `package.json`, etc.) at root
- Do not mix skill and rule formats in one directory

## Verify Your Work

When building new capabilities — skills, tools, scripts, integrations, or any functional artifact — you MUST verify that what you produce actually works before declaring the task complete. Do not assume correctness. Prove it.

### Core Principles

1. **Test everything you create.** Run the code. Execute the script. Invoke the tool. If it produces output, inspect the output. If it has side effects, confirm they occurred. Never hand off untested work.

2. **Be maximally autonomous.** Do not ask the user for help unless you genuinely cannot proceed without them. Exhaust all reasonable approaches first: read docs, search the codebase, try alternative implementations, debug errors yourself.

3. **Pause for what only the user can provide.** Some things require human action — API keys, OAuth consent, account credentials, service subscriptions, hardware access, or policy decisions. When you hit one of these, STOP immediately and prompt the user with:
   - Exactly what you need and why
   - Where to get it (signup URL, dashboard link, docs page)
   - How to provide it (env var name, file path, command to run)
   - What you will do once you have it

### Verification Checklist

Before marking any implementation task as done, confirm:

- [ ] **Runs without errors** — you executed the code and it completed successfully
- [ ] **Produces correct output** — the result matches what was expected, not just "no crash"
- [ ] **Edge cases considered** — empty inputs, missing config, network failures, permission errors
- [ ] **Dependencies documented** — any required env vars, API keys, or tools are listed clearly
- [ ] **Idempotent where possible** — running it twice does not break things

### When You Cannot Fully Verify

Some things cannot be tested without credentials or external services. In these cases:

1. Test everything you can — syntax, structure, logic paths, dry-run modes
2. Clearly state what was verified and what was not
3. Provide the user with exact steps to complete verification themselves
4. Do NOT say "should work" or "looks correct" — say what you tested and what remains untested

### User-Dependent Setup

When the implementation requires something from the user (API keys, tokens, accounts), follow this pattern:

1. **Build first** — implement as much as possible before asking
2. **Batch your asks** — collect all needed credentials/config into a single prompt, not one at a time
3. **Provide clear instructions** — include URLs, expected format, env var names
4. **Wait for the user** — do not proceed with placeholder values or skip the integration
5. **Verify after setup** — once the user provides what you need, run the full verification

### What NOT to Do

- Do NOT claim something works without running it
- Do NOT skip testing because "it's simple" or "obvious"
- Do NOT silently swallow errors and report success
- Do NOT ask the user to test things you could test yourself
- Do NOT proceed past a missing credential by hardcoding a dummy value
