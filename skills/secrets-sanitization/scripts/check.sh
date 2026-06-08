#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="$script_dir/validate_secrets_sanitization_report.py"
valid=0
for fixture in "$script_dir"/fixtures/valid-*.json; do python3 -m json.tool "$fixture" >/dev/null; python3 "$validator" "$fixture" >/dev/null; valid=$((valid+1)); done
invalid=0
for fixture in "$script_dir"/fixtures/invalid-*.json; do python3 -m json.tool "$fixture" >/dev/null; if python3 "$validator" "$fixture" >/dev/null 2>&1; then echo "ERROR: invalid fixture unexpectedly passed: $fixture" >&2; exit 1; fi; invalid=$((invalid+1)); done
echo "secrets-sanitization check passed: valid=$valid invalid=$invalid"
