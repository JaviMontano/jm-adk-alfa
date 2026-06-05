#!/usr/bin/env python3
"""Compile a deterministic resumable workflow orchestration plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def lower(value: Any) -> str:
    return str(value or "").strip().lower()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_required_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        require(field in obj and (obj[field] or obj[field] is False), f"{label} missing field: {field}", errors)


def validate_text_list(items: list[Any], label: str, minimum: int, errors: list[str]) -> None:
    require(len(items) >= minimum, f"{label} must contain at least {minimum} item(s)", errors)
    for index, item in enumerate(items, start=1):
        require(nonempty(item), f"{label}[{index}] must be non-empty text", errors)


def contains_any(text: str, markers: list[str]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def validate_checkpoint(checkpoint: dict[str, Any], label: str, schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    validate_required_fields(checkpoint, schema["checkpoint_required_fields"], f"{label}.checkpoint", errors)
    require(nonempty(checkpoint.get("name")), f"{label}.checkpoint.name must be non-empty", errors)
    validate_text_list(as_list(checkpoint.get("criteria")), f"{label}.checkpoint.criteria", int(policy["minimum_checkpoint_criteria"]), errors)
    validate_text_list(as_list(checkpoint.get("evidence")), f"{label}.checkpoint.evidence", int(policy["minimum_checkpoint_evidence"]), errors)
    require(checkpoint.get("onPass") in policy["blocked_on_pass"], f"{label}.checkpoint.onPass is not accepted", errors)
    require(checkpoint.get("onFail") in policy["blocked_on_fail"], f"{label}.checkpoint.onFail is not accepted", errors)


def validate_stage(stage: dict[str, Any], expected_number: int, schema: dict[str, Any], checkpoint_policy: dict[str, Any], resume_policy: dict[str, Any], errors: list[str]) -> None:
    label = f"stage {expected_number}"
    validate_required_fields(stage, schema["stage_required_fields"], label, errors)
    require(stage.get("number") == expected_number, f"{label}.number must be {expected_number}", errors)
    require(nonempty(stage.get("name")), f"{label}.name must be non-empty", errors)
    require(nonempty(stage.get("agent")), f"{label}.agent must be non-empty", errors)
    require(stage.get("status") in checkpoint_policy["accepted_statuses"], f"{label}.status is not accepted", errors)
    validate_text_list(as_list(stage.get("inputs")), f"{label}.inputs", 1, errors)
    validate_text_list(as_list(stage.get("actions")), f"{label}.actions", int(checkpoint_policy["minimum_actions_per_stage"]), errors)
    validate_text_list(as_list(stage.get("outputs")), f"{label}.outputs", 1, errors)
    validate_text_list(as_list(stage.get("failureSignals")), f"{label}.failureSignals", 1, errors)
    validate_text_list(as_list(stage.get("recoveryActions")), f"{label}.recoveryActions", 1, errors)
    for action in as_list(stage.get("actions")):
        action_text = lower(action)
        for vague in checkpoint_policy["vague_terms"]:
            require(vague not in action_text, f"{label}.actions contains vague term: {vague}", errors)
    resume_state = as_dict(stage.get("resumeState"))
    require(len(resume_state) >= int(resume_policy["minimum_resume_state_keys"]), f"{label}.resumeState lacks minimum keys", errors)
    for key, value in resume_state.items():
        require(nonempty(key), f"{label}.resumeState contains empty key", errors)
        require(lower(value) not in set(resume_policy["blocked_resume_values"]), f"{label}.resumeState.{key} is not resumable", errors)
    validate_checkpoint(as_dict(stage.get("checkpoint")), label, schema, checkpoint_policy, errors)


def validate_spec(spec: dict[str, Any]) -> list[str]:
    schema = load_json(ASSET_DIR / "orchestration-schema.json")
    checkpoint_policy = load_json(ASSET_DIR / "checkpoint-policy.json")
    resume_policy = load_json(ASSET_DIR / "resume-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["required_top_fields"], "orchestration", errors)
    if errors:
        return errors

    require(bool(re.match(resume_policy["id_pattern"], str(spec.get("id", "")))), "id must be kebab-case", errors)
    for field in ["title", "objective", "trigger"]:
        require(nonempty(spec.get(field)), f"{field} must be non-empty", errors)
    validate_text_list(as_list(spec.get("agents")), "agents", 1, errors)
    validate_text_list(as_list(spec.get("inputs")), "inputs", 1, errors)
    validate_text_list(as_list(spec.get("outputs")), "outputs", 1, errors)
    validate_text_list(as_list(spec.get("completionCriteria")), "completionCriteria", 2, errors)

    stages = [as_dict(item) for item in as_list(spec.get("stages"))]
    minimum_stages = int(checkpoint_policy["minimum_stages"])
    maximum_stages = int(checkpoint_policy["maximum_stages"])
    require(len(stages) >= minimum_stages, f"stages must contain at least {minimum_stages} stages", errors)
    require(len(stages) <= maximum_stages, f"stages must contain at most {maximum_stages} stages", errors)
    if stages:
        require(contains_any(str(stages[0].get("name", "")), checkpoint_policy["required_stage_name_markers"]["first"]), "first stage must discover/intake/plan/clarify", errors)
        require(contains_any(str(stages[-1].get("name", "")), checkpoint_policy["required_stage_name_markers"]["last"]), "final stage must verify/validate/close/review", errors)
    for index, stage in enumerate(stages, start=1):
        validate_stage(stage, index, schema, checkpoint_policy, resume_policy, errors)

    resume = as_dict(spec.get("resume"))
    validate_required_fields(resume, schema["resume_required_fields"], "resume", errors)
    require(bool(re.match(resume_policy["token_pattern"], str(resume.get("token", "")))), "resume.token must be kebab-case", errors)
    require(resume.get("stateStore") in resume_policy["allowed_state_stores"], "resume.stateStore is not accepted", errors)
    require(nonempty(resume.get("idempotencyKey")), "resume.idempotencyKey must be non-empty", errors)
    require(resume.get("retryPolicy") in resume_policy["allowed_retry_policies"], "resume.retryPolicy is not accepted", errors)
    require(isinstance(resume.get("resumeFrom"), int) and resume.get("resumeFrom") >= 1, "resume.resumeFrom must be a stage number", errors)

    observability = as_dict(spec.get("observability"))
    validate_required_fields(observability, schema["observability_required_fields"], "observability", errors)
    for field, minimum in resume_policy["required_observability_minimums"].items():
        validate_text_list(as_list(observability.get(field)), f"observability.{field}", int(minimum), errors)
    return errors


def bullets(items: list[Any]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_stages(stages: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for stage in stages:
        checkpoint = stage["checkpoint"]
        blocks.append(
            "\n".join(
                [
                    f"### {stage['number']}. {stage['name']} ({stage['status']})",
                    f"- Agent: {stage['agent']}",
                    f"- Actions: {'; '.join(stage['actions'])}",
                    f"- Outputs: {', '.join(stage['outputs'])}",
                    f"- Failure signals: {'; '.join(stage['failureSignals'])}",
                    f"- Recovery actions: {'; '.join(stage['recoveryActions'])}",
                    f"- Checkpoint: {checkpoint['name']} -> pass={checkpoint['onPass']} fail={checkpoint['onFail']}",
                    f"- Resume state: {', '.join(f'{key}={value}' for key, value in stage['resumeState'].items())}",
                ]
            )
        )
    return "\n\n".join(blocks)


def render_resume(resume: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"- Token: `{resume['token']}`",
            f"- State store: `{resume['stateStore']}`",
            f"- Idempotency key: `{resume['idempotencyKey']}`",
            f"- Retry policy: `{resume['retryPolicy']}`",
            f"- Resume from stage: `{resume['resumeFrom']}`",
        ]
    )


def render_observability(observability: dict[str, Any]) -> str:
    sections = []
    for field in ["logs", "metrics", "auditTrail"]:
        sections.append(f"### {field}\n{bullets(observability[field])}")
    return "\n\n".join(sections)


def render_report(spec: dict[str, Any]) -> str:
    template = (ASSET_DIR / "orchestration-template.md").read_text(encoding="utf-8")
    return template.format(
        title=spec["title"],
        objective=spec["objective"],
        trigger=spec["trigger"],
        agents=bullets(spec["agents"]),
        inputs=bullets(spec["inputs"]),
        stages=render_stages(spec["stages"]),
        resume_contract=render_resume(spec["resume"]),
        observability=render_observability(spec["observability"]),
        completion=bullets(spec["completionCriteria"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic workflow orchestration plan.")
    parser.add_argument("--input", required=True, type=Path, help="Path to orchestration JSON input.")
    parser.add_argument("--output", type=Path, help="Optional Markdown output path.")
    args = parser.parse_args()

    spec = load_json(args.input)
    errors = validate_spec(spec)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    report = render_report(spec)
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
