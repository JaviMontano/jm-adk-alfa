#!/usr/bin/env python3
"""
Auto-Primer — Context Assembly Before Generation
=================================================
Assembles all context needed BEFORE a skill executes:
- Schema contract (required fields, types, defaults)
- Template selection (best match for format)
- Brand tokens (colors, fonts, logo)
- Workspace context (active workspace, task history)
- Knowledge injection (domain rules from skill's knowledge/)

Usage:
    python primer.py invoice-generator --format html
    python primer.py acta-formal --data '{"date": "2026-04-02"}'
    python primer.py meeting-notes --auto  # auto-fill defaults

Output: JSON context ready for generate.py
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from skill_loader import load_skill, SKILLS_ROOT


def load_brand_tokens():
    """Load brand design tokens."""
    brand_path = SKILLS_ROOT.parent / "references" / "brand" / "design-tokens.json"
    if brand_path.exists():
        with open(brand_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "colors": {"primary": "#16213e", "secondary": "#0f3460", "accent": "#e94560"},
        "fonts": {"heading": "Segoe UI", "body": "Calibri"},
        "company": "MetodologIA · JM Labs",
    }


def load_workspace_context():
    """Load active workspace info."""
    ws_root = SKILLS_ROOT.parent / "workspace"
    registry = ws_root / ".workspace-registry.json"

    if not registry.exists():
        return {"active": None}

    with open(registry, "r", encoding="utf-8") as f:
        reg = json.load(f)

    active_id = reg.get("activeWorkspace")
    if not active_id or active_id == "null":
        return {"active": None}

    return {
        "active": active_id,
        "artifacts_dir": str(ws_root / active_id / "artifacts"),
    }


def apply_defaults(data, schema):
    """Apply default values from schema for missing fields."""
    properties = schema.get("properties", {})
    for field, spec in properties.items():
        if field not in data and "default" in spec:
            data[field] = spec["default"]
    return data


def auto_fill(data, skill_name):
    """Auto-fill common fields with sensible defaults."""
    now = datetime.now()

    # Date
    data.setdefault("date", now.strftime("%Y-%m-%d"))

    # Folio generation
    if skill_name == "invoice-generator" and "folio" not in data:
        folio_script = SKILLS_ROOT.parent / "skills" / "folio-generator" / "scripts" / "next-folio-number.sh"
        if folio_script.exists():
            import subprocess
            try:
                result = subprocess.run(
                    ["bash", str(folio_script), "FAC"],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    data["folio"] = result.stdout.strip()
            except Exception:
                pass

    if skill_name == "folio-generator" and "folio_id" not in data:
        prefix = data.get("folio_type", "DOC")
        if prefix in ("cotizacion", "quote"):
            prefix = "COT"
        elif prefix in ("memo", "memorandum"):
            prefix = "MEM"

        folio_script = SKILLS_ROOT.parent / "skills" / "folio-generator" / "scripts" / "next-folio-number.sh"
        if folio_script.exists():
            import subprocess
            try:
                result = subprocess.run(
                    ["bash", str(folio_script), prefix],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    data["folio_id"] = result.stdout.strip()
                    data["folio"] = data["folio_id"]
            except Exception:
                pass

    if skill_name == "acta-formal" and "acta_number" not in data:
        folio_script = SKILLS_ROOT.parent / "skills" / "folio-generator" / "scripts" / "next-folio-number.sh"
        if folio_script.exists():
            import subprocess
            try:
                result = subprocess.run(
                    ["bash", str(folio_script), "MIN"],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    data["acta_number"] = result.stdout.strip()
            except Exception:
                pass

    # Company defaults
    brand = load_brand_tokens()
    data.setdefault("company_name", brand.get("company", "MetodologIA · JM Labs"))

    return data


def prime(skill_name, fmt=None, data=None, auto=False):
    """
    Assemble complete context for skill execution.

    Returns:
        dict: {skill_info, data, brand, workspace, output_dir, ready, missing}
    """
    # Load skill resources
    skill_info = load_skill(skill_name, fmt)

    if skill_info.get("error"):
        return {"error": skill_info["error"], "ready": False}

    # Initialize data
    if data is None:
        data = {}

    # Apply schema defaults
    if skill_info.get("schema"):
        data = apply_defaults(data, skill_info["schema"])

    # Auto-fill if requested
    if auto:
        data = auto_fill(data, skill_name)

    # Determine output directory
    ws = load_workspace_context()
    if ws.get("active"):
        output_dir = ws["artifacts_dir"]
    else:
        output_dir = str(SKILLS_ROOT.parent / "output")

    # Build context
    context = {
        "skill": skill_info["name"],
        "schema_path": skill_info.get("schema_path"),
        "template_path": skill_info.get("template_path"),
        "format": skill_info.get("format") or fmt,
        "formats_available": skill_info.get("templates_available", []),
        "data": data,
        "brand": load_brand_tokens(),
        "workspace": ws,
        "output_dir": output_dir,
        "knowledge": skill_info.get("knowledge", []),
        "agents": skill_info.get("agents", []),
        "ready": skill_info.get("ready", False),
        "missing": skill_info.get("missing", []),
    }

    # Check readiness
    if context["ready"] and skill_info.get("schema"):
        required = skill_info["schema"].get("required", [])
        for field in required:
            if field not in data:
                context["ready"] = False
                context["missing"].append(f"data.{field}")

    return context


def main():
    parser = argparse.ArgumentParser(description="Auto-Primer — Context Assembly")
    parser.add_argument("skill", help="Skill name")
    parser.add_argument("--format", help="Output format")
    parser.add_argument("--data", help="JSON data string or file path")
    parser.add_argument("--auto", action="store_true", help="Auto-fill defaults (date, folio, company)")

    args = parser.parse_args()

    # Parse data
    data = {}
    if args.data:
        if args.data.startswith("{"):
            data = json.loads(args.data)
        elif Path(args.data).exists():
            with open(args.data) as f:
                data = json.load(f)

    context = prime(args.skill, args.format, data, args.auto)
    print(json.dumps(context, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
