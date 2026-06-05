#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
VALIDATOR="$ROOT/skills/output-contract-enforcer/scripts/validate_output_contract.py"
FIXTURES="$ROOT/skills/output-contract-enforcer/scripts/fixtures"

python3 -B "$VALIDATOR" \
  --contract "$FIXTURES/markdown-contract.json" \
  --output "$FIXTURES/good-report.md" \
  --artifact-name "good-report.md" \
  --expect pass >/dev/null

for fixture in missing-section.md missing-evidence.md wrong-tag.md; do
  if python3 -B "$VALIDATOR" \
    --contract "$FIXTURES/markdown-contract.json" \
    --output "$FIXTURES/$fixture" \
    --artifact-name "$fixture" \
    --expect pass >/dev/null 2>&1; then
    echo "$fixture unexpectedly passed"
    exit 1
  fi
done

if python3 -B "$VALIDATOR" \
  --contract "$FIXTURES/markdown-contract.json" \
  --output "$FIXTURES/good-report.md" \
  --artifact-name "Final Report 2026.md" \
  --expect pass >/dev/null 2>&1; then
  echo "bad filename unexpectedly passed"
  exit 1
fi

python3 -B "$VALIDATOR" \
  --contract "$FIXTURES/json-contract.json" \
  --output "$FIXTURES/good-packet.json" \
  --artifact-name "good-packet.json" \
  --expect pass >/dev/null

if python3 -B "$VALIDATOR" \
  --contract "$FIXTURES/json-contract.json" \
  --output "$FIXTURES/missing-status.json" \
  --artifact-name "missing-status.json" \
  --expect pass >/dev/null 2>&1; then
  echo "missing-status unexpectedly passed"
  exit 1
fi

echo "OK: output-contract-enforcer validator fixtures passed"
