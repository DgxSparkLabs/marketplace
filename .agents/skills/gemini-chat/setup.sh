#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# gemini-chat setup script
# Configures the GEMINI_API_KEY for the Google Gemini API.
# ---------------------------------------------------------------------------

bold()  { printf '\033[1m%s\033[0m' "$*"; }
green() { printf '\033[1;32m%s\033[0m' "$*"; }
yellow(){ printf '\033[1;33m%s\033[0m' "$*"; }
red()   { printf '\033[1;31m%s\033[0m' "$*"; }

ok()   { echo "  $(green "✔") $*"; }
warn() { echo "  $(yellow "!") $*"; }
fail() { echo "  $(red "✘") $*"; }

# ---------------------------------------------------------------------------
# 1. Header
# ---------------------------------------------------------------------------
echo ""
echo "$(bold "gemini-chat setup")"
echo ""

# ---------------------------------------------------------------------------
# 2. Check for existing GEMINI_API_KEY
# ---------------------------------------------------------------------------
NEED_KEY=true

if [[ -n "${GEMINI_API_KEY:-}" ]]; then
    masked="${GEMINI_API_KEY:0:6}…"
    ok "GEMINI_API_KEY is already set ($masked)"
    echo ""
    read -r -p "  Do you want to reconfigure? [y/N] " answer
    case "${answer:-n}" in
        [Yy]*) NEED_KEY=true ;;
        *)     NEED_KEY=false ;;
    esac
fi

# ---------------------------------------------------------------------------
# 3. Prompt for API key & validate
# ---------------------------------------------------------------------------
if [[ "$NEED_KEY" == "true" ]]; then
    echo ""
    echo "  Get a free Gemini API key at:"
    echo "    $(bold "https://aistudio.google.com/apikey")"
    echo ""

    read -r -p "  Paste your Gemini API key: " key

    if [[ -z "$key" ]]; then
        fail "No key provided."
        exit 1
    fi

    echo "  Validating key..."
    http_code=$(curl -s -o /dev/null -w "%{http_code}" \
        "https://generativelanguage.googleapis.com/v1beta/models?key=$key")

    if [[ "$http_code" == "200" ]]; then
        ok "API key is valid."
    else
        fail "API key validation failed (HTTP $http_code)."
        echo "    Please check your key and try again."
        exit 1
    fi

    export GEMINI_API_KEY="$key"

    # -------------------------------------------------------------------
    # 4. Offer to save to shell profile
    # -------------------------------------------------------------------
    echo ""
    echo "  $(bold "Save to shell profile")"
    echo "  This adds $(bold "export GEMINI_API_KEY=\"...\"") to your shell config"
    echo "  so the key is available in future sessions."
    echo ""

    # Detect shell profile
    if [[ -f "$HOME/.zshrc" ]]; then
        PROFILE="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        PROFILE="$HOME/.bashrc"
    elif [[ -f "$HOME/.bash_profile" ]]; then
        PROFILE="$HOME/.bash_profile"
    else
        PROFILE="$HOME/.profile"
    fi

    read -r -p "  Save to $PROFILE? [Y/n] " save_answer
    case "${save_answer:-y}" in
        [Nn]*)
            warn "Skipped — export the key manually before using the skill."
            ;;
        *)
            # Remove any existing GEMINI_API_KEY line to avoid duplicates
            if grep -q 'export GEMINI_API_KEY=' "$PROFILE" 2>/dev/null; then
                sed -i '/^export GEMINI_API_KEY=/d' "$PROFILE"
            fi
            echo "export GEMINI_API_KEY=\"$GEMINI_API_KEY\"" >> "$PROFILE"
            ok "Saved to $PROFILE"
            echo "    Run $(bold "source $PROFILE") or open a new terminal to pick it up."
            ;;
    esac
fi

# ---------------------------------------------------------------------------
# 5. Done
# ---------------------------------------------------------------------------
echo ""
echo "$(bold "Setup complete.")"
echo ""
echo "  Usage:"
echo "    uv run gemini-chat/scripts/chat.py --check          # verify setup"
echo "    uv run gemini-chat/scripts/chat.py -m \"Hello Gemini!\"  # single message"
echo "    uv run gemini-chat/scripts/chat.py                  # interactive mode"
echo ""
