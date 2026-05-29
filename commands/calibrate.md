---
description: "Inspect or force Pristino persona auto-calibration: show the deterministic persona/mode/optimizer signals for a prompt and run the calibration contract."
user-invocable: true
---

# /jm-adk:calibrate

## Purpose

Surface and exercise the deterministic persona model. The `persona-calibrate.sh` UserPromptSubmit hook runs automatically on every prompt; this command lets you inspect what it decided, or force a calibrated answer on demand.

## Workflow

1. Run `CLAUDE_USER_PROMPT="<text>" bash scripts/persona-calibrate.sh` to print the `PRISTINO-CALIBRATION:` block (persona, confidence, mode, complexity, optimizer, delegate).
2. Execute the `pristino-calibration` skill contract against that block: persona label on line 1, mode/optimizer-shaped response, precedence Veracidad>Seguridad>Objetivo>Formato>Estilo, evidence tags, declared confidence.
3. If `LOW-CONFIDENCE` is present, ask ≤2 clarifying questions first.

## Modes

- `!<text>` — bypass: plain answer, no persona ceremony.
- `MODO: SOLO_PROMPT <text>` — emit only the optimized prompt.
- `MODO: SOLO_RESPUESTA <text>` — emit only the response.

## Agents And Skills

- Skill: `pristino-calibration`
- Registry: `references/ontology/personas.json`
- Spec: `references/ontology/persona-protocol.md`
- Validator: `python3 scripts/validate-personas.py`

## Examples

- `/jm-adk:calibrate diseña la arquitectura de un sistema de colas` → persona `Arquitecto de Software`, 3 sections.
- `/jm-adk:calibrate !ping` → bypass, plain answer.
