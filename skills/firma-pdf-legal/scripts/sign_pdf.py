#!/usr/bin/env python3
"""Place a handwritten-signature PNG over the correct line of a legal PDF.

Finds a text anchor (e.g. "El empleado" / "Firma" / a configurable label),
inserts a transparent signature image just above the signature line for every
match, optionally writes a mention ("Leída y aprobada"), and verifies by
rendering the page. Original PDF is never modified — output is a new file.

Deterministic + verifiable (kata: firma-pdf-legal). Requires PyMuPDF (fitz).

Exit codes: 0 ok · 2 anchor not found · 3 missing dependency/input.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception:  # noqa: BLE001
    print("ERROR: PyMuPDF (fitz) required: pip install pymupdf")
    raise SystemExit(3)


def sign(src: Path, out: Path, sig: Path, anchor: str, mention: str | None,
         dy_above: float, width: float, height: float) -> int:
    if not src.exists() or not sig.exists():
        print(f"ERROR: missing input pdf/signature: {src} | {sig}")
        return 3
    doc = fitz.open(str(src))
    placed = 0
    for pno in range(doc.page_count):
        pg = doc[pno]
        for r in pg.search_for(anchor):
            # signature sits just above the anchor (the signature line/label)
            x0 = r.x0
            y1 = r.y0 - dy_above
            rect = fitz.Rect(x0, y1 - height, x0 + width, y1)
            pg.insert_image(rect, filename=str(sig), overlay=True, keep_proportion=True)
            if mention:
                pg.insert_text(fitz.Point(x0 + width + 8, y1 - height / 2),
                               mention, fontsize=7, color=(0, 0, 0))
            placed += 1
    if placed == 0:
        print(f"ERROR: anchor {anchor!r} not found in {src.name}")
        return 2
    doc.save(str(out))
    # verification render (proves the page is renderable post-edit)
    v = fitz.open(str(out))
    png = out.with_suffix(".verify.png")
    v[max(0, v.page_count - 1)].get_pixmap(dpi=120).save(str(png))
    print(f"OK placed={placed} -> {out.name} (verify {png.name})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Sign a legal PDF over an anchored line")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--signature", required=True, help="Transparent PNG signature")
    ap.add_argument("--out", required=True)
    ap.add_argument("--anchor", default="Firma", help="Text label marking the signature line")
    ap.add_argument("--mention", default=None, help='e.g. "Leída y aprobada"')
    ap.add_argument("--dy-above", type=float, default=2.0)
    ap.add_argument("--width", type=float, default=150.0)
    ap.add_argument("--height", type=float, default=38.0)
    a = ap.parse_args()
    return sign(Path(a.pdf), Path(a.out), Path(a.signature), a.anchor,
                a.mention, a.dy_above, a.width, a.height)


if __name__ == "__main__":
    raise SystemExit(main())
