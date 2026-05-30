<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-plan-mode-exploration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Plan Mode Exploration Output

## Summary

{summary}

## Evidence

{evidence}

## plan.md propuesto

### Hallazgos

{hallazgos}

### Arquitectura propuesta

{arquitectura_propuesta}

### Cambios a realizar (tras aprobación)

{cambios_propuestos}

## Configuración de seguridad

- permission_mode: `plan`
- allowed_tools: `["Read","Glob","Grep"]`
- hook PreToolUse: deniega `{write_tools}` mientras `mode=="plan"`

## Aprobación

- Estado: {estado_aprobacion}
- Firmado por: {firmante}
- Transición a escritura: {transicion}

## Validation

{validation}

## Risks and Limits

{risks}
