# act-runner

Run GitHub Actions workflows locally using [act](https://github.com/nektos/act) with podman as the container runtime. No Docker daemon required.

## Setup

1. Install podman (container runtime):
   ```bash
   # Debian/Ubuntu
   sudo apt install podman

   # macOS
   brew install podman
   podman machine init && podman machine start
   ```

2. Run the setup command to install act and verify everything:
   ```bash
   bash act-runner/scripts/act-runner.sh setup
   ```

   This downloads `act` automatically if not already installed.

## Usage

```bash
# Run all workflows in .github/workflows/
bash act-runner/scripts/act-runner.sh run

# Run a specific workflow
bash act-runner/scripts/act-runner.sh run ci.yml

# Run a specific job within a workflow
bash act-runner/scripts/act-runner.sh run ci.yml -j test

# Dry-run (validate without containers)
bash act-runner/scripts/act-runner.sh dry-run

# List jobs in workflows
bash act-runner/scripts/act-runner.sh list

# Pass secrets
bash act-runner/scripts/act-runner.sh run --secret GITHUB_TOKEN=ghp_xxx

# Pass environment variables
bash act-runner/scripts/act-runner.sh run --env NODE_ENV=test
```

### Commands

| Command | Description |
|---------|-------------|
| `run [workflow] [flags...]` | Run a workflow (default: all in `.github/workflows/`) |
| `dry-run [workflow]` | Dry-run without containers — validates the workflow |
| `list [workflow]` | List jobs in a workflow |
| `setup` | Install act and verify podman socket |

### Options

All extra flags are passed through to `act`. Common ones:

| Flag | Description |
|------|-------------|
| `-j JOB` | Run only a specific job |
| `-W PATH` | Override workflow file or directory path |
| `--verbose` | Show detailed act output |
| `--env NAME=VAL` | Pass an environment variable |
| `--secret NAME=VAL` | Pass a secret |
| `--secret-file PATH` | Load secrets from a file |
| `--matrix KEY:VAL` | Limit matrix to specific values |

### Examples

```bash
# Verify a project's CI passes before pushing
bash act-runner/scripts/act-runner.sh run

# Debug a failing workflow
bash act-runner/scripts/act-runner.sh run ci.yml --verbose

# Run only the lint job
bash act-runner/scripts/act-runner.sh run ci.yml -j lint

# Check what jobs exist
bash act-runner/scripts/act-runner.sh list

# Quick syntax validation
bash act-runner/scripts/act-runner.sh dry-run
```

## How it works

1. **act** is auto-installed to `~/.cache/act-runner/act` if not on PATH
2. **podman socket** is auto-detected (user socket, system socket, or macOS machine socket) — started automatically if needed
3. **actrc** is created at `~/.config/act/actrc` with a default image mapping (`ubuntu-latest` -> `catthehacker/ubuntu:act-latest`)
4. Workflows are resolved from `.github/workflows/` — you can pass a full path, a filename, or just a name without extension

## Limitations

- Some GitHub-specific features (OIDC, artifact caching, large runners) have limited support in act
- Paid/custom actions that require GitHub authentication may need a `GITHUB_TOKEN` secret
- macOS and Windows runner images are not available — only `ubuntu-latest`

## As an Agent Skill

Copy this directory into your agent's skills directory:

```bash
# Global (available everywhere)
cp -r act-runner/ ~/.config/devin/skills/act-runner/
# or: cp -r act-runner/ ~/.windsurf/skills/act-runner/

# Project-specific
cp -r act-runner/ /path/to/project/.devin/skills/act-runner/
# or: cp -r act-runner/ /path/to/project/.windsurf/skills/act-runner/
```

Then invoke with `/act-runner` in a session.
