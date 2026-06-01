#!/usr/bin/env bash
# Runtime checks for functional-toolbelt deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

input="$script_dir/fixtures/toolbelt-input.json"
invalid="$script_dir/fixtures/invalid-missing-traceability.json"
expected="$script_dir/fixtures/expected-report-fragments.json"
output="$tmp_dir/functional-toolbelt-report.md"

python3 -m json.tool "$input" >/dev/null
python3 -m json.tool "$invalid" >/dev/null
python3 -m json.tool "$expected" >/dev/null
python3 -m json.tool "$script_dir/../assets/manifest.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/toolbelt-tools.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/traceability-matrix-schema.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/anti-pattern-rules.json" >/dev/null

python3 "$script_dir/compile-functional-toolbelt.py" --input "$input" --output "$output"

python3 - "$output" "$expected" <<'PY'
import json
import sys

text = open(sys.argv[1], encoding="utf-8").read()
fragments = json.load(open(sys.argv[2], encoding="utf-8"))["required_fragments"]
missing = [fragment for fragment in fragments if fragment not in text]
if missing:
    raise SystemExit(f"missing report fragment(s): {missing}")
for section in [
    "Tool 1: Event Storming",
    "Tool 2: Story Mapping",
    "Tool 3: Business Rule Extraction",
    "Tool 4: Acceptance Criteria",
    "Tool 5: Traceability Matrix",
    "Tool 6: Anti-Pattern Detection",
]:
    if section not in text:
        raise SystemExit(f"missing section: {section}")
PY

if python3 "$script_dir/compile-functional-toolbelt.py" --input "$invalid" >/dev/null 2>&1; then
  echo "ERROR: invalid functional toolbelt input should fail" >&2
  exit 1
fi

echo "OK: functional-toolbelt scripts are deterministic"
