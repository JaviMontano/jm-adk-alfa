#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SKILL_DIR="$ROOT_DIR/skills/persistent-memory-design"
VALIDATOR="$SKILL_DIR/scripts/validate_persistent_memory_report.py"
FIXTURES="$SKILL_DIR/scripts/fixtures"

valid_cases=(
  valid-pii-audit-report.json
  valid-multisession-research-report.json
)

invalid_cases=(
  invalid-missing-evidence.json
  invalid-reread-each-turn.json
  invalid-raw-transcript.json
  invalid-schema-drift.json
  invalid-unsafe-path.json
  invalid-full-rewrite.json
  invalid-conversation-dependency.json
)

for case in "${valid_cases[@]}"; do
  python3 -B "$VALIDATOR" "$FIXTURES/$case"
done

for case in "${invalid_cases[@]}"; do
  if python3 -B "$VALIDATOR" "$FIXTURES/$case" >/tmp/persistent-memory-design-invalid.log 2>&1; then
    echo "expected fixture to fail: $case" >&2
    cat /tmp/persistent-memory-design-invalid.log >&2
    exit 1
  fi
  echo "report=$case expected=fail status=pass"
done

echo "persistent-memory-design fixture validation passed"
