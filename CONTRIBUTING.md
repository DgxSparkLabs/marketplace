# Contributing

Thanks for your interest in contributing to the marketplace.

This repo contains two types of items: **skills** (invoked on demand) and **rules** (always-on). For the full format specifications, see:
- [docs/SKILL_FORMAT.md](./docs/SKILL_FORMAT.md) — SKILL.md specification
- [docs/RULE_FORMAT.md](./docs/RULE_FORMAT.md) — Rule format specification

---

## Adding a New Skill

### 1. Copy the template

```bash
cp -r _template/ skills/my-skill/
```

Replace all `REPLACE` placeholders in the copied files.

### 2. Skill directory structure

```
my-skill/
├── SKILL.md            # Required — skill definition with YAML frontmatter and prompt
├── README.md           # Required — user-facing documentation
├── scripts/            # Optional — supporting scripts (Python, shell, etc.)
├── setup.sh            # Optional — prerequisite installer (e.g., API setup, tool install)
└── references/         # Optional — reference docs that can be included via @ syntax
```

### 3. Write the SKILL.md

See [docs/SKILL_FORMAT.md](./docs/SKILL_FORMAT.md) for the full field reference.

### 4. Write supporting scripts

- **Python**: Use PEP 723 inline metadata so `uv run scripts/name.py` works with zero install:
  ```python
  # /// script
  # requires-python = ">=3.11"
  # dependencies = ["some-library>=1.0.0"]
  # ///
  ```
- **Shell**: Include a shebang and `set -euo pipefail`
- Never hardcode secrets. Use environment variables.
- Scripts must be self-contained.

### 5. Write the skill README.md

Include: one-line description, setup/prerequisites, usage examples, options table, installation instructions. Use [skills/send-email/README.md](./skills/send-email/README.md) as a reference.

### 6. Update the root README.md

Add a row to the **Skills** table in the `## Catalog` section. Keep it sorted alphabetically.

---

## Adding a New Rule

### 1. Copy the reference

Use `no-ai-credit/` as a starting point:

```bash
cp -r rules/no-ai-credit/ rules/my-rule/
```

### 2. Rule directory structure

```
my-rule/
├── rule.md             # Required — rule content in plain Markdown (no frontmatter)
├── README.md           # Required — documentation with install instructions
├── install.sh          # Required — multi-format install script
└── formats/            # Required — tool-specific rule files
    ├── windsurf.md     # trigger: always_on
    └── cursor.md       # alwaysApply: true
```

### 3. Write rule.md

Plain Markdown, no frontmatter. This is the universal format (AGENTS.md).

### 4. Create format-specific files

Wrap the same rule content with tool-specific frontmatter. See [docs/RULE_FORMAT.md](./docs/RULE_FORMAT.md).

### 5. Adapt install.sh

Update the install script to use your rule name and check for your rule's identifier when deduplicating.

### 6. Write the rule README.md

Include: what it enforces, quick install commands, manual install for each format, how-it-works table. Use [rules/no-ai-credit/README.md](./rules/no-ai-credit/README.md) as a reference.

### 7. Update the root README.md

Add a row to the **Rules** table in the `## Catalog` section. Keep it sorted alphabetically.

---

## Quality Checklist

### Skills

- [ ] `SKILL.md` has valid YAML frontmatter with `name` and `description` (recommended but technically optional per spec)
- [ ] `allowed-tools` is set and restricted to only what the skill needs
- [ ] The prompt body gives clear, actionable instructions
- [ ] Scripts are self-contained (PEP 723 for Python, no global deps assumed)
- [ ] No secrets, API keys, or credentials are committed
- [ ] `README.md` documents setup, usage, and requirements
- [ ] The catalog table in root `README.md` is updated
- [ ] The skill has been tested in an agent session

### Rules

- [ ] `rule.md` contains clear, enforceable instructions
- [ ] `formats/windsurf.md` uses `trigger: always_on` frontmatter
- [ ] `formats/cursor.md` uses `alwaysApply: true` frontmatter
- [ ] `install.sh` is executable, supports `--global` and `--format`, and is idempotent
- [ ] No secrets, API keys, or credentials are committed
- [ ] `README.md` documents what the rule enforces and how to install
- [ ] The catalog table in root `README.md` is updated
- [ ] The rule has been tested by installing it and verifying it loads

---

## Testing

This project has an automated test suite that validates all skills, rules, and install scripts. **All tests must pass before any changes are submitted.**

### Running tests

```bash
uv run tests/test_marketplace.py        # all tests (104)
uv run tests/test_marketplace.py -v     # verbose output
uv run tests/test_marketplace.py -k skill  # only skill tests
uv run tests/test_marketplace.py -k rule   # only rule tests
```

### What the tests check

- Directory structure (required files present, correct naming)
- YAML frontmatter (valid syntax, required fields)
- Catalog consistency (README.md table matches actual directories)
- PEP 723 metadata (Python scripts have inline dependency declarations)
- Shell script safety (shebang, `set -euo pipefail`)
- Install script behavior (`--help`, `--global`, idempotency)
- Format file content parity (Windsurf/Cursor files match rule.md)
- Secret scanning (no API keys, tokens, or credentials committed)

### Running CI locally

Use [act](https://github.com/nektos/act) with podman to run the full GitHub Actions workflow:

```bash
./tests/run-ci-local.sh          # run the full CI workflow locally
./tests/run-ci-local.sh -n       # dry-run (no container)
```

---

## Submitting

1. Fork this repository
2. Add your skill directory under `skills/` or rule directory under `rules/`
3. Update the catalog in `README.md`
4. Run `uv run tests/test_marketplace.py` — all tests must pass
5. Open a pull request

Commit message format:
```
Add <name> skill|rule

<one-line description>
```

---

## Best Practices

- **One item, one job.** Keep skills and rules focused on a single concern.
- **Restrict tools.** For skills, always set `allowed-tools` to the minimum needed.
- **Self-contained scripts.** Use PEP 723 inline metadata for Python so `uv run` works without a separate install step.
- **No hardcoded paths.** Use environment variables or arguments for all configuration.
- **Document prerequisites.** If something needs an API key, a CLI tool, or a service, say so in both the SKILL.md/rule.md and README.md.
- **Test before submitting.** Install the skill/rule and verify it works in a real agent session.
- **Read AGENTS.md first.** It contains project conventions, research directory rules, and verification requirements.
