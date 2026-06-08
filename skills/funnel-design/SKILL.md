---
name: funnel-design
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  TOFU/MOFU/BOFU content mapping, lead scoring, nurture flow design. [EXPLICIT]
  Trigger: "funnel design", "TOFU/MOFU/BOFU", "content mapping",
  "lead scoring", "nurture flow", "qualification rules".
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Funnel Design

> "Method over hacks. Evidence over assumption."

## TL;DR

Deterministic funnel design for TOFU/MOFU/BOFU content mapping, lead scoring, nurture flow logic, qualification rules, and handoff criteria. [EXPLICIT]

Use this skill when the user needs a marketing or sales funnel blueprint before implementation, campaign production, CRM setup, or analytics instrumentation. [EXPLICIT]

## Procedure

### Step 1: Discover funnel context
- Capture product, offer, target audience, funnel goal, conversion event, sales motion, and available content inventory. [EXPLICIT]
- Separate acquisition intent (TOFU), consideration intent (MOFU), and conversion intent (BOFU). [EXPLICIT]
- If structured data exists, normalize it to `assets/funnel-design-schema.json`. [EXPLICIT]

### Step 2: Map content by stage
- Use `assets/stage-content-model.json` to map awareness, education, evaluation, proof, objection handling, and decision content. [EXPLICIT]
- Every stage needs owner, audience intent, core question, content assets, CTA, and success metric. [EXPLICIT]
- Do not place BOFU sales pressure in TOFU unless the input explicitly requires direct response. [EXPLICIT]

### Step 3: Define lead scoring
- Use `assets/lead-scoring-model.json` for fit, intent, and engagement scoring. [EXPLICIT]
- Scores must map to explicit lifecycle states: cold, engaged, MQL, SQL, and sales-ready. [EXPLICIT]
- Flag missing scoring evidence instead of inventing behavior or firmographic data. [EXPLICIT]

### Step 4: Design nurture flow
- Use `assets/nurture-flow-schema.json` to define triggers, delays, branch conditions, messages, and exit criteria. [EXPLICIT]
- Keep nurture steps tied to lead score changes and stage intent. [EXPLICIT]
- Include reactivation and disqualification paths when evidence is incomplete. [EXPLICIT]

### Step 5: Compile deterministic output
- Prefer `scripts/compile-funnel-design.py --input <json> --output <report.md>` when structured data is available. [EXPLICIT]
- Return content map, scoring rules, nurture paths, gaps, risks, and handoff checklist in `templates/output.md` order. [EXPLICIT]

## Quality Criteria

- [ ] TOFU/MOFU/BOFU stages are all present.
- [ ] Every stage has intent, content assets, CTA, metric, and owner.
- [ ] Lead scoring is explicit and threshold-based.
- [ ] Nurture flow has triggers, delays, branch rules, and exits.
- [ ] Sales handoff criteria are deterministic.
- [ ] Gaps are marked instead of invented.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Stage soup | Content mixed without buyer intent | Map every asset to TOFU, MOFU, or BOFU |
| Vanity scoring | Points without qualification meaning | Link scores to lifecycle thresholds |
| Infinite nurture | No exit or handoff | Define trigger, branch, exit, and owner |
| Missing evidence tags | Claims without basis | Tag every assertion |

## Related Skills

- `funnel-analytics` for measured conversion/drop-off diagnosis after launch.

## Usage

Example invocations:

- "/funnel-design" — Run the full funnel design workflow
- "funnel design on this project" — Apply to current context
- "Map TOFU/MOFU/BOFU content for this campaign" — Build content map and CTAs
- "Create lead scoring and nurture flow" — Build scoring thresholds and automation path


## Assumptions & Limits

- Assumes the user can provide audience, offer, goal, and at least one conversion event. [EXPLICIT]
- Does not claim campaign performance; use `funnel-analytics` after measurement exists. [EXPLICIT]
- Does not replace legal/privacy review for email, CRM, consent, or tracking rules. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request audience, offer, goal, conversion event, and sales motion |
| Missing content inventory | Produce gap map and minimum viable content plan |
| Conflicting funnel goals | Flag conflict and split acquisition, activation, and revenue paths |
| No CRM or email platform | Produce platform-neutral nurture logic |
| Out-of-scope request | Redirect analytics work to `funnel-analytics` |

## Deterministic Assets

- `assets/manifest.json` lists local assets and consumers. [EXPLICIT]
- `assets/funnel-design-schema.json` defines required structured input. [EXPLICIT]
- `assets/stage-content-model.json` defines TOFU/MOFU/BOFU stage requirements. [EXPLICIT]
- `assets/lead-scoring-model.json` defines scoring dimensions and lifecycle thresholds. [EXPLICIT]
- `assets/nurture-flow-schema.json` defines nurture steps, branches, and exits. [EXPLICIT]
- `assets/qualification-rules.json` defines deterministic handoff/disqualification rules. [EXPLICIT]
- `scripts/compile-funnel-design.py` compiles a deterministic Markdown funnel design. [EXPLICIT]
