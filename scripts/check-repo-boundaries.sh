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

if git ls-files | grep -E '(^|/)\.codex/' >/dev/null; then
  fail "tracked .codex state detected"
fi

if git ls-files | grep -E '^workspace/' | grep -v '^workspace/\.gitkeep$' >/dev/null; then
  fail "tracked workspace state detected outside workspace/.gitkeep"
fi

USER_CONTEXT_ALLOWED='^user-context/(\.gitignore|\.jm-adk-context\.json|README\.md|AGENTS\.md|_INDICE\.md|manifest\.example\.json|context/README\.md|context/\.gitkeep|preferences/README\.md|preferences/\.gitkeep|memory/README\.md|memory/\.gitkeep|sources/README\.md|sources/\.gitkeep|resources/README\.md|resources/\.gitkeep|personal-skills/README\.md|personal-skills/_INDICE\.md|personal-skills/\.jm-adk-personal-skills\.json|personal-skills/skills/\.gitkeep|schemas/README\.md|schemas/[^/]+\.schema\.json)$'
if git ls-files user-context | grep -Ev "$USER_CONTEXT_ALLOWED" >/dev/null; then
  fail "tracked private user-context content detected"
fi

if git ls-files user-context/resources | grep -Ev '^user-context/resources/(README\.md|\.gitkeep)$' >/dev/null; then
  fail "tracked private user resources detected"
fi

if git ls-files user-context/personal-skills/skills | grep -v '^user-context/personal-skills/skills/\.gitkeep$' >/dev/null; then
  fail "tracked private personal skills detected"
fi

if find . -path './.git' -prune -o -type d \( -name 'jm-adk-alfa' -o -name 'jm-agentic-development-kit' \) -print | grep . >/dev/null; then
  fail "clone-like directory detected inside repo"
fi

# Placement guard must remain installed (anti-regression: prevents silent return
# to advisory-only placement discipline).
[ -f scripts/artifact-placement-guard.sh ] || fail "artifact-placement-guard.sh missing"
[ -f references/guardrails/placement-policy.json ] || fail "placement-policy.json missing"
grep -q 'artifact-placement-guard.sh' hooks/hooks.json || fail "placement guard not registered in hooks.json"

# User context repo identity must remain explicit and private-by-default.
[ -f user-context/.jm-adk-context.json ] || fail "user-context marker missing"
[ -f user-context/personal-skills/.jm-adk-personal-skills.json ] || fail "personal skills marker missing"
[ -f references/ontology/user-context-contract.md ] || fail "user-context contract missing"
grep -q 'jm-adk-user-context' user-context/.jm-adk-context.json || fail "user-context marker kind missing"
grep -q 'jm-adk-personal-skills' user-context/personal-skills/.jm-adk-personal-skills.json || fail "personal skills marker kind missing"
grep -q 'context_repo_globs' references/guardrails/placement-policy.json || fail "user-context placement policy missing"

if ! python3 scripts/validate-runtime-instructions.py >/tmp/jm-adk-runtime-instructions.log 2>&1; then
  fail "runtime instruction mirrors are not homologated"
  sed 's/^/  /' /tmp/jm-adk-runtime-instructions.log >&2 || true
fi

# Naming standard + contract must remain installed.
[ -f scripts/lib/naming.sh ] || fail "scripts/lib/naming.sh missing"
[ -f references/ontology/placement-naming-contract.md ] || fail "placement-naming-contract.md missing"
grep -q '"naming"' references/guardrails/placement-policy.json || fail "naming block missing from placement-policy.json"

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi

printf 'Repo boundaries OK\n'
