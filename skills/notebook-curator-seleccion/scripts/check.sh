#!/usr/bin/env bash
# Deterministic script contract check for notebook-curator-seleccion.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/validate_archetype.py"

python3 "$validator" --emit >/dev/null

valid_count=0
blocked_count=0
invalid_count=0

for fixture in "$script_dir"/fixtures/valid-*.json; do
  python3 "$validator" --input "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

for fixture in "$script_dir"/fixtures/blocked-*.json; do
  if python3 "$validator" --input "$fixture" >/dev/null 2>&1; then
    echo "ERROR: expected blocked fixture to fail readiness: $fixture" >&2
    exit 1
  fi
  blocked_count=$((blocked_count + 1))
done

for fixture in "$script_dir"/fixtures/invalid-*.json; do
  if python3 "$validator" --input "$fixture" >/dev/null 2>&1; then
    echo "ERROR: expected invalid fixture to fail: $fixture" >&2
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

echo "notebook-curator-seleccion check passed: valid=$valid_count blocked=$blocked_count invalid=$invalid_count"
