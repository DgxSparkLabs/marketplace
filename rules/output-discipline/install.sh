#!/usr/bin/env bash
set -euo pipefail
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/scripts/install-rule.sh" "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" "$@"
