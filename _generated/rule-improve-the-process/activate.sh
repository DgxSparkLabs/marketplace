#!/usr/bin/env bash
# activate.sh — symlink this plugin's rule file(s) into the project's .claude/rules/
# Run once after installing this plugin.
#
# Usage:
#   bash <path>/activate.sh                   # default target: .claude/rules
#   bash <path>/activate.sh <rules-dir>       # custom target
set -euo pipefail

RULES_DIR="${1:-.claude/rules}"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$RULES_DIR"
for rule in "$PLUGIN_DIR/rules"/*.md; do
  [ -e "$rule" ] || continue
  ln -sfn "$rule" "$RULES_DIR/$(basename "$rule")"
done
echo "Symlinked rule(s) into $RULES_DIR. Claude Code will load them at next session start."
