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
#   2. Clones the marketplace repo to ~/.local/share/marketplace (persistent)
#   3. Runs the interactive TUI installer
#
# The clone is kept because installed skills are symlinked back to it.
#
# Pass arguments through to install.py:
#   curl ... | bash -s -- --uninstall

REPO="https://github.com/ForkYoraiLevi/marketplace.git"
BRANCH="main"
MARKETPLACE_DIR="${MARKETPLACE_HOME:-$HOME/.local/share/marketplace}"

# ── Helpers ──────────────────────────────────────────────────────────────────

info()  { printf '\033[1;36m%s\033[0m\n' "$*"; }
error() { printf '\033[1;31mError: %s\033[0m\n' "$*" >&2; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

# ── Install uv if missing ───────────────────────────────────────────────────

ensure_uv() {
    if command_exists uv; then
        return
    fi
    info "uv (Python package manager) is required but not installed."
    info "It will be installed from https://astral.sh/uv/install.sh"
    echo ""
    # When piped (curl | bash), stdin is the pipe — cannot prompt interactively.
    # Just inform the user and proceed.
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

# ── Clone or update marketplace ──────────────────────────────────────────────

ensure_marketplace() {
    if ! command_exists git; then
        error "git is required. Install git and try again."
        exit 1
    fi
    if [[ -d "$MARKETPLACE_DIR/.git" ]]; then
        info "Updating marketplace in $MARKETPLACE_DIR..."
        git -C "$MARKETPLACE_DIR" fetch --depth 1 origin "$BRANCH" 2>&1 | tail -1
        git -C "$MARKETPLACE_DIR" reset --hard "origin/$BRANCH" >/dev/null
    else
        info "Cloning marketplace to $MARKETPLACE_DIR..."
        mkdir -p "$(dirname "$MARKETPLACE_DIR")"
        git clone --depth 1 --branch "$BRANCH" "$REPO" "$MARKETPLACE_DIR" 2>&1 | tail -1
    fi
    echo "$MARKETPLACE_DIR"
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
    info "Skills Marketplace Installer"
    echo ""

    ensure_uv

    local marketplace_dir
    marketplace_dir="$(ensure_marketplace)"

    info "Launching interactive installer..."
    echo ""
    uv run "$marketplace_dir/install.py" "$@"
}

main "$@"
