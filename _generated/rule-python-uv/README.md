# python-uv

An always-on rule that forces AI agents to use `uv` for all Python operations — running scripts, managing dependencies, creating virtualenvs, and installing tools. Prevents use of `pip`, `venv`, `conda`, `poetry`, and other legacy tooling.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

```bash
# Native Claude Code plugin install:
/plugin marketplace add DgxSparkLabs/marketplace
/plugin install rule-python-uv@marketplace

# Then activate (one-time):
bash ~/.claude/plugins/cache/DgxSparkLabs/marketplace/rule-python-uv/activate.sh
```nFor other platforms (Devin, Cursor, Windsurf), see the auto-generated mirrors in `.devin/rules/`, `.cursor/rules/`, `.windsurf/rules/` after `git clone`.

## What it enforces

- Use `uv run` with PEP 723 inline metadata for scripts
- Use `uv add` / `uv remove` for project dependencies
- Use `uv venv` instead of `python -m venv` or `virtualenv`
- Use `uv run pytest` for running tests (add pytest with `uv add --dev pytest`)
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
