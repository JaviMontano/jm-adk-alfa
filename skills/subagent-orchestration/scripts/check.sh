#!/usr/bin/env bash
# Deterministic script contract check for subagent-orchestration.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/validate_orchestration_plan.py"
fixtures="$script_dir/fixtures"

valid_count=0
blocked_count=0
invalid_count=0

for fixture in "$fixtures"/valid-*.json; do
  python3 -B "$validator" --input "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

for fixture in "$fixtures"/blocked-*.json; do
  if python3 -B "$validator" --input "$fixture" >/tmp/subagent-orchestration-blocked.out 2>&1; then
    echo "ERROR: blocked fixture passed unexpectedly: $fixture"
    cat /tmp/subagent-orchestration-blocked.out
    exit 1
  fi
  blocked_count=$((blocked_count + 1))
done

for fixture in "$fixtures"/invalid-*.json; do
  if python3 -B "$validator" --input "$fixture" >/tmp/subagent-orchestration-invalid.out 2>&1; then
    echo "ERROR: invalid fixture passed unexpectedly: $fixture"
    cat /tmp/subagent-orchestration-invalid.out
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

echo "subagent-orchestration check passed: valid=$valid_count blocked=$blocked_count invalid=$invalid_count"
