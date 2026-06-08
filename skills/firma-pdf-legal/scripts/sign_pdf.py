#!/usr/bin/env python3
"""Place a supplied handwritten-signature PNG over an anchored line in a PDF.

The source PDF is never modified. The script writes a new output PDF and a
verification PNG. Requires PyMuPDF (fitz). Deterministic validation for DoD is
implemented separately in signature_packet_lint.py so CI does not need private
PDF fixtures or external services.

Exit codes: 0 ok, 2 anchor not found, 3 missing dependency/input.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import fitz  # type: ignore[import-not-found]
except Exception:  # noqa: BLE001
    print("ERROR: PyMuPDF (fitz) required: pip install pymupdf")
    raise SystemExit(3)


def sign(src: Path, out: Path, sig: Path, anchor: str, mention: str | None,
         dy_above: float, width: float, height: float) -> int:
    if not src.exists() or not sig.exists():
        print(f"ERROR: missing input pdf/signature: {src} | {sig}")
        return 3
    if src.resolve() == out.resolve():
        print("ERROR: output path must differ from source PDF")
        return 3
    doc = fitz.open(str(src))
    placed = 0
    for pno in range(doc.page_count):
        page = doc[pno]
        for rect in page.search_for(anchor):
            x0 = rect.x0
            y1 = rect.y0 - dy_above
            image_rect = fitz.Rect(x0, y1 - height, x0 + width, y1)
            page.insert_image(image_rect, filename=str(sig), overlay=True, keep_proportion=True)
            if mention:
                page.insert_text(
                    fitz.Point(x0 + width + 8, y1 - height / 2),
                    mention,
                    fontsize=7,
                    color=(0, 0, 0),
                )
            placed += 1
    if placed == 0:
        print(f"ERROR: anchor {anchor!r} not found in {src.name}")
        return 2
    doc.save(str(out))
    rendered = out.with_suffix(".verify.png")
    verified_doc = fitz.open(str(out))
    verified_doc[max(0, verified_doc.page_count - 1)].get_pixmap(dpi=120).save(str(rendered))
    print(f"OK placed={placed} output={out.name} verify={rendered.name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sign a legal PDF over an anchored line")
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--signature", required=True, help="Transparent PNG signature")
    parser.add_argument("--out", required=True)
    parser.add_argument("--anchor", default="Firma", help="Text label marking the signature line")
    parser.add_argument("--mention", default=None, help="Example: Leida y aprobada")
    parser.add_argument("--dy-above", type=float, default=2.0)
    parser.add_argument("--width", type=float, default=150.0)
    parser.add_argument("--height", type=float, default=38.0)
    args = parser.parse_args()
    return sign(
        Path(args.pdf),
        Path(args.out),
        Path(args.signature),
        args.anchor,
        args.mention,
        args.dy_above,
        args.width,
        args.height,
    )


if __name__ == "__main__":
    raise SystemExit(main())
