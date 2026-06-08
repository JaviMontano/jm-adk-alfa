#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/validate_post_tool_use_report.py"

valid_count=0
for fixture in "$script_dir"/fixtures/valid-*.json; do
  python3 -m json.tool "$fixture" >/dev/null
  python3 "$validator" "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

invalid_count=0
for fixture in "$script_dir"/fixtures/invalid-*.json; do
  python3 -m json.tool "$fixture" >/dev/null
  if python3 "$validator" "$fixture" >/dev/null 2>&1; then
    echo "ERROR: invalid fixture unexpectedly passed: $fixture" >&2
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

echo "post-tool-use-validator check passed: valid=$valid_count invalid=$invalid_count"
