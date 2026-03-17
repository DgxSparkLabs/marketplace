---
trigger: always_on
description: "Use uv for all Python operations — never pip, venv, conda, or poetry"
---

## Python UV

ALWAYS use `uv`. NEVER use `pip`, `pip install`, `virtualenv`, `venv`, `pyenv`, `conda`, or `poetry`.

- **Scripts:** PEP 723 inline metadata + `uv run script.py`
- **Projects:** `uv init`, `uv add`, `uv sync`, `uv run`
- **Virtualenvs:** `uv venv` (never `python -m venv`)
- **Global tools:** `uv tool install` (never `pip install --user` or `pipx`)
- If an existing project uses pip/requirements.txt, follow its conventions — do not migrate without asking.
