---
name: gratitud-post-proceso
version: 0.2.0
description: "Redacta agradecimientos post-proceso diferenciados por persona, evidencia de interaccion, voz de marca y lint offline contra FOMO, hustle, servilismo y promesas no verificables."
owner: "JM Labs"
triggers:
  - gratitud-post-proceso
  - agradecimiento
  - thank-you
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Gratitud Post Proceso

## Purpose

Use this skill after an interview, selection process, workshop, review panel, or professional conversation when the user needs a thank-you note that is specific, grounded in supplied evidence, and safe to send. The skill produces differentiated messages per recipient, preserves factual boundaries, and validates tone with `scripts/lint_gratitud.py`.

## Inputs Expected

- Process or meeting context.
- Recipient name, role, and relationship to the process.
- Evidence from the interaction: topics discussed, contribution, decision stage, or next step.
- Channel constraints: email, LinkedIn, WhatsApp, note, or internal message.
- Brand voice constraints and any promises that must not be made.

## Outputs Expected

- One message per recipient or persona.
- Recipient-specific evidence line.
- Subject or opening line when the channel needs it.
- Tone and risk notes for FOMO, hustle, servility, overpromising, or invented process details.
- Validation command evidence when a JSON packet is provided.

## Procedure

### Discover

Identify the process stage, channel, recipient, relationship, evidence from the interaction, and whether the user wants a message draft or a reusable template.

### Analyze

Apply `assets/recipient-differentiation-policy.json`, `assets/evidence-policy.json`, `assets/brand-voice-policy.json`, and `assets/promise-boundary-policy.json` before drafting.

### Execute

Write concise gratitude that names a real contribution, avoids pressure, and states next steps only when the user supplied them. Do not invent interview details, relationship warmth, availability, outcomes, or deadlines.

### Validate

Run the deterministic fixture suite:

```bash
bash skills/gratitud-post-proceso/scripts/check.sh
```

For a specific packet:

```bash
python3 skills/gratitud-post-proceso/scripts/lint_gratitud.py --input <packet.json>
```

## Assets

- `assets/recipient-differentiation-policy.json`
- `assets/evidence-policy.json`
- `assets/brand-voice-policy.json`
- `assets/promise-boundary-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- Each message has a named recipient or explicit recipient archetype.
- Each message includes at least one interaction-specific evidence detail.
- Tone is grateful, concrete, and calm; it avoids servility, pressure, and performative urgency.
- Brand phrases are not stacked; at most one distinctive phrase is allowed per message.
- Follow-up or availability statements are conditional on user-provided facts.
- Missing process evidence produces a partial or blocked output instead of invented detail.

## Edge Cases

- No recipient: produce a blocked checklist and ask for the target person or persona.
- No interaction evidence: provide a generic-safe template and mark missing evidence.
- Multiple recipients: differentiate by role and contribution, not by flattery intensity.
- User asks to pressure the recipient: remove FOMO and state a neutral follow-up.
- User asks to apologize excessively: rewrite to gratitude without servility.
- User asks to imply acceptance, offer, or commitment: block unless supplied as fact.

## Assumptions and Limits

- The skill improves professional communication; it does not guarantee process outcomes.
- If evidence is unavailable, mark the message as template-only or ask for context.
- Do not include private contact details in examples or fixtures.

## Scripts

`scripts/lint_gratitud.py --input <json>` validates gratitude packets for recipient specificity, interaction evidence, tone blockers, promise boundaries, and output sections. It also accepts plain text for ad hoc tone linting. `scripts/check.sh` runs deterministic valid and invalid fixtures offline.

## Related Skills

- `proceso-seleccion-orchestrator`
- `negociacion-oferta`

## Evidence Requirements

- Tie every specific thanks, topic, next step, or process claim to user-provided evidence.
- Mark missing evidence as a blocker or assumption.
- Report validation commands and results when a machine-readable packet is used.

## Update-Safety Notes

- Default to draft text unless the user explicitly asks to edit files.
- Preserve the user's facts, names, and relationships.
- Do not add network checks, wall-clock timestamps, random IDs, or live process-status claims to validation.
