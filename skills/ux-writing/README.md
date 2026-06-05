# UX Writing

Deterministic UX writing skill for auditing information hierarchy, cognitive load, scannability, microcopy, and readability in stakeholder deliverables and product copy.

## Activation

Use this skill when the request asks to improve readability, fix information hierarchy, reduce cognitive load, write or review microcopy, improve CTAs, create error/empty-state/help text, or check readability.

Do not use it as the primary skill for technical accuracy, security validation, visual design, or end-user adoption risk assessment.

## Required Input

- Source copy, UI labels, or deliverable text.
- Target audience or product context.
- Any known constraints, such as language, tone, character limits, reading-level target, or accessibility requirement.

If context is missing, mark it `[SUPUESTO]` or ask for the minimum missing fact. Do not invent product features, metrics, owners, compliance status, or dates.

## Output Contract

Markdown packets must include:

- `# UX Writing Audit`
- `## Audience And Source`
- `## Findings`
- `## Rewrites`
- `## Accessibility And Readability`
- `## Validation`

For microcopy, include before/after pairs. For error messages, include what happened, why it happened when known, and how to fix. For empty states, include what is missing and the next action.

## Assets And Scripts

- `assets/ux-writing-checklist.md` defines the deterministic checklist.
- `assets/microcopy-patterns.json` defines allowed patterns and anti-patterns.
- `assets/readability-rubric.json` defines reading-level and accessibility checks.
- `scripts/validate_ux_writing_packet.py` validates Markdown packets against the local contract.

## Local Gates

```bash
bash skills/ux-writing/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ux-writing
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ux-writing
```
