#!/usr/bin/env bash
# post-create.sh — one-time setup after the dev container is built.
# Invoked by devcontainer.json's "postCreateCommand". Adds the project-specific
# Python tooling on top of what the Dev Container Features already provide.
set -euo pipefail

# uv is the canonical Python tool for this repo per AGENTS.md "Python UV" rules.
# The python feature ships pip/setuptools but explicitly NOT uv; install it
# from astral.sh so we get the latest stable.
curl -LsSf https://astral.sh/uv/install.sh | sh

# uv installs to ~/.local/bin; persist that on PATH for interactive shells.
if ! grep -q '.local/bin' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

# Flask is the only dependency of the hermetic Claude stub at
# tests/fixtures/claude-stub/. We install it system-wide via apt rather than
# uv venv so that `python3 tests/fixtures/claude-stub/stub.py` Just Works
# without the operator having to remember to activate a virtualenv.
sudo apt-get update
sudo apt-get install -y --no-install-recommends python3-flask

# Make the new PATH active in this script so the version checks below work.
export PATH="$HOME/.local/bin:$PATH"

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
printf '  flask   %s\n' "$(python3 -c 'import flask; print(flask.__version__)')"
printf '  git     %s\n' "$(git --version 2>&1)"
printf '  gh      %s\n' "$(gh --version 2>&1 | head -1)"
echo "===================================================================="
echo ""
echo "What to do next:"
echo "  Operator QA path:      docs/TEST_YOURSELF.md  (start with the Claude section)"
echo "  Hermetic Claude stub:  python3 tests/fixtures/claude-stub/stub.py"
echo "  Marketplace tests:     uv run tests/test_marketplace.py"
echo "  Schema fitness tests:  uv run tests/test_schema_fitness.py"
echo "  Regenerate manifests:  uv run scripts/generate_manifest.py"
echo "  Roadmap + open tasks:  docs/ROADMAP.md"
echo "===================================================================="
