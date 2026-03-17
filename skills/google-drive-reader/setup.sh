#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# google-drive-reader enrollment script
# Walks the user through every setup step interactively.
# ---------------------------------------------------------------------------

AUTH_DIR="$HOME/.auth"
CREDENTIALS_FILE="$AUTH_DIR/google-drive-credentials.json"
TOKEN_FILE="$AUTH_DIR/google-drive-token.json"
SKILL_SCRIPT="$(cd "$(dirname "$0")" && pwd)/scripts/read_drive_doc.py"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

bold()  { printf '\033[1m%s\033[0m' "$*"; }
green() { printf '\033[1;32m%s\033[0m' "$*"; }
yellow(){ printf '\033[1;33m%s\033[0m' "$*"; }
red()   { printf '\033[1;31m%s\033[0m' "$*"; }

step() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $(bold "Step $1") — $2"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

ok()   { echo "  $(green "✔") $*"; }
warn() { echo "  $(yellow "!") $*"; }
fail() { echo "  $(red "✘") $*"; }

pause() {
    echo ""
    read -r -p "  Press Enter when ready to continue… "
}

ask_yes_no() {
    local prompt="$1" default="${2:-y}"
    while true; do
        if [[ "$default" == "y" ]]; then
            read -r -p "  $prompt [Y/n] " answer
            answer="${answer:-y}"
        else
            read -r -p "  $prompt [y/N] " answer
            answer="${answer:-n}"
        fi
        case "$answer" in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
        esac
    done
}

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

clear 2>/dev/null || true
echo ""
echo "  ┌──────────────────────────────────────────────────┐"
echo "  │                                                  │"
echo "  │   $(bold "Google Drive Reader") — Setup Wizard            │"
echo "  │                                                  │"
echo "  │   This will walk you through connecting your     │"
echo "  │   personal Google Drive (read-only) so the       │"
echo "  │   skill can read your Google Docs.               │"
echo "  │                                                  │"
echo "  │   Estimated time: 3–5 minutes                    │"
echo "  │                                                  │"
echo "  └──────────────────────────────────────────────────┘"
echo ""

# ---------------------------------------------------------------------------
# Step 0 — Prerequisites
# ---------------------------------------------------------------------------

step "0" "Checking prerequisites"

# Check uv
if command -v uv &>/dev/null; then
    ok "uv is installed ($(uv --version 2>/dev/null || echo 'unknown version'))"
else
    fail "uv is not installed."
    echo ""
    echo "    Install it with:  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "    Or:               brew install uv"
    echo ""
    echo "    After installing, re-run this script."
    exit 1
fi

# Check script exists
if [[ -f "$SKILL_SCRIPT" ]]; then
    ok "Skill script found at $SKILL_SCRIPT"
else
    fail "Skill script not found at $SKILL_SCRIPT"
    echo "    Make sure you're running this from the google-drive-reader directory."
    exit 1
fi

# Check for existing setup
if [[ -f "$TOKEN_FILE" ]]; then
    echo ""
    warn "An existing token was found at $TOKEN_FILE"
    if ask_yes_no "Do you want to start fresh? (This will delete the existing token)" "n"; then
        rm -f "$TOKEN_FILE"
        ok "Token deleted."
    else
        echo ""
        echo "  Skipping to validation…"
        # Jump to validation
        SKIP_TO_VALIDATE=true
    fi
fi

# ---------------------------------------------------------------------------
# Step 1 — Google Cloud project & Drive API
# ---------------------------------------------------------------------------

if [[ "${SKIP_TO_VALIDATE:-}" != "true" ]]; then

step "1" "Create a Google Cloud project & enable the Drive API"

echo "  You need a Google Cloud project with the Drive API enabled."
echo ""
echo "  $(bold "If you already have one, skip ahead.")"
echo ""
echo "  Otherwise, follow these steps:"
echo ""
echo "    1. Open $(bold "https://console.cloud.google.com/")"
echo "    2. Click the project dropdown at the top → $(bold "New Project")"
echo "    3. Name it anything (e.g. \"drive-reader\") → Create"
echo "    4. Go to $(bold "APIs & Services > Library")"
echo "    5. Search for $(bold "Google Drive API") → click $(bold "Enable")"
echo ""
echo "  $(yellow "Common mistake:") Forgetting to enable the API causes a"
echo "  \"403: Google Drive API has not been used\" error later."

pause

# ---------------------------------------------------------------------------
# Step 2 — OAuth consent screen
# ---------------------------------------------------------------------------

step "2" "Configure the OAuth consent screen"

echo "  The consent screen is what you see when authorizing access."
echo ""
echo "    1. Go to $(bold "APIs & Services > OAuth consent screen")"
echo "    2. Choose $(bold "External") user type → Create"
echo "    3. Fill in:"
echo "       • App name — anything (e.g. \"drive-reader\")"
echo "       • User support email — your email"
echo "       • Developer contact — your email"
echo "    4. Click $(bold "Save and Continue") through Scopes and Summary"
echo ""
echo "  $(bold "Important:") The app starts in $(yellow "Testing") mode."
echo "  Only listed test users can authorize."
echo ""
echo "    5. Go to $(bold "OAuth consent screen > Test users")"
echo "    6. Click $(bold "Add users") → enter the Gmail you'll authorize with"
echo ""
echo "  $(yellow "Common mistake:") Skipping this causes"
echo "  \"403: access_denied — app has not completed verification\" later."
echo ""
echo "  $(bold "Tip:") For personal use, you can click $(bold "Publish App") instead"
echo "  to skip the test-user requirement entirely."

pause

# ---------------------------------------------------------------------------
# Step 3 — Create OAuth credentials & download JSON
# ---------------------------------------------------------------------------

step "3" "Create OAuth credentials"

echo "  Now create the credentials this script will use to authenticate."
echo ""
echo "    1. Go to $(bold "APIs & Services > Credentials")"
echo "    2. Click $(bold "Create Credentials > OAuth client ID")"
echo "    3. Application type: $(bold "Desktop app")"
echo "    4. Name it anything → click $(bold "Create")"
echo "    5. Click $(bold "Download JSON")"
echo ""
echo "  $(yellow "Common mistake:") Choosing \"Web application\" instead of"
echo "  \"Desktop app\" causes a redirect_uri_mismatch error later."

pause

# ---------------------------------------------------------------------------
# Step 4 — Place the credentials file
# ---------------------------------------------------------------------------

step "4" "Place the credentials file"

mkdir -p "$AUTH_DIR"

if [[ -f "$CREDENTIALS_FILE" ]]; then
    ok "Credentials file already exists at $CREDENTIALS_FILE"
    if ask_yes_no "Replace it with a new one?" "n"; then
        rm -f "$CREDENTIALS_FILE"
    else
        echo "  Keeping existing credentials."
    fi
fi

if [[ ! -f "$CREDENTIALS_FILE" ]]; then
    echo "  Enter the full path to the JSON file you just downloaded."
    echo "  (Tip: drag the file into the terminal to paste its path)"
    echo ""

    while true; do
        read -r -p "  Path to credentials JSON: " input_path

        # Expand ~ and trim whitespace/quotes
        input_path="${input_path//\"/}"
        input_path="${input_path//\'/}"
        input_path="${input_path/#\~/$HOME}"

        if [[ -f "$input_path" ]]; then
            # Validate it looks like a Google credentials file
            if grep -q "client_id" "$input_path" 2>/dev/null; then
                cp "$input_path" "$CREDENTIALS_FILE"
                ok "Credentials saved to $CREDENTIALS_FILE"
                break
            else
                fail "That file doesn't look like a Google OAuth credentials JSON."
                echo "    It should contain \"client_id\" and \"client_secret\" fields."
            fi
        else
            fail "File not found: $input_path"
            echo "    Please check the path and try again."
        fi
    done
fi

# ---------------------------------------------------------------------------
# Step 5 — Set environment variable
# ---------------------------------------------------------------------------

step "5" "Set environment variables"

export GOOGLE_DRIVE_CREDENTIALS_FILE="$CREDENTIALS_FILE"
export GOOGLE_DRIVE_TOKEN_FILE="$TOKEN_FILE"
ok "GOOGLE_DRIVE_CREDENTIALS_FILE set for this session."
ok "GOOGLE_DRIVE_TOKEN_FILE set for this session."

# Write a sourceable env file into ~/.auth/ so the variables persist.
# Shells that source ~/.auth/* on startup (skipping .json) will pick these up.
ENV_FILE="$AUTH_DIR/google-drive"
{
    echo "export GOOGLE_DRIVE_CREDENTIALS_FILE=\"$CREDENTIALS_FILE\""
    echo "export GOOGLE_DRIVE_TOKEN_FILE=\"$TOKEN_FILE\""
} > "$ENV_FILE"
ok "Env file written to $ENV_FILE"

# Also offer to add a sourcing block to the shell profile if not already there.
SHELL_NAME="$(basename "${SHELL:-/bin/bash}")"
case "$SHELL_NAME" in
    zsh)  PROFILE="$HOME/.zshrc" ;;
    bash) PROFILE="$HOME/.bashrc" ;;
    fish) PROFILE="$HOME/.config/fish/config.fish" ;;
    *)    PROFILE="$HOME/.profile" ;;
esac

if grep -q '\.auth' "$PROFILE" 2>/dev/null; then
    ok "Shell profile already sources ~/.auth/ files."
else
    echo ""
    echo "  To auto-load env vars on shell startup, add this to $(bold "$PROFILE"):"
    echo ""
    echo '    # Source credential env files (skip .json and other data files)'
    echo '    if [ -d "$HOME/.auth" ]; then'
    echo '        for f in "$HOME/.auth"/*; do'
    echo '            case "$f" in *.json) continue ;; esac'
    echo '            [ -f "$f" ] && . "$f" 2>/dev/null'
    echo '        done'
    echo '    fi'
    echo ""
    if ask_yes_no "Add this block to $PROFILE now?"; then
        {
            echo ""
            echo '# Source credential env files (skip .json and other data files)'
            echo 'if [ -d "$HOME/.auth" ]; then'
            echo '    for f in "$HOME/.auth"/*; do'
            echo '        case "$f" in *.json) continue ;; esac'
            echo '        [ -f "$f" ] && . "$f" 2>/dev/null'
            echo '    done'
            echo 'fi'
        } >> "$PROFILE"
        ok "Added to $PROFILE"
        echo "    Run $(bold "source $PROFILE") or open a new terminal to pick it up."
    else
        warn "Skipped. Source $ENV_FILE manually or add the block later."
    fi
fi

# ---------------------------------------------------------------------------
# Step 6 — Authenticate with Google
# ---------------------------------------------------------------------------

step "6" "Authenticate with Google"

echo "  Running the OAuth flow now. A URL will be printed below."
echo ""
echo "    1. Open the URL in any browser"
echo "    2. Sign in and grant read-only Drive access"
echo "    3. Your browser will redirect to a localhost page"
echo "    4. The page may show an error — $(bold "that's expected")"
echo "    5. Copy the $(bold "full URL") from the address bar"
echo "    6. Paste it back here when prompted"
echo ""

uv run "$SKILL_SCRIPT" --auth

if [[ -f "$TOKEN_FILE" ]]; then
    ok "Token saved to $TOKEN_FILE"
else
    fail "Token file not found. Authentication may have failed."
    echo "    Try running:  uv run $SKILL_SCRIPT --auth"
    exit 1
fi

fi  # end SKIP_TO_VALIDATE

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

step "✓" "Validating setup"

echo "  Testing connection to Google Drive…"
echo ""

VALIDATION_OUTPUT=$(GOOGLE_DRIVE_CREDENTIALS_FILE="$CREDENTIALS_FILE" GOOGLE_DRIVE_TOKEN_FILE="$TOKEN_FILE" uv run "$SKILL_SCRIPT" --list --max-results 3 2>&1) && STATUS=0 || STATUS=$?

if [[ $STATUS -eq 0 ]]; then
    ok "Successfully connected to Google Drive!"
    echo ""
    echo "  Here are your most recent documents:"
    echo ""
    echo "$VALIDATION_OUTPUT" | head -20 | sed 's/^/    /'
else
    fail "Connection failed:"
    echo ""
    echo "$VALIDATION_OUTPUT" | sed 's/^/    /'
    echo ""
    echo "  Check the troubleshooting section in README.md for help."
    exit 1
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  $(green "Setup complete!") You're ready to use google-drive-reader."
echo ""
echo "  $(bold "Quick start:")"
echo ""
echo "    # List your docs"
echo "    uv run $SKILL_SCRIPT --list"
echo ""
echo "    # Read a doc and extract URLs + conclusions"
echo "    uv run $SKILL_SCRIPT <doc-id-or-url>"
echo ""
echo "    # Search for a doc"
echo "    uv run $SKILL_SCRIPT --list --query \"meeting notes\""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
