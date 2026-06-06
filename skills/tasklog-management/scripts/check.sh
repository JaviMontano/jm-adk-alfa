#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_tasklog_report.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-add-report.json"
python3 -B "$validator" "$fixtures/valid-stale-blocked-report.json"

if python3 -B "$validator" "$fixtures/invalid-stale-unflagged.json" >/tmp/tasklog-stale.log 2>&1; then
  echo "ERROR: invalid-stale-unflagged.json unexpectedly passed"
  cat /tmp/tasklog-stale.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-bad-id.json" >/tmp/tasklog-bad-id.log 2>&1; then
  echo "ERROR: invalid-bad-id.json unexpectedly passed"
  cat /tmp/tasklog-bad-id.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-unauthorized-update.json" >/tmp/tasklog-unauthorized.log 2>&1; then
  echo "ERROR: invalid-unauthorized-update.json unexpectedly passed"
  cat /tmp/tasklog-unauthorized.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-bridge-path.json" >/tmp/tasklog-bridge.log 2>&1; then
  echo "ERROR: invalid-bridge-path.json unexpectedly passed"
  cat /tmp/tasklog-bridge.log
  exit 1
fi

echo "tasklog-management fixture validation passed"
