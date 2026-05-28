#!/bin/bash
# post-tool-check.sh v4.0.0 — PostToolUse hook
#
# Delegates to workspace-manager.sh log → single write path for tasklog.
# Filters read-only tools (Read, Glob, Grep, etc.) which produce 80%+ of calls and bury signal.
# ~50ms overhead per call. Acceptable against 100ms–10s per tool call.

PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
SCRIPT_DIR="$PROJECT_ROOT/scripts"

[ ! -f "$PROJECT_ROOT/workspace/.workspace-registry.json" ] && exit 0

TOOL="${CLAUDE_TOOL_NAME:-}"
case "$TOOL" in Read|Glob|Grep|TodoWrite|TaskOutput|WebSearch|WebFetch|AskUserQuestion|"") exit 0;; esac

bash "$SCRIPT_DIR/workspace-manager.sh" log "$TOOL" "${CLAUDE_TOOL_INPUT:-}" 2>/dev/null
exit 0
