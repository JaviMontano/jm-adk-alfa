#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

SCRIPT="skills/prompt-creator/scripts/validate_prompt_artifact.py"

python3 -B "$SCRIPT" --fixture "skills/prompt-creator/scripts/fixtures/valid-handoff.json" >/dev/null

if python3 -B "$SCRIPT" --fixture "skills/prompt-creator/scripts/fixtures/invalid-missing-omit.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-missing-omit fixture passed unexpectedly"
  exit 1
fi

if python3 -B "$SCRIPT" --fixture "skills/prompt-creator/scripts/fixtures/invalid-placeholder.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-placeholder fixture passed unexpectedly"
  exit 1
fi

echo "OK: prompt-creator prompt artifact validator passed"

