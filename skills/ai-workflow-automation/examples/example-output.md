<!--
generated-by: scripts/scaffold-skill.py
generated-for: ai-workflow-automation
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The support triage automation is safe to pilot as a gated workflow: AI performs
classification and drafting, while human approval is required for P0 escalation
and outbound replies. [CONFIG][INFERENCIA]

## Actors

| actor | role | evidence |
|-------|------|----------|
| AI classifier | Classify severity and route draft | `tickets/inbound/*.json` [CONFIG] |
| Support lead | Approve P0 escalation and outbound response | `docs/support/escalation-policy.md` [DOC] |
| Ticket system | Stores draft and approval status | `tickets/inbound/*.json` [CONFIG] |

## Step Graph

| id | actor | action | output | approval | retry | fallback |
|----|-------|--------|--------|----------|-------|----------|
| S1 | system | Load ticket JSON and policy references | normalized intake | no | 0 | block on invalid JSON |
| S2 | ai | Classify severity using policy excerpts | severity label with rationale | no | 1 | hand off to support lead |
| S3 | ai | Draft response using approved template | response draft | yes | 1 | no outbound message |
| S4 | human | Approve P0 escalation or response | approval decision | yes | 0 | manual triage |

## Approval Gates

- G1 before S3/S4: Support lead approves P0 escalation and every outbound
  customer response with decision values `approved`, `rejected`, or `needs-info`.
  [DOC][CONFIG]

## Handoffs

- H1 transfers failed classification packets from AI classifier to Support lead
  with ticket id, source message, policy excerpt, attempted label, and failure
  reason. [CONFIG]

## Validation

- AI steps include input refs, output contract, deterministic check, retry limit,
  and fallback. [CONFIG]
- High-risk outbound response is gated by human approval before execution.
  [DOC][CONFIG]
- Remaining risk: classifier quality still needs a labeled-ticket regression set
  before production rollout. [INFERENCIA]
