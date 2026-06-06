#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SKILL_DIR="$ROOT_DIR/skills/katas-session-resume-fork"
VALIDATOR="$SKILL_DIR/scripts/validate_kata_session_report.py"
FIXTURES="$SKILL_DIR/scripts/fixtures"

valid_cases=(
  valid-resume-report.json
  valid-fork-report.json
  valid-fresh-report.json
)

invalid_cases=(
  invalid-resume-after-refactor.json
  invalid-fork-shared-state.json
  invalid-fresh-raw-transcript.json
  invalid-missing-reason.json
  invalid-command-mismatch.json
  invalid-fresh-missing-summary.json
)

for case in "${valid_cases[@]}"; do
  python3 -B "$VALIDATOR" "$FIXTURES/$case"
done

for case in "${invalid_cases[@]}"; do
  if python3 -B "$VALIDATOR" "$FIXTURES/$case" >/tmp/katas-session-resume-fork-invalid.log 2>&1; then
    echo "expected fixture to fail: $case" >&2
    cat /tmp/katas-session-resume-fork-invalid.log >&2
    exit 1
  fi
  echo "report=$case expected=fail status=pass"
done

echo "katas-session-resume-fork fixture validation passed"
