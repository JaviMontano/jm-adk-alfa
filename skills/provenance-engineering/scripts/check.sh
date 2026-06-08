#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VALIDATOR="$ROOT/skills/provenance-engineering/scripts/validate_provenance_engineering.py"
FIXTURES="$ROOT/skills/provenance-engineering/scripts/fixtures"

python3 -B "$VALIDATOR" --fixture-suite "$FIXTURES"
