#!/usr/bin/env python3
"""Compile deterministic context window engineering reports from JSON specs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_required_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        require(field in obj and obj[field] not in ("", None), f"{label} missing required field: {field}", errors)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for item in value.values():
            strings.extend(flatten_strings(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(flatten_strings(item))
        return strings
    return []


def block_label(block: dict[str, Any]) -> str:
    return f"block {block.get('id', '<missing>')}"


def validate_context_window(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    window = as_dict(spec.get("contextWindow"))
    validate_required_fields(window, schema["requiredContextWindowFields"], "contextWindow", errors)
    max_tokens = window.get("maxTokens")
    steady_tokens = window.get("expectedSteadyStateTokens")
    require(isinstance(max_tokens, int) and max_tokens > 0, "contextWindow.maxTokens must be positive integer", errors)
    require(
        isinstance(steady_tokens, int) and isinstance(max_tokens, int) and 0 < steady_tokens <= max_tokens,
        "contextWindow.expectedSteadyStateTokens must be positive and <= maxTokens",
        errors,
    )


def validate_blocks(blocks: list[Any], required_fields: list[str], label: str, errors: list[str]) -> list[dict[str, Any]]:
    normalized = [as_dict(item) for item in blocks]
    require(bool(normalized), f"{label} requires at least one block", errors)
    seen: set[str] = set()
    for index, block in enumerate(normalized, start=1):
        item_label = f"{label} block {index}"
        validate_required_fields(block, required_fields, item_label, errors)
        block_id = str(block.get("id", ""))
        require(nonempty(block_id), f"{item_label} id must be non-empty", errors)
        require(block_id not in seen, f"duplicate block id: {block_id}", errors)
        seen.add(block_id)
    return normalized


def validate_static_prefix(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> set[str]:
    prefix = as_dict(spec.get("staticPrefix"))
    validate_required_fields(prefix, ["blocks"], "staticPrefix", errors)
    blocks = validate_blocks(as_list(prefix.get("blocks")), schema["requiredBlockFields"], "staticPrefix", errors)
    allowed_kinds = set(policy["staticPrefix"]["allowedKinds"])
    blocked_tokens = [str(item).lower() for item in policy["staticPrefix"]["blockedVolatileTokens"]]
    block_ids: set[str] = set()
    for block in blocks:
        label = block_label(block)
        block_ids.add(str(block["id"]))
        kind = str(block.get("kind", ""))
        require(kind in allowed_kinds, f"{label} kind not allowed in static prefix: {kind}", errors)
        require(block.get("stable") is True, f"{label} must be stable", errors)
        joined = "\n".join(flatten_strings(block)).lower()
        for token in blocked_tokens:
            if token in joined:
                errors.append(f"{label} contains volatile token in static prefix: {token}")
    return block_ids


def validate_middle(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> set[str]:
    middle = as_dict(spec.get("middle"))
    validate_required_fields(middle, schema["requiredMiddleFields"], "middle", errors)
    require(middle.get("compactable") is True, "middle.compactable must be true", errors)
    blocks = validate_blocks(as_list(middle.get("blocks")), schema["requiredBlockFields"], "middle", errors)
    return {str(block["id"]) for block in blocks}


def validate_dynamic_tail(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> set[str]:
    tail = as_dict(spec.get("dynamicTail"))
    validate_required_fields(tail, schema["requiredDynamicTailFields"], "dynamicTail", errors)
    require(tail.get("position") == policy["dynamicTail"]["requiredPosition"], "dynamicTail.position must be final", errors)
    blocks = validate_blocks(as_list(tail.get("blocks")), schema["requiredBlockFields"], "dynamicTail", errors)
    require(str(blocks[-1].get("kind")) == policy["dynamicTail"]["requiredKind"], "dynamicTail final block must be reminder", errors)
    volatile_count = 0
    for block in blocks:
        label = block_label(block)
        require(block.get("stable") is False, f"{label} in dynamicTail must not be stable", errors)
        volatile_fields = as_list(block.get("volatileFields"))
        volatile_count += len(volatile_fields)
    require(volatile_count > 0, "dynamicTail must declare volatileFields", errors)
    return {str(block["id"]) for block in blocks}


def validate_critical_rules(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> list[str]:
    rules = [as_dict(item) for item in as_list(spec.get("criticalRules"))]
    require(bool(rules), "criticalRules requires at least one rule", errors)
    required_placements = set(policy["criticalRules"]["requiredPlacements"])
    rule_ids: list[str] = []
    for index, rule in enumerate(rules, start=1):
        label = f"criticalRule {index}"
        validate_required_fields(rule, schema["requiredCriticalRuleFields"], label, errors)
        rule_ids.append(str(rule.get("id", "")))
        placements = {str(item) for item in as_list(rule.get("placements"))}
        missing = sorted(required_placements - placements)
        require(not missing, f"{label} missing edge placements: {', '.join(missing)}", errors)
        require(nonempty(rule.get("text")), f"{label}.text must be non-empty", errors)
    return rule_ids


def validate_compaction(
    spec: dict[str, Any],
    schema: dict[str, Any],
    policy: dict[str, Any],
    static_ids: set[str],
    middle_ids: set[str],
    tail_ids: set[str],
    errors: list[str],
) -> None:
    compaction = as_dict(spec.get("compaction"))
    validate_required_fields(compaction, schema["requiredCompactionFields"], "compaction", errors)
    require(compaction.get("enabled") is True, "compaction.enabled must be true", errors)
    threshold = compaction.get("threshold")
    require(isinstance(threshold, (int, float)), "compaction.threshold must be numeric", errors)
    if isinstance(threshold, (int, float)):
        require(threshold >= policy["compaction"]["minThreshold"], "compaction.threshold below minimum", errors)
        require(threshold <= policy["compaction"]["maxThreshold"], "compaction.threshold above maximum", errors)
    preserve_ids = {str(item) for item in as_list(compaction.get("preserveBlockIds"))}
    require(bool(static_ids & preserve_ids), "compaction must preserve at least one static prefix block", errors)
    require(bool(tail_ids & preserve_ids), "compaction must preserve at least one dynamic tail block", errors)
    summarize_kinds = {str(item) for item in as_list(compaction.get("summarizeBlockKinds"))}
    require(bool(summarize_kinds), "compaction.summarizeBlockKinds must be non-empty", errors)
    require(bool(middle_ids), "compaction requires middle blocks to summarize", errors)


def validate_validation(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    validation = as_dict(spec.get("validation"))
    validate_required_fields(validation, schema["requiredValidationFields"], "validation", errors)
    for field in schema["requiredValidationFields"]:
        require(validation.get(field) is True, f"validation.{field} must be true", errors)


def validate_antipatterns(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    joined = "\n".join(flatten_strings(spec)).lower()
    for token in policy["blockedAntiPatterns"]:
        if token in joined:
            errors.append(f"blocked anti-pattern token present: {token}")


def validate(spec: dict[str, Any]) -> None:
    schema = load_json(ASSET_DIR / "context-assembly-schema.json")
    policy = load_json(ASSET_DIR / "context-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["requiredTopLevel"], "contextAssembly", errors)
    if errors:
        raise ValueError("\n".join(errors))
    require(nonempty(spec.get("application")), "application must be non-empty", errors)
    validate_context_window(spec, schema, errors)
    static_ids = validate_static_prefix(spec, schema, policy, errors)
    middle_ids = validate_middle(spec, schema, errors)
    tail_ids = validate_dynamic_tail(spec, schema, policy, errors)
    validate_critical_rules(spec, schema, policy, errors)
    validate_compaction(spec, schema, policy, static_ids, middle_ids, tail_ids, errors)
    validate_validation(spec, schema, errors)
    require(bool(as_list(spec.get("risks"))), "risks requires at least one item", errors)
    validate_antipatterns(spec, policy, errors)
    if errors:
        raise ValueError("\n".join(errors))


def bullet_list(items: list[Any]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_blocks(blocks: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for block in blocks:
        lines.extend(
            [
                f"### {block['id']}",
                "",
                f"- Kind: `{block['kind']}`",
                f"- Stable: `{block['stable']}`",
                f"- Content: {block['content']}",
                "",
            ]
        )
        if as_list(block.get("volatileFields")):
            lines.append(f"- Volatile fields: {', '.join(str(item) for item in block['volatileFields'])}")
            lines.append("")
    return "\n".join(lines).strip()


def render_critical_rules(rules: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for rule in rules:
        lines.append(f"- `{rule['id']}`: {rule['text']} (placements: {', '.join(rule['placements'])})")
    return "\n".join(lines)


def render_report(spec: dict[str, Any]) -> str:
    template = (ASSET_DIR / "context-report-template.md").read_text(encoding="utf-8")
    static_blocks = [as_dict(item) for item in spec["staticPrefix"]["blocks"]]
    middle_blocks = [as_dict(item) for item in spec["middle"]["blocks"]]
    tail_blocks = [as_dict(item) for item in spec["dynamicTail"]["blocks"]]
    compaction = spec["compaction"]
    return template.format(
        application=spec["application"],
        maxTokens=spec["contextWindow"]["maxTokens"],
        expectedSteadyStateTokens=spec["contextWindow"]["expectedSteadyStateTokens"],
        compactionThreshold=compaction["threshold"],
        staticPrefixIds=", ".join(block["id"] for block in static_blocks),
        dynamicTailIds=", ".join(block["id"] for block in tail_blocks),
        staticPrefixMarkdown=render_blocks(static_blocks),
        middleMarkdown=render_blocks(middle_blocks),
        dynamicTailMarkdown=render_blocks(tail_blocks),
        criticalRulesMarkdown=render_critical_rules([as_dict(item) for item in spec["criticalRules"]]),
        compactionEnabled=compaction["enabled"],
        preserveBlockIds=", ".join(compaction["preserveBlockIds"]),
        summarizeBlockKinds=", ".join(compaction["summarizeBlockKinds"]),
        risksMarkdown=bullet_list(spec["risks"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a context window engineering contract")
    parser.add_argument("input", type=Path, help="Path to context assembly JSON contract")
    parser.add_argument("--output", type=Path, help="Write generated report")
    args = parser.parse_args()
    try:
        spec = load_json(args.input)
        validate(spec)
        report = render_report(spec)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
