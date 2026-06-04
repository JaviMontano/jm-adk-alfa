#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/x-ray-skill"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/rubric-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/gate-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/certified-skill.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/draft-skill.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-no-skill.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/expected-report-fragments.json" >/dev/null

python3 -m py_compile "$SKILL_DIR/scripts/compile-x-ray-report.py"

python3 "$SKILL_DIR/scripts/compile-x-ray-report.py" \
  --fixture "$SKILL_DIR/scripts/fixtures/certified-skill.json" \
  --format markdown \
  --output "$TMP_DIR/certified.md"

python3 "$SKILL_DIR/scripts/compile-x-ray-report.py" \
  --fixture "$SKILL_DIR/scripts/fixtures/certified-skill.json" \
  --format json \
  --output "$TMP_DIR/certified.json"

python3 "$SKILL_DIR/scripts/compile-x-ray-report.py" \
  --fixture "$SKILL_DIR/scripts/fixtures/draft-skill.json" \
  --format markdown \
  --output "$TMP_DIR/draft.md"

python3 "$SKILL_DIR/scripts/compile-x-ray-report.py" \
  --skill-dir "$SKILL_DIR" \
  --format markdown \
  --output "$TMP_DIR/self.md"

python3 - "$SKILL_DIR/scripts/fixtures/expected-report-fragments.json" "$TMP_DIR/certified.md" "$TMP_DIR/draft.md" "$TMP_DIR/self.md" "$TMP_DIR/certified.json" <<'PY'
import json
import sys
from pathlib import Path

expected = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
certified = Path(sys.argv[2]).read_text(encoding="utf-8")
draft = Path(sys.argv[3]).read_text(encoding="utf-8")
self_report = Path(sys.argv[4]).read_text(encoding="utf-8")
certified_json = Path(sys.argv[5]).read_text(encoding="utf-8")

for fragment in expected["certified_markdown"]:
    if fragment not in certified:
        raise SystemExit(f"missing certified markdown fragment: {fragment}")
for fragment in expected["draft_markdown"]:
    if fragment not in draft:
        raise SystemExit(f"missing draft markdown fragment: {fragment}")
for fragment in expected["self_markdown"]:
    if fragment not in self_report:
        raise SystemExit(f"missing self markdown fragment: {fragment}")
for fragment in expected["certified_json"]:
    if fragment not in certified_json:
        raise SystemExit(f"missing certified json fragment: {fragment}")
PY

if python3 "$SKILL_DIR/scripts/compile-x-ray-report.py" \
  --fixture "$SKILL_DIR/scripts/fixtures/invalid-no-skill.json" \
  --format markdown >/dev/null 2>"$TMP_DIR/no-skill.err"; then
  echo "ERROR: invalid-no-skill fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "SKILL.md not found at skill root" "$TMP_DIR/no-skill.err"

echo "OK: x-ray-skill scripts are deterministic"
