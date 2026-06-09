---
name: notebook-curator-seleccion
version: 0.2.0
description: "Cura notebooks SEL-EMPRESA para procesos de seleccion con slots canonicos, evidencia offline, deduplicacion y bloqueo de claims no leidos o dependencias de red."
owner: "JM Labs"
triggers:
  - notebook-curator
  - sel-empresa
  - curar-notebook
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Notebook Curator Seleccion

## Purpose

Use this skill to curate a selection-process notebook archetype named `SEL-EMPRESA`. The skill verifies that the notebook has canonical source slots, each source is grounded in supplied evidence, and any missing source is explicitly marked as a blocker or open question. It never assumes NotebookLM, live URLs, or external retrieval succeeded.

## Inputs Expected

- Company or process identifier for the notebook.
- Offline source inventory exported or supplied by the user.
- Canonical slot mapping for role, company, process, interviews, preparation, offer, gratitude, and retrospective.
- Deduplication or rename requests.
- Output preference: readiness audit, missing-source checklist, curation plan, or handoff packet.

## Outputs Expected

- `SEL-EMPRESA` readiness status: complete, partial, or blocked.
- Canonical source-slot table with evidence refs.
- Missing or duplicate slot findings.
- Curation actions that are safe and deterministic.
- Open questions and validation command evidence when a JSON packet is supplied.

## Procedure

### Discover

Identify the target company/process, the notebook identifier, and the source inventory. If the user only names a company, request the exported source list before claiming readiness.

### Analyze

Apply `assets/source-slot-contract.json`, `assets/evidence-policy.json`, `assets/curation-policy.json`, and `assets/offline-boundary-policy.json`. Do not infer source contents from file names alone; names can help classify a slot but cannot support claims.

### Execute

Produce the readiness table and curation plan. Mark missing slots as blockers, duplicate slots as cleanup actions, and extra sources as optional only when they do not replace a canonical slot. Keep all actions additive unless the user explicitly authorizes edits.

### Validate

Run the deterministic fixture suite:

```bash
bash skills/notebook-curator-seleccion/scripts/check.sh
```

For one notebook packet:

```bash
python3 skills/notebook-curator-seleccion/scripts/validate_archetype.py --input <packet.json>
```

To print the canonical slots:

```bash
python3 skills/notebook-curator-seleccion/scripts/validate_archetype.py --emit
```

## Assets

- `assets/source-slot-contract.json`
- `assets/evidence-policy.json`
- `assets/curation-policy.json`
- `assets/offline-boundary-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- Every canonical slot is present exactly once or is reported missing.
- Every present source includes a title, evidence type, and evidence detail.
- Curation actions use allowed deterministic operations only.
- Network, NotebookLM, browser, or live-sync requirements are blocked unless the user separately authorizes that workflow outside this offline validator.
- Claims about source contents require supplied excerpts or notes, not just source names.

## Edge Cases

- Empty inventory: block and request exported sources.
- Duplicate slot: block readiness and propose a dedupe action.
- Extra source: keep it optional; do not count it as a canonical slot.
- URL-only source requiring fetch: block as network-dependent.
- NotebookLM mentioned without export: ask for exported source list.
- User requests "assume it is complete": refuse and validate actual slots.

## Assumptions and Limits

- This skill validates notebook curation state, not the truth of interview, company, or offer claims.
- It does not call NotebookLM, browse URLs, or sync external systems.
- It can prepare a handoff packet for a later NotebookLM workflow, but that workflow is outside this deterministic check.

## Scripts

`scripts/validate_archetype.py --input <json>` validates `SEL-EMPRESA` packets for canonical slots, evidence, duplicates, offline boundaries, and curation actions. `scripts/check.sh` runs valid, blocked, and invalid fixtures offline.

## Related Skills

- `proceso-seleccion-orchestrator`
- `simulador-entrevista`
- `gratitud-post-proceso`
- `negociacion-oferta`

## Evidence Requirements

- Tie slot readiness to supplied source inventory.
- Tie claims about source content to supplied excerpts, notes, or metadata.
- Mark absent sources and live-sync dependencies as blockers.

## Update-Safety Notes

- Do not edit notebooks or external systems by default.
- Do not add network checks, wall-clock timestamps, random IDs, or hidden NotebookLM calls to validation.
- Do not touch other skills while hardening this one.
