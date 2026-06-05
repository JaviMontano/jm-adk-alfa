#!/usr/bin/env bash
# Deterministic script contract check for cv-cover-optimizer.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 -m json.tool "$script_dir/fixtures/example-input.json" >/dev/null
python3 -m json.tool "$script_dir/fixtures/expected-output.json" >/dev/null

echo "OK: cv-cover-optimizer script fixtures validated"
