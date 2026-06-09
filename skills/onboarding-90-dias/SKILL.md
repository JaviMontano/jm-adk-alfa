---
name: onboarding-90-dias
version: 0.2.0
description: "Genera y valida planes 30/60/90 para nuevos roles con evidencia, hitos verificables, limites anti-burnout, prioridades acotadas y sin promesas de desempeno no sustentadas."
owner: "JM Labs"
triggers:
  - onboarding-90-dias
  - plan-30-60-90
  - onboarding
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Onboarding 90 Dias

## Purpose

Use this skill to design a sustainable 30/60/90 onboarding plan for a new role, engagement, or internal transition. The skill converts supplied role evidence into phase-specific priorities, measurable deliverables, learning goals, stakeholder actions, and validation checkpoints while enforcing anti-burnout limits.

## Inputs Expected

- Role title, organization or team context, and source evidence for the role expectations.
- User constraints: weekly hours, energy boundaries, non-negotiables, relocation or parallel-stream constraints.
- Stakeholder map or known onboarding contacts.
- Phase priorities for days 1-30, 31-60, and 61-90.
- Desired output: plan, audit, overload report, stakeholder handoff, or validation packet.

## Outputs Expected

- A 30/60/90 plan with exactly three phases.
- At most four priorities per phase and a sustainable weekly-hour estimate.
- Each priority has a deliverable, validation signal, and evidence reference.
- Burnout, always-on, vague promise, missing evidence, and unverifiable task findings.
- Validation command evidence when a JSON packet is supplied.

## Procedure

### Discover

Identify role context, constraints, stakeholders, available evidence, and the user's preferred planning granularity. If role expectations or weekly capacity are missing, block confident planning and request them.

### Analyze

Apply `assets/phase-contract.json`, `assets/burnout-policy.json`, `assets/evidence-policy.json`, `assets/validation-policy.json`, and `assets/output-contract.json`. Treat dates, performance guarantees, stakeholder availability, and organizational priorities as unsupported unless supplied.

### Execute

Build the plan phase by phase:

- Days 1-30: learn, listen, map systems, and ship one small trust-building artifact.
- Days 31-60: contribute to prioritized work, reduce ambiguity, and validate working agreements.
- Days 61-90: own a bounded improvement, document learnings, and propose next operating cadence.

Keep each phase small enough to execute sustainably. Replace always-on language with explicit recovery boundaries.

### Validate

Run the deterministic fixture suite:

```bash
bash skills/onboarding-90-dias/scripts/check.sh
```

For one plan packet:

```bash
python3 skills/onboarding-90-dias/scripts/plan_30_60_90.py --input <packet.json>
```

## Assets

- `assets/phase-contract.json`
- `assets/burnout-policy.json`
- `assets/evidence-policy.json`
- `assets/validation-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- The plan contains phases 30, 60, and 90 exactly once.
- No phase has more than four priorities; three or fewer is preferred.
- Weekly hours are at or below 45 and include recovery boundaries.
- Every priority has evidence, a deliverable, and a validation signal.
- Vague goals like "be strategic" are converted into observable behavior.
- Performance outcomes are framed as intended contributions, not guaranteed results.
- Missing role evidence produces a blocked or partial plan, not invented priorities.

## Edge Cases

- Empty role: block and request the role context.
- Weekly hours above 45: flag overload and return nonzero validation.
- More than four priorities in one phase: flag overload and return nonzero validation.
- Missing phase: block readiness.
- Always-on or hustle language: block and rewrite with sustainable cadence.
- No stakeholders: ask for known contacts or mark stakeholder map as open.
- User asks for guaranteed promotion or impact: reframe as measurable contribution.

## Assumptions and Limits

- This skill supports planning and onboarding; it does not guarantee role success, promotion, compensation, visa, legal, HR, or health outcomes.
- It does not read calendars, fetch company systems, or infer hidden organizational priorities.
- Time estimates are planning inputs supplied by the user, not live workload telemetry.

## Scripts

`scripts/plan_30_60_90.py --input <json>` validates onboarding packets for phase completeness, priority limits, evidence, deliverables, validation signals, anti-burnout rules, and unsupported promise language. `scripts/check.sh` runs valid, blocked, and invalid fixtures offline.

## Related Skills

- `negociacion-oferta`
- `red-y-referencias`
- `proceso-seleccion-orchestrator`

## Evidence Requirements

- Tie role expectations, stakeholder commitments, deliverables, and validation signals to supplied evidence.
- Mark missing evidence, stakeholder uncertainty, and capacity assumptions as open questions.
- Report validation commands and results when a machine-readable packet is used.

## Update-Safety Notes

- Keep validation offline and deterministic.
- Do not add calendar, HR system, or network calls.
- Do not modify other skills while hardening this one.
