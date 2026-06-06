---
name: discovery-orchestrator
description: This skill should be used when the user asks to "plan discovery", "orchestrate discovery", "run the discovery pipeline", "sequence discovery skills", "manage G1/G2/G3 gates", "resume discovery state", or coordinate phases 0-6 without performing the underlying analysis.
version: 1.0.0
status: production
owner: Javier Montaño
tags: [analysis, orchestrator, pipeline, coordination]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# discovery-orchestrator {Analysis} (v1.0)

Coordinate the discovery pipeline from phase 0 through phase 6. Sequence the canonical discovery skills, enforce the quality gates, expose blocked handoffs, and keep the output evidence-tagged. Do not perform stakeholder analysis, AS-IS analysis, scenario scoring, feasibility analysis, solution design, pricing, proposal writing, or implementation planning inside this skill.

## Activation

Activate for requests that ask to coordinate, sequence, resume, audit, gate, or hand off a discovery pipeline. Activate for explicit phrases such as `discovery-orchestrator`, `plan discovery`, `run completo`, `run intermedio`, `run express`, `manage G1`, `coordinate discovery gates`, or `resume discovery state`.

Do not activate for domain analysis requests that should be handled by a downstream skill, such as stakeholder mapping, AS-IS analysis, flow mapping, scenario analysis, feasibility, roadmap, functional specification, executive pitch, or handover authoring. In those cases, route to the specific skill and keep this skill limited to sequencing and gate governance.

## Core Laws

1. **Evidence law:** Every pipeline claim uses `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`, or `[ASSUMPTION]`.
2. **Boundary law:** Coordinate the work; never create domain findings or implementation steps.
3. **Gate law:** Stop at G1, G2, and G3 until the required evidence is present.
4. **No-price law:** Express planning magnitude as effort ranges such as FTE-months and assumptions; never provide currency, rates, or prices.
5. **Determinism law:** Use stable inputs, explicit dates, deterministic statuses, and the offline contract in `scripts/`.

## Operating Modes

| Mode | Use | Required Output |
|------|-----|-----------------|
| `sequence` | Build or revise the phase/skill order. | Ordered phases, skill sequence, dependencies, gates, blockers. |
| `gate-check` | Decide whether a gate can pass. | Gate evidence, pass/block decision, missing evidence, next action. |
| `dashboard` | Report current discovery state. | Phase status, owners, deliverables, risks, validation state. |
| `handoff-readiness` | Prepare the move to phase 6. | Handoff readiness, deliverable register, unresolved blockers. |

## Canonical Pipeline

Read `references/skills-catalog.md`, `references/prompt-integration.md`, and `references/quality-gates.md` only when their details are needed. Use the asset contracts first:

- `assets/phase-contract.json` defines phase ids, ordering, and required fields.
- `assets/skill-sequence-contract.json` defines canonical discovery skills and allowed phases.
- `assets/gate-policy.json` defines G1, feasibility checkpoint, G2, and G3 requirements.
- `assets/non-analysis-boundary.json` defines fields and behaviors this skill must reject.
- `assets/report-contract.json` defines the offline-validatable orchestration packet.

## Workflow

1. **Intake:** Identify requested mode, project name, known artifacts, missing artifacts, target variant, and requested output format.
2. **State check:** Inventory phase status, deliverables, owners, blockers, assumptions, and prior approvals.
3. **Sequence:** Produce a phase plan and skill sequence using only canonical discovery skills.
4. **Gate governance:** Evaluate gate readiness from evidence. Mark `pass`, `block`, or `pending`; never infer approval.
5. **Boundary check:** Confirm `does_not_analyze`, `no_prices`, and `no_downstream_execution` before delivery.
6. **Validation:** For JSON packets, run `bash skills/discovery-orchestrator/scripts/check.sh` or validate a packet with `scripts/validate_discovery_orchestrator_packet.py`.
7. **Handoff:** Emit next skill, required input, owner, and stop condition.

## Gate Rules

### G1: Scenario Selection Gate

Pass only when the packet proves at least three scenarios, complete scoring, explicit decision tree, recommended scenario id, at least three assumptions, and explicit approval. If assumptions exceed 30% of the packet claims, require a warning banner.

### Feasibility Checkpoint

Pass only when technical feasibility and software viability have explicit verdicts that do not block phase 4. If either verdict is not feasible or high-risk, hold the pipeline and route to the relevant downstream skill.

### G2: Roadmap Gate

Pass only when roadmap, prerequisites, effort expressed without prices, risks, and sponsor approval are present.

### G3: Final Approval Gate

Pass only after proposal QA, risk review, complete deliverable register, and client approval are present. Phase 6 handover starts only after G3 passes.

## Output Contract

Use `templates/output.md` for prose output and `assets/report-contract.json` for JSON packet output. A packet must include:

- `skill`, `reference_date`, `mode`, and evidence-tagged `summary`.
- Ordered `phase_plan`.
- Canonical `skill_sequence`.
- `gates` with explicit criteria and decisions.
- `handoff` with deliverables and next action.
- `boundary_checks` proving no analysis, no prices, and no downstream execution.
- Evidence-tagged `validation` and `risks`.

## Validation Gate

- [ ] Output uses the requested operating mode.
- [ ] Every claim has an evidence tag.
- [ ] Phase order matches `assets/phase-contract.json`.
- [ ] Skill names match `assets/skill-sequence-contract.json`.
- [ ] G1 cannot pass without required scenario evidence and approval.
- [ ] No domain findings, implementation steps, or prices appear in the output.
- [ ] Assumption ratio above 30% triggers a warning banner.
- [ ] JSON packet passes `scripts/validate_discovery_orchestrator_packet.py`.

## Self-Correction

If requested to analyze content, stop and route to the downstream analysis skill. If requested to proceed past a gate without evidence, mark the gate `block` and list missing evidence. If a packet uses moving time words such as `today`, `tomorrow`, `soon`, or `TBD`, replace them with exact dates or explicit blocker states.
