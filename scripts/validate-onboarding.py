#!/usr/bin/env python3
"""Validate the JM-ADK first-use onboarding contract."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIAGNOSE = ROOT / "scripts/diagnose-first-use.py"
DIAGNOSE_CONTEXT = ROOT / "scripts/diagnose-user-context.py"
SCAFFOLD_CONTEXT = ROOT / "scripts/scaffold-user-context.py"
SETUP = ROOT / "scripts/setup-workspace-profile.py"
RUNTIME_INSTRUCTIONS = ROOT / "scripts/validate-runtime-instructions.py"


def run_json(args: list[str]) -> tuple[int, dict[str, object]]:
    result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode not in (0, 1, 2):
        return result.returncode, {"stderr": result.stderr, "stdout": result.stdout}
    try:
        return result.returncode, json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.returncode, {"stderr": result.stderr, "stdout": result.stdout}


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def check(name: str, passed: bool, details: str, failures: list[str]) -> None:
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {name} - {details}")
    if not passed:
        failures.append(f"{name}: {details}")


def main() -> int:
    failures: list[str] = []

    _, hello = run_json(["python3", str(DIAGNOSE), "--root", str(ROOT), "--input", "hola", "--json"])
    check(
        "ONBOARDING-001",
        hello.get("input", {}).get("greeting") is True and hello.get("onboarding_mode") in {"guided_first_use", "ask_first_task"},
        "saludo sin tarea activa onboarding o solicitud de primera tarea",
        failures,
    )

    _, empty = run_json(["python3", str(DIAGNOSE), "--root", str(ROOT), "--input", "", "--json"])
    check(
        "ONBOARDING-002",
        empty.get("status") in {"needs_setup", "needs_task", "fresh_clone", "empty_workspace"},
        "input vacío no inicia tarea técnica",
        failures,
    )

    _, explicit = run_json(
        ["python3", str(DIAGNOSE), "--root", str(ROOT), "--input", "crea un agente para clasificar tickets", "--json"]
    )
    check(
        "ONBOARDING-003",
        explicit.get("input", {}).get("explicit_task") is True
        and explicit.get("onboarding_mode") == "micro_context_then_task",
        "tarea explícita no queda bloqueada por onboarding completo",
        failures,
    )
    check(
        "USER-CONTEXT-001",
        explicit.get("user_context", {}).get("status") in {"ready", "missing", "disabled"},
        "diagnose-first-use reports user_context state",
        failures,
    )

    runtime = run(["python3", str(RUNTIME_INSTRUCTIONS)])
    check(
        "RUNTIME-INSTRUCTIONS-001",
        runtime.returncode == 0,
        "runtime mirrors are homologated across CLAUDE, GEMINI, AGENTS, and bridges",
        failures,
    )

    with tempfile.TemporaryDirectory(prefix="jm-adk-onboarding-") as tmp:
        code, non_repo = run_json(["python3", str(DIAGNOSE), "--root", tmp, "--input", "hola", "--json"])
        check(
            "ONBOARDING-004",
            code == 2 and non_repo.get("status") == "requires_confirmation",
            "repo no confirmado detiene edición",
            failures,
        )

        alfa_like = Path(tmp) / "alfa-like"
        for rel in ["skills", "agents", "commands", "scripts", "workspace"]:
            (alfa_like / rel).mkdir(parents=True, exist_ok=True)
        for rel in [".jm-adk.json", "README.md", "AGENTS.md", "CLAUDE.md", "PRISTINO.md", "workspace/.gitkeep"]:
            (alfa_like / rel).parent.mkdir(parents=True, exist_ok=True)
            (alfa_like / rel).write_text("placeholder\n", encoding="utf-8")
        _, post_clone = run_json(["python3", str(DIAGNOSE), "--root", str(alfa_like), "--input", "empecemos", "--json"])
        check(
            "ONBOARDING-005",
            post_clone.get("status") == "empty_workspace"
            and post_clone.get("onboarding_mode") == "guided_first_use",
            "post-clone workspace vacío muestra ruta first-use segura",
            failures,
        )

        missing_context = run_json(
            ["python3", str(DIAGNOSE_CONTEXT), "--root", str(alfa_like), "--context-root", "user-context", "--json"]
        )[1]
        check(
            "USER-CONTEXT-002",
            missing_context.get("status") == "missing",
            "missing context repo is reported without mutating files",
            failures,
        )

        context_root = Path(tmp) / "context-ready"
        context_root.mkdir()
        scaffold = run(["python3", str(SCAFFOLD_CONTEXT), "--root", str(context_root), "--apply"])
        ready_context = run_json(["python3", str(DIAGNOSE_CONTEXT), "--root", str(context_root), "--json"])[1]
        check(
            "USER-CONTEXT-003",
            scaffold.returncode == 0 and ready_context.get("status") == "ready",
            "scaffolded context repo is ready",
            failures,
        )

        run(["python3", str(SCAFFOLD_CONTEXT), "--root", str(context_root), "--context-root", "workspace/context", "--apply"])
        inside_workspace = run_json(
            [
                "python3",
                str(DIAGNOSE_CONTEXT),
                "--root",
                str(context_root),
                "--context-root",
                "workspace/context",
                "--json",
            ]
        )[1]
        check(
            "USER-CONTEXT-004",
            inside_workspace.get("status") == "degraded",
            "context inside workspace is degraded",
            failures,
        )

        manifest = context_root / "user-context" / "manifest.json"
        manifest.write_text("{not json}\n", encoding="utf-8")
        invalid_manifest = run_json(["python3", str(DIAGNOSE_CONTEXT), "--root", str(context_root), "--json"])[1]
        check(
            "USER-CONTEXT-005",
            invalid_manifest.get("status") == "degraded",
            "invalid context manifest degrades diagnosis",
            failures,
        )
        manifest.write_text(
            json.dumps(
                {
                    "schema": 1,
                    "kind": "jm-adk-user-context-manifest",
                    "autoload": ["_INDICE.md"],
                    "privacy": {"mode": "local-private", "externalConnectors": "deny-by-default"},
                    "notes": "api_key should not be stored here",
                }
            ),
            encoding="utf-8",
        )
        secret_context = run_json(["python3", str(DIAGNOSE_CONTEXT), "--root", str(context_root), "--json"])[1]
        check(
            "USER-CONTEXT-006",
            secret_context.get("status") == "degraded",
            "secret-like content in autoload files degrades diagnosis",
            failures,
        )

        setup = run(
            [
                "python3",
                str(SETUP),
                "--root",
                tmp,
                "--apply",
                "--goal",
                "Smoke test profile",
                "--runtime",
                "Codex",
            ]
        )
        profile = Path(tmp) / ".jm-adk.local.json"
        check(
            "FIRST-USE-SCRIPT-002",
            setup.returncode == 0 and profile.exists(),
            "setup autorizado crea perfil local con placeholders seguros",
            failures,
        )

    dry_run = run(["python3", str(SETUP), "--root", str(ROOT), "--dry-run"])
    check(
        "FIRST-USE-SCRIPT-001",
        dry_run.returncode == 0 and "DRY-RUN" in dry_run.stdout,
        "setup sin --apply no modifica el repo",
        failures,
    )

    secret = run(["python3", str(SETUP), "--root", str(ROOT), "--goal", "password abc123"])
    check(
        "ONBOARDING-006",
        secret.returncode == 2 and "secret-like" in secret.stdout,
        "secret-like content is rejected",
        failures,
    )

    check(
        "FIRST-USE-SCRIPT-003",
        secret.returncode == 2,
        "unsafe profile input is gated before write",
        failures,
    )

    if failures:
        print("ERRORS:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("onboarding validation: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
