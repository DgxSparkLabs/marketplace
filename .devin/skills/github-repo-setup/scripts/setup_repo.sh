#!/usr/bin/env bash
# github-repo-setup — Create a GitHub repo with CI, rulesets, and branch naming
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Defaults ─────────────────────────────────────────────────────────────────
VISIBILITY="public"
DESCRIPTION=""
SKIP_CI=false
SKIP_RULESETS=false
DRY_RUN=false

# ── Parse arguments ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --visibility) VISIBILITY="$2"; shift 2 ;;
        --description) DESCRIPTION="$2"; shift 2 ;;
        --no-ci) SKIP_CI=true; shift ;;
        --no-rulesets) SKIP_RULESETS=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --help|-h)
            echo "Usage: $(basename "$0") [options]"
            echo ""
            echo "Options:"
            echo "  --visibility <public|private>  Repo visibility (default: public)"
            echo "  --description \"<text>\"         Repo description"
            echo "  --no-ci                        Skip CI workflow generation"
            echo "  --no-rulesets                   Skip branch protection rulesets"
            echo "  --dry-run                      Show what would be done"
            echo "  --help                         Show this help"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# ── Preflight checks ────────────────────────────────────────────────────────
echo "=== GitHub Repo Setup ==="
echo ""

# Check gh
if ! command -v gh &>/dev/null; then
    echo "FAIL: gh CLI not found. Install from https://cli.github.com/"
    exit 1
fi

# Check gh auth
if ! gh auth status &>/dev/null; then
    echo "FAIL: gh is not authenticated. Run: gh auth login"
    exit 1
fi

GH_USER="$(gh api user --jq '.login' 2>/dev/null)"
echo "  GitHub user: $GH_USER"

# Check git repo
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "FAIL: Not inside a git repository."
    exit 1
fi

REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
echo "  Repository:  $REPO_NAME"
echo "  Visibility:  $VISIBILITY"
[[ -n "$DESCRIPTION" ]] && echo "  Description: $DESCRIPTION"

# Detect language
LANG_TYPE="unknown"
if [[ -f Cargo.toml ]]; then
    LANG_TYPE="rust"
elif [[ -f pyproject.toml ]] || [[ -f setup.py ]]; then
    LANG_TYPE="python"
elif [[ -f package.json ]]; then
    LANG_TYPE="nodejs"
elif [[ -f go.mod ]]; then
    LANG_TYPE="go"
fi
echo "  Language:    $LANG_TYPE"
echo ""

if [[ "$DRY_RUN" = true ]]; then
    echo "[dry-run] Would create $VISIBILITY repo: $GH_USER/$REPO_NAME"
    [[ "$SKIP_CI" = false ]] && echo "[dry-run] Would generate CI workflow for $LANG_TYPE"
    [[ "$SKIP_RULESETS" = false ]] && echo "[dry-run] Would create 4 branch rulesets"
    exit 0
fi

# ── Step 1: Create GitHub repo ───────────────────────────────────────────────
echo "[1/4] Creating GitHub repository..."

# Check if repo already exists
if gh repo view "$GH_USER/$REPO_NAME" &>/dev/null; then
    echo "  Repository $GH_USER/$REPO_NAME already exists."
    echo "  Adding remote and pushing..."
    git remote get-url origin &>/dev/null || git remote add origin "https://github.com/$GH_USER/$REPO_NAME.git"
else
    DESC_FLAG=""
    [[ -n "$DESCRIPTION" ]] && DESC_FLAG="--description=$DESCRIPTION"
    gh repo create "$REPO_NAME" "--$VISIBILITY" --source=. $DESC_FLAG --push
fi

# Ensure main is the default branch
CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    git branch -m "$CURRENT_BRANCH" main 2>/dev/null || true
    git push -u origin main 2>/dev/null || true
fi
gh repo edit --default-branch main 2>/dev/null || true

# Clean up old default branch if it was pushed
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    git push origin --delete "$CURRENT_BRANCH" 2>/dev/null || true
fi

echo "  OK: https://github.com/$GH_USER/$REPO_NAME"

# ── Step 2: Generate CI workflow ─────────────────────────────────────────────
if [[ "$SKIP_CI" = false ]]; then
    echo ""
    echo "[2/4] Generating CI workflow..."
    mkdir -p .github/workflows

    case "$LANG_TYPE" in
        rust)
            cat > .github/workflows/ci.yml << 'CIEOF'
name: CI

on:
  push:
    branches: [main, "pub/**"]
  pull_request:
    branches: [main, "pub/**"]

env:
  CARGO_TERM_COLOR: always
  RUSTFLAGS: "-D warnings"

jobs:
  fmt:
    name: Format check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt
      - run: cargo fmt --all -- --check

  clippy:
    name: Clippy lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
      - uses: Swatinem/rust-cache@v2
      - run: cargo clippy --all-targets --all-features -- -D warnings

  test:
    name: Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo test --workspace

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo build --workspace
CIEOF
            CI_CHECKS='[{"context":"Format check"},{"context":"Clippy lint"},{"context":"Tests"},{"context":"Build"}]'
            ;;
        python)
            cat > .github/workflows/ci.yml << 'CIEOF'
name: CI

on:
  push:
    branches: [main, "pub/**"]
  pull_request:
    branches: [main, "pub/**"]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .

  typecheck:
    name: Type check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --dev
      - run: uv run mypy .

  test:
    name: Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --dev
      - run: uv run pytest
CIEOF
            CI_CHECKS='[{"context":"Lint"},{"context":"Type check"},{"context":"Tests"}]'
            ;;
        nodejs)
            cat > .github/workflows/ci.yml << 'CIEOF'
name: CI

on:
  push:
    branches: [main, "pub/**"]
  pull_request:
    branches: [main, "pub/**"]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    name: Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          cache: 'npm'
      - run: npm ci
      - run: npm test

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
CIEOF
            CI_CHECKS='[{"context":"Lint"},{"context":"Tests"},{"context":"Build"}]'
            ;;
        go)
            cat > .github/workflows/ci.yml << 'CIEOF'
name: CI

on:
  push:
    branches: [main, "pub/**"]
  pull_request:
    branches: [main, "pub/**"]

jobs:
  vet:
    name: Vet
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: 'stable'
      - run: go vet ./...

  test:
    name: Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: 'stable'
      - run: go test ./...

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: 'stable'
      - run: go build ./...
CIEOF
            CI_CHECKS='[{"context":"Vet"},{"context":"Tests"},{"context":"Build"}]'
            ;;
        *)
            echo "  SKIP: Unknown language. Create .github/workflows/ci.yml manually."
            SKIP_CI=true
            CI_CHECKS='[]'
            ;;
    esac

    if [[ "$SKIP_CI" = false ]]; then
        git add .github/workflows/ci.yml
        git commit -m "Add CI workflow" 2>/dev/null || true
        git push origin main 2>/dev/null || true
        echo "  OK: CI workflow created for $LANG_TYPE"
    fi
else
    echo ""
    echo "[2/4] Skipping CI generation (--no-ci)"
    CI_CHECKS='[]'
fi

# ── Step 3: Create branch protection rulesets ────────────────────────────────
if [[ "$SKIP_RULESETS" = false ]]; then
    echo ""
    echo "[3/4] Creating branch protection rulesets..."

    # Build status checks array for rulesets
    STATUS_CHECKS_JSON="$CI_CHECKS"

    # Ruleset 1: Protect main
    echo "  Creating: Protect main..."
    gh api "repos/$GH_USER/$REPO_NAME/rulesets" --method POST --silent --input - <<EOF
{
  "name": "Protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
  "rules": [
    {"type": "pull_request", "parameters": {"required_approving_review_count": 0, "dismiss_stale_reviews_on_push": true, "require_code_owner_review": false, "require_last_push_approval": false, "required_review_thread_resolution": false}},
    {"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": true, "required_status_checks": $STATUS_CHECKS_JSON}},
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "required_linear_history"}
  ],
  "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
}
EOF
    echo "    PR required, CI checks, linear history, no delete/force-push"

    # Ruleset 2: Protect pub branches
    echo "  Creating: Protect pub branches..."
    gh api "repos/$GH_USER/$REPO_NAME/rulesets" --method POST --silent --input - <<EOF
{
  "name": "Protect pub branches",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/heads/pub/**"], "exclude": []}},
  "rules": [
    {"type": "pull_request", "parameters": {"required_approving_review_count": 0, "dismiss_stale_reviews_on_push": true, "require_code_owner_review": false, "require_last_push_approval": false, "required_review_thread_resolution": false}},
    {"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": true, "required_status_checks": $STATUS_CHECKS_JSON}},
    {"type": "deletion"},
    {"type": "non_fast_forward"}
  ],
  "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
}
EOF
    echo "    PR required, CI checks, no delete/force-push"

    # Ruleset 3: Protect pvt branches
    echo "  Creating: Protect pvt branches..."
    gh api "repos/$GH_USER/$REPO_NAME/rulesets" --method POST --silent --input - <<EOF
{
  "name": "Protect pvt branches",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/heads/pvt/**"], "exclude": []}},
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"}
  ],
  "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
}
EOF
    echo "    No delete/force-push (direct push allowed)"

    # Ruleset 4: Branch naming convention
    echo "  Creating: Branch naming convention..."
    gh api "repos/$GH_USER/$REPO_NAME/rulesets" --method POST --silent --input - <<EOF
{
  "name": "Branch naming convention",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~ALL"], "exclude": ["refs/heads/main", "refs/heads/usr/*", "refs/heads/usr/**/*", "refs/heads/pvt/*", "refs/heads/pvt/**/*", "refs/heads/pub/*", "refs/heads/pub/**/*"]}},
  "rules": [{"type": "creation"}],
  "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
}
EOF
    echo "    Only main, usr/<user>/<topic>, pvt/<topic>, pub/<topic> allowed"

    echo "  OK: 4 rulesets created"
else
    echo ""
    echo "[3/4] Skipping rulesets (--no-rulesets)"
fi

# ── Step 4: Summary ──────────────────────────────────────────────────────────
echo ""
echo "[4/4] Done!"
echo ""
echo "  Repository: https://github.com/$GH_USER/$REPO_NAME"
echo "  Visibility: $VISIBILITY"
echo "  CI:         $([[ "$SKIP_CI" = false ]] && echo "$LANG_TYPE" || echo "skipped")"
echo "  Rulesets:   $([[ "$SKIP_RULESETS" = false ]] && echo "4 active" || echo "skipped")"
echo ""
echo "  Verify CI:      gh run list --limit 1"
echo "  Verify rules:   gh api repos/$GH_USER/$REPO_NAME/rulesets --jq '.[].name'"
