#!/usr/bin/env bash
# activate-installed-rules.sh — bulk-symlink every installed rule plugin
# from this marketplace into .claude/rules/.
#
# Use this after installing one or more rule plugins from the marketplace
# instead of running each plugin's own activate.sh individually.
#
# Usage:
#   bash activate-installed-rules.sh               # default target: .claude/rules
#   bash activate-installed-rules.sh <rules-dir>   # custom target
#
# Locates installed rule plugins by scanning the Claude Code plugin cache
# at ~/.claude/plugins/cache/ for directories named rule-* whose source
# is this marketplace (DgxSparkLabs/marketplace).
set -euo pipefail

RULES_DIR="${1:-.claude/rules}"
CACHE_ROOT="${HOME}/.claude/plugins/cache"

if [ ! -d "$CACHE_ROOT" ]; then
  echo "Error: Claude Code plugin cache not found at $CACHE_ROOT"
  echo "Have you installed any plugins yet? Try:"
  echo "  /plugin marketplace add DgxSparkLabs/marketplace"
  echo "  /plugin install rule-blast-radius@dgxsparklabs-marketplace"
  exit 1
fi

mkdir -p "$RULES_DIR"

count=0
mode="symlinked"
# Cache layout: ~/.claude/plugins/cache/<marketplace-name>/<plugin-name>/<version>/
# We walk every marketplace, every rule-* plugin, every installed version.
for rules_md in "$CACHE_ROOT"/*/rule-*/*/rules/*.md; do
  [ -e "$rules_md" ] || continue
  target="$RULES_DIR/$(basename "$rules_md")"
  rm -f "$target"
  if ln -s "$rules_md" "$target" 2>/dev/null && [ -L "$target" ]; then
    :  # real symlink created
  else
    cp -f "$rules_md" "$target"
    mode="copied"
  fi
  count=$((count + 1))
done

if [ "$count" -eq 0 ]; then
  echo "No rule plugins found in $CACHE_ROOT. Install some first:"
  echo "  /plugin install rule-blast-radius@dgxsparklabs-marketplace"
  echo "  /plugin install rules-quality@dgxsparklabs-marketplace"
  exit 0
fi

echo "$mode $count rule file(s) into $RULES_DIR."
echo "Claude Code will load them at next session start."
if [ "$mode" = "copied" ]; then
  echo "Note: copies, not symlinks (your platform doesn't allow symlinks here)."
  echo "      Re-run this script after a plugin update to refresh."
fi
