---
name: discovery-orchestration
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Orchestrates the discovery pipeline by sequencing skills, enforcing quality
  gates, and tracking deliverable completion. Manages the flow from initial
  input through analysis to validated output. [EXPLICIT]
  Trigger: "discovery pipeline", "orchestrate", "gate enforcement", "deliverable tracking"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Discovery Orchestration

> "Orchestration is the art of making many instruments sound like one voice." — Leopold Stokowski

## TL;DR

Manages the end-to-end discovery pipeline by sequencing skill execution, enforcing quality gates between phases, and tracking deliverable completion. Use this skill when running a full discovery engagement, coordinating multiple analysis skills, or ensuring nothing falls through the cracks. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the discovery scope: full engagement or focused analysis
- Determine which skills are needed based on project type and objectives
- Assess available inputs: existing documentation, stakeholder access, codebase
- Check for existing discovery artifacts that can be reused or updated
- Capture deliverables, owners, dependencies, phase gates, blockers, and exit
  criteria before sequencing.

### Step 2: Analyze
- Sequence skills based on dependencies (requirements before architecture, stakeholders before communication)
- Define quality gates between phases with explicit pass/fail criteria
- Identify parallel execution opportunities (skills that don't depend on each other)
- Estimate effort per skill and total discovery timeline
- Use `assets/dependency-policy.json` to avoid cycles and unsupported parallelism.
- Use `assets/gate-policy.json` and `assets/deliverable-policy.json` for gate
  and completion status.

### Step 3: Execute
- Generate `plan-YYYY-MM-DD-task-name.md` at pipeline start using the template
  from `references/ontology/intent-integrity-governance.md`. Plan file is a
  prerequisite for any downstream execution (Constitution XIII)
- Execute skills in dependency order, passing outputs as inputs to downstream skills
- Enforce Constitution phase gates: Think (G0 pre-flight) → Act (G1 post-spec) →
  Verify (G2 post-plan) → Integration (G3 deploy-ready). Block phase transitions
  when gate criteria are unmet
- When ambiguity is detected during execution, trigger Socratic debate
  (Constitution governance) before proceeding
- Track deliverable status: not started, in progress, complete, validated
- Produce a discovery dashboard showing progress, blockers, and next steps
- Aggregate findings into a unified discovery report

### Step 4: Validate
- Verify all required deliverables are complete and validated
- Confirm quality gates were enforced (no shortcuts taken)
- Check cross-references between deliverables for consistency
- Review the complete discovery package with stakeholders
- For JSON orchestration packets, run
  `bash skills/discovery-orchestration/scripts/check.sh`.

## Deterministic Assets

- `assets/manifest.json` lists local assets and consumers.
- `assets/pipeline-schema.json` defines pipeline and phase fields.
- `assets/gate-policy.json` defines pass/block gate criteria.
- `assets/deliverable-policy.json` defines deliverable states and validation.
- `assets/dependency-policy.json` defines dependency graph rules.
- `assets/status-taxonomy.json` defines canonical status values.
- `assets/report-contract.json` defines the offline-validatable orchestration
  packet.

## Quality Criteria

- [ ] Skill sequence respects dependency graph
- [ ] Quality gates have explicit, measurable criteria
- [ ] All deliverables are tracked with status and owner
- [ ] Cross-deliverable consistency is verified
- [ ] Evidence tags applied to all claims
- [ ] Dependency graph is acyclic
- [ ] Every phase transition has a gate
- [ ] A ready pipeline has only validated deliverables and passing gates
- [ ] A blocked pipeline has explicit blockers and next actions

## Anti-Patterns

- Skipping quality gates under time pressure
- Running all skills sequentially when parallel execution is possible
- Discovery without a defined end state or exit criteria
- Marking deliverables complete without validation evidence
- Parallelizing dependent skills in the same phase

## Related Skills

- `input-analysis` — Amplifies initial input before pipeline processing
- `requirements-engineering` — Key deliverable in the discovery pipeline
- `system-architecture` — Downstream consumer of discovery outputs
- `integrity-chain-validation` — Validates the governance chain end-to-end
- `socratic-debate` — Resolves ambiguities during pipeline execution

## Usage

Example invocations:

- "/discovery-orchestration" — Run the full discovery orchestration workflow
- "discovery orchestration on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Cyclic dependency | Block sequencing and report the cycle |
| Missing gate criteria | Block phase transition |
| Ready status with unvalidated deliverables | Downgrade to blocked |
