#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/validate_ai_documentation_packet.py"
FIXTURE_DIR="${SCRIPT_DIR}/fixtures"
status=0

for packet in "${FIXTURE_DIR}"/valid-*.json; do
  python3 -B "${VALIDATOR}" "${packet}" || status=1
done

for packet in "${FIXTURE_DIR}"/invalid-*.json; do
  if python3 -B "${VALIDATOR}" "${packet}" >/tmp/ai-documentation-invalid.out 2>/tmp/ai-documentation-invalid.err; then
    echo "ERROR expected invalid fixture to fail: $(basename "${packet}")" >&2
    status=1
  else
    echo "packet=$(basename "${packet}") expected=fail status=pass"
  fi
done

if [[ "${status}" -eq 0 ]]; then
  echo "ai-documentation fixture validation passed"
fi

exit "${status}"
