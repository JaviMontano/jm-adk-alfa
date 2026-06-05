#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
VALIDATOR="$ROOT/skills/prompt-forge/scripts/validate_forge_packet.py"
FIXTURES="$ROOT/skills/prompt-forge/scripts/fixtures"

python3 -B "$VALIDATOR" "$FIXTURES/valid-create-packet.json" >/dev/null

if python3 -B "$VALIDATOR" "$FIXTURES/invalid-hidden-reasoning.json" >/dev/null 2>&1; then
  echo "invalid-hidden-reasoning unexpectedly passed"
  exit 1
fi

if python3 -B "$VALIDATOR" "$FIXTURES/invalid-missing-rubric.json" >/dev/null 2>&1; then
  echo "invalid-missing-rubric unexpectedly passed"
  exit 1
fi

if python3 -B "$VALIDATOR" "$FIXTURES/invalid-porting-losses.json" >/dev/null 2>&1; then
  echo "invalid-porting-losses unexpectedly passed"
  exit 1
fi

echo "OK: prompt-forge forge packet validator passed"
