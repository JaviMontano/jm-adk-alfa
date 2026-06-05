#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/bmad-method"
SCRIPT="$SKILL_DIR/scripts/validate_bmad_packet.py"
CONTRACT="$SKILL_DIR/assets/bmad-packet-contract.json"

python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-greenfield-packet.md" --scenario greenfield --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-quick-flow-packet.md" --scenario quick-flow --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/invalid-gate-fail-packet.md" --scenario gate-fail --expect fail >/dev/null

echo "OK: bmad-method packets validated"
