<!--
generated-by: scripts/scaffold-skill.py
generated-for: funnel-design
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Funnel Design

Deterministic funnel blueprinting for TOFU/MOFU/BOFU content maps, lead scoring, nurture paths, qualification rules, and sales handoff.

## Triggers

- funnel-design
- TOFU/MOFU/BOFU
- content mapping
- lead scoring
- nurture flow
- qualification rules

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when a request needs a campaign funnel structure before content production, CRM automation, or analytics measurement.

When structured data exists, run:

```bash
python3 skills/funnel-design/scripts/compile-funnel-design.py \
  --input skills/funnel-design/scripts/fixtures/funnel-design-input.json
```

## Output Format

Markdown with funnel context, TOFU/MOFU/BOFU content map, lead scoring, nurture flow, handoff rules, gaps, validation, and risks.
