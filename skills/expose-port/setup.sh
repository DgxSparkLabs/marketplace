#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# expose-port setup script
# Installs the bore client binary and configures ~/.auth/bore.
# localhost.run requires no setup (just ssh).
# ---------------------------------------------------------------------------

AUTH_DIR="$HOME/.auth"
AUTH_FILE="$AUTH_DIR/bore"
BORE_VERSION="0.6.0"

bold()  { printf '\033[1m%s\033[0m' "$*"; }
green() { printf '\033[1;32m%s\033[0m' "$*"; }
yellow(){ printf '\033[1;33m%s\033[0m' "$*"; }
red()   { printf '\033[1;31m%s\033[0m' "$*"; }

ok()   { echo "  $(green "✔") $*"; }
warn() { echo "  $(yellow "!") $*"; }
fail() { echo "  $(red "✘") $*"; }

# ---------------------------------------------------------------------------
# 1. Check / install bore binary
# ---------------------------------------------------------------------------
echo ""
echo "$(bold "expose-port setup")"
echo ""

if command -v bore &>/dev/null; then
    ok "bore already installed: $(bore --version 2>&1)"
else
    echo "  Installing bore v${BORE_VERSION}..."

    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64)  BORE_ARCH="x86_64-unknown-linux-musl" ;;
        aarch64) BORE_ARCH="aarch64-unknown-linux-musl" ;;
        *)
            fail "Unsupported architecture: $ARCH"
            echo "  Install bore manually: https://github.com/ekzhang/bore#installation"
            exit 1
            ;;
    esac

    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"

    if curl -fsSL "https://github.com/ekzhang/bore/releases/download/v${BORE_VERSION}/bore-v${BORE_VERSION}-${BORE_ARCH}.tar.gz" \
        | tar xz -C "$INSTALL_DIR" bore; then
        chmod +x "$INSTALL_DIR/bore"
        ok "Installed bore to $INSTALL_DIR/bore"

        # Make sure ~/.local/bin is on PATH
        if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
            warn "$INSTALL_DIR is not on your PATH"
            echo "  Add to your ~/.bashrc:  export PATH=\"\$HOME/.local/bin:\$PATH\""
        fi
    else
        fail "Failed to download bore"
        echo "  Install manually: https://github.com/ekzhang/bore#installation"
        exit 1
    fi
fi

# ---------------------------------------------------------------------------
# 2. Check ssh (needed for localhost.run)
# ---------------------------------------------------------------------------
if command -v ssh &>/dev/null; then
    ok "ssh available (for localhost.run backend)"
else
    warn "ssh not found — localhost.run backend won't work"
fi

# ---------------------------------------------------------------------------
# 3. Configure bore server (optional)
# ---------------------------------------------------------------------------
echo ""
echo "  $(bold "Bore server configuration") (optional)"
echo "  If you have a bore server, enter its address below."
echo "  This lets you run 'expose-port start PORT' without --bore flags."
echo "  Press Enter to skip."
echo ""

read -r -p "  Bore server address (IP or hostname): " bore_server

if [[ -n "$bore_server" ]]; then
    read -r -p "  Bore secret (leave empty for none): " bore_secret

    mkdir -p "$AUTH_DIR"
    {
        echo "export BORE_SERVER=\"$bore_server\""
        if [[ -n "$bore_secret" ]]; then
            echo "export BORE_SECRET=\"$bore_secret\""
        fi
    } > "$AUTH_FILE"

    ok "Saved to $AUTH_FILE"

    # Check if bashrc sources it
    if grep -q '\.auth/bore' "$HOME/.bashrc" 2>/dev/null; then
        ok "~/.bashrc already sources $AUTH_FILE"
    else
        echo "" >> "$HOME/.bashrc"
        echo "[ -f ~/.auth/bore ] && source ~/.auth/bore" >> "$HOME/.bashrc"
        ok "Added source line to ~/.bashrc"
    fi
else
    echo ""
    ok "Skipped — you can configure later by creating $AUTH_FILE:"
    echo "      export BORE_SERVER=\"your-server-ip\""
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "$(bold "Setup complete.")"
echo ""
echo "  Usage:"
echo "    expose-port start 8080                   # localhost.run (HTTPS)"
if [[ -n "${bore_server:-}" ]]; then
    echo "    expose-port start 8080                   # bore (auto, from config)"
fi
echo "    expose-port start 8080 --bore SERVER     # bore (explicit server)"
echo "    expose-port list                         # show active tunnels"
echo "    expose-port stop all                     # stop all tunnels"
echo ""
echo "  Bore server setup guide: docs/bore-server-setup.md"
echo ""
