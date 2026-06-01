# Form UX Advanced — Body of Knowledge

## Canon

Advanced form UX reduces completion friction without weakening validation. It covers step count, field burden, validation timing, smart defaults, progress visibility, back navigation, draft preservation, error summaries, retry behavior, and post-failure recovery.

## Heuristics

| Heuristic | Good Pattern | Risk Pattern |
|---|---|---|
| Step flow | Two or three clear steps with progress and back navigation. | Long wizards without orientation. |
| Inline validation | Blur or debounced feedback with specific copy. | Blocking keypress validation. |
| Smart defaults | Defaults from trusted context with user override. | Reasking known data. |
| Error recovery | Preserve answers, focus summary, link to invalid fields, retry safely. | Wiping the form after failure. |
| Required fields | Ask only what is needed to continue. | Treating every field as mandatory. |

## Scripted Audit

Use `scripts/audit-form-ux.py --journey <journey.json>` when a form journey can be represented structurally. The script loads `assets/ux-heuristics.json`, scores friction deterministically, and flags missing recovery capabilities.

## Asset Usage

- `assets/ux-heuristics.json`: scoring thresholds and penalties.
- `assets/inline-validation-copy.json`: field-level copy patterns.
- `assets/wizard-progress-template.html`: accessible progress baseline.
- `assets/error-recovery-checklist.md`: required recovery behavior after failures.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Friction score | >= 75 | `scripts/audit-form-ux.py` score. |
| Recovery coverage | 100% | Progress, back navigation, draft preservation, summary, and retry present. |
| Validation timing | 0 blocking keypress checks | Audit findings. |
| Smart defaults | At least one meaningful default when context exists | Journey field metadata. |
