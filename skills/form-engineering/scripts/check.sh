#!/usr/bin/env bash
# Runtime checks for form-engineering deterministic scripts.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

spec="$script_dir/fixtures/enterprise-intake-spec.json"
invalid="$script_dir/fixtures/invalid-missing-server-validation.json"
expected="$script_dir/fixtures/expected-contract-fragments.json"
output="$tmp_dir/form-engineering-contract.md"

python3 -m json.tool "$spec" >/dev/null
python3 -m json.tool "$invalid" >/dev/null
python3 -m json.tool "$expected" >/dev/null
python3 -m json.tool "$script_dir/../assets/manifest.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/form-engineering-policy.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/error-message-patterns.json" >/dev/null

python3 "$script_dir/compile-form-contract.py" --spec "$spec" --output "$output"

python3 - "$output" "$expected" <<'PY'
import json
import sys

text = open(sys.argv[1], encoding="utf-8").read()
fragments = json.load(open(sys.argv[2], encoding="utf-8"))["required_fragments"]
missing = [fragment for fragment in fragments if fragment not in text]
if missing:
    raise SystemExit(f"missing contract fragment(s): {missing}")
for required in ["Validation Parity", "Accessibility Hooks", "Optimistic Submission", "Asset Hooks"]:
    if required not in text:
        raise SystemExit(f"missing section: {required}")
PY

if python3 "$script_dir/compile-form-contract.py" --spec "$invalid" >/dev/null 2>&1; then
  echo "ERROR: invalid form engineering spec should fail" >&2
  exit 1
fi

echo "OK: form-engineering scripts are deterministic"
