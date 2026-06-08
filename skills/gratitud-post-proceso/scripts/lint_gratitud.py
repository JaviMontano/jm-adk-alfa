#!/usr/bin/env python3
"""Lint a thank-you message against MetodologIA brand-voice rules.

Deterministic checks:
- At most ONE trademark/conviction phrase per message (no stacking).
- No FOMO/urgency manipulation.
- No hustle glorification.
- No servility / over-apology.

Input: a text file with the message. Exit 0 clean · 1 violations · 3 bad input.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TRADEMARKS = [
    "el futuro es humano", "method first", "method-first", "ai-native",
    "logremos más y mejor", "logremos mas y mejor", "convierte intención",
]
FOMO = ["última oportunidad", "ultima oportunidad", "no te lo pierdas", "solo por hoy",
        "actúa ya", "actua ya", "cupos limitados", "antes de que sea tarde"]
HUSTLE = ["hustle", "sin descanso", "24/7", "siempre encendido", "always-on",
          "darlo todo siempre", "rendir al máximo siempre", "no dormir"]
SERVILE = ["perdón por molestar", "perdon por molestar", "disculpa la molestia",
           "sé que no merezco", "se que no merezco", "lamento mucho insistir"]


def lint(text: str) -> list[str]:
    low = text.lower()
    issues = []
    tm = [t for t in TRADEMARKS if t in low]
    if len(tm) > 1:
        issues.append(f"trademarks apiladas ({len(tm)}): {tm} — máximo 1 por mensaje")
    for label, pats in (("FOMO", FOMO), ("hustle", HUSTLE), ("servilismo", SERVILE)):
        hit = [p for p in pats if p in low]
        if hit:
            issues.append(f"{label}: {hit}")
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint thank-you message (brand voice)")
    ap.add_argument("--input", required=True)
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    issues = lint(p.read_text(encoding="utf-8"))
    if not issues:
        print("gratitud lint: OK (voz de marca limpia)"); return 0
    print("gratitud lint: VIOLACIONES")
    for i in issues:
        print(f"  {i}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
