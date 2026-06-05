# Constitution Compliance Meta Prompt

Decide whether `constitution-compliance` should activate for the current user
request and define the safe audit scope. [EXPLICIT]

## Activation Check

- Activate when the request mentions JM-ADK Constitution, Pristino governance,
  constitutional audit, G0-G3 gates, evidence-tag compliance, or pre-delivery
  Constitution validation.
- Do not activate for generic legal/political constitution questions.
- Do not activate for creating an agent constitution; route to
  `agent-constitution-creator`.
- If the user asks to edit the Constitution source text, route to the
  Constitution management workflow instead of auditing an artifact.

## Scope Check

- One artifact per report unless the user explicitly asks for a portfolio
  summary.
- Read-only audit by default.
- Missing artifact or missing gate evidence means `not_verified`.
- Use v6.0.0 as the target and treat stale version references as findings.
