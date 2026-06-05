#!/usr/bin/env python3
"""Filter an incoming user prompt before agent or tool execution."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def require_list(data: dict, key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key}: expected non-empty list")
    result = [str(item).strip() for item in value]
    if any(not item for item in result):
        raise ValueError(f"{key}: list items must be non-empty")
    return result


def validate_input(data: dict) -> None:
    schema = load_json(ASSETS_DIR / "filter-input-schema.json")
    for key in schema["required"]:
        if key not in data:
            raise ValueError(f"{key}: required")
    prompt = str(data.get("prompt", "")).strip()
    if not prompt:
        raise ValueError("prompt: required")
    surface = str(data.get("surface", "")).strip()
    allowed_surfaces = set(schema["properties"]["surface"]["allowed"])
    if surface not in allowed_surfaces:
        raise ValueError(f"surface: must be one of {', '.join(sorted(allowed_surfaces))}")
    require_list(data, "protected_assets")
    require_list(data, "allowed_actions")


def find_spans(prompt: str, pattern: str) -> list[str]:
    spans: list[str] = []
    for match in re.finditer(re.escape(pattern), prompt, flags=re.IGNORECASE):
        start = max(0, match.start() - 24)
        end = min(len(prompt), match.end() + 48)
        spans.append(prompt[start:end].strip())
    return spans


def redact(text: str, policy: dict) -> str:
    redacted = text
    token = policy["redaction_token"]
    secret_patterns = [
        r"\b[A-Za-z0-9_\-]{24,}\b",
        r"(?i)(api[_ -]?key|token|password|secret)\s*[:=]\s*\S+",
    ]
    for pattern in secret_patterns:
        redacted = re.sub(pattern, token, redacted)
    for term in policy["protected_terms"]:
        redacted = re.sub(re.escape(term), token, redacted, flags=re.IGNORECASE)
    return redacted


def classify(prompt: str) -> list[dict]:
    taxonomy = load_json(ASSETS_DIR / "threat-taxonomy.json")
    sanitize_policy = load_json(ASSETS_DIR / "sanitization-policy.json")
    matches: list[dict] = []
    for threat in taxonomy["threats"]:
        evidence: list[str] = []
        for pattern in threat["patterns"]:
            evidence.extend(find_spans(prompt, pattern))
        if evidence:
            matches.append(
                {
                    "id": threat["id"],
                    "label": threat["label"],
                    "score": int(threat["base_score"]),
                    "action": threat["action"],
                    "evidence": [redact(item, sanitize_policy) for item in evidence[:3]],
                }
            )
    return matches


def has_benign_indicator(prompt: str) -> bool:
    taxonomy = load_json(ASSETS_DIR / "threat-taxonomy.json")
    lowered = prompt.lower()
    return any(indicator in lowered for indicator in taxonomy["benign_indicators"])


def severity(score: int) -> str:
    scoring = load_json(ASSETS_DIR / "risk-scoring-policy.json")
    for item in scoring["severity"]:
        if int(item["min"]) <= score <= int(item["max"]):
            return item["name"]
    return "critical"


def decide(prompt: str, matches: list[dict]) -> tuple[str, int, str]:
    if not matches:
        return "allow", 0, "high"
    score = min(10, max(int(item["score"]) for item in matches))
    ids = {item["id"] for item in matches}
    benign = has_benign_indicator(prompt)
    if benign and ids <= {"prompt_injection", "secret_exfiltration", "protected_context_leakage"}:
        return "allow_with_constraints", min(score, 5), "medium"
    if "secret_exfiltration" in ids or "protected_context_leakage" in ids:
        return "block", max(score, 9), "high"
    if "ambiguous_authority" in ids:
        return "escalate", max(score, 6), "medium"
    if "prompt_injection" in ids and ("tool_override" in ids or "destructive_action" in ids):
        return "block", max(score, 9), "high"
    if "prompt_injection" in ids or "tool_override" in ids:
        return "block", max(score, 8), "high"
    if "destructive_action" in ids:
        return "escalate", max(score, 6), "medium"
    return "allow_with_constraints", score, "medium"


def sanitize_prompt(prompt: str, data: dict, matches: list[dict]) -> str:
    policy = load_json(ASSETS_DIR / "sanitization-policy.json")
    sanitized = prompt
    for pattern in policy["remove_patterns"]:
        sanitized = re.sub(re.escape(pattern), "", sanitized, flags=re.IGNORECASE)
    sanitized = redact(sanitized, policy)
    sanitized = re.sub(r"\s+", " ", sanitized).strip(" .")
    if not sanitized:
        actions = require_list(data, "allowed_actions")
        sanitized = "Perform only the allowed task: " + "; ".join(actions)
    constraints = " ".join(policy["default_constraints"])
    return f"{sanitized}. {constraints}".strip()


def build_report(data: dict) -> dict:
    validate_input(data)
    prompt = str(data["prompt"])
    matches = classify(prompt)
    decision, score, confidence = decide(prompt, matches)
    policy = load_json(ASSETS_DIR / "sanitization-policy.json")
    constraints = list(policy["default_constraints"])
    protected_assets = require_list(data, "protected_assets")
    if protected_assets:
        constraints.append("Protected assets: " + ", ".join(protected_assets))
    report = {
        "decision": decision,
        "risk_score": score,
        "severity": severity(score),
        "confidence": confidence,
        "matched_threats": matches,
        "sanitized_prompt": sanitize_prompt(prompt, data, matches),
        "downstream_constraints": constraints,
        "residual_risk": [
            "Runtime permissions must still enforce tool, filesystem, network, and approval limits.",
            "Ambiguous authority requires owner confirmation before mutation.",
        ],
    }
    return report


def render_markdown(report: dict) -> str:
    lines = [
        "# User Prompt Filter Report",
        "",
        "## Decision",
        "",
        f"- Decision: `{report['decision']}`",
        f"- Severity: `{report['severity']}`",
        f"- Risk score: `{report['risk_score']}`",
        f"- Confidence: `{report['confidence']}`",
        "",
        "## Matched Threats",
        "",
        "| Threat | Evidence | Action |",
        "|---|---|---|",
    ]
    if report["matched_threats"]:
        for threat in report["matched_threats"]:
            evidence = "; ".join(threat["evidence"]) or "[REDACTED]"
            lines.append(f"| {threat['id']} | {evidence} | {threat['action']} |")
    else:
        lines.append("| none | No threat patterns matched | allow |")
    lines.extend(
        [
            "",
            "## Sanitized Prompt",
            "",
            report["sanitized_prompt"],
            "",
            "## Downstream Constraints",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in report["downstream_constraints"])
    lines.extend(["", "## Residual Risk", ""])
    lines.extend(f"- {item}" for item in report["residual_risk"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter an incoming user prompt")
    parser.add_argument("--input", required=True, help="JSON input file")
    parser.add_argument("--output", help="Optional output file")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()
    try:
        report = build_report(load_json(Path(args.input)))
        rendered = (
            json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
            if args.format == "json"
            else render_markdown(report)
        )
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
