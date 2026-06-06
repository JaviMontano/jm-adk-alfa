#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/discovery-orchestration/scripts/validate_discovery_orchestration_packet.py"
FIXTURES="$ROOT_DIR/skills/discovery-orchestration/scripts/fixtures"

python3 -B "$SCRIPT" "$FIXTURES/valid-ready-pipeline.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-blocked-pipeline.json"

invalid=(
  invalid-missing-gate.json
  invalid-dependency-cycle.json
  invalid-ready-unvalidated-deliverable.json
  invalid-missing-owner.json
  invalid-moving-time-word.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >/tmp/discovery-orchestration-check.out 2>&1; then
    cat /tmp/discovery-orchestration-check.out
    echo "expected failure for $fixture"
    exit 1
  fi
done

echo "discovery-orchestration check passed: valid=2 invalid=${#invalid[@]}"
