#!/usr/bin/env bash
# Runtime checks for folio-generator deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

fixture="$script_dir/fixtures/tracker.json"
expected_json="$script_dir/fixtures/expected-next-cot-2026.json"
tracker="$tmp_dir/tracker.json"
before="$tmp_dir/before.json"

python3 -m json.tool "$fixture" >/dev/null
python3 -m json.tool "$expected_json" >/dev/null
cp "$fixture" "$tracker"
cp "$fixture" "$before"

expected="$(python3 - "$expected_json" <<'PY'
import json
import sys

print(json.load(open(sys.argv[1], encoding="utf-8"))["expected_folio"])
PY
)"

actual="$(bash "$script_dir/next-folio-number.sh" --dry-run --date 2026-05-31 --tracker "$tracker" COT)"
if [ "$actual" != "$expected" ]; then
  echo "ERROR: dry-run expected $expected, got $actual" >&2
  exit 1
fi

if ! cmp -s "$before" "$tracker"; then
  echo "ERROR: dry-run mutated tracker" >&2
  exit 1
fi

applied="$(bash "$script_dir/next-folio-number.sh" --apply --date 2026-05-31 --tracker "$tracker" COT)"
if [ "$applied" != "$expected" ]; then
  echo "ERROR: apply expected $expected, got $applied" >&2
  exit 1
fi

python3 - "$tracker" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["folios"]["COT"]["2026"] == 43
assert data["last_updated"]
PY

rendered="$tmp_dir/rendered.html"
python3 "$script_dir/render-folio-html.py" \
  --data "$script_dir/fixtures/render-data.json" \
  --output "$rendered"

python3 - "$rendered" "$script_dir/fixtures/expected-render-fragments.json" <<'PY'
import json
import sys

html = open(sys.argv[1], encoding="utf-8").read()
fragments = json.load(open(sys.argv[2], encoding="utf-8"))["required_fragments"]
missing = [fragment for fragment in fragments if fragment not in html]
if missing:
    raise SystemExit(f"missing rendered fragment(s): {missing}")
PY

if bash "$script_dir/next-folio-number.sh" --dry-run --date 2026-05-31 --tracker "$tracker" cot >/dev/null 2>&1; then
  echo "ERROR: lowercase prefix should fail" >&2
  exit 1
fi

echo "OK: folio-generator scripts are deterministic"
