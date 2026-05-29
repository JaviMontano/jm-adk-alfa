#!/usr/bin/env python3
"""Run safe adversarial tests for JM-ADK guardrails.

The suite creates isolated temporary git repositories for destructive-looking
fixtures, so it can exercise failure paths without touching the local workspace.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable


REQUIRED_FILES = [
    "README.md",
    "agents/lead.md",
    "agents/support.md",
    "agents/guardian.md",
    "agents/specialist.md",
    "knowledge/body-of-knowledge.md",
    "knowledge/knowledge-graph.json",
    "prompts/primary.md",
    "prompts/meta.md",
    "prompts/variations/quick.md",
    "prompts/variations/deep.md",
    "templates/output.md",
    "evals/evals.json",
    "examples/example-input.md",
    "examples/example-output.md",
]


@dataclass
class TestResult:
    name: str
    purpose: str
    risk: str
    fixture: str
    expected: str
    actual: str
    passed: bool
    fix: str


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return Path(result.stdout.strip())


ROOT = repo_root()
SCAFFOLD = ROOT / "scripts" / "scaffold-skill.py"
VALIDATE = ROOT / "scripts" / "validate-skills.py"
BOUNDARIES = ROOT / "scripts" / "check-repo-boundaries.sh"
SYNC = ROOT / "scripts" / "sync-upstream-safe.sh"


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def summarize(process: subprocess.CompletedProcess[str], limit: int = 500) -> str:
    text = "\n".join(part for part in [process.stdout.strip(), process.stderr.strip()] if part)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def init_git(path: Path) -> None:
    process = run(["git", "init", "-b", "main"], path)
    if process.returncode != 0:
        fallback = run(["git", "init"], path)
        if fallback.returncode != 0:
            raise RuntimeError(summarize(fallback))
        run(["git", "checkout", "-b", "main"], path)


def write_skill(base: Path, slug: str, allowed_tools: list[str] | None = None, trigger: str | None = None) -> None:
    skill_dir = base / "skills" / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    tools = allowed_tools or ["Read", "Grep"]
    trigger_value = trigger or slug
    tool_lines = "\n".join(f"  - {tool}" for tool in tools)
    (skill_dir / "SKILL.md").write_text(
        f"""---
name: {slug}
version: 0.1.0
description: "Fixture skill"
triggers:
  - {trigger_value}
allowed-tools:
{tool_lines}
---

# {slug}

## Procedure

Discover, analyze, execute, and validate.

## Quality Criteria

- Fixture is valid enough for validator tests.
""",
        encoding="utf-8",
    )
    for rel in REQUIRED_FILES:
        path = skill_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith(".json"):
            path.write_text('{"schema": 1}\n', encoding="utf-8")
        elif not path.exists():
            path.write_text(f"# {slug} {rel}\n", encoding="utf-8")


def result(
    name: str,
    purpose: str,
    risk: str,
    fixture: str,
    expected: str,
    process: subprocess.CompletedProcess[str],
    passed: bool,
    fix: str,
) -> TestResult:
    return TestResult(
        name=name,
        purpose=purpose,
        risk=risk,
        fixture=fixture,
        expected=expected,
        actual=f"exit={process.returncode}; {summarize(process)}",
        passed=passed,
        fix=fix,
    )


def test_scaffold_rejects_path_traversal() -> TestResult:
    process = run([sys.executable, str(SCAFFOLD), "--name", "../evil", "--dry-run"], ROOT)
    return result(
        "scaffold_rejects_path_traversal",
        "Reject path-like skill names before rendering a target path.",
        "Path traversal or accidental writes outside the intended skill root.",
        "repo root; no files written",
        "non-zero exit and slug-like-name error",
        process,
        process.returncode != 0 and "slug-like name" in process.stderr,
        "Keep name sanitization in scaffold-skill.py.",
    )


def test_scaffold_rejects_duplicate_without_force() -> TestResult:
    process = run(
        [
            sys.executable,
            str(SCAFFOLD),
            "--name",
            "bmad-method",
            "--description",
            "Duplicate fixture",
            "--dry-run",
        ],
        ROOT,
    )
    return result(
        "scaffold_rejects_duplicate_without_force",
        "Refuse an existing skill slug unless --force is explicit.",
        "Silent no-op or overwrite confusion during skill lifecycle work.",
        "existing skills/bmad-method",
        "non-zero exit and skill already exists message",
        process,
        process.returncode != 0 and "skill already exists" in process.stderr,
        "Preserve duplicate-slug guard and require --force after diff review.",
    )


def test_scaffold_rejects_unknown_tool() -> TestResult:
    process = run(
        [
            sys.executable,
            str(SCAFFOLD),
            "--name",
            "qa-bad-tool",
            "--description",
            "Bad tool fixture",
            "--allowed-tools",
            "Read,Destroy",
            "--dry-run",
        ],
        ROOT,
    )
    return result(
        "scaffold_rejects_unknown_tool",
        "Reject unknown tools at scaffold time.",
        "Skills advertise tools an agent runner cannot provide.",
        "repo root; dry-run",
        "non-zero exit and unknown allowed tool message",
        process,
        process.returncode != 0 and "unknown allowed tool" in process.stderr,
        "Keep scaffold allowed-tool validation aligned with validate-skills.py.",
    )


def test_scaffold_local_dry_run_stays_local() -> TestResult:
    process = run(
        [
            sys.executable,
            str(SCAFFOLD),
            "--name",
            "qa-local-smoke",
            "--description",
            "Local dry-run fixture",
            "--local",
            "--dry-run",
        ],
        ROOT,
    )
    return result(
        "scaffold_local_dry_run_stays_local",
        "Confirm local skill mode targets ignored .local/skills.",
        "Experimental skills accidentally enter versioned kit paths.",
        "repo root; dry-run",
        "zero exit and .local/skills target in plan",
        process,
        process.returncode == 0 and ".local/skills/qa-local-smoke/SKILL.md" in process.stdout,
        "Keep .local skill path ignored and visible in dry-run output.",
    )


def test_validator_rejects_unknown_tool_strict() -> TestResult:
    with tempfile.TemporaryDirectory(prefix="jm-adk-qa-") as tmp:
        base = Path(tmp)
        init_git(base)
        write_skill(base, "bad-tool", allowed_tools=["Read", "Destroy"])
        process = run([sys.executable, str(VALIDATE), "--strict"], base)
    return result(
        "validator_rejects_unknown_tool_strict",
        "Fail strict validation when a skill declares an unknown tool.",
        "CI lets unusable skill contracts pass.",
        "temporary git repo with skills/bad-tool",
        "non-zero exit and unknown allowed tool error",
        process,
        process.returncode != 0 and "unknown allowed tool" in process.stdout,
        "Keep unknown-tool findings as errors in strict mode.",
    )


def test_validator_detects_duplicate_high_risk_trigger() -> TestResult:
    with tempfile.TemporaryDirectory(prefix="jm-adk-qa-") as tmp:
        base = Path(tmp)
        init_git(base)
        write_skill(base, "deploy-one", trigger="deploy")
        write_skill(base, "deploy-two", trigger="deploy")
        process = run([sys.executable, str(VALIDATE), "--strict"], base)
    return result(
        "validator_detects_duplicate_high_risk_trigger",
        "Detect duplicated generic activation triggers.",
        "False activation by agents when several skills claim the same broad intent.",
        "temporary git repo with two deploy-trigger skills",
        "non-zero exit and high-risk duplicate trigger error",
        process,
        process.returncode != 0 and "high-risk duplicate trigger 'deploy'" in process.stdout,
        "Keep high-risk duplicate trigger checks active in strict validation.",
    )


def test_validator_reports_invalid_json() -> TestResult:
    with tempfile.TemporaryDirectory(prefix="jm-adk-qa-") as tmp:
        base = Path(tmp)
        init_git(base)
        write_skill(base, "bad-json")
        (base / "skills" / "bad-json" / "evals" / "evals.json").write_text('{"schema": \n', encoding="utf-8")
        process = run([sys.executable, str(VALIDATE), "--strict"], base)
    return result(
        "validator_reports_invalid_json",
        "Fail validation with a concrete path for invalid JSON.",
        "Broken evals or knowledge graph files reach users undetected.",
        "temporary git repo with invalid evals/evals.json",
        "non-zero exit and invalid JSON path",
        process,
        process.returncode != 0 and "invalid JSON" in process.stdout and "evals/evals.json" in process.stdout,
        "Keep JSON validation for evals and knowledge graph files.",
    )


def test_boundaries_detect_tracked_codex() -> TestResult:
    with tempfile.TemporaryDirectory(prefix="jm-adk-qa-") as tmp:
        base = Path(tmp)
        init_git(base)
        codex_config = base / ".codex" / "config.toml"
        codex_config.parent.mkdir()
        codex_config.write_text("model = 'fixture'\n", encoding="utf-8")
        run(["git", "add", ".codex/config.toml"], base)
        process = run(["bash", str(BOUNDARIES)], base)
    return result(
        "boundaries_detect_tracked_codex",
        "Reject tracked Codex local state.",
        "Agent-specific local config leaks into the shared kit.",
        "temporary git repo with staged .codex/config.toml",
        "non-zero exit and tracked .codex state error",
        process,
        process.returncode != 0 and "tracked .codex state" in process.stderr,
        "Keep .codex in .gitignore and boundary checks.",
    )


def test_boundaries_detect_nested_git() -> TestResult:
    with tempfile.TemporaryDirectory(prefix="jm-adk-qa-") as tmp:
        base = Path(tmp)
        init_git(base)
        nested = base / "fixtures" / "nested" / ".git"
        nested.mkdir(parents=True)
        process = run(["bash", str(BOUNDARIES)], base)
    return result(
        "boundaries_detect_nested_git",
        "Reject nested .git directories.",
        "A cloned repo inside the kit becomes invisible or dangerous during updates.",
        "temporary git repo with fixtures/nested/.git",
        "non-zero exit and nested git repository error",
        process,
        process.returncode != 0 and "nested git repository" in process.stderr,
        "Keep nested repository detection in boundary checks.",
    )


def test_sync_aborts_dirty_tree() -> TestResult:
    with tempfile.TemporaryDirectory(prefix="jm-adk-qa-") as tmp:
        base = Path(tmp)
        init_git(base)
        (base / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        process = run(["bash", str(SYNC), "--remote", "origin"], base)
    return result(
        "sync_aborts_dirty_tree",
        "Abort sync before remote operations when the working tree is dirty.",
        "Safe update scripts overwrite or mix local work.",
        "temporary git repo with untracked dirty.txt",
        "non-zero exit and working tree is not clean",
        process,
        process.returncode != 0 and "working tree is not clean" in process.stderr,
        "Keep dirty-tree gate before fetch/merge/push operations.",
    )


def test_scripts_run_from_subdirectory() -> TestResult:
    process = run([sys.executable, str(ROOT / "scripts" / "count-components.py"), "--check-docs"], ROOT / "docs")
    return result(
        "scripts_run_from_subdirectory",
        "Confirm scripts resolve the git root instead of assuming cwd=root.",
        "Vibe coders run commands from docs or skill folders and get false failures.",
        "repo docs/ directory",
        "zero exit and component counts",
        process,
        process.returncode == 0 and "components=1296" in process.stdout,
        "Keep git rev-parse root detection in repo scripts.",
    )


TESTS: list[Callable[[], TestResult]] = [
    test_scaffold_rejects_path_traversal,
    test_scaffold_rejects_duplicate_without_force,
    test_scaffold_rejects_unknown_tool,
    test_scaffold_local_dry_run_stays_local,
    test_validator_rejects_unknown_tool_strict,
    test_validator_detects_duplicate_high_risk_trigger,
    test_validator_reports_invalid_json,
    test_boundaries_detect_tracked_codex,
    test_boundaries_detect_nested_git,
    test_sync_aborts_dirty_tree,
    test_scripts_run_from_subdirectory,
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run JM-ADK adversarial QA tests")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    args = parser.parse_args()

    results = [test() for test in TESTS]
    if args.json:
        print(json.dumps([asdict(item) for item in results], indent=2, ensure_ascii=False))
    else:
        for item in results:
            status = "PASS" if item.passed else "FAIL"
            print(f"{status} {item.name}")
            print(f"  purpose: {item.purpose}")
            print(f"  risk: {item.risk}")
            print(f"  expected: {item.expected}")
            print(f"  actual: {item.actual}")
            if not item.passed:
                print(f"  fix: {item.fix}")
        passed = sum(1 for item in results if item.passed)
        print(f"summary: passed={passed} failed={len(results) - passed} total={len(results)}")
    return 0 if all(item.passed for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
