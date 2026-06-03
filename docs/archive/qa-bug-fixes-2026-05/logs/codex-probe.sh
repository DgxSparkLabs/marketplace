#!/bin/bash
set -x
echo "===node/npm==="
node --version
npm --version
echo "===installing codex==="
npm install -g @openai/codex 2>&1 | tail -20
echo "===codex version==="
codex --version || echo "codex not found"
which codex
echo "===marketplace register==="
codex plugin marketplace add DgxSparkLabs/marketplace 2>&1 || echo "marketplace add failed"
echo "===plugin add==="
codex plugin add agent-example@dgxsparklabs-marketplace 2>&1 || echo "plugin add failed"
echo "===where did the TOML land==="
find / -name '*.toml' -path '*/agents/*' 2>/dev/null
find / -name 'notebook-reviewer*' 2>/dev/null
echo "===~/.codex tree==="
find ~/.codex -maxdepth 6 2>/dev/null | head -100
echo "===config.toml==="
cat ~/.codex/config.toml 2>/dev/null || echo "no config.toml"
echo "===after manual copy==="
mkdir -p ~/.codex/agents
ls ~/.codex/.tmp/marketplaces/ 2>/dev/null
# Find any .toml inside the plugin tree and try copying it
TOML=$(find ~/.codex -name 'notebook-reviewer.toml' 2>/dev/null | head -1)
echo "Found TOML at: $TOML"
if [ -n "$TOML" ]; then
  cp "$TOML" ~/.codex/agents/notebook-reviewer.toml
  ls -la ~/.codex/agents/
fi
echo "===listing agents via codex==="
# can't run interactive; just check exit-status of help
codex agents list 2>&1 || codex agents 2>&1 || echo "no agents subcommand"
codex --help 2>&1 | head -40
