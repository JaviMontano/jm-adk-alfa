#!/usr/bin/env python3
"""Validate deterministic brand-docx artifacts."""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


HEX_RE = re.compile(r"^[0-9A-Fa-f]{6}$")
ALLOWED_OOXML_URL_PREFIXES = (
    "http://schemas.openxmlformats.org",
    "http://purl.org",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_hex(value: str) -> str:
    raw = str(value).strip().lstrip("#").upper()
    if not HEX_RE.match(raw):
        raise ValueError(f"invalid hex color: {value}")
    return raw


def brand_config(fixture: dict, contract: dict) -> dict:
    cfg = fixture.get("brand_config") or {}
    colors = contract["fallback_colors"] | {
        key: normalize_hex(value)
        for key, value in (cfg.get("colors") or {}).items()
        if key in contract["fallback_colors"]
    }
    fonts = contract["fallback_fonts"] | {
        key: str(value)
        for key, value in (cfg.get("typography") or {}).items()
        if key in contract["fallback_fonts"]
    }
    brand = {
        "name": cfg.get("brand", {}).get("name", "Fallback Brand"),
        "wordmark": cfg.get("brand", {}).get("wordmark", "Fallback"),
        "tagline": cfg.get("brand", {}).get("tagline", "Deterministic DOCX")
    }
    docx = {
        "artifact_date": cfg.get("docx", {}).get("artifact_date", fixture.get("artifact_date", "2026-06-05")),
        "year": cfg.get("docx", {}).get("year", fixture.get("year", "2026")),
        "confidential": bool(cfg.get("docx", {}).get("confidential", fixture.get("confidential", False)))
    }
    return {"brand": brand, "colors": colors, "fonts": fonts, "docx": docx}


def paragraph(text: str, font: str, color: str) -> str:
    return (
        "<w:p><w:r><w:rPr>"
        f"<w:rFonts w:ascii=\"{escape(font)}\" w:hAnsi=\"{escape(font)}\"/>"
        f"<w:color w:val=\"{color}\"/>"
        "</w:rPr>"
        f"<w:t>{escape(text)}</w:t>"
        "</w:r></w:p>"
    )


def table_xml(rows: list[list[str]], colors: dict, font: str) -> str:
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    cells = "".join(
        "<w:tc><w:tcPr>"
        f"<w:shd w:fill=\"{colors['primary']}\"/>"
        "</w:tcPr>"
        f"{paragraph(cell, font, colors['white'])}</w:tc>"
        for cell in header
    )
    xml = "<w:tbl><w:tr><w:trPr><w:tblHeader/></w:trPr>" + cells + "</w:tr>"
    for row in body:
        xml += "<w:tr>" + "".join(f"<w:tc>{paragraph(cell, font, colors['black'])}</w:tc>" for cell in row) + "</w:tr>"
    return xml + "</w:tbl>"


def document_xml(fixture: dict, cfg: dict, contract: dict) -> str:
    colors = cfg["colors"]
    fonts = cfg["fonts"]
    brand = cfg["brand"]
    docx = cfg["docx"]
    title = fixture.get("title", "Untitled DOCX")
    sections = fixture.get("sections") or [{"heading": "Summary", "body": "Deterministic section."}]
    parts = [
        paragraph(brand["wordmark"], fonts["display"], colors["black"]),
        paragraph(title, fonts["display"], colors["black"]),
        paragraph(brand["tagline"], fonts["body"], colors["primary"]),
        paragraph("brand tokens " + " ".join(colors.values()), fonts["body"], colors["black"]),
    ]
    for section in sections:
        parts.append(paragraph(section.get("heading", "Section"), fonts["display"], colors["black"]))
        parts.append(paragraph(section.get("body", ""), fonts["body"], colors["black"]))
        if section.get("table"):
            parts.append(table_xml(section["table"], colors, fonts["body"]))
    footer = f"{docx['year']}"
    if docx["confidential"]:
        footer = "CONFIDENTIAL | " + footer
    parts.append(paragraph(footer, fonts["body"], colors["muted"]))
    if fixture.get("inject_remote_asset"):
        parts.append(paragraph("https://fonts.googleapis.com/css2?family=Inter", fonts["body"], colors["black"]))
    if fixture.get("inject_placeholder"):
        parts.append(paragraph("{{DATE}}", fonts["body"], colors["black"]))
    for color in fixture.get("inject_hardcoded_colors", []):
        parts.append(paragraph("legacy hardcoded color", fonts["body"], normalize_hex(color)))
    body = "".join(parts)
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">"
        f"<w:body>{body}<w:sectPr/></w:body></w:document>"
    )


def styles_xml(cfg: dict) -> str:
    fonts = cfg["fonts"]
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:styles xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">"
        f"<w:style w:type=\"paragraph\" w:styleId=\"CoverTitle\"><w:name w:val=\"CoverTitle\"/><w:rPr><w:rFonts w:ascii=\"{escape(fonts['display'])}\"/></w:rPr></w:style>"
        f"<w:style w:type=\"paragraph\" w:styleId=\"BodyText\"><w:name w:val=\"BodyText\"/><w:rPr><w:rFonts w:ascii=\"{escape(fonts['body'])}\"/></w:rPr></w:style>"
        "</w:styles>"
    )


def core_xml(fixture: dict, cfg: dict) -> str:
    title = fixture.get("title", "Untitled DOCX")
    date = cfg["docx"]["artifact_date"]
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\" "
        "xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\">"
        f"<dc:title>{escape(title)}</dc:title><dc:creator>brand-docx</dc:creator>"
        f"<dcterms:created>{escape(date)}</dcterms:created>"
        "</cp:coreProperties>"
    )


def docx_bytes(fixture: dict, contract: dict) -> bytes:
    if fixture.get("artifact_kind") == "html_renamed":
        return b"<!DOCTYPE html><html><body>Not a DOCX package</body></html>"
    cfg = brand_config(fixture, contract)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\"><Default Extension=\"xml\" ContentType=\"application/xml\"/></Types>")
        zf.writestr("_rels/.rels", "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rId1\" Type=\"officeDocument\" Target=\"word/document.xml\"/></Relationships>")
        if not fixture.get("omit_core_properties"):
            zf.writestr("docProps/core.xml", core_xml(fixture, cfg))
        zf.writestr("word/document.xml", document_xml(fixture, cfg, contract))
        zf.writestr("word/styles.xml", styles_xml(cfg))
    return buffer.getvalue()


def read_package(payload: bytes) -> tuple[list[str], str, list[str]]:
    errors: list[str] = []
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        return [], "", ["artifact is not a DOCX zip package"]
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = zf.namelist()
        text_parts = []
        for name in names:
            if name.endswith(".xml"):
                text_parts.append(zf.read(name).decode("utf-8", errors="replace"))
    return names, "\n".join(text_parts), errors


def validate(fixture: dict, contract: dict) -> list[str]:
    errors: list[str] = []
    try:
        cfg = brand_config(fixture, contract)
    except ValueError as exc:
        return [str(exc)]
    names, package_text, package_errors = read_package(docx_bytes(fixture, contract))
    errors.extend(package_errors)
    if errors:
        return errors
    for part in contract.get("required_zip_parts", []):
        if part not in names:
            errors.append(f"missing required DOCX part: {part}")
    for pattern in contract.get("forbidden_patterns", []):
        if pattern in {"http://", "https://"}:
            continue
        if pattern in package_text:
            errors.append(f"forbidden pattern present: {pattern}")
    for url in re.findall(r"https?://[^\"'<\s]+", package_text):
        if not url.startswith(ALLOWED_OOXML_URL_PREFIXES):
            errors.append(f"remote URL present: {url}")
    required_text = [
        fixture.get("title", "Untitled DOCX"),
        cfg["brand"]["wordmark"],
        cfg["docx"]["year"],
        cfg["colors"]["primary"],
        cfg["colors"]["black"],
        cfg["colors"]["white"],
        cfg["fonts"]["display"],
        cfg["fonts"]["body"],
    ]
    if cfg["docx"]["confidential"]:
        required_text.append("CONFIDENTIAL")
    for value in required_text:
        if value and value not in package_text:
            errors.append(f"missing expected DOCX value: {value}")
    if fixture.get("requires_table") and "<w:tbl>" not in package_text:
        errors.append("missing branded table")
    configured_colors = set(cfg["colors"].values())
    for legacy in contract.get("forbidden_legacy_colors_unless_configured", []):
        if legacy not in configured_colors and legacy in package_text:
            errors.append(f"legacy hardcoded color present: {legacy}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a deterministic brand-docx fixture")
    parser.add_argument("--contract", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--expect", choices=["pass", "fail"], required=True)
    args = parser.parse_args()

    contract = load_json(Path(args.contract))
    fixture = load_json(Path(args.fixture))
    errors = validate(fixture, contract)
    passed = not errors
    expected_pass = args.expect == "pass"
    if passed != expected_pass:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"expected={args.expect} actual={'pass' if passed else 'fail'}")
        return 1
    print(f"OK: {Path(args.fixture).name} {'passed' if passed else 'failed as expected'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
