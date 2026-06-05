---
name: workflow-creator
version: 1.0.1
description: Generates deterministic 17-field workflow definitions with step contracts, DoD, RACI, KPIs, validation rules, and failure handling for agentic ecosystems. Use when the user asks to create a workflow, define workflow steps, build workflow YAML, generate a workflow spec, design a RACI-backed procedure, or convert an agentic process into a repeatable workflow.
argument-hint: workflow-id [owning-skill-id]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Workflow Creator

Create complete workflow definitions that can be reviewed, executed, and
validated. A valid workflow is a 17-field contract with 3-7 ordered steps,
each step carrying 12 traceability fields, plus DoD, QA, RACI, KPIs, fallback,
and escalation routes. [EXPLICIT]

## Deterministic Assets

Load only the local assets needed for the request. [EXPLICIT]

| Path | Use |
|---|---|
| `assets/workflow-definition-contract.json` | Required fields, field types, and deterministic validation rules |
| `assets/activation-policy.json` | Activate/decline rules, clarification triggers, and network policy |
| `assets/quality-gates.json` | Blocking quality gates for workflow definitions |
| `assets/workflow-output-template.md` | Stable Markdown/YAML section order |
| `scripts/validate_workflow_spec.py` | Offline validator for JSON workflow specs |
| `scripts/check.sh` | Deterministic positive and negative fixture check |

The validator reads local JSON only. It does not call APIs, MCP tools, model
providers, the network, system time, random sources, or repo-global state beyond
the provided files. [EXPLICIT]

## When To Activate

Use this skill for workflow definitions, not for generic plans or one-off task
lists. [EXPLICIT]

| User intent | Activate? | Reason |
|---|---:|---|
| "Create a workflow for agent handoff review" | Yes | Needs ordered steps, roles, QA, and failure routes |
| "Build workflow YAML with RACI and KPIs" | Yes | Requests the 17-field workflow contract |
| "Define the steps, DoD, and escalation route" | Yes | Workflow governance is explicit |
| "Give me a quick checklist" | No | Checklist does not require full workflow contract |
| "Write a project plan" | No | Use planning/project-management skills unless workflow fields are requested |
| "What is a workflow?" | No | Answer directly without loading assets |

If the user provides a workflow ID but no owning skill, ask for the owning skill
or state that the workflow is standalone before producing the final spec.
[EXPLICIT]

## Inputs

Minimum input required before final output: [EXPLICIT]

| Input | Rule |
|---|---|
| `workflow_id` | Kebab-case identifier, unique in the target context |
| `owning_skill_id` | Existing or explicitly proposed owner; unknown values stay `[OPEN]` |
| `objective` | Measurable outcome that names the deliverable |
| `trigger` | Concrete event, command, condition, or request |
| `actors` | Agents or human roles used in RACI/escalation |
| `inputs` | Named data required to start the workflow |
| `success_evidence` | Observable completion signals |
| `failure_modes` | At least one recoverable and one unrecoverable failure route |

Ask for missing blocking inputs. If the user asks to proceed with gaps, mark
each gap `[OPEN]` and lower confidence instead of inventing facts. [EXPLICIT]

## Output Contract

Produce a Markdown response with an embedded `workflow.yaml` block. The YAML
must contain these 17 top-level fields in this order: [EXPLICIT]

```yaml
- id: "{kebab-case-id}"
  title: "{Human-readable title}"
  objective: "{Measurable outcome that produces a named deliverable}"
  trigger: "{Specific event, command, or condition}"
  preconditions:
    - "{Checkable condition before starting}"
  inputs:
    - name: "{name}"
      type: "{string|object|array|boolean|number|file|url}"
      required: true
      description: "{what it provides and why it matters}"
  steps:
    - stepNumber: 1
      title: "{2-5 words}"
      desc: "{1-2 sentences}"
      whyThisMatters: "{Failure consequence, not a restatement}"
      inputNeeded: "{Specific data with types}"
      actionInstruction: "{Concrete operation or prompt construction rule}"
      promptToUse: "{Full prompt text, or null (mechanical step)}"
      expectedOutput: "{Success output format and content}"
      validationRule: "{Observable pass/fail condition}"
      failureSignal: "{Observable failure condition}"
      recoveryAction: "{Concrete recovery action}"
      handoffIfNeeded: "{agent-id, human role, or null}"
  mainOutput: "{Primary deliverable with format}"
  secondaryOutputs:
    - "{logs, metrics, notifications, state changes}"
  DoD:
    - "{Verifiable assertion that blocks completion}"
  qaChecklist:
    - "{Specific quality check}"
  raci:
    responsible: "{agent or role}"
    accountable: "{agent or role}"
    consulted: "{agent, role, or none}"
    informed: "{agent, role, or none}"
  kpis:
    - metric: "{metric name}"
      target: "{numeric or bounded value}"
      unit: "{seconds|minutes|percentage|count|ratio|boolean}"
      measurement: "{how to measure}"
  cadence: "{on-demand|hourly|daily|weekly|per-event|per-request}"
  errorHandling: "{Unrecoverable error strategy}"
  fallbackRoute: "{workflow-id, direct-response, or stop-and-ask}"
  escalationRoute: "{agent-id or human role}"
```

When a deterministic check is required, mirror the YAML as JSON and run:

```bash
python3 skills/workflow-creator/scripts/validate_workflow_spec.py \
  --contract skills/workflow-creator/assets/workflow-definition-contract.json \
  --spec path/to/workflow.json
```

## Creation Process

1. Confirm activation using `assets/activation-policy.json`. [EXPLICIT]
2. Read the owning skill or local catalog only when available in the workspace.
   Unknown references must remain `[OPEN]`. [EXPLICIT]
3. Identify workflow ID, objective, trigger, actors, inputs, outputs, KPIs,
   failure modes, and escalation target. [EXPLICIT]
4. Decompose into 3-7 linear steps. Each step must have all 12 traceability
   fields. [EXPLICIT]
5. Assign RACI roles using real agents or explicit human roles. Do not use
   anonymous owners such as "team" or "someone". [EXPLICIT]
6. Add DoD, QA checklist, KPIs, fallback route, and escalation route before
   writing the final answer. [EXPLICIT]
7. Validate against `assets/quality-gates.json`; run the script when a JSON
   spec or fixture is available. [EXPLICIT]

## Quality Standards

| Field | Good | Block |
|---|---|---|
| `objective` | "Produce a reviewed PR package with local gates passed" | "Handle the PR" |
| `trigger` | "`/jm:harden-skill workflow-creator` is invoked" | "When needed" |
| `whyThisMatters` | "Without validation, ledger closure may certify an untested skill" | "This step validates" |
| `actionInstruction` | "Run `validate-skill-dod.py --skill {{skill}}` and capture exit code" | "Check the skill" |
| `validationRule` | "Exit code is 0 and output contains `dod=pass`" | "Looks correct" |
| `failureSignal` | "Exit code non-zero or missing `dod=pass` token" | "It fails" |
| `recoveryAction` | "Stop, patch missing asset or eval case, rerun the gate" | "Try again" |
| `kpis` | "`local_gate_failures`, target `0`, unit `count`" | "Quality is good" |

## Validation Gate

- [ ] All 17 top-level fields are present.
- [ ] `id` is kebab-case and `title` is human-readable.
- [ ] `objective` names the expected deliverable and success outcome.
- [ ] `trigger` is a specific event, command, condition, or request.
- [ ] `preconditions`, `inputs`, `secondaryOutputs`, `DoD`, `qaChecklist`,
  and `kpis` are non-empty lists.
- [ ] There are 3-7 ordered steps.
- [ ] Every step includes all 12 step fields and `stepNumber` values are
  sequential.
- [ ] Every `validationRule`, `failureSignal`, and `recoveryAction` is
  observable enough to fail closed.
- [ ] RACI fields name concrete agents or roles.
- [ ] KPI units are measurable and target values are bounded.
- [ ] `fallbackRoute` and `escalationRoute` name concrete destinations.
- [ ] No placeholder values such as `TBD`, `when needed`, `someone`, or
  `check everything` remain.

## Edge Cases

- **Conditional logic:** Keep the main step sequence linear. Put alternatives
  in `validationRule`, `recoveryAction`, `fallbackRoute`, or a named
  sub-workflow.
- **External service:** Include timeout, retry budget, error code, and fallback.
- **Single-agent workflow:** Still use 3 phases: prepare, execute, verify.
- **Missing owning skill:** Ask once; if the user proceeds, mark owner `[OPEN]`.
- **Workflow too small:** Recommend a checklist or runbook instead of forcing
  the 17-field contract.
- **Workflow too large:** Split into parent workflow plus sub-workflows.

## Assumptions And Limits

- This skill creates workflow definitions; it does not execute them.
- Deterministic validation proves structure, not strategic correctness.
- Catalog alignment depends on local files available in the current workspace.
- Network lookup is off by default and requires explicit user request plus
  source attribution.

---
**Author:** Javier Montano | **Last updated:** 2026-06-05
