#!/usr/bin/env bash
# post-create.sh — one-time setup after the dev container is built.
# Invoked by devcontainer.json's "postCreateCommand". Adds the project-specific
# Python tooling on top of what the Dev Container Features already provide.
set -euo pipefail

# --------------------------------------------------------------------
# Fix EACCES on the persisted /home/vscode/.claude volume mount.
# Docker mounts named volumes root-owned by default; the `vscode` user
# can't mkdir inside ~/.claude/plugins/ without a chown.
# This is the canonical fix from the Anthropic reference container.
# --------------------------------------------------------------------
sudo chown -R "$(id -u)":"$(id -g)" "$HOME/.claude" 2>/dev/null || true
mkdir -p "$HOME/.claude/plugins"

# --------------------------------------------------------------------
# uv is the canonical Python tool for this repo per AGENTS.md "Python UV"
# rules. The Python feature ships pip but explicitly NOT uv; install it
# from astral.sh so we get the latest stable.
# --------------------------------------------------------------------
curl -LsSf https://astral.sh/uv/install.sh | sh

# Persist uv on PATH for interactive shells.
if ! grep -q '.local/bin' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
export PATH="$HOME/.local/bin:$PATH"

# --------------------------------------------------------------------
# No apt python3-flask: the hermetic stubs at tests/fixtures/claude-stub/
# carry their own PEP 723 inline metadata. `uv run stub.py` fetches Flask
# into an ephemeral env on first invocation. This keeps the rule "always
# use uv" from AGENTS.md and avoids the silent apt failure mode we saw
# during the first operator pass.
# --------------------------------------------------------------------

echo ""
echo "===================================================================="
echo "Dev container ready."
echo ""
echo "Tools installed:"
printf '  node    %s\n' "$(node --version)"
printf '  npm     %s\n' "$(npm --version)"
printf '  claude  %s\n' "$(claude --version 2>&1 | head -1)"
printf '  uv      %s\n' "$(uv --version 2>&1)"
printf '  python  %s\n' "$(python3 --version 2>&1)"
printf '  git     %s\n' "$(git --version 2>&1)"
printf '  gh      %s\n' "$(gh --version 2>&1 | head -1)"
echo "===================================================================="
echo ""
echo "What to do next:"
echo "  Operator QA path:      docs/TEST_YOURSELF.md  (start with the Claude section)"
echo "  Hermetic stub:         uv run tests/fixtures/claude-stub/stub.py"
echo "  Marketplace tests:     uv run tests/test_marketplace.py"
echo "  Schema fitness tests:  uv run tests/test_schema_fitness.py"
echo "  Regenerate manifests:  uv run scripts/generate_manifest.py"
echo "  Roadmap + open tasks:  docs/ROADMAP.md"
echo "===================================================================="
