#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/validate_analytics_implementation.py"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"
status=0
invalid_out="$(mktemp)"
invalid_err="$(mktemp)"
trap 'rm -f "${invalid_out}" "${invalid_err}"' EXIT

for report in "${FIXTURE_DIR}"/valid-*.json; do
  python3 -B "${VALIDATOR}" "${report}" || status=1
done

for report in "${FIXTURE_DIR}"/invalid-*.json; do
  if python3 -B "${VALIDATOR}" "${report}" >"${invalid_out}" 2>"${invalid_err}"; then
    echo "ERROR expected invalid fixture to fail: $(basename "${report}")" >&2
    status=1
  else
    echo "report=$(basename "${report}") expected=fail status=pass"
  fi
done

if [[ "${status}" -eq 0 ]]; then
  echo "analytics-implementation fixture validation passed"
fi

exit "${status}"
