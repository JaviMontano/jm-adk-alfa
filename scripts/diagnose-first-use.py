#!/usr/bin/env python3
"""Diagnose JM-ADK first-use readiness without modifying files."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


TARGET_REPO = "JaviMontano/jm-adk-alfa"
GREETING_INPUTS = {"hola", "buenas", "hey", "hello", "empecemos"}
TASK_VERBS = {
    "add",
    "analyze",
    "build",
    "create",
    "crea",
    "debug",
    "fix",
    "implement",
    "mejora",
    "modify",
    "review",
    "update",
}
ALFA_SIGNALS = [
    ".jm-adk.json",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "PRISTINO.md",
    "skills",
    "agents",
    "commands",
    "scripts",
]


def git_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    return start.resolve()


def git_remotes(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "remote", "-v"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def has_alfa_signals(root: Path) -> bool:
    return sum(1 for signal in ALFA_SIGNALS if (root / signal).exists()) >= 5


def confirmed_alfa(root: Path) -> bool:
    return any(TARGET_REPO in remote for remote in git_remotes(root)) or has_alfa_signals(root)


def local_profile_exists(root: Path) -> bool:
    return (root / ".jm-adk.local.json").exists()


def workspace_registry_exists(root: Path) -> bool:
    return (root / "workspace/.workspace-registry.json").exists()


def workspace_has_user_state(root: Path) -> bool:
    workspace = root / "workspace"
    if not workspace.exists():
        return False
    for path in workspace.rglob("*"):
        rel = path.relative_to(workspace)
        if rel.parts and rel.parts[0] == "archive":
            continue
        if path.name == ".gitkeep":
            continue
        return True
    return False


def active_workspace(root: Path) -> str | None:
    registry = root / "workspace/.workspace-registry.json"
    if not registry.exists():
        return None
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    value = data.get("activeWorkspace")
    return value if isinstance(value, str) and value else None


def has_task_context(root: Path) -> bool:
    candidates = [
        "workspace",
        "docs/audits",
        "PRISTINO-INDEX.md",
    ]
    return bool(active_workspace(root)) or any((root / item).exists() for item in candidates)


def user_context_status(root: Path) -> dict[str, object]:
    script = root / "scripts" / "diagnose-user-context.py"
    if not script.exists():
        return {"status": "missing", "enabled": False, "error": "diagnose-user-context.py missing"}
    result = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--json", "--dry-run"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "status": "degraded",
            "enabled": True,
            "error": result.stderr.strip() or result.stdout.strip() or "invalid user-context diagnosis",
        }
    return {
        "status": data.get("status"),
        "enabled": data.get("enabled"),
        "context_root": data.get("context_root"),
        "problems": data.get("problems", []),
    }


def classify_input(text: str) -> dict[str, bool]:
    normalized = " ".join(text.lower().strip().split())
    if not normalized:
        return {"empty": True, "greeting": False, "explicit_task": False}
    words = set(normalized.replace("/", " ").replace(":", " ").split())
    return {
        "empty": False,
        "greeting": normalized in GREETING_INPUTS,
        "explicit_task": bool(words.intersection(TASK_VERBS)) or len(normalized.split()) >= 4,
    }


def diagnose(root: Path, user_input: str) -> dict[str, object]:
    is_alfa = confirmed_alfa(root)
    input_state = classify_input(user_input)
    profile = local_profile_exists(root)
    registry = workspace_registry_exists(root)
    workspace_empty = not workspace_has_user_state(root)
    active = active_workspace(root)
    task_context = has_task_context(root)
    context = user_context_status(root) if is_alfa else {"status": "unknown", "enabled": False}

    if not is_alfa:
        status = "requires_confirmation"
        onboarding_mode = "stop"
    elif input_state["explicit_task"]:
        status = "ready" if profile or task_context else "needs_setup"
        onboarding_mode = "micro_context_then_task"
    elif input_state["greeting"] or input_state["empty"]:
        status = "empty_workspace" if not profile and workspace_empty else ("needs_setup" if not profile else "needs_task")
        onboarding_mode = "guided_first_use"
    elif not profile:
        status = "fresh_clone" if not registry else "needs_setup"
        onboarding_mode = "guided_first_use"
    elif not active:
        status = "needs_task"
        onboarding_mode = "ask_first_task"
    else:
        status = "ready"
        onboarding_mode = "continue"

    return {
        "schema": 1,
        "repo_root": str(root),
        "target_repo": TARGET_REPO,
        "confirmed_alfa": is_alfa,
        "status": status,
        "onboarding_mode": onboarding_mode,
        "input": {
            "empty": input_state["empty"],
            "greeting": input_state["greeting"],
            "explicit_task": input_state["explicit_task"],
        },
        "signals": {
            "local_profile": profile,
            "workspace_registry": registry,
            "workspace_empty": workspace_empty,
            "active_workspace": active,
            "task_context": task_context,
        },
        "user_context": context,
        "next_action": next_action(status, onboarding_mode),
    }


def next_action(status: str, onboarding_mode: str) -> str:
    if status == "requires_confirmation":
        return "Dato requerido: confirmar ruta o remote de Alfa antes de editar."
    if onboarding_mode == "guided_first_use":
        return "Run first-use guided setup before starting technical work."
    if onboarding_mode == "micro_context_then_task":
        return "Collect only missing critical context, then proceed with the explicit task."
    if onboarding_mode == "ask_first_task":
        return "Ask for the first concrete task."
    return "Proceed with normal JM-ADK workflow."


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose JM-ADK first-use readiness")
    parser.add_argument("--root", default=".", help="Directory to inspect")
    parser.add_argument("--input", default="", help="User input to classify")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--dry-run", action="store_true", help="Compatibility flag; diagnosis is always read-only")
    args = parser.parse_args()

    root = git_root(Path(args.root))
    result = diagnose(root, args.input)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"STATUS: {result['status']}")
        print(f"ONBOARDING: {result['onboarding_mode']}")
        print(f"CONFIRMED_ALFA: {str(result['confirmed_alfa']).lower()}")
        print(f"NEXT: {result['next_action']}")
    return 0 if result["status"] != "requires_confirmation" else 2


if __name__ == "__main__":
    raise SystemExit(main())
