#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/adaptive-investigation-method"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/investigation-schema.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/investigation-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/auth-repo-investigation.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/corpus-investigation.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-no-budget.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-reflexive-replan.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/expected-report-fragments.json" >/dev/null

python3 -m py_compile "$SKILL_DIR/scripts/compile-adaptive-investigation.py"

python3 "$SKILL_DIR/scripts/compile-adaptive-investigation.py" \
  --input "$SKILL_DIR/scripts/fixtures/auth-repo-investigation.json" \
  --format markdown \
  --output "$TMP_DIR/auth.md"

python3 "$SKILL_DIR/scripts/compile-adaptive-investigation.py" \
  --input "$SKILL_DIR/scripts/fixtures/corpus-investigation.json" \
  --format json \
  --output "$TMP_DIR/corpus.json"

python3 - "$SKILL_DIR/scripts/fixtures/expected-report-fragments.json" "$TMP_DIR/auth.md" "$TMP_DIR/corpus.json" <<'PY'
import json
import sys
from pathlib import Path

expected = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
auth = Path(sys.argv[2]).read_text(encoding="utf-8")
corpus = Path(sys.argv[3]).read_text(encoding="utf-8")
for fragment in expected["auth_markdown"]:
    if fragment not in auth:
        raise SystemExit(f"missing auth fragment: {fragment}")
for fragment in expected["corpus_json"]:
    if fragment not in corpus:
        raise SystemExit(f"missing corpus fragment: {fragment}")
PY

if python3 "$SKILL_DIR/scripts/compile-adaptive-investigation.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-no-budget.json" \
  --format markdown >/dev/null 2>"$TMP_DIR/no-budget.err"; then
  echo "ERROR: invalid-no-budget fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "budget missing required field: total" "$TMP_DIR/no-budget.err"

if python3 "$SKILL_DIR/scripts/compile-adaptive-investigation.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-reflexive-replan.json" \
  --format markdown >/dev/null 2>"$TMP_DIR/reflexive.err"; then
  echo "ERROR: invalid-reflexive-replan fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "replan only allowed on hypothesis_invalidated" "$TMP_DIR/reflexive.err"

echo "OK: adaptive-investigation-method scripts are deterministic"
