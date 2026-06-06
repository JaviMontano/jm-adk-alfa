#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_session_manager_report.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-planned-report.json"
python3 -B "$validator" "$fixtures/valid-blocked-missing-context.json"

if python3 -B "$validator" "$fixtures/invalid-missing-context-pass.json" >/tmp/session-manager-missing-context.log 2>&1; then
  echo "ERROR: invalid-missing-context-pass.json unexpectedly passed"
  cat /tmp/session-manager-missing-context.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-stage-skip.json" >/tmp/session-manager-stage-skip.log 2>&1; then
  echo "ERROR: invalid-stage-skip.json unexpectedly passed"
  cat /tmp/session-manager-stage-skip.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-implementing-no-tasks.json" >/tmp/session-manager-implementing.log 2>&1; then
  echo "ERROR: invalid-implementing-no-tasks.json unexpectedly passed"
  cat /tmp/session-manager-implementing.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-unauthorized-write.json" >/tmp/session-manager-unauthorized.log 2>&1; then
  echo "ERROR: invalid-unauthorized-write.json unexpectedly passed"
  cat /tmp/session-manager-unauthorized.log
  exit 1
fi

echo "session-manager fixture validation passed"
