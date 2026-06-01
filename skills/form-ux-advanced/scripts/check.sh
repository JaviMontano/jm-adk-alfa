#!/usr/bin/env bash
# Runtime checks for form-ux-advanced deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

journey="$script_dir/fixtures/intake-journey.json"
invalid="$script_dir/fixtures/invalid-missing-recovery.json"
expected="$script_dir/fixtures/expected-audit-fragments.json"
output="$tmp_dir/form-ux-audit.md"

python3 -m json.tool "$journey" >/dev/null
python3 -m json.tool "$invalid" >/dev/null
python3 -m json.tool "$expected" >/dev/null
python3 -m json.tool "$script_dir/../assets/manifest.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/ux-heuristics.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/inline-validation-copy.json" >/dev/null

python3 "$script_dir/audit-form-ux.py" --journey "$journey" --output "$output"

python3 - "$output" "$expected" <<'PY'
import json
import sys

text = open(sys.argv[1], encoding="utf-8").read()
fragments = json.load(open(sys.argv[2], encoding="utf-8"))["required_fragments"]
missing = [fragment for fragment in fragments if fragment not in text]
if missing:
    raise SystemExit(f"missing audit fragment(s): {missing}")
for required in ["Score:", "Rating:", "Findings", "Recommended Assets"]:
    if required not in text:
        raise SystemExit(f"missing section: {required}")
PY

if python3 "$script_dir/audit-form-ux.py" --journey "$invalid" >/dev/null 2>&1; then
  echo "ERROR: invalid form UX journey should fail" >&2
  exit 1
fi

echo "OK: form-ux-advanced scripts are deterministic"
