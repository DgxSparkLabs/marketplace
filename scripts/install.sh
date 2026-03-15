#!/usr/bin/env bash
set -euo pipefail

# Bootstrap installer for the Skills Marketplace.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/ForkYoraiLevi/marketplace/main/scripts/install.sh | bash
#   wget -qO- https://raw.githubusercontent.com/ForkYoraiLevi/marketplace/main/scripts/install.sh | bash
#
# What it does:
#   1. Installs uv (if not already installed)
#   2. Clones the marketplace repo to a temp directory
#   3. Runs the interactive TUI installer
#   4. Cleans up the temp directory
#
# Pass arguments through to install.py:
#   curl ... | bash -s -- --uninstall
#   curl ... | bash -s -- --project

REPO="https://github.com/ForkYoraiLevi/marketplace.git"
BRANCH="main"

# ── Helpers ──────────────────────────────────────────────────────────────────

info()  { printf '\033[1;36m%s\033[0m\n' "$*"; }
error() { printf '\033[1;31mError: %s\033[0m\n' "$*" >&2; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

cleanup() {
    if [[ -n "${TMPDIR_CREATED:-}" && -d "${TMPDIR_CREATED}" ]]; then
        rm -rf "$TMPDIR_CREATED"
    fi
}
trap cleanup EXIT

# ── Install uv if missing ───────────────────────────────────────────────────

ensure_uv() {
    if command_exists uv; then
        return
    fi
    info "Installing uv..."
    if command_exists curl; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command_exists wget; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        error "Neither curl nor wget found. Install uv manually: https://docs.astral.sh/uv/"
        exit 1
    fi
    # Add uv to PATH for this session
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    if ! command_exists uv; then
        error "uv installed but not found in PATH. Restart your shell and try again."
        exit 1
    fi
}

# ── Clone marketplace ────────────────────────────────────────────────────────

clone_marketplace() {
    if ! command_exists git; then
        error "git is required. Install git and try again."
        exit 1
    fi
    TMPDIR_CREATED="$(mktemp -d)"
    info "Cloning marketplace to $TMPDIR_CREATED..."
    git clone --depth 1 --branch "$BRANCH" "$REPO" "$TMPDIR_CREATED/marketplace" 2>&1 | tail -1
    echo "$TMPDIR_CREATED/marketplace"
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
    info "Skills Marketplace Installer"
    echo ""

    ensure_uv

    local marketplace_dir
    marketplace_dir="$(clone_marketplace)"

    info "Launching interactive installer..."
    echo ""
    uv run "$marketplace_dir/install.py" "$@"
}

main "$@"
