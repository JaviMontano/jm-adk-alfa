#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/validate_ai_testing_strategy.py"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"
status=0

for report in "${FIXTURE_DIR}"/valid-*.json; do
  python3 -B "${VALIDATOR}" "${report}" || status=1
done

for report in "${FIXTURE_DIR}"/invalid-*.json; do
  if python3 -B "${VALIDATOR}" "${report}" >/tmp/ai-testing-strategy-invalid.out 2>/tmp/ai-testing-strategy-invalid.err; then
    echo "ERROR expected invalid fixture to fail: $(basename "${report}")" >&2
    status=1
  else
    echo "report=$(basename "${report}") expected=fail status=pass"
  fi
done

if [[ "${status}" -eq 0 ]]; then
  echo "ai-testing-strategy fixture validation passed"
fi

exit "${status}"
