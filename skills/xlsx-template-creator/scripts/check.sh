#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/xlsx-template-creator"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/xlsx-template-schema.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/template-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/formula-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/tracking-matrix.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/metrics-dashboard.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-unguarded-formula.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-dropdown-source.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/expected-report-fragments.json" >/dev/null

python3 -m py_compile "$SKILL_DIR/scripts/compile-xlsx-template.py"

python3 "$SKILL_DIR/scripts/compile-xlsx-template.py" \
  --input "$SKILL_DIR/scripts/fixtures/tracking-matrix.json" \
  --format markdown \
  --output "$TMP_DIR/tracking.md"

python3 "$SKILL_DIR/scripts/compile-xlsx-template.py" \
  --input "$SKILL_DIR/scripts/fixtures/metrics-dashboard.json" \
  --format yaml \
  --output "$TMP_DIR/dashboard.yml"

python3 - "$SKILL_DIR/scripts/fixtures/expected-report-fragments.json" "$TMP_DIR/tracking.md" "$TMP_DIR/dashboard.yml" <<'PY'
import json
import sys
from pathlib import Path

expected = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
tracking = Path(sys.argv[2]).read_text(encoding="utf-8")
dashboard = Path(sys.argv[3]).read_text(encoding="utf-8")
for fragment in expected["tracking_markdown"]:
    if fragment not in tracking:
        raise SystemExit(f"missing tracking fragment: {fragment}")
for fragment in expected["dashboard_yaml"]:
    if fragment not in dashboard:
        raise SystemExit(f"missing dashboard fragment: {fragment}")
PY

if python3 "$SKILL_DIR/scripts/compile-xlsx-template.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-unguarded-formula.json" \
  --format markdown >/dev/null 2>"$TMP_DIR/invalid-formula.err"; then
  echo "ERROR: invalid-unguarded-formula fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "formula with division requires IF guard" "$TMP_DIR/invalid-formula.err"

if python3 "$SKILL_DIR/scripts/compile-xlsx-template.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-dropdown-source.json" \
  --format markdown >/dev/null 2>"$TMP_DIR/invalid-dropdown.err"; then
  echo "ERROR: invalid-dropdown-source fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "dropdown source must reference Config or named range" "$TMP_DIR/invalid-dropdown.err"

echo "OK: xlsx-template-creator scripts are deterministic"
