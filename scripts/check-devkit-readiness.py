#!/usr/bin/env python3
"""Check JM-ADK developer-kit readiness without changing files."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "CLAUDE.md",
    "AGENTS.md",
    "GEMINI.md",
    "CODEX.md",
    "ANTIGRAVITY.md",
    "docs/FIRST_USE_ONBOARDING.md",
    "docs/WORKSPACE_SETUP.md",
    "docs/PROMPTING.md",
    "docs/META_PROMPTING.md",
    "docs/SCRIPTING_AND_BASH.md",
    "docs/EVALS.md",
    "docs/NO_REGRESSION_CHECKLIST.md",
    "docs/TROUBLESHOOTING.md",
    "docs/ARCHIVE_POLICY.md",
    "docs/audits/local-pattern-inventory.md",
    "references/ontology/user-context-contract.md",
    "user-context/.jm-adk-context.json",
    "user-context/README.md",
    "user-context/AGENTS.md",
    "user-context/_INDICE.md",
    "user-context/schemas/user-context-manifest.schema.json",
    "scripts/diagnose-user-context.py",
    "scripts/scaffold-user-context.py",
    "scripts/validate-runtime-instructions.py",
    "evals/onboarding/evals.json",
    "agents/first-use-onboarding-agent.md",
    "agents/workspace-diagnostic-agent.md",
    "agents/runtime-routing-agent.md",
    "agents/task-intake-agent.md",
    "commands/first-use.md",
    "commands/diagnose-workspace.md",
    "commands/setup-workspace.md",
    "commands/validate-onboarding.md",
    "commands/explain-devkit.md",
    "commands/start-task.md",
    "scripts/diagnose-first-use.py",
    "scripts/setup-workspace-profile.py",
    "scripts/validate-onboarding.py",
    "scripts/check-devkit-readiness.py",
]

REQUIRED_SKILLS = [
    "first-use-onboarding",
    "workspace-setup",
    "runtime-routing",
    "prompting-and-meta-prompting",
    "safe-scripting-and-bash",
]


def valid_json(path: Path) -> tuple[bool, str]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True, "ok"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def tracked(path: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", path],
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    for skill in REQUIRED_SKILLS:
        if not (ROOT / "skills" / skill / "SKILL.md").exists():
            errors.append(f"missing required skill: {skill}")

    for rel in [".jm-adk.json", ".claude-plugin/plugin.json", "evals/onboarding/evals.json"]:
        path = ROOT / rel
        if path.exists():
            ok, detail = valid_json(path)
            if not ok:
                errors.append(f"invalid JSON in {rel}: {detail}")

    for local in [".jm-adk.local.json", ".env", ".env.local"]:
        if tracked(local):
            errors.append(f"local or secret-bearing file is tracked: {local}")

    runtime = subprocess.run(
        ["python3", str(ROOT / "scripts/validate-runtime-instructions.py")],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if runtime.returncode != 0:
        detail = runtime.stdout.strip() or runtime.stderr.strip()
        errors.append(f"runtime instruction validation failed: {detail}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("devkit readiness: passed")
    print("required files: present")
    print("required skills: present")
    print("local override files: untracked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
