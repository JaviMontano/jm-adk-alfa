---
name: official-source-verifier
version: 1.0.0
description: "Consult official sources (ADK, Agent Skills spec, GitHub/Git docs, framework docs) when a decision depends on them. Prioritizes official over secondary, cites source and date, records the change a finding justifies. Never elevates a secondary source to authority."
owner: "JM Labs (Javier Montaño)"
triggers:
  - official source
  - verify docs
  - adk spec
  - authoritative reference
  - source priority
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
---

# Official Source Verifier

## Capacidad

Verifica decisiones técnicas contra fuentes oficiales antes de modificar código, documentación o criterios de arquitectura. Prioriza documentación oficial sobre blogs, issues, respuestas de foro, snippets o resúmenes generados. Si una fuente secundaria ayuda al descubrimiento, se marca como pista y nunca se eleva a autoridad.

## Cuándo usarla

- Una decisión depende de documentación vigente de ADK, Agent Skills spec, GitHub/Git, frameworks, SDKs, APIs o servicios cloud.
- Una propuesta cita una fuente secundaria y hay que confirmar si una fuente oficial la respalda.
- Un cambio de repo necesita registrar qué fuente oficial justifica el hallazgo.
- Hay contradicción entre fuentes y se requiere priorización explícita.

No la uses para hechos triviales del código local que pueden verificarse directamente con Read/Grep/Glob.

## Contrato determinístico

Usa los assets de `assets/` para certificar reportes:

- `assets/official-source-verifier-contract.json`: campos obligatorios del reporte.
- `assets/source-priority-policy.json`: jerarquía oficial, vendor, spec, repo, secondary.
- `assets/claim-evidence-policy.json`: cada claim debe mapear a fuente oficial o quedar `unverified`.
- `assets/citation-policy.json`: URL, fecha de consulta y extracto/paráfrasis breve.
- `assets/decision-policy.json`: cambios autorizados sólo por evidencia oficial.
- `assets/evidence-policy.json`: evidencia mínima aceptada.

Cuando el entregable sea JSON, valida offline con `scripts/validate_official_source_verifier.py`. Para la smoke determinística completa ejecuta `scripts/check.sh`, que acepta fixtures válidos y rechaza mutaciones inválidas.

## Procedimiento

1. Define la `question`: la decisión concreta que depende de autoridad externa.
2. Registra fuentes en `source_registry` con `source_id`, `source_type`, `url`, `accessed_date`, `publisher`, `official`, y `role`.
3. Busca primero fuentes oficiales. Usa fuentes secundarias sólo para descubrir rutas o vocabulario.
4. Para cada claim, exige `source_ids` y `official_source_ids`; si no hay fuente oficial, marca `status=unverified` y no autorices cambios.
5. Si fuentes oficiales se contradicen, prioriza spec o docs oficiales del proveedor más cercano al producto afectado y registra el conflicto.
6. La `decision` debe declarar `change_authorized`, `justified_change`, `scope`, y `blocking_gaps`.
7. Guardian bloquea si una fuente secundaria es autoridad, si falta fecha de consulta, si hay claim sin fuente oficial, o si el cambio no está justificado.

## Checklist de validación

- ¿Cada fuente tiene URL, publisher, fecha de consulta y tipo?
- ¿Cada claim tiene evidencia oficial o queda marcado `unverified`?
- ¿Ninguna fuente secundaria se usa como autoridad?
- ¿La decisión autorizada está vinculada a claims oficiales?
- ¿Los gaps bloqueantes impiden marcar `pass`?
- ¿El reporte pasa `scripts/check.sh` si se requiere evidencia offline?

## Related Skills

- `workspace-governance`
- `quality-gatekeeper`
- `repo-sync-auditor`
