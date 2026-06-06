#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SKILL_DIR="$ROOT_DIR/skills/katas-persistent-scratchpad"
VALIDATOR="$SKILL_DIR/scripts/validate_kata_scratchpad_report.py"
FIXTURES="$SKILL_DIR/scripts/fixtures"

valid_cases=(
  valid-parser-investigation-report.json
  valid-resume-report.json
)

invalid_cases=(
  invalid-missing-evidence.json
  invalid-reread-each-turn.json
  invalid-internal-monologue.json
  invalid-overwrite-existing.json
  invalid-missing-section.json
  invalid-conversation-memory-only.json
)

for case in "${valid_cases[@]}"; do
  python3 -B "$VALIDATOR" "$FIXTURES/$case"
done

for case in "${invalid_cases[@]}"; do
  if python3 -B "$VALIDATOR" "$FIXTURES/$case" >/tmp/katas-persistent-scratchpad-invalid.log 2>&1; then
    echo "expected fixture to fail: $case" >&2
    cat /tmp/katas-persistent-scratchpad-invalid.log >&2
    exit 1
  fi
  echo "report=$case expected=fail status=pass"
done

echo "katas-persistent-scratchpad fixture validation passed"
