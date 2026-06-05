#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

SCRIPT="skills/prompt-engineering/scripts/validate_prompt_packet.py"

python3 -B "$SCRIPT" "skills/prompt-engineering/scripts/fixtures/valid-structured-output.json" >/dev/null

if python3 -B "$SCRIPT" "skills/prompt-engineering/scripts/fixtures/invalid-missing-adversarial.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-missing-adversarial fixture passed unexpectedly"
  exit 1
fi

if python3 -B "$SCRIPT" "skills/prompt-engineering/scripts/fixtures/invalid-weak-guardrails.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-weak-guardrails fixture passed unexpectedly"
  exit 1
fi

echo "OK: prompt-engineering prompt packet validator passed"
