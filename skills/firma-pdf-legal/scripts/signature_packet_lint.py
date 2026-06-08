#!/usr/bin/env python3
"""Validate deterministic evidence packets for firma-pdf-legal.

Input JSON describes a PDF signing operation after execution or dry-run proof.
The validator checks source preservation, consent, hashes, anchor placement,
render verification, and evidence shape. It never reads private PDF bytes and
never calls network services.

Exit codes: 0 valid packet, 1 validation issues, 3 unreadable input.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

HASH_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_KEYS = {"timestamp", "signed_at", "current_time", "remote_certificate_url"}
ALLOWED_STRATEGIES = {"anchor_text", "explicit_coordinates"}
ALLOWED_MODES = {"dry_run", "write_new_file"}


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.fullmatch(value))


def number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def check_packet(data: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    if data.get("schema") != 1:
        issues.append("schema must be 1")
    if data.get("skill") != "firma-pdf-legal":
        issues.append("skill must be firma-pdf-legal")

    seen_forbidden = FORBIDDEN_KEYS.intersection(data.keys())
    if seen_forbidden:
        issues.append(f"forbidden non-deterministic keys: {sorted(seen_forbidden)}")

    document = data.get("document")
    signature = data.get("signature")
    placement = data.get("placement")
    verification = data.get("verification")
    consent = data.get("consent")
    evidence = data.get("evidence")

    for name, value in [
        ("document", document),
        ("signature", signature),
        ("placement", placement),
        ("verification", verification),
        ("consent", consent),
    ]:
        if not isinstance(value, dict):
            issues.append(f"{name} must be an object")

    if isinstance(document, dict):
        if not str(document.get("path", "")).endswith(".pdf"):
            issues.append("document.path must end with .pdf")
        if not is_hash(document.get("sha256")):
            issues.append("document.sha256 must be a 64-char lowercase hex hash")
        pages = document.get("pages")
        if not isinstance(pages, int) or pages < 1:
            issues.append("document.pages must be a positive integer")
    else:
        pages = None

    if isinstance(signature, dict):
        if not str(signature.get("path", "")).endswith(".png"):
            issues.append("signature.path must end with .png")
        if not is_hash(signature.get("sha256")):
            issues.append("signature.sha256 must be a 64-char lowercase hex hash")
        if signature.get("transparent_background") is not True:
            issues.append("signature.transparent_background must be true")
        for field in ["width_px", "height_px"]:
            if not isinstance(signature.get(field), int) or signature[field] <= 0:
                issues.append(f"signature.{field} must be a positive integer")

    if isinstance(placement, dict):
        anchor = str(placement.get("anchor", "")).strip()
        if len(anchor) < 3:
            issues.append("placement.anchor must identify the signature line")
        if placement.get("strategy") not in ALLOWED_STRATEGIES:
            issues.append(f"placement.strategy must be one of {sorted(ALLOWED_STRATEGIES)}")
        page = placement.get("page")
        if not isinstance(page, int) or page < 1:
            issues.append("placement.page must be a positive integer")
        elif isinstance(pages, int) and page > pages:
            issues.append("placement.page cannot exceed document.pages")
        for field in ["x", "y"]:
            if not number(placement.get(field)) or placement[field] < 0:
                issues.append(f"placement.{field} must be a non-negative number")
        for field in ["width", "height"]:
            if not number(placement.get(field)) or placement[field] <= 0:
                issues.append(f"placement.{field} must be a positive number")
        mention = placement.get("mention", "")
        if mention is not None and len(str(mention)) > 80:
            issues.append("placement.mention must be at most 80 characters")

    if isinstance(verification, dict):
        if verification.get("anchor_found") is not True:
            issues.append("verification.anchor_found must be true")
        if not isinstance(verification.get("placed_count"), int) or verification["placed_count"] < 1:
            issues.append("verification.placed_count must be a positive integer")
        if not str(verification.get("rendered_png", "")).endswith(".png"):
            issues.append("verification.rendered_png must end with .png")
        if not is_hash(verification.get("render_sha256")):
            issues.append("verification.render_sha256 must be a 64-char lowercase hex hash")

    if isinstance(consent, dict):
        if consent.get("user_confirmed") is not True:
            issues.append("consent.user_confirmed must be true")
        if consent.get("source_preserved") is not True:
            issues.append("consent.source_preserved must be true")
        if consent.get("operation_mode") not in ALLOWED_MODES:
            issues.append(f"consent.operation_mode must be one of {sorted(ALLOWED_MODES)}")
        if consent.get("user_supplied_signature") is not True:
            issues.append("consent.user_supplied_signature must be true")

    if not isinstance(evidence, list) or len(evidence) < 3:
        issues.append("evidence must contain at least three entries")
    elif not all(isinstance(item, dict) and item.get("source") and item.get("claim") for item in evidence):
        issues.append("every evidence entry must include source and claim")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate firma-pdf-legal signing packet")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    path = Path(args.input)
    if not path.exists():
        print(f"ERROR: not found: {path}")
        return 3
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: bad JSON: {exc}")
        return 3
    if not isinstance(data, dict):
        print("ERROR: root must be an object")
        return 3
    issues = check_packet(data)
    if not issues:
        print("signature packet: OK")
        return 0
    print("signature packet: ISSUES")
    for issue in issues:
        print(f"  {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
