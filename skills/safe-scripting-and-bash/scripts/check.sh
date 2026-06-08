#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VALIDATOR="$ROOT/skills/safe-scripting-and-bash/scripts/validate_safe_scripting_and_bash.py"
FIXTURES="$ROOT/skills/safe-scripting-and-bash/scripts/fixtures"

python3 -B "$VALIDATOR" --fixture-suite "$FIXTURES"
