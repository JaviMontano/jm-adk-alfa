# Official Source Verifier

Verifica decisiones técnicas contra fuentes oficiales antes de cambiar código, documentación o criterios de arquitectura.

## Resumen ejecutivo

Usa esta skill cuando una decisión dependa de documentación vigente de ADK, Agent Skills, GitHub/Git, frameworks, SDKs, APIs o servicios cloud. El resultado debe priorizar fuentes oficiales, fechar la consulta, mapear cada claim a evidencia y registrar qué cambio justifica cada hallazgo.

## Contrato determinístico

El entregable certificable es un reporte JSON compatible con `assets/official-source-verifier-contract.json` y validable offline con `scripts/check.sh`.

Debe incluir:

- `question`: decisión concreta que depende de fuentes oficiales.
- `source_registry`: fuentes oficiales y secundarias, con URL, fecha de consulta y rol.
- `claims`: cada claim con fuente oficial primaria o, si no existe, marcado como `unverified`.
- `decision`: cambio autorizado por la evidencia y su alcance.
- `validation`: flags que prueban que no se elevó una fuente secundaria a autoridad.
- `guardian`: decisión final.

## Quick Use

1. Identifica la decisión que necesita autoridad externa.
2. Busca primero fuentes oficiales y registra fecha de consulta.
3. Usa fuentes secundarias sólo como pistas, nunca como autoridad.
4. Vincula cada claim a fuentes por `source_id`.
5. Autoriza cambios sólo cuando la fuente oficial justifique el hallazgo.

## Output Format

Markdown o JSON con summary, evidence, result, validation y risks. Para validación offline usa el JSON contract de `assets/`.
