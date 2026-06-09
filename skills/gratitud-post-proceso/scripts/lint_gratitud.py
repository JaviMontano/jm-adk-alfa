#!/usr/bin/env python3
"""Lint gratitude packets against deterministic post-process rules.

Input is usually JSON:
{
  "recipient": {"name_or_role": "...", "relationship": "...", "channel": "email"},
  "process": {"context": "...", "stage": "..."},
  "evidence": [{"type": "topic_discussed", "detail": "..."}],
  "message": {"subject": "...", "body": "...", "next_step_claim": "..."}
}

Plain text is accepted for ad hoc tone linting. Exit 0 clean, 1 violations,
3 bad input.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

TRADEMARKS = [
    "el futuro es humano",
    "method first",
    "method-first",
    "ai-native",
    "logremos mas y mejor",
    "convierte intencion",
]
FOMO = [
    "ultima oportunidad",
    "no te lo pierdas",
    "solo por hoy",
    "actua ya",
    "cupos limitados",
    "antes de que sea tarde",
]
HUSTLE = ["hustle", "sin descanso", "24/7", "siempre encendido", "always-on", "no dormir"]
SERVILE = [
    "perdon por molestar",
    "disculpa la molestia",
    "se que no merezco",
    "lamento mucho insistir",
]
UNSUPPORTED = [
    "seguro me haran oferta",
    "ya fui aceptado",
    "manana me contratan",
    "cuenten conmigo de forma exclusiva",
]
ALLOWED_EVIDENCE_TYPES = {
    "topic_discussed",
    "advice_received",
    "next_step_supplied",
    "contribution",
    "shared_decision",
}


def normalize(text: str) -> str:
    replacements = str.maketrans("áéíóúÁÉÍÓÚñÑ", "aeiouAEIOUnN")
    return text.translate(replacements).lower()


def tone_issues(text: str) -> list[str]:
    low = normalize(text)
    issues: list[str] = []
    trademarks = [phrase for phrase in TRADEMARKS if phrase in low]
    if len(trademarks) > 1:
        issues.append(f"stacked brand phrases: {trademarks}")
    for label, patterns in (("fomo", FOMO), ("hustle", HUSTLE), ("servility", SERVILE), ("unsupported_claim", UNSUPPORTED)):
        hits = [pattern for pattern in patterns if pattern in low]
        if hits:
            issues.append(f"{label}: {hits}")
    return issues


def packet_issues(data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if data.get("schema") != 1:
        issues.append("schema must be 1")
    if data.get("skill") != "gratitud-post-proceso":
        issues.append("skill must be gratitud-post-proceso")

    recipient = data.get("recipient")
    process = data.get("process")
    evidence = data.get("evidence")
    message = data.get("message")

    if not isinstance(recipient, dict):
        issues.append("recipient must be an object")
    else:
        for field in ["name_or_role", "relationship", "channel"]:
            if not str(recipient.get(field, "")).strip():
                issues.append(f"recipient.{field} is required")

    if not isinstance(process, dict):
        issues.append("process must be an object")
    elif not str(process.get("context", "")).strip():
        issues.append("process.context is required")

    if not isinstance(evidence, list) or not evidence:
        issues.append("evidence must contain at least one item")
    else:
        for item in evidence:
            if not isinstance(item, dict):
                issues.append("every evidence item must be an object")
                continue
            if item.get("type") not in ALLOWED_EVIDENCE_TYPES:
                issues.append(f"unsupported evidence type: {item.get('type')}")
            if len(str(item.get("detail", "")).split()) < 2:
                issues.append("evidence.detail must be specific")

    if not isinstance(message, dict):
        issues.append("message must be an object")
        body = ""
    else:
        body = str(message.get("body", "")).strip()
        if len(body.split()) < 25:
            issues.append("message.body must contain at least 25 words")
        if "{recipient}" in body or "{evidence}" in body:
            issues.append("message.body contains unresolved placeholders")
        next_step = str(message.get("next_step_claim", "")).strip()
        if next_step and not any(isinstance(item, dict) and item.get("type") == "next_step_supplied" for item in evidence or []):
            issues.append("next_step_claim requires next_step_supplied evidence")

    combined = " ".join(
        [
            str(message.get("subject", "")) if isinstance(message, dict) else "",
            body,
        ]
    )
    issues.extend(tone_issues(combined))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint post-process gratitude packets")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    path = Path(args.input)
    if not path.exists():
        print(f"ERROR: not found: {path}")
        return 3
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        issues = tone_issues(text)
    else:
        if not isinstance(data, dict):
            print("ERROR: JSON root must be an object")
            return 3
        issues = packet_issues(data)

    if not issues:
        print("gratitud lint: OK")
        return 0
    print("gratitud lint: ISSUES")
    for issue in issues:
        print(f"  {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
