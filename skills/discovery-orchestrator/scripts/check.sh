#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/discovery-orchestrator/scripts/validate_discovery_orchestrator_packet.py"
FIXTURES="$ROOT_DIR/skills/discovery-orchestrator/scripts/fixtures"
TMP_OUT="${TMPDIR:-/tmp}/discovery-orchestrator-check.out"

python3 -B "$SCRIPT" "$FIXTURES/valid-g1-pass-packet.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-g1-blocked-packet.json"

invalid=(
  invalid-analyzes-content.json
  invalid-missing-g1-approval.json
  invalid-phase-order.json
  invalid-skill-out-of-range.json
  invalid-assumption-warning-missing.json
  invalid-price-output.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >"$TMP_OUT" 2>&1; then
    cat "$TMP_OUT"
    echo "expected failure for $fixture"
    exit 1
  fi
done

rm -f "$TMP_OUT"
echo "discovery-orchestrator check passed: valid=2 invalid=${#invalid[@]}"
