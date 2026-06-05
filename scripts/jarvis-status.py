#!/usr/bin/env python3
"""Report Personal Jarvis OS health. Read-only.

Checks a Jarvis OS root for: sector presence, station count, NOW<=3 across all
TAREAS.md, latest cadence outputs, and basic context health. Prints a concise
status; never modifies files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

SECTORS = ["00_Recursos", "01_Estaciones", "02_Proyectos", "03_Lab", "04_Cadencias"]


def count_now(tareas: Path) -> int:
    """Count non-empty cells in the NOW column of a 5-column TAREAS.md table."""
    now = 0
    for line in tareas.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        first = cells[0]
        low = first.lower()
        if low.startswith("now") or set(first) <= set("- "):
            continue  # header or separator row
        if first:
            now += 1
    return now


def main() -> int:
    ap = argparse.ArgumentParser(description="Report Personal Jarvis OS health (read-only)")
    ap.add_argument("--root", required=True, help="Jarvis OS root directory")
    args = ap.parse_args()

    root = Path(args.root).expanduser()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}")
        return 1

    print(f"jarvis-status: {root}")

    # Sectors
    present = [s for s in SECTORS if (root / s).is_dir()]
    print(f"sectors: {len(present)}/{len(SECTORS)} present ({', '.join(present) or 'none'})")

    # Stations
    est = root / "01_Estaciones"
    stations = sorted([p.name for p in est.iterdir() if p.is_dir()]) if est.is_dir() else []
    print(f"stations: {len(stations)}" + (f" ({', '.join(stations)})" if stations else ""))

    # Projects
    proj = root / "02_Proyectos"
    projects = sorted([p.name for p in proj.iterdir() if p.is_dir()]) if proj.is_dir() else []
    print(f"projects: {len(projects)}")

    # NOW <= 3 across all TAREAS.md
    over = []
    for tareas in root.rglob("TAREAS.md"):
        n = count_now(tareas)
        if n > 3:
            over.append(f"{tareas.relative_to(root)}={n}")
    if over:
        print(f"WARN NOW>3: {', '.join(over)}")
    else:
        print("NOW<=3: ok")

    # Latest cadence output
    planes = root / "04_Cadencias" / "planes"
    if planes.is_dir():
        latest = sorted(planes.glob("*-daily-plan.md"))
        print(f"latest daily plan: {latest[-1].name if latest else 'none'}")

    print("jarvis-status: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
