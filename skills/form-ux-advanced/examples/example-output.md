<!--
generated-by: scripts/scaffold-skill.py
generated-for: form-ux-advanced
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The enterprise intake journey scores `86/pass` because it keeps the flow to two steps, preserves recovery paths, and avoids punitive validation timing.

## Deterministic Audit

- Run: `python3 skills/form-ux-advanced/scripts/audit-form-ux.py --journey skills/form-ux-advanced/scripts/fixtures/intake-journey.json`
- Required assets: `assets/ux-heuristics.json`, `assets/inline-validation-copy.json`, `assets/wizard-progress-template.html`, `assets/error-recovery-checklist.md`.

## UX Controls

- Keep progress visible with the wizard progress template.
- Validate work email on blur and upload state with debounced feedback.
- Preserve draft state on network failure and retry the same payload.
- Use a top summary after submit and inline messages connected to each field.

## Validation

- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill form-ux-advanced`
- `python3 -B scripts/validate-skill-dod.py --skill form-ux-advanced`
