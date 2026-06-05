---
name: jarvis-os
version: 0.1.0
description: "Pack paraguas del Personal Jarvis OS: COOL, 5 sectores, 12 niveles, 8 capacidades, cadencias y scaffolders. Enruta a las skills del pack."
owner: "JM Labs"
triggers:
  - jarvis-os
  - jarvis
  - trabajar-amplificado
  - personal-jarvis
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Jarvis OS — Pack paraguas

Materializa el método **Trabajar Amplificado / MetodologIA Personal Jarvis OS** sobre alfa. Filosofía: *"Method First, (Gen)AI Next. Soberanía digital."* La guía completa vive en `docs/jarvis-os/` (playbook + runbook).

## Principios COOL

- **Clarify** — absorber input externo (email, reunión, decisión, dato) con timestamp + intención.
- **Organize** — colocar la captura en la ubicación correcta usando taxonomía estable.
- **Optimize** — validar antes de actuar; cargar el contexto/modelo/skill correcto.
- **Liberate** — producir y entregar el artefacto con precisión.

`Organize + Optimize` = motor estable; `Clarify + Liberate` se adaptan por dominio.

## Cinco sectores (N0–N4)

| Sector | Capa | Carpeta | Skill scaffolder |
|---|---|---|---|
| I Foundations | N0 | `00_Recursos/` | `jarvis-bootstrap` |
| II Base | N1 | `01_Estaciones/` | `station-create` |
| III Core | N2 | `02_Proyectos/` | `project-create` |
| IV R&D+i | N3 | `03_Lab/` | `lab-session` |
| V Maintenance | N4 | `04_Cadencias/` | cadence skills |

## Cadencias (6)

`dbr-daily-plan` (P09) · `daily-close` (P10) · `wbr-weekly-review` (P11) · `weekly-retro` (P12) · `qbr-quarterly` (P13) · `monthly-audit` (P22). MBR/ABR documentadas en runbook.

## Foundation skills (4)

`input-analysis` (reuso) · `revisor-veracidad` · `frontload-prompt` · `cierre-conversacion`.

## Reglas operativas

- **NOW ≤ 3** tareas simultáneas en cualquier `TAREAS.md`.
- **Rule stacking**: root → estación → proyecto; cada capa especializa sin repetir.
- **Rule-9 (tamaño CLAUDE.md)**: root ≤200, sector ≤60, estación ≤50, proyecto ≤70 líneas.
- **Verification tags** inline: ver `references/verification-tags.md`.
- **Regla de 3**: codificar una skill solo tras ejecutar el patrón 3+ veces.
- **14 días** en modo supervisado antes de automatizar una tarea programada.

## 12 niveles de adopción

Chat → Chat+prompts → Chat Projects → Cowork → Cowork Projects → **Skills** → Plugins → Mini-apps → Plugin engineering → Orchestrator Station → Web mini-apps → **Portabilidad** (soberanía digital).

## 8 capacidades (Anthropic)

Acceso a archivos · memoria persistente · conectores MCP · Skills · Cowork Projects · extensión navegador · tareas programadas · Dispatch móvil.

## Orquestación

El agente `jarvis-orchestrator` (en `agents/`) aplica COOL, detecta sector/estación, hace rule-stacking y marca verification tags. El ruteo personal del operador (íntimo) vive en `user-context/context/routing-map.md`.

## Scaffolders

`jarvis-bootstrap` · `station-create` · `project-create` · `lab-session` · `task-subfolder`.

## Quality Criteria

- La estructura generada respeta sectores N0–N4 y nombres kebab-case.
- NOW ≤ 3 y rule-stacking preservados.
- Sin secretos; contenido íntimo va a `user-context/`, nunca a `skills/` tracked.

## Related Skills

- `input-analysis`
- `revisor-veracidad`
- `workspace-setup`
