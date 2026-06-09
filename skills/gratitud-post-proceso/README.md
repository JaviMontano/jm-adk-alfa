# Gratitud Post Proceso

`gratitud-post-proceso` drafts professional thank-you messages after interviews, selection processes, workshops, review panels, or business conversations. It keeps messages specific to each recipient, grounded in supplied evidence, and aligned to a calm brand voice.

## Triggers

- `gratitud-post-proceso`
- `agradecimiento`
- `thank-you`

## Deterministic Contract

- Require recipient identity or role.
- Require at least one interaction-specific evidence detail.
- Avoid FOMO, hustle framing, servility, and stacked brand phrases.
- Do not invent next steps, acceptance signals, commitments, or process outcomes.
- Validate JSON packets offline with `scripts/lint_gratitud.py`.

## Local Validation

```bash
bash skills/gratitud-post-proceso/scripts/check.sh
python3 skills/gratitud-post-proceso/scripts/lint_gratitud.py --input skills/gratitud-post-proceso/scripts/fixtures/valid-interview-thank-you.json
```

## Assets

- `assets/recipient-differentiation-policy.json`
- `assets/evidence-policy.json`
- `assets/brand-voice-policy.json`
- `assets/promise-boundary-policy.json`
- `assets/output-contract.json`
