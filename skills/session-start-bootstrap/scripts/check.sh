#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_session_start_packet.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-start-packet.json"
python3 -B "$validator" "$fixtures/valid-blocked-dirty-tree.json"

if python3 -B "$validator" "$fixtures/invalid-missing-environment.json" >/tmp/session-start-invalid-env.log 2>&1; then
  echo "ERROR: invalid-missing-environment.json unexpectedly passed"
  cat /tmp/session-start-invalid-env.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-dirty-pass.json" >/tmp/session-start-invalid-dirty-pass.log 2>&1; then
  echo "ERROR: invalid-dirty-pass.json unexpectedly passed"
  cat /tmp/session-start-invalid-dirty-pass.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-missing-first-action.json" >/tmp/session-start-invalid-first-action.log 2>&1; then
  echo "ERROR: invalid-missing-first-action.json unexpectedly passed"
  cat /tmp/session-start-invalid-first-action.log
  exit 1
fi

echo "session-start-bootstrap fixture validation passed"
