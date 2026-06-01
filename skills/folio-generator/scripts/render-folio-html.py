#!/usr/bin/env python3
"""Render a folio HTML document from JSON data and bundled assets."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "folio_id",
    "subject",
    "company_name",
    "company_address",
    "date",
    "validity",
    "recipient_name",
    "recipient_company",
    "reference",
    "body_content",
    "signer_name",
    "signer_role",
    "validity_days",
]


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_data(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input data must be a JSON object")
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")
    return data


def render_conditionals(template: str, data: dict[str, object]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        block = match.group(2)
        return block if data.get(key) not in ("", None, False) else ""

    return re.sub(r"\{\{#if ([a-zA-Z0-9_]+)\}\}(.*?)\{\{/if\}\}", replace, template, flags=re.DOTALL)


def render(template: str, css: str, data: dict[str, object]) -> str:
    merged = dict(data)
    merged["folio_css"] = css
    rendered = render_conditionals(template, merged)

    def replace_placeholder(match: re.Match[str]) -> str:
        key = match.group(1)
        value = merged.get(key, "")
        if key in {"folio_css", "body_content"}:
            return str(value)
        return html.escape(str(value), quote=True)

    return re.sub(r"\{\{([a-zA-Z0-9_]+)\}\}", replace_placeholder, rendered)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render folio HTML deterministically")
    parser.add_argument("--data", required=True, help="JSON data file")
    parser.add_argument("--output", help="Write rendered HTML to this path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    template = (base / "templates" / "folio-template.html").read_text(encoding="utf-8")
    css = (base / "assets" / "folio-style.css").read_text(encoding="utf-8")
    data = load_data(Path(args.data))
    output = render(template, css, data)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
