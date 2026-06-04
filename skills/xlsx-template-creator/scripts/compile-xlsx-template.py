#!/usr/bin/env python3
"""Compile deterministic XLSX template specifications from structured JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_required_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        require(field in obj and obj[field] not in ("", None, []), f"{label} missing required field: {field}", errors)


def validate_color(value: str, policy: dict[str, Any], label: str, errors: list[str]) -> None:
    allowed = set(policy["semanticColors"].values())
    if value.startswith("#"):
        require(bool(re.match(r"^#[0-9a-fA-F]{6}$", value)), f"{label} has invalid hex color: {value}", errors)
    require(value in allowed, f"{label} must use a semantic color token from policy: {value}", errors)


def validate_formula(formula: str, formula_policy: dict[str, Any], label: str, errors: list[str]) -> None:
    require(formula.startswith(formula_policy["formulaPrefix"]), f"{label} formula must start with =", errors)
    upper = formula.upper()
    for token in formula_policy["blockedFormulaTokens"]:
        require(token not in upper, f"{label} formula uses blocked volatile/external token: {token}", errors)
    if formula_policy["divisionRequiresIfGuard"] and "/" in formula:
        require("IF(" in upper, f"{label} formula with division requires IF guard", errors)


def validate_column(column: dict[str, Any], index: int, sheet_name: str, template_policy: dict[str, Any], formula_policy: dict[str, Any], errors: list[str]) -> None:
    label = f"{sheet_name} column {index}"
    schema = load_json(ASSET_DIR / "xlsx-template-schema.json")
    validate_required_fields(column, schema["requiredColumnFields"], label, errors)
    width = column.get("width")
    require(isinstance(width, int), f"{label} width must be integer", errors)
    if isinstance(width, int):
        require(template_policy["columnWidth"]["min"] <= width <= template_policy["columnWidth"]["max"], f"{label} width is outside policy range", errors)
    col_type = column.get("type")
    require(col_type in template_policy["allowedColumnTypes"], f"{label} has unsupported type: {col_type}", errors)
    if col_type == "dropdown":
        source = str(column.get("source", ""))
        require(bool(source), f"{label} dropdown requires source", errors)
        require(any(source.startswith(prefix) for prefix in formula_policy["acceptedDropdownSourcePrefixes"]), f"{label} dropdown source must reference Config or named range", errors)
    if col_type == "formula" or column.get("formula"):
        validate_formula(str(column.get("formula", "")), formula_policy, label, errors)
    conditional = as_dict(column.get("conditionalFormat"))
    for key, value in conditional.items():
        if isinstance(value, dict):
            for color_field in ["bg", "font", "color"]:
                if color_field in value:
                    validate_color(str(value[color_field]), template_policy, f"{label} conditionalFormat.{key}.{color_field}", errors)


def validate_sheet(sheet: dict[str, Any], template_type: str, schema: dict[str, Any], template_policy: dict[str, Any], formula_policy: dict[str, Any], errors: list[str]) -> None:
    name = str(sheet.get("name", ""))
    validate_required_fields(sheet, schema["requiredSheetFields"], f"sheet {name or '<missing>'}", errors)
    columns = as_list(sheet.get("columns"))
    require(len(columns) >= int(template_policy["minimums"]["columnsPerDataSheet"]) or name == "Config", f"sheet {name} lacks minimum columns", errors)
    require(nonempty(sheet.get("printArea")), f"sheet {name} requires printArea", errors)
    if name != "Config":
        require(sheet.get("mergedCellsInDataArea") is False, f"sheet {name} must set mergedCellsInDataArea=false", errors)
    if name in {"Tracker", "KPIs", "Alerts"}:
        require(sheet.get("autoFilter") is True, f"sheet {name} must enable autoFilter", errors)
    if name == "Config":
        require("edit" in str(sheet.get("purpose", "")).lower(), "Config sheet purpose must tell users it is editable", errors)
    for index, raw_column in enumerate(columns, start=1):
        validate_column(as_dict(raw_column), index, name, template_policy, formula_policy, errors)


def validate_named_ranges(spec: dict[str, Any], schema: dict[str, Any], template_policy: dict[str, Any], formula_policy: dict[str, Any], errors: list[str]) -> None:
    ranges = [as_dict(item) for item in as_list(spec.get("namedRanges"))]
    minimum = int(template_policy["minimums"]["namedRanges"])
    require(len(ranges) >= minimum, f"namedRanges requires at least {minimum} items", errors)
    name_re = re.compile(formula_policy["namedRangePattern"])
    range_re = re.compile(formula_policy["cellRangePattern"])
    for index, item in enumerate(ranges, start=1):
        validate_required_fields(item, schema["requiredNamedRangeFields"], f"namedRange {index}", errors)
        name = str(item.get("name", ""))
        refers_to = str(item.get("refersTo", ""))
        require(bool(name_re.match(name)), f"namedRange {index} name must be workbook-safe", errors)
        require(bool(range_re.match(refers_to)), f"namedRange {index} refersTo must be a sheet cell range", errors)


def validate_validation_rows(spec: dict[str, Any], schema: dict[str, Any], template_policy: dict[str, Any], formula_policy: dict[str, Any], errors: list[str]) -> None:
    rows = [as_dict(item) for item in as_list(spec.get("validation"))]
    minimum = int(template_policy["minimums"]["validationChecks"])
    statuses = set(formula_policy["allowedValidationStatuses"])
    require(len(rows) >= minimum, f"validation requires at least {minimum} checks", errors)
    for index, item in enumerate(rows, start=1):
        validate_required_fields(item, schema["requiredValidationFields"], f"validation {index}", errors)
        require(item.get("status") in statuses, f"validation {index} has unsupported status", errors)
        require(nonempty(item.get("evidence")), f"validation {index} evidence is required", errors)


def validate(spec: dict[str, Any]) -> None:
    schema = load_json(ASSET_DIR / "xlsx-template-schema.json")
    template_policy = load_json(ASSET_DIR / "template-policy.json")
    formula_policy = load_json(ASSET_DIR / "formula-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["requiredTopLevel"], "workbook", errors)
    if errors:
        raise ValueError("\n".join(errors))

    template_type = str(spec.get("templateType", ""))
    require(template_type in template_policy["acceptedTemplateTypes"], f"unsupported templateType: {template_type}", errors)
    require(len(str(spec.get("title", "")).strip()) >= 6, "title must be specific", errors)
    sheets = [as_dict(item) for item in as_list(spec.get("sheets"))]
    require(len(sheets) >= int(template_policy["minimums"]["sheets"]), "not enough sheets", errors)
    names = [str(sheet.get("name", "")) for sheet in sheets]
    require(len(names) == len(set(names)), "sheet names must be unique", errors)
    required_sheets = set(template_policy["requiredSheets"].get(template_type, []))
    require(required_sheets.issubset(set(names)), f"{template_type} missing required sheets: {', '.join(sorted(required_sheets - set(names)))}", errors)
    for sheet in sheets:
        validate_sheet(sheet, template_type, schema, template_policy, formula_policy, errors)
    validate_named_ranges(spec, schema, template_policy, formula_policy, errors)
    validate_validation_rows(spec, schema, template_policy, formula_policy, errors)
    validate_required_fields(as_dict(spec.get("handoff")), schema["requiredHandoffFields"], "handoff", errors)
    if errors:
        raise ValueError("\n".join(errors))


def yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def render_yaml(spec: dict[str, Any]) -> str:
    lines = [
        f"templateType: {yaml_scalar(spec['templateType'])}",
        f"title: {yaml_scalar(spec['title'])}",
        f"locale: {yaml_scalar(spec['locale'])}",
        "sheets:",
    ]
    for sheet in spec["sheets"]:
        lines.extend(
            [
                f"  - name: {yaml_scalar(sheet['name'])}",
                f"    purpose: {yaml_scalar(sheet['purpose'])}",
                f"    printArea: {yaml_scalar(sheet['printArea'])}",
                f"    autoFilter: {yaml_scalar(bool(sheet.get('autoFilter', False)))}",
                f"    mergedCellsInDataArea: {yaml_scalar(bool(sheet.get('mergedCellsInDataArea', False)))}",
                "    columns:",
            ]
        )
        for column in sheet["columns"]:
            lines.extend(
                [
                    f"      - header: {yaml_scalar(column['header'])}",
                    f"        width: {yaml_scalar(column['width'])}",
                    f"        type: {yaml_scalar(column['type'])}",
                    f"        description: {yaml_scalar(column['description'])}",
                ]
            )
            if column.get("source"):
                lines.append(f"        source: {yaml_scalar(column['source'])}")
            if column.get("formula"):
                lines.append(f"        formula: {yaml_scalar(column['formula'])}")
    lines.append("namedRanges:")
    for item in spec["namedRanges"]:
        lines.extend(
            [
                f"  - name: {yaml_scalar(item['name'])}",
                f"    refersTo: {yaml_scalar(item['refersTo'])}",
                f"    purpose: {yaml_scalar(item['purpose'])}",
            ]
        )
    return "\n".join(lines) + "\n"


def table(headers: list[str], rows: list[list[Any]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(output)


def render_markdown(spec: dict[str, Any]) -> str:
    sheet_rows = [[sheet["name"], sheet["purpose"], len(sheet["columns"]), sheet["printArea"]] for sheet in spec["sheets"]]
    column_rows: list[list[Any]] = []
    for sheet in spec["sheets"]:
        for column in sheet["columns"]:
            signal = column.get("formula") or column.get("source") or ""
            column_rows.append([sheet["name"], column["header"], column["type"], column["width"], signal])
    range_rows = [[item["name"], item["refersTo"], item["purpose"]] for item in spec["namedRanges"]]
    validation_rows = [[item["status"], item["check"], item["evidence"]] for item in spec["validation"]]
    handoff = spec["handoff"]
    return "\n\n".join(
        [
            f"# XLSX Template Spec: {spec['title']}",
            "## Summary\n\n"
            + "\n".join(
                [
                    f"- Template type: `{spec['templateType']}`",
                    f"- Locale: `{spec['locale']}`",
                    f"- Sheets: `{len(spec['sheets'])}`",
                    f"- Named ranges: `{len(spec['namedRanges'])}`",
                    f"- Validation checks: `{len(spec['validation'])}`",
                ]
            ),
            "## Sheets\n\n" + table(["Sheet", "Purpose", "Columns", "Print area"], sheet_rows),
            "## Columns\n\n" + table(["Sheet", "Header", "Type", "Width", "Formula/source"], column_rows),
            "## Named Ranges\n\n" + table(["Name", "Reference", "Purpose"], range_rows),
            "## Validation\n\n" + table(["Status", "Check", "Evidence"], validation_rows),
            "## Handoff\n\n"
            + "\n".join(
                [
                    f"- Renderer: `{handoff['renderer']}`",
                    f"- Output format: `{handoff['outputFormat']}`",
                    f"- Notes: {handoff['notes']}",
                ]
            ),
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic XLSX template spec")
    parser.add_argument("--input", required=True, help="Path to workbook template JSON")
    parser.add_argument("--format", choices=["markdown", "yaml"], default="markdown")
    parser.add_argument("--output", help="Optional output file")
    args = parser.parse_args()

    try:
        spec = load_json(Path(args.input))
        validate(spec)
        rendered = render_yaml(spec) if args.format == "yaml" else render_markdown(spec)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
