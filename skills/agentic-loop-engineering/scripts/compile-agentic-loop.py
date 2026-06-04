#!/usr/bin/env python3
"""Compile deterministic agentic control loops from structured JSON."""

from __future__ import annotations

import argparse
import json
import re
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


def validate_budget(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    max_iterations = spec.get("maxIterations")
    require(isinstance(max_iterations, int), "maxIterations must be an integer", errors)
    if isinstance(max_iterations, int):
        limits = as_dict(policy.get("budget"))
        require(limits["minIterations"] <= max_iterations <= limits["maxIterations"], "maxIterations outside policy range", errors)


def validate_stop_handlers(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    handlers = [as_dict(item) for item in as_list(spec.get("stopHandlers"))]
    require(bool(handlers), "stopHandlers requires at least one handler", errors)
    allowed_reasons = set(policy["allowedStopReasons"])
    allowed_actions = set(policy["allowedActions"])
    required_actions = as_dict(policy["requiredActions"])
    seen: dict[str, str] = {}
    for index, handler in enumerate(handlers, start=1):
        label = f"stopHandler {index}"
        validate_required_fields(handler, schema["requiredStopHandlerFields"], label, errors)
        reason = str(handler.get("stopReason", ""))
        action = str(handler.get("action", ""))
        require(reason in allowed_reasons, f"{label} stopReason unsupported", errors)
        require(action in allowed_actions, f"{label} action unsupported", errors)
        require(handler.get("observable") is True, f"{label} must be observable", errors)
        if reason in seen:
            errors.append(f"duplicate stop handler: {reason}")
        seen[reason] = action
    for reason in policy["requiredStopReasons"]:
        require(reason in seen, f"missing required stop handler: {reason}", errors)
    for reason, action in required_actions.items():
        if reason in seen:
            require(seen[reason] == action, f"{reason} must use action {action}", errors)
    require(spec.get("unknownStopAction") == "raise_unhandled_stop", "unknownStopAction must raise_unhandled_stop", errors)


def validate_tool_use(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    tool_use = as_dict(spec.get("toolUse"))
    validate_required_fields(tool_use, schema["requiredToolUseFields"], "toolUse", errors)
    contract = as_dict(policy["toolResult"])
    require(tool_use.get("resultRole") == contract["role"], "toolUse.resultRole must be user", errors)
    require(tool_use.get("resultType") == contract["type"], "toolUse.resultType must be tool_result", errors)
    require(tool_use.get("correlationField") == contract["correlationField"], "toolUse.correlationField must be tool_use_id", errors)
    require(tool_use.get("blockIdField") == contract["blockIdField"], "toolUse.blockIdField must be id", errors)
    require(tool_use.get("handlerLookup") == contract["handlerLookup"], "toolUse.handlerLookup must be handlers[block.name]", errors)
    require(tool_use.get("emitEvent") is True, "toolUse.emitEvent must be true", errors)


def validate_handlers(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    handlers = [as_dict(item) for item in as_list(spec.get("handlers"))]
    require(bool(handlers), "handlers requires at least one entry", errors)
    names: set[str] = set()
    for index, handler in enumerate(handlers, start=1):
        label = f"handler {index}"
        validate_required_fields(handler, schema["requiredHandlerFields"], label, errors)
        name = str(handler.get("name", ""))
        require(bool(re.match(r"^[a-z][a-z0-9_]*$", name)), f"{label} name must be snake_case", errors)
        require(nonempty(handler.get("callable")), f"{label} callable must be non-empty", errors)
        if name in names:
            errors.append(f"duplicate handler name: {name}")
        names.add(name)


def validate_instrumentation(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    instrumentation = as_dict(spec.get("instrumentation"))
    validate_required_fields(instrumentation, schema["requiredInstrumentationFields"], "instrumentation", errors)
    require(nonempty(instrumentation.get("emitter")), "instrumentation.emitter must be non-empty", errors)
    events = set(str(item) for item in as_list(instrumentation.get("events")))
    require(len(events) >= policy["instrumentation"]["minimumEvents"], "instrumentation.events below minimum", errors)
    for event in policy["instrumentation"]["requiredEvents"]:
        require(event in events, f"instrumentation missing event: {event}", errors)


def validate_errors(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    error_spec = as_dict(spec.get("errors"))
    validate_required_fields(error_spec, schema["requiredErrorFields"], "errors", errors)
    require(error_spec.get("failurePolicy") == policy["errors"]["failurePolicy"], "errors.failurePolicy must be raise", errors)
    exception_names = set(str(item) for item in as_list(error_spec.get("exceptionNames")))
    for name in policy["errors"]["requiredExceptions"]:
        require(name in exception_names, f"errors.exceptionNames missing {name}", errors)


def validate_antipatterns(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    joined = "\n".join(flatten_strings(spec)).lower()
    for token in policy["blockedAntiPatterns"]:
        if token in joined:
            errors.append(f"blocked anti-pattern token present: {token}")


def validate(spec: dict[str, Any]) -> None:
    schema = load_json(ASSET_DIR / "loop-contract.schema.json")
    policy = load_json(ASSET_DIR / "loop-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["requiredTopLevel"], "loop", errors)
    if errors:
        raise ValueError("\n".join(errors))
    require(nonempty(spec.get("name")), "name must be non-empty", errors)
    require(nonempty(spec.get("modelConstant")), "modelConstant must be non-empty", errors)
    require(nonempty(spec.get("clientCall")), "clientCall must be non-empty", errors)
    require(nonempty(spec.get("messagesVariable")), "messagesVariable must be non-empty", errors)
    require(nonempty(spec.get("toolsVariable")), "toolsVariable must be non-empty", errors)
    require(spec.get("handlersVariable") == "handlers", "handlersVariable must be handlers", errors)
    require(spec.get("resultContract") == "return_response_on_end_turn", "resultContract must be return_response_on_end_turn", errors)
    validate_budget(spec, policy, errors)
    validate_stop_handlers(spec, schema, policy, errors)
    validate_tool_use(spec, schema, policy, errors)
    validate_handlers(spec, schema, errors)
    validate_instrumentation(spec, schema, policy, errors)
    validate_errors(spec, schema, policy, errors)
    validate_antipatterns(spec, policy, errors)
    if errors:
        raise ValueError("\n".join(errors))


def render_python(spec: dict[str, Any]) -> str:
    model = spec["modelConstant"]
    client_call = spec["clientCall"]
    default_iterations = spec["maxIterations"]
    return f'''class UnhandledStop(Exception):
    pass


class BudgetExceeded(Exception):
    pass


def _field(value, name, default=None):
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def run_agent_loop(client, messages, tools, handlers, max_iterations={default_iterations}, emit_loop_event=None):
    def emit(event, **payload):
        if emit_loop_event is not None:
            emit_loop_event({{"event": event, **payload}})

    for iteration in range(max_iterations):
        emit("iteration_started", iteration=iteration)
        resp = {client_call}(model={model}, messages=messages, tools=tools)
        messages.append({{"role": "assistant", "content": resp.content}})
        emit("stop_reason", iteration=iteration, stop_reason=resp.stop_reason)

        if resp.stop_reason == "end_turn":
            emit("halted", iteration=iteration, stop_reason=resp.stop_reason)
            return resp

        if resp.stop_reason == "tool_use":
            tool_results = []
            for block in resp.content:
                if _field(block, "type") != "tool_use":
                    continue
                name = _field(block, "name")
                handler = handlers[name]
                emit("tool_dispatched", iteration=iteration, tool_name=name)
                result = handler(**(_field(block, "input", {{}}) or {{}}))
                tool_results.append({{
                    "type": "tool_result",
                    "tool_use_id": _field(block, "id"),
                    "content": result,
                }})
                emit("tool_result_injected", iteration=iteration, tool_name=name, tool_use_id=_field(block, "id"))
            messages.append({{"role": "user", "content": tool_results}})
            continue

        raise UnhandledStop(resp.stop_reason)

    emit("budget_exceeded", max_iterations=max_iterations)
    raise BudgetExceeded(max_iterations)
'''


def render_report(spec: dict[str, Any], code: str) -> str:
    template = (ASSET_DIR / "loop-report-template.md").read_text(encoding="utf-8")
    return template.format(
        name=spec["name"],
        modelConstant=spec["modelConstant"],
        clientCall=spec["clientCall"],
        maxIterations=spec["maxIterations"],
        stopReasons=", ".join(item["stopReason"] for item in spec["stopHandlers"]),
        handlers=", ".join(item["name"] for item in spec["handlers"]),
        generatedCode=code.rstrip(),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an agentic loop contract")
    parser.add_argument("input", type=Path, help="Path to loop JSON contract")
    parser.add_argument("--output", type=Path, help="Write generated Python code")
    parser.add_argument("--report", type=Path, help="Write markdown validation report")
    args = parser.parse_args()
    try:
        spec = load_json(args.input)
        validate(spec)
        code = render_python(spec)
        if args.output:
            args.output.write_text(code, encoding="utf-8")
        if args.report:
            args.report.write_text(render_report(spec, code), encoding="utf-8")
        if not args.output and not args.report:
            print(code)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
