#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/claude-md-architecture"
TMP_DIR="${TMPDIR:-/tmp}/claude-md-architecture-check.$$"
trap 'rm -rf "$TMP_DIR"' EXIT
mkdir -p "$TMP_DIR"

python3 -B "$SKILL_DIR/scripts/compile-claude-md-architecture.py" \
  "$SKILL_DIR/scripts/fixtures/monorepo-architecture.json" \
  --output "$TMP_DIR/monorepo.md"

python3 -B "$SKILL_DIR/scripts/compile-claude-md-architecture.py" \
  "$SKILL_DIR/scripts/fixtures/nested-modules-architecture.json" \
  --output "$TMP_DIR/nested.md"

python3 - "$TMP_DIR/monorepo.md" "$SKILL_DIR/scripts/fixtures/expected-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

generated = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["monorepo.md"]
missing = [fragment for fragment in fragments if fragment not in generated]
if missing:
    raise SystemExit("missing generated fragments: " + ", ".join(missing))
PY

python3 - "$SKILL_DIR/scripts/compile-claude-md-architecture.py" <<'PY'
import sys
from pathlib import Path

source = Path(sys.argv[1]).read_text(encoding="utf-8")
compile(source, sys.argv[1], "exec")
PY

for fixture in \
  invalid-missing-user-scope.json \
  invalid-monolithic-root.json \
  invalid-module-glob-missing.json \
  invalid-precedence.json
do
  if python3 -B "$SKILL_DIR/scripts/compile-claude-md-architecture.py" "$SKILL_DIR/scripts/fixtures/$fixture" >"$TMP_DIR/$fixture.out" 2>&1; then
    echo "ERROR: invalid fixture passed: $fixture" >&2
    cat "$TMP_DIR/$fixture.out" >&2
    exit 1
  fi
done

bash -n "$SKILL_DIR/scripts/check.sh"
echo "OK: claude-md-architecture scripts are deterministic"
