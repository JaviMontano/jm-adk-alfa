#!/usr/bin/env python3
"""Extract interviewers, roles and dates from raw selection-process emails.

Input: a text file (concatenated emails/notes). Heuristic extraction of
people + role + date lines like:
  "06/05 Juan Guillermo Dorado (Lead Delivery Manager)"
  "2026-05-21 Cahê Kuczera - EVP"
Outputs JSON with ordered stages and marks the latest (next-to-act).

Deterministic. Exit 0 always (empty list if nothing found).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# date (dd/mm or yyyy-mm-dd) ... Name ... (role) or - role
LINE = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2})\s+"
    r"(?P<name>[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ.]+(?:\s+[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ.]+){0,3})"
    r"\s*(?:\((?P<role1>[^)]+)\)|[-–]\s*(?P<role2>[^\n]+))"
)


def norm_date(d: str) -> str:
    return d  # keep as-is; sorting handles both forms lexicographically enough


def extract(text: str) -> list[dict]:
    out = []
    for m in LINE.finditer(text):
        role = (m.group("role1") or m.group("role2") or "").strip()
        out.append({"date": m.group("date"), "name": m.group("name").strip(), "role": role})
    # stable order by appearance; mark last as next
    for i, r in enumerate(out):
        r["stage"] = i + 1
        r["next"] = (i == len(out) - 1)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract interviewers from emails")
    ap.add_argument("--input", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    people = extract(p.read_text(encoding="utf-8"))
    if a.json:
        print(json.dumps({"interviewers": people, "count": len(people)}, ensure_ascii=False, indent=2))
    else:
        for r in people:
            flag = " <- NEXT/formaliza" if r["next"] else ""
            print(f"  [{r['stage']}] {r['date']}  {r['name']}  ({r['role']}){flag}")
        print(f"count={len(people)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
