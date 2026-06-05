---
name: constitution-compliance
author: JM Labs (Javier Montano)
version: 1.0.1
description: Validates outputs, plans, PRs, reports, or workflows against JM-ADK Constitution v6.0.0 using an 18-principle matrix, G0-G3 gate impact, evidence tags, severity, remediation, and fail-closed missing-evidence handling. Use when the user asks for constitution compliance, constitutional audit, Pristino governance validation, pre-delivery compliance, or whether an artifact violates JM-ADK principles.
argument-hint: "artifact-path | artifact-json | --gate G0|G1|G2|G3"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
model: opus
context: fork
---

# Constitution Compliance

Validate an artifact against JM-ADK Constitution v6.0.0. A valid compliance
report covers all 18 principles, maps findings to G0-G3 gates, classifies
severity, requires remediation for every failure, and treats missing evidence as
`not_verified` rather than a pass. [EXPLICIT]

## Deterministic Assets

Use these local assets before producing a report. [EXPLICIT]

| Path | Use |
|---|---|
| `assets/constitution-v6-principles.json` | Canonical 18-principle map and G0-G3 gates derived from `references/ontology/constitution-v6.0.0.md` |
| `assets/compliance-report-contract.json` | Required report sections, status values, evidence tags, and blocked phrases |
| `assets/severity-policy.json` | Severity mapping for P0, P1, P2, P3 findings and gate impact |
| `assets/activation-policy.json` | Activation, false-positive, version-drift, and missing-evidence rules |
| `scripts/validate_constitution_report.py` | Offline JSON compliance report validator |
| `scripts/check.sh` | Deterministic positive and negative fixture check |

The validator reads only explicit local JSON files. It does not call the
network, current time, model providers, MCP tools, or random sources. [EXPLICIT]

## When To Activate

Activate for constitutional audits, pre-delivery checks, Pristino governance
validation, gate compliance, evidence-tag checks, or requests asking whether an
artifact violates the JM-ADK Constitution. [EXPLICIT]

Do not activate for:

- viewing or amending the Constitution itself; route to `/jm-adk:constitution`
- creating an agent constitution; route to `agent-constitution-creator`
- generic legal or political constitution questions
- generic quality review without JM-ADK/Pristino governance scope

## Required Inputs

At least one input must be explicit: [EXPLICIT]

| Input | Rule |
|---|---|
| `artifact` | Text, path, PR summary, report, workflow, plan, or implementation output to audit |
| `gate` | Optional `G0`, `G1`, `G2`, or `G3`; if absent, infer from artifact type and mark inference |
| `evidence_sources` | Files, command outputs, review docs, or stated missing evidence |
| `claim_tag_policy` | Use repo tags `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`, `[ASSUMPTION]`; Spanish tags may be used in user-facing summaries |

If the artifact or evidence sources are missing, return `not_verified` findings
and ask for the missing input. Never mark a principle `pass` from silence.
[EXPLICIT]

## Compliance Process

1. Confirm the target Constitution version is v6.0.0. If the artifact cites
   v5.2.0, classify as version drift and use the v6 cross-reference. [EXPLICIT]
2. Load `assets/constitution-v6-principles.json`,
   `assets/compliance-report-contract.json`, and `assets/severity-policy.json`.
3. Inspect the artifact and evidence sources. Cite file paths, command output,
   or explicit user-provided statements.
4. Produce one matrix row per principle, with status
   `pass|fail|not_verified|not_applicable`.
5. For every `fail`, include severity, gate impact, evidence, and remediation.
6. For every `not_verified`, list the missing evidence and the next command,
   file, or decision needed.
7. Block delivery when any P0/P1 failure exists or when a required gate has
   `not_verified` evidence.
8. If a JSON report is available, run `scripts/validate_constitution_report.py`
   before final delivery.

## Report Contract

Every report must include: [EXPLICIT]

1. Constitution version: `v6.0.0`.
2. Artifact description and audit gate.
3. Overall status: `pass`, `blocked`, or `not_verified`.
4. Matrix with all 18 principles.
5. G0-G3 gate impact.
6. Violations table.
7. Missing evidence table.
8. Remediation plan.
9. Decision and confidence.
10. Explicit caveats.

## Validation Gate

- [ ] Constitution version is `v6.0.0`.
- [ ] All 18 principles are represented exactly once.
- [ ] Every principle row has status, evidence, severity, remediation, and gate
  impact.
- [ ] Any `fail` row has non-empty remediation.
- [ ] Any `not_verified` row names missing evidence.
- [ ] Overall status is `blocked` when any P0/P1 failure is present.
- [ ] Overall status is not `pass` when required evidence is missing.
- [ ] G0-G3 impact is explicit.
- [ ] Evidence tags appear on factual claims.
- [ ] No stale `v5.2.0` target remains except as a version-drift finding.

## Severity Policy

| Severity | Meaning | Delivery Decision |
|---|---|---|
| `P0` | Security, secret, data integrity, or hard constitutional breach | Block |
| `P1` | Gate-blocking missing evidence, stale version, broken process, or false pass | Block |
| `P2` | Important compliance gap with bounded workaround | Conditional |
| `P3` | Low-risk documentation or wording gap | Warn |
| `none` | Principle passes or does not apply | Allow |

## Edge Cases

- **Artifact cites v5.2.0:** audit against v6.0.0 and include a version-drift
  violation.
- **Missing artifact:** return `not_verified`, not `pass`.
- **Conflicting requirements:** map each conflict to the affected principles and
  require an owner decision.
- **Non-JM-ADK constitution question:** decline this skill and answer with a
  generic or legal/compliance skill as appropriate.
- **Partial evidence:** mark only evidenced principles as `pass`; remaining
  principles are `not_verified`.

## Reference Files

| File | Content | Load When |
|---|---|---|
| `references/ontology/constitution-v6.0.0.md` | Canonical Constitution v6.0.0 text and cross-reference to v5.2.0 | When verifying source text or crosswalk |
| `assets/constitution-v6-principles.json` | Machine-readable principle and gate map | Always |
| `assets/compliance-report-contract.json` | Report schema and blocked phrases | Always |
| `assets/severity-policy.json` | Severity and delivery policy | Always |
| `scripts/check.sh` | Fixture-backed deterministic check | When local scripts can run |

---
**Author:** Javier Montano | **Last updated:** 2026-06-05
