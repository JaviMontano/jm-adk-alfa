#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SKILL_DIR="$ROOT_DIR/skills/input-analysis"
VALIDATOR="$SKILL_DIR/scripts/validate_input_analysis_report.py"
FIXTURES="$SKILL_DIR/scripts/fixtures"

valid_cases=(
  valid-rfp-report.json
  valid-assumption-warning-report.json
)

invalid_cases=(
  invalid-missing-evidence-tag.json
  invalid-score-out-of-range.json
  invalid-assumption-warning-missing.json
  invalid-implementation-details.json
  invalid-missing-action.json
)

for case in "${valid_cases[@]}"; do
  python3 -B "$VALIDATOR" "$FIXTURES/$case"
done

for case in "${invalid_cases[@]}"; do
  if python3 -B "$VALIDATOR" "$FIXTURES/$case" >/tmp/input-analysis-invalid.log 2>&1; then
    echo "expected fixture to fail: $case" >&2
    cat /tmp/input-analysis-invalid.log >&2
    exit 1
  fi
  echo "report=$case expected=fail status=pass"
done

echo "input-analysis fixture validation passed"
