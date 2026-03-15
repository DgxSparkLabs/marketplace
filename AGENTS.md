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
- Script filenames: **snake_case**
- Python scripts: PEP 723, runnable via `uv run`
- Shell scripts: shebang + `set -euo pipefail`
- Never commit secrets
- Do not add project-level config (`pyproject.toml`, `package.json`, etc.) at root
- Do not mix skill and rule formats in one directory
