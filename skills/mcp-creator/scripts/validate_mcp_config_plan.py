#!/usr/bin/env python3
"""Validate deterministic MCP Creator JSON plans."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "jm-labs.mcp-creator.plan.v1"
REQUIRED_TOP = {"schema", "skill", "server", "transport", "scope", "auth", "preflight", "rollback", "evidence", "validation"}
REQUIRED_CHECKS = {
    "assets",
    "deterministic_scripts",
    "quality_criteria",
    "transport_policy",
    "scope_policy",
    "secret_policy",
    "preflight_required",
    "rollback_plan",
    "evidence_required",
}
TAGS = {"[CÓDIGO]", "[CONFIG]", "[DOC]", "[INFERENCIA]", "[SUPUESTO]"}
SCOPE_CONFIG = {
    "local": {"tracked": False},
    "user": {"tracked": False},
    "project": {"tracked": True},
    "plugin": {"tracked": False},
}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]+"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]+"),
    re.compile(r"password=", re.IGNORECASE),
    re.compile(r"api_key=", re.IGNORECASE),
    re.compile(r"client_secret=", re.IGNORECASE),
]
ENV_REF = re.compile(r"^\$\{[A-Z][A-Z0-9_]*(?::-[^}]*)?\}$")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def object_at(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    require(isinstance(value, dict), errors, f"{key} must be object")
    return value if isinstance(value, dict) else {}


def text_list(value: Any, ctx: str, errors: list[str]) -> list[str]:
    require(isinstance(value, list), errors, f"{ctx} must be list")
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for i, item in enumerate(value):
        require(is_text(item), errors, f"{ctx}[{i}] must be non-empty string")
        if is_text(item):
            out.append(item)
    return out


def scan_secret(value: Any, ctx: str, errors: list[str]) -> None:
    if isinstance(value, str):
        if ENV_REF.match(value):
            return
        for pattern in SECRET_PATTERNS:
            require(not pattern.search(value), errors, f"{ctx} contains hardcoded secret-like literal")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            scan_secret(item, f"{ctx}[{i}]", errors)
    elif isinstance(value, dict):
        for key, item in value.items():
            scan_secret(item, f"{ctx}.{key}", errors)


def validate_server(data: dict[str, Any], errors: list[str]) -> None:
    server = object_at(data, "server", errors)
    name = server.get("name")
    require(is_text(name) and bool(KEBAB.match(name)), errors, "server.name must be kebab-case")
    require(server.get("name_collision_checked") is True, errors, "server.name_collision_checked must be true")
    require(is_text(server.get("description")), errors, "server.description required")


def validate_transport(data: dict[str, Any], errors: list[str]) -> None:
    transport = object_at(data, "transport", errors)
    ttype = transport.get("type")
    require(ttype in {"stdio", "http"}, errors, "transport.type must be stdio or http")
    require(ttype != "sse", errors, "transport.type must not be sse")
    if ttype == "stdio":
        require(is_text(transport.get("command")), errors, "transport.command required for stdio")
        args = text_list(transport.get("args"), "transport.args", errors)
        require(bool(args), errors, "transport.args must not be empty for stdio")
    if ttype == "http":
        url = transport.get("url")
        require(is_text(url) and url.startswith("https://"), errors, "transport.url must be https:// for http")
    scan_secret(transport, "transport", errors)


def validate_scope(data: dict[str, Any], errors: list[str]) -> None:
    scope = object_at(data, "scope", errors)
    stype = scope.get("type")
    require(stype in SCOPE_CONFIG, errors, "scope.type invalid")
    require(is_text(scope.get("config_path")), errors, "scope.config_path required")
    require(isinstance(scope.get("tracked_file"), bool), errors, "scope.tracked_file must be boolean")
    require(is_text(scope.get("rationale")), errors, "scope.rationale required")
    if stype in SCOPE_CONFIG:
        require(scope.get("tracked_file") is SCOPE_CONFIG[stype]["tracked"], errors, f"scope.tracked_file mismatch for {stype}")


def validate_auth(data: dict[str, Any], errors: list[str]) -> None:
    auth = object_at(data, "auth", errors)
    require(auth.get("type") in {"none", "env", "oauth"}, errors, "auth.type invalid")
    env_vars = text_list(auth.get("env_vars"), "auth.env_vars", errors)
    require(auth.get("secrets_hardcoded") is False, errors, "auth.secrets_hardcoded must be false")
    if auth.get("type") in {"env", "oauth"}:
        require(bool(env_vars), errors, "auth.env_vars required for env or oauth auth")
    for var in env_vars:
        require(bool(re.match(r"^[A-Z][A-Z0-9_]*$", var)), errors, f"auth.env_vars invalid: {var}")
    scan_secret(auth, "auth", errors)


def validate_preflight(data: dict[str, Any], errors: list[str]) -> None:
    preflight = object_at(data, "preflight", errors)
    require(preflight.get("existing_config_reviewed") is True, errors, "preflight.existing_config_reviewed must be true")
    require(preflight.get("live_validation_deferred") is True, errors, "preflight.live_validation_deferred must be true")
    require(is_text(preflight.get("deferred_reason")), errors, "preflight.deferred_reason required")


def validate_rollback(data: dict[str, Any], errors: list[str]) -> None:
    rollback = object_at(data, "rollback", errors)
    require(is_text(rollback.get("remove_command")), errors, "rollback.remove_command required")
    require(rollback.get("config_backup_required") is True, errors, "rollback.config_backup_required must be true")


def validate_evidence(data: dict[str, Any], errors: list[str]) -> None:
    evidence = data.get("evidence")
    require(isinstance(evidence, list) and bool(evidence), errors, "evidence must be non-empty list")
    if not isinstance(evidence, list):
        return
    for i, item in enumerate(evidence):
        ctx = f"evidence[{i}]"
        require(isinstance(item, dict), errors, f"{ctx} must be object")
        if not isinstance(item, dict):
            continue
        require(is_text(item.get("claim")), errors, f"{ctx}.claim required")
        require(item.get("evidence_tag") in TAGS, errors, f"{ctx}.evidence_tag invalid")
        require(is_text(item.get("source")), errors, f"{ctx}.source required")


def validate_validation(data: dict[str, Any], errors: list[str]) -> None:
    validation = object_at(data, "validation", errors)
    require(validation.get("status") in {"pass", "warn", "block"}, errors, "validation.status invalid")
    require(validation.get("offline") is True, errors, "validation.offline must be true")
    require(validation.get("network_required") is False, errors, "validation.network_required must be false")
    require(validation.get("deterministic") is True, errors, "validation.deterministic must be true")
    checks = set(text_list(validation.get("checks"), "validation.checks", errors))
    require(REQUIRED_CHECKS.issubset(checks), errors, "validation.checks missing required checks")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP - set(data))
    require(not missing, errors, f"missing top-level fields: {', '.join(missing)}")
    if errors:
        return errors
    require(data.get("schema") == SCHEMA, errors, "schema mismatch")
    require(data.get("skill") == "mcp-creator", errors, "skill must be mcp-creator")
    validate_server(data, errors)
    validate_transport(data, errors)
    validate_scope(data, errors)
    validate_auth(data, errors)
    validate_preflight(data, errors)
    validate_rollback(data, errors)
    validate_evidence(data, errors)
    validate_validation(data, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_mcp_config_plan.py <plan.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data if isinstance(data, dict) else {})
    print(f"plan={path.name} status={'pass' if not errors else 'fail'} errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
