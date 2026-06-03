#!/usr/bin/env bash
# validate-codex-local.sh — Local-dev validation for Codex CLI compatibility.
#
# GitHub Actions blocks @openai/codex at the org policy level, so CI cannot run
# these checks. Contributors with the Codex CLI installed locally run this script
# before opening PRs to verify Codex compatibility manually.
#
# Usage:
#   ./scripts/validate-codex-local.sh
#
# Requirements:
#   - Codex CLI: npm install -g @openai/codex
#   - uv: https://docs.astral.sh/uv/
#
# The checks here mirror the CI assertions in .github/workflows/compat-marketplace-add.yml
# and .github/workflows/compat-mcp.yml (codex matrix rows). Output format matches CI
# so local runs look identical to future passing CI runs.

set -euo pipefail

MARKETPLACE_NAME="dgxsparklabs-marketplace"

# Check if Codex CLI is installed
if ! which codex >/dev/null 2>&1; then
  echo "Codex CLI not installed. To install: npm install -g @openai/codex"
  echo "Skipping Codex local validation."
  exit 0
fi

echo "==> Codex CLI found: $(codex --version)"
echo ""

# Ensure generated manifests are in sync
echo "==> Regenerating manifests from sources..."
uv run scripts/generate_manifest.py
echo ""

# --- Marketplace registration ---
echo "==> [marketplace-add] Register marketplace..."
codex plugin marketplace add ./ 2>&1
echo "==> [marketplace-add] Verify marketplace appears in config..."
if grep -F "${MARKETPLACE_NAME}" ~/.codex/config.toml >/dev/null; then
  echo "    PASS: ${MARKETPLACE_NAME} found in ~/.codex/config.toml"
else
  echo "    FAIL: ${MARKETPLACE_NAME} not found in ~/.codex/config.toml"
  exit 1
fi
echo ""

# --- MCP server ---
echo "==> [mcp] Verify codex mcp list returns exit 0 (baseline)..."
codex mcp list 2>&1
echo ""

echo "==> [mcp] Add example MCP server..."
codex mcp add example -- uvx mcp-server-fetch 2>&1
echo ""

echo "==> [mcp] Assert example appears in mcp list..."
if codex mcp list 2>&1 | grep -F "example" >/dev/null; then
  echo "    PASS: example found in codex mcp list"
else
  echo "    FAIL: example not found in codex mcp list"
  exit 1
fi
echo ""

echo "==> [mcp] Assert codex mcp get example --json returns valid output..."
codex mcp get example --json 2>&1
echo ""

# --- Features ---
echo "==> [features] Verify codex features list returns exit 0..."
codex features list >/dev/null 2>&1 && echo "    PASS: codex features list returned exit 0"
echo ""

# --- Cleanup ---
echo "==> Cleaning up..."
codex plugin marketplace remove "${MARKETPLACE_NAME}" 2>&1 || true
echo ""

echo "All Codex local validation checks passed."
