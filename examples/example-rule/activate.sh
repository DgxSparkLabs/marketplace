#!/usr/bin/env bash
# activate.sh — symlink this plugin's rule file into the project's .claude/rules/
# Run this once after `/plugin install example-rule@marketplace`.
#
# Usage:
#   bash <path-to-this-script>
#   bash <path-to-this-script> <target-rules-dir>    # custom target
#
# Default target: .claude/rules/ in the current working directory.
set -euo pipefail

RULES_DIR="${1:-.claude/rules}"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$RULES_DIR"
for rule in "$PLUGIN_DIR/rules"/*.md; do
  ln -sfn "$rule" "$RULES_DIR/$(basename "$rule")"
done

echo "Symlinked rule(s) into $RULES_DIR. Claude Code will load them at next session start."
