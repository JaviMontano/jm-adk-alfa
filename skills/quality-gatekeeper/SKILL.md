---
name: quality-gatekeeper
description: Validates deliverables at JM-ADK quality gates G0-G3 using deterministic criteria, evidence tags, sequential gate order, score-history entry contracts, remediation, and fail-closed missing-evidence handling. Use before phase transitions, release decisions, `/jm:advance`, PR readiness, or any request asking whether a gate can pass.
version: 1.0.1
status: production
owner: Javier Montaño
tags: [core, quality, gates, validation]
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Quality Gatekeeper

Validate one artifact or release packet against JM-ADK G0-G3 quality gates. A
valid gate report evaluates every required criterion for the scoped gate(s),
uses evidence tags, blocks on failures or missing evidence, and emits a
score-history entry contract without mutating project state unless an
orchestrator explicitly requests a write. [EXPLICIT]

## Deterministic Assets

Use these local assets before producing or validating a report. [EXPLICIT]

| Path | Use |
|---|---|
| `assets/gate-criteria.json` | Canonical G0-G3 criteria, required evidence, and phase order |
| `assets/report-contract.json` | Required report sections, statuses, severities, and decision rules |
| `assets/evidence-policy.json` | Evidence tag vocabulary and assumption-ratio warning policy |
| `assets/score-history-schema.json` | Required score-history entry fields |
| `assets/activation-policy.json` | Activation and false-positive routing rules |
| `scripts/validate_gate_report.py` | Offline JSON gate report validator |
| `scripts/check.sh` | Deterministic fixture check for pass, block, and false-pass cases |

The validator reads only explicit local JSON paths. It does not call the
network, current time, model providers, MCP tools, or random sources. [EXPLICIT]

## When To Activate

Activate for JM-ADK quality gate decisions, phase transitions, `/jm:advance`,
release readiness, PR gate readiness, score-history entry validation, or
requests asking whether G0, G1, G2, or G3 can pass. [EXPLICIT]

Do not activate for:

- generic writing quality review without JM-ADK gate scope
- generic CI log explanation unless the user asks for a G0-G3 decision
- Lighthouse-only audits; route to performance/accessibility skills unless tied
  to G3
- creating or editing the Constitution; route to constitution workflows
- human role assignment such as "find a gatekeeper"

## Required Inputs

At least one artifact or explicit missing-evidence statement is required.
[EXPLICIT]

| Input | Rule |
|---|---|
| `gate_id` | `G0`, `G1`, `G2`, `G3`, or a scoped list; if absent, infer from artifact type and mark inference |
| `source_stage` | Current phase before transition; used to enforce sequential gate order |
| `target_stage` | Requested phase after gate approval |
| `artifacts` | Files, PR checks, reports, commands, or user-provided evidence |
| `score_history` | Existing entry when re-evaluating; otherwise emit a proposed `score_history_entry` |

If required evidence is absent, mark the criterion `not_verified`. Never mark a
criterion `pass` from silence. [EXPLICIT]

## Gate Process

1. Load `assets/gate-criteria.json`, `assets/report-contract.json`,
   `assets/evidence-policy.json`, and `assets/score-history-schema.json`.
2. Identify the requested gate(s) and enforce order `G0 -> G1 -> G2 -> G3`.
3. Evaluate every required criterion for each scoped gate.
4. Require evidence tags on every factual criterion row.
5. Classify criterion status as `pass`, `fail`, `not_verified`, or
   `not_applicable`.
6. Block advancement when any required criterion is `fail` or `not_verified`.
7. Add remediation for every `fail` or `not_verified` criterion.
8. Emit a score-history entry contract with gate, branch/commit when available,
   evidence summary, blocked flag, decision, and evaluator.
9. If a JSON report is available, run `scripts/validate_gate_report.py` before
   final delivery.

## Gate Criteria Summary

| Gate | Required Criteria | Pass Condition |
|---|---|---|
| G0 Pre-flight | secrets scan, branch isolation, Constitution compliance | zero blocking findings |
| G1 Analysis | spec complete, evidence tags, stakeholder/checklist coverage | all analysis artifacts evidenced |
| G2 Architecture | data model, API/contracts, security rules, BDD traceability, design tokens | architecture evidence complete |
| G3 Deploy-ready | tests, Lighthouse >= 90, emulator/security checks, accessibility audit, brand voice/monitoring | all release checks green |

Use `assets/gate-criteria.json` as the canonical criterion list. [EXPLICIT]

## Report Contract

Every report must include: [EXPLICIT]

1. Summary with `gate_scope`, `source_stage`, `target_stage`,
   `overall_status`, `blocking_findings`, `not_verified_count`,
   `assumption_ratio`, and confidence.
2. Gate results for all scoped gates.
3. Criterion results for every required criterion in scoped gates.
4. Violations table.
5. Missing evidence table.
6. Remediation plan.
7. Proposed `score_history_entry`.
8. Decision: `allow`, `block`, or `needs_evidence`.
9. Caveats and explicit assumptions.

## Validation Gate

- [ ] Gate scope is explicit.
- [ ] Sequential gate order is checked.
- [ ] Every required criterion for scoped gates is represented exactly once.
- [ ] Every `pass` row has tagged evidence.
- [ ] Every `fail` row has severity and remediation.
- [ ] Every `not_verified` row lists missing evidence and remediation.
- [ ] Overall status is `blocked` when required criteria fail or are missing.
- [ ] Assumption ratio above 0.30 emits a warning banner.
- [ ] Score-history entry includes required fields.
- [ ] No external network, clock, or random value is needed to validate the
  report.

## Severity Policy

| Severity | Meaning | Delivery Decision |
|---|---|---|
| `P0` | Secret, security, data integrity, or forbidden stack breach | Block |
| `P1` | Required gate criterion failed, missing, or out-of-sequence | Block |
| `P2` | Important gap with bounded workaround outside the current gate | Conditional |
| `P3` | Low-risk wording or documentation gap | Warn |
| `none` | Criterion passes or does not apply | Allow |

## Edge Cases

- **G3 requested before G1:** block with sequential gate violation.
- **No files or docs yet:** return `not_verified`, not `pass`.
- **Partial green checks:** block the gate; no "mostly pass" language.
- **Assumption-heavy report:** if more than 30% of criterion evidence is
  `[ASSUMPTION]`, add a warning banner and avoid `allow`.
- **Score-history file absent:** emit a valid proposed entry; do not invent that
  it was written.
- **Explicit write request:** only update `.specify/score-history.json` after
  the user/orchestrator permits writes and a valid report exists.

## Reference Files

| File | Content | Load When |
|---|---|---|
| `assets/gate-criteria.json` | G0-G3 criteria and sequence | Always |
| `assets/report-contract.json` | Report schema and decision rules | Always |
| `assets/evidence-policy.json` | Evidence tags and warning thresholds | Always |
| `assets/score-history-schema.json` | Score-history entry requirements | When emitting score history |
| `scripts/check.sh` | Fixture-backed deterministic check | When local scripts can run |

---
**Author:** Javier Montano | **Last updated:** 2026-06-05
