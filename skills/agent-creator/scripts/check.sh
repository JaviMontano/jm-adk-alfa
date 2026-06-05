#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/agent-creator/scripts/compile-agent.py"
FIXTURES="$ROOT_DIR/skills/agent-creator/scripts/fixtures"
OUT="$(mktemp "${TMPDIR:-/tmp}/agent-creator-check.XXXXXX")"

python3 "$SCRIPT" --input "$FIXTURES/agent-spec-input.json" --output "$OUT"

python3 - "$OUT" "$FIXTURES/expected-agent-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in output]
if missing:
    print("missing fragments:")
    for fragment in missing:
        print(fragment)
    raise SystemExit(1)
PY

for invalid in \
  invalid-name-collision.json \
  invalid-wildcard-tool.json \
  invalid-missing-trigger.json \
  invalid-no-negative-boundary.json
do
  if python3 "$SCRIPT" --input "$FIXTURES/$invalid" >/dev/null 2>&1; then
    echo "invalid fixture unexpectedly passed: $invalid" >&2
    exit 1
  fi
done

echo "agent-creator fixtures passed"
