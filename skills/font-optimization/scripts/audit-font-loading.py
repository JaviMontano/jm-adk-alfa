#!/usr/bin/env python3
"""Audit web files for deterministic font-loading anti-patterns."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ANTI_PATTERNS = {
    "google_fonts_runtime": re.compile(r"https://fonts\.googleapis\.com|https://fonts\.gstatic\.com", re.I),
    "css_import": re.compile(r"@import\s+url\(|@import\s+['\"]", re.I),
    "font_display_block": re.compile(r"font-display\s*:\s*block", re.I),
    "non_woff2_font": re.compile(r"\.(ttf|otf|woff)(['\")?#\s]|$)", re.I),
}


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_budget() -> dict[str, object]:
    path = skill_dir() / "assets" / "font-budget.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("budgets", {}) if isinstance(data, dict) else {}


def analyze_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[dict[str, object]] = []
    for code, pattern in ANTI_PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append({"code": code, "line": line, "match": match.group(0)})

    preload_count = len(re.findall(r"rel=['\"]preload['\"][^>]+as=['\"]font['\"]|as=['\"]font['\"][^>]+rel=['\"]preload['\"]", text, re.I))
    font_face_count = len(re.findall(r"@font-face", text, re.I))
    font_display_count = len(re.findall(r"font-display\s*:", text, re.I))
    woff2_count = len(re.findall(r"\.woff2", text, re.I))

    if font_face_count and font_display_count < font_face_count:
        findings.append({"code": "missing_font_display", "line": 1, "match": "@font-face without font-display"})
    if font_face_count and woff2_count == 0:
        findings.append({"code": "missing_woff2", "line": 1, "match": "@font-face without .woff2"})
    if font_face_count and preload_count == 0:
        findings.append({"code": "missing_preload", "line": 1, "match": "critical font without preload"})

    return {
        "path": str(path),
        "font_face_count": font_face_count,
        "font_display_count": font_display_count,
        "preload_count": preload_count,
        "woff2_count": woff2_count,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit font loading patterns")
    parser.add_argument("paths", nargs="+", help="HTML/CSS files to audit")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    load_budget()
    reports = [analyze_file(Path(path)) for path in args.paths]
    total_findings = sum(len(report["findings"]) for report in reports)

    if args.json:
        print(json.dumps({"files": reports, "finding_count": total_findings}, indent=2, ensure_ascii=False))
    else:
        for report in reports:
            print(f"{report['path']}: findings={len(report['findings'])}")
            for finding in report["findings"]:
                print(f"  line {finding['line']}: {finding['code']} -> {finding['match']}")
    return 1 if total_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
