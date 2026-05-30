#!/usr/bin/env python3
"""Deterministic, additive, idempotent quality pass over every skill (Etapa H).

Applies the katas lessons mechanically and SAFELY to all skills:
  - knowledge-graph.json: add ontology / evidence / anti-pattern nodes + edges
    (Kata 20 provenance, Kata 30 anti-pattern awareness) — never removes nodes.
  - evals/evals.json: ensure the canonical edge cases exist (Kata 30 false
    positives, empty input) — never removes cases.

It ONLY touches files that match the scaffold schema; anything custom is reported
and left untouched. Default is dry-run; pass --apply to write. Re-running is a
no-op (idempotent), so it is safe in CI and on every upgrade.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True,
                         text=True, stdout=subprocess.PIPE).stdout.strip()
    return Path(out)


def classify_domain(slug: str) -> str:
    """Coarse ontology bucket for the skill, derived from name. Additive only."""
    table = [
        (("hook", "guardrail", "pretooluse", "posttooluse"), "agentic-architecture/hooks"),
        (("loop", "agentic", "subagent", "hub-and-spoke", "orchestration", "handoff", "escalation", "multiagent", "investigation"), "agentic-architecture"),
        (("mcp", "tool-use", "tool-description", "builtin-tool", "structured-output", "extraction"), "tool-design-mcp"),
        (("claude-md", "path-", "plan-mode", "custom-commands", "custom-tooling", "session", "memory"), "claude-code-config"),
        (("fewshot", "few-shot", "chaining", "retry", "validation", "review", "confidence", "false-positive", "evaluation", "self-correction"), "prompt-structured-output"),
        (("prefix", "context-", "dilution", "scratchpad", "provenance", "persistent"), "context-reliability"),
    ]
    for needles, bucket in table:
        if any(n in slug for n in needles):
            return bucket
    return "general"


def node_ids(graph: dict) -> set:
    return {str(n.get("id")) for n in graph.get("nodes", []) if isinstance(n, dict)}


def edge_key(e: dict) -> tuple:
    return (str(e.get("from")), str(e.get("to")), str(e.get("type")))


def edge_keys(graph: dict) -> set:
    return {edge_key(e) for e in graph.get("edges", []) if isinstance(e, dict)}


def enrich_graph(path: Path, slug: str) -> bool:
    """Return True if the file was (or would be) changed. Idempotent."""
    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if not isinstance(graph, dict) or not isinstance(graph.get("nodes"), list) or not isinstance(graph.get("edges"), list):
        return False  # custom shape -> leave untouched

    changed = False
    ids = node_ids(graph)
    keys = edge_keys(graph)
    domain = classify_domain(slug)

    add_nodes = [
        {"id": f"{slug}:ontology", "type": "ontology", "label": f"Domain: {domain}"},
        {"id": f"{slug}:evidence", "type": "gate", "label": "Evidence / provenance requirements"},
        {"id": f"{slug}:antipattern", "type": "risk", "label": "Canonical anti-pattern to avoid"},
    ]
    for node in add_nodes:
        if node["id"] not in ids:
            graph["nodes"].append(node)
            ids.add(node["id"])
            changed = True

    add_edges = [
        {"from": slug, "to": f"{slug}:ontology", "type": "classified_as"},
        {"from": slug, "to": f"{slug}:evidence", "type": "validated_by"},
        {"from": slug, "to": f"{slug}:antipattern", "type": "guards_against"},
    ]
    for edge in add_edges:
        if edge_key(edge) not in keys:
            graph["edges"].append(edge)
            keys.add(edge_key(edge))
            changed = True

    if changed:
        path.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


CANONICAL_CASES = {
    "false_positive": ("This request is unrelated to the skill domain.", False),
    "empty_input": ("", False),
}


def enrich_evals(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return False

    have = {str(c.get("id")) for c in data["cases"] if isinstance(c, dict)}
    changed = False
    for cid, (text, expected) in CANONICAL_CASES.items():
        if cid not in have:
            data["cases"].append({
                "id": cid, "input": text, "expected_activation": expected,
                "expected_checks": ["evidence", "quality_criteria", "upgrade_safety"],
            })
            changed = True
    if changed:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic additive skill improver (Etapa H)")
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run report)")
    parser.add_argument("--skills-dir", default="skills")
    parser.add_argument("--only-prefix", default="", help="Limit to skills whose name starts with this prefix")
    args = parser.parse_args()

    root = repo_root()
    skills_dir = root / args.skills_dir
    graphs_changed = evals_changed = scanned = skipped_custom = 0

    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        if args.only_prefix and not skill_dir.name.startswith(args.only_prefix):
            continue
        scanned += 1
        slug = skill_dir.name
        graph_path = skill_dir / "knowledge" / "knowledge-graph.json"
        evals_path = skill_dir / "evals" / "evals.json"

        if graph_path.exists():
            if args.apply:
                if enrich_graph(graph_path, slug):
                    graphs_changed += 1
            else:
                # dry-run: load + simulate
                try:
                    g = json.loads(graph_path.read_text(encoding="utf-8"))
                    if isinstance(g, dict) and isinstance(g.get("nodes"), list):
                        if f"{slug}:ontology" not in node_ids(g):
                            graphs_changed += 1
                    else:
                        skipped_custom += 1
                except Exception:
                    skipped_custom += 1
        if evals_path.exists():
            if args.apply:
                if enrich_evals(evals_path):
                    evals_changed += 1
            else:
                try:
                    d = json.loads(evals_path.read_text(encoding="utf-8"))
                    if isinstance(d, dict) and isinstance(d.get("cases"), list):
                        have = {str(c.get("id")) for c in d["cases"] if isinstance(c, dict)}
                        if any(cid not in have for cid in CANONICAL_CASES):
                            evals_changed += 1
                except Exception:
                    pass

    mode = "applied" if args.apply else "dry-run"
    print(f"{mode}: scanned={scanned} graphs_changed={graphs_changed} "
          f"evals_changed={evals_changed} skipped_custom_graphs={skipped_custom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
