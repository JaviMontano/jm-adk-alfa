# Code Review Checklist Report

## Scope

- Review type: `{{review_type}}`
- Sources reviewed: `{{sources_reviewed}}`
- Minimum inputs missing: `{{minimum_inputs_missing}}`
- Mode: `{{mode}}`

## Scores

| Domain | Score |
|---|---:|
| security | `{{scores.security}}` |
| performance_firebase | `{{scores.performance_firebase}}` |
| quality_types | `{{scores.quality_types}}` |

## Checklist Results

| ID | Domain | Status | Evidence | Why |
|---|---|---|---|---|
| `{{id}}` | `{{domain}}` | `{{status}}` | `{{source.file}}:{{source.line}} {{evidence_tag}}` | `{{why}}` |

## Findings

| ID | Check | Severity | Evidence | Claim | Remediation |
|---|---|---|---|---|---|
| `{{finding_id}}` | `{{check_id}}` | `{{severity}}` | `{{file}}:{{line}} {{evidence_tag}}` | `{{claim}}` | `{{remediation}}` |

## Missing Evidence

- `{{missing_evidence}}`

## Validation

- Blocking failures: `{{blocking_failures}}`
- Checks run: `{{checks_run}}`
- Not verified: `{{not_verified}}`

## Decision

- Release decision: `{{release_decision}}`
- Reason: `{{reason}}`
- Next action: `{{next_action}}`

## Risks and Limits

- `{{risk_or_limit}}`
