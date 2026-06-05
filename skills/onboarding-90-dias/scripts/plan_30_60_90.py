#!/usr/bin/env python3
"""Generate a sustainable 30/60/90 onboarding plan (anti-burnout).

Input JSON: {"role":"...", "focus_30":[...], "focus_60":[...], "focus_90":[...],
"weekly_hours": N}. Emits a structured plan and flags overload (anti-burnout
guard: > 45h/week sustained, or > 4 NOW priorities in any phase).

Exit 0 ok · 1 burnout/overload flag · 3 bad input.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

MAX_HOURS = 45
MAX_PRIORITIES = 4


def main() -> int:
    ap = argparse.ArgumentParser(description="30/60/90 onboarding plan")
    ap.add_argument("--input", required=True)
    a = ap.parse_args()
    p = Path(a.input)
    if not p.exists():
        print(f"ERROR: not found: {p}"); return 3
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: bad JSON: {e}"); return 3
    flags = []
    print(f"Plan 30/60/90 — {d.get('role','(rol)')}")
    for phase, key, theme in [(30, "focus_30", "Aprender · escuchar · mapear"),
                              (60, "focus_60", "Contribuir · primeros entregables"),
                              (90, "focus_90", "Apropiar · proponer mejoras")]:
        items = d.get(key, [])
        print(f"  D{phase} ({theme}):")
        for it in items[:MAX_PRIORITIES]:
            print(f"    - {it}")
        if len(items) > MAX_PRIORITIES:
            flags.append(f"D{phase}: {len(items)} prioridades (> {MAX_PRIORITIES}) — recortar (NOW<=3 ideal)")
    wh = d.get("weekly_hours", 0)
    if wh > MAX_HOURS:
        flags.append(f"{wh}h/semana sostenidas (> {MAX_HOURS}) — riesgo burnout")
    for f in flags:
        print(f"  FLAG: {f}")
    print("  PRINCIPIO: ritmo sostenible; energía > tiempo; sin always-on.")
    return 0 if not flags else 1


if __name__ == "__main__":
    raise SystemExit(main())
