# Form Builder Assets

These assets provide deterministic form construction resources for semantic, accessible, multi-step forms.

## Files

- `form-control.css`: minimal accessible form styling for generated HTML.
- `form-step-template.html`: reusable semantic step/fieldset pattern.
- `validation-policy.json`: default validation and accessibility policy.
- `manifest.json`: machine-readable asset inventory and usage map.

## Contract

- Assets must preserve semantic labels and keyboard navigation.
- Assets must avoid framework-specific assumptions unless the user asks for a specific stack.
- Update `manifest.json` whenever a reusable asset changes purpose or usage.
