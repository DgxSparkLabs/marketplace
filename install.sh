#!/usr/bin/env bash
# install.sh — one-line POSIX installer for the `agents` CLI (D-17).
#
# Drops a Python wrapper at ~/.local/bin/agents (override via AGENTS_DEST)
# and clones the agents_cli package into ~/.local/share/agents/ (override
# via AGENTS_LIB). AGENTS_REF selects the marketplace branch (default main).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/DgxSparkLabs/marketplace/main/install.sh | bash
#   bash install.sh                       # install from the repo's main branch
#   AGENTS_REF=my-branch bash install.sh  # install from a different ref
#   bash install.sh install skill-example # install + immediately invoke
set -euo pipefail

DEST="${AGENTS_DEST:-$HOME/.local/bin/agents}"
LIB="${AGENTS_LIB:-$HOME/.local/share/agents}"
REF="${AGENTS_REF:-main}"
REPO_URL="${AGENTS_MARKETPLACE_URL:-https://github.com/DgxSparkLabs/marketplace}"

PYTHON="${AGENTS_PYTHON:-}"
if [ -z "$PYTHON" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON=python
  else
    echo "error: python3 not found on PATH. Install Python 3.11+ first." >&2
    exit 1
  fi
fi
# Sanity-check Python version (>= 3.11 per tomllib + pattern matching).
if ! "$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'; then
  echo "error: Python 3.11+ required (found $($PYTHON --version 2>&1))." >&2
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "error: git not found on PATH. Install git first." >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")" "$LIB"

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

echo "Cloning $REPO_URL @ $REF ..."
git clone --depth 1 --branch "$REF" "$REPO_URL" "$TMPDIR/marketplace" >/dev/null

# Copy the CLI package + the md_to_toml converter (agent install depends on it).
rm -rf "$LIB/agents_cli" "$LIB/converters"
cp -r "$TMPDIR/marketplace/scripts/agents_cli" "$LIB/agents_cli"
cp -r "$TMPDIR/marketplace/scripts/converters" "$LIB/converters"

# Write the wrapper.
cat > "$DEST" <<WRAPPER
#!/usr/bin/env bash
PYTHONPATH="$LIB:\${PYTHONPATH:-}" exec "$PYTHON" -m agents_cli.main "\$@"
WRAPPER
chmod +x "$DEST"

echo "Installed 'agents' to $DEST"
echo "Library at      $LIB"
case ":$PATH:" in
  *":$(dirname "$DEST"):"*) ;;
  *) echo "note: $(dirname "$DEST") is not on PATH — add it to use the 'agents' command directly." ;;
esac

# Pass-through: if the user piped extra args after `install.sh`, exec them.
if [ "$#" -gt 0 ]; then
  exec "$DEST" "$@"
fi
