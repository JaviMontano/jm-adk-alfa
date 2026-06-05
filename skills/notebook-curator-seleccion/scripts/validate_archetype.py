#!/usr/bin/env python3
"""Validate a [SEL-EMPRESA] selection notebook against the canonical archetype.

The archetype requires these source slots:
  job-description · empresa-research · entrevista-notas · material-prep ·
  oferta-precontrato · notas-gratitud · post-mortem
Input JSON: {"sources": ["slot", ...]}. Reports missing/extra slots.
With --emit prints the canonical checklist instead.

Exit 0 complete · 1 missing slots · 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SLOTS = [
    "job-description", "empresa-research", "entrevista-notas", "material-prep",
    "oferta-precontrato", "notas-gratitud", "post-mortem",
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate SEL-EMPRESA notebook archetype")
    ap.add_argument("--input")
    ap.add_argument("--emit", action="store_true", help="Print canonical checklist")
    a = ap.parse_args()
    if a.emit or not a.input:
        print("[SEL-EMPRESA] fuentes canónicas:")
        for s in SLOTS:
            print(f"  - {s}")
        return 0
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: bad JSON: {e}"); return 3
    have = {s.lower() for s in d.get("sources", [])}
    missing = [s for s in SLOTS if s not in have]
    extra = [s for s in have if s not in SLOTS]
    print(f"archetype: {'COMPLETO' if not missing else 'INCOMPLETO'} ({len(SLOTS)-len(missing)}/{len(SLOTS)})")
    for m in missing:
        print(f"  FALTA: {m}")
    for e in extra:
        print(f"  extra: {e}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
