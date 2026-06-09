# Gratitud Post Proceso Primary Prompt

## Objective

Draft recipient-specific post-process gratitude that is concrete, evidence-backed, and safe to send.

## Required Inputs

- Recipient name or role.
- Process context and channel.
- Interaction evidence: topic discussed, contribution, advice, or next step.
- Tone constraints and forbidden claims.

## Process

1. Identify recipient, process, channel, and evidence.
2. Apply the assets policies for differentiation, evidence, tone, and promises.
3. Draft concise gratitude with only supplied facts.
4. Validate a JSON packet with `scripts/lint_gratitud.py` when available.
5. Report validation and risks.

## Output

Return message drafts plus evidence, validation status, and remaining risks.
