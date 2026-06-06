#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_session_cleanup_report.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-closeout-report.json"
python3 -B "$validator" "$fixtures/valid-blocked-report.json"

if python3 -B "$validator" "$fixtures/invalid-missing-validation.json" >/tmp/session-end-cleanup-invalid-validation.log 2>&1; then
  echo "ERROR: invalid-missing-validation.json unexpectedly passed"
  cat /tmp/session-end-cleanup-invalid-validation.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-untagged-task.json" >/tmp/session-end-cleanup-invalid-task.log 2>&1; then
  echo "ERROR: invalid-untagged-task.json unexpectedly passed"
  cat /tmp/session-end-cleanup-invalid-task.log
  exit 1
fi

echo "session-end-cleanup fixture validation passed"
