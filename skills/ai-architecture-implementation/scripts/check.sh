#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/validate_ai_architecture_implementation_plan.py"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"
status=0

for plan in "${FIXTURE_DIR}"/valid-*.json; do
  python3 -B "${VALIDATOR}" "${plan}" || status=1
done

for plan in "${FIXTURE_DIR}"/invalid-*.json; do
  if python3 -B "${VALIDATOR}" "${plan}" >/tmp/ai-architecture-implementation-invalid.out 2>/tmp/ai-architecture-implementation-invalid.err; then
    echo "ERROR expected invalid fixture to fail: $(basename "${plan}")" >&2
    status=1
  else
    echo "plan=$(basename "${plan}") expected=fail status=pass"
  fi
done

if [[ "${status}" -eq 0 ]]; then
  echo "ai-architecture-implementation fixture validation passed"
fi

exit "${status}"
