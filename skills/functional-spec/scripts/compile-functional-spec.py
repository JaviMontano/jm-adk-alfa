#!/usr/bin/env python3
"""Compile a deterministic functional specification from a structured JSON spec."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def validate_use_cases(spec: dict[str, Any], schema: dict[str, Any]) -> None:
    use_cases = require_list(spec, "use_cases")
    minimum = int(schema["minimum_count"])
    if len(use_cases) < minimum:
        raise ValueError(f"use_cases must contain at least {minimum} entries")
    id_re = re.compile(str(schema["id_pattern"]))
    required = set(schema["required_fields"])
    seen: set[str] = set()
    for case in use_cases:
        if not isinstance(case, dict):
            raise ValueError("each use case must be an object")
        missing = required - set(case)
        if missing:
            raise ValueError(f"use case missing fields: {sorted(missing)}")
        case_id = str(case["id"])
        if not id_re.fullmatch(case_id):
            raise ValueError(f"use case id must match {schema['id_pattern']}: {case_id}")
        if case_id in seen:
            raise ValueError(f"duplicate use case id: {case_id}")
        seen.add(case_id)
        if not isinstance(case["main_flow"], list) or not case["main_flow"]:
            raise ValueError(f"main_flow must be non-empty for {case_id}")
        if not isinstance(case["acceptance"], list) or not case["acceptance"]:
            raise ValueError(f"acceptance must be non-empty for {case_id}")


def validate_business_rules(spec: dict[str, Any], taxonomy: dict[str, Any]) -> None:
    rules = require_list(spec, "business_rules")
    id_re = re.compile(str(taxonomy["id_pattern"]))
    allowed = set(taxonomy["rule_types"])
    required = set(taxonomy["required_fields"])
    use_case_ids = {case["id"] for case in spec["use_cases"]}
    seen: set[str] = set()
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("each business rule must be an object")
        missing = required - set(rule)
        if missing:
            raise ValueError(f"business rule missing fields: {sorted(missing)}")
        rule_id = str(rule["id"])
        if not id_re.fullmatch(rule_id):
            raise ValueError(f"business rule id must match {taxonomy['id_pattern']}: {rule_id}")
        if rule_id in seen:
            raise ValueError(f"duplicate business rule id: {rule_id}")
        seen.add(rule_id)
        if rule["type"] not in allowed:
            raise ValueError(f"unsupported business rule type for {rule_id}: {rule['type']}")
        linked = rule["use_cases"]
        if not isinstance(linked, list) or not linked:
            raise ValueError(f"business rule must link use cases: {rule_id}")
        unknown = [case for case in linked if case not in use_case_ids]
        if unknown:
            raise ValueError(f"business rule {rule_id} links unknown use cases: {unknown}")


def validate_firestore(spec: dict[str, Any], firestore_template: dict[str, Any]) -> None:
    data_model = spec.get("firestore_model")
    if not isinstance(data_model, dict):
        raise ValueError("firestore_model must be an object")
    collections = data_model.get("collections")
    if not isinstance(collections, list) or not collections:
        raise ValueError("firestore_model.collections must be a non-empty list")
    required = set(firestore_template["required_collection_fields"])
    for collection in collections:
        if not isinstance(collection, dict):
            raise ValueError("each Firestore collection must be an object")
        missing = required - set(collection)
        if missing:
            raise ValueError(f"Firestore collection missing fields: {sorted(missing)}")
        if not collection.get("required_fields"):
            raise ValueError(f"Firestore collection required_fields cannot be empty: {collection.get('name')}")


def validate_spec(spec: dict[str, Any], base: Path) -> None:
    for key in ["product_name", "evidence", "mvp_modules", "out_of_scope", "open_questions"]:
        if key not in spec:
            raise ValueError(f"missing required section: {key}")
    if not str(spec["product_name"]).strip():
        raise ValueError("product_name is required")
    if not isinstance(spec["evidence"], dict):
        raise ValueError("evidence must be an object")
    require_list(spec, "mvp_modules")
    require_list(spec, "out_of_scope")
    require_list(spec, "open_questions")
    validate_use_cases(spec, load_json(base / "assets" / "use-case-schema.json"))
    validate_business_rules(spec, load_json(base / "assets" / "business-rule-taxonomy.json"))
    validate_firestore(spec, load_json(base / "assets" / "firestore-model-template.json"))


def lines_for_list(items: list[Any], prefix: str = "-") -> str:
    return "\n".join(f"{prefix} {item}" for item in items)


def render(spec: dict[str, Any], base: Path) -> str:
    template = (base / "assets" / "functional-spec-template.md").read_text(encoding="utf-8")
    evidence = spec["evidence"]
    evidence_summary = "\n".join(f"- {key}: {value}" for key, value in sorted(evidence.items()))
    modules = "\n".join(f"- `{module['id']}`: {module['name']} — {module['purpose']}" for module in spec["mvp_modules"])
    use_cases = []
    for case in spec["use_cases"]:
        use_cases.append(
            f"### {case['id']} — {case['goal']}\n"
            f"- Actor: {case['actor']}\n"
            f"- Trigger: {case['trigger']}\n"
            f"- Preconditions: {', '.join(case['preconditions'])}\n"
            f"- Main flow: {'; '.join(case['main_flow'])}\n"
            f"- Acceptance: {'; '.join(case['acceptance'])}"
        )
    rules = "\n".join(
        f"- `{rule['id']}` [{rule['type']}]: {rule['statement']} (source: {rule['source']}; use cases: {', '.join(rule['use_cases'])})"
        for rule in spec["business_rules"]
    )
    criteria = []
    for case in spec["use_cases"]:
        for criterion in case["acceptance"]:
            criteria.append(f"- `{case['id']}`: {criterion}")
    firestore = []
    for collection in spec["firestore_model"]["collections"]:
        firestore.append(
            f"- `{collection['name']}`: {collection['purpose']}; owner `{collection['owner']}`; "
            f"PII `{collection['pii']}`; fields {', '.join(collection['required_fields'])}; "
            f"indexes {', '.join(collection['indexes'])}; retention {collection['retention']}"
        )
    replacements = {
        "{{PRODUCT_NAME}}": str(spec["product_name"]),
        "{{EVIDENCE_SUMMARY}}": evidence_summary,
        "{{MVP_MODULES}}": modules,
        "{{USE_CASES}}": "\n\n".join(use_cases),
        "{{BUSINESS_RULES}}": rules,
        "{{ACCEPTANCE_CRITERIA}}": "\n".join(criteria),
        "{{FIRESTORE_MODEL}}": "\n".join(firestore),
        "{{OUT_OF_SCOPE}}": lines_for_list(spec["out_of_scope"]),
        "{{OPEN_QUESTIONS}}": lines_for_list(spec["open_questions"]),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic functional specification")
    parser.add_argument("--spec", required=True, help="Structured functional spec JSON")
    parser.add_argument("--output", help="Write Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        spec = load_json(Path(args.spec))
        validate_spec(spec, base)
        output = render(spec, base)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
