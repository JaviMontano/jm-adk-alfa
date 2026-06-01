#!/usr/bin/env bash
# Runtime checks for form-builder deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

schema="$script_dir/fixtures/intake-form.json"
invalid="$script_dir/fixtures/invalid-form.json"
expected="$script_dir/fixtures/expected-render-fragments.json"
output="$tmp_dir/form.html"

python3 -m json.tool "$schema" >/dev/null
python3 -m json.tool "$invalid" >/dev/null
python3 -m json.tool "$expected" >/dev/null
python3 -m json.tool "$script_dir/../assets/manifest.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/validation-policy.json" >/dev/null

python3 "$script_dir/render-form-schema.py" --schema "$schema" --output "$output"

python3 - "$output" "$expected" <<'PY'
import json
import sys

html = open(sys.argv[1], encoding="utf-8").read()
fragments = json.load(open(sys.argv[2], encoding="utf-8"))["required_fragments"]
missing = [fragment for fragment in fragments if fragment not in html]
if missing:
    raise SystemExit(f"missing rendered fragment(s): {missing}")
if "<label" not in html or "<fieldset" not in html:
    raise SystemExit("rendered form must include labels and fieldsets")
PY

if python3 "$script_dir/render-form-schema.py" --schema "$invalid" >/dev/null 2>&1; then
  echo "ERROR: invalid form schema should fail" >&2
  exit 1
fi

echo "OK: form-builder scripts are deterministic"
