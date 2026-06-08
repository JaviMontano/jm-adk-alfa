#!/usr/bin/env python3
"""ATS + brand-voice lint for a CV / cover letter (extends cv-transformer).

Checks a CV/cover text against a job description: keyword coverage, required
sections, length sanity, contact presence, and stacked-trademark/hustle voice.
Deterministic. Input JSON: {"text": "...", "job_keywords": [...], "kind": "cv"|"cover"}.

Exit 0 ok · 1 issues found · 3 bad input.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CV_SECTIONS = ["experien", "educa", "skill", "habilidad", "logro", "achiev"]
CONTACT = re.compile(r"(@|\+?\d[\d \-]{6,}|linkedin\.com)", re.I)
TRADEMARKS = ["el futuro es humano", "method first", "method-first", "ai-native"]
HUSTLE = ["24/7", "always-on", "siempre encendido", "sin descanso"]


def lint(text: str, kws: list[str], kind: str) -> list[str]:
    low = text.lower()
    issues = []
    missing = [k for k in kws if k.lower() not in low]
    if missing:
        issues.append(f"keywords ATS ausentes: {missing}")
    if kind == "cv":
        if not any(s in low for s in CV_SECTIONS):
            issues.append("faltan secciones reconocibles (experiencia/educación/skills/logros)")
        if not CONTACT.search(text):
            issues.append("sin datos de contacto detectables (email/teléfono/linkedin)")
        words = len(text.split())
        if words < 120:
            issues.append(f"CV demasiado corto ({words} palabras)")
    if kind == "cover":
        words = len(text.split())
        if words > 400:
            issues.append(f"cover demasiado largo ({words} palabras; ideal < 350)")
    tm = [t for t in TRADEMARKS if t in low]
    if len(tm) > 1:
        issues.append(f"trademarks apiladas ({tm}) — máx 1")
    hu = [h for h in HUSTLE if h in low]
    if hu:
        issues.append(f"glorificación de hustle: {hu}")
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="ATS + brand lint for CV/cover")
    ap.add_argument("--input", required=True)
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: bad JSON: {e}"); return 3
    issues = lint(d.get("text", ""), d.get("job_keywords", []), d.get("kind", "cv"))
    if not issues:
        print("cv/cover lint: OK"); return 0
    print("cv/cover lint: ISSUES")
    for i in issues:
        print(f"  {i}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
