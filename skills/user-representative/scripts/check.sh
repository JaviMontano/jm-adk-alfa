#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
VALIDATOR="$ROOT/skills/user-representative/scripts/validate_user_representative_review.py"
FIXTURES="$ROOT/skills/user-representative/scripts/fixtures"
CONTRACT="$FIXTURES/review-contract.json"

python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --review "$FIXTURES/valid-review.md" \
  --expect pass >/dev/null

for fixture in invalid-missing-section.md invalid-wrong-verdict.md invalid-missing-evidence.md; do
  if python3 -B "$VALIDATOR" \
    --contract "$CONTRACT" \
    --review "$FIXTURES/$fixture" \
    --expect pass >/dev/null 2>&1; then
    echo "$fixture unexpectedly passed"
    exit 1
  fi
done

echo "OK: user-representative review validator fixtures passed"
