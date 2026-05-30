<!--
generated-by: scripts/scaffold-skill.py
generated-for: persistent-memory-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Estoy auditando una base de código grande para encontrar todas las rutas que tocan PII. Es una investigación que va a durar varias sesiones y la ventana de contexto se compacta cada cierto rato; cada vez que pasa, el agente "olvida" qué módulos ya revisó y los vuelve a inspeccionar.

Diseña una memoria persistente para esta auditoría: que sobreviva a `/compact` y a empezar sesión nueva mañana, que guarde solo lo confirmado (módulos validados, decisiones, pendientes) con su evidencia, y que no me rompa el rendimiento releyendo todo cada turno. La ruta puede ser `.agent/scratchpad.md`.
