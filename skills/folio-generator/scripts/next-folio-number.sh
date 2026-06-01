#!/usr/bin/env bash
# Deterministically calculate and, when requested, reserve the next folio ID.

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  next-folio-number.sh [--dry-run|--apply] [--date YYYY-MM-DD] [--tracker FILE] PREFIX

Outputs:
  PREFIX-YYYY-NNN

Defaults:
  --dry-run
  --tracker .folio-tracker.json
  --date today

Rules:
  PREFIX must be exactly 3 uppercase letters.
  --dry-run never creates or mutates the tracker.
  --apply writes the incremented counter atomically.
USAGE
}

mode="dry-run"
tracker=".folio-tracker.json"
folio_date="$(date +%F)"
prefix=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      mode="dry-run"
      ;;
    --apply)
      mode="apply"
      ;;
    --date)
      if [ "$#" -lt 2 ]; then
        echo "ERROR: --date requires YYYY-MM-DD" >&2
        exit 2
      fi
      folio_date="$2"
      shift
      ;;
    --tracker)
      if [ "$#" -lt 2 ]; then
        echo "ERROR: --tracker requires a file path" >&2
        exit 2
      fi
      tracker="$2"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [ -n "$prefix" ]; then
        echo "ERROR: only one PREFIX is allowed" >&2
        exit 2
      fi
      prefix="$1"
      ;;
  esac
  shift
done

if [ -z "$prefix" ]; then
  echo "ERROR: PREFIX is required" >&2
  usage >&2
  exit 2
fi

if ! printf '%s\n' "$prefix" | grep -Eq '^[A-Z]{3}$'; then
  echo "ERROR: Prefix must be 3 uppercase letters (got: $prefix)" >&2
  exit 2
fi

python3 - "$mode" "$tracker" "$prefix" "$folio_date" <<'PY'
from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def fail(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


mode, tracker_arg, prefix, raw_date = sys.argv[1:5]
if mode not in {"dry-run", "apply"}:
    fail(f"unknown mode: {mode}", 2)

try:
    year = str(datetime.strptime(raw_date, "%Y-%m-%d").year)
except ValueError:
    fail(f"--date must be YYYY-MM-DD (got: {raw_date})", 2)

tracker = Path(tracker_arg)
if tracker.exists():
    try:
        data = json.loads(tracker.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"tracker is not valid JSON: {tracker}: {exc}")
else:
    data = {"folios": {}, "last_updated": ""}

if not isinstance(data, dict):
    fail("tracker root must be a JSON object")
folios = data.setdefault("folios", {})
if not isinstance(folios, dict):
    fail("tracker field 'folios' must be an object")

prefix_counts = folios.setdefault(prefix, {})
if not isinstance(prefix_counts, dict):
    fail(f"tracker field 'folios.{prefix}' must be an object")

current_raw = prefix_counts.get(year, 0)
try:
    current = int(current_raw)
except (TypeError, ValueError):
    fail(f"tracker counter for {prefix}-{year} must be an integer")
if current < 0:
    fail(f"tracker counter for {prefix}-{year} must be non-negative")

next_number = current + 1
folio_id = f"{prefix}-{year}-{next_number:03d}"

if mode == "apply":
    prefix_counts[year] = next_number
    data["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tracker.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(tracker.parent),
        delete=False,
        prefix=f".{tracker.name}.",
        suffix=".tmp",
    ) as tmp:
        json.dump(data, tmp, indent=2, ensure_ascii=False)
        tmp.write("\n")
        tmp_name = tmp.name
    os.replace(tmp_name, tracker)

print(folio_id)
PY
