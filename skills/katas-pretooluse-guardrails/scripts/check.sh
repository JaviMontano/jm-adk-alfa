#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/katas-pretooluse-guardrails"
VALIDATOR="$SKILL_DIR/scripts/validate_pretooluse_guardrails.py"
FIXTURES="$SKILL_DIR/scripts/fixtures"

valid_count=0
for fixture in "$FIXTURES"/valid-*.json; do
  python3 -B "$VALIDATOR" "$fixture" >/dev/null
  valid_count=$((valid_count + 1))
done

invalid_count="$(
  python3 -B - "$SKILL_DIR" <<'PY'
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

skill_dir = Path(sys.argv[1])
validator_path = skill_dir / "scripts" / "validate_pretooluse_guardrails.py"
spec = importlib.util.spec_from_file_location("pretooluse_validator", validator_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def locate(root, path: str):
    current = root
    parts = path.split(".")
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current, parts[-1]


def apply_operation(data, operation):
    parent, key = locate(data, operation["path"])
    if operation["op"] == "set":
        if isinstance(parent, list):
            parent[int(key)] = operation["value"]
        else:
            parent[key] = operation["value"]
    elif operation["op"] == "remove":
        if isinstance(parent, list):
            del parent[int(key)]
        else:
            del parent[key]
    else:
        raise ValueError(f"unknown operation: {operation['op']}")


mutations = load_json(skill_dir / "scripts" / "fixtures" / "invalid-mutations.json")["cases"]
failures = []
for case in mutations:
    base = load_json(skill_dir / "scripts" / "fixtures" / case["base"])
    mutated = copy.deepcopy(base)
    for operation in case["operations"]:
        apply_operation(mutated, operation)
    errors = module.validate(mutated)
    if not errors:
        failures.append(case["id"])

if failures:
    for failure in failures:
        print(f"invalid mutation passed unexpectedly: {failure}", file=sys.stderr)
    raise SystemExit(1)

print(len(mutations))
PY
)"

printf 'katas-pretooluse-guardrails check passed: valid=%s invalid=%s\n' "$valid_count" "$invalid_count"
