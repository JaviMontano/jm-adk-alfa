#!/usr/bin/env python3
"""Gate references on explicit consent + track follow-up cadence.

A reference may only be listed/contacted when it carries an explicit consent
flag. Input JSON: {"references":[{"name","relation","consent":bool,
"last_contact_days":N}]}. Blocks non-consented refs; flags stale follow-ups.

Exit 0 all consented · 1 a non-consented ref present · 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

FOLLOWUP_DAYS = 30


def main() -> int:
    ap = argparse.ArgumentParser(description="Reference consent + follow-up check")
    ap.add_argument("--input", required=True)
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: bad JSON: {e}"); return 3
    blocked = []
    for r in d.get("references", []):
        name = r.get("name", "?")
        if not r.get("consent", False):
            blocked.append(name)
            print(f"  BLOQUEADA (sin consentimiento): {name}")
            continue
        days = r.get("last_contact_days")
        cad = f" · follow-up vencido ({days}d)" if isinstance(days, (int, float)) and days > FOLLOWUP_DAYS else ""
        print(f"  OK: {name} ({r.get('relation','')}){cad}")
    if blocked:
        print(f"  REGLA: nunca contactar/listar sin OK explícito. Pendientes: {blocked}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
