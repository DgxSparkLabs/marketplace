# github-repo-setup

Create a GitHub repository from a local git repo and configure it with CI workflows, branch protection rulesets, and branch naming conventions.

## Setup

1. Install the GitHub CLI:
   ```bash
   # Debian/Ubuntu
   sudo apt install gh

   # macOS
   brew install gh
   ```

2. Authenticate:
   ```bash
   gh auth login
   ```
   Ensure your token has `repo` and `workflow` scopes. If not:
   ```bash
   gh auth refresh -s repo,workflow
   ```

## Usage

```bash
# Full setup (CI + rulesets + branch naming)
bash github-repo-setup/scripts/setup_repo.sh

# With options
bash github-repo-setup/scripts/setup_repo.sh --visibility private --description "My project"

# Skip CI generation (just repo + rulesets)
bash github-repo-setup/scripts/setup_repo.sh --no-ci

# Dry run
bash github-repo-setup/scripts/setup_repo.sh --dry-run
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `--visibility <public\|private>` | No | Repo visibility (default: public) |
| `--description "<text>"` | No | Repository description |
| `--no-ci` | No | Skip CI workflow generation |
| `--no-rulesets` | No | Skip branch protection rulesets |
| `--dry-run` | No | Show what would be done |

### Examples

```bash
# Create a public Rust project with full CI
cd my-rust-project
bash github-repo-setup/scripts/setup_repo.sh --description "A fast CLI tool"

# Create a private Python project, skip rulesets
cd my-python-lib
bash github-repo-setup/scripts/setup_repo.sh --visibility private --no-rulesets
```

## What It Does

1. **Creates the GitHub repo** from the current git directory
2. **Sets `main` as default branch** (renames if needed)
3. **Generates CI workflow** based on detected language:
   - **Rust**: fmt, clippy, test, build
   - **Python**: ruff lint, mypy, pytest
   - **Node.js**: lint, test, build
   - **Go**: vet, test, build
4. **Creates 4 branch protection rulesets**:
   - `main` — PR required, CI checks, linear history, no deletion/force-push
   - `pub/**` — PR required, CI checks, no deletion/force-push
   - `pvt/**` — no deletion/force-push (direct push allowed)
   - Branch naming — only `main`, `usr/<user>/<topic>`, `pvt/<topic>`, `pub/<topic>`

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r github-repo-setup/ ~/.config/devin/skills/github-repo-setup/

# Project-specific
cp -r github-repo-setup/ /path/to/project/.devin/skills/github-repo-setup/
```

Then invoke with `/github-repo-setup` in a session.
