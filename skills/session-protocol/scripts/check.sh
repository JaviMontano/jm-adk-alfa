#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_session_protocol_report.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-session-protocol-report.json"
python3 -B "$validator" "$fixtures/valid-blocked-report.json"

if python3 -B "$validator" "$fixtures/invalid-auto-closure.json" >/tmp/session-protocol-auto-close.log 2>&1; then
  echo "ERROR: invalid-auto-closure.json unexpectedly passed"
  cat /tmp/session-protocol-auto-close.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-missing-context-loading.json" >/tmp/session-protocol-missing-context.log 2>&1; then
  echo "ERROR: invalid-missing-context-loading.json unexpectedly passed"
  cat /tmp/session-protocol-missing-context.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-work-before-confirmation.json" >/tmp/session-protocol-unconfirmed-work.log 2>&1; then
  echo "ERROR: invalid-work-before-confirmation.json unexpectedly passed"
  cat /tmp/session-protocol-unconfirmed-work.log
  exit 1
fi

echo "session-protocol fixture validation passed"
