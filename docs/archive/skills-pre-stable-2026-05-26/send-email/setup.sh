#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# send-email setup script
# Configures the Resend API key for sending emails.
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
echo "$(bold "send-email setup")"
echo ""

# ---------------------------------------------------------------------------
# 2. Check for existing key
# ---------------------------------------------------------------------------
NEED_KEY=true

if [[ -n "${RESEND_API_KEY:-}" ]]; then
    MASKED="${RESEND_API_KEY:0:6}…"
    ok "RESEND_API_KEY is already set ($MASKED)"
    echo ""
    read -r -p "  Reconfigure? [y/N] " answer
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
    echo "  To send emails you need a Resend API key."
    echo ""
    echo "    1. Sign up at $(bold "https://resend.com")"
    echo "    2. Create an API key at $(bold "https://resend.com/api-keys")"
    echo ""

    read -r -p "  Paste your Resend API key: " api_key

    if [[ -z "$api_key" ]]; then
        fail "No key provided."
        exit 1
    fi

    echo ""
    echo "  Validating key..."

    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $api_key" \
        "https://api.resend.com/api-keys")

    if [[ "$HTTP_CODE" == "200" ]]; then
        ok "API key is valid."
    else
        fail "Invalid API key (HTTP $HTTP_CODE)."
        echo "    Double-check the key at https://resend.com/api-keys and try again."
        exit 1
    fi

    RESEND_API_KEY="$api_key"

    # -----------------------------------------------------------------------
    # 4. Save to shell profile
    # -----------------------------------------------------------------------
    echo ""
    EXPORT_LINE="export RESEND_API_KEY=\"$RESEND_API_KEY\""

    # Detect shell profile
    if [[ -f "$HOME/.zshrc" ]]; then
        PROFILE="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        PROFILE="$HOME/.bashrc"
    elif [[ -f "$HOME/.bash_profile" ]]; then
        PROFILE="$HOME/.bash_profile"
    elif [[ -f "$HOME/.profile" ]]; then
        PROFILE="$HOME/.profile"
    else
        PROFILE="$HOME/.profile"
    fi

    read -r -p "  Save to $(bold "$PROFILE")? [Y/n] " save_answer
    case "${save_answer:-y}" in
        [Nn]*)
            warn "Skipped. Export the key manually:"
            echo "    $EXPORT_LINE"
            ;;
        *)
            # Remove any existing RESEND_API_KEY line to avoid duplicates
            if grep -q 'export RESEND_API_KEY=' "$PROFILE" 2>/dev/null; then
                sed -i '/^export RESEND_API_KEY=/d' "$PROFILE"
            fi
            echo "" >> "$PROFILE"
            echo "$EXPORT_LINE" >> "$PROFILE"
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
echo "    uv run send-email/scripts/send_email.py --check"
echo "    uv run send-email/scripts/send_email.py --to \"you@example.com\" --subject \"Test\" --body \"Hello!\""
echo ""
