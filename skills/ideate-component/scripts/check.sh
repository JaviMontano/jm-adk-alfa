#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/ideate-component/scripts/validate_ideate_component_concept.py"
FIXTURES="$ROOT_DIR/skills/ideate-component/scripts/fixtures"
TMP_OUT="${TMPDIR:-/tmp}/ideate-component-check.out"

python3 -B "$SCRIPT" "$FIXTURES/valid-skill-component.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-hook-component.json"

invalid=(
  invalid-duplicate-name.json
  invalid-bad-component-type.json
  invalid-missing-conflict-resolution.json
  invalid-overdeep-moat.json
  invalid-hook-event.json
  invalid-tool-unknown.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >"$TMP_OUT" 2>&1; then
    cat "$TMP_OUT"
    echo "expected failure for $fixture"
    exit 1
  fi
done

rm -f "$TMP_OUT"
echo "ideate-component check passed: valid=2 invalid=${#invalid[@]}"
