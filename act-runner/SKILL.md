---
name: act-runner
description: Run GitHub Actions workflows locally with act and podman
argument-hint: "[workflow] [options]"
allowed-tools:
  - exec
  - read
  - glob
  - grep
permissions:
  allow:
    - Exec(bash)
    - Exec(act)
    - Exec(podman)
    - Exec(curl)
triggers:
  - user
  - model
---

# Act Runner

Run GitHub Actions workflows locally using [act](https://github.com/nektos/act) with podman as the container runtime. No Docker daemon required.

## Prerequisites

- **podman** must be installed and its socket reachable (user or system). If the socket isn't running, the script starts it automatically.
- **act** is downloaded automatically if not found on PATH.

No API keys or environment variables are required.

## Usage

```
bash act-runner/scripts/act-runner.sh [command] [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `run [workflow] [act-flags...]` | Run a workflow (default: all workflows in `.github/workflows/`) |
| `dry-run [workflow]` | Dry-run a workflow (no containers, just validate) |
| `list [workflow]` | List jobs in a workflow without running |
| `setup` | Install act and verify podman — no workflow execution |

### Options

All extra flags after the command are passed directly to `act`. Common ones:

| Flag | Description |
|------|-------------|
| `-j JOB` | Run only a specific job |
| `-W PATH` | Path to workflow file or directory |
| `--verbose` | Show detailed act output |
| `--env NAME=VAL` | Pass an environment variable into the runner |
| `--secret NAME=VAL` | Pass a secret into the runner |
| `--matrix KEY:VAL` | Limit matrix to specific values |

## Instructions

### Step 1: Find the workflow

Look for GitHub Actions workflows in the project:

```
find .github/workflows -name '*.yml' -o -name '*.yaml' 2>/dev/null
```

If no workflows exist, tell the user and offer to help create one.

### Step 2: Run it

```
bash act-runner/scripts/act-runner.sh run                              # all workflows
bash act-runner/scripts/act-runner.sh run .github/workflows/ci.yml     # specific workflow
bash act-runner/scripts/act-runner.sh run -j test                      # specific job
bash act-runner/scripts/act-runner.sh dry-run                          # validate only
bash act-runner/scripts/act-runner.sh list                             # show jobs
```

### Step 3: Interpret results

- If the run succeeds, report which jobs passed.
- If a job fails, read the output carefully and report the failing step and error.
- Common issues:
  - **Missing secrets**: use `--secret NAME=VAL` or `--secret-file .env`
  - **Image pull failures**: check internet connectivity and podman socket
  - **Action not supported by act**: some GitHub-specific actions (caching, OIDC) have limited support — note this to the user

### Error handling

- If podman is not installed, tell the user to install it: `sudo apt install podman` (Debian/Ubuntu) or `brew install podman` (macOS).
- If a workflow references secrets the user hasn't provided, list exactly which secrets are needed.
- If act reports an unsupported action, suggest workarounds or skipping that step with `--action-offline-mode`.

User arguments: $ARGUMENTS
