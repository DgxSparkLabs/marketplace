# project-bootstrap

Initialize the three-tier documentation structure for any project so agents have the files they need from session one.

## Setup

No setup required. The script is self-contained with no external dependencies.

## Usage

```bash
uv run project-bootstrap/scripts/bootstrap.py
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--name` | No | Project name for headers (default: directory name) |
| `--dir` | No | Target directory (default: cwd) |
| `--force` | No | Overwrite existing files |
| `--dry-run` | No | Preview without writing |

### Examples

```bash
# Bootstrap current directory
uv run project-bootstrap/scripts/bootstrap.py

# Bootstrap with a project name
uv run project-bootstrap/scripts/bootstrap.py --name "my-api"

# Bootstrap a different directory
uv run project-bootstrap/scripts/bootstrap.py --dir /path/to/project --name "my-api"

# Preview what would be created
uv run project-bootstrap/scripts/bootstrap.py --dry-run
```

## Files Created

| File | Purpose |
|------|---------|
| `AGENTS.md` | Project-specific rules and conventions |
| `HANDOFF.md` | Current state — what works, how to build/test, what's next |
| `CHANGELOG.md` | Append-only milestone history |
| `PITFALLS.md` | Bugs encountered and lessons learned |

Existing files are preserved by default.

## As an Agent Skill

```bash
cp -r project-bootstrap/ ~/.config/devin/skills/project-bootstrap/
```

Then invoke with `/project-bootstrap` in a session.
