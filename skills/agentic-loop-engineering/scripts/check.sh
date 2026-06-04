#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/agentic-loop-engineering"
TMP_DIR="${TMPDIR:-/tmp}/agentic-loop-engineering-check.$$"
trap 'rm -rf "$TMP_DIR"' EXIT
mkdir -p "$TMP_DIR"

python3 -B "$SKILL_DIR/scripts/compile-agentic-loop.py" \
  "$SKILL_DIR/scripts/fixtures/basic-agent-loop.json" \
  --output "$TMP_DIR/basic-loop.py" \
  --report "$TMP_DIR/basic-loop.md"

python3 -B "$SKILL_DIR/scripts/compile-agentic-loop.py" \
  "$SKILL_DIR/scripts/fixtures/observable-agent-loop.json" \
  --output "$TMP_DIR/observable-loop.py"

python3 - "$TMP_DIR/basic-loop.py" "$SKILL_DIR/scripts/fixtures/expected-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

generated = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["basic-loop.py"]
missing = [fragment for fragment in fragments if fragment not in generated]
if missing:
    raise SystemExit("missing generated fragments: " + ", ".join(missing))
PY

python3 - "$SKILL_DIR/scripts/compile-agentic-loop.py" <<'PY'
import sys
from pathlib import Path

source = Path(sys.argv[1]).read_text(encoding="utf-8")
compile(source, sys.argv[1], "exec")
PY

for fixture in \
  invalid-no-budget.json \
  invalid-prose-control.json \
  invalid-tool-result-role.json \
  invalid-unknown-stop-action.json
do
  if python3 -B "$SKILL_DIR/scripts/compile-agentic-loop.py" "$SKILL_DIR/scripts/fixtures/$fixture" >"$TMP_DIR/$fixture.out" 2>&1; then
    echo "ERROR: invalid fixture passed: $fixture" >&2
    cat "$TMP_DIR/$fixture.out" >&2
    exit 1
  fi
done

bash -n "$SKILL_DIR/scripts/check.sh"
echo "OK: agentic-loop-engineering scripts are deterministic"
