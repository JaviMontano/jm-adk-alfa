<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Session Lifecycle Management Output

## Decisión de transición

{transition}  <!-- resume | fork | fresh -->

**Razón:** {reason}

## Evidencia de staleness

| Tool result | Fuente | Señal | Estado |
|---|---|---|---|
| {result} | {source} | {mtime_or_hash_or_head} | {fresh_or_stale} |

## TypedSummary (si fresh)

```json
{
  "goal": "{goal}",
  "decisions": [],
  "open_questions": [],
  "verified_facts": [],
  "stale_dropped": []
}
```

## Forks (si fork)

- {branch}: scratchpad y workspace aislados → {isolation_note}

## Validación

- [ ] Staleness detectada contra la fuente
- [ ] Summary tipado (no transcript crudo)
- [ ] Forks sin estado mutable compartido
- [ ] Transición trazada con su razón
- [ ] Stale crítico fuerza fresh

## Riesgos y límites

{risks}
