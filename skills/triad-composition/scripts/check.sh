#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$SKILL_DIR/scripts/validate_triad_packet.py"
CONTRACT="$SKILL_DIR/assets/triad-output-contract.json"

python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-requirements-packet.md" --scenario requirements --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-ambiguous-packet.md" --scenario ambiguous --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-missing-context-packet.md" --scenario missing-context --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-false-positive-packet.md" --scenario false-positive --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/invalid-no-guardian-packet.md" --scenario invalid-no-guardian --expect fail >/dev/null

echo "OK: triad-composition packets validated"
