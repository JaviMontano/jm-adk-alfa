#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/validate_workspace_setup_plan.py"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"
status=0
valid_count=0
invalid_count=0

for plan in "${FIXTURE_DIR}"/valid-*.json; do
  python3 -B "${VALIDATOR}" "${plan}" || status=1
  valid_count=$((valid_count + 1))
done

for plan in "${FIXTURE_DIR}"/invalid-*.json; do
  if python3 -B "${VALIDATOR}" "${plan}" >/tmp/workspace-setup-invalid.out 2>/tmp/workspace-setup-invalid.err; then
    echo "ERROR expected invalid fixture to fail: $(basename "${plan}")" >&2
    status=1
  else
    echo "plan=$(basename "${plan}") expected=fail status=pass"
  fi
  invalid_count=$((invalid_count + 1))
done

if [[ "${status}" -eq 0 ]]; then
  echo "workspace-setup check passed: valid=${valid_count} invalid=${invalid_count}"
fi

exit "${status}"
