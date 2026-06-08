#!/usr/bin/env python3
"""Score job offers against acceptance filters + a P.I.V.O.T.E. gate.

Acceptance filters (from P-001 method):
  1. salary floor met (>= min) OR USD 10k+/mo if full-time exclusive
  2. allows parallel streams (not asphyxiating exclusivity)
  3. P.I.V.O.T.E. >= 7/10
  4. no hustle glorification
  5. compatible with relocation goal

Input JSON: {"offers":[{"name","monthly_usd","allows_streams":bool,
"pivote":0-10,"hustle_culture":bool,"relocation_ok":bool}], "floor_usd":...}
Output: per-offer pass/fail per filter + ranking of passing offers by pivote.

Exit 0 if >=1 offer passes all · 1 if none passes · 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def evaluate(offer: dict, floor: float) -> tuple[bool, list[str]]:
    fails = []
    if not (offer.get("monthly_usd", 0) >= floor or
            (offer.get("monthly_usd", 0) >= 10000 and offer.get("full_time_exclusive"))):
        fails.append("salario bajo piso")
    if not offer.get("allows_streams", False):
        fails.append("exclusividad asfixiante (bloquea streams)")
    if float(offer.get("pivote", 0)) < 7:
        fails.append(f"P.I.V.O.T.E. {offer.get('pivote',0)}<7")
    if offer.get("hustle_culture", False):
        fails.append("glorifica hustle")
    if not offer.get("relocation_ok", True):
        fails.append("incompatible con relocación")
    return (len(fails) == 0, fails)


def main() -> int:
    ap = argparse.ArgumentParser(description="Score offers vs acceptance filters + PIVOTE")
    ap.add_argument("--input", required=True)
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: bad JSON: {e}"); return 3
    floor = float(d.get("floor_usd", 0))
    passing = []
    for o in d.get("offers", []):
        ok, fails = evaluate(o, floor)
        print(f"  {o.get('name','?')}: {'PASA' if ok else 'FALLA'}" + ("" if ok else f" — {', '.join(fails)}"))
        if ok:
            passing.append(o)
    passing.sort(key=lambda o: float(o.get("pivote", 0)), reverse=True)
    if passing:
        print("RANKING (pasan todos los filtros):")
        for i, o in enumerate(passing, 1):
            print(f"  {i}. {o.get('name','?')} (P.I.V.O.T.E. {o.get('pivote')})")
        return 0
    print("Ninguna oferta pasa todos los filtros.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
