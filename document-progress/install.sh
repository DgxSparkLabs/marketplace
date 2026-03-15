#!/usr/bin/env bash
set -euo pipefail

# Install document-progress rule for AI agent tools.
# Supports: AGENTS.md, Windsurf, Cursor
#
# Usage:
#   ./install.sh                  # Install into current project
#   ./install.sh --global         # Install globally (all projects)
#   ./install.sh --format agents  # Install only AGENTS.md format
#
# Formats: agents (default), windsurf, cursor, all

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULE_FILE="$SCRIPT_DIR/rule.md"
FORMATS_DIR="$SCRIPT_DIR/formats"

SCOPE="project"
FORMAT="agents"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --global|-g) SCOPE="global"; shift ;;
        --format|-f)
            [[ $# -lt 2 ]] && echo "Error: --format requires a value (agents|windsurf|cursor|all)" && exit 1
            FORMAT="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: ./install.sh [--global] [--format agents|windsurf|cursor|all]"
            echo ""
            echo "Options:"
            echo "  --global, -g     Install globally (all projects)"
            echo "  --format, -f     Install for a specific tool (default: agents)"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

case "$FORMAT" in
    all|agents|windsurf|cursor) ;;
    *) echo "Unknown format: $FORMAT. Valid formats: agents, windsurf, cursor, all"; exit 1 ;;
esac

install_agents() {
    local target="$1"
    if [[ -f "$target" ]]; then
        if grep -q "Document Progress" "$target" 2>/dev/null; then
            echo "  AGENTS.md: already contains document-progress rule, skipping"
            return
        fi
        echo "" >> "$target"
        cat "$RULE_FILE" >> "$target"
        echo "  AGENTS.md: appended rule to $target"
    else
        mkdir -p "$(dirname "$target")"
        cp "$RULE_FILE" "$target"
        echo "  AGENTS.md: created $target"
    fi
}

install_windsurf() {
    local dir="$1"
    mkdir -p "$dir"
    cp "$FORMATS_DIR/windsurf.md" "$dir/document-progress.md"
    echo "  Windsurf: installed to $dir/document-progress.md"
}

install_cursor() {
    local dir="$1"
    mkdir -p "$dir"
    cp "$FORMATS_DIR/cursor.md" "$dir/document-progress.md"
    echo "  Cursor: installed to $dir/document-progress.md"
}

echo "Installing document-progress rule ($SCOPE, format: $FORMAT)"
echo ""

if [[ "$SCOPE" == "global" ]]; then
    if [[ "$FORMAT" == "all" || "$FORMAT" == "agents" ]]; then
        install_agents "$HOME/.config/cognition/AGENTS.md"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "windsurf" ]]; then
        install_windsurf "$HOME/.windsurf/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "cursor" ]]; then
        install_cursor "$HOME/.cursor/rules"
    fi
else
    if [[ "$FORMAT" == "all" || "$FORMAT" == "agents" ]]; then
        install_agents "AGENTS.md"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "windsurf" ]]; then
        install_windsurf ".windsurf/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "cursor" ]]; then
        install_cursor ".cursor/rules"
    fi
fi

echo ""
echo "Done. The document-progress rule is now active."
