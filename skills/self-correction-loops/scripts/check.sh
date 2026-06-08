#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VALIDATOR="$ROOT/skills/self-correction-loops/scripts/validate_self_correction_loops.py"
FIXTURES="$ROOT/skills/self-correction-loops/scripts/fixtures"

python3 -B "$VALIDATOR" --fixture-suite "$FIXTURES"
