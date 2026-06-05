#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
FACTORY="$ROOT/scripts/doc-factory"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

export DOC_FACTORY_TIMESTAMP="2026-06-05T00:00:00+00:00"

python3 -m py_compile "$FACTORY"/*.py "$FACTORY"/engines/*.py

formats="csv"
if python3 -c 'import jinja2' >/dev/null 2>&1; then
  formats="html,md,csv"
fi
echo "doc-factory formats under test: $formats"

python3 "$FACTORY/validate.py" \
  --schema "$FACTORY/fixtures/invoice-schema.json" \
  --data "$FACTORY/fixtures/invoice-sample.json"

python3 "$FACTORY/generate.py" \
  --schema "$FACTORY/fixtures/invoice-schema.json" \
  --data "$FACTORY/fixtures/invoice-sample.json" \
  --formats "$formats" \
  --output "$TMP_DIR/output" >/dev/null

python3 "$FACTORY/verify.py" --state "$TMP_DIR/output/generation-state.json"

first_hashes="$(find "$TMP_DIR/output" -type f -print0 | sort -z | xargs -0 shasum -a 256)"

python3 "$FACTORY/generate.py" \
  --schema "$FACTORY/fixtures/invoice-schema.json" \
  --data "$FACTORY/fixtures/invoice-sample.json" \
  --formats "$formats" \
  --output "$TMP_DIR/output" >/dev/null

second_hashes="$(find "$TMP_DIR/output" -type f -print0 | sort -z | xargs -0 shasum -a 256)"

if [[ "$first_hashes" != "$second_hashes" ]]; then
  echo "ERROR: doc-factory output is not deterministic" >&2
  exit 1
fi

python3 "$FACTORY/analyze.py" --compact "Genera factura para Acme Corp, 10 horas de consultoria a 150 USD" \
  | python3 -c 'import json,sys; data=json.load(sys.stdin); assert data["skill"] == "invoice-generator"; assert "html" in data["formats"] or data["formats"]'

echo "OK: doc-factory deterministic smoke check passed"
