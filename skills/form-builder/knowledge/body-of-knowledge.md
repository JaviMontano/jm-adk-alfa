# Form Builder — Body of Knowledge

## Canon

Forms are data contracts with a user interface. The form-builder skill must preserve semantic HTML, explicit labels, accessible hints, deterministic validation rules, and clear submission boundaries before implementation details such as React, Angular, or Firebase are selected.

## Schema Rules

| Rule | Target |
|---|---|
| Step wrapper | `fieldset` with `legend` |
| Control label | Every control has a matching `label for` |
| Hints | Hints use stable ids and `aria-describedby` |
| Required fields | Render both `required` attribute and visual marker |
| Conditional fields | Driver field must appear before dependent field |
| Submit | Explicit `<button type="submit">` |

## Asset Rules

- Use `assets/validation-policy.json` to constrain supported field types.
- Use `assets/form-step-template.html` for semantic multi-step structure.
- Use `assets/form-control.css` for accessible baseline styling.
- Keep `assets/manifest.json` synchronized with reusable assets.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Accessibility semantics | 100% controls labeled | Static render check |
| Conditional validity | 0 missing driver fields | Schema validation |
| Responsive readiness | Mobile-first structure | Template review |
| Evidence coverage | 100% | Claims cite schema/assets/tests |
| Validation Gate pass | 100% | DoD + script checks |
