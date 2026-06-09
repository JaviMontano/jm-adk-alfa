#!/usr/bin/env python3
"""Validate deterministic Colombian liquidation arithmetic reports."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


COMPONENTS = ("cesantias", "intereses_cesantias", "prima", "vacaciones")
TOLERANCE = Decimal("1")
FORBIDDEN_LEGAL_TERMS = (
    "legally final",
    "fully compliant",
    "safe to sign",
    "firma tranquilo",
    "cumple totalmente",
    "definitive legal conclusion",
)


def money(value: Any, label: str, errors: list[str]) -> Decimal:
    try:
        amount = Decimal(str(value))
    except Exception:  # noqa: BLE001
        errors.append(f"{label} must be numeric")
        return Decimal("0")
    if amount < 0:
        errors.append(f"{label} must be non-negative")
    return amount


def rounded(value: Decimal) -> Decimal:
    return value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def close(a: Decimal, b: Decimal) -> bool:
    return abs(a - b) <= TOLERANCE


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def text(value: Any) -> str:
    return str(value or "").strip()


def all_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(all_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(all_text(v) for v in value)
    return text(value)


def as_dict(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def as_list(data: dict[str, Any], key: str, errors: list[str], allow_empty: bool = False) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or (not value and not allow_empty):
        errors.append(f"{key} must be a {'list' if allow_empty else 'non-empty list'}")
        return []
    out: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
        else:
            out.append(item)
    return out


def recompute(basis: dict[str, Any], errors: list[str]) -> dict[str, Decimal]:
    salary_benefits = money(basis.get("salary_base_prestaciones"), "salary_base_prestaciones", errors)
    salary_vacations = money(basis.get("salary_base_vacaciones"), "salary_base_vacaciones", errors)
    days = money(basis.get("days_worked"), "days_worked", errors)
    if days <= 0:
        errors.append("days_worked must be positive")
    cesantias = rounded(salary_benefits * days / Decimal("360"))
    intereses = rounded(cesantias * Decimal("0.12") * days / Decimal("360"))
    prima = rounded(salary_benefits * days / Decimal("360"))
    if basis.get("vacation_days") is not None:
        vacation_days = money(basis.get("vacation_days"), "vacation_days", errors)
        vacaciones = rounded(salary_vacations * vacation_days / Decimal("30"))
    else:
        vacaciones = rounded(salary_vacations * days / Decimal("720"))
    return {
        "cesantias": cesantias,
        "intereses_cesantias": intereses,
        "prima": prima,
        "vacaciones": vacaciones,
    }


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != 1:
        errors.append("schema must be 1")
    if data.get("skill") != "validar-liquidacion-co":
        errors.append("skill must be validar-liquidacion-co")
    if text(data.get("currency")) != "COP":
        errors.append("currency must be COP")
    if any(term in all_text(data).lower() for term in FORBIDDEN_LEGAL_TERMS):
        errors.append("legal-final or safe-to-sign language is forbidden")

    evidence = as_list(data, "evidence", errors)
    evidence_ids: list[str] = []
    for item in evidence:
        ev_id = text(item.get("id"))
        evidence_ids.append(ev_id)
        if not ev_id:
            errors.append("evidence.id is required")
        if text(item.get("type")) not in {"settlement_doc", "payroll_summary", "manual_entry", "deduction_note", "vacation_note"}:
            errors.append(f"{ev_id}: unsupported evidence type")
        for key in ("source", "summary"):
            if not text(item.get(key)):
                errors.append(f"{ev_id}.{key} is required")
    evidence_id_set = set(evidence_ids)

    basis = as_dict(data, "calculation_basis", errors)
    if text(basis.get("evidence_ref")) not in evidence_id_set:
        errors.append("calculation_basis.evidence_ref is unresolved")
    expected = recompute(basis, errors)

    reported = as_dict(data, "reported_components", errors)
    for component in COMPONENTS:
        if component not in reported:
            errors.append(f"reported_components.{component} is required")
            continue
        reported_amount = money(reported.get(component), f"reported_components.{component}", errors)
        if not close(reported_amount, expected[component]):
            errors.append(f"{component}: reported={reported_amount} recomputed={expected[component]}")

    deductions = as_dict(data, "deductions", errors)
    for key, value in deductions.items():
        money(value, f"deductions.{key}", errors)
    other_payments = data.get("other_payments", {})
    if not isinstance(other_payments, dict):
        errors.append("other_payments must be an object")
        other_payments = {}
    for key, value in other_payments.items():
        money(value, f"other_payments.{key}", errors)

    total_payments = sum(money(v, f"reported_components.{k}", errors) for k, v in reported.items())
    total_payments += sum(money(v, f"other_payments.{k}", errors) for k, v in other_payments.items())
    total_deductions = sum(money(v, f"deductions.{k}", errors) for k, v in deductions.items())
    net_expected = total_payments - total_deductions
    net_reported = money(data.get("net_reported"), "net_reported", errors)
    if not close(net_reported, net_expected):
        errors.append(f"net_reported={net_reported} recomputed={net_expected}")

    open_questions = data.get("open_questions", [])
    if not isinstance(open_questions, list):
        errors.append("open_questions must be a list")
        open_questions = []
    paz = as_dict(data, "paz_y_salvo", errors)
    recommendation = text(paz.get("recommendation"))
    if recommendation not in {"do_not_sign_yet", "sign_under_reservation", "no_objection_arithmetic_only"}:
        errors.append("paz_y_salvo.recommendation is unsupported")
    if open_questions and recommendation == "no_objection_arithmetic_only":
        errors.append("open questions require sign_under_reservation or do_not_sign_yet")
    if recommendation == "sign_under_reservation" and not text(paz.get("reservation_text")):
        errors.append("reservation_text is required for sign_under_reservation")

    validation = as_dict(data, "validation", errors)
    if validation.get("offline") is not True:
        errors.append("validation.offline must be true")
    if validation.get("network_used") not in (False, None):
        errors.append("validation.network_used must be false")
    if validation.get("not_legal_advice") is not True:
        errors.append("validation.not_legal_advice must be true")
    if validation.get("legal_review_recommended") is not True:
        errors.append("validation.legal_review_recommended must be true")
    if text(validation.get("result")) not in {"pass", "blocked"}:
        errors.append("validation.result must be pass or blocked")
    if errors and text(validation.get("result")) == "pass":
        errors.append("validation.result must not be pass when errors exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate validar-liquidacion-co JSON report")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        data = load_json(Path(args.input))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 3
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"liquidacion_report={'pass' if not errors else 'fail'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
