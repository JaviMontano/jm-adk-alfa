#!/usr/bin/env bash
# Deterministic script contract check for simulador-entrevista.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/interview_sim_validator.py"
fixtures="$script_dir/fixtures"

valid_count=0
blocked_count=0
invalid_count=0

python3 -m json.tool "$script_dir/question_bank.json" >/dev/null

for fixture in "$fixtures"/valid-*.json; do
  python3 "$validator" --input "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

for fixture in "$fixtures"/blocked-*.json; do
  if python3 "$validator" --input "$fixture" >/tmp/simulador-entrevista-blocked.out 2>&1; then
    echo "ERROR: blocked fixture passed unexpectedly: $fixture"
    cat /tmp/simulador-entrevista-blocked.out
    exit 1
  fi
  blocked_count=$((blocked_count + 1))
done

for fixture in "$fixtures"/invalid-*.json; do
  if python3 "$validator" --input "$fixture" >/tmp/simulador-entrevista-invalid.out 2>&1; then
    echo "ERROR: invalid fixture passed unexpectedly: $fixture"
    cat /tmp/simulador-entrevista-invalid.out
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

echo "simulador-entrevista check passed: valid=$valid_count blocked=$blocked_count invalid=$invalid_count"
