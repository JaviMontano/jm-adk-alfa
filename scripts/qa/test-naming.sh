#!/bin/bash
# test-naming.sh — smoke tests for scripts/lib/naming.sh canonical slugify.
set -uo pipefail

ROOT="$(git -C "$(dirname "$0")/../.." rev-parse --show-toplevel)"
NAMING="$ROOT/scripts/lib/naming.sh"
PASS=0; FAIL=0

eq() {
  local got exp="$2" label="$3"
  got="$(bash "$NAMING" slugify "$1")"
  if [ "$got" = "$exp" ]; then echo "PASS: $label → $got"; PASS=$((PASS+1))
  else echo "FAIL: $label expected '$exp' got '$got'"; FAIL=$((FAIL+1)); fi
}
fn() {
  bash "$NAMING" validate-filename "$1" >/dev/null 2>&1
  local got=$?
  if [ "$got" = "$2" ]; then echo "PASS: filename '$1' rc=$got"; PASS=$((PASS+1))
  else echo "FAIL: filename '$1' expected rc=$2 got rc=$got"; FAIL=$((FAIL+1)); fi
}

eq "Build a landing page for MetodologIA" "landing-page-metodologia" "drop stopwords + lead verb"
eq "Fix the login bug"                    "login-bug"                "drop article + lead verb"
eq "Aplicar a Empresa X"                  "aplicar-empresa-x"        "es stopwords"
eq "report report report final"          "report-final"             "dedupe consecutive"
eq "Diseñar la campaña de búsqueda"       "disenar-campana-busqueda" "transliterate accents"

fn "reporte-final.md"  0
fn "CLAUDE.md"         0
fn "_TEMPLATE-x.md"    0
fn ".gitkeep"          0
fn "Reporte Final.md"  1
fn "MyComponent.md"    1

echo "---"
echo "RESULT: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
