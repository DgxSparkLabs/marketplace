# REPLACE: skill-name

One-sentence description of what this skill does.

## Setup

1. Prerequisite one (e.g., get an API key)
   ```bash
   export SOME_API_KEY="..."
   ```
2. Prerequisite two (e.g., install a tool)
   ```bash
   curl -LsSf https://example.com/install.sh | sh
   ```

## Usage

The script is self-contained with inline dependencies (PEP 723). No install step needed:

```bash
uv run _template/scripts/example.py --flag "value"
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--flag` | Yes | Description of this flag |
| `--optional` | No | Description of this optional flag |

### Examples

```bash
# Basic usage
uv run _template/scripts/example.py --flag "hello"

# Advanced usage
uv run _template/scripts/example.py --flag "hello" --optional "world"
```

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r _template/ ~/.config/devin/skills/_template/
# or: cp -r _template/ ~/.windsurf/skills/_template/

# Project-specific
cp -r _template/ /path/to/project/.devin/skills/_template/
# or: cp -r _template/ /path/to/project/.windsurf/skills/_template/
```

Then invoke with `/_template` in a session.
