#!/usr/bin/env python3
"""Render one personalized follow-up email from structured meeting data."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path


REQUIRED_ROOT_FIELDS = ["meeting_title", "date", "sender_name", "next_steps", "recipients"]
REQUIRED_RECIPIENT_FIELDS = ["name", "email", "action_items"]
REQUIRED_ITEM_FIELDS = ["task", "deadline", "context", "priority"]


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("data must be a JSON object")
    missing = [field for field in REQUIRED_ROOT_FIELDS if field not in data]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")
    recipients = data.get("recipients")
    if not isinstance(recipients, list) or not recipients:
        raise ValueError("recipients must be a non-empty list")
    for recipient in recipients:
        if not isinstance(recipient, dict):
            raise ValueError("each recipient must be an object")
        missing_recipient = [field for field in REQUIRED_RECIPIENT_FIELDS if field not in recipient]
        if missing_recipient:
            raise ValueError(f"recipient missing field(s): {', '.join(missing_recipient)}")
        items = recipient.get("action_items")
        if not isinstance(items, list):
            raise ValueError("recipient action_items must be a list")
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("each action item must be an object")
            missing_item = [field for field in REQUIRED_ITEM_FIELDS if field not in item]
            if missing_item:
                raise ValueError(f"action item missing field(s): {', '.join(missing_item)}")
    return data


def select_recipient(data: dict[str, object], email: str) -> dict[str, object]:
    for recipient in data["recipients"]:  # type: ignore[index]
        if isinstance(recipient, dict) and str(recipient.get("email", "")).lower() == email.lower():
            return recipient
    raise ValueError(f"recipient not found: {email}")


def load_tokens(base: Path) -> dict[str, object]:
    tokens_path = base / "assets" / "email-copy-tokens.json"
    data = json.loads(tokens_path.read_text(encoding="utf-8"))
    return data.get("tokens", {}) if isinstance(data, dict) else {}


def render_markdown(data: dict[str, object], recipient: dict[str, object], tokens: dict[str, object]) -> str:
    subject = f"{tokens.get('subject_prefix', 'Seguimiento')}: {data['meeting_title']}"
    signoff = str(tokens.get("default_signoff", "Saludos"))
    lines = [
        f"Subject: {subject}",
        "",
        f"Hola {recipient['name']},",
        "",
        f"Gracias por participar en la reunion \"{data['meeting_title']}\" del {data['date']}.",
        "",
        "## Tus Action Items",
        "",
    ]
    action_items = recipient.get("action_items", [])
    if not action_items:
        lines.append("No tienes action items asignados en este seguimiento.")
    else:
        for item in action_items:  # type: ignore[assignment]
            priority = str(item["priority"]).upper()
            lines.extend(
                [
                    f"- [ ] **{item['task']}**",
                    f"  - Prioridad: {priority}",
                    f"  - Fecha limite: {item['deadline']}",
                    f"  - Contexto: {item['context']}",
                ]
            )
    lines.extend(
        [
            "",
            "## Proximos Pasos",
            "",
            str(data["next_steps"]),
            "",
            "Si tienes dudas sobre alguno de estos puntos, responde a este correo antes de la fecha limite.",
            "",
            f"{signoff},",
            str(data["sender_name"]),
        ]
    )
    return "\n".join(lines) + "\n"


def markdown_to_html(markdown: str, css: str) -> str:
    body_lines = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            body_lines.append("")
        elif line.startswith("Subject:"):
            body_lines.append(f"<div class=\"meta\">{html.escape(line)}</div>")
        elif line.startswith("## "):
            body_lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("- [ ] "):
            body_lines.append(f"<div class=\"action-item\">{html.escape(line[6:])}</div>")
        elif line.startswith("- "):
            body_lines.append(f"<p>{html.escape(line)}</p>")
        else:
            body_lines.append(f"<p>{html.escape(line)}</p>")
    return (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"UTF-8\">\n"
        f"<style>\n{css}\n</style>\n</head>\n<body>\n<div class=\"email\">\n"
        + "\n".join(body_lines)
        + "\n</div>\n</body>\n</html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a personalized follow-up email")
    parser.add_argument("--data", required=True, help="Structured meeting JSON")
    parser.add_argument("--recipient", required=True, help="Recipient email to render")
    parser.add_argument("--format", choices=["markdown", "html"], default="markdown")
    parser.add_argument("--output", help="Write output to path; stdout by default")
    args = parser.parse_args()

    base = skill_dir()
    data = load_json(Path(args.data))
    recipient = select_recipient(data, args.recipient)
    tokens = load_tokens(base)
    rendered = render_markdown(data, recipient, tokens)
    if args.format == "html":
        css = (base / "assets" / "email-style.css").read_text(encoding="utf-8")
        rendered = markdown_to_html(rendered, css)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
