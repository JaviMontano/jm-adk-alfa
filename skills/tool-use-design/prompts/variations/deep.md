<!--
generated-by: scripts/scaffold-skill.py
generated-for: tool-use-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Tool Use Design Deep Variation

Úsala cuando el tool surface es grande (muchas tools), hay overloading múltiple, o el cambio afecta el routing de todo un agente en producción.

Incluye:
- **Discovery:** inventario completo del tool surface + matriz de solapamientos por pares.
- **Opciones consideradas:** rename + split vs. merge vs. dejar como está, con el costo de routing de cada una.
- **Approach elegido:** descripciones-contrato finales con frontera recíproca para cada par en conflicto.
- **Estrategia de lectura:** `Grep → Read → Edit` aplicada al repo objetivo, con el fallback Read+Write para Edit documentado.
- **Validation:** checklist completo + casos de selección probados.
- **Risks:** tools que aún podrían confundirse y plan de telemetría de routing.
