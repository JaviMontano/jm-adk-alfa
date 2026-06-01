#!/usr/bin/env bash
# Runtime checks for follow-up-email deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

fixture="$script_dir/fixtures/meeting-data.json"
expected="$script_dir/fixtures/expected-ana-fragments.json"

python3 -m json.tool "$fixture" >/dev/null
python3 -m json.tool "$expected" >/dev/null
python3 -m json.tool "$script_dir/../assets/manifest.json" >/dev/null

ana="$tmp_dir/ana.md"
carlos="$tmp_dir/carlos.md"
html="$tmp_dir/ana.html"

python3 "$script_dir/render-follow-up-email.py" \
  --data "$fixture" \
  --recipient "ana@example.com" \
  --output "$ana"

python3 "$script_dir/render-follow-up-email.py" \
  --data "$fixture" \
  --recipient "carlos@example.com" \
  --output "$carlos"

python3 "$script_dir/render-follow-up-email.py" \
  --data "$fixture" \
  --recipient "ana@example.com" \
  --format html \
  --output "$html"

python3 - "$ana" "$expected" <<'PY'
import json
import sys

body = open(sys.argv[1], encoding="utf-8").read()
fragments = json.load(open(sys.argv[2], encoding="utf-8"))["required_fragments"]
missing = [fragment for fragment in fragments if fragment not in body]
if missing:
    raise SystemExit(f"missing Ana fragment(s): {missing}")
if "Publicar dashboard de metricas" in body:
    raise SystemExit("privacy leak: Carlos action item appeared in Ana email")
PY

if grep -q "Preparar minuta ejecutiva" "$carlos"; then
  echo "ERROR: Ana action item leaked into Carlos email" >&2
  exit 1
fi

grep -q "<!DOCTYPE html>" "$html"
grep -q "Subject: Seguimiento: Q2 Planning" "$html"

if python3 "$script_dir/render-follow-up-email.py" --data "$fixture" --recipient "missing@example.com" >/dev/null 2>&1; then
  echo "ERROR: missing recipient should fail" >&2
  exit 1
fi

echo "OK: follow-up-email scripts are deterministic"
