#!/bin/bash
# test-placement-guard.sh — smoke tests for artifact-placement-guard.sh
# Asserts the three-bucket classification and the maintainer-mode gate.
set -uo pipefail

ROOT="$(git -C "$(dirname "$0")/../.." rev-parse --show-toplevel)"
GUARD="$ROOT/scripts/artifact-placement-guard.sh"
PASS=0; FAIL=0

# run <expected_exit> <tool> <json_input> <mode> <label>
run() {
  local exp="$1" tool="$2" inp="$3" mode="$4" label="$5"
  local env_mode=""
  [ "$mode" = "maintainer" ] && env_mode="maintainer"
  CLAUDE_TOOL_NAME="$tool" CLAUDE_TOOL_INPUT="$inp" JM_ADK_MODE="$env_mode" \
    bash "$GUARD" >/dev/null 2>&1
  local got=$?
  if [ "$got" = "$exp" ]; then
    echo "PASS: $label (exit $got)"; PASS=$((PASS+1))
  else
    echo "FAIL: $label (expected $exp, got $got)"; FAIL=$((FAIL+1))
  fi
}

A="$(bash "$ROOT/scripts/workspace-manager.sh" ensure "placement guard test" 2>/dev/null | grep -oE 'workspace/[^ ]*' | head -1)"
WS="$(grep -o '"activeWorkspace"[^,]*' "$ROOT/workspace/.workspace-registry.json" | sed 's/.*: *"//; s/"//')"

run 0 Bash   '{"command":"ls"}'                                          task       "non-write tool ignored"
run 0 Write  "{\"file_path\":\"$ROOT/workspace/$WS/artifacts/out.md\"}"  task       "workspace artifact allowed"
run 2 Write  "{\"file_path\":\"$ROOT/skills/foo/SKILL.md\"}"             task       "kit path blocked in task mode"
run 0 Write  "{\"file_path\":\"$ROOT/skills/foo/SKILL.md\"}"             maintainer "kit path allowed in maintainer mode"
run 2 Write  "{\"file_path\":\"$ROOT/random-output.txt\"}"               task       "ad-hoc root file blocked + routed"
run 2 Write  "{\"file_path\":\"$ROOT/output/report.pdf\"}"               task       "ad-hoc nested file blocked + routed"
run 0 Write  '{"file_path":"/Users/someone/elsewhere/note.md"}'          task       "write outside repo root ignored"
run 2 Write  "{\"file_path\":\"$ROOT/workspace/$WS/artifacts/Bad Name.md\"}" task    "new non-kebab filename blocked (naming)"
run 0 Write  "{\"file_path\":\"$ROOT/workspace/$WS/artifacts/good-name.md\"}" task    "new kebab filename allowed"
run 2 Write  "{\"file_path\":\"$ROOT/workspace/$WS/loose-note.md\"}"      task       "deliverable at task root routed to artifacts/"
run 0 Write  "{\"file_path\":\"$ROOT/workspace/$WS/plan.md\"}"            task       "canonical task file allowed"

echo "---"
echo "RESULT: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
