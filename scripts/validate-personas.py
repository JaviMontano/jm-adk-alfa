#!/usr/bin/env python3
"""validate-personas.py v1.0.0 — schema gate for references/ontology/personas.json

Checks (deterministic, exit 0 = pass, 1 = fail):
  - file parses as JSON
  - every persona has unique non-empty id and label
  - exactly one persona has default: true
  - every persona has at least one trigger and an integer priority
  - every capability_agents entry references an existing agents/<name>.md
  - modes block present with bypass/soloPrompt/soloRespuesta keys

Usage: python3 scripts/validate-personas.py [--json]
"""
import json, os, sys, subprocess

def root():
    try:
        return subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                       text=True).strip()
    except Exception:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    as_json = "--json" in sys.argv
    R = root()
    reg_path = os.path.join(R, "references", "ontology", "personas.json")
    errors, warnings = [], []

    if not os.path.isfile(reg_path):
        errors.append(f"missing registry: {reg_path}")
        return report(errors, warnings, 0, as_json)

    try:
        reg = json.load(open(reg_path, encoding="utf-8"))
    except Exception as e:
        errors.append(f"JSON parse error: {e}")
        return report(errors, warnings, 0, as_json)

    personas = reg.get("personas", [])
    if not personas:
        errors.append("no personas defined")

    ids, labels, defaults = set(), set(), 0
    agents_dir = os.path.join(R, "agents")
    for i, p in enumerate(personas):
        pid = p.get("id", "")
        label = p.get("label", "")
        where = pid or f"index {i}"
        if not pid:
            errors.append(f"persona {where}: missing id")
        elif pid in ids:
            errors.append(f"persona {where}: duplicate id")
        ids.add(pid)
        if not label:
            errors.append(f"persona {where}: missing label")
        elif label in labels:
            errors.append(f"persona {where}: duplicate label")
        labels.add(label)
        if p.get("default") is True:
            defaults += 1
        if not p.get("triggers"):
            errors.append(f"persona {where}: empty triggers")
        if not isinstance(p.get("priority"), int):
            errors.append(f"persona {where}: priority must be int")
        for a in p.get("capability_agents", []):
            if not os.path.isfile(os.path.join(agents_dir, f"{a}.md")):
                errors.append(f"persona {where}: capability_agent '{a}' has no agents/{a}.md")

    if defaults != 1:
        errors.append(f"exactly one default persona required, found {defaults}")

    modes = reg.get("modes", {})
    for k in ("bypass", "soloPrompt", "soloRespuesta"):
        if k not in modes:
            errors.append(f"modes: missing key '{k}'")

    return report(errors, warnings, len(personas), as_json)

def report(errors, warnings, count, as_json):
    if as_json:
        print(json.dumps({"personas": count, "errors": errors, "warnings": warnings}, indent=2))
    else:
        print(f"personas={count} warnings={len(warnings)} errors={len(errors)}")
        for e in errors:
            print(f"ERROR: {e}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
