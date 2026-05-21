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
  echo "  /plugin install rule-blast-radius@marketplace"
  exit 1
fi

mkdir -p "$RULES_DIR"

count=0
for marketplace_dir in "$CACHE_ROOT"/*/marketplace; do
  [ -d "$marketplace_dir" ] || continue
  for rule_plugin in "$marketplace_dir"/rule-*; do
    [ -d "$rule_plugin" ] || continue
    # Walk rules/*.md inside the plugin (always one file per individual rule plugin)
    for rule in "$rule_plugin"/rules/*.md; do
      [ -e "$rule" ] || continue
      ln -sfn "$rule" "$RULES_DIR/$(basename "$rule")"
      count=$((count + 1))
    done
  done
done

if [ "$count" -eq 0 ]; then
  echo "No rule plugins found in $CACHE_ROOT. Install some first:"
  echo "  /plugin install rule-blast-radius@marketplace"
  echo "  /plugin install rules-quality@marketplace"
  exit 0
fi

echo "Symlinked $count rule file(s) into $RULES_DIR."
echo "Claude Code will load them at next session start."
