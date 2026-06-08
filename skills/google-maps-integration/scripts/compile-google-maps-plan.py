#!/usr/bin/env python3
"""Compile a deterministic Google Maps Platform plan from local JSON.

The compiler is intentionally offline. It reads only local assets and fixtures;
it never calls Google Maps Platform APIs, Cloud Console, OAuth, or package
registries.
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


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    return value


def text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(text_values(item))
        return values
    if isinstance(value, dict):
        values = []
        for item in value.values():
            values.extend(text_values(item))
        return values
    return []


def reject_monetary_amounts(data: dict[str, Any], schema: dict[str, Any]) -> None:
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in schema["forbidden_monetary_patterns"]]
    for value in text_values(data):
        if any(pattern.search(value) for pattern in patterns):
            raise ValueError("monetary prices are not allowed in google-maps-integration plans")


def validate_project(data: dict[str, Any], schema: dict[str, Any]) -> None:
    project = require_object(data, "project")
    require_fields(project, schema["required_project_fields"], "project")
    if project["platform"] not in schema["allowed_platforms"]:
        raise ValueError(f"unsupported project.platform: {project['platform']}")
    origins = require_list(project, "deployment_origins")
    if not origins:
        raise ValueError("project.deployment_origins must not be empty")


def validate_requirements(data: dict[str, Any], schema: dict[str, Any]) -> None:
    requirements = require_object(data, "requirements")
    require_fields(requirements, schema["required_requirements_fields"], "requirements")
    features = require_list(requirements, "features")
    invalid = [feature for feature in features if feature not in schema["allowed_features"]]
    if invalid:
        raise ValueError(f"unsupported requirement features: {invalid}")
    marker_count = requirements["marker_count_estimate"]
    if not isinstance(marker_count, int) or marker_count < 0:
        raise ValueError("requirements.marker_count_estimate must be a non-negative integer")


def selected_api_records(data: dict[str, Any], policy: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, Any]]:
    features = set(require_object(data, "requirements")["features"])
    requirements = data["requirements"]
    selected: list[dict[str, Any]] = []
    for record in policy["api_decisions"]:
        triggers = set(record["triggers"])
        needed = bool(features & triggers)
        if record["id"] == "places-api-new" and requirements["requires_places_autocomplete"]:
            needed = True
        if record["id"] == "geocoding-api" and requirements["requires_server_side_geocoding"]:
            needed = True
        if record["id"] == "directions-api-legacy" and requirements["requires_directions"]:
            needed = True
        if needed:
            selected.append(record)
    selected_labels = {record["label"] for record in selected}
    candidates = set(require_object(data, "apis").get("candidate_apis", []))
    missing = selected_labels - candidates
    if missing:
        raise ValueError(f"apis.candidate_apis missing selected APIs: {sorted(missing)}")
    for candidate in candidates:
        if candidate not in schema["allowed_candidate_apis"]:
            raise ValueError(f"unsupported candidate API: {candidate}")
    return selected


def selected_libraries(data: dict[str, Any], policy: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, Any]]:
    features = set(data["requirements"]["features"])
    map_ui = require_object(data, "map_ui")
    cluster = require_object(map_ui, "marker_clustering")
    threshold = int(cluster.get("threshold", schema["marker_cluster_threshold_default"]))
    marker_count = data["requirements"]["marker_count_estimate"]
    selected: list[dict[str, Any]] = []
    for record in policy["library_decisions"]:
        if record["id"] == "advanced-markers" and map_ui.get("advanced_markers"):
            selected.append(record)
        elif record["id"] == "marker-clusterer" and (cluster.get("enabled") or marker_count >= threshold):
            selected.append(record)
        elif record["trigger"] in features:
            selected.append(record)
    return selected


def validate_api_selection(data: dict[str, Any], policy: dict[str, Any], schema: dict[str, Any]) -> None:
    selected = selected_api_records(data, policy, schema)
    apis = require_object(data, "apis")
    if any(record["id"] == "directions-api-legacy" for record in selected):
        if apis.get("directions_legacy_acknowledged") is not True:
            raise ValueError("Directions API (Legacy) requires apis.directions_legacy_acknowledged=true")


def validate_keys(data: dict[str, Any], schema: dict[str, Any], selected: list[dict[str, Any]]) -> None:
    keys = require_list(data, "keys")
    if not keys:
        raise ValueError("keys must not be empty")
    restrictions_seen: set[str] = set()
    has_browser = False
    has_server = False
    for key in keys:
        if not isinstance(key, dict):
            raise ValueError("each key must be an object")
        require_fields(key, schema["required_key_fields"], "key")
        runtime = key["runtime"]
        if runtime not in schema["allowed_key_runtimes"]:
            raise ValueError(f"unsupported key runtime: {runtime}")
        allowed_restrictions = schema[f"{runtime}_application_restrictions"]
        if key["application_restriction"] not in allowed_restrictions:
            raise ValueError(f"{key['name']} has invalid {runtime} application restriction")
        api_restrictions = require_list(key, "api_restrictions")
        if not api_restrictions:
            raise ValueError(f"{key['name']} must restrict at least one API")
        invalid = [api for api in api_restrictions if api not in schema["allowed_api_restrictions"]]
        if invalid:
            raise ValueError(f"{key['name']} has unsupported API restrictions: {invalid}")
        restrictions_seen.update(str(api) for api in api_restrictions)
        if runtime == "browser":
            has_browser = True
            if not key.get("allowed_referrers"):
                raise ValueError(f"{key['name']} browser key requires allowed_referrers")
            if key.get("separate_from_server") is not True:
                raise ValueError(f"{key['name']} must be separate_from_server=true")
        if runtime == "server":
            has_server = True
            if not key.get("allowed_ips"):
                raise ValueError(f"{key['name']} server key requires allowed_ips")
            if key.get("separate_from_client") is not True:
                raise ValueError(f"{key['name']} must be separate_from_client=true")
    required_restrictions = {record["restriction_name"] for record in selected}
    missing = required_restrictions - restrictions_seen
    if missing:
        raise ValueError(f"selected APIs missing key restrictions: {sorted(missing)}")
    if has_browser and has_server and len(keys) < 2:
        raise ValueError("browser and server usage require separate keys")


def validate_data_flow(data: dict[str, Any], schema: dict[str, Any]) -> None:
    data_flow = require_object(data, "data_flow")
    require_fields(data_flow, schema["required_data_flow_sections"], "data_flow")
    places = require_object(data_flow, "places")
    if data["requirements"]["requires_places_autocomplete"] and places.get("session_tokens") is not True:
        raise ValueError("Places autocomplete requires data_flow.places.session_tokens=true")
    fields = require_list(places, "fields")
    if not fields:
        raise ValueError("data_flow.places.fields must not be empty")
    geocoding = require_object(data_flow, "geocoding")
    for field in ["cache_policy", "input_validation"]:
        if not str(geocoding.get(field, "")).strip():
            raise ValueError(f"data_flow.geocoding.{field} is required")
    directions = require_object(data_flow, "directions")
    if data["requirements"]["requires_directions"] and directions.get("legacy_acknowledged") is not True:
        raise ValueError("Directions flow requires data_flow.directions.legacy_acknowledged=true")
    for field in ["origin_source", "destination_source", "mode", "waypoints_policy"]:
        if not str(directions.get(field, "")).strip():
            raise ValueError(f"data_flow.directions.{field} is required")


def validate_map_ui(data: dict[str, Any], schema: dict[str, Any]) -> None:
    map_ui = require_object(data, "map_ui")
    if map_ui.get("advanced_markers") and map_ui.get("map_id_required") is not True:
        raise ValueError("Advanced Markers require map_ui.map_id_required=true")
    cluster = require_object(map_ui, "marker_clustering")
    threshold = cluster.get("threshold", schema["marker_cluster_threshold_default"])
    if not isinstance(threshold, int) or threshold <= 0:
        raise ValueError("map_ui.marker_clustering.threshold must be a positive integer")
    marker_count = data["requirements"]["marker_count_estimate"]
    if marker_count >= threshold and cluster.get("enabled") is not True:
        raise ValueError("dense marker plans require map_ui.marker_clustering.enabled=true")
    accessibility = require_object(map_ui, "accessibility")
    require_fields(accessibility, schema["required_accessibility_fields"], "map_ui.accessibility")
    for field in ["keyboard_paths", "marker_titles", "list_alternative"]:
        if accessibility[field] is not True:
            raise ValueError(f"map_ui.accessibility.{field} must be true")
    if not str(accessibility["map_summary"]).strip():
        raise ValueError("map_ui.accessibility.map_summary must not be empty")


def validate_billing_privacy_confirmation(data: dict[str, Any], schema: dict[str, Any]) -> None:
    billing = require_object(data, "billing_quota")
    require_fields(billing, schema["required_billing_quota_fields"], "billing_quota")
    for field in ["budgets_alerts_configured", "quotas_reviewed", "rate_limits_defined", "no_prices"]:
        if billing[field] is not True:
            raise ValueError(f"billing_quota.{field} must be true")
    if not str(billing["monitoring_owner"]).strip():
        raise ValueError("billing_quota.monitoring_owner must not be empty")
    privacy = require_object(data, "privacy")
    require_fields(privacy, schema["required_privacy_fields"], "privacy")
    if data["requirements"]["requires_personal_location"] and privacy["consent_required"] is not True:
        raise ValueError("personal location plans require privacy.consent_required=true")
    if privacy["human_confirmation_required"] is not True:
        raise ValueError("privacy.human_confirmation_required must be true")
    operations = require_object(data, "operations")
    require_fields(operations, schema["required_operation_fields"], "operations")
    if operations["offline_plan_only"] is not True:
        raise ValueError("operations.offline_plan_only must be true")
    if operations["external_api_calls"] is not False:
        raise ValueError("operations.external_api_calls must be false")
    confirmation = require_object(data, "human_confirmation")
    require_fields(confirmation, ["status", "confirmed_by", "confirmation_text"], "human_confirmation")
    if confirmation["status"] not in schema["confirmation_statuses"]:
        raise ValueError("human_confirmation.status must be confirmed")
    text = str(confirmation["confirmation_text"]).lower()
    if "offline" not in text or "do not call google apis" not in text:
        raise ValueError("human_confirmation.confirmation_text must include offline and do not call Google APIs")


def validate_input(
    data: dict[str, Any],
    schema: dict[str, Any],
    api_policy: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require_fields(data, schema["required_root_fields"], "root")
    if data["schema_version"] != schema["schema_version"]:
        raise ValueError(f"schema_version must be {schema['schema_version']}")
    reject_monetary_amounts(data, schema)
    validate_project(data, schema)
    validate_requirements(data, schema)
    validate_api_selection(data, api_policy, schema)
    selected_apis = selected_api_records(data, api_policy, schema)
    validate_keys(data, schema, selected_apis)
    validate_data_flow(data, schema)
    validate_map_ui(data, schema)
    validate_billing_privacy_confirmation(data, schema)
    evidence = require_object(data, "evidence")
    if not evidence:
        raise ValueError("evidence must not be empty")
    return selected_apis, selected_libraries(data, api_policy, schema)


def line_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def strip_leading_tag(text: str) -> str:
    return re.sub(r"^\[[A-Z]+\]\s+", "", text)


def checked(label: str, ok: bool, tag: str = "[CODE]") -> str:
    mark = "x" if ok else " "
    return f"- [{mark}] {tag} {label}"


def render_summary(data: dict[str, Any], selected_apis: list[dict[str, Any]], libraries: list[dict[str, Any]]) -> str:
    project = data["project"]
    api_names = ", ".join(record["label"] for record in selected_apis)
    library_names = ", ".join(record["label"] for record in libraries) or "no marker library"
    return "\n".join(
        [
            f"- [CODE] Project: `{project['name']}`.",
            f"- [CODE] Environment: `{project['environment']}` on `{project['platform']}`.",
            f"- [CODE] Review date: `{project['review_date']}`.",
            f"- [INFERENCE] Selected APIs: {api_names}.",
            f"- [INFERENCE] Selected map libraries/features: {library_names}.",
            "- [CONFIG] Output is an offline plan only; no external API calls are performed.",
        ]
    )


def render_evidence(data: dict[str, Any], policies: dict[str, dict[str, Any]]) -> str:
    lines = [f"- [CODE] {key}: {value}" for key, value in sorted(data["evidence"].items())]
    lines.extend(
        [
            f"- [DOC] Maps JavaScript API: {policies['api']['sources']['maps_javascript_api']}",
            f"- [DOC] Advanced Markers: {policies['api']['sources']['advanced_markers']}",
            f"- [DOC] Marker clustering: {policies['api']['sources']['marker_clustering']}",
            f"- [DOC] Geocoding API: {policies['data_flow']['sources']['geocoding_api']}",
            f"- [DOC] Places API: {policies['data_flow']['sources']['places_api']}",
            f"- [DOC] Directions API: {policies['data_flow']['sources']['directions_api']}",
            f"- [DOC] API security best practices: {policies['keys']['source']}",
        ]
    )
    return "\n".join(lines)


def render_api_selection(selected_apis: list[dict[str, Any]], libraries: list[dict[str, Any]]) -> str:
    sections: list[str] = []
    for record in selected_apis:
        controls = "; ".join(record["required_controls"])
        rationale = strip_leading_tag(record["rationale"])
        sections.append(f"- [DOC] `{record['label']}`: {rationale} Controls: {controls}.")
    for record in libraries:
        controls = "; ".join(record["required_controls"])
        rationale = strip_leading_tag(record["rationale"])
        sections.append(f"- [DOC] `{record['label']}`: {rationale} Controls: {controls}.")
    return "\n".join(sections)


def render_key_restrictions(data: dict[str, Any], key_policy: dict[str, Any]) -> str:
    lines = []
    for key in data["keys"]:
        restriction = key["application_restriction"]
        apis = ", ".join(key["api_restrictions"])
        lines.append(f"- [CODE] `{key['name']}` runtime `{key['runtime']}` uses `{restriction}` and APIs: {apis}.")
        if key["runtime"] == "browser":
            refs = ", ".join(key["allowed_referrers"])
            lines.append(f"  - [CODE] Allowed referrers: {refs}.")
        if key["runtime"] == "server":
            ips = ", ".join(key["allowed_ips"])
            lines.append(f"  - [CODE] Allowed IPs: {ips}.")
    lines.extend(f"- {item}" for item in key_policy["principles"])
    return "\n".join(lines)


def render_data_flow(data: dict[str, Any], data_policy: dict[str, Any]) -> str:
    flow = data["data_flow"]
    places = flow["places"]
    geocoding = flow["geocoding"]
    directions = flow["directions"]
    return "\n".join(
        [
            f"- [CODE] Places input: {places['input']}.",
            f"- [CODE] Places fields: {', '.join(places['fields'])}.",
            f"- [CODE] Places storage: {', '.join(places['store_fields'])}.",
            f"- [CODE] Places session tokens enabled: {places['session_tokens']}.",
            f"- [DOC] Places rationale: {strip_leading_tag(data_policy['places']['rationale'])}",
            f"- [CODE] Geocoding direction: {geocoding['direction']}.",
            f"- [CODE] Geocoding cache policy: {geocoding['cache_policy']}.",
            f"- [CODE] Geocoding input validation: {geocoding['input_validation']}.",
            f"- [DOC] Geocoding rationale: {strip_leading_tag(data_policy['geocoding']['rationale'])}",
            f"- [CODE] Directions mode: {directions['mode']}.",
            f"- [CODE] Directions origin/destination: {directions['origin_source']} -> {directions['destination_source']}.",
            f"- [CODE] Directions waypoints policy: {directions['waypoints_policy']}.",
            f"- [DOC] Directions rationale: {strip_leading_tag(data_policy['directions']['rationale'])}",
        ]
    )


def render_map_ui(data: dict[str, Any], marker_policy: dict[str, Any]) -> str:
    map_ui = data["map_ui"]
    cluster = map_ui["marker_clustering"]
    lines = [
        f"- [CODE] Advanced Markers enabled: {map_ui['advanced_markers']}.",
        f"- [CODE] Map ID required: {map_ui['map_id_required']}.",
        f"- [CODE] Marker clustering enabled: {cluster['enabled']} at threshold `{cluster['threshold']}`.",
        f"- [CODE] Marker clustering library: `{cluster['library']}`.",
        f"- [DOC] Advanced Markers policy: {strip_leading_tag(marker_policy['advanced_markers']['rationale'])}",
        f"- [DOC] Marker clustering policy: {strip_leading_tag(marker_policy['marker_clustering']['rationale'])}",
    ]
    return "\n".join(lines)


def render_accessibility_privacy(data: dict[str, Any], marker_policy: dict[str, Any]) -> str:
    accessibility = data["map_ui"]["accessibility"]
    privacy = data["privacy"]
    lines = [
        checked("Map summary is present.", bool(accessibility["map_summary"])),
        checked("Keyboard path exists for search, markers, and result list.", accessibility["keyboard_paths"]),
        checked("Markers include titles or accessible names.", accessibility["marker_titles"]),
        checked("Locations have a non-map list/table alternative.", accessibility["list_alternative"]),
        checked("Precise location collection is consent-gated.", privacy["consent_required"], "[CONFIG]"),
        f"- [CODE] Map summary: {accessibility['map_summary']}",
        f"- [CODE] Privacy retention: {privacy['retention']}.",
        f"- [CODE] Privacy redaction: {privacy['redaction']}.",
    ]
    lines.extend(f"- [DOC] Accessibility check: {item}." for item in marker_policy["accessibility_checks"])
    return "\n".join(lines)


def render_billing_quota(data: dict[str, Any], checklist_text: str) -> str:
    billing = data["billing_quota"]
    lines = [
        checked("Budget alerts configured.", billing["budgets_alerts_configured"], "[CONFIG]"),
        checked("Quotas reviewed.", billing["quotas_reviewed"], "[CONFIG]"),
        checked("Application rate limits defined.", billing["rate_limits_defined"], "[CODE]"),
        checked("No monetary prices included.", billing["no_prices"], "[CONFIG]"),
        f"- [CODE] Monitoring owner: `{billing['monitoring_owner']}`.",
        "",
        checklist_text.strip(),
    ]
    return "\n".join(lines)


def render_confirmation(data: dict[str, Any]) -> str:
    confirmation = data["human_confirmation"]
    operations = data["operations"]
    return "\n".join(
        [
            f"- [CODE] Status: `{confirmation['status']}`.",
            f"- [CODE] Confirmed by: `{confirmation['confirmed_by']}`.",
            f"- [CODE] Confirmation text: {confirmation['confirmation_text']}",
            f"- [CONFIG] Offline plan only: {operations['offline_plan_only']}.",
            f"- [CONFIG] External API calls: {operations['external_api_calls']}.",
        ]
    )


def render_implementation_checklist(data: dict[str, Any]) -> str:
    cluster = data["map_ui"]["marker_clustering"]
    return "\n".join(
        [
            checked("Enable selected APIs in the Google Cloud project before implementation.", True, "[CONFIG]"),
            checked("Create separate browser and server keys with the restrictions listed above.", True, "[CONFIG]"),
            checked("Load Maps JavaScript API only on screens that need a map.", True, "[INFERENCE]"),
            checked("Configure a map ID before using Advanced Markers.", data["map_ui"]["map_id_required"], "[DOC]"),
            checked(f"Use `{cluster['library']}` for dense markers.", cluster["enabled"], "[DOC]"),
            checked("Use Places session tokens and selected fields.", data["data_flow"]["places"]["session_tokens"], "[DOC]"),
            checked("Cache geocoding outputs and redact raw address logs.", True, "[CODE]"),
            checked("Keep Directions API (Legacy) behind explicit legacy acknowledgement.", data["data_flow"]["directions"]["legacy_acknowledged"], "[DOC]"),
            checked("Provide route steps and location results outside the map canvas.", data["map_ui"]["accessibility"]["list_alternative"], "[CODE]"),
        ]
    )


def render_risks(data: dict[str, Any]) -> str:
    risks = [
        "- [INFERENCE] Directions API is Legacy, so new production builds should evaluate newer routing services before final implementation.",
        "- [INFERENCE] Billing exposure remains possible if public traffic exceeds planned quota assumptions.",
        "- [INFERENCE] Accessibility still requires browser and assistive-technology testing after implementation.",
        "- [INFERENCE] Privacy controls still require legal/product confirmation for retention and consent wording.",
    ]
    if data["requirements"]["requires_personal_location"]:
        risks.append("- [CONFIG] Precise user location is in scope, so consent and redaction checks remain mandatory.")
    return "\n".join(risks)


def render_report(
    data: dict[str, Any],
    selected_apis: list[dict[str, Any]],
    libraries: list[dict[str, Any]],
    policies: dict[str, dict[str, Any]],
    template: str,
    checklist_text: str,
) -> str:
    replacements = {
        "{{SUMMARY}}": render_summary(data, selected_apis, libraries),
        "{{EVIDENCE}}": render_evidence(data, policies),
        "{{API_SELECTION}}": render_api_selection(selected_apis, libraries),
        "{{KEY_RESTRICTIONS}}": render_key_restrictions(data, policies["keys"]),
        "{{DATA_FLOW}}": render_data_flow(data, policies["data_flow"]),
        "{{MAP_UI}}": render_map_ui(data, policies["markers"]),
        "{{ACCESSIBILITY_PRIVACY}}": render_accessibility_privacy(data, policies["markers"]),
        "{{BILLING_QUOTA}}": render_billing_quota(data, checklist_text),
        "{{HUMAN_CONFIRMATION}}": render_confirmation(data),
        "{{IMPLEMENTATION_CHECKLIST}}": render_implementation_checklist(data),
        "{{RISKS}}": render_risks(data),
    }
    report = template
    for placeholder, value in replacements.items():
        report = report.replace(placeholder, value)
    return report.rstrip() + "\n"


def compile_plan(input_path: Path, output_path: Path | None) -> str:
    base = skill_dir()
    schema = load_json(base / "assets" / "maps-platform-plan-schema.json")
    policies = {
        "api": load_json(base / "assets" / "api-selection-policy.json"),
        "keys": load_json(base / "assets" / "api-key-restriction-policy.json"),
        "data_flow": load_json(base / "assets" / "data-flow-policy.json"),
        "markers": load_json(base / "assets" / "marker-accessibility-policy.json"),
    }
    data = load_json(input_path)
    selected_apis, libraries = validate_input(data, schema, policies["api"])
    template = (base / "assets" / "maps-platform-plan-template.md").read_text(encoding="utf-8")
    checklist = (base / "assets" / "billing-quota-risk-checklist.md").read_text(encoding="utf-8")
    report = render_report(data, selected_apis, libraries, policies, template, checklist)
    if output_path:
        output_path.write_text(report, encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an offline Google Maps Platform plan")
    parser.add_argument("--input", required=True, help="Path to local JSON plan input")
    parser.add_argument("--output", help="Optional path for Markdown output")
    args = parser.parse_args()

    try:
        report = compile_plan(Path(args.input), Path(args.output) if args.output else None)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if not args.output:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
