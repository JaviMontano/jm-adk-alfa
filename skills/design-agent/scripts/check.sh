#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/design-agent/scripts/validate_design_agent_spec.py"
FIXTURES="$ROOT_DIR/skills/design-agent/scripts/fixtures"
TMP_OUT="${TMPDIR:-/tmp}/design-agent-check.out"

python3 -B "$SCRIPT" "$FIXTURES/valid-plugin-orchestrator.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-readonly-auditor.json"

invalid=(
  invalid-forbidden-hooks.json
  invalid-tools-disallowed-conflict.json
  invalid-maxturns-mismatch.json
  invalid-missing-flow.json
  invalid-generic-principle.json
  invalid-bad-agent-name.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >"$TMP_OUT" 2>&1; then
    cat "$TMP_OUT"
    echo "expected failure for $fixture"
    exit 1
  fi
done

rm -f "$TMP_OUT"
echo "design-agent check passed: valid=2 invalid=${#invalid[@]}"
