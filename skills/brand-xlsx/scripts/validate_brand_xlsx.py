#!/usr/bin/env python3
"""Validate deterministic brand-xlsx artifacts."""

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


def cell_ref(row: int, column: int) -> str:
    letters = ""
    n = column
    while n:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row}"


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
        "tagline": cfg.get("brand", {}).get("tagline", "Deterministic XLSX")
    }
    xlsx = {
        "artifact_date": cfg.get("xlsx", {}).get("artifact_date", fixture.get("artifact_date", "2026-06-06")),
        "year": cfg.get("xlsx", {}).get("year", fixture.get("year", "2026")),
        "domain": cfg.get("xlsx", {}).get("domain", fixture.get("domain", "example.invalid"))
    }
    return {"brand": brand, "colors": colors, "fonts": fonts, "xlsx": xlsx}


def inline_cell(row: int, col: int, value: str, style: int = 0) -> str:
    return (
        f"<c r=\"{cell_ref(row, col)}\" t=\"inlineStr\" s=\"{style}\">"
        f"<is><t>{escape(str(value))}</t></is></c>"
    )


def worksheet_xml(fixture: dict, cfg: dict) -> str:
    colors = cfg["colors"]
    brand = cfg["brand"]
    xlsx = cfg["xlsx"]
    title = fixture.get("title", "Untitled XLSX")
    subtitle = fixture.get("subtitle", brand["tagline"])
    headers = fixture.get("headers") or ["Metric", "Value", "Owner"]
    rows = fixture.get("rows") or [["Revenue", "100", "Ops"], ["Churn", "4", "CS"]]
    footer = " | ".join(part for part in [brand["wordmark"], brand["tagline"], xlsx["year"], xlsx["domain"]] if part)
    width_count = max(len(headers), max((len(row) for row in rows), default=0), 8)

    sheet_rows = [
        f"<row r=\"1\" ht=\"36\" customHeight=\"1\">{inline_cell(1, 1, title, 1)}</row>",
        f"<row r=\"2\" ht=\"18\" customHeight=\"1\">{inline_cell(2, 1, subtitle, 2)}</row>",
        f"<row r=\"4\" ht=\"26\" customHeight=\"1\">" + "".join(inline_cell(4, i, header, 3) for i, header in enumerate(headers, 1)) + "</row>",
    ]
    for index, row in enumerate(rows, 5):
        style = 4 if (index - 5) % 2 == 0 else 5
        sheet_rows.append(f"<row r=\"{index}\" ht=\"20\" customHeight=\"1\">" + "".join(inline_cell(index, i, value, style) for i, value in enumerate(row, 1)) + "</row>")
    footer_row = len(rows) + 6
    sheet_rows.append(f"<row r=\"{footer_row}\" ht=\"16\" customHeight=\"1\">{inline_cell(footer_row, 1, footer, 6)}</row>")
    if fixture.get("inject_placeholder"):
        sheet_rows.append(f"<row r=\"{footer_row + 1}\">{inline_cell(footer_row + 1, 1, '{{DATE}}', 0)}</row>")
    if fixture.get("inject_remote_asset"):
        sheet_rows.append(f"<row r=\"{footer_row + 2}\">{inline_cell(footer_row + 2, 1, 'https://fonts.googleapis.com/css2?family=Inter', 0)}</row>")
    if fixture.get("inject_off_token_color"):
        sheet_rows.append(f"<row r=\"{footer_row + 3}\">{inline_cell(footer_row + 3, 1, 'legacy color 122562', 0)}</row>")

    cols = "".join(f"<col min=\"{i}\" max=\"{i}\" width=\"14\" customWidth=\"1\"/>" for i in range(1, width_count + 1))
    merge_ref = f"A1:{cell_ref(1, width_count)}"
    footer_ref = f"A{footer_row}:{cell_ref(footer_row, width_count)}"
    auto_filter = f"A4:{cell_ref(max(4, len(rows) + 4), len(headers))}"
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">"
        f"<sheetPr><tabColor rgb=\"FF{colors['primary']}\"/></sheetPr>"
        "<sheetViews><sheetView workbookViewId=\"0\"><pane xSplit=\"1\" ySplit=\"4\" topLeftCell=\"B5\" activePane=\"bottomRight\" state=\"frozen\"/></sheetView></sheetViews>"
        f"<cols>{cols}</cols><sheetData>{''.join(sheet_rows)}</sheetData>"
        f"<autoFilter ref=\"{auto_filter}\"/>"
        f"<mergeCells count=\"2\"><mergeCell ref=\"{merge_ref}\"/><mergeCell ref=\"{footer_ref}\"/></mergeCells>"
        f"<headerFooter><oddFooter>{escape(footer)}</oddFooter></headerFooter>"
        "</worksheet>"
    )


def styles_xml(cfg: dict, contract: dict, fixture: dict) -> str:
    colors = cfg["colors"]
    font = escape(cfg["fonts"]["body"])
    extra_fill = ""
    if fixture.get("inject_off_token_color"):
        extra_fill = "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FF122562\"/></patternFill></fill>"
    fills = [
        "none",
        colors["primary"],
        colors["black"],
        colors["white"],
        colors["background"],
        colors["muted"],
        colors["primarySoft"],
    ]
    fill_xml = "<fill><patternFill patternType=\"none\"/></fill>" + "".join(
        f"<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FF{color}\"/></patternFill></fill>"
        for color in fills[1:]
    ) + extra_fill
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<styleSheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
        "<fonts count=\"4\">"
        f"<font><name val=\"{font}\"/><sz val=\"18\"/><b/><color rgb=\"FF{colors['black']}\"/></font>"
        f"<font><name val=\"{font}\"/><sz val=\"10\"/><b/><color rgb=\"FF{colors['primary']}\"/></font>"
        f"<font><name val=\"{font}\"/><sz val=\"10\"/><color rgb=\"FF{colors['black']}\"/></font>"
        f"<font><name val=\"{font}\"/><sz val=\"8\"/><color rgb=\"FF{colors['muted']}\"/></font>"
        "</fonts>"
        f"<fills count=\"{7 + (1 if extra_fill else 0)}\">{fill_xml}</fills>"
        "<borders count=\"2\"><border/><border><bottom style=\"medium\"><color rgb=\"FF"
        f"{colors['primary']}\"/></bottom></border></borders>"
        "<cellXfs count=\"7\">"
        "<xf fontId=\"2\" fillId=\"0\" borderId=\"0\"/>"
        "<xf fontId=\"0\" fillId=\"1\" borderId=\"0\" applyFill=\"1\"/>"
        "<xf fontId=\"1\" fillId=\"2\" borderId=\"0\" applyFill=\"1\"/>"
        "<xf fontId=\"1\" fillId=\"2\" borderId=\"1\" applyFill=\"1\" applyBorder=\"1\"/>"
        "<xf fontId=\"2\" fillId=\"3\" borderId=\"0\" applyFill=\"1\"/>"
        "<xf fontId=\"2\" fillId=\"4\" borderId=\"0\" applyFill=\"1\"/>"
        "<xf fontId=\"3\" fillId=\"2\" borderId=\"0\" applyFill=\"1\"/>"
        "</cellXfs>"
        "</styleSheet>"
    )


def workbook_xml(fixture: dict) -> str:
    sheet_name = fixture.get("sheet_name", "Report")
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<workbook xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">"
        f"<sheets><sheet name=\"{escape(sheet_name)}\" sheetId=\"1\" r:id=\"rId1\"/></sheets>"
        "</workbook>"
    )


def core_xml(fixture: dict, cfg: dict) -> str:
    title = fixture.get("title", "Untitled XLSX")
    date = cfg["xlsx"]["artifact_date"]
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\" "
        "xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\">"
        f"<dc:title>{escape(title)}</dc:title><dc:creator>brand-xlsx</dc:creator>"
        f"<dcterms:created>{escape(date)}</dcterms:created>"
        "</cp:coreProperties>"
    )


def xlsx_bytes(fixture: dict, contract: dict) -> bytes:
    if fixture.get("artifact_kind") == "html_renamed":
        return b"<!DOCTYPE html><html><body>Not an XLSX package</body></html>"
    if fixture.get("artifact_kind") == "csv_renamed":
        return b"metric,value\nrevenue,100\n"
    cfg = brand_config(fixture, contract)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\"><Default Extension=\"xml\" ContentType=\"application/xml\"/></Types>")
        zf.writestr("_rels/.rels", "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rId1\" Type=\"officeDocument\" Target=\"xl/workbook.xml\"/></Relationships>")
        if not fixture.get("omit_core_properties"):
            zf.writestr("docProps/core.xml", core_xml(fixture, cfg))
        zf.writestr("xl/workbook.xml", workbook_xml(fixture))
        zf.writestr("xl/_rels/workbook.xml.rels", "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rId1\" Type=\"worksheet\" Target=\"worksheets/sheet1.xml\"/><Relationship Id=\"rId2\" Type=\"styles\" Target=\"styles.xml\"/></Relationships>")
        if not fixture.get("omit_styles"):
            zf.writestr("xl/styles.xml", styles_xml(cfg, contract, fixture))
        if not fixture.get("omit_sheet"):
            zf.writestr("xl/worksheets/sheet1.xml", worksheet_xml(fixture, cfg))
        if fixture.get("inject_remote_relationship"):
            zf.writestr("xl/_rels/remote.xml.rels", "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rRemote\" Target=\"https://example.invalid/logo.png\" TargetMode=\"External\"/></Relationships>")
    return buffer.getvalue()


def read_package(payload: bytes) -> tuple[list[str], str, list[str]]:
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        return [], "", ["artifact is not an XLSX zip package"]
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = zf.namelist()
        text_parts = []
        for name in names:
            if name.endswith(".xml") or name.endswith(".rels"):
                text_parts.append(zf.read(name).decode("utf-8", errors="replace"))
    return names, "\n".join(text_parts), []


def validate(fixture: dict, contract: dict) -> list[str]:
    errors: list[str] = []
    try:
        cfg = brand_config(fixture, contract)
    except ValueError as exc:
        return [str(exc)]
    names, package_text, package_errors = read_package(xlsx_bytes(fixture, contract))
    errors.extend(package_errors)
    if errors:
        return errors
    for part in contract.get("required_zip_parts", []):
        if part not in names:
            errors.append(f"missing required XLSX part: {part}")
    for pattern in contract.get("forbidden_patterns", []):
        if pattern in {"http://", "https://"}:
            continue
        if pattern in package_text:
            errors.append(f"forbidden pattern present: {pattern}")
    for url in re.findall(r"https?://[^\"'<\s]+", package_text):
        if not url.startswith(ALLOWED_OOXML_URL_PREFIXES):
            errors.append(f"remote URL present: {url}")
    colors = cfg["colors"]
    required_text = [
        fixture.get("title", "Untitled XLSX"),
        cfg["brand"]["wordmark"],
        cfg["brand"]["tagline"],
        cfg["xlsx"]["year"],
        cfg["xlsx"]["domain"],
        colors["primary"],
        colors["black"],
        colors["white"],
        colors["background"],
        colors["muted"],
        cfg["fonts"]["body"],
    ]
    for value in required_text:
        if value and value not in package_text:
            errors.append(f"missing expected XLSX value: {value}")
    if 'name="Sheet1"' in package_text:
        errors.append("sheet name must be meaningful, not Sheet1")
    for marker in ["<tabColor", "<mergeCell", "<pane", "<autoFilter", "<cols>", "<oddFooter>"]:
        if marker not in package_text:
            errors.append(f"missing workbook feature: {marker}")
    configured_colors = set(colors.values())
    for legacy in contract.get("forbidden_legacy_colors_unless_configured", []):
        if legacy not in configured_colors and legacy in package_text:
            errors.append(f"legacy hardcoded color present: {legacy}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a deterministic brand-xlsx fixture")
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
