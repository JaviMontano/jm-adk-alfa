<!--
generated-by: scripts/scaffold-skill.py
generated-for: form-engineering
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The enterprise intake form needs a two-step implementation contract with validation parity, an accessible upload control, draft preservation, and idempotent optimistic submit.

## Deterministic Contract

- Run: `python3 skills/form-engineering/scripts/compile-form-contract.py --spec skills/form-engineering/scripts/fixtures/enterprise-intake-spec.json`
- Output sections: Validation Parity, Flow, Error System, Accessibility Hooks, Optimistic Submission, Asset Hooks.

## Required Engineering Controls

- `contact_email` uses `type=email` on the client and server-side normalization plus corporate-domain checks.
- `security_brief` accepts only PDF files, enforces a 10 MB maximum, shows progress, supports retry, and stores under `private/prospect/security-briefs`.
- The submit path uses an idempotency key so a retry does not duplicate the intake.
- Field errors render below controls and the summary focuses links to invalid fields.

## Validation

- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill form-engineering`
- `python3 -B scripts/validate-skill-dod.py --skill form-engineering`
