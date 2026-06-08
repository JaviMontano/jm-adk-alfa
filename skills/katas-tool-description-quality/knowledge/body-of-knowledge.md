# Katas Tool Description Quality Body of Knowledge

## Canon

La descripcion de un tool es contrato de seleccion. El modelo decide por `name`, `description` e `input_schema`; no ve la implementacion.

## Required Contract Elements

| Element | Requirement |
|---|---|
| Input format | Declara el shape aceptado. |
| Query example | Incluye disparador concreto. |
| Boundary | Dice cuando usar otro tool. |
| Reciprocity | El otro tool devuelve la frontera inversa. |
| Name clarity | El nombre describe proposito y evita verbos genericos. |

## Decisions

- `rename`: usar cuando el nombre confunde el dominio o el shape.
- `split`: usar cuando un tool tiene varios modos o outputs incompatibles.
- `boundary_only`: usar cuando el nombre es claro pero falta frontera.
- `keep`: usar solo cuando el contrato ya es especifico y verificable.

## Anti-Pattern

`Analyzes content` y `Analyzes documents` son contratos solapados porque no declaran input format ni frontera.
