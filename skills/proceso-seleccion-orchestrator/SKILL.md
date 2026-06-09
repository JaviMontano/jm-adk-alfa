---
name: proceso-seleccion-orchestrator
version: 0.2.0
description: "This skill should be used when the user asks to track a hiring or selection process, extract interview stages from supplied notes or emails, reconcile interviewer roles, build a candidate status board, identify the next action, or audit handoff evidence for an active selection workflow."
owner: "JM Labs"
triggers:
  - proceso-seleccion
  - seleccion-orchestrator
  - hiring pipeline
  - interview status board
  - next interview action
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Proceso Seleccion Orchestrator

## Purpose

Orchestrate a supplied hiring or selection-process packet into a deterministic status board. Extract only facts present in the provided messages, notes, interview feedback, or manual entries. Track candidate alias, target role, interviewer contacts, process stages, decision risks, evidence references, and exactly one next action.

Use the skill for process tracking, not for legal, salary, immigration, background-check, or employment-law advice. Do not infer private facts, interview outcomes, compensation, dates, or commitments that are not present in evidence.

## Deterministic Contract

Follow `assets/output-contract.json` for the JSON report shape and `templates/output.md` for the human-readable handoff. Use stable ordering:

1. Sort evidence by `received_date`, then `id`.
2. Sort contacts by normalized `name`, then `role`.
3. Sort stages by explicit `sequence`.
4. Keep risk order by severity rank from `assets/risk-policy.json`, then `id`.

All dates must be ISO `YYYY-MM-DD`. If the user provides relative dates such as "tomorrow", "next Tuesday", or "ayer", preserve the text in notes and set a blocker instead of normalizing from the current clock. Do not call calendars, email, web, or network services unless the user separately provides that data in the prompt or workspace.

## Required Inputs

- Candidate alias or anonymized identifier.
- Target role or opportunity.
- At least one evidence item from supplied email text, meeting notes, recruiter messages, interview feedback, or manual entry.
- Known stages or enough evidence to derive stages.

When inputs are incomplete, return a blocked report with missing fields. Do not fabricate placeholders such as `TBD` as if they were evidence.

## Workflow

1. Inventory all supplied evidence. Assign stable IDs such as `E-001`, `E-002`, and record source type using `assets/evidence-policy.json`.
2. Extract contacts only when a name and role/title are present in the supplied evidence. Preserve original names in display text, but use deterministic ASCII normalization only for sorting.
3. Build stages using `assets/status-policy.json`. Each stage needs `id`, `sequence`, `label`, `owner`, `status`, `status_reason`, and `evidence_ref`.
4. Select exactly one next action. It must point to one existing stage and one existing evidence item.
5. Add risks only when evidence supports them. Use the allowed severities and require mitigation text.
6. Validate the JSON report with `scripts/selection_board_validator.py`.
7. Produce the markdown handoff from `templates/output.md`, including validation status and remaining risks.

## Output Rules

- Tag claims with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- Use `blocked` when evidence is missing, dates are relative, outcomes are promised, or stage status is contradictory.
- Never claim a candidate is hired, rejected, selected, or guaranteed unless the provided evidence explicitly says so.
- Never use the current date to resolve deadlines.
- Never expose raw email bodies in the final board; cite evidence IDs and short summaries.

## Assets

- `assets/manifest.json` lists every deterministic asset.
- `assets/output-contract.json` defines the required report structure.
- `assets/status-policy.json` defines allowed stage statuses and terminal states.
- `assets/evidence-policy.json` defines allowed evidence types and minimum fields.
- `assets/date-policy.json` defines ISO-only date handling and relative-date blockers.
- `assets/risk-policy.json` defines severity ranks and mitigation requirements.

## Scripts

Run local validation before using a report as evidence:

```bash
python3 skills/proceso-seleccion-orchestrator/scripts/selection_board_validator.py --input <report.json>
bash skills/proceso-seleccion-orchestrator/scripts/check.sh
```

The validator is offline, deterministic, and rejects missing evidence, duplicate stages, unsupported statuses, relative dates, guaranteed-outcome language, unresolved evidence references, and missing next actions.

## Related Skills

- `simulador-entrevista`
- `gratitud-post-proceso`
- `red-y-referencias`

## Stop Conditions

Stop and ask for missing source data when the request requires accessing private mailboxes, live calendars, applicant tracking systems, or external profiles not supplied in the workspace. Stop when a requested change would require employment-law advice or direct modification of another skill.
