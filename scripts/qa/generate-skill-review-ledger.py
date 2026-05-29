#!/usr/bin/env python3
"""Generate the one-skill-at-a-time review ledger.

The ledger is intentionally simple CSV so humans and agents can update one row
per reviewed skill without touching the whole skill corpus.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
from datetime import date
from pathlib import Path


DEFAULT_OUTPUT = Path("docs/audits/skill-review-ledger.csv")
FIELDS = [
    "skill",
    "purpose",
    "status",
    "last_reviewed",
    "review_doc",
    "severity",
    "decision",
    "notes",
]


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return Path(result.stdout.strip())


def frontmatter_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    return match.group(1) if match else ""


def purpose_from_skill(path: Path) -> str:
    fm = frontmatter_text(path)
    match = re.search(r"^description:\s*(?:>\s*)?\n?(.*?)(?:\n[A-Za-z_-]+:|\Z)", fm, re.DOTALL | re.MULTILINE)
    if not match:
        return ""
    lines = []
    for raw in match.group(1).splitlines():
        stripped = raw.strip()
        if not stripped or stripped.lower().startswith("trigger:"):
            continue
        lines.append(stripped.strip('"'))
    return " ".join(" ".join(lines).split())


def existing_rows(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {row["skill"]: row for row in reader if row.get("skill")}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or refresh the skill review ledger")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--mark-reviewed", help="Skill slug to mark as reviewed")
    parser.add_argument("--review-doc", default="")
    parser.add_argument("--severity", default="")
    parser.add_argument("--decision", default="")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    root = repo_root()
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    existing = existing_rows(output)
    rows: list[dict[str, str]] = []

    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        slug = skill_md.parent.name
        row = {field: "" for field in FIELDS}
        row.update(existing.get(slug, {}))
        row["skill"] = slug
        row["purpose"] = purpose_from_skill(skill_md)
        row.setdefault("status", "")
        if not row["status"]:
            row["status"] = "pending"
        if args.mark_reviewed == slug:
            row["status"] = "reviewed"
            row["last_reviewed"] = date.today().isoformat()
            row["review_doc"] = args.review_doc
            row["severity"] = args.severity
            row["decision"] = args.decision
            row["notes"] = args.notes
        rows.append(row)

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    reviewed = sum(1 for row in rows if row["status"] == "reviewed")
    print(f"ledger={output.relative_to(root)} skills={len(rows)} reviewed={reviewed} pending={len(rows) - reviewed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
