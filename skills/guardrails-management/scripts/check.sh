#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/guardrails-management/scripts/validate_guardrails_packet.py"
FIXTURES="$ROOT_DIR/skills/guardrails-management/scripts/fixtures"

python3 -B "$SCRIPT" "$FIXTURES/valid-confirmed-guideline.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-unconfirmed-proposal.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-deactivate-rule.json"

invalid=(
  invalid-unconfirmed-persist.json
  invalid-wrong-target-file.json
  invalid-duplicate-active-rule.json
  invalid-missing-verifiable-check.json
  invalid-delete-instead-of-deactivate.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >/tmp/guardrails-management-check.out 2>&1; then
    cat /tmp/guardrails-management-check.out
    echo "expected failure for $fixture"
    exit 1
  fi
done

echo "guardrails-management check passed: valid=3 invalid=${#invalid[@]}"
