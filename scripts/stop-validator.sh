#!/bin/bash
# stop-validator.sh v4.0.0 — Stop hook
#
# Marks session boundary in tasklog. Does not write summaries (model's job).
# Updates .workspace.json timestamp and .jm-adk.json lastSession (best-effort).

PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
REG="$PROJECT_ROOT/workspace/.workspace-registry.json"

[ ! -f "$REG" ] && { echo "STOP: no-workspace-system" >&2; exit 0; }

A=$(grep -o '"activeWorkspace"[[:space:]]*:[[:space:]]*"[^"]*"' "$REG" 2>/dev/null | \
  sed 's/.*"activeWorkspace"[[:space:]]*:[[:space:]]*"//' | sed 's/"//') || true
[ -z "$A" ] || [ "$A" = "null" ] && { echo "STOP: no-active-workspace" >&2; exit 0; }
[ ! -d "$PROJECT_ROOT/workspace/$A" ] && { echo "STOP: orphaned-workspace" >&2; exit 0; }

NOW_TIME=$(date +"%H:%M")
NOW_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TL="$PROJECT_ROOT/workspace/$A/tasklog.md"

if [ -f "$TL" ]; then
  ACTIONS=$(grep -c '^### ' "$TL" 2>/dev/null || echo "0")
  printf "\n---\n\n### %s — Session boundary\n- Actions logged: %s\n" "$NOW_TIME" "$ACTIONS" >> "$TL"
fi

# Best-effort timestamp updates
META="$PROJECT_ROOT/workspace/$A/.workspace.json"
[ -f "$META" ] && sed -i '' "s/\"updated\": \"[^\"]*\"/\"updated\": \"$NOW_ISO\"/" "$META" 2>/dev/null

CFG="$PROJECT_ROOT/.jm-adk.json"
[ -f "$CFG" ] && sed -i '' "s/\"date\": [^,]*/\"date\": \"$(date +%Y-%m-%d)\"/" "$CFG" 2>/dev/null

echo "STOP: workspace=$A actions=$ACTIONS" >&2
exit 0
