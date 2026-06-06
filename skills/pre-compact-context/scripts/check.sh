#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_pre_compact_packet.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-pre-compact-packet.json"
python3 -B "$validator" "$fixtures/valid-blocked-packet.json"

if python3 -B "$validator" "$fixtures/invalid-drops-p0.json" >/tmp/pre-compact-invalid-drop.log 2>&1; then
  echo "ERROR: invalid-drops-p0.json unexpectedly passed"
  cat /tmp/pre-compact-invalid-drop.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-missing-rehydration.json" >/tmp/pre-compact-invalid-rehydration.log 2>&1; then
  echo "ERROR: invalid-missing-rehydration.json unexpectedly passed"
  cat /tmp/pre-compact-invalid-rehydration.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-secret-leak.json" >/tmp/pre-compact-invalid-secret.log 2>&1; then
  echo "ERROR: invalid-secret-leak.json unexpectedly passed"
  cat /tmp/pre-compact-invalid-secret.log
  exit 1
fi

echo "pre-compact-context fixture validation passed"
