---
name: form-ux-advanced
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Multi-step forms, inline validation, smart defaults, error recovery. [EXPLICIT]
  Trigger: "form ux advanced"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Form Ux Advanced
> "Method over hacks."
## TL;DR
Multi-step forms, inline validation, smart defaults, error recovery. [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather form journey context: user goal, steps, field count, required fields, abandonment risks, device mix, and completion constraints.
- Load reusable assets from `assets/`: `ux-heuristics.json`, `inline-validation-copy.json`, `wizard-progress-template.html`, and `error-recovery-checklist.md`.
### Step 2: Analyze
- Audit friction across steps, required fields, validation timing, smart defaults, progress visibility, back navigation, and recovery after failure.
- Use `scripts/audit-form-ux.py --journey <journey.json>` when the form journey can be expressed as JSON.
### Step 3: Execute
- Produce a prioritized UX improvement plan with friction score, blocking issues, recovery patterns, and deterministic copy recommendations.
- Apply `wizard-progress-template.html` for multi-step progress and `inline-validation-copy.json` for actionable field messages.
### Step 4: Validate
- Run `scripts/check.sh` after changing bundled assets, fixtures, or the UX audit script.
- Verify the journey preserves user input, supports back navigation, avoids premature errors, and gives a retry path after submit failure.
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] `assets/manifest.json` declares every reusable form UX asset
- [ ] `scripts/audit-form-ux.py` flags excessive friction, missing smart defaults, harsh validation timing, and weak recovery
- [ ] Multi-step UX includes progress, back navigation, draft preservation, inline feedback, and post-error recovery

## Usage

Example invocations:

- "/form-ux-advanced" — Run the full form ux advanced workflow
- "form ux advanced on this project" — Apply to current context

## Deterministic Script Contract

- Runtime script: `scripts/audit-form-ux.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill form-ux-advanced`
- Default behavior: render a Markdown audit to stdout; write files only with `--output`.
- Safety boundary: invalid journeys fail nonzero instead of producing incomplete UX advice.

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every reusable asset and where it is used.
- `assets/ux-heuristics.json` defines scoring thresholds and required journey capabilities.
- `assets/inline-validation-copy.json` provides deterministic copy patterns by validation problem.
- `assets/wizard-progress-template.html` provides accessible progress markup.
- `assets/error-recovery-checklist.md` provides the recovery baseline for failed submissions.


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
