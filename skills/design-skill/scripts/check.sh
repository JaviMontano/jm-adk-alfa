#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/design-skill/scripts/validate_design_skill_spec.py"
FIXTURES="$ROOT_DIR/skills/design-skill/scripts/fixtures"
TMP_OUT="${TMPDIR:-/tmp}/design-skill-check.out"

python3 -B "$SCRIPT" "$FIXTURES/valid-readonly-skill.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-generation-skill.json"

invalid=(
  invalid-bad-name.json
  invalid-write-for-readonly.json
  invalid-short-procedure.json
  invalid-generic-quality.json
  invalid-missing-edge-cases.json
  invalid-low-moat-score.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >"$TMP_OUT" 2>&1; then
    cat "$TMP_OUT"
    echo "expected failure for $fixture"
    exit 1
  fi
done

rm -f "$TMP_OUT"
echo "design-skill check passed: valid=2 invalid=${#invalid[@]}"
