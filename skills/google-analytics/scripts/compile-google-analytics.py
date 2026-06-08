#!/usr/bin/env python3
"""Compile a deterministic GA4/GTM measurement plan from JSON.

This script is intentionally offline. It reads local assets and fixtures only;
it never calls Google Analytics, Google Tag Manager, OAuth, MCP, or the network.
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


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def require_fields(data: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def require_list(data: dict[str, Any], key: str, *, non_empty: bool = True) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    if non_empty and not value:
        raise ValueError(f"{key} must be a non-empty list")
    return value


def require_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def validate_root(data: dict[str, Any], schema: dict[str, Any]) -> None:
    require_fields(data, schema["required_root_fields"], "root")
    mode = data["implementation_mode"]
    if mode in schema["blocked_implementation_modes"]:
        raise ValueError("Measurement Protocol must supplement tagging; measurement_protocol_only is blocked")
    if mode not in schema["allowed_implementation_modes"]:
        raise ValueError(f"unsupported implementation_mode: {mode}")


def validate_property_state(data: dict[str, Any], schema: dict[str, Any]) -> None:
    state = require_object(data, "property_state")
    require_fields(state, schema["required_property_state_fields"], "property_state")
    for field in schema["required_property_state_fields"]:
        require_bool(state[field], f"property_state.{field}")


def validate_measurement_strategy(data: dict[str, Any], schema: dict[str, Any]) -> None:
    strategy = require_object(data, "measurement_strategy")
    require_fields(strategy, schema["required_measurement_strategy_fields"], "measurement_strategy")
    if strategy["implementation_surface"] not in schema["allowed_implementation_surfaces"]:
        raise ValueError(f"unsupported measurement_strategy.implementation_surface: {strategy['implementation_surface']}")
    for field in ["primary_business_goal", "owner"]:
        if not str(strategy[field]).strip():
            raise ValueError(f"measurement_strategy.{field} must be non-empty")
    for field in ["reporting_questions", "kpis"]:
        values = strategy[field]
        if not isinstance(values, list) or not values or any(not str(item).strip() for item in values):
            raise ValueError(f"measurement_strategy.{field} must be a non-empty string list")


def validate_consent_privacy(
    data: dict[str, Any],
    schema: dict[str, Any],
    privacy_policy: dict[str, Any],
    *,
    workflow_mutates: bool,
) -> None:
    consent = require_object(data, "consent_privacy")
    require_fields(consent, schema["required_consent_privacy_fields"], "consent_privacy")
    if consent["consent_mode_plan"] not in schema["allowed_consent_mode_plans"]:
        raise ValueError(f"unsupported consent_mode_plan: {consent['consent_mode_plan']}")
    for field in ["cmp_present", "default_denied_before_consent", "ads_personalization_review", "data_redaction_review"]:
        require_bool(consent[field], f"consent_privacy.{field}")
    for field in ["region_profile", "pii_policy", "legal_review_owner"]:
        if not str(consent[field]).strip():
            raise ValueError(f"consent_privacy.{field} must be non-empty")
    if workflow_mutates and not str(consent["legal_review_owner"]).strip():
        raise ValueError(privacy_policy["blocking_rules"]["missing_legal_owner"])
    if workflow_mutates and consent["consent_mode_plan"] == "to_be_confirmed":
        raise ValueError(privacy_policy["blocking_rules"]["consent_required_unknown"])


def validate_parameter(
    parameter: dict[str, Any],
    schema: dict[str, Any],
    taxonomy: dict[str, Any],
    privacy_policy: dict[str, Any],
    event_id: str,
) -> None:
    require_fields(parameter, schema["required_parameter_fields"], f"parameter for {event_id}")
    if not re.match(schema["event_name_pattern"], str(parameter["name"])):
        raise ValueError(f"parameter.name must match lowercase_snake_case for {event_id}: {parameter['name']}")
    if parameter["type"] not in schema["allowed_parameter_types"]:
        raise ValueError(f"unsupported parameter.type for {event_id}: {parameter['type']}")
    if parameter["scope"] not in schema["allowed_parameter_scopes"]:
        raise ValueError(f"unsupported parameter.scope for {event_id}: {parameter['scope']}")
    if parameter["pii_risk"] not in schema["allowed_pii_risks"]:
        raise ValueError(f"unsupported parameter.pii_risk for {event_id}: {parameter['pii_risk']}")
    require_bool(parameter["required"], f"parameter.required for {event_id}")
    if parameter["pii_risk"] == "high":
        raise ValueError(f"PII risk high is blocking for {event_id}.{parameter['name']}")
    pii_names = {str(item) for item in privacy_policy["pii_blocklist_examples"]}
    if str(parameter["name"]) in pii_names:
        raise ValueError(f"PII-like parameter name is blocked for {event_id}.{parameter['name']}")
    if not str(parameter["value_source"]).strip():
        raise ValueError(f"parameter.value_source must be non-empty for {event_id}.{parameter['name']}")
    if taxonomy["parameter_rules"]["currency_required_when_value_is_monetary"]:
        if parameter["name"] == "value" and parameter["type"] != "number":
            raise ValueError(f"value parameter must be numeric for {event_id}")


def validate_events(
    data: dict[str, Any],
    schema: dict[str, Any],
    taxonomy: dict[str, Any],
    privacy_policy: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    events = require_list(data, "events")
    event_by_name: dict[str, dict[str, Any]] = {}
    event_ids: set[str] = set()
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("each event must be an object")
        require_fields(event, schema["required_event_fields"], "event")
        if event["id"] in event_ids:
            raise ValueError(f"duplicate event id: {event['id']}")
        event_ids.add(str(event["id"]))
        event_name = str(event["event_name"])
        if not re.match(schema["event_name_pattern"], event_name):
            raise ValueError(f"event_name must match lowercase_snake_case: {event_name}")
        if event_name in event_by_name:
            raise ValueError(f"duplicate event_name: {event_name}")
        if event["event_type"] not in schema["allowed_event_types"]:
            raise ValueError(f"unsupported event_type for {event_name}: {event['event_type']}")
        if event["implementation_surface"] not in schema["allowed_event_surfaces"]:
            raise ValueError(f"unsupported event implementation_surface for {event_name}: {event['implementation_surface']}")
        for field in ["recommended_event_candidate", "key_event_candidate"]:
            require_bool(event[field], f"event.{field} for {event_name}")
        if event["event_type"] == "recommended" and event["recommended_event_candidate"] is not True:
            raise ValueError(f"recommended event must set recommended_event_candidate=true: {event_name}")
        if event["event_type"] == "custom" and not str(event.get("custom_event_justification", "")).strip():
            raise ValueError(f"custom event requires custom_event_justification: {event_name}")
        parameters = require_list(event, "parameters", non_empty=False)
        for parameter in parameters:
            if not isinstance(parameter, dict):
                raise ValueError(f"each parameter must be an object for {event_name}")
            validate_parameter(parameter, schema, taxonomy, privacy_policy, event_name)
        for field in ["business_goal", "user_action", "trigger", "privacy_review", "debug_expectation"]:
            if not str(event[field]).strip():
                raise ValueError(f"event.{field} must be non-empty for {event_name}")
        event_by_name[event_name] = event
    return event_by_name


def validate_key_events(data: dict[str, Any], schema: dict[str, Any], event_by_name: dict[str, dict[str, Any]]) -> None:
    key_events = require_list(data, "key_events")
    for item in key_events:
        if not isinstance(item, dict):
            raise ValueError("each key event must be an object")
        require_fields(item, schema["required_key_event_fields"], "key_event")
        event_name = str(item["event_name"])
        if event_name not in event_by_name:
            raise ValueError(f"key_event references unknown event_name: {event_name}")
        if event_by_name[event_name]["key_event_candidate"] is not True:
            raise ValueError(f"key_event requires event.key_event_candidate=true: {event_name}")
        if item["value_strategy"] not in schema["allowed_value_strategies"]:
            raise ValueError(f"unsupported value_strategy for {event_name}: {item['value_strategy']}")
        require_bool(item["currency_required"], f"key_event.currency_required for {event_name}")
        if item["value_strategy"] == "monetary" and item["currency_required"] is not True:
            raise ValueError(f"monetary key_event requires currency_required=true: {event_name}")
        for field in ["business_reason", "expected_volume", "owner"]:
            if not str(item[field]).strip():
                raise ValueError(f"key_event.{field} must be non-empty for {event_name}")


def validate_tags(data: dict[str, Any], schema: dict[str, Any]) -> bool:
    tags = require_list(data, "tags")
    tag_ids: set[str] = set()
    workflow_mutates = False
    for tag in tags:
        if not isinstance(tag, dict):
            raise ValueError("each tag must be an object")
        require_fields(tag, schema["required_tag_fields"], "tag")
        if tag["id"] in tag_ids:
            raise ValueError(f"duplicate tag id: {tag['id']}")
        tag_ids.add(str(tag["id"]))
        if tag["platform"] not in schema["allowed_tag_platforms"]:
            raise ValueError(f"unsupported tag.platform for {tag['id']}: {tag['platform']}")
        if tag["tag_type"] not in schema["allowed_tag_types"]:
            raise ValueError(f"unsupported tag.tag_type for {tag['id']}: {tag['tag_type']}")
        require_bool(tag["mutation_requested"], f"tag.mutation_requested for {tag['id']}")
        workflow_mutates = workflow_mutates or tag["mutation_requested"]
        for field in ["tag_name", "trigger_name", "verification"]:
            if not str(tag[field]).strip():
                raise ValueError(f"tag.{field} must be non-empty for {tag['id']}")
        checks = tag["consent_checks"]
        if not isinstance(checks, list) or not checks or any(not str(check).strip() for check in checks):
            raise ValueError(f"tag.consent_checks must be a non-empty string list for {tag['id']}")
    return workflow_mutates


def validate_debug_plan(data: dict[str, Any], schema: dict[str, Any]) -> None:
    debug = require_object(data, "debug_plan")
    require_fields(debug, schema["required_debug_plan_fields"], "debug_plan")
    for field in schema["required_debug_plan_fields"]:
        require_bool(debug[field], f"debug_plan.{field}")


def validate_confirmation(
    data: dict[str, Any],
    confirmation_policy: dict[str, Any],
    *,
    workflow_mutates: bool,
) -> None:
    confirmation = require_object(data, "human_confirmation")
    require_fields(confirmation, ["status", "confirmed_by", "confirmation_text", "mutations_allowed"], "human_confirmation")
    require_bool(confirmation["mutations_allowed"], "human_confirmation.mutations_allowed")
    if not workflow_mutates:
        return
    if confirmation["status"] != confirmation_policy["required_status"]:
        raise ValueError("mutating GA4/GTM plan requires human_confirmation.status=confirmed")
    if not str(confirmation["confirmed_by"]).strip():
        raise ValueError("mutating GA4/GTM plan requires human_confirmation.confirmed_by")
    prefix = str(confirmation_policy["confirmation_phrase_prefix"])
    if not str(confirmation["confirmation_text"]).startswith(prefix):
        raise ValueError(f"human_confirmation.confirmation_text must start with {prefix}")
    if confirmation["mutations_allowed"] is not True:
        raise ValueError("mutating GA4/GTM plan requires human_confirmation.mutations_allowed=true")


def validate_evidence(data: dict[str, Any], schema: dict[str, Any]) -> None:
    evidence = require_object(data, "evidence")
    require_fields(evidence, schema["required_evidence_fields"], "evidence")
    for field in schema["required_evidence_fields"]:
        if not str(evidence[field]).strip():
            raise ValueError(f"evidence.{field} must be non-empty")


def validate_input(data: dict[str, Any], assets: dict[str, dict[str, Any]]) -> bool:
    schema = assets["schema"]
    validate_root(data, schema)
    validate_property_state(data, schema)
    validate_measurement_strategy(data, schema)
    workflow_mutates = validate_tags(data, schema)
    validate_consent_privacy(data, schema, assets["privacy_policy"], workflow_mutates=workflow_mutates)
    event_by_name = validate_events(data, schema, assets["taxonomy"], assets["privacy_policy"])
    validate_key_events(data, schema, event_by_name)
    validate_debug_plan(data, schema)
    validate_confirmation(data, assets["confirmation_policy"], workflow_mutates=workflow_mutates)
    validate_evidence(data, schema)
    return workflow_mutates


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [DOC] {key}: {value}" for key, value in sorted(evidence.items()))


def bool_status(value: bool) -> str:
    return "yes" if value else "no"


def property_checklist(data: dict[str, Any]) -> str:
    state = data["property_state"]
    lines = ["| Check | Status |", "|---|---|"]
    labels = {
        "ga4_account_created": "GA4 account created",
        "ga4_property_created": "GA4 property created",
        "web_data_stream_created": "Web data stream created",
        "measurement_id_known": "Measurement ID known",
        "enhanced_measurement_reviewed": "Enhanced measurement reviewed"
    }
    for key, label in labels.items():
        lines.append(f"| {label} | {bool_status(state[key])} |")
    return "\n".join(lines)


def measurement_strategy_lines(data: dict[str, Any]) -> str:
    strategy = data["measurement_strategy"]
    questions = "\n".join(f"- [CODE] {item}" for item in strategy["reporting_questions"])
    kpis = "\n".join(f"- [CODE] {item}" for item in strategy["kpis"])
    return "\n".join(
        [
            f"- [CODE] Owner: {strategy['owner']}.",
            f"- [CODE] Implementation surface: `{strategy['implementation_surface']}`.",
            "",
            "### Reporting Questions",
            questions,
            "",
            "### KPIs",
            kpis,
        ]
    )


def event_table(data: dict[str, Any]) -> str:
    lines = [
        "| Event | Type | Surface | Goal | Key Event Candidate | Debug Expectation |",
        "|---|---|---|---|---|---|",
    ]
    for event in data["events"]:
        lines.append(
            f"| `{event['event_name']}` | {event['event_type']} | {event['implementation_surface']} | "
            f"{event['business_goal']} | {bool_status(event['key_event_candidate'])} | {event['debug_expectation']} |"
        )
    return "\n".join(lines)


def parameter_table(data: dict[str, Any]) -> str:
    lines = [
        "| Event | Parameter | Type | Scope | Required | PII Risk | Source |",
        "|---|---|---|---|---|---|---|",
    ]
    has_parameters = False
    for event in data["events"]:
        for parameter in event["parameters"]:
            has_parameters = True
            lines.append(
                f"| `{event['event_name']}` | `{parameter['name']}` | {parameter['type']} | {parameter['scope']} | "
                f"{bool_status(parameter['required'])} | {parameter['pii_risk']} | {parameter['value_source']} |"
            )
    if not has_parameters:
        lines.append("| [CODE] No custom parameters supplied | - | - | - | - | - | - |")
    return "\n".join(lines)


def key_event_plan(data: dict[str, Any]) -> str:
    lines = [
        "| Event | Reason | Value Strategy | Currency Required | Expected Volume | Owner |",
        "|---|---|---|---|---|---|",
    ]
    for event in data["key_events"]:
        lines.append(
            f"| `{event['event_name']}` | {event['business_reason']} | {event['value_strategy']} | "
            f"{bool_status(event['currency_required'])} | {event['expected_volume']} | {event['owner']} |"
        )
    return "\n".join(lines)


def tag_plan(data: dict[str, Any]) -> str:
    lines = [
        "| ID | Platform | Tag Type | Tag Name | Trigger | Mutation Requested | Verification |",
        "|---|---|---|---|---|---|---|",
    ]
    for tag in data["tags"]:
        lines.append(
            f"| {tag['id']} | {tag['platform']} | {tag['tag_type']} | `{tag['tag_name']}` | "
            f"`{tag['trigger_name']}` | {bool_status(tag['mutation_requested'])} | {tag['verification']} |"
        )
    return "\n".join(lines)


def consent_privacy_lines(data: dict[str, Any], privacy_policy: dict[str, Any]) -> str:
    consent = data["consent_privacy"]
    checks = "\n".join(f"- [DOC] {check}" for check in privacy_policy["consent_checks"])
    return "\n".join(
        [
            f"- [CODE] Region profile: {consent['region_profile']}.",
            f"- [CODE] CMP present: {bool_status(consent['cmp_present'])}.",
            f"- [CODE] Consent Mode plan: `{consent['consent_mode_plan']}`.",
            f"- [CODE] Default denied before consent: {bool_status(consent['default_denied_before_consent'])}.",
            f"- [CODE] Ads personalization review: {bool_status(consent['ads_personalization_review'])}.",
            f"- [CODE] Data redaction review: {bool_status(consent['data_redaction_review'])}.",
            f"- [CODE] PII policy: {consent['pii_policy']}.",
            f"- [CODE] Legal review owner: {consent['legal_review_owner']}.",
            "",
            "### Required Checks",
            checks,
        ]
    )


def debug_checklist(data: dict[str, Any], debug_policy: dict[str, Any]) -> str:
    debug = data["debug_plan"]
    lines = ["| Check | Planned | Purpose |", "|---|---|---|"]
    for item in debug_policy["checks"]:
        lines.append(f"| {item['tool']} | {bool_status(debug[item['id']])} | {item['purpose']} |")
    gates = "\n".join(f"- [CODE] {gate}" for gate in debug_policy["publish_gate"])
    return "\n".join(lines + ["", "### Publish Gate", gates])


def confirmation_gate(data: dict[str, Any], confirmation_policy: dict[str, Any], workflow_mutates: bool) -> str:
    confirmation = data["human_confirmation"]
    lines = [
        f"- [CODE] Required status for mutations: `{confirmation_policy['required_status']}`.",
        f"- [CODE] Current status: `{confirmation['status']}`.",
        f"- [CODE] Confirmed by: `{confirmation['confirmed_by']}`.",
        f"- [CODE] Mutations allowed: {bool_status(confirmation['mutations_allowed'])}.",
        f"- [CODE] Confirmation text: {confirmation['confirmation_text']}",
    ]
    if workflow_mutates:
        lines.append("- [CODE] Live tag/container recommendations are blocked unless this confirmation is retained with the plan.")
    else:
        lines.append("- [CODE] No live tag/container mutation is requested by this plan.")
    return "\n".join(lines)


def validation_lines(data: dict[str, Any], workflow_mutates: bool) -> str:
    event_names = ", ".join(f"`{event['event_name']}`" for event in data["events"])
    key_events = ", ".join(f"`{event['event_name']}`" for event in data["key_events"])
    return "\n".join(
        [
            "- [CODE] Structured input passed GA4/GTM schema and policy validation.",
            f"- [CODE] Event taxonomy covered: {event_names}.",
            f"- [CODE] Key-event candidates covered: {key_events}.",
            f"- [CODE] Mutation gate required: {bool_status(workflow_mutates)}.",
            "- [CODE] Event names and parameter names follow lowercase_snake_case.",
            "- [CODE] No high-risk PII parameter was accepted.",
            "- [CODE] The compiler performed no network, OAuth, Google Analytics, GTM, or MCP calls.",
        ]
    )


def risk_lines(data: dict[str, Any]) -> str:
    risks = [
        "- [INFERENCE] This plan does not prove that a GA4 property, web stream, GTM container, or tag currently exists.",
        "- [INFERENCE] Live implementation still depends on account permissions, container workspace state, consent tooling, browser behavior, and human confirmation.",
        "- [INFERENCE] Standard GA4 reports can lag after implementation; DebugView and Realtime are only verification aids, not final business reporting.",
    ]
    if data["implementation_mode"] == "measurement_protocol_supplement":
        risks.append("- [DOC] Measurement Protocol should augment, not replace, tagging-based collection.")
    return "\n".join(risks)


def measurement_protocol_mode(data: dict[str, Any]) -> str:
    if data["implementation_mode"] == "measurement_protocol_supplement":
        return "supplement"
    surfaces = {event["implementation_surface"] for event in data["events"]}
    return "supplement" if "measurement_protocol_supplement" in surfaces else "not planned"


def render(data: dict[str, Any], base: Path, assets: dict[str, dict[str, Any]], workflow_mutates: bool) -> str:
    template = (base / "assets" / "ga4-gtm-plan-template.md").read_text(encoding="utf-8")
    strategy = data["measurement_strategy"]
    replacements = {
        "{{PLAN_ID}}": str(data["plan_id"]),
        "{{REQUEST_TITLE}}": str(data["request_title"]),
        "{{IMPLEMENTATION_MODE}}": str(data["implementation_mode"]),
        "{{MEASUREMENT_PROTOCOL_MODE}}": measurement_protocol_mode(data),
        "{{MUTATING_WORKFLOW}}": str(workflow_mutates),
        "{{PRIMARY_BUSINESS_GOAL}}": str(strategy["primary_business_goal"]),
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{PROPERTY_CHECKLIST}}": property_checklist(data),
        "{{MEASUREMENT_STRATEGY}}": measurement_strategy_lines(data),
        "{{EVENT_TABLE}}": event_table(data),
        "{{PARAMETER_TABLE}}": parameter_table(data),
        "{{KEY_EVENT_PLAN}}": key_event_plan(data),
        "{{TAG_PLAN}}": tag_plan(data),
        "{{CONSENT_PRIVACY}}": consent_privacy_lines(data, assets["privacy_policy"]),
        "{{DEBUG_CHECKLIST}}": debug_checklist(data, assets["debug_policy"]),
        "{{CONFIRMATION_GATE}}": confirmation_gate(data, assets["confirmation_policy"], workflow_mutates),
        "{{VALIDATION}}": validation_lines(data, workflow_mutates),
        "{{RISKS}}": risk_lines(data),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def load_assets(base: Path) -> dict[str, dict[str, Any]]:
    return {
        "schema": load_json(base / "assets" / "ga4-gtm-plan-schema.json"),
        "taxonomy": load_json(base / "assets" / "event-taxonomy-policy.json"),
        "privacy_policy": load_json(base / "assets" / "privacy-consent-policy.json"),
        "confirmation_policy": load_json(base / "assets" / "tag-mutation-confirmation-policy.json"),
        "debug_policy": load_json(base / "assets" / "debug-checklist-policy.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic GA4/GTM measurement plan")
    parser.add_argument("--input", required=True, help="Structured GA4/GTM JSON input")
    parser.add_argument("--output", help="Write Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        data = load_json(Path(args.input))
        assets = load_assets(base)
        workflow_mutates = validate_input(data, assets)
        output = render(data, base, assets, workflow_mutates)
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
