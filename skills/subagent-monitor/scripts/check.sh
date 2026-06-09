#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/validate_subagent_monitor_report.py"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"
status=0
valid_count=0
invalid_count=0

for report in "${FIXTURE_DIR}"/valid-*.json; do
  python3 -B "${VALIDATOR}" "${report}" || status=1
  valid_count=$((valid_count + 1))
done

for report in "${FIXTURE_DIR}"/invalid-*.json; do
  if python3 -B "${VALIDATOR}" "${report}" >/tmp/subagent-monitor-invalid.out 2>/tmp/subagent-monitor-invalid.err; then
    echo "ERROR expected invalid fixture to fail: $(basename "${report}")" >&2
    status=1
  else
    echo "report=$(basename "${report}") expected=fail status=pass"
  fi
  invalid_count=$((invalid_count + 1))
done

if [[ "${status}" -eq 0 ]]; then
  echo "subagent-monitor check passed: valid=${valid_count} invalid=${invalid_count}"
fi

exit "${status}"
