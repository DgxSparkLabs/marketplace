# python-uv

An always-on rule that forces AI agents to use `uv` for all Python operations — running scripts, managing dependencies, creating virtualenvs, and installing tools. Prevents use of `pip`, `venv`, `conda`, `poetry`, and other legacy tooling.

Unlike a skill (which must be invoked), this is a **rule** — it activates automatically in every session with no user action needed.

## Install

### Claude Code (filesystem only — not a plugin)

Per code.claude.com/docs/en/plugins-reference (2026-05-26), rules are not a Claude plugin component. Install into Claude's memory subsystem at `.claude/rules/` directly:

```bash
mkdir -p .claude/rules
ln -s "$(pwd)/rules/python-uv/rule.md" .claude/rules/python-uv.md   # symlink (live updates)
# or:
cp rules/python-uv/rule.md .claude/rules/python-uv.md                # copy (portable)
```

For user-scope (every project on this machine), replace `.claude/rules/` with `~/.claude/rules/`. See `docs/USER_GUIDE.md` Claude section for the full operator workflow.

### Cursor / Codex / Gemini / Windsurf

`rule-python-uv` IS still a plugin for these platforms. Install via the platform's native marketplace surface or clone the marketplace; the rule is auto-mirrored to `.cursor/rules/`, `.windsurf/rules/`, etc.


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
