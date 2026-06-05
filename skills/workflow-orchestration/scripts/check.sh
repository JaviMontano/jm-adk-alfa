#!/usr/bin/env bash
# Runtime checks for workflow-orchestration deterministic scripts.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

export PYTHONPYCACHEPREFIX="$tmp_dir/pycache"

product_input="$script_dir/fixtures/product-launch-orchestration.json"
incident_input="$script_dir/fixtures/incident-recovery-orchestration.json"
invalid_input="$script_dir/fixtures/invalid-no-resume-orchestration.json"
expected_fragments="$script_dir/fixtures/expected-report-fragments.json"

python3 -m json.tool "$script_dir/../assets/orchestration-schema.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/checkpoint-policy.json" >/dev/null
python3 -m json.tool "$script_dir/../assets/resume-policy.json" >/dev/null
python3 -m json.tool "$product_input" >/dev/null
python3 -m json.tool "$incident_input" >/dev/null
python3 -m json.tool "$invalid_input" >/dev/null
python3 -m json.tool "$expected_fragments" >/dev/null
python3 -m py_compile "$script_dir/compile-orchestration-plan.py"

product_output="$tmp_dir/product.md"
incident_output="$tmp_dir/incident.md"
python3 "$script_dir/compile-orchestration-plan.py" --input "$product_input" --output "$product_output"
python3 "$script_dir/compile-orchestration-plan.py" --input "$incident_input" --output "$incident_output"

python3 - "$expected_fragments" "$product_output" "$incident_output" <<'PY'
import json
import sys
from pathlib import Path

fragments = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
product = Path(sys.argv[2]).read_text(encoding="utf-8")
incident = Path(sys.argv[3]).read_text(encoding="utf-8")
for fragment in fragments["product"]:
    if fragment not in product:
        raise SystemExit(f"missing product fragment: {fragment}")
for fragment in fragments["incident"]:
    if fragment not in incident:
        raise SystemExit(f"missing incident fragment: {fragment}")
PY

if python3 "$script_dir/compile-orchestration-plan.py" --input "$invalid_input" >/dev/null 2>&1; then
  echo "ERROR: invalid orchestration should fail" >&2
  exit 1
fi

echo "OK: workflow-orchestration scripts are deterministic"
