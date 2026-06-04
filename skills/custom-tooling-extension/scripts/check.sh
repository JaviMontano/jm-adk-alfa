#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/custom-tooling-extension"
TMP_DIR="${TMPDIR:-/tmp}/custom-tooling-extension-check.$$"
trap 'rm -rf "$TMP_DIR"' EXIT
mkdir -p "$TMP_DIR"

python3 -B "$SKILL_DIR/scripts/compile-custom-tooling.py" \
  "$SKILL_DIR/scripts/fixtures/release-notes-skill.json" \
  --output "$TMP_DIR/release-notes.md"

python3 -B "$SKILL_DIR/scripts/compile-custom-tooling.py" \
  "$SKILL_DIR/scripts/fixtures/deploy-check-command.json" \
  --output "$TMP_DIR/deploy-check.md"

python3 - "$TMP_DIR/release-notes.md" "$SKILL_DIR/scripts/fixtures/expected-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

generated = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["release-notes.md"]
missing = [fragment for fragment in fragments if fragment not in generated]
if missing:
    raise SystemExit("missing generated fragments: " + ", ".join(missing))
PY

python3 - "$SKILL_DIR/scripts/compile-custom-tooling.py" <<'PY'
import sys
from pathlib import Path

source = Path(sys.argv[1]).read_text(encoding="utf-8")
compile(source, sys.argv[1], "exec")
PY

for fixture in \
  invalid-user-scope-team.json \
  invalid-skill-without-fork.json \
  invalid-unrestricted-tools.json \
  invalid-command-contextual.json
do
  if python3 -B "$SKILL_DIR/scripts/compile-custom-tooling.py" "$SKILL_DIR/scripts/fixtures/$fixture" >"$TMP_DIR/$fixture.out" 2>&1; then
    echo "ERROR: invalid fixture passed: $fixture" >&2
    cat "$TMP_DIR/$fixture.out" >&2
    exit 1
  fi
done

bash -n "$SKILL_DIR/scripts/check.sh"
echo "OK: custom-tooling-extension scripts are deterministic"
