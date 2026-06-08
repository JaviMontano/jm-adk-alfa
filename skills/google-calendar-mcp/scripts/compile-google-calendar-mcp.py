#!/usr/bin/env python3
"""Compile a deterministic Google Calendar MCP operation plan from JSON.

This script is intentionally offline. It reads local assets and fixtures only;
it never calls Google Calendar, OAuth, or MCP tools.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
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


def parse_rfc3339(value: str, label: str) -> datetime:
    if not re.search(r"(Z|[+-]\d{2}:\d{2})$", value):
        raise ValueError(f"{label} must include a timezone offset")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an RFC3339 timestamp: {value}") from exc


def validate_timezone(value: str, pattern: str, label: str) -> None:
    if not re.match(pattern, value):
        raise ValueError(f"{label} must be an IANA timezone name or UTC: {value}")


def validate_scope(data: dict[str, Any], scope_policy: dict[str, Any]) -> None:
    operation = data["operation"]
    if data.get("app_created_only"):
        expected = scope_policy["minimum_scopes"]["app_created_calendar_event"]["scope"]
    else:
        expected = scope_policy["minimum_scopes"][operation]["scope"]
    actual = data["requested_scope"]
    if actual != expected:
        raise ValueError(f"requested_scope must be minimum scope for {operation}: {expected}")
    if actual in scope_policy["broad_scopes_to_avoid_by_default"]:
        raise ValueError(f"requested_scope is broader than needed: {actual}")


def validate_read_only_first(data: dict[str, Any], schema: dict[str, Any]) -> None:
    ro = require_object(data, "read_only_first")
    require_fields(ro, schema["required_read_only_first_fields"], "read_only_first")
    if data["operation"] in schema["mutating_operations"]:
        for key in ["calendars_listed", "events_checked"]:
            if ro[key] is not True:
                raise ValueError(f"mutating operation requires read_only_first.{key}=true")
        conflicts = ro["conflicts"]
        if not isinstance(conflicts, list):
            raise ValueError("read_only_first.conflicts must be a list")


def validate_confirmation(data: dict[str, Any], schema: dict[str, Any]) -> None:
    confirmation = require_object(data, "human_confirmation")
    require_fields(confirmation, schema["required_confirmation_fields"], "human_confirmation")
    if data["operation"] in schema["mutating_operations"] and confirmation["status"] != "confirmed":
        raise ValueError("mutating operation requires human_confirmation.status=confirmed")


def validate_calendar_access(data: dict[str, Any], schema: dict[str, Any]) -> None:
    if data["operation"] not in schema["mutating_operations"]:
        return
    access = require_object(data, "calendar_access")
    if access.get("write_access_confirmed") is not True:
        raise ValueError("mutating operation requires calendar_access.write_access_confirmed=true")


def validate_attendees(event: dict[str, Any], schema: dict[str, Any]) -> None:
    attendees = event.get("attendees", [])
    if not isinstance(attendees, list):
        raise ValueError("event.attendees must be a list")
    email_re = re.compile(schema["email_pattern"])
    for attendee in attendees:
        if not isinstance(attendee, dict):
            raise ValueError("each attendee must be an object")
        email = str(attendee.get("email", ""))
        if not email_re.match(email):
            raise ValueError(f"invalid attendee email: {email}")
    if attendees and event.get("send_updates") not in schema["send_updates_values"]:
        raise ValueError("event.send_updates must be explicit when attendees are present")


def validate_meet(event: dict[str, Any], data: dict[str, Any], schema: dict[str, Any]) -> None:
    meet = event.get("meet", {"required": False})
    if not isinstance(meet, dict):
        raise ValueError("event.meet must be an object")
    if not meet.get("required"):
        return
    if meet.get("conference_data_version") != 1:
        raise ValueError("Google Meet requires conference_data_version=1")
    request_id = str(meet.get("request_id", ""))
    if not re.match(schema["request_id_pattern"], request_id):
        raise ValueError("Google Meet requires a valid conferenceData.createRequest.requestId")
    idempotency = require_object(data, "idempotency")
    if idempotency.get("conference_request_id") != request_id:
        raise ValueError("idempotency.conference_request_id must match meet.request_id")


def validate_event(data: dict[str, Any], schema: dict[str, Any]) -> None:
    if data["operation"] == "cancel_event":
        if not data.get("target_event_id"):
            raise ValueError("cancel_event requires target_event_id")
        return
    if data["operation"] in {"query_agenda", "freebusy_check"}:
        window = require_object(data, "query_window")
        require_fields(window, ["time_min", "time_max", "time_zone"], "query_window")
        validate_timezone(window["time_zone"], schema["timezone_pattern"], "query_window.time_zone")
        time_min = parse_rfc3339(window["time_min"], "query_window.time_min")
        time_max = parse_rfc3339(window["time_max"], "query_window.time_max")
        if time_max <= time_min:
            raise ValueError("query_window.time_max must be after time_min")
        return

    event = require_object(data, "event")
    require_fields(event, schema["required_event_fields"], "event")
    for key in ["start", "end"]:
        section = require_object(event, key)
        require_fields(section, schema["required_event_time_fields"], f"event.{key}")
        validate_timezone(section["time_zone"], schema["timezone_pattern"], f"event.{key}.time_zone")
    validate_timezone(data["time_zone"], schema["timezone_pattern"], "time_zone")
    if event["start"]["time_zone"] != event["end"]["time_zone"]:
        raise ValueError("event.start.time_zone and event.end.time_zone must match")
    start = parse_rfc3339(event["start"]["date_time"], "event.start.date_time")
    end = parse_rfc3339(event["end"]["date_time"], "event.end.date_time")
    if end <= start:
        raise ValueError("event.end.date_time must be after event.start.date_time")
    validate_attendees(event, schema)
    validate_meet(event, data, schema)
    if data["operation"] == "create_event":
        idempotency = require_object(data, "idempotency")
        if not idempotency.get("event_id"):
            raise ValueError("create_event requires idempotency.event_id")
    if data["operation"] == "update_event" and not data.get("target_event_id"):
        raise ValueError("update_event requires target_event_id")


def validate_input(data: dict[str, Any], schema: dict[str, Any], scope_policy: dict[str, Any]) -> None:
    require_fields(data, schema["required_root_fields"], "root")
    if data["operation"] not in schema["allowed_operations"]:
        raise ValueError(f"unsupported operation: {data['operation']}")
    validate_timezone(data["time_zone"], schema["timezone_pattern"], "time_zone")
    validate_scope(data, scope_policy)
    validate_read_only_first(data, schema)
    validate_confirmation(data, schema)
    validate_calendar_access(data, schema)
    evidence = require_object(data, "evidence")
    if not evidence:
        raise ValueError("evidence must not be empty")
    validate_event(data, schema)


def evidence_lines(evidence: dict[str, Any]) -> str:
    return "\n".join(f"- [CODE] {key}: {value}" for key, value in sorted(evidence.items()))


def scope_lines(data: dict[str, Any], scope_policy: dict[str, Any]) -> str:
    operation = "app_created_calendar_event" if data.get("app_created_only") else data["operation"]
    policy = scope_policy["minimum_scopes"][operation]
    return "\n".join(
        [
            f"- [DOC] Selected scope: `{policy['scope']}`.",
            f"- [INFERENCE] Rationale: {policy['rationale']}",
        ]
    )


def read_only_first_lines(data: dict[str, Any]) -> str:
    ro = data["read_only_first"]
    conflicts = ro["conflicts"]
    conflict_text = "none" if not conflicts else "; ".join(str(item) for item in conflicts)
    return "\n".join(
        [
            f"- [CODE] Calendars listed: {ro['calendars_listed']}.",
            f"- [CODE] Events checked: {ro['events_checked']}.",
            f"- [CODE] Conflicts: {conflict_text}.",
        ]
    )


def confirmation_lines(data: dict[str, Any]) -> str:
    confirmation = data["human_confirmation"]
    return "\n".join(
        [
            f"- [CODE] Status: `{confirmation['status']}`.",
            f"- [CODE] Confirmed by: `{confirmation['confirmed_by']}`.",
            f"- [CODE] Confirmation text: {confirmation['confirmation_text']}",
        ]
    )


def event_payload(data: dict[str, Any]) -> dict[str, Any]:
    operation = data["operation"]
    if operation in {"query_agenda", "freebusy_check"}:
        window = data["query_window"]
        return {
            "calendarId": data["calendar_id"],
            "timeMin": window["time_min"],
            "timeMax": window["time_max"],
            "timeZone": window["time_zone"],
            "singleEvents": True,
            "orderBy": "startTime" if operation == "query_agenda" else None,
        }
    if operation == "cancel_event":
        return {
            "calendarId": data["calendar_id"],
            "eventId": data["target_event_id"],
            "sendUpdates": data.get("send_updates", "none"),
            "operation": "cancel"
        }

    event = data["event"]
    resource: dict[str, Any] = {
        "summary": event["summary"],
        "start": {
            "dateTime": event["start"]["date_time"],
            "timeZone": event["start"]["time_zone"],
        },
        "end": {
            "dateTime": event["end"]["date_time"],
            "timeZone": event["end"]["time_zone"],
        },
    }
    for optional in ["description", "location", "recurrence", "reminders"]:
        if optional in event:
            resource[optional] = event[optional]
    if event.get("attendees"):
        resource["attendees"] = [{"email": item["email"]} for item in event["attendees"]]
    if event.get("meet", {}).get("required"):
        resource["conferenceData"] = {
            "createRequest": {
                "requestId": event["meet"]["request_id"],
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        }

    payload: dict[str, Any] = {
        "calendarId": data["calendar_id"],
        "sendUpdates": event.get("send_updates", "none"),
        "resource": resource,
    }
    if data["operation"] == "create_event":
        payload["eventId"] = data["idempotency"]["event_id"]
    if data["operation"] == "update_event":
        payload["eventId"] = data["target_event_id"]
    if event.get("meet", {}).get("required"):
        payload["conferenceDataVersion"] = 1
    return payload


def payload_preview(data: dict[str, Any]) -> str:
    payload = event_payload(data)
    cleaned = {key: value for key, value in payload.items() if value is not None}
    return "```json\n" + json.dumps(cleaned, indent=2, sort_keys=True) + "\n```"


def mcp_plan_lines(data: dict[str, Any]) -> str:
    operation = data["operation"]
    lines = [
        "- [CODE] First call read-only tools only: `mcp__workspace-mcp__list_calendars` and/or `mcp__workspace-mcp__get_events`.",
    ]
    if operation in {"query_agenda", "freebusy_check"}:
        lines.append("- [CODE] Stop after read-only retrieval; no mutating MCP tool is needed.")
    elif operation == "cancel_event":
        lines.append("- [CODE] After confirmation, call `mcp__workspace-mcp__manage_event` to cancel the target event id.")
    else:
        lines.append(f"- [CODE] After confirmation, call `mcp__workspace-mcp__manage_event` for `{operation}`.")
    lines.append("- [CODE] After any mutation, call `mcp__workspace-mcp__get_events` to read back and verify the result.")
    return "\n".join(lines)


def validation_lines(data: dict[str, Any]) -> str:
    lines = [
        "- [CODE] Structured input validates against local assets.",
        "- [CODE] Compiler made no Google Calendar, OAuth, or MCP calls.",
        "- [CODE] Requested scope matches the operation minimum-scope policy.",
    ]
    if data["operation"] in {"create_event", "update_event", "cancel_event"}:
        lines.append("- [CODE] Human confirmation and read-only-first checks are present.")
    if data["operation"] in {"create_event", "update_event"} and data["event"].get("meet", {}).get("required"):
        lines.append("- [CODE] Google Meet request includes `conferenceDataVersion=1` and requestId.")
    return "\n".join(lines)


def risk_lines(data: dict[str, Any]) -> str:
    risks = [
        "- [INFERENCE] A real MCP mutation still depends on authenticated `workspace-mcp` permissions.",
        "- [INFERENCE] Calendar should be read back after mutation because Meet conference generation can be asynchronous.",
        "- [ASSUMPTION] Fixture evidence accurately represents the prior read-only checks.",
    ]
    event = data.get("event", {})
    if isinstance(event, dict) and event.get("attendees") and event.get("send_updates") == "none":
        risks.append("- [DOC] `sendUpdates=none` can have adverse sync effects for some attendees.")
    return "\n".join(risks)


def summary_line(data: dict[str, Any]) -> str:
    operation = data["operation"]
    if operation in {"query_agenda", "freebusy_check"}:
        window = data["query_window"]
        return f"- [CODE] `{operation}` on `{data['calendar_id']}` from {window['time_min']} to {window['time_max']}."
    if operation == "cancel_event":
        return f"- [CODE] `cancel_event` on `{data['calendar_id']}` target event `{data['target_event_id']}`."
    event = data["event"]
    return (
        f"- [CODE] `{operation}` on `{data['calendar_id']}` for `{event['summary']}` "
        f"from {event['start']['date_time']} to {event['end']['date_time']}."
    )


def render(data: dict[str, Any], base: Path) -> str:
    template = (base / "assets" / "google-calendar-operation-template.md").read_text(encoding="utf-8")
    scope_policy = load_json(base / "assets" / "scope-policy.json")
    replacements = {
        "{{OPERATION_ID}}": str(data["operation_id"]),
        "{{SUMMARY}}": summary_line(data),
        "{{EVIDENCE}}": evidence_lines(data["evidence"]),
        "{{SCOPE}}": scope_lines(data, scope_policy),
        "{{READ_ONLY_FIRST}}": read_only_first_lines(data),
        "{{HUMAN_CONFIRMATION}}": confirmation_lines(data),
        "{{PAYLOAD_PREVIEW}}": payload_preview(data),
        "{{MCP_OPERATION_PLAN}}": mcp_plan_lines(data),
        "{{VALIDATION}}": validation_lines(data),
        "{{RISKS}}": risk_lines(data),
    }
    output = template
    for token, value in replacements.items():
        output = output.replace(token, value)
    return output.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an offline Google Calendar MCP operation plan")
    parser.add_argument("--input", required=True, help="Structured Calendar operation JSON")
    parser.add_argument("--output", help="Write Markdown to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    try:
        data = load_json(Path(args.input))
        schema = load_json(base / "assets" / "google-calendar-operation-schema.json")
        scope_policy = load_json(base / "assets" / "scope-policy.json")
        validate_input(data, schema, scope_policy)
        output = render(data, base)
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
