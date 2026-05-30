<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Deterministic Agent Loop Meta Prompt

Decide si la Kata 01 (bucle agéntico determinista) debe activarse, si el alcance es seguro y qué agentes de apoyo participan.

## Activation Check

- ¿El request involucra un bucle agéntico que llama a la API en iteraciones?
- ¿El control de halt depende (o podría depender) de parsear texto del modelo?
- ¿Aparecen los triggers `deterministic loop`, `stop_reason`, `agent loop control` o `budget exceeded`?
- ¿Hay condición de parada, manejo de `tool_use`/`end_turn` o límite de iteraciones en juego?

## No activar si

- El input está vacío → pedir el objetivo del bucle.
- El request es ajeno al control de bucles agénticos.
- El usuario pide explícitamente ignorar la validación/evidencia (conflicto: enunciar y elegir la interpretación segura).

## Support routing

- `lead` para implementar el patrón.
- `support` para detectar parseo de prosa y stops sin manejar.
- `guardian` para certificar el argumento y bloquear el anti-patrón.
- `specialist` para semántica de `stop_reason` del SDK / Claude Code.
