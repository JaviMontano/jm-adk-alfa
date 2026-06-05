# Quality Gate Report

## Summary

| Field | Value |
|---|---|
| Gate scope | G3 |
| Source stage | G1-passed |
| Target stage | deploy-ready |
| Overall status | blocked |
| Blocking findings | 2 |
| Not verified | 1 |
| Assumption ratio | 0.40 |
| Confidence | 0.67 |

## Warning

[CONFIG] Assumption-tagged evidence exceeds 30%; clarify before release.

## Gate Results

| Gate | Status | Blocking | Evidence |
|---|---|---:|---|
| G3 | blocked | true | [CODE] G2 is missing, Lighthouse is below 90, and security output is absent. |

## Criteria Results

| Gate | Criterion | Status | Severity | Evidence | Remediation |
|---|---|---|---|---|---|
| G3 | tests_pass | pass | none | [CODE] Unit and E2E tests passed. | none |
| G3 | lighthouse_at_least_90 | fail | P1 | [CODE] Lighthouse score is 84, below the required 90. | Improve performance and rerun Lighthouse until score is at least 90. |
| G3 | security_or_emulator_clean | not_verified | P0 | [ASSUMPTION] Security was reported verbally without command output. | Run security/emulator checks and attach output. |
| G3 | accessibility_audit_clean | not_verified | P1 | [DOC] No accessibility report was included. | Run accessibility audit and attach report. |
| G3 | brand_voice_and_monitoring_ready | pass | none | [DOC] Release packet links monitoring and brand voice evidence. | none |

## Missing Evidence

| Criterion | Missing | Next Step |
|---|---|---|
| G2 sequence | G2 pass record | Complete and validate G2 before G3. |
| security_or_emulator_clean | Security or emulator command output | Run checks and attach output. |
| accessibility_audit_clean | Accessibility audit report | Run audit and attach report. |

## Remediation Plan

1. [CONFIG] Complete and record G2.
2. [CONFIG] Improve Lighthouse score to at least 90.
3. [CONFIG] Attach security/emulator output.
4. [CONFIG] Attach accessibility audit output.

## Proposed Score-History Entry

```json
{
  "gate_scope": ["G3"],
  "source_stage": "G1-passed",
  "target_stage": "deploy-ready",
  "overall_status": "blocked",
  "blocked": true,
  "evaluator": "quality-gatekeeper",
  "evidence_summary": "[CODE] G3 blocked by missing G2, Lighthouse score, and missing security/accessibility evidence.",
  "commands": ["quality-gatekeeper validate G3"],
  "decision": "block"
}
```

## Decision

- release_decision: block
- reason: [CODE] Required G3 criteria failed or were not verified.
- next_action: fix findings and rerun G3 after G2 is passed

## Caveats

- [INFERENCE] The decision validates the supplied evidence only; unstated checks
  are not treated as passed.
