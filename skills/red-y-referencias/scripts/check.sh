#!/usr/bin/env bash
# Deterministic script contract check for red-y-referencias.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/reference_network_validator.py"
fixtures="$script_dir/fixtures"

valid_count=0
blocked_count=0
invalid_count=0

for fixture in "$fixtures"/valid-*.json; do
  python3 "$validator" --input "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

for fixture in "$fixtures"/blocked-*.json; do
  if python3 "$validator" --input "$fixture" >/tmp/red-y-referencias-blocked.out 2>&1; then
    echo "ERROR: blocked fixture passed unexpectedly: $fixture"
    cat /tmp/red-y-referencias-blocked.out
    exit 1
  fi
  blocked_count=$((blocked_count + 1))
done

for fixture in "$fixtures"/invalid-*.json; do
  if python3 "$validator" --input "$fixture" >/tmp/red-y-referencias-invalid.out 2>&1; then
    echo "ERROR: invalid fixture passed unexpectedly: $fixture"
    cat /tmp/red-y-referencias-invalid.out
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

echo "red-y-referencias check passed: valid=$valid_count blocked=$blocked_count invalid=$invalid_count"
