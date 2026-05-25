#!/bin/bash
set -x
echo "===versions==="
node --version
npm --version
echo "===install gemini==="
npm install -g @google/gemini-cli 2>&1 | tail -5
gemini --version || echo "no gemini"
which gemini
echo "===install marketplace ext (no auth, may fail)==="
mkdir -p /workspace && cd /workspace
gemini extensions install https://github.com/DgxSparkLabs/marketplace --consent 2>&1 | head -50 || echo "install fail"
echo "===ext tree==="
find ~/.gemini -type f 2>/dev/null | head -80
echo "===our hooks file in installed ext==="
find ~/.gemini/extensions -name "hooks.json" -exec sh -c 'echo "== $1 ==" ; cat "$1"' _ {} \; 2>/dev/null
echo "===our agents files in installed ext==="
find ~/.gemini/extensions -name "*.md" -path "*/agents/*" -exec sh -c 'echo "== $1 ==" ; cat "$1"' _ {} \; 2>/dev/null
echo "===gemini help==="
gemini --help 2>&1 | head -80
echo "===gemini extensions list==="
gemini extensions list 2>&1 || true
