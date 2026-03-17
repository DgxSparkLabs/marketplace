# python-uv

An always-on rule that forces AI agents to use `uv` for all Python operations — running scripts, managing dependencies, creating virtualenvs, and installing tools. Prevents use of `pip`, `venv`, `conda`, `poetry`, and other legacy tooling.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Quick Install

```bash
git clone https://github.com/ForkYoraiLevi/marketplace.git /tmp/marketplace

# Install into current project (AGENTS.md)
/tmp/marketplace/python-uv/install.sh

# Install globally (all projects)
/tmp/marketplace/python-uv/install.sh --global

# Install for a specific tool only
/tmp/marketplace/python-uv/install.sh --format windsurf
/tmp/marketplace/python-uv/install.sh --format cursor
/tmp/marketplace/python-uv/install.sh --format agents
```

## Manual Install

Copy the appropriate format file to your project or global config:

### AGENTS.md (universal)

Append the contents of `rule.md` to your project's `AGENTS.md`:

```bash
cat python-uv/rule.md >> AGENTS.md
```

### Windsurf

```bash
mkdir -p .windsurf/rules
cp python-uv/formats/windsurf.md .windsurf/rules/python-uv.md
```

### Cursor

```bash
mkdir -p .cursor/rules
cp python-uv/formats/cursor.md .cursor/rules/python-uv.md
```
## What it enforces

- Use `uv run` with PEP 723 inline metadata for scripts
- Use `uv add` / `uv remove` for project dependencies
- Use `uv venv` instead of `python -m venv` or `virtualenv`
- Use `uv tool install` instead of `pip install --user` or `pipx`
- Never `pip install`, `pip freeze`, or `requirements.txt` for new projects
- Respect existing pip/requirements.txt projects — do not migrate without asking

## How it works

This is a **rule**, not a skill. Rules are loaded automatically at session start and stay active for the entire session. No invocation needed.

| Format | File installed | Activation |
|--------|---------------|------------|
| AGENTS.md | `AGENTS.md` (appended) | Always on |
| Windsurf | `.windsurf/rules/python-uv.md` | `trigger: always_on` |
| Cursor | `.cursor/rules/python-uv.md` | `alwaysApply: true` |
