#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/validate_ai_conops_report.py"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"
TMP_ROOT="${TMPDIR:-/tmp}"
status=0

for report in "${FIXTURE_DIR}"/valid-*.json; do
  python3 -B "${VALIDATOR}" "${report}" || status=1
done

for report in "${FIXTURE_DIR}"/invalid-*.json; do
  out_file="${TMP_ROOT}/ai-conops-invalid-$(basename "${report}").out"
  err_file="${TMP_ROOT}/ai-conops-invalid-$(basename "${report}").err"
  if python3 -B "${VALIDATOR}" "${report}" >"${out_file}" 2>"${err_file}"; then
    echo "ERROR expected invalid fixture to fail: $(basename "${report}")" >&2
    status=1
  else
    echo "report=$(basename "${report}") expected=fail status=pass"
  fi
done

if [[ "${status}" -eq 0 ]]; then
  echo "ai-conops fixture validation passed"
fi

exit "${status}"
