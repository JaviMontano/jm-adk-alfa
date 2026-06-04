#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/input-analyst"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/input-analysis.md"
JSON_OUT="$TMP_DIR/input-analysis.json"

python3 "$SKILL_DIR/scripts/compile-input-analysis.py" \
  --input "$SKILL_DIR/scripts/fixtures/input-analysis-input.json" \
  --output "$OUT"

python3 "$SKILL_DIR/scripts/compile-input-analysis.py" \
  --input "$SKILL_DIR/scripts/fixtures/input-analysis-input.json" \
  --json \
  --output "$JSON_OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-analysis-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

python3 - "$JSON_OUT" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
required = {
    "surface_errors",
    "five_whys",
    "seven_so_whats",
    "intent_gap_analysis",
    "ambiguity_register",
    "actionability_score",
    "clarified_prompt",
    "routing_hints",
    "user_safety_privacy_flags",
    "confidence",
}
missing = sorted(required - set(data))
if missing:
    raise SystemExit(f"missing JSON sections: {missing}")
if data["user_safety_privacy_flags"]["external_api_required"]:
    raise SystemExit("external_api_required must be false")
PY

if python3 "$SKILL_DIR/scripts/compile-input-analysis.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-empty-input.json" \
  >"$TMP_DIR/invalid-empty.out" 2>"$TMP_DIR/invalid-empty.err"; then
  echo "ERROR: invalid empty-input fixture unexpectedly passed" >&2
  exit 1
fi
grep -q "raw_input must not be empty" "$TMP_DIR/invalid-empty.err"

if python3 "$SKILL_DIR/scripts/compile-input-analysis.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-external-routing.json" \
  >"$TMP_DIR/invalid-routing.out" 2>"$TMP_DIR/invalid-routing.err"; then
  echo "ERROR: invalid external-routing fixture unexpectedly passed" >&2
  exit 1
fi
grep -q "offline_only=true and allow_external_apis=false" "$TMP_DIR/invalid-routing.err"

echo "OK: input-analyst scripts are deterministic and offline"
