---
name: workflow-forge
description: Creates slash-command workflow definitions with phase maps, agent handoffs, verification checkpoints, and deterministic validation. Use when the user asks to create a workflow, forge a slash command, turn a process into phases, define an agent workflow, or prepare a repeatable command flow.
version: 1.0.0
status: production
owner: Javier Montaño
tags: [core, forge, workflow, scaffold]
argument-hint: "workflow-spec.json [--format markdown|json]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Workflow Forge

Create slash-command workflow definitions that are explicit enough to run,
review, and validate. A workflow is not a loose checklist: it is a phase-based
contract with named agents, inputs, outputs, checkpoints, and a final
verification gate. [EXPLICIT]

## Deterministic Workflow Compiler

Use `scripts/compile-workflow-forge.py` when the task needs a reproducible
workflow artifact from structured input. The compiler reads only local JSON
fixtures and local `assets/` policies; it never calls APIs, MCP tools, model
providers, or the network. [EXPLICIT]

```bash
python3 skills/workflow-forge/scripts/compile-workflow-forge.py \
  --input skills/workflow-forge/scripts/fixtures/skill-audit-workflow.json \
  --output /tmp/skill-audit-workflow.md
```

For machine-readable output, add `--format json`. The stable output sections
are `frontmatter`, `phase_map`, `checkpoints`, `quality_gates`,
`example_dialogue`, and `validation`. [EXPLICIT]

Read `assets/workflow-forge-schema.json` for the input contract,
`assets/workflow-policy.json` for phase and checkpoint rules, and
`assets/source-map.md` for local source references. [EXPLICIT]

## When to Activate

Use this skill for workflow definitions, not for generic project plans. [EXPLICIT]

| User intent | Activate? | Reason |
|---|---:|---|
| "Create `/jm:triage-ticket` with phases and agents" | Yes | Slash-command workflow contract |
| "Turn this support process into a command flow" | Yes | Repeatable phase-based process |
| "Define agent handoffs and verification gates" | Yes | Workflow governance |
| "Write a one-off task list" | No | Use a plan/checklist skill |
| "Create a spreadsheet template" | No | Use a template/spreadsheet skill |

## Before Forging

1. Confirm the trigger command and deliverable are explicit. If either is
   missing, ask before writing. [EXPLICIT]
2. Inspect existing command/workflow files to avoid duplicating a command name.
   [EXPLICIT]
3. Cross-check declared agents and skills against available catalogs when the
   repo provides them. Unknown references must be marked `[OPEN]`. [EXPLICIT]
4. Load only the needed local assets: schema, workflow policy, output template,
   and source map. [EXPLICIT]

## Workflow Contract

A valid workflow definition must include: [EXPLICIT]

| Field | Rule |
|---|---|
| `workflow_id` | Kebab-case identifier, unique inside the workflow namespace |
| `command` | Slash command beginning with `/` |
| `description` | One-line purpose with the expected outcome |
| `deliverable` | Concrete output produced by the workflow |
| `skills_involved` | Non-empty list of skill IDs |
| `agents_coordinated` | Non-empty list of agent IDs |
| `phases` | At least 2 phases; first is clarification/planning; final is verification |
| `quality_gates` | Testable criteria that block completion |
| `example_dialogue` | Minimal user/assistant exchange showing activation |

## Core Process

### Phase 1: Intent Mapping

- Extract `command`, `workflow_id`, deliverable, audience, and boundary of use.
- Identify missing inputs that would make the workflow ambiguous.
- Decide whether the request is a workflow, a runbook, or a one-off plan.

### Phase 2: Catalog Alignment

- List participating skills and agents.
- Mark each reference as `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- Reject anonymous work: every phase must name at least one responsible agent.

### Phase 3: Phase Design

- Build 3-7 phases where possible.
- Phase 1 handles clarification/planning.
- Middle phases execute work with clear inputs and outputs.
- The final phase verifies completion against quality gates.
- Each phase includes a checkpoint that can fail closed before the next phase.

### Phase 4: Assembly

- Write frontmatter with `description`, `command`, `skills_involved`, and
  `agents_coordinated`.
- Render a phase map, handoff table, checkpoints, quality gates, and example
  dialogue.
- Include failure handling for missing inputs, unknown agents, and blocked
  validation.

### Phase 5: Verification

- Validate against `assets/workflow-policy.json`.
- Run the local compiler/check script when structured input is available.
- Confirm the workflow has no prohibited stack references and no missing final
  verification phase.

## Quality Standards

| Standard | Good | Bad |
|---|---|---|
| Command | `/jm:review-skill` | `review stuff` |
| Phase | "Verify gates: validate DoD, scripts, diff hygiene" | "Check everything" |
| Agent | `quality-guardian` owns final validation | "someone validates" |
| Checkpoint | "All phase outputs have owner, status, and evidence tag" | "Looks good" |
| Failure route | "Stop and ask for command name if missing" | "Continue with assumptions" |

## Validation Gate

- [ ] Frontmatter has `description`, `command`, `skills_involved`, and `agents_coordinated`
- [ ] Workflow has at least 2 phases
- [ ] First phase is clarification or planning
- [ ] Final phase is verification
- [ ] Every phase declares agents, inputs, outputs, and checkpoint criteria
- [ ] Every declared phase agent appears in `agents_coordinated`
- [ ] Every quality gate is observable and testable
- [ ] Example dialogue shows the workflow activation
- [ ] Missing or unknown references are marked `[OPEN]`
- [ ] No prohibited stack references appear unless the user explicitly scopes them

## Antipatterns

| Antipattern | Why it fails | Fix |
|---|---|---|
| Single-phase workflow | No handoff or verification boundary | Split into clarify, execute, verify |
| Agentless workflow | Accountability disappears | Assign responsible agents per phase |
| Vague checkpoint | Cannot fail closed | Use observable pass/fail criteria |
| Hidden assumptions | Surprises the user during execution | Mark assumptions and ask when blocking |
| Stack leakage | Violates local kit constraints | Reject or flag prohibited stack terms |

## Edge Cases

- **Single-agent workflow:** Keep the same agent across phases, but still
  separate clarification, execution, and verification.
- **Unknown agent or skill:** Mark `[OPEN]`; do not invent a catalog entry.
- **Conflicting phase order:** Stop and resolve the dependency before writing.
- **Workflow too small:** Suggest a checklist or runbook instead of a command.
- **Workflow too large:** Split into parent workflow plus sub-workflows.
- **External stack requested:** Include only if user explicitly scopes it and the
  repo policy allows it.

## Reference Files

| Path | Use |
|---|---|
| `assets/workflow-forge-schema.json` | Input/output contract for deterministic compilation |
| `assets/workflow-policy.json` | Phase, checkpoint, stack, and quality gate rules |
| `assets/workflow-output-template.md` | Stable Markdown section order |
| `assets/source-map.md` | Local reference map for the skill |
| `scripts/compile-workflow-forge.py` | Offline compiler and validator |
| `scripts/check.sh` | Deterministic runtime check for positive and negative fixtures |

## Assumptions & Limits

- This skill creates workflow definitions; it does not execute the workflow.
- Catalog checks are only as complete as the files available in the current repo.
- Deterministic validation proves structure, not business correctness.
- Free-form user requests may still require clarification before compilation.

---
**Author:** Javier Montaño | **Last updated:** 2026-06-04
