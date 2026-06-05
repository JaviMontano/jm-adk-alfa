#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
VALIDATOR="$ROOT/skills/ux-writing/scripts/validate_ux_writing_packet.py"
FIXTURES="$ROOT/skills/ux-writing/scripts/fixtures"
CONTRACT="$FIXTURES/ux-writing-contract.json"

python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --packet "$FIXTURES/valid-audit.md" \
  --expect pass >/dev/null

for fixture in invalid-missing-section.md invalid-generic-after.md invalid-unsupported-claim.md; do
  if python3 -B "$VALIDATOR" \
    --contract "$CONTRACT" \
    --packet "$FIXTURES/$fixture" \
    --expect pass >/dev/null 2>&1; then
    echo "$fixture unexpectedly passed"
    exit 1
  fi
done

echo "OK: ux-writing packet validator fixtures passed"
