#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/error-recovery-automation"
VALIDATOR="$SKILL_DIR/scripts/validate_error_recovery.py"
TMP_OUTPUT="$(mktemp)"
trap 'rm -f "$TMP_OUTPUT"' EXIT

valid_count=0
invalid_count=0

for fixture in "$SKILL_DIR"/scripts/fixtures/valid-*.json; do
  python3 -B "$VALIDATOR" "$fixture" >"$TMP_OUTPUT"
  valid_count=$((valid_count + 1))
done

for fixture in "$SKILL_DIR"/scripts/fixtures/invalid-*.json; do
  if python3 -B "$VALIDATOR" "$fixture" >"$TMP_OUTPUT" 2>&1; then
    printf 'ERROR: invalid fixture passed unexpectedly: %s\n' "$fixture" >&2
    cat "$TMP_OUTPUT" >&2
    exit 1
  fi
  invalid_count=$((invalid_count + 1))
done

printf 'error-recovery-automation check passed: valid=%s invalid=%s\n' "$valid_count" "$invalid_count"
