#!/usr/bin/env bash
set -euo pipefail
"$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/scripts/install-rule.sh" "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" "$@"
echo "Make sure the telegram-notify skill is also installed."
