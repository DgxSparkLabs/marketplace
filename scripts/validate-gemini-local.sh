#!/usr/bin/env bash
# validate-gemini-local.sh — Local-dev validation for Gemini CLI compatibility.
#
# GitHub Actions blocks @google/gemini-cli at the org policy level, so CI cannot run
# these checks. Contributors with the Gemini CLI installed locally run this script
# before opening PRs to verify Gemini compatibility manually.
#
# Usage:
#   ./scripts/validate-gemini-local.sh
#
# Requirements:
#   - Gemini CLI: npm install -g @google/gemini-cli
#   - uv: https://docs.astral.sh/uv/
#
# The checks here mirror the CI assertions in:
#   .github/workflows/compat-skill.yml (gemini matrix row)
#   .github/workflows/compat-mcp.yml (gemini matrix row)
#   .github/workflows/compat-hook.yml (gemini-migration-check row)
#   .github/workflows/compat-extension.yml
# Output format matches CI so local runs look identical to future passing CI runs.
#
# Note on workspace trust: gemini skills list may report
# "Skipping project agents due to untrusted folder."
# Add --skip-trust to bypass for local testing if needed.

set -euo pipefail

# Check if Gemini CLI is installed
if ! which gemini >/dev/null 2>&1; then
  echo "Gemini CLI not installed. To install: npm install -g @google/gemini-cli"
  echo "Skipping Gemini local validation."
  exit 0
fi

echo "==> Gemini CLI found: $(gemini --version)"
echo ""

# Ensure generated manifests are in sync
echo "==> Regenerating manifests from sources..."
uv run scripts/generate_manifest.py
echo ""

# --- Skill install + list ---
echo "==> [skill] Install skill-telegram-notify via Gemini..."
echo "y" | gemini skills install ./_generated/skill-telegram-notify 2>&1
echo ""

echo "==> [skill] Assert telegram-notify appears in gemini skills list --all..."
if gemini skills list --all 2>&1 | grep -F "telegram-notify" >/dev/null; then
  echo "    PASS: telegram-notify found in gemini skills list --all"
else
  echo "    FAIL: telegram-notify not found in gemini skills list --all"
  exit 1
fi
echo ""

# --- MCP list ---
echo "==> [mcp] Verify gemini mcp list returns exit 0 (baseline)..."
gemini mcp list 2>&1
echo ""

echo "==> [mcp] Add example-fetch MCP server..."
gemini mcp add example-fetch uvx mcp-server-fetch 2>&1
echo ""

echo "==> [mcp] Assert example-fetch appears in mcp list..."
if gemini mcp list 2>&1 | grep -F "example-fetch" >/dev/null; then
  echo "    PASS: example-fetch found in gemini mcp list"
else
  echo "    FAIL: example-fetch not found in gemini mcp list"
  exit 1
fi
echo ""

# --- Hook migration check ---
echo "==> [hook] Run gemini hooks migrate dry-run against our hooks.json..."
if gemini hooks migrate examples/example-hook/hooks/hooks.json --dry-run 2>&1; then
  echo "    PASS: gemini hooks migrate dry-run succeeded"
else
  echo "    FAIL: gemini hooks migrate dry-run failed"
  exit 1
fi
echo ""

# --- Extensions list ---
echo "==> [extension] Verify gemini extensions list returns exit 0..."
gemini extensions list 2>&1
echo ""

# --- Cleanup ---
echo "==> Cleaning up..."
gemini skills uninstall telegram-notify 2>&1 || true
gemini mcp remove example-fetch 2>&1 || true
echo ""

echo "All Gemini local validation checks passed."
