#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/brand-docx"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

SCRIPT="$SKILL_DIR/scripts/validate_brand_docx.py"
CONTRACT="$SKILL_DIR/assets/brand-docx-contract.json"

python3 -m json.tool "$SKILL_DIR/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/evidence-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/fallback-brand-config.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/style-token-map.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/fixture-manifest.json" >/dev/null

python3 -m py_compile "$SCRIPT"

python3 -B "$SCRIPT" --contract "$CONTRACT" --fixture "$SKILL_DIR/scripts/fixtures/valid-proposal.json" --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --fixture "$SKILL_DIR/scripts/fixtures/valid-fallback.json" --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --fixture "$SKILL_DIR/scripts/fixtures/valid-long-table.json" --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --fixture "$SKILL_DIR/scripts/fixtures/invalid-html-renamed.json" --expect fail >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --fixture "$SKILL_DIR/scripts/fixtures/invalid-remote-assets.json" --expect fail >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --fixture "$SKILL_DIR/scripts/fixtures/invalid-unresolved-placeholder.json" --expect fail >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --fixture "$SKILL_DIR/scripts/fixtures/invalid-hardcoded-token.json" --expect fail >/dev/null

echo "OK: brand-docx artifacts validated deterministically"
