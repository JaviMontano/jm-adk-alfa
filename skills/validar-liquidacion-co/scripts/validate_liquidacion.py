#!/usr/bin/env python3
"""Recompute and validate a Colombian severance settlement (liquidación).

Input JSON: {salario_base, dias, pagos:{cesantias,intereses_cesantias,prima,
vacaciones,...}, descuentos:{...}, neto, vacaciones_dias?}

Recomputes by Colombian norm:
  cesantías            = salario_base * dias / 360
  intereses cesantías  = cesantías * 0.12 * dias / 360
  prima                = salario_base * dias / 360
  vacaciones           = vacaciones_dias * salario_base / 30
Validates that the document's stated amounts match (tolerance) and that
sum(pagos) - sum(descuentos) == neto. Flags paz-y-salvo and lists what to ask.

Exit codes: 0 ok · 1 deviation found · 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

TOL = 1.0  # COP rounding tolerance


def close(a: float, b: float) -> bool:
    return abs(float(a) - float(b)) <= TOL


def validate(d: dict) -> tuple[bool, list[str], list[str]]:
    issues: list[str] = []
    asks: list[str] = []
    base = float(d["salario_base"]); dias = float(d["dias"])
    pagos = d.get("pagos", {}); desc = d.get("descuentos", {})
    exp = {
        "cesantias": base * dias / 360,
        "intereses_cesantias": (base * dias / 360) * 0.12 * dias / 360,
        "prima": base * dias / 360,
    }
    if "vacaciones_dias" in d:
        exp["vacaciones"] = float(d["vacaciones_dias"]) * base / 30
    for k, v in exp.items():
        if k in pagos and not close(pagos[k], v):
            issues.append(f"{k}: doc={pagos[k]:.0f} != recompute={v:.0f}")
    total_pagos = sum(float(x) for x in pagos.values())
    total_desc = sum(float(x) for x in desc.values())
    neto = total_pagos - total_desc
    if "neto" in d and not close(d["neto"], neto):
        issues.append(f"neto: doc={float(d['neto']):.0f} != sum={neto:.0f}")
    # advisory asks (not arithmetic errors)
    if "vacaciones_dias" in d:
        asks.append(f"Confirmar cómo se determinaron {d['vacaciones_dias']} días de vacaciones.")
    for k in desc:
        if "fund" in k.lower() or "fondo" in k.lower() or "credi" in k.lower():
            asks.append(f"Fondo/crédito '{k}': ¿se devuelve ahorro+rendimientos por separado?")
        if "prepagada" in k.lower() or "poliza" in k.lower() or "póliza" in k.lower():
            asks.append(f"Póliza '{k}': base y periodo del descuento.")
    asks.append("PAZ Y SALVO: no firmar con dudas abiertas sin avisar; opción 'bajo reserva de metodología'.")
    return (len(issues) == 0, issues, asks)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a Colombian liquidación JSON")
    ap.add_argument("--input", required=True)
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: input not found: {p}"); return 3
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: bad JSON: {e}"); return 3
    ok, issues, asks = validate(d)
    print(f"liquidacion: {'OK' if ok else 'DESVIO'}")
    for i in issues:
        print(f"  DESVIO: {i}")
    for q in asks:
        print(f"  PEDIR: {q}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
