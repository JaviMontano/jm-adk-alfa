#!/usr/bin/env python3
"""Scaffold the Personal Jarvis OS sector structure (N0-N4) at a destination.

Creates the canonical Trabajar Amplificado / MetodologIA Jarvis OS layout:
00_Recursos, 01_Estaciones, 02_Proyectos, 03_Lab, 04_Cadencias + root
CLAUDE.md / MEMORY.md / TAREAS.md templates. Default is dry-run.

This is generic kit tooling: it writes only structure + placeholder templates,
never secrets, never the operator's private content.
"""

from __future__ import annotations

import argparse
from pathlib import Path

DIRS = [
    "00_Recursos",
    "01_Estaciones",
    "02_Proyectos",
    "03_Lab",
    "04_Cadencias/planes",
    "04_Cadencias/repasos-semanales",
    "04_Cadencias/repasos-mensuales",
    "04_Cadencias/repasos-trimestrales",
    "04_Cadencias/repasos-anuales",
]

ROOT_CLAUDE = """# CLAUDE.md - Jarvis OS Root

> Rules, routing, governance. Keep under 200 lines (Rule-9). Loads every session.

## Memory
Read MEMORY.md at session start. Persist durable learnings there only on request.

## Routing Map
Task -> station (01_Estaciones/). See station CLAUDE.md for specialization.

## Rules (imperative)
- Stack rules: root -> station -> project.
- NOW <= 3 tasks across all TAREAS.md.
- Mark non-verifiable claims with verification tags.
- No secrets in any tracked file.
"""

ROOT_MEMORY = """# MEMORY.md - Jarvis OS

## Memory (learnings & preferences)
- (seed) Adopted MetodologIA Personal Jarvis OS.

## Active Projects
- (none yet)
"""

ROOT_TAREAS = """# TAREAS.md

| NOW (<=3) | NEXT (<=5) | BACKLOG | DONE | KILLED |
|---|---|---|---|---|
|  |  |  |  |  |
"""

FILES = {
    "CLAUDE.md": ROOT_CLAUDE,
    "MEMORY.md": ROOT_MEMORY,
    "TAREAS.md": ROOT_TAREAS,
    "_ESTRUCTURA.md": "# _ESTRUCTURA.md\n\nContrato de repositorio Jarvis OS. Sectores N0-N4.\n",
}


def plan(dest: Path) -> list[str]:
    actions = []
    for d in DIRS:
        p = dest / d
        actions.append(f"mkdir {p}" if not p.exists() else f"skip-dir {p}")
    for name in FILES:
        p = dest / name
        actions.append(f"write {p}" if not p.exists() else f"skip-file {p}")
    return actions


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold Personal Jarvis OS structure (N0-N4)")
    ap.add_argument("--dest", required=True, help="Destination directory for the Jarvis OS")
    ap.add_argument("--apply", action="store_true", help="Actually create dirs/files")
    ap.add_argument("--dry-run", action="store_true", help="Show planned actions (default)")
    ap.add_argument("--force", action="store_true", help="Overwrite existing root templates")
    args = ap.parse_args()

    dest = Path(args.dest).expanduser()
    actions = plan(dest)

    if not args.apply:
        print(f"DRY-RUN: scaffold Jarvis OS at {dest}")
        for a in actions:
            print(f"  {a}")
        return 0

    for d in DIRS:
        (dest / d).mkdir(parents=True, exist_ok=True)
        print(f"mkdir: {dest / d}")
    for name, body in FILES.items():
        p = dest / name
        if p.exists() and not args.force:
            print(f"skip-file: {p} (exists; --force to overwrite)")
            continue
        p.write_text(body, encoding="utf-8")
        print(f"write: {p}")
    print("jarvis-os scaffold: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
