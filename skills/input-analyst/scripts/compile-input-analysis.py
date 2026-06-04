#!/usr/bin/env python3
"""Compile a deterministic offline analysis of raw user input.

The compiler uses local assets only. It does not call model providers, MCP
tools, network resources, or external APIs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def asset(name: str) -> Path:
    return skill_dir() / "assets" / name


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def load_assets() -> dict[str, dict[str, Any] | str]:
    return {
        "schema": load_json(asset("input-analysis-schema.json")),
        "surface": load_json(asset("surface-patterns.json")),
        "gaps": load_json(asset("intent-gap-taxonomy.json")),
        "quality": load_json(asset("quality-calibration.json")),
        "template": asset("input-analysis-template.md").read_text(encoding="utf-8"),
    }


def require_fields(data: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any] | str]) -> None:
    schema = assets["schema"]
    if not isinstance(schema, dict):
        raise ValueError("schema asset must be an object")
    require_fields(data, schema["required_root_fields"], "root")
    if data["schema_version"] != schema["schema"]:
        raise ValueError(f"schema_version must be {schema['schema']}")
    raw_input = str(data.get("raw_input", ""))
    if not raw_input.strip():
        raise ValueError("raw_input must not be empty")
    routing_policy = require_object(data, "routing_policy")
    require_fields(routing_policy, schema["required_routing_policy_fields"], "routing_policy")
    if routing_policy["offline_only"] is not True or routing_policy["allow_external_apis"] is not False:
        raise ValueError("routing_policy must enforce offline_only=true and allow_external_apis=false")
    requested = data.get("requested_passes")
    if requested is not None:
        if not isinstance(requested, list):
            raise ValueError("requested_passes must be a list when provided")
        unsupported = [item for item in requested if item not in schema["supported_passes"]]
        if unsupported:
            raise ValueError(f"unsupported requested_passes: {unsupported}")


def word_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_'/:-]+", text.lower())


def apply_surface_analysis(text: str, surface: dict[str, Any]) -> dict[str, Any]:
    corrected = text
    corrections: list[dict[str, str]] = []
    for item in surface["corrections"]:
        pattern = re.compile(str(item["pattern"]), flags=re.IGNORECASE)
        if pattern.search(corrected):
            before = corrected
            corrected = pattern.sub(str(item["replacement"]), corrected)
            corrections.append(
                {
                    "pattern": str(item["pattern"]),
                    "replacement": str(item["replacement"]),
                    "confidence": str(item["confidence"]),
                    "category": str(item["category"]),
                    "before": before,
                    "after": corrected,
                }
            )
    flags: list[dict[str, str]] = []
    for item in surface["flags"]:
        if re.search(str(item["pattern"]), text, flags=re.IGNORECASE):
            flags.append({"label": str(item["label"]), "message": str(item["message"])})

    lowered = set(word_tokens(text))
    language_markers = surface["mixed_language_markers"]
    spanish_hits = sorted(lowered.intersection(set(language_markers["spanish"])))
    english_hits = sorted(lowered.intersection(set(language_markers["english_technical"])))
    mixed_language = bool(spanish_hits and english_hits)
    if mixed_language:
        flags.append(
            {
                "label": "mixed_language",
                "message": f"Spanish markers {spanish_hits} with English technical markers {english_hits}.",
            }
        )

    return {
        "original": text,
        "corrected_text": corrected,
        "corrections": corrections,
        "flags": flags,
        "mixed_language": mixed_language,
    }


def detect_privacy(text: str, surface: dict[str, Any]) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []
    for item in surface["privacy_patterns"]:
        if re.search(str(item["pattern"]), text, flags=re.IGNORECASE):
            flags.append({"label": str(item["label"]), "severity": "review"})
    return flags


def select_passes(raw_input: str, surface: dict[str, Any], data: dict[str, Any], taxonomy: dict[str, Any]) -> list[str]:
    requested = data.get("requested_passes")
    if isinstance(requested, list) and requested:
        return [str(item) for item in requested]
    tokens = word_tokens(raw_input)
    gaps = detect_gaps(raw_input, taxonomy)
    if len(tokens) < 5:
        return ["intent", "reformulation"]
    if surface["corrections"] or surface["flags"] or len(gaps) >= 2:
        return ["surface", "five_whys", "seven_so_whats", "intent", "reformulation"]
    if gaps:
        return ["five_whys", "intent", "reformulation"]
    return ["intent", "reformulation"]


def detect_gaps(text: str, taxonomy: dict[str, Any]) -> list[dict[str, Any]]:
    lowered = text.lower()
    gap_types = taxonomy["gap_types"]
    priority = {name: index for index, name in enumerate(taxonomy["priority_order"])}
    detected: list[dict[str, Any]] = []
    for gap_type, spec in gap_types.items():
        hits = [signal for signal in spec["signals"] if re.search(rf"\b{re.escape(signal)}\b", lowered)]
        if not hits:
            continue
        detected.append(
            {
                "type": gap_type,
                "evidence": hits,
                "description": spec["description"],
                "real_ask_fragment": spec["default_real_ask"],
                "confidence": "medium" if len(hits) == 1 else "high",
            }
        )
    detected.sort(key=lambda item: priority.get(str(item["type"]), 99))
    return detected


def explicit_statements(raw_input: str, context: dict[str, Any]) -> list[str]:
    statements = [raw_input.strip()]
    constraints = context.get("constraints") if isinstance(context, dict) else None
    if isinstance(constraints, list):
        statements.extend(f"Constraint: {item}" for item in constraints if str(item).strip())
    return statements


def implicit_signals(surface: dict[str, Any], gaps: list[dict[str, Any]]) -> list[str]:
    signals = []
    signals.extend(f"surface:{item['category']}" for item in surface["corrections"])
    signals.extend(f"flag:{item['label']}" for item in surface["flags"])
    signals.extend(f"gap:{gap['type']}={','.join(gap['evidence'])}" for gap in gaps)
    return signals or ["no strong implicit signal detected"]


def ambiguity_register(raw_input: str, gaps: list[dict[str, Any]]) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    lowered = raw_input.lower()
    if any(gap["type"] == "context" for gap in gaps):
        questions.append(
            {
                "question": "What specific object, meeting, change, or artifact does the request refer to?",
                "affects": "Scope, deliverable, and downstream routing.",
            }
        )
    if re.search(r"\b(fix|bug|broken|not working)\b", lowered):
        questions.append(
            {
                "question": "What are the reproduction steps, expected behavior, and observed behavior?",
                "affects": "Root cause and validation criteria.",
            }
        )
    if re.search(r"\b(ai|smart|smarter|strategy|solution)\b", lowered):
        questions.append(
            {
                "question": "Which measurable outcome should the vague capability improve?",
                "affects": "Vocabulary mapping and success criteria.",
            }
        )
    if not questions:
        questions.append(
            {
                "question": "No blocking ambiguity detected.",
                "affects": "Proceed with the clarified prompt.",
            }
        )
    return questions


def five_whys(raw_input: str, gaps: list[dict[str, Any]], ambiguities: list[dict[str, str]]) -> dict[str, Any]:
    if not gaps or all(gap["type"] in {"vocabulary"} for gap in gaps):
        chain = [
            {
                "why": 1,
                "answer": "The user supplied enough surface detail for intent verification.",
                "evidence_type": "inferred",
            }
        ]
        root = "Confirm the literal request and preserve its stated outcome."
    elif any(gap["type"] == "context" for gap in gaps):
        chain = [
            {
                "why": 1,
                "answer": "The input depends on missing antecedents such as this, that, thing, or meeting.",
                "evidence_type": "explicit",
            },
            {
                "why": 2,
                "answer": "The root need cannot be safely determined until the missing context is named.",
                "evidence_type": "open_question",
            },
        ]
        root = "Clarify the missing context before executing or routing downstream."
    else:
        primary = gaps[0]
        chain = [
            {
                "why": 1,
                "answer": f"The request shows a {primary['type']} gap through {', '.join(primary['evidence'])}.",
                "evidence_type": "explicit",
            },
            {
                "why": 2,
                "answer": primary["real_ask_fragment"],
                "evidence_type": "inferred",
            },
        ]
        root = str(primary["real_ask_fragment"])
    return {
        "surface_request": raw_input,
        "chain": chain,
        "root_need": root,
        "open_questions": [item for item in ambiguities if item["question"] != "No blocking ambiguity detected."],
    }


def seven_so_whats(root_need: str, gaps: list[dict[str, Any]], quality: dict[str, Any]) -> dict[str, Any]:
    depth = 1
    if any(gap["type"] in {"scope", "expertise"} for gap in gaps):
        depth = 3
    if any(gap["type"] == "emotional" for gap in gaps):
        depth = max(depth, 3)
    if any(gap["type"] == "context" for gap in gaps):
        depth = 1
    chain = []
    outcomes = [
        "The immediate request becomes explicit enough to act on.",
        "The downstream agent can choose the right workflow without guessing.",
        "Validation criteria and risk controls can be attached before execution.",
        "The work can be sequenced by impact instead of user phrasing.",
        "Stakeholders get a traceable prompt with known limits.",
    ]
    for index in range(depth):
        chain.append(
            {
                "level": index + 1,
                "outcome": outcomes[index],
                "evidence_type": "inferred",
                "specificity": "qualified",
            }
        )
    if depth >= 5:
        quality_level = "Flagship"
    elif depth >= 3:
        quality_level = "Premium"
    else:
        quality_level = "Standard"
    return {
        "chain": chain,
        "quality_level": quality_level,
        "calibration_reason": quality["quality_calibration"][quality_level]["description"],
    }


def actionability_score(
    raw_input: str,
    surface: dict[str, Any],
    gaps: list[dict[str, Any]],
    ambiguities: list[dict[str, str]],
    quality: dict[str, Any],
) -> dict[str, Any]:
    model = quality["actionability"]
    score = int(model["base"])
    score -= len(surface["corrections"]) * int(model["surface_error_penalty"])
    score -= len(gaps) * int(model["gap_penalty"])
    blocking = [item for item in ambiguities if item["question"] != "No blocking ambiguity detected."]
    score -= len(blocking) * int(model["open_question_penalty"])
    if len(word_tokens(raw_input)) < 5:
        score -= int(model["very_short_penalty"])
    if not re.search(r"\b(write|create|fix|review|analyze|plan|make|build|generate|help|necesito|need)\b", raw_input, re.I):
        score -= int(model["missing_deliverable_penalty"])
    score = max(int(model["minimum"]), min(int(model["maximum"]), score))
    if score >= quality["confidence"]["high_min_score"]:
        band = "high"
    elif score >= quality["confidence"]["medium_min_score"]:
        band = "medium"
    else:
        band = "low"
    return {
        "score": score,
        "band": band,
        "drivers": {
            "surface_corrections": len(surface["corrections"]),
            "intent_gaps": len(gaps),
            "blocking_ambiguities": len(blocking),
        },
    }


def clarified_prompt(raw_input: str, surface: dict[str, Any], gaps: list[dict[str, Any]], whys: dict[str, Any], score: dict[str, Any]) -> str:
    corrected = surface["corrected_text"].strip()
    if score["score"] < 55 or any(gap["type"] == "context" for gap in gaps):
        return (
            "Clarify the missing context before executing: identify the specific artifact, "
            "audience, deadline, expected output, and success criteria. Original request: "
            f"{corrected}"
        )
    if gaps:
        gap_summary = "; ".join(f"{gap['type']} gap: {gap['real_ask_fragment']}" for gap in gaps[:2])
        return (
            f"Analyze and execute the request with this clarified intent: {whys['root_need']} "
            f"Preserve explicit constraints from the user input. Gap handling: {gap_summary}. "
            f"Corrected request: {corrected}"
        )
    return f"Execute the request as stated, preserving scope and constraints: {corrected}"


def routing_hints(score: dict[str, Any], so_whats: dict[str, Any], quality: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    routing = quality["routing"]
    candidates = data.get("downstream_candidates")
    if not isinstance(candidates, list) or not candidates:
        candidates = routing["default_downstream"]
    if score["drivers"]["blocking_ambiguities"] > 0 or score["score"] < routing["ask_clarification_below"]:
        next_action = "ask_clarification"
    elif score["score"] >= routing["execute_at_or_above"]:
        next_action = "execute"
    else:
        next_action = "confirm_then_execute"
    return {
        "next_action": next_action,
        "suggested_downstream": candidates,
        "quality_level": so_whats["quality_level"],
        "offline_only": True,
    }


def confidence(score: dict[str, Any], selected_passes: list[str]) -> dict[str, Any]:
    per_pass = {name: score["band"] for name in selected_passes}
    return {
        "overall": score["band"],
        "per_pass": per_pass,
        "aggregation_rule": "overall uses the actionability band after penalties for corrections, gaps, and open questions",
    }


def safety_privacy(raw_input: str, privacy_flags: list[dict[str, str]], routing_policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "privacy_flags": privacy_flags,
        "user_safety_flags": [],
        "external_api_required": False,
        "offline_policy": {
            "offline_only": routing_policy["offline_only"],
            "allow_external_apis": routing_policy["allow_external_apis"],
        },
        "redaction_required": bool(privacy_flags),
    }


def build_analysis(data: dict[str, Any], assets: dict[str, dict[str, Any] | str]) -> dict[str, Any]:
    raw_input = str(data["raw_input"])
    context = data.get("context") if isinstance(data.get("context"), dict) else {}
    surface_asset = assets["surface"]
    taxonomy = assets["gaps"]
    quality = assets["quality"]
    if not isinstance(surface_asset, dict) or not isinstance(taxonomy, dict) or not isinstance(quality, dict):
        raise ValueError("assets must be objects")

    surface = apply_surface_analysis(raw_input, surface_asset)
    gaps = detect_gaps(raw_input, taxonomy)
    selected = select_passes(raw_input, surface, data, taxonomy)
    ambiguities = ambiguity_register(raw_input, gaps)
    whys = five_whys(raw_input, gaps, ambiguities)
    so_whats = seven_so_whats(whys["root_need"], gaps, quality)
    score = actionability_score(raw_input, surface, gaps, ambiguities, quality)
    prompt = clarified_prompt(raw_input, surface, gaps, whys, score)
    routing = routing_hints(score, so_whats, quality, data)
    privacy_flags = detect_privacy(raw_input, surface_asset)
    safety = safety_privacy(raw_input, privacy_flags, data["routing_policy"])

    return {
        "schema_version": "input-analysis-output.v1",
        "selected_passes": selected,
        "surface_errors": surface,
        "five_whys": whys,
        "seven_so_whats": so_whats,
        "intent_gap_analysis": {
            "explicit_statements": explicit_statements(raw_input, context),
            "implicit_signals": implicit_signals(surface, gaps),
            "gaps": gaps,
            "real_ask": prompt,
        },
        "ambiguity_register": ambiguities,
        "actionability_score": score,
        "clarified_prompt": prompt,
        "routing_hints": routing,
        "user_safety_privacy_flags": safety,
        "confidence": confidence(score, selected),
    }


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None"


def render_surface(surface: dict[str, Any]) -> str:
    lines = [f"- [CODE] Corrected text: {surface['corrected_text']}"]
    for correction in surface["corrections"]:
        lines.append(
            "- [CODE] "
            f"{correction['category']} {correction['pattern']} -> {correction['replacement']} "
            f"confidence={correction['confidence']}"
        )
    for flag in surface["flags"]:
        lines.append(f"- [INFERENCE] {flag['label']}: {flag['message']}")
    return "\n".join(lines)


def render_whys(whys: dict[str, Any]) -> str:
    lines = [f"- [CODE] Surface request: {whys['surface_request']}"]
    for item in whys["chain"]:
        lines.append(f"- [{item['evidence_type'].upper()}] Why {item['why']}: {item['answer']}")
    lines.append(f"- [INFERENCE] Root need: {whys['root_need']}")
    return "\n".join(lines)


def render_so_whats(so_whats: dict[str, Any]) -> str:
    lines = []
    for item in so_whats["chain"]:
        lines.append(
            f"- [{item['evidence_type'].upper()}] So What {item['level']}: "
            f"{item['outcome']} specificity={item['specificity']}"
        )
    lines.append(f"- [CODE] Quality level: {so_whats['quality_level']}")
    lines.append(f"- [INFERENCE] Calibration: {so_whats['calibration_reason']}")
    return "\n".join(lines)


def render_gaps(intent: dict[str, Any]) -> str:
    lines = bullets([f"[CODE] Explicit: {item}" for item in intent["explicit_statements"]]).splitlines()
    lines.extend(f"- [INFERENCE] Signal: {item}" for item in intent["implicit_signals"])
    if intent["gaps"]:
        for gap in intent["gaps"]:
            lines.append(
                f"- [INFERENCE] {gap['type']} gap evidence={gap['evidence']} "
                f"confidence={gap['confidence']} real_ask={gap['real_ask_fragment']}"
            )
    else:
        lines.append("- [CODE] No significant intent gap detected.")
    return "\n".join(lines)


def render_ambiguities(items: list[dict[str, str]]) -> str:
    return "\n".join(f"- [OPEN] {item['question']} Affects: {item['affects']}" for item in items)


def render_safety(safety: dict[str, Any]) -> str:
    lines = [f"- [CODE] external_api_required={str(safety['external_api_required']).lower()}"]
    lines.append(f"- [CODE] redaction_required={str(safety['redaction_required']).lower()}")
    if safety["privacy_flags"]:
        for flag in safety["privacy_flags"]:
            lines.append(f"- [CODE] privacy_flag={flag['label']} severity={flag['severity']}")
    else:
        lines.append("- [CODE] No privacy flags detected.")
    return "\n".join(lines)


def render_markdown(analysis: dict[str, Any], template: str) -> str:
    replacements = {
        "{{SUMMARY}}": (
            f"[CODE] schema={analysis['schema_version']} "
            f"selected_passes={', '.join(analysis['selected_passes'])}"
        ),
        "{{SURFACE_ERRORS}}": render_surface(analysis["surface_errors"]),
        "{{FIVE_WHYS}}": render_whys(analysis["five_whys"]),
        "{{SEVEN_SO_WHATS}}": render_so_whats(analysis["seven_so_whats"]),
        "{{INTENT_GAP_ANALYSIS}}": render_gaps(analysis["intent_gap_analysis"]),
        "{{AMBIGUITY_REGISTER}}": render_ambiguities(analysis["ambiguity_register"]),
        "{{ACTIONABILITY_SCORE}}": (
            f"- [CODE] score={analysis['actionability_score']['score']} "
            f"band={analysis['actionability_score']['band']} "
            f"drivers={analysis['actionability_score']['drivers']}"
        ),
        "{{CLARIFIED_PROMPT}}": f"- [INFERENCE] {analysis['clarified_prompt']}",
        "{{ROUTING_HINTS}}": (
            f"- [CODE] next_action={analysis['routing_hints']['next_action']}\n"
            f"- [CODE] suggested_downstream={analysis['routing_hints']['suggested_downstream']}\n"
            f"- [CODE] quality_level={analysis['routing_hints']['quality_level']}\n"
            f"- [CODE] offline_only={str(analysis['routing_hints']['offline_only']).lower()}"
        ),
        "{{SAFETY_PRIVACY_FLAGS}}": render_safety(analysis["user_safety_privacy_flags"]),
        "{{CONFIDENCE}}": (
            f"- [CODE] overall={analysis['confidence']['overall']}\n"
            f"- [CODE] per_pass={analysis['confidence']['per_pass']}\n"
            f"- [DOC] aggregation_rule={analysis['confidence']['aggregation_rule']}"
        ),
    }
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile offline input analysis")
    parser.add_argument("--input", required=True, help="JSON input file")
    parser.add_argument("--output", help="Output path; defaults to stdout")
    parser.add_argument("--json", action="store_true", help="Emit stable JSON instead of Markdown")
    args = parser.parse_args()

    try:
        assets = load_assets()
        data = load_json(Path(args.input))
        validate_input(data, assets)
        analysis = build_analysis(data, assets)
        if args.json:
            content = json.dumps(analysis, indent=2, sort_keys=True) + "\n"
        else:
            template = assets["template"]
            if not isinstance(template, str):
                raise ValueError("template asset must be text")
            content = render_markdown(analysis, template)
        if args.output:
            Path(args.output).write_text(content, encoding="utf-8")
        else:
            print(content, end="")
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
