#!/usr/bin/env python3
"""
Full Pipeline — Analyze → Prime → Generate → Calibrate
========================================================
End-to-end pipeline that chains all doc-factory components.

Usage:
    python pipeline.py "Genera factura para Acme Corp, 10 horas consultoria a $150"
    python pipeline.py "Crea el acta de la reunion de hoy con Ana y Carlos"
    python pipeline.py --data invoice.json --skill invoice-generator --formats html,docx
    python pipeline.py "Minuta del standup" --auto --dry-run

Pipeline stages:
    1. ANALYZE: Extract intent, skill, data from natural language
    2. PRIME:   Load schema, template, brand, fill defaults
    3. GENERATE: Deterministic template → output
    4. CALIBRATE: Log result, update confidence
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure doc-factory is in path
_factory_dir = str(Path(__file__).resolve().parent)
if _factory_dir not in sys.path:
    sys.path.insert(0, _factory_dir)

from analyze import analyze_input
from skill_loader import load_skill
from primer import prime
from calibrate import log_execution


def run_pipeline(text=None, data=None, skill=None, formats=None, auto=True, dry_run=False, output_dir=None):
    """
    Execute the full pipeline.

    Args:
        text: Raw user input (natural language)
        data: Pre-extracted JSON data (bypasses analyze stage)
        skill: Force specific skill (bypasses analyze stage)
        formats: Override output formats
        auto: Auto-fill defaults (date, folio, company)
        dry_run: Only analyze + prime, don't generate
        output_dir: Override output directory

    Returns:
        dict: Pipeline result with stages, outputs, and calibration.
    """
    pipeline_result = {
        "timestamp": datetime.now().isoformat(),
        "stages": {},
        "outputs": [],
        "success": False,
    }

    # ── STAGE 1: ANALYZE ──────────────────────────────────────
    if text and not skill:
        analysis = analyze_input(text)
        pipeline_result["stages"]["analyze"] = {
            "skill": analysis["skill"],
            "confidence": analysis["confidence"],
            "data_extracted": len(analysis["data"]),
            "suggestions": analysis["suggestions"],
        }

        if not analysis["skill"]:
            pipeline_result["stages"]["analyze"]["error"] = "No skill matched"
            pipeline_result["error"] = "Could not determine what to generate. Try being more specific."
            return pipeline_result

        skill = analysis["skill"]
        if not data:
            data = analysis["data"]
        if not formats:
            formats = analysis["formats"]
    elif not skill:
        pipeline_result["error"] = "Provide --text or --skill"
        return pipeline_result

    # ── STAGE 2: PRIME ─────────────────────────────────────────
    fmt = formats[0] if formats else None
    context = prime(skill, fmt, data, auto)
    pipeline_result["stages"]["prime"] = {
        "skill": skill,
        "ready": context["ready"],
        "missing": context["missing"],
        "format": context.get("format"),
        "knowledge_loaded": context.get("knowledge_count", 0),
        "agents_loaded": context.get("agents_count", 0),
    }

    if not formats:
        formats = context.get("formats_available", ["html"])

    # Use workspace output dir if available, unless overridden
    if not output_dir:
        output_dir = context.get("output_dir", "./output")

    if dry_run:
        pipeline_result["stages"]["generate"] = {"status": "DRY_RUN — skipped"}
        pipeline_result["dry_run"] = True
        pipeline_result["data_assembled"] = context["data"]
        pipeline_result["would_generate"] = formats
        pipeline_result["output_dir"] = output_dir
        pipeline_result["success"] = True
        return pipeline_result

    # ── STAGE 3: GENERATE ──────────────────────────────────────
    # Import generate module
    sys.modules.setdefault("generate", __import__("generate"))
    from generate import generate, discover_engines
    discover_engines()

    try:
        gen_state = generate(
            schema_path=context.get("schema_path"),
            data_path=None,  # We'll pass data directly
            template_path=context.get("template_path"),
            formats=formats,
            output_dir=output_dir,
        )
    except Exception:
        # generate() expects a file path for data, so write it temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(context["data"], tmp, ensure_ascii=False)
            tmp_path = tmp.name

        gen_state = generate(
            schema_path=context.get("schema_path"),
            data_path=tmp_path,
            template_path=context.get("template_path"),
            formats=formats,
            output_dir=output_dir,
        )

        Path(tmp_path).unlink(missing_ok=True)

    pipeline_result["stages"]["generate"] = {
        "files_generated": len(gen_state.get("output_files", [])),
        "errors": gen_state.get("errors", []),
    }
    pipeline_result["outputs"] = gen_state.get("output_files", [])
    pipeline_result["generation_state"] = str(Path(output_dir) / "generation-state.json")

    # ── STAGE 4: CALIBRATE ─────────────────────────────────────
    success = len(gen_state.get("errors", [])) == 0
    confidence = pipeline_result["stages"].get("analyze", {}).get("confidence", 0.8)

    cal_result = log_execution(
        skill_name=skill,
        success=success,
        generation_state=gen_state,
        failure_reason=gen_state["errors"][0] if gen_state.get("errors") else None,
        confidence=confidence,
    )

    pipeline_result["stages"]["calibrate"] = {
        "success_rate": cal_result["success_rate"],
        "total_executions": cal_result["executions"],
    }

    pipeline_result["success"] = success
    return pipeline_result


def main():
    parser = argparse.ArgumentParser(
        description="Full Pipeline — Analyze → Prime → Generate → Calibrate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Genera factura para Acme Corp, 10 horas consultoria a \\$150"
  %(prog)s "Crea minuta del standup con Ana y Carlos"
  %(prog)s --skill invoice-generator --data invoice.json --formats html,docx
  %(prog)s "Cotizacion para Maria Garcia" --dry-run
        """,
    )
    parser.add_argument("text", nargs="?", help="Natural language input")
    parser.add_argument("--skill", help="Force specific skill")
    parser.add_argument("--data", help="Path to JSON data file")
    parser.add_argument("--formats", help="Comma-separated output formats")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--auto", action="store_true", default=True, help="Auto-fill defaults (default: True)")
    parser.add_argument("--no-auto", action="store_true", help="Disable auto-fill")
    parser.add_argument("--dry-run", action="store_true", help="Analyze + Prime only, no generation")

    args = parser.parse_args()

    # Parse data
    data = None
    if args.data:
        if Path(args.data).exists():
            with open(args.data) as f:
                data = json.load(f)
        else:
            data = json.loads(args.data)

    formats = args.formats.split(",") if args.formats else None
    auto = not args.no_auto

    result = run_pipeline(
        text=args.text,
        data=data,
        skill=args.skill,
        formats=formats,
        auto=auto,
        dry_run=args.dry_run,
        output_dir=args.output,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
