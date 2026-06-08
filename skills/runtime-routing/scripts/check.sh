#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VALIDATOR="$ROOT/skills/runtime-routing/scripts/validate_runtime_routing.py"
FIXTURES="$ROOT/skills/runtime-routing/scripts/fixtures"

python3 -B "$VALIDATOR" --fixture-suite "$FIXTURES"
