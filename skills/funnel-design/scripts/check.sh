#!/usr/bin/env bash
# Runtime checks for funnel-design deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

input="$script_dir/fixtures/funnel-design-input.json"
invalid="$script_dir/fixtures/invalid-missing-bofu.json"
expected="$script_dir/fixtures/expected-report-fragments.json"
output="$tmp_dir/funnel-design-report.md"

python3 -m json.tool "$input" >/dev/null
python3 -m json.tool "$invalid" >/dev/null
python3 -m json.tool "$expected" >/dev/null
python3 -m json.tool "$script_dir/../assets/manifest.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/funnel-design-schema.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/stage-content-model.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/lead-scoring-model.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/nurture-flow-schema.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/qualification-rules.json" >/dev/null

python3 "$script_dir/compile-funnel-design.py" --input "$input" --output "$output"

python3 - "$output" "$expected" <<'PY'
import json
import sys

text = open(sys.argv[1], encoding="utf-8").read()
fragments = json.load(open(sys.argv[2], encoding="utf-8"))["required_fragments"]
missing = [fragment for fragment in fragments if fragment not in text]
if missing:
    raise SystemExit(f"missing report fragment(s): {missing}")
for section in [
    "## Stage Content Map",
    "## Lead Scoring",
    "## Nurture Flow",
    "## Handoff Rules",
]:
    if section not in text:
        raise SystemExit(f"missing section: {section}")
PY

if python3 "$script_dir/compile-funnel-design.py" --input "$invalid" >/dev/null 2>&1; then
  echo "ERROR: invalid funnel design input should fail" >&2
  exit 1
fi

echo "OK: funnel-design scripts are deterministic"
