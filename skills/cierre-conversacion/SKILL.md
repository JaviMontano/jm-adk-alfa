---
name: cierre-conversacion
version: 0.2.0
description: "Cosecha aprendizajes, valida evidencia y produce un cierre de conversacion reproducible con handoff, riesgos y plan de actualizaciones durables."
owner: "JM Labs"
triggers:
  - cierre-conversacion
  - session-audit
  - cosechar-aprendizajes
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Cierre Conversacion

## Purpose

Use this skill to close a long or explicitly ended conversation without losing useful state. It turns the session into a deterministic closeout packet: what was decided, what changed, what remains open, which learnings are reusable, which validations are real, and which durable updates are only proposed unless authority is explicit.

## Activation

Activate when any of these conditions is true:

- The user explicitly asks for `cierre-conversacion`, `session-audit`, closeout, retrospective, handoff, or learning harvest.
- The conversation is long enough that decisions, risks, or next steps may be lost across sessions.
- A process requires a final packet before merge, handoff, archive, or thread cleanup.

Do not activate for generic filesystem cleanup, unrelated summarization, or requests to erase history without preserving required evidence.

## Inputs Expected

- Current objective and scope.
- Known files, branches, PRs, commands, or artifacts touched.
- Validation results, blockers, and unresolved risks.
- Explicit authority status for tasklog, changelog, memory, or other durable writes.

## Outputs Expected

- Conversation closeout summary with evidence tags.
- Decisions, tasks, learnings, risks, and validation evidence.
- Durable update plan that separates confirmed writes from proposals.
- Next handoff with the safest next action.
- Guardian decision: `pass` when closure evidence is enough, `block` when it is not.

## Procedure

### 1. Detect Closure Mode

Classify the trigger as explicit, threshold-based, or manual audit. If activation is ambiguous, produce a short proposal rather than claiming a completed closeout.

### 2. Harvest Evidence

Collect only observable facts from the conversation, files, commands, PRs, or user-provided context. Tag every claim as `[CÓDIGO]`, `[CONFIG]`, `[DOC]`, `[INFERENCIA]`, `[SUPUESTO]`, or `[POR_CONFIRMAR]`.

### 3. Build Closeout Packet

Fill the required sections in this order:

1. Summary.
2. Decisions.
3. Completed work.
4. Open tasks.
5. Learnings and reusable patterns.
6. Risks and blockers.
7. Validation evidence.
8. Durable update plan.
9. Next handoff.
10. Guardian decision.

### 4. Control Writes

Do not update tasklog, changelog, memory, or skill assets unless the current authority is explicit. When authority is missing, return the proposed update text and mark it `[POR_CONFIRMAR]`.

### 5. Validate

Before declaring pass, ensure no completed task relies only on `[SUPUESTO]` or `[POR_CONFIRMAR]`, every validation claim has command or artifact evidence, and no failed validation is hidden behind a pass decision.

## Quality Criteria

- Closure packet is deterministic and section-complete.
- Evidence tags are present on all non-obvious claims.
- Durable updates are separated from unapproved proposals.
- Open tasks have owners or next actions when known.
- Guardian blocks false completion, contradictory CI/validation evidence, and unrelated local changes.

## Assets

Use `assets/activation-policy.json`, `assets/output-contract.json`, `assets/evidence-policy.json`, `assets/harvest-checklist.json`, and `assets/durable-update-policy.json` as the deterministic source of truth for activation, output shape, evidence tags, harvest checks, and durable update authority.

## Edge Cases

- Empty closeout request: ask for the objective or produce a minimal blocked packet.
- Conflicting evidence: preserve both claims and block green completion until resolved.
- No durable-write authority: output proposed updates only.
- Long conversation with many details: prioritize durable decisions, blockers, and next five actions.
- Merge or deployment claim without evidence: mark `[POR_CONFIRMAR]` and keep Guardian blocked.

## Scripts

Deterministic checks live in `scripts/`. Run:

```bash
bash skills/cierre-conversacion/scripts/check.sh
```

The script validates closeout report fixtures offline and requires invalid fixtures to fail.

## Related Skills

- `session-end-cleanup`
- `tasklog-management`
- `changelog-management`
- `pre-compact-context`

## Evidence Requirements

- `[CÓDIGO]`: local files, commands, PR metadata, CI output, or diff evidence.
- `[CONFIG]`: user instructions, repository policy, or workflow contract.
- `[DOC]`: stable project documentation.
- `[INFERENCIA]`: derived conclusion from evidence.
- `[SUPUESTO]`: unverified assumption.
- `[POR_CONFIRMAR]`: pending user, CI, remote, or external confirmation.

## Update-Safety Notes

- Default mode is report-only.
- Durable writes require explicit authority and must be listed in `durable_update_plan`.
- Never erase unresolved risks or failed validation evidence during closure.
