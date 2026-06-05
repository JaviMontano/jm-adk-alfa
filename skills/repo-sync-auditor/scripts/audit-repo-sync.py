#!/usr/bin/env python3
"""Audit repository sync state without mutating Git history or files."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GENERATED_FILES = [
    ".agent/skills_index.json",
    "PRISTINO-INDEX.md",
    "AGENTS.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
    ".cursorrules",
    ".windsurfrules",
]


def run_git(root: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def resolve_root(path: str | None) -> Path:
    start = Path(path or ".").resolve()
    code, output = run_git(start, ["rev-parse", "--show-toplevel"])
    if code != 0:
        raise SystemExit(f"ERROR: not a git repository: {start}\n{output}")
    return Path(output).resolve()


def git_value(root: Path, args: list[str], default: str = "") -> str:
    code, output = run_git(root, args)
    return output if code == 0 else default


def ref_exists(root: Path, ref: str) -> bool:
    code, _ = run_git(root, ["show-ref", "--verify", "--quiet", ref])
    return code == 0


def ahead_behind(root: Path, left: str, right: str) -> dict[str, int] | None:
    code, output = run_git(root, ["rev-list", "--left-right", "--count", f"{left}...{right}"])
    if code != 0:
        return None
    parts = output.split()
    if len(parts) != 2:
        return None
    return {"behind": int(parts[0]), "ahead": int(parts[1])}


def status_path(line: str) -> str:
    if line.startswith("?? "):
        return line[3:]
    if len(line) >= 4 and line[2] == " ":
        return line[3:]
    return line[2:].lstrip()


def git_report(root: Path) -> dict[str, Any]:
    branch = git_value(root, ["branch", "--show-current"], "DETACHED")
    head = git_value(root, ["rev-parse", "HEAD"])
    upstream = git_value(root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    status_lines = git_value(root, ["status", "--porcelain=v1"]).splitlines()
    dirty_files = [status_path(line) for line in status_lines]

    origin_main = ""
    origin_main_ref = "refs/remotes/origin/main"
    if ref_exists(root, origin_main_ref):
        origin_main = git_value(root, ["rev-parse", "origin/main"])

    ahead: dict[str, Any] = {}
    if upstream:
        ahead["upstream"] = ahead_behind(root, upstream, "HEAD")
    if origin_main:
        ahead["origin_main"] = ahead_behind(root, "origin/main", "HEAD")

    return {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "origin_main": origin_main,
        "dirty_count": len(status_lines),
        "dirty_files": dirty_files[:50],
        "ahead_behind": ahead,
    }


def read_ledger(root: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    path = root / "docs" / "audits" / "skill-review-ledger.csv"
    if not path.exists():
        return {}, [f"missing ledger: {path}"]
    rows: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                slug = (row.get("skill") or "").strip()
                if slug:
                    rows[slug] = {str(k): str(v or "") for k, v in row.items() if k}
    except Exception as exc:  # noqa: BLE001
        errors.append(f"ledger parse error: {exc}")
    return rows, errors


def list_skills(root: Path) -> list[str]:
    skills_dir = root / "skills"
    if not skills_dir.exists():
        return []
    return sorted(p.name for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def review_docs(root: Path) -> dict[str, str]:
    review_dir = root / "docs" / "audits" / "skills"
    if not review_dir.exists():
        return {}
    docs: dict[str, str] = {}
    for path in sorted(review_dir.glob("*-review.md")):
        docs[path.name.removesuffix("-review.md")] = str(path.relative_to(root))
    return docs


def script_skills(root: Path, skills: list[str]) -> list[str]:
    return [slug for slug in skills if (root / "skills" / slug / "scripts" / "check.sh").exists()]


def ledger_report(root: Path) -> dict[str, Any]:
    rows, errors = read_ledger(root)
    skills = list_skills(root)
    docs = review_docs(root)
    scripted = script_skills(root, skills)

    untracked = [slug for slug in skills if slug not in rows]
    review_docs_pending = [
        slug for slug in docs if rows.get(slug, {}).get("status", "missing") != "dod-complete"
    ]
    script_skills_pending = [
        slug for slug in scripted if rows.get(slug, {}).get("status", "missing") != "dod-complete"
    ]
    complete_missing_review = [
        slug for slug, row in rows.items() if row.get("status") == "dod-complete" and slug not in docs
    ]

    return {
        "ledger_path": "docs/audits/skill-review-ledger.csv",
        "ledger_rows": len(rows),
        "ledger_errors": errors,
        "skill_count": len(skills),
        "untracked_skill_count": len(untracked),
        "untracked_skills": untracked[:50],
        "dod_complete_count": sum(1 for row in rows.values() if row.get("status") == "dod-complete"),
        "review_doc_count": len(docs),
        "review_docs_pending_count": len(review_docs_pending),
        "review_docs_pending": review_docs_pending[:50],
        "dod_complete_missing_review_count": len(complete_missing_review),
        "dod_complete_missing_review": complete_missing_review[:50],
        "script_skill_count": len(scripted),
        "script_skills_pending_count": len(script_skills_pending),
        "script_skills_pending": script_skills_pending[:50],
    }


def generated_report(root: Path, dirty_files: list[str]) -> dict[str, Any]:
    dirty_set = set(dirty_files)
    tracked = [path for path in GENERATED_FILES if (root / path).exists()]
    dirty = [path for path in tracked if path in dirty_set]
    return {
        "tracked": tracked,
        "dirty": dirty,
        "dirty_count": len(dirty),
        "note": "Run adapter/index generators separately; this audit does not mutate generated files.",
    }


def classify(git: dict[str, Any], ledger: dict[str, Any], generated: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if git["dirty_count"]:
        blockers.append({
            "id": "dirty_tree",
            "severity": "high",
            "message": f"working tree has {git['dirty_count']} dirty or untracked entries",
            "evidence": "[CODE] git status --porcelain=v1",
        })
    origin_state = git.get("ahead_behind", {}).get("origin_main")
    if origin_state and origin_state.get("behind", 0) > 0:
        blockers.append({
            "id": "behind_origin_main",
            "severity": "high",
            "message": f"HEAD is behind origin/main by {origin_state['behind']} commits",
            "evidence": "[CODE] git rev-list --left-right --count origin/main...HEAD",
        })
    if ledger["ledger_errors"]:
        blockers.append({
            "id": "ledger_parse_error",
            "severity": "high",
            "message": "; ".join(ledger["ledger_errors"]),
            "evidence": "[CODE] docs/audits/skill-review-ledger.csv",
        })
    if ledger["untracked_skill_count"]:
        blockers.append({
            "id": "untracked_skills",
            "severity": "high",
            "message": f"{ledger['untracked_skill_count']} skill directories are absent from the ledger",
            "evidence": "[CODE] skills/* vs docs/audits/skill-review-ledger.csv",
        })
    if ledger["review_docs_pending_count"]:
        blockers.append({
            "id": "review_docs_pending",
            "severity": "medium",
            "message": f"{ledger['review_docs_pending_count']} review docs map to non-complete ledger rows",
            "evidence": "[CODE] docs/audits/skills/*-review.md",
        })
    if ledger["script_skills_pending_count"]:
        blockers.append({
            "id": "script_skills_pending",
            "severity": "medium",
            "message": f"{ledger['script_skills_pending_count']} script-backed skills are not dod-complete in the ledger",
            "evidence": "[CODE] skills/*/scripts/check.sh",
        })
    if generated["dirty_count"]:
        blockers.append({
            "id": "generated_files_dirty",
            "severity": "medium",
            "message": f"{generated['dirty_count']} generated adapter/index files are dirty",
            "evidence": "[CODE] git status --porcelain=v1",
        })
    return blockers


def recommendations(blockers: list[dict[str, str]]) -> list[str]:
    ids = {item["id"] for item in blockers}
    recs: list[str] = []
    if "dirty_tree" in ids:
        recs.append("[INFERENCE] Commit, stash, or isolate local edits before switching branches or applying patches.")
    if "behind_origin_main" in ids:
        recs.append("[INFERENCE] Recreate the work branch from updated origin/main before opening a PR.")
    if {"untracked_skills", "review_docs_pending", "script_skills_pending"} & ids:
        recs.append("[INFERENCE] Prefer a dedicated ledger reconciliation PR before trusting cursor counts.")
    if "generated_files_dirty" in ids:
        recs.append("[INFERENCE] Regenerate and review adapters/PRISTINO in the same PR that changes skill metadata.")
    if not recs:
        recs.append("[INFERENCE] Repository state is ready for a scoped PR from the audited baseline.")
    return recs


def build_report(root: Path) -> dict[str, Any]:
    git = git_report(root)
    ledger = ledger_report(root)
    generated = generated_report(root, git["dirty_files"])
    blockers = classify(git, ledger, generated)
    return {
        "schema": 1,
        "skill": "repo-sync-auditor",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "git": git,
        "ledger": ledger,
        "generated_files": generated,
        "blockers": blockers,
        "recommendations": recommendations(blockers),
        "evidence": [
            "[CODE] git rev-parse, git status, git rev-list, local refs",
            "[CODE] docs/audits/skill-review-ledger.csv",
            "[CODE] docs/audits/skills/*-review.md",
            "[CODE] skills/*/scripts/check.sh",
            "[CONFIG] audit is local-ref and read-only by default",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    git = report["git"]
    ledger = report["ledger"]
    generated = report["generated_files"]
    lines = [
        "# Repo Sync Audit",
        "",
        f"[CODE] Root: `{report['root']}`",
        f"[CODE] Branch: `{git['branch']}`",
        f"[CODE] HEAD: `{git['head']}`",
        f"[CODE] Upstream: `{git['upstream'] or 'none'}`",
        f"[CODE] origin/main: `{git['origin_main'] or 'missing-local-ref'}`",
        f"[CODE] Dirty entries: `{git['dirty_count']}`",
        "",
        "## Ledger",
        "",
        f"[CODE] Ledger rows: `{ledger['ledger_rows']}`",
        f"[CODE] Skill directories: `{ledger['skill_count']}`",
        f"[CODE] Untracked skills: `{ledger['untracked_skill_count']}`",
        f"[CODE] Review docs pending in ledger: `{ledger['review_docs_pending_count']}`",
        f"[CODE] Script-backed skills pending in ledger: `{ledger['script_skills_pending_count']}`",
        "",
        "## Generated Files",
        "",
        f"[CODE] Dirty generated files: `{generated['dirty_count']}`",
        f"[CONFIG] {generated['note']}",
        "",
        "## Blockers",
        "",
    ]
    if report["blockers"]:
        for item in report["blockers"]:
            lines.append(f"- {item['evidence']} `{item['severity']}` `{item['id']}`: {item['message']}")
    else:
        lines.append("- [CODE] No blockers detected.")
    lines.extend(["", "## Recommendations", ""])
    lines.extend(f"- {rec}" for rec in report["recommendations"])
    lines.extend(["", "## Evidence", ""])
    lines.extend(f"- {item}" for item in report["evidence"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only repository sync audit")
    parser.add_argument("--root", help="Repository root or child path. Defaults to current directory.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    root = resolve_root(args.root)
    report = build_report(root)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
