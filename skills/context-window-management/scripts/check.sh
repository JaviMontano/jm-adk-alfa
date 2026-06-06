#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_context_window_report.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-over-budget-report.json"
python3 -B "$validator" "$fixtures/valid-at-limit-report.json"

if python3 -B "$validator" "$fixtures/invalid-over-budget-no-plan.json" >/tmp/context-window-over-budget.log 2>&1; then
  echo "ERROR: invalid-over-budget-no-plan.json unexpectedly passed"
  cat /tmp/context-window-over-budget.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-p0-evicted.json" >/tmp/context-window-p0.log 2>&1; then
  echo "ERROR: invalid-p0-evicted.json unexpectedly passed"
  cat /tmp/context-window-p0.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-compression-expands.json" >/tmp/context-window-expand.log 2>&1; then
  echo "ERROR: invalid-compression-expands.json unexpectedly passed"
  cat /tmp/context-window-expand.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-missing-preserve.json" >/tmp/context-window-preserve.log 2>&1; then
  echo "ERROR: invalid-missing-preserve.json unexpectedly passed"
  cat /tmp/context-window-preserve.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-missing-estimate.json" >/tmp/context-window-estimate.log 2>&1; then
  echo "ERROR: invalid-missing-estimate.json unexpectedly passed"
  cat /tmp/context-window-estimate.log
  exit 1
fi

echo "context-window-management fixture validation passed"
