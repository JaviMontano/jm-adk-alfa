#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/ai-workflow-automation/scripts/validate_ai_workflow_plan.py"
FIXTURES="$ROOT_DIR/skills/ai-workflow-automation/scripts/fixtures"

python3 -B "$SCRIPT" "$FIXTURES/valid-support-triage-plan.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-invoice-review-plan.json"

invalid=(
  invalid-missing-approval-gate.json
  invalid-ai-step-no-output-contract.json
  invalid-unbounded-retry.json
  invalid-handoff-missing-acceptance.json
  invalid-moving-time-word.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >/tmp/ai-workflow-automation-check.out 2>&1; then
    cat /tmp/ai-workflow-automation-check.out
    echo "expected failure for $fixture"
    exit 1
  fi
done

echo "ai-workflow-automation check passed: valid=2 invalid=${#invalid[@]}"
