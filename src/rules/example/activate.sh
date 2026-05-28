#!/usr/bin/env bash
# activate.sh — symlink (or copy on platforms without symlink support)
# this plugin's rule file into the project's .claude/rules/.
# Run this once after `/plugin install rule-example@dgxsparklabs-marketplace`.
#
# On Linux/macOS: creates symlinks so plugin updates auto-propagate.
# On Windows (Git Bash, MSYS) without symlink privileges: falls back
# to file copy. After a plugin update, re-run activate.sh to refresh.
set -euo pipefail

RULES_DIR="${1:-.claude/rules}"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$RULES_DIR"
mode="symlinked"
for rule in "$PLUGIN_DIR/rules"/*.md; do
  [ -e "$rule" ] || continue
  target="$RULES_DIR/$(basename "$rule")"
  rm -f "$target"
  if ln -s "$rule" "$target" 2>/dev/null && [ -L "$target" ]; then
    :
  else
    cp -f "$rule" "$target"
    mode="copied"
  fi
done

echo "$mode rule(s) into $RULES_DIR. Claude Code will load them at next session start."
if [ "$mode" = "copied" ]; then
  echo "Note: copies, not symlinks. Re-run activate.sh after a plugin update."
fi
