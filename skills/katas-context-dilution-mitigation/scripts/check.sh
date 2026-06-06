#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SKILL_DIR="$ROOT_DIR/skills/katas-context-dilution-mitigation"
VALIDATOR="$SKILL_DIR/scripts/validate_context_dilution_report.py"
FIXTURES="$SKILL_DIR/scripts/fixtures"

valid_cases=(
  valid-compaction-required-report.json
  valid-below-threshold-report.json
)

invalid_cases=(
  invalid-middle-only-rule.json
  invalid-threshold-too-late.json
  invalid-drops-rules.json
  invalid-no-compaction-over-threshold.json
  invalid-bulk-context-at-edge.json
)

for case in "${valid_cases[@]}"; do
  python3 -B "$VALIDATOR" "$FIXTURES/$case"
done

for case in "${invalid_cases[@]}"; do
  if python3 -B "$VALIDATOR" "$FIXTURES/$case" >/tmp/katas-context-dilution-invalid.log 2>&1; then
    echo "expected fixture to fail: $case" >&2
    cat /tmp/katas-context-dilution-invalid.log >&2
    exit 1
  fi
  echo "report=$case expected=fail status=pass"
done

echo "katas-context-dilution-mitigation fixture validation passed"
