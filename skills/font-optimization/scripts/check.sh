#!/usr/bin/env bash
# Runtime checks for font-optimization deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

bad="$script_dir/fixtures/bad-font-loading.html"
good="$script_dir/fixtures/good-font-loading.html"
expected_bad="$script_dir/fixtures/expected-bad-findings.json"
expected_good="$script_dir/fixtures/expected-good-summary.json"
report="$tmp_dir/report.json"

python3 -m json.tool "$script_dir/../assets/font-budget.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/manifest.json" >/dev/null
python3 -m json.tool "$expected_bad" >/dev/null
python3 -m json.tool "$expected_good" >/dev/null

if python3 "$script_dir/audit-font-loading.py" "$bad" >/dev/null 2>&1; then
  echo "ERROR: bad fixture should fail font audit" >&2
  exit 1
fi

python3 "$script_dir/audit-font-loading.py" "$bad" --json > "$report" || true
python3 - "$report" "$expected_bad" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
expected = json.load(open(sys.argv[2], encoding="utf-8"))["required_codes"]
codes = {finding["code"] for item in data["files"] for finding in item["findings"]}
required = set(expected)
missing = sorted(required - codes)
if missing:
    raise SystemExit(f"missing expected finding codes: {missing}")
PY

python3 "$script_dir/audit-font-loading.py" "$good" --json > "$report"
python3 - "$report" "$expected_good" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
expected = json.load(open(sys.argv[2], encoding="utf-8"))
if data["finding_count"] != expected["finding_count"]:
    raise SystemExit(f"expected 0 findings, got {data['finding_count']}")
item = data["files"][0]
if item["font_face_count"] != expected["font_face_count"]:
    raise SystemExit("unexpected font_face_count")
if item["preload_count"] != expected["preload_count"]:
    raise SystemExit("unexpected preload_count")
if item["woff2_count"] < expected["woff2_count_min"]:
    raise SystemExit("unexpected woff2_count")
PY

echo "OK: font-optimization scripts are deterministic"
