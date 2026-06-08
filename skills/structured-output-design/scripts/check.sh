#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VALIDATOR="$ROOT/skills/structured-output-design/scripts/validate_structured_output_design.py"
FIXTURES="$ROOT/skills/structured-output-design/scripts/fixtures"

python3 -B "$VALIDATOR" --fixture-suite "$FIXTURES"
