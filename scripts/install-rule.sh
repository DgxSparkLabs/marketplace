#!/usr/bin/env bash
set -euo pipefail

# Shared rule installer. Called by each rule's install.sh wrapper.
#
# Usage (from wrapper):
#   exec "$(dirname "$0")/../scripts/install-rule.sh" "$(dirname "$0")" "$@"
#
# Arguments:
#   $1          Path to the rule directory (contains rule.md, formats/)
#   Remaining   User flags: --global, --format <name>, --help

RULE_DIR="$(cd "$1" && pwd)"
shift

RULE_NAME="$(basename "$RULE_DIR")"
RULE_FILE="$RULE_DIR/rule.md"
FORMATS_DIR="$RULE_DIR/formats"

# Extract the rule title from the first ## heading in rule.md
RULE_TITLE="$(head -5 "$RULE_FILE" | grep -oP '(?<=^## ).*' | head -1)"

if [[ -z "$RULE_TITLE" ]]; then
    echo "Error: could not extract title from $RULE_FILE (expected '## Title' in first 5 lines)"
    exit 1
fi

SCOPE="project"
FORMAT="agents"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --global|-g) SCOPE="global"; shift ;;
        --format|-f)
            [[ $# -lt 2 ]] && echo "Error: --format requires a value (agents|windsurf|cursor|all)" && exit 1
            FORMAT="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: $RULE_NAME/install.sh [--global] [--format agents|windsurf|cursor|all]"
            echo ""
            echo "Options:"
            echo "  --global, -g     Install globally (all projects)"
            echo "  --format, -f     Install for a specific tool (default: agents)"
            echo ""
            echo "Formats:"
            echo "  agents           AGENTS.md (recommended, works with Devin CLI + Claude Code)"
            echo "  windsurf         .windsurf/rules/ (Windsurf only)"
            echo "  cursor           .cursor/rules/ (Cursor only)"
            echo "  all              All three — WARNING: causes duplicate rules if your tool"
            echo "                   reads from multiple locations (e.g. Devin reads AGENTS.md"
            echo "                   + .windsurf/ + .cursor/ by default)"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

case "$FORMAT" in
    all|agents|windsurf|cursor) ;;
    *) echo "Unknown format: $FORMAT. Valid formats: agents, windsurf, cursor, all"; exit 1 ;;
esac

if [[ "$FORMAT" == "all" ]]; then
    echo "Warning: --format all installs to AGENTS.md + Windsurf + Cursor."
    echo "If your agent reads from multiple sources, the rule will appear"
    echo "multiple times in context. Prefer --format agents (the default)"
    echo "unless you need rules in a specific tool's format."
    echo ""
fi

install_agents() {
    local target="$1"
    if [[ -f "$target" ]]; then
        if grep -qF "$RULE_TITLE" "$target" 2>/dev/null; then
            echo "  AGENTS.md: already contains $RULE_NAME rule, skipping"
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

install_format_file() {
    local label="$1" fmt="$2" dir="$3"
    local src="$FORMATS_DIR/$fmt.md"
    local dest="$dir/$RULE_NAME.md"
    mkdir -p "$dir"
    if [[ -f "$dest" ]] && diff -q "$src" "$dest" >/dev/null 2>&1; then
        echo "  $label: already up to date, skipping"
        return
    fi
    cp "$src" "$dest"
    echo "  $label: installed to $dest"
}

# Warn if rule is already installed in the other scope
check_scope_collision() {
    local other_target="$1" other_scope="$2"
    if [[ -f "$other_target" ]] && grep -qF "$RULE_TITLE" "$other_target" 2>/dev/null; then
        echo "  Note: this rule is also installed at $other_scope scope ($other_target)."
        echo "  If your agent reads both, the rule will appear twice in context."
    fi
}

echo "Installing $RULE_NAME rule ($SCOPE, format: $FORMAT)"
echo ""

if [[ "$SCOPE" == "global" ]]; then
    if [[ "$FORMAT" == "all" || "$FORMAT" == "agents" ]]; then
        check_scope_collision "AGENTS.md" "project"
        install_agents "$HOME/.config/devin/AGENTS.md"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "windsurf" ]]; then
        install_format_file "Windsurf" "windsurf" "$HOME/.windsurf/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "cursor" ]]; then
        install_format_file "Cursor" "cursor" "$HOME/.cursor/rules"
    fi
else
    if [[ "$FORMAT" == "all" || "$FORMAT" == "agents" ]]; then
        check_scope_collision "$HOME/.config/devin/AGENTS.md" "global"
        install_agents "AGENTS.md"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "windsurf" ]]; then
        install_format_file "Windsurf" "windsurf" ".windsurf/rules"
    fi
    if [[ "$FORMAT" == "all" || "$FORMAT" == "cursor" ]]; then
        install_format_file "Cursor" "cursor" ".cursor/rules"
    fi
fi

echo ""
echo "Done. The $RULE_NAME rule is now active."
