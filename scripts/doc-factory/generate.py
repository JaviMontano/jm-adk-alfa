#!/usr/bin/env python3
"""
Doc Factory — Spec-Driven Document Generation Engine
=====================================================
Generates documents deterministically from schema + template + data.
BMAD Pattern: Schema (WHAT) > Template (HOW) > Data (INPUT) > Output (RESULT)
SDD Pattern: Validate > Generate > Verify (with SHA-256 provenance)

Usage:
    python generate.py --schema schema.json --data data.json --template template.docx --formats docx,pdf
    python generate.py --schema schema.json --data data.json --formats html,md  # uses default templates
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from runtime import timestamp_iso, timestamp_slug

# Engine registry — each format has a dedicated engine
ENGINES = {}


def register_engine(fmt):
    """Decorator to register a format engine."""
    def decorator(cls):
        ENGINES[fmt] = cls
        return cls
    return decorator


def load_json(path):
    """Load and parse a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def sha256_file(path):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return f"sha256:{h.hexdigest()[:16]}"


def sha256_data(data):
    """Compute SHA-256 hash of a JSON-serializable object."""
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False).encode('utf-8')
    return f"sha256:{hashlib.sha256(raw).hexdigest()[:16]}"


def discover_engines():
    """Import all engine modules to trigger registration."""
    factory_dir = Path(__file__).resolve().parent
    engines_dir = factory_dir / 'engines'
    if not engines_dir.exists():
        return
    # Ensure the doc-factory directory is in sys.path (absolute)
    factory_str = str(factory_dir)
    if factory_str not in sys.path:
        sys.path.insert(0, factory_str)
    import importlib
    for py_file in sorted(engines_dir.glob('*_engine.py')):
        module_name = f'engines.{py_file.stem}'
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)
        except Exception as e:
            print(f"WARNING: Could not load engine {module_name}: {e}", file=sys.stderr)


def generate(schema_path, data_path, template_path, formats, output_dir):
    """
    Main generation pipeline.

    Returns:
        dict: Generation state with hashes and output paths.
    """
    # Load inputs
    schema = load_json(schema_path) if schema_path else {}
    data = load_json(data_path)

    # Ensure output directory exists
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build generation state (SDD provenance pattern)
    timestamp = timestamp_iso()
    state = {
        "id": f"gen-{timestamp_slug(timestamp)}",
        "timestamp": timestamp,
        "schema_version": schema.get("$id", "unknown"),
        "input_data_hash": sha256_data(data),
        "output_files": [],
        "gates": {},
        "errors": []
    }

    if template_path:
        state["template_hash"] = sha256_file(template_path)

    # Generate each format
    for fmt in formats:
        fmt = fmt.strip().lower()

        if fmt not in ENGINES:
            state["errors"].append(f"No engine registered for format: {fmt}")
            continue

        engine = ENGINES[fmt]()

        # Determine template for this format
        tmpl = None
        if template_path:
            tmpl = Path(template_path)
            # If template_path is a directory, look for format-specific template
            if tmpl.is_dir():
                candidates = [
                    tmpl / f"template.{fmt}",
                    tmpl / f"template.{fmt}.html",  # for pdf via html
                ]
                for c in candidates:
                    if c.exists():
                        tmpl = c
                        break
                else:
                    tmpl = None

        # Derive output filename
        base_name = data.get("folio", data.get("title", data.get("name", "output")))
        # Sanitize filename
        base_name = "".join(c if c.isalnum() or c in '-_' else '-' for c in str(base_name))
        out_path = output_dir / f"{base_name}.{fmt}"

        try:
            engine.generate(
                data=data,
                template_path=tmpl,
                output_path=out_path,
                schema=schema
            )

            state["output_files"].append({
                "format": fmt,
                "path": str(out_path),
                "hash": sha256_file(out_path),
                "size_bytes": out_path.stat().st_size
            })
        except Exception as e:
            state["errors"].append(f"{fmt}: {str(e)}")

    # Write generation state
    state_path = output_dir / "generation-state.json"
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    return state


def main():
    parser = argparse.ArgumentParser(
        description='Doc Factory — Spec-Driven Document Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --data invoice.json --formats html,md
  %(prog)s --schema schema.json --data data.json --template tmpl.docx --formats docx,pdf
  %(prog)s --data report.json --formats csv --output ./reports/
        """
    )
    parser.add_argument('--schema', help='Path to JSON Schema file')
    parser.add_argument('--data', required=True, help='Path to JSON data file')
    parser.add_argument('--template', help='Path to template file or templates directory')
    parser.add_argument('--formats', required=True, help='Comma-separated output formats: docx,xlsx,pptx,pdf,html,csv,md')
    parser.add_argument('--output', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('--validate-only', action='store_true', help='Only validate inputs, do not generate')

    args = parser.parse_args()

    # Discover and load engines
    discover_engines()

    formats = [f.strip() for f in args.formats.split(',')]

    # Validate-only mode
    if args.validate_only:
        from validate import validate_inputs
        ok = validate_inputs(args.schema, args.data, args.template, formats)
        sys.exit(0 if ok else 1)

    # Run generation
    state = generate(
        schema_path=args.schema,
        data_path=args.data,
        template_path=args.template,
        formats=formats,
        output_dir=args.output
    )

    # Report results
    if state["errors"]:
        print(f"ERRORS: {len(state['errors'])}")
        for err in state["errors"]:
            print(f"  - {err}")
        sys.exit(1)

    print(f"GENERATED: {len(state['output_files'])} files")
    for f in state["output_files"]:
        print(f"  {f['format']:5s} → {f['path']} ({f['size_bytes']} bytes, {f['hash']})")
    print(f"STATE: {args.output}/generation-state.json")


if __name__ == '__main__':
    # Ensure doc-factory directory is in sys.path for engine imports
    _factory_dir = str(Path(__file__).resolve().parent)
    if _factory_dir not in sys.path:
        sys.path.insert(0, _factory_dir)
    # Make this module importable as 'generate' (not just __main__)
    # so engines can do: from generate import register_engine
    sys.modules['generate'] = sys.modules[__name__]
    main()
