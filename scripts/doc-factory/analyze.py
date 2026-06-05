#!/usr/bin/env python3
"""
Input Analyzer — Intent Extraction + Data Mining from Natural Language
======================================================================
Intercepts user input BEFORE any skill executes.
Extracts: intent, target skill, structured data fields, output format, confidence.

This is the DETERMINISTIC layer — it uses pattern matching, not LLM generation.
The LLM's job is to call this script with the raw user text.

Usage:
    python analyze.py "Genera factura para Acme Corp, 10 horas a $150"
    python analyze.py --input user-text.txt
    python analyze.py --json '{"text": "..."}'

Output: JSON with extracted intent, skill, data, format, confidence.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Skill trigger patterns — ordered by specificity (most specific first)
SKILL_TRIGGERS = [
    {
        "skill": "invoice-generator",
        "patterns": [
            r"(?:genera|crea|haz|make|create|build)\s*(?:una?\s+)?(?:factura|invoice)",
            r"factura\s+(?:para|for|de)",
            r"invoice\s+(?:for|to)",
        ],
        "data_extractors": {
            "client_name": [
                r"(?:para|for|a|to)\s+([A-Z][\w\s&.]+?)(?:\s*[,;.]|\s+(?:por|for|de|con|at)\b)",
                r"(?:cliente|client|customer)[\s:]+([A-Z][\w\s&.]+?)(?:\s*[,;.]|\s+\b)",
            ],
            "items": [
                r"(\d+)\s*(?:horas?|hrs?|hours?)\s*(?:de\s+)?(.+?)(?:\s+a\s+\$?([\d,.]+))",
                r"(\d+)\s*(.+?)(?:\s+(?:a|at|@)\s*\$?([\d,.]+))",
            ],
            "currency": [
                r"\b(USD|MXN|EUR|COP)\b",
                r"\$\s*([\d,.]+)",  # $ implies local currency
            ],
        },
        "default_formats": ["html", "docx"],
    },
    {
        "skill": "acta-formal",
        "patterns": [
            r"(?:genera|crea|redacta|write)\s*(?:el\s+)?(?:acta|formal\s+minutes|acta\s+formal)",
            r"acta\s+(?:de\s+)?(?:la\s+)?(?:reunion|junta|sesion|meeting)",
            r"(?:formal|official)\s+(?:minutes|record|acta)",
        ],
        "data_extractors": {
            "meeting_type": [
                r"(?:junta|reunion|sesion|asamblea|comite)\s+(?:de\s+)?(\w[\w\s]*?)(?:\s*[,;.]|\s+del?\b)",
            ],
            "date": [
                r"(?:del?|on|fecha)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
                r"(?:de\s+)?(?:hoy|today)",
                r"(\d{4}-\d{2}-\d{2})",
            ],
        },
        "default_formats": ["html", "docx"],
    },
    {
        "skill": "meeting-notes",
        "patterns": [
            r"(?:genera|crea|toma|write|take)\s*(?:las?\s+)?(?:minuta|notas|notes|minutes)",
            r"(?:minuta|notas)\s+(?:de\s+)?(?:la\s+)?(?:reunion|meeting|junta|standup|retro)",
            r"meeting\s+(?:notes|minutes)",
        ],
        "data_extractors": {
            "title": [
                r"(?:minuta|notas|notes|minutes)\s+(?:de\s+)?(?:la\s+)?(.+?)(?:\s*[,;.]|\s+del?\b)",
            ],
        },
        "default_formats": ["md", "html"],
    },
    {
        "skill": "folio-generator",
        "patterns": [
            r"(?:genera|crea|asigna)\s*(?:un?\s+)?(?:folio|cotizacion|memo|documento\s+numerado)",
            r"folio\s+(?:para|de|tipo)",
            r"(?:cotizacion|quotation|quote)\s+(?:para|for)",
            r"(?:COT|MEM|FAC|MIN|DOC)-\d{4}-\d{3}",
        ],
        "data_extractors": {
            "folio_type": [
                r"\b(COT|MEM|FAC|MIN|DOC)\b",
                r"(?:cotizacion|quote)\b",  # implies COT
                r"(?:memo|memorandum)\b",  # implies MEM
                r"(?:factura|invoice)\b",  # implies FAC
            ],
            "recipient_name": [
                r"(?:para|for|a)\s+([A-Z][\w\s&.]+?)(?:\s*[,;.]|\s+\b)",
            ],
        },
        "default_formats": ["html", "docx"],
    },
    {
        "skill": "cv-transformer",
        "patterns": [
            r"(?:genera|crea|transforma|make|create|build)\s*(?:un?\s+)?(?:cv|curriculum|resume|hoja\s+de\s+vida)",
            r"(?:cv|curriculum|resume)\s+(?:para|for|de)",
        ],
        "data_extractors": {
            "name": [
                r"(?:para|for|de)\s+([A-Z][\w\s]+?)(?:\s*[,;.]|\s+\b)",
            ],
        },
        "default_formats": ["html", "docx"],
    },
    {
        "skill": "sales-tracker",
        "patterns": [
            r"(?:registra|log|track|anota)\s*(?:la\s+)?(?:venta|sale|transaccion)",
            r"(?:ventas?|sales?)\s+(?:del?\s+)?(?:dia|hoy|today)",
            r"(?:reporte|report)\s+(?:de\s+)?(?:ventas|sales)",
        ],
        "data_extractors": {},
        "default_formats": ["xlsx"],
    },
    {
        "skill": "inventory-management",
        "patterns": [
            r"(?:inventario|inventory|stock)",
            r"(?:registra|actualiza|update)\s+(?:el\s+)?(?:inventario|stock)",
            r"(?:control|gestion)\s+(?:de\s+)?(?:inventario|stock)",
        ],
        "data_extractors": {},
        "default_formats": ["xlsx"],
    },
    {
        "skill": "follow-up-email",
        "patterns": [
            r"(?:envia|send|manda)\s*(?:el?\s+)?(?:follow\s*-?\s*up|seguimiento)",
            r"(?:follow\s*-?\s*up)\s+(?:de\s+)?(?:la\s+)?(?:reunion|meeting)",
            r"(?:action\s+items?)\s+(?:por\s+)?(?:email|correo)",
        ],
        "data_extractors": {},
        "default_formats": ["html"],
    },
]

# Format detection patterns
FORMAT_PATTERNS = {
    "docx": [r"\b(?:word|docx|documento)\b"],
    "xlsx": [r"\b(?:excel|xlsx|spreadsheet|hoja\s+de\s+calculo)\b"],
    "pptx": [r"\b(?:powerpoint|pptx|presentacion|slides?|deck)\b"],
    "pdf": [r"\b(?:pdf)\b"],
    "html": [r"\b(?:html|web|pagina)\b"],
    "csv": [r"\b(?:csv|comma)\b"],
    "md": [r"\b(?:markdown|md)\b"],
}


def extract_numbers(text):
    """Extract all numbers from text."""
    return [float(n.replace(",", "")) for n in re.findall(r"\$?([\d,]+\.?\d*)", text)]


def extract_email(text):
    """Extract email addresses."""
    return re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)


def extract_date(text):
    """Extract dates in various formats."""
    from datetime import datetime

    # ISO format
    iso = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    if iso:
        return iso[0]

    # "hoy" / "today"
    if re.search(r"\b(?:hoy|today)\b", text, re.I):
        return datetime.now().strftime("%Y-%m-%d")

    # DD/MM/YYYY or MM/DD/YYYY
    dates = re.findall(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", text)
    if dates:
        d, m, y = dates[0]
        y = f"20{y}" if len(y) == 2 else y
        return f"{y}-{m.zfill(2)}-{d.zfill(2)}"

    return datetime.now().strftime("%Y-%m-%d")


def analyze_input(text):
    """
    Analyze raw user input and extract structured information.

    Returns:
        dict: {skill, confidence, data, formats, raw_text, suggestions}
    """
    text_lower = text.lower().strip()
    result = {
        "raw_text": text,
        "skill": None,
        "confidence": 0.0,
        "data": {},
        "formats": [],
        "suggestions": [],
        "extractors_used": [],
    }

    # 1. Match skill by trigger patterns
    best_match = None
    best_score = 0

    for trigger in SKILL_TRIGGERS:
        for pattern in trigger["patterns"]:
            match = re.search(pattern, text_lower)
            if match:
                # Score by pattern specificity (longer match = higher score)
                score = len(match.group(0)) / len(text_lower) + 0.5
                if score > best_score:
                    best_score = score
                    best_match = trigger

    if best_match:
        result["skill"] = best_match["skill"]
        result["confidence"] = min(best_score, 1.0)
        result["formats"] = best_match["default_formats"]

        # 2. Extract data fields using skill-specific extractors
        for field, patterns in best_match.get("data_extractors", {}).items():
            for pattern in patterns:
                match = re.search(pattern, text, re.I)
                if match:
                    if field == "items":
                        # Special handling for line items
                        items = []
                        for m in re.finditer(pattern, text, re.I):
                            groups = m.groups()
                            if len(groups) >= 3:
                                items.append({
                                    "quantity": float(groups[0].replace(",", "")),
                                    "description": groups[1].strip(),
                                    "unit_price": float(groups[2].replace(",", "")),
                                })
                        if items:
                            result["data"]["items"] = items
                            result["extractors_used"].append(f"{field}:{pattern}")
                    else:
                        value = match.group(1) if match.lastindex else match.group(0)
                        result["data"][field] = value.strip()
                        result["extractors_used"].append(f"{field}:{pattern}")
                    break

    # 3. Extract common fields (date, email, numbers)
    if "date" not in result["data"]:
        result["data"]["date"] = extract_date(text)

    emails = extract_email(text)
    if emails:
        result["data"]["client_email"] = emails[0]

    # 4. Detect requested formats
    for fmt, patterns in FORMAT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                if fmt not in result["formats"]:
                    result["formats"].append(fmt)

    # 5. Generate suggestions for missing required fields
    if result["skill"]:
        schema_path = Path(f"skills/{result['skill']}/templates/schema.json")
        if schema_path.exists():
            with open(schema_path) as f:
                schema = json.load(f)
            required = schema.get("required", [])
            for field in required:
                if field not in result["data"] and field not in ("folio", "folio_id"):
                    result["suggestions"].append(
                        f"Missing required field: '{field}'"
                    )

    # 6. Confidence adjustment
    if result["skill"] and result["suggestions"]:
        # Reduce confidence if required fields are missing
        missing_ratio = len(result["suggestions"]) / max(
            len(result.get("data", {})) + len(result["suggestions"]), 1
        )
        result["confidence"] *= 1 - (missing_ratio * 0.3)

    result["confidence"] = round(result["confidence"], 3)

    return result


def main():
    parser = argparse.ArgumentParser(description="Input Analyzer — Intent + Data Extraction")
    parser.add_argument("text", nargs="?", help="Raw user input text")
    parser.add_argument("--input", help="Path to file with user input")
    parser.add_argument("--json", help="JSON string with 'text' field")
    parser.add_argument("--compact", action="store_true", help="Compact JSON output")

    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.input:
        text = Path(args.input).read_text(encoding="utf-8").strip()
    elif args.json:
        text = json.loads(args.json)["text"]
    else:
        text = sys.stdin.read().strip()

    result = analyze_input(text)

    indent = None if args.compact else 2
    print(json.dumps(result, indent=indent, ensure_ascii=False))


if __name__ == "__main__":
    main()
