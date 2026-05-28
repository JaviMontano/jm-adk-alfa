#!/usr/bin/env bash
# Validate repo boundaries and local-state safety.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

ERRORS=0

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  ERRORS=$((ERRORS + 1))
}

while IFS= read -r path; do
  [ "$path" = "./.git" ] && continue
  fail "nested git repository detected: ${path#./}"
done < <(find . -path './.git' -prune -o -name .git -type d -print)

if git ls-files | grep -E '(^|/)\.env($|\.)' >/dev/null; then
  fail "tracked .env-like file detected"
fi

if git ls-files | grep -E '(^|/)\.jm-adk\.local\.json$' >/dev/null; then
  fail "tracked .jm-adk.local.json detected"
fi

if git ls-files | grep -E '(^|/)\.local/' >/dev/null; then
  fail "tracked .local state detected"
fi

if git ls-files | grep -E '^workspace/' | grep -v '^workspace/\.gitkeep$' >/dev/null; then
  fail "tracked workspace state detected outside workspace/.gitkeep"
fi

if find . -path './.git' -prune -o -type d \( -name 'jm-adk-alfa' -o -name 'jm-agentic-development-kit' \) -print | grep . >/dev/null; then
  fail "clone-like directory detected inside repo"
fi

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi

printf 'Repo boundaries OK\n'
