#!/usr/bin/env python3
"""Compile a deterministic X-Ray scorecard for a skill directory."""

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


def read_policy() -> tuple[dict[str, Any], dict[str, Any]]:
    return load_json(ASSET_DIR / "rubric-policy.json"), load_json(ASSET_DIR / "gate-policy.json")


def normalize_path(path: str) -> str:
    return path.strip().replace("\\", "/").lstrip("./")


def load_files_from_dir(skill_dir: Path) -> dict[str, str]:
    if not skill_dir.exists() or not skill_dir.is_dir():
        raise ValueError(f"skill directory not found: {skill_dir}")
    files: dict[str, str] = {}
    for path in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        rel = normalize_path(str(path.relative_to(skill_dir)))
        try:
            files[rel] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            files[rel] = ""
    return files


def load_files_from_fixture(path: Path) -> dict[str, str]:
    data = load_json(path)
    files = data.get("files")
    if not isinstance(files, dict):
        raise ValueError("fixture must contain a files object")
    return {normalize_path(str(key)): str(value) for key, value in files.items()}


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, str | None]:
    if not text.startswith("---\n"):
        return {}, text, "SKILL.md frontmatter missing opening marker"
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, "SKILL.md frontmatter missing closing marker"
    raw = text[4:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    frontmatter: dict[str, Any] = {}
    current_key = ""
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current_key:
            value = frontmatter.get(current_key, "")
            addition = line.strip().lstrip("-").strip()
            if isinstance(value, list):
                value.append(addition)
            else:
                frontmatter[current_key] = f"{value} {addition}".strip()
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            stripped = value.strip()
            if stripped in {">", "|"}:
                frontmatter[current_key] = ""
            elif stripped == "":
                frontmatter[current_key] = ""
            else:
                frontmatter[current_key] = stripped.strip('"')
        elif line.strip().startswith("-") and current_key:
            existing = frontmatter.get(current_key)
            item = line.strip().lstrip("-").strip()
            if not isinstance(existing, list):
                frontmatter[current_key] = []
            frontmatter[current_key].append(item)
    return frontmatter, body, None


def section_text(body: str, title: str) -> str:
    pattern = re.compile(rf"^##+\s+{re.escape(title)}\b.*$", flags=re.IGNORECASE | re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", body[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(body)
    return body[start:end]


def count_lines(text: str) -> int:
    return len(text.splitlines())


def extract_references(text: str) -> list[str]:
    pattern = re.compile(
        r"(?:`|\b)((?:references|assets|scripts|evals|examples|templates|prompts|agents|knowledge)/[A-Za-z0-9._/-]+)(?:`|\b)"
    )
    refs = []
    for match in pattern.finditer(text):
        ref = normalize_path(match.group(1).rstrip(".,):"))
        if ref not in refs:
            refs.append(ref)
    return refs


def has_component(files: dict[str, str], component: str) -> bool:
    if component.endswith("/"):
        return any(path.startswith(component) for path in files)
    return component in files


def count_edge_cases(body: str) -> int:
    edge = section_text(body, "Edge Cases")
    if not edge:
        return 0
    bold_count = len(re.findall(r"^\s*[-*]\s+\*\*", edge, flags=re.MULTILINE))
    row_count = len([line for line in edge.splitlines() if line.startswith("|") and "---" not in line]) - 1
    bullet_count = len(re.findall(r"^\s*[-*]\s+", edge, flags=re.MULTILINE))
    return max(bold_count, row_count, bullet_count)


def count_assumption_limits(body: str) -> int:
    section = section_text(body, "Assumptions & Limits") or section_text(body, "Assumptions and Limits")
    return len(re.findall(r"^\s*[-*]\s+", section, flags=re.MULTILINE))


def validation_criteria_count(body: str) -> int:
    section = section_text(body, "Validation Gate")
    return len(re.findall(r"^\s*[-*]\s+\[[ xX]\]", section, flags=re.MULTILINE))


def skill_type(files: dict[str, str], skill_lines: int) -> str:
    if len(files) == 1:
        return "single-file"
    if skill_lines >= 400 or has_component(files, "agents/"):
        return "orchestrator"
    return "multi-file"


def evaluate_gates(files: dict[str, str], frontmatter: dict[str, Any], body: str) -> list[dict[str, Any]]:
    skill_text = files.get("SKILL.md", "")
    description = str(frontmatter.get("description", "")).strip()
    references = extract_references(skill_text)
    unresolved = [ref for ref in references if ref not in files and not any(path.startswith(ref.rstrip("/") + "/") for path in files)]
    dangerous = re.search(r"\brm\s+-rf\s+/|\bsudo\b|AKIA[0-9A-Z]{16}|BEGIN PRIVATE KEY", "\n".join(files.values()))
    trigger_count = len(re.findall(r'"[^"]{3,80}"', description))
    lower_text = skill_text.lower()
    gates = [
        (1, "One SKILL.md in top-level directory", list(files).count("SKILL.md") == 1, "`SKILL.md` found at skill root"),
        (2, "Frontmatter has name and description", bool(frontmatter.get("name")) and bool(description), "frontmatter parsed"),
        (
            3,
            "Description is third person, trigger-rich, and pushy",
            "this skill should be used" in description.lower() and trigger_count >= 3 and len(description) <= 1024,
            f"quoted triggers={trigger_count}, length={len(description)}",
        ),
        (
            4,
            "Body uses imperative form",
            not re.search(r"\byou should\b|\byou can\b|\byou need\b", lower_text),
            "no weak second-person modal phrase detected",
        ),
        (5, "SKILL.md under 500 lines", count_lines(skill_text) <= 500, f"lines={count_lines(skill_text)}"),
        (
            6,
            "One or more Good vs Bad examples",
            "good" in lower_text and "bad" in lower_text,
            "Good and Bad markers detected" if "good" in lower_text and "bad" in lower_text else "missing Good vs Bad pair",
        ),
        (
            7,
            "Validation gate has five or more criteria",
            validation_criteria_count(body) >= 5,
            f"criteria={validation_criteria_count(body)}",
        ),
        (
            8,
            "Assumptions and Limits section is specific",
            count_assumption_limits(body) >= 3,
            f"limits={count_assumption_limits(body)}",
        ),
        (9, "Edge Cases section has three or more scenarios", count_edge_cases(body) >= 3, f"edge_cases={count_edge_cases(body)}"),
        (10, "All referenced files exist", not unresolved, "unresolved=" + ",".join(unresolved) if unresolved else "all references resolve"),
        (
            11,
            "Progressive disclosure mechanism is present",
            "load when" in lower_text or "before " in lower_text or "reference files" in lower_text,
            "load condition detected",
        ),
        (12, "No security-compromising content", dangerous is None, "no dangerous token pattern detected"),
        (
            13,
            "Intent matches user-facing description",
            any(term in lower_text for term in ["scorecard", "x-ray report", "diagnostic", "audit"]),
            "diagnostic/report intent detected",
        ),
    ]
    return [
        {"id": gate_id, "checkpoint": checkpoint, "result": "PASS" if passed else "FAIL", "evidence": evidence}
        for gate_id, checkpoint, passed, evidence in gates
    ]


def component_classification(files: dict[str, str]) -> list[dict[str, str]]:
    rows = []
    for component in ["SKILL.md", "references/", "scripts/", "agents/", "evals/evals.json", "assets/", "examples/", "templates/", "prompts/"]:
        present = has_component(files, component)
        if present:
            status = "PRESENT"
            tag = "FORTALEZA"
        elif component == "SKILL.md":
            status = "MISSING-CRITICAL"
            tag = "GAP"
        else:
            status = "MISSING-OPTIONAL"
            tag = "GAP"
        rows.append({"component": component, "status": status, "tag": tag})
    return rows


def score_dimension(key: str, files: dict[str, str], frontmatter: dict[str, Any], body: str, gates: list[dict[str, Any]], policy: dict[str, Any]) -> tuple[int, str, str]:
    text = "\n".join(files.values())
    lower = text.lower()
    failed_gates = [gate for gate in gates if gate["result"] == "FAIL"]
    generic_hits = [marker for marker in policy["genericMarkers"] if marker in text]
    vague_hits = [term for term in policy["vagueTerms"] if re.search(rf"\b{re.escape(term)}\b", lower)]
    unresolved_gate = next((gate for gate in gates if gate["id"] == 10 and gate["result"] == "FAIL"), None)
    skill_lines = count_lines(files.get("SKILL.md", ""))

    if key == "foundation":
        hits = sum(lower.count(signal) for signal in ["because", "trade-off", "rationale", "why", "reason"])
        score = 9 if hits >= 4 else 7 if hits >= 1 else 5
        return score, f"rationale signals={hits}", "SKILL.md/ref rationale scan"
    if key == "truthfulness":
        unsupported = len(re.findall(r"\d+%|\b(always|never|best|guaranteed)\b", lower))
        score = 10 if unsupported == 0 else 8 if unsupported <= 3 else 5
        return score, f"unsupported absolute/percentage signals={unsupported}", "claim scan"
    if key == "quality":
        score = 10
        if failed_gates:
            score -= min(4, len(failed_gates))
        if unresolved_gate:
            score -= 2
        return max(score, 1), f"failed gates={len(failed_gates)}", "13-point gate"
    if key == "density":
        score = 9 if not generic_hits else 5
        if skill_lines > 500:
            score -= 2
        return max(score, 1), f"generic markers={len(generic_hits)}", "scaffold marker scan"
    if key == "simplicity":
        score = 9 if len(vague_hits) <= 2 else 7 if len(vague_hits) <= 8 else 5
        return score, f"vague terms={len(vague_hits)}", "vague qualifier scan"
    if key == "clarity":
        required_words = ["usage", "summary", "gate", "report"]
        hits = sum(1 for word in required_words if word in lower)
        score = 9 if hits >= 4 else 7 if hits >= 3 else 5
        return score, f"clarity anchors={hits}/4", "section/term scan"
    if key == "precision":
        numeric = len(re.findall(r"\b\d+\b", text))
        checkboxes = validation_criteria_count(body)
        score = 10 if numeric >= 10 and checkboxes >= 5 else 8 if numeric >= 5 else 5
        return score, f"numeric thresholds={numeric}, validation criteria={checkboxes}", "threshold scan"
    if key == "depth":
        edges = count_edge_cases(body)
        failures = "Failure Modes" in body
        anti = "Anti-Patterns" in body or "Antipattern" in body
        score = 10 if edges >= 5 and failures and anti else 8 if edges >= 3 and failures else 5
        return score, f"edge_cases={edges}, failure_modes={failures}, antipatterns={anti}", "depth sections"
    if key == "coherence":
        component_count = sum(1 for row in component_classification(files) if row["status"] == "PRESENT")
        score = 10 if not unresolved_gate and component_count >= 6 else 8 if not unresolved_gate else 5
        return score, f"present components={component_count}, unresolved refs={bool(unresolved_gate)}", "component/ref scan"
    if key == "value":
        has_action = "recommended next step" in lower or "fix:" in lower or "specific action" in lower
        score = 9 if has_action and not generic_hits else 6 if has_action else 5
        return score, f"actionable guidance={has_action}, generic markers={len(generic_hits)}", "value scan"
    return 7, "default score", "fallback"


def build_report(files: dict[str, str]) -> dict[str, Any]:
    if "SKILL.md" not in files:
        raise ValueError("SKILL.md not found at skill root")
    rubric_policy, gate_policy = read_policy()
    frontmatter, body, parse_error = parse_frontmatter(files["SKILL.md"])
    if parse_error:
        raise ValueError(parse_error)
    gates = evaluate_gates(files, frontmatter, body)
    scores = []
    for item in rubric_policy["dimensions"]:
        score, finding, evidence = score_dimension(item["key"], files, frontmatter, body, gates, rubric_policy)
        scores.append(
            {
                "id": item["id"],
                "criterion": item["label"],
                "score": score,
                "keyFinding": finding,
                "evidence": evidence,
            }
        )
    average = round(sum(item["score"] for item in scores) / len(scores), 1)
    passed = sum(1 for gate in gates if gate["result"] == "PASS")
    min_score = min(item["score"] for item in scores)
    thresholds = rubric_policy["passThresholds"]
    if min_score >= thresholds["dimensionMinimum"] and average >= thresholds["averageMinimum"] and passed == thresholds["certifiedGateMinimum"]:
        certification = "CERTIFIED"
    elif min_score >= 6 and average >= thresholds["averageMinimum"] and passed >= thresholds["conditionalGateMinimum"]:
        certification = "CONDITIONAL"
    else:
        certification = "BLOCKED"
    gate_status = "PASS" if passed == 13 else "CONDITIONAL" if passed >= 11 else "BLOCKED"
    issues = build_issues(scores, gates, certification)
    return {
        "skill_name": str(frontmatter.get("name") or "unknown-skill"),
        "average": average,
        "gate_status": gate_status,
        "gate_passed": passed,
        "certification": certification,
        "file_count": len(files),
        "total_lines": sum(count_lines(value) for value in files.values()),
        "skill_type": skill_type(files, count_lines(files["SKILL.md"])),
        "rubric_scores": scores,
        "gate_results": gates,
        "top_issues": issues[:5],
        "components": component_classification(files),
        "recommended_next_step": recommended_next_step(certification, issues),
    }


def build_issues(scores: list[dict[str, Any]], gates: list[dict[str, Any]], certification: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for gate in gates:
        if gate["result"] == "FAIL":
            issues.append(
                {
                    "severity": "BLOCKER",
                    "issue": f"Gate {gate['id']} failed: {gate['checkpoint']}",
                    "fix": "Address the checkpoint and rerun the X-Ray compiler.",
                }
            )
    for score in sorted(scores, key=lambda item: item["score"]):
        if score["score"] < 7:
            issues.append(
                {
                    "severity": "WARNING" if certification != "BLOCKED" else "BLOCKER",
                    "issue": f"{score['criterion']} scored {score['score']}/10 ({score['keyFinding']})",
                    "fix": "Use the cited evidence to add specific, testable skill instructions.",
                }
            )
    if not issues:
        issues.append(
            {
                "severity": "INFO",
                "issue": "No certification-blocking issues detected.",
                "fix": "Run certify-skill or keep the current skill unchanged.",
            }
        )
    return issues


def recommended_next_step(certification: str, issues: list[dict[str, str]]) -> str:
    if certification == "CERTIFIED":
        return "No action needed; optionally run certify-skill for an independent final gate."
    if certification == "CONDITIONAL":
        return "Fix the top one or two warnings, then rerun x-ray-skill and certify-skill."
    blocker_count = sum(1 for issue in issues if issue["severity"] == "BLOCKER")
    return f"Run surgeon-skill or patch manually; {blocker_count} blocker issue(s) require resolution."


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def render_markdown(report: dict[str, Any]) -> str:
    score_rows = [
        [item["id"], item["criterion"], f"{item['score']}/10", item["keyFinding"], item["evidence"]]
        for item in report["rubric_scores"]
    ]
    gate_rows = [[item["id"], item["checkpoint"], item["result"], item["evidence"]] for item in report["gate_results"]]
    issue_rows = [[item["severity"], item["issue"], item["fix"]] for item in report["top_issues"]]
    component_rows = [[item["component"], item["status"], item["tag"]] for item in report["components"]]
    return "\n\n".join(
        [
            f"# X-Ray Report: {report['skill_name']}",
            "## Summary\n\n"
            + "\n".join(
                [
                    f"- Overall score: `{report['average']}/10`",
                    f"- Gate: `{report['gate_status']} ({report['gate_passed']}/13)`",
                    f"- Certification readiness: `{report['certification']}`",
                    f"- Files: `{report['file_count']}` files, `{report['total_lines']}` total lines",
                    f"- Skill type: `{report['skill_type']}`",
                ]
            ),
            "## Rubric Scores\n\n" + markdown_table(["#", "Criterion", "Score", "Key Finding", "Evidence"], score_rows),
            "## Gate Results\n\n" + markdown_table(["#", "Checkpoint", "Result", "Evidence"], gate_rows),
            "## Top Issues\n\n" + markdown_table(["Severity", "Issue", "Fix"], issue_rows),
            "## Component Classification\n\n" + markdown_table(["Component", "Status", "Tag"], component_rows),
            "## Recommended Next Step\n\n" + f"- {report['recommended_next_step']}",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a deterministic X-Ray skill report")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--skill-dir", help="Path to a real skill directory")
    source.add_argument("--fixture", help="Path to a virtual skill fixture JSON")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Optional output file")
    args = parser.parse_args()

    try:
        files = load_files_from_fixture(Path(args.fixture)) if args.fixture else load_files_from_dir(Path(args.skill_dir))
        report = build_report(files)
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n" if args.format == "json" else render_markdown(report)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
