#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/brand-html"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

SCRIPT="$SKILL_DIR/scripts/validate_brand_html.py"
CONTRACT="$SKILL_DIR/assets/brand-html-contract.json"
EVIDENCE="$SKILL_DIR/assets/evidence-policy.json"
FAVICON="$SKILL_DIR/assets/favicon.svg"

python3 -m json.tool "$SKILL_DIR/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/favicon-policy.json" >/dev/null
python3 -m json.tool "$EVIDENCE" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/fallback-brand-config.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/fixture-manifest.json" >/dev/null

python3 -m py_compile "$SCRIPT"
grep -q '<svg' "$FAVICON"
grep -q 'viewBox="0 0 32 32"' "$FAVICON"

python3 -B "$SCRIPT" --contract "$CONTRACT" --html "$SKILL_DIR/scripts/fixtures/valid-landing.html" --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --html "$SKILL_DIR/scripts/fixtures/valid-rtl.html" --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --html "$SKILL_DIR/scripts/fixtures/invalid-hardcoded-color.html" --expect fail >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --html "$SKILL_DIR/scripts/fixtures/invalid-low-contrast.html" --expect fail >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --html "$SKILL_DIR/scripts/fixtures/invalid-external-dependency.html" --expect fail >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --html "$SKILL_DIR/scripts/fixtures/invalid-favicon.html" --expect fail >/dev/null

echo "OK: brand-html artifacts validated deterministically"
