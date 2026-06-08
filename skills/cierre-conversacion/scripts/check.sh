#!/usr/bin/env bash
# Deterministic report validator for cierre-conversacion.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/validate_cierre_conversacion_report.py"

valid_count=0
invalid_count=0

for fixture in "$script_dir"/fixtures/valid-*.json; do
  python3 "$validator" "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

for fixture in "$script_dir"/fixtures/invalid-*.json; do
  if python3 "$validator" "$fixture" >/dev/null 2>&1; then
    echo "ERROR: expected invalid fixture to fail: $fixture" >&2
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

echo "cierre-conversacion check passed: valid=$valid_count invalid=$invalid_count"
