<!--
generated-by: scripts/scaffold-skill.py
generated-for: form-builder
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Se genero un formulario multi-step semantico para lead intake.

## Assets Used

- `assets/form-control.css`
- `assets/form-step-template.html`
- `assets/validation-policy.json`

## Render Evidence

- `scripts/render-form-schema.py --schema scripts/fixtures/intake-form.json` produce HTML con `form`, `fieldset`, `legend`, labels y submit explicito.
- El campo `automation_scope` queda condicionado por `project_type=automation`.
- El schema invalido falla cuando una condicion referencia un campo inexistente.

## Validation

- Todos los controles tienen label.
- Los hints usan `aria-describedby`.
- Los campos condicionales dependen de campos previos.
- El renderer no escribe archivos salvo que se use `--output`.
