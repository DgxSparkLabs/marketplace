#!/usr/bin/env bash
set -euo pipefail

# Install no-ai-credit rule for AI agent tools.
# Supports: AGENTS.md, Windsurf, Cursor, Claude Code
#
# Usage:
#   ./install.sh                  # Install into current project
#   ./install.sh --global         # Install globally (all projects)
#   ./install.sh --format agents  # Install only AGENTS.md format
#
# Formats: agents, windsurf, cursor, claude, all (default)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULE_FILE="$SCRIPT_DIR/rule.md"
FORMATS_DIR="$SCRIPT_DIR/formats"

SCOPE="project"
FORMAT="all"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --global|-g) SCOPE="global"; shift ;;
        --format|-f)
            [[ $# -lt 2 ]] && echo "Error: --format requires a value (agents|windsurf|cursor|claude|all)" && exit 1
            FORMAT="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: ./install.sh [--global] [--format agents|windsurf|cursor|claude|all]"
            echo ""
            echo "Options:"
            echo "  --global, -g     Install globally (all projects)"
            echo "  --format, -f     Install for a specific tool (default: all)"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

case "$FORMAT" in
    all|agents|windsurf|cursor|claude) ;;
    *) echo "Unknown format: $FORMAT. Valid formats: agents, windsurf, cursor, claude, all"; exit 1 ;;
esac

install_agents() {
    local target="$1"
    if [[ -f "$target" ]]; then
        if grep -q "No AI Credit" "$target" 2>/dev/null; then
            echo "  AGENTS.md: already contains no-ai-credit rule, skipping"
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
    cp "$FORMATS_DIR/windsurf.md" "$dir/no-ai-credit.md"
    echo "  Windsurf: installed to $dir/no-ai-credit.md"
}

install_cursor() {
    local dir="$1"
    mkdir -p "$dir"
    cp "$FORMATS_DIR/cursor.md" "$dir/no-ai-credit.md"
    echo "  Cursor: installed to $dir/no-ai-credit.md"
}

install_claude() {
    local target="$1"
    if [[ -f "$target" ]]; then
        if grep -q "No AI Credit" "$target" 2>/dev/null; then
            echo "  Claude: already contains no-ai-credit rule, skipping"
            return
        fi
        echo "" >> "$target"
        cat "$RULE_FILE" >> "$target"
        echo "  Claude: appended rule to $target"
    else
        mkdir -p "$(dirname "$target")"
        cp "$RULE_FILE" "$target"
        echo "  Claude: created $target"
    fi
}

echo "Installing no-ai-credit rule ($SCOPE, format: $FORMAT)"
echo ""

if [[ "$SCOPE" == "global" ]]; then
    # Global installs
    if [[ "$FORMAT" == "all" || "$FORMAT" == "agents" ]]; then
        install_agents "$HOME/.config/cognition/AGENTS.md"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "windsurf" ]]; then
        install_windsurf "$HOME/.windsurf/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "cursor" ]]; then
        install_cursor "$HOME/.cursor/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "claude" ]]; then
        install_claude "$HOME/.claude/CLAUDE.md"
    fi
else
    # Project installs (current directory)
    if [[ "$FORMAT" == "all" || "$FORMAT" == "agents" ]]; then
        install_agents "AGENTS.md"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "windsurf" ]]; then
        install_windsurf ".windsurf/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "cursor" ]]; then
        install_cursor ".cursor/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "claude" ]]; then
        install_claude "CLAUDE.md"
    fi
fi

echo ""
echo "Done. The no-ai-credit rule is now active."
