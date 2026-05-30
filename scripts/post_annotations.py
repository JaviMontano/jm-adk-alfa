#!/usr/bin/env python3
"""Validate and post headless code-review annotations (Kata 13).

Consumes the JSON emitted by `claude -p "$PROMPT" --output-format=json` and
validates it against references/schemas/annotations.schema.json. If the payload
is invalid the job exits non-zero (no prose parsing, no silent "ajuste").

Stdlib only — implements the small subset of JSON Schema the contract needs, so
CI does not require the `jsonschema` package or the `claude` binary.

Usage:
  python3 scripts/post_annotations.py --validate-only path/to/out.json
  python3 scripts/post_annotations.py --post path/to/out.json   # prints gh commands
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return Path(result.stdout.strip())


SEVERITIES = {"error", "warning", "info"}


def validate(payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict) or "annotations" not in payload:
        return ["root object must have an 'annotations' array"]
    items = payload["annotations"]
    if not isinstance(items, list):
        return ["'annotations' must be an array"]
    for i, item in enumerate(items):
        where = f"annotations[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        for field in ("file", "line", "severity", "rule_id", "message"):
            if field not in item:
                errors.append(f"{where}: missing required field '{field}'")
        if not isinstance(item.get("file", ""), str) or not item.get("file"):
            errors.append(f"{where}.file: must be a non-empty string")
        if not isinstance(item.get("line"), int) or isinstance(item.get("line"), bool) or item.get("line", 0) < 1:
            errors.append(f"{where}.line: must be an integer >= 1")
        if item.get("severity") not in SEVERITIES:
            errors.append(f"{where}.severity: must be one of {sorted(SEVERITIES)}")
        if not isinstance(item.get("rule_id", ""), str) or not item.get("rule_id"):
            errors.append(f"{where}.rule_id: must be a non-empty string")
        if not isinstance(item.get("message", ""), str) or not item.get("message"):
            errors.append(f"{where}.message: must be a non-empty string")
    return errors


def post_commands(payload: dict) -> list[str]:
    cmds = []
    for item in payload["annotations"]:
        body = f"[{item['severity']}] {item['rule_id']}: {item['message']}"
        cmds.append(
            f"gh pr comment --body {json.dumps(body)} "
            f"# {item['file']}:{item['line']}"
        )
    return cmds


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate/post review annotations")
    parser.add_argument("input", help="Path to the JSON annotations file")
    parser.add_argument("--validate-only", action="store_true", help="Only validate, do not emit post commands")
    parser.add_argument("--post", action="store_true", help="Print the gh comment commands for each annotation")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 1

    errors = validate(payload)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"INVALID: {len(errors)} schema violation(s); job fails (no comments posted).", file=sys.stderr)
        return 1

    count = len(payload["annotations"])
    print(f"VALID: {count} annotation(s) conform to annotations.schema.json")
    if args.post and not args.validate_only:
        for cmd in post_commands(payload):
            print(cmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
