#!/usr/bin/env python3
"""Validate deterministic brand-html artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}")


class TagCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: set[str] = set()
        self.attrs: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.add(tag.lower())
        self.attrs.append((tag.lower(), {k.lower(): v or "" for k, v in attrs}))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def luminance(hex_color: str) -> float:
    raw = hex_color.lstrip("#")
    values = [int(raw[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    adjusted = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return 0.2126 * adjusted[0] + 0.7152 * adjusted[1] + 0.0722 * adjusted[2]


def contrast_ratio(a: str, b: str) -> float:
    left = luminance(a)
    right = luminance(b)
    high, low = max(left, right), min(left, right)
    return (high + 0.05) / (low + 0.05)


def root_block(html: str) -> str:
    match = re.search(r":root\s*\{(?P<body>.*?)\}", html, re.DOTALL)
    return match.group("body") if match else ""


def validate_favicon(collector: TagCollector) -> list[str]:
    errors: list[str] = []
    icon_links = []
    for tag, attrs in collector.attrs:
        if tag != "link":
            continue
        rel = attrs.get("rel", "").lower().split()
        if "icon" in rel:
            icon_links.append(attrs)

    if not icon_links:
        return ["missing svg favicon link"]

    valid_icon = False
    for attrs in icon_links:
        icon_type = attrs.get("type", "").lower()
        href = attrs.get("href", "").strip()
        href_lower = href.lower()
        if icon_type != "image/svg+xml":
            errors.append("favicon link must use type=image/svg+xml")
            continue
        if not href:
            errors.append("favicon link missing href")
            continue
        if href_lower.startswith(("http://", "https://")):
            errors.append("favicon href must not be remote")
            continue
        if ";base64" in href_lower:
            errors.append("favicon href must not use base64")
            continue
        if href_lower.startswith("data:image/svg+xml,"):
            if "%3csvg" not in href_lower and "<svg" not in href_lower:
                errors.append("favicon data URI must contain svg markup")
                continue
            valid_icon = True
            continue
        if href_lower.endswith(".svg") and "://" not in href_lower:
            valid_icon = True
            continue
        errors.append("favicon href must be a relative .svg path or URL-encoded SVG data URI")

    if not valid_icon:
        errors.append("missing valid svg favicon link")
    return errors


def validate(html: str, contract: dict) -> list[str]:
    errors: list[str] = []
    collector = TagCollector()
    collector.feed(html)

    if "<!DOCTYPE html>" not in html:
        errors.append("missing doctype")
    for required in contract.get("required_elements", []):
        if required == "!DOCTYPE html":
            continue
        if required.strip("<") not in collector.tags and required not in html:
            errors.append(f"missing required element: {required}")

    root = root_block(html)
    if not root:
        errors.append("missing :root token block")
    for token in contract.get("required_tokens", []):
        if token not in root:
            errors.append(f"missing token: {token}")

    if "@media" not in html:
        errors.append("missing responsive media query")
    for pattern in contract.get("forbidden_patterns", []):
        if pattern in html:
            errors.append(f"forbidden pattern present: {pattern}")
    if re.search(r"<script\b", html, re.IGNORECASE):
        errors.append("external or inline script is not allowed")
    if re.search(r"\s(?:src|href)=[\"']https?://", html, re.IGNORECASE):
        errors.append("remote src/href is not allowed by default")
    if re.search(r"\{\{[^}]+\}\}", html):
        errors.append("unresolved placeholder present")
    errors.extend(validate_favicon(collector))

    root_hex = set(HEX_RE.findall(root))
    all_hex = set(HEX_RE.findall(html))
    off_token = sorted(color for color in all_hex if color not in root_hex)
    if off_token:
        errors.append(f"off-token hex color(s): {', '.join(off_token)}")

    style_pairs = re.findall(r"background(?:-color)?\s*:\s*(#[0-9A-Fa-f]{6}).{0,80}?color\s*:\s*(#[0-9A-Fa-f]{6})", html, re.DOTALL)
    style_pairs += re.findall(r"color\s*:\s*(#[0-9A-Fa-f]{6}).{0,80}?background(?:-color)?\s*:\s*(#[0-9A-Fa-f]{6})", html, re.DOTALL)
    for first, second in style_pairs:
        if contrast_ratio(first, second) < 4.5:
            errors.append(f"low contrast pair: {first} {second}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a brand-html artifact")
    parser.add_argument("--contract", required=True)
    parser.add_argument("--html", required=True)
    parser.add_argument("--expect", choices=["pass", "fail"], required=True)
    args = parser.parse_args()

    contract = load_json(Path(args.contract))
    html = Path(args.html).read_text(encoding="utf-8")
    errors = validate(html, contract)
    passed = not errors
    expected_pass = args.expect == "pass"
    if passed != expected_pass:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"expected={args.expect} actual={'pass' if passed else 'fail'}")
        return 1
    print(f"OK: {Path(args.html).name} {'passed' if passed else 'failed as expected'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
