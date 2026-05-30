#!/bin/bash
# PreToolUse hook: block dangerous commands before execution (Kata 02).
# Exit code 2 = block the tool call (deterministic deny). Exit code 0 = allow.
#
# Policy is hot-reloaded from references/guardrails/tool-policy.json on every call,
# so critical rules live in code/config, not in the system prompt. If the policy
# file or python3 is unavailable, a hardcoded fallback still blocks the worst cases.

TOOL_NAME="${CLAUDE_TOOL_NAME:-}"
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
POLICY_FILE="$SCRIPT_DIR/../references/guardrails/tool-policy.json"

# Policy-driven path (preferred): evaluate via python3 against the JSON policy.
if command -v python3 >/dev/null 2>&1 && [ -f "$POLICY_FILE" ]; then
  decision="$(
    CLAUDE_TOOL_NAME="$TOOL_NAME" CLAUDE_TOOL_INPUT="$TOOL_INPUT" POLICY_FILE="$POLICY_FILE" \
    python3 - <<'PY'
import json, os, re, sys

tool = os.environ.get("CLAUDE_TOOL_NAME", "")
data = os.environ.get("CLAUDE_TOOL_INPUT", "")
policy_file = os.environ.get("POLICY_FILE", "")

try:
    with open(policy_file, encoding="utf-8") as fh:
        policy = json.load(fh)
except Exception:
    print("OK")
    sys.exit(0)

write_tools = set(policy.get("write_tools", []))

# Dangerous Bash command patterns -> hard deny.
if tool == "Bash":
    for pattern in policy.get("deny_bash_patterns", []):
        try:
            if re.search(pattern, data, re.IGNORECASE):
                print("DENY:dangerous command matches policy pattern '%s'" % pattern)
                sys.exit(0)
        except re.error:
            continue

# Protected paths -> deny writes, warn elsewhere.
for needle in policy.get("protected_path_substrings", []):
    if needle and needle in data:
        if tool in write_tools:
            print("DENY:write to protected path '%s' is blocked by policy" % needle)
            sys.exit(0)

# Sensitive file access -> warn but allow.
for needle in policy.get("sensitive_warn_substrings", []):
    if needle and needle.lower() in data.lower():
        print("WARN:accessing sensitive pattern '%s'" % needle)
        sys.exit(0)

print("OK")
PY
  )"
  case "$decision" in
    DENY:*)
      echo "BLOCKED: ${decision#DENY:}" >&2
      exit 2
      ;;
    WARN:*)
      echo "WARNING: ${decision#WARN:}" >&2
      exit 0
      ;;
    *)
      exit 0
      ;;
  esac
fi

# Fallback (policy file or python3 unavailable): minimal hardcoded guard.
if [ "$TOOL_NAME" != "Bash" ]; then
  exit 0
fi

DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "git reset --hard"
  "git push --force"
  "git push -f"
  "git clean -fd"
  "mkfs\\."
  "dd if="
)
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$TOOL_INPUT" | grep -qiE "$pattern"; then
    echo "BLOCKED: dangerous command detected — '$pattern'" >&2
    exit 2
  fi
done

exit 0
