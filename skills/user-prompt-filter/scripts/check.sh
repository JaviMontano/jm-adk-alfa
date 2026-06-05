#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/user-prompt-filter/scripts/filter-prompt.py"
FIXTURES="$ROOT_DIR/skills/user-prompt-filter/scripts/fixtures"
OUT="$(mktemp "${TMPDIR:-/tmp}/user-prompt-filter-check.XXXXXX")"

python3 "$SCRIPT" --input "$FIXTURES/prompt-injection.json" --output "$OUT"
python3 "$SCRIPT" --input "$FIXTURES/benign-summary.json" --format json > "$OUT.json"
python3 "$SCRIPT" --input "$FIXTURES/secret-exfiltration.json" --format json > "$OUT.secret.json"
python3 "$SCRIPT" --input "$FIXTURES/ambiguous-authority.json" --format json > "$OUT.authority.json"

python3 - "$OUT" "$OUT.json" "$OUT.secret.json" "$OUT.authority.json" "$FIXTURES/expected-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

markdown = Path(sys.argv[1]).read_text(encoding="utf-8")
benign = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
secret = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
authority = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
fragments = json.loads(Path(sys.argv[5]).read_text(encoding="utf-8"))

missing = [fragment for fragment in fragments["prompt_injection"] if fragment not in markdown]
if missing:
    print("missing prompt injection fragments:", missing)
    raise SystemExit(1)

if benign["decision"] != "allow":
    print("benign prompt should be allowed")
    raise SystemExit(1)

if secret["decision"] != "block" or "[REDACTED]" not in json.dumps(secret):
    print("secret exfiltration should be blocked and redacted")
    raise SystemExit(1)

if authority["decision"] != "escalate":
    print("ambiguous authority should escalate")
    raise SystemExit(1)
PY

if python3 "$SCRIPT" --input "$FIXTURES/invalid-missing-prompt.json" >/dev/null 2>&1; then
  echo "invalid missing prompt fixture unexpectedly passed" >&2
  exit 1
fi

echo "user-prompt-filter fixtures passed"
