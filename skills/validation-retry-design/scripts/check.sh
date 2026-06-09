#!/usr/bin/env bash
# Deterministic script contract check for validation-retry-design.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/validate_retry_plan.py"
fixtures="$script_dir/fixtures"

valid_count=0
blocked_count=0
invalid_count=0

for fixture in "$fixtures"/valid-*.json; do
  python3 -B "$validator" --input "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

for fixture in "$fixtures"/blocked-*.json; do
  if python3 -B "$validator" --input "$fixture" >/tmp/validation-retry-blocked.out 2>&1; then
    echo "ERROR: blocked fixture passed unexpectedly: $fixture"
    cat /tmp/validation-retry-blocked.out
    exit 1
  fi
  blocked_count=$((blocked_count + 1))
done

for fixture in "$fixtures"/invalid-*.json; do
  if python3 -B "$validator" --input "$fixture" >/tmp/validation-retry-invalid.out 2>&1; then
    echo "ERROR: invalid fixture passed unexpectedly: $fixture"
    cat /tmp/validation-retry-invalid.out
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

echo "validation-retry-design check passed: valid=$valid_count blocked=$blocked_count invalid=$invalid_count"
