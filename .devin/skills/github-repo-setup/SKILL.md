---
name: github-repo-setup
description: Create a GitHub repo with CI, branch protection, and naming rules
argument-hint: "[visibility] [description]"
allowed-tools:
  - exec
  - Bash
  - read
  - Read
  - edit
  - Edit
  - glob
  - Glob
  - grep
  - Grep
permissions:
  allow:
    - Exec(gh)
    - Exec(git)
    - Exec(bash)
    - Exec(uv run)
triggers:
  - user
---

# GitHub Repo Setup

Create a GitHub repository from a local git repo and configure it with CI workflows, branch protection rulesets, and branch naming conventions — all via the `gh` CLI.

## Prerequisites

- **gh** must be installed and authenticated (`gh auth status` should succeed)
- **git** repo must exist in the current directory with at least one commit
- Required `gh` token scopes: `repo`, `workflow`

If `gh` is not authenticated, tell the user:
```
gh auth login
```

## What It Configures

1. **GitHub repository** — creates from local git, sets `main` as default branch
2. **CI workflow** — detects project language and generates `.github/workflows/ci.yml`
3. **CD workflow** — auto-tags releases on push to main after CI passes (`.github/workflows/cd.yml`)
4. **Branch protection rulesets** via GitHub API:
   - `main` — PR required, CI status checks, no deletion, no force push, linear history
   - `pub/**` — PR required, CI status checks, no deletion, no force push
   - `pvt/**` — no deletion, no force push (direct push allowed)
5. **Branch naming convention** — only allows: `main`, `usr/<user>/<topic>`, `pvt/<topic>`, `pub/<topic>`

## Usage

```
bash $SKILL_DIR/scripts/setup_repo.sh [options]
```

### Options

- `--visibility <public|private>` — repo visibility (default: public)
- `--description "<text>"` — repo description
- `--no-ci` — skip CI workflow generation (just create repo + rulesets)
- `--no-rulesets` — skip branch protection rulesets
- `--dry-run` — show what would be done without making changes

## Instructions

### Step 1: Verify prerequisites

Run the script with no arguments to check prerequisites:
```
bash $SKILL_DIR/scripts/setup_repo.sh --dry-run
```

### Step 2: Detect project type and plan CI

Before running, examine the project to determine the language and build system:
- **Rust** (Cargo.toml): fmt, clippy, test, build
- **Python** (pyproject.toml / setup.py): ruff, mypy, pytest
- **Node.js** (package.json): lint, typecheck, test, build
- **Go** (go.mod): vet, staticcheck, test, build

If the project has an existing Makefile with quality targets, prefer those commands.

If the project does not have a Makefile, generate one with these conventions:
- `.DEFAULT_GOAL := help` — bare `make` shows help
- `help` target that dynamically lists all targets with descriptions
- Each target uses `## description` after the colon for self-documenting help
- Pattern: `target: deps ## Short description`

Example Makefile template:
```makefile
.PHONY: help install lint format test check clean

.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	...

lint: ## Run linter
	...

test: ## Run tests
	...

check: lint test ## Run all quality checks
	...

clean: ## Remove build artifacts
	...
```

### Step 3: Run the setup

```
bash $SKILL_DIR/scripts/setup_repo.sh --visibility public --description "Project description"
```

### Step 4: Verify

After setup, verify:
1. The repo exists on GitHub: `gh repo view`
2. CI passes: `gh run list --limit 1`
3. Rulesets are active: `gh api repos/{owner}/{repo}/rulesets`

### Step 5: Report

Tell the user:
- Repository URL
- CI jobs configured and their status
- Rulesets created and what they enforce
- Branch naming rules

## Language-Specific CI Templates

The script generates CI based on detected language. If the project uses a language not listed, ask the user what CI steps to include.

### Rust
Jobs: `fmt` (cargo fmt --check), `clippy` (cargo clippy -D warnings), `test` (cargo test), `build` (cargo build)

### Python (uv)
Jobs: `lint` (ruff check + ruff format --check), `typecheck` (mypy), `test` (pytest)

### Node.js
Jobs: `lint` (npm run lint), `typecheck` (npm run typecheck), `test` (npm test), `build` (npm run build)

### Go
Jobs: `vet` (go vet), `lint` (staticcheck), `test` (go test), `build` (go build)

## Error Handling

- If the repo already exists on GitHub, ask the user whether to add a remote and push, or abort.
- If `gh` lacks required scopes, tell the user to re-authenticate: `gh auth refresh -s repo,workflow`
- If CI generation fails, still proceed with repo creation and rulesets.
- If a ruleset creation fails, report the error and continue with remaining rulesets.

## CD Workflow and Version Tagging

After generating the CI workflow, also generate a CD workflow (`.github/workflows/cd.yml`) that auto-tags releases on push to main.

### Version scheme

Tags follow date-based versioning with patch support:
- `vYYYY.MM.DD` — first release of the day
- `vYYYY.MM.DD-1`, `vYYYY.MM.DD-2` — same-day patches

### CD workflow behavior

The CD workflow triggers via `workflow_run` after CI completes on `main`:

1. **Gate on CI**: `if: github.event.workflow_run.conclusion == 'success'` — only proceeds if all CI checks passed
2. **Run e2e tests** (optional): additional integration/smoke tests beyond CI
3. **Auto-tag**: computes the next version tag for today and pushes it

```yaml
name: CD

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

permissions:
  contents: write

jobs:
  tag:
    if: github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Compute and push version tag
        run: |
          TODAY=$(date -u +%Y.%m.%d)
          EXISTING=$(git tag -l "v${TODAY}" "v${TODAY}-*" | sort -V)
          if [ -z "$EXISTING" ]; then
            TAG="v${TODAY}"
          else
            LAST=$(echo "$EXISTING" | tail -1)
            if [ "$LAST" = "v${TODAY}" ]; then
              TAG="v${TODAY}-1"
            else
              N=$(echo "$LAST" | sed "s/v${TODAY}-//")
              TAG="v${TODAY}-$((N + 1))"
            fi
          fi
          echo "Tagging: $TAG"
          git tag "$TAG"
          git push origin "$TAG"
```

### Makefile release target

When generating a Makefile, include a `release` target for manual tagging:

```makefile
release: ## Tag a release (vYYYY.MM.DD or vYYYY.MM.DD-N) and push
	@TODAY=$$(date -u +%Y.%m.%d); \
	EXISTING=$$(git tag -l "v$$TODAY" "v$$TODAY-*" | sort -V); \
	if [ -z "$$EXISTING" ]; then TAG="v$$TODAY"; \
	else LAST=$$(echo "$$EXISTING" | tail -1); \
		if [ "$$LAST" = "v$$TODAY" ]; then TAG="v$$TODAY-1"; \
		else N=$$(echo "$$LAST" | sed "s/v$$TODAY-//"); TAG="v$$TODAY-$$((N + 1))"; fi; \
	fi; \
	echo "Tagging: $$TAG"; git tag "$$TAG"; git push origin "$$TAG"
```

User arguments: $ARGUMENTS
