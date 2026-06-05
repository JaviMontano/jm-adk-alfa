---
name: assumption-log
description: Track and validate project assumptions with A-NNN identifiers, allowed statuses, evidence tags, contradiction links, decision links, and a validation queue. [EXPLICIT]
version: 1.0.1
status: production
owner: Javier Montaño
tags: [analysis, assumptions, tracking, validation, evidence]
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# assumption-log

Track project assumptions as a deterministic register before architecture,
planning, implementation, or release decisions. [EXPLICIT]

## Purpose

Use this skill to separate verified facts from assumptions, keep assumption IDs
stable, validate or invalidate assumptions with evidence, and maintain the next
actions needed to reduce delivery risk. [EXPLICIT]

## Deterministic Assets

Use these local files before producing or reviewing an assumption log:

| Path | Use |
|---|---|
| `assets/activation-policy.json` | Activation, false-positive, and clarification rules |
| `assets/status-policy.json` | Allowed statuses, transitions, IDs, impact, and risk levels |
| `assets/log-contract.json` | Required report sections and fields |
| `assets/evidence-policy.json` | Evidence tags and proof requirements |
| `scripts/validate_assumption_log.py` | Offline JSON report validator |
| `scripts/check.sh` | Positive and negative fixture check |

The validator reads only local JSON files. It does not call the network, current
time, random sources, model providers, or MCP tools. [EXPLICIT]

## When To Activate

Activate when the user asks to:

- identify, list, track, validate, invalidate, review, or retire assumptions;
- create an assumption log, assumption register, hypothesis tracker, evidence
  gap list, risk assumption list, or validation queue;
- prepare for planning by separating known facts from unvalidated claims.

Do not activate for statistics assumptions, grammar review, weather questions,
generic activity logs, certificate documents, or implementation-only requests
that do not need assumption tracking. [EXPLICIT]

If the request lacks a project scope or evidence source, ask for the minimum
missing input or produce a gap analysis without inventing claims. [EXPLICIT]

## Input Contract

Accept any mix of:

- project scope or decision context;
- claims, requirements, risks, meeting notes, architecture notes, or code/docs;
- existing assumption IDs that must be preserved;
- evidence sources with paths, snippets, or document references.

## Output Contract

Produce Markdown by default and keep it compatible with the JSON contract in
`assets/log-contract.json`. [EXPLICIT]

Required sections:

1. `Summary`
2. `Assumptions`
3. `Contradictions`
4. `Decision Links`
5. `Validation Queue`
6. `Warnings`

Every assumption row must include:

- `id`: gapless ascending `A-001`, `A-002`, `A-003`, ...
- `statement`: one testable claim
- `status`: one of `unvalidated`, `validating`, `validated`, `invalidated`,
  `superseded`, `blocked`, or `stale`
- `evidence_tag`: one of `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`, or
  `[ASSUMPTION]`
- `evidence`: source, observation, or explicit absence of evidence
- `impact`: `low`, `medium`, `high`, or `critical`
- `validation_action`: the next action for open assumptions
- `owner`: role or team accountable for validation
- `decision_link`: related decision, ADR, risk, or backlog item

Validated and invalidated assumptions require a strong evidence tag:
`[CODE]`, `[CONFIG]`, or `[DOC]`. Unvalidated assumptions must use
`[ASSUMPTION]` and must not be written as facts. [EXPLICIT]

## Process

1. Confirm activation with `assets/activation-policy.json`.
2. Extract candidate assumptions from the supplied scope and evidence.
3. Normalize each assumption to one testable statement.
4. Preserve existing `A-NNN` IDs when supplied; assign new IDs gaplessly.
5. Assign status, evidence tag, source reference, impact, owner, and decision link.
6. Detect contradictions by citing the conflicting assumptions or sources.
7. Build the validation queue for every high-impact open assumption.
8. Calculate evidence-tag percentages and `assumption_ratio`.
9. Add a `HIGH_ASSUMPTION_RATIO` warning when more than 30% of entries use
   `[ASSUMPTION]`.
10. Validate the report against the local contract when JSON output is supplied.

## Local Validation

Run the skill check:

```bash
bash skills/assumption-log/scripts/check.sh
```

Validate a JSON report:

```bash
python3 -B skills/assumption-log/scripts/validate_assumption_log.py \
  --contract skills/assumption-log/assets/log-contract.json \
  --status-policy skills/assumption-log/assets/status-policy.json \
  --evidence-policy skills/assumption-log/assets/evidence-policy.json \
  --report <assumption-log.json>
```

## Quality Gate

- All IDs are `A-NNN`, ascending, unique, and gapless.
- All statuses and evidence tags are from the local policies.
- Closed statuses have strong evidence and `source_ref`.
- High-impact open assumptions appear in the validation queue.
- Contradictions and decisions reference known assumption IDs.
- The warning threshold is calculated, not guessed.
- No implementation work is performed as part of assumption logging.

## Assumptions & Limits

- This skill is read-only for project artifacts. It may run local validators but
  does not modify the target project. [EXPLICIT]
- If evidence is unavailable, mark the entry `unvalidated` instead of promoting
  it to a fact. [EXPLICIT]
- Dates must come from user-provided context or explicit source material; do not
  infer review dates from wall-clock time unless the user asks for "today."
  [EXPLICIT]
