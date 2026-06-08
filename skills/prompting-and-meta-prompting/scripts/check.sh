#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VALIDATOR="$ROOT/skills/prompting-and-meta-prompting/scripts/validate_prompting_and_meta_prompting.py"
FIXTURES="$ROOT/skills/prompting-and-meta-prompting/scripts/fixtures"

python3 -B "$VALIDATOR" --fixture-suite "$FIXTURES"
