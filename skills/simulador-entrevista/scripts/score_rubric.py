#!/usr/bin/env python3
"""Score a mock-interview answer on THREE separate rubrics.

Deliberately keeps the dimensions SEPARATE (substance, English, presence) so
feedback never collapses into one blurred number.

Input JSON: {"substance":1-5,"english":1-5,"presence":1-5,"notes":...}
Output: per-dimension verdict + flags + single next step. No averaging.

Exit 0 ok · 1 a dimension is below floor (2) · 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DIMS = {
    "substance": "Sustancia ejecutiva (claridad, evidencia, impacto)",
    "english": "Inglés (fluidez, precisión, registro)",
    "presence": "Presencia (estructura, calma, señales de liderazgo)",
}
FLOOR = 2


def score(d: dict) -> tuple[bool, list[str], list[str]]:
    lines, flags = [], []
    for k, label in DIMS.items():
        v = int(d.get(k, 0))
        verdict = "fuerte" if v >= 4 else "ok" if v == 3 else "a reforzar"
        lines.append(f"{label}: {v}/5 — {verdict}")
        if v < FLOOR:
            flags.append(f"{k} bajo piso ({v}/5)")
    return (len(flags) == 0, lines, flags)


def main() -> int:
    ap = argparse.ArgumentParser(description="Score interview answer (3 rubrics)")
    ap.add_argument("--input", required=True)
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: bad JSON: {e}"); return 3
    ok, lines, flags = score(d)
    for ln in lines:
        print(f"  {ln}")
    weakest = min(DIMS, key=lambda k: int(d.get(k, 0)))
    print(f"  SIGUIENTE PASO: enfocar '{weakest}' en la próxima ronda.")
    for f in flags:
        print(f"  FLAG: {f}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
