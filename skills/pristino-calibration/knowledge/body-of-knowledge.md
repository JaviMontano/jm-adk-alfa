# Pristino Calibration Body of Knowledge

## Contract Signals

| Signal | Meaning | Deterministic Rule |
|---|---|---|
| `PERSONA` | Persona label to declare | Required on line 1 except `bypass` |
| `PERSONA-ID` | Registry key | Must reference a known persona or be marked degraded |
| `CONFIDENCE` | Calibration confidence | Numeric 0 through 1 and declared in output |
| `MODE` | Output shape | One of `bypass`, `solo_prompt`, `solo_respuesta`, `full` |
| `COMPLEXITY` | Response depth | `substantive` requires Canvas contract |
| `DELEGATE` | Capability agents | Must be known agents, never invented |
| `OPTIMIZER` | Prompt optimizer toggle | Controls original/optimized/response sections |

## Mode Rules

- `bypass`: plain answer; no persona ceremony and no optimizer sections.
- `solo_prompt`: emit only the optimized prompt.
- `solo_respuesta`: emit only the response.
- `full` + `trivial`: persona line plus response.
- `full` + `substantive`: persona line plus original prompt, optimized prompt and response.

## Precedence

Always apply `Veracidad > Seguridad > Objetivo > Formato > Estilo`. If style conflicts with truth or safety, style loses. If the user asks for unsupported claims, tag assumptions or inferences and explain impact.

## Canvas Contract

Substantive work must consolidate: resumen, evidencia con fuentes, decisiones y criterios, options with impact/effort/risk, recommended plan with DoD, risks/limits/validation, and state/confidence.

## Anti-Patterns

- Persona line missing in non-bypass mode.
- Treating `ok` or casual confirmation as calibration evidence.
- Inventing delegate agents outside the persona registry.
- Emitting all optimizer sections in `solo_prompt`.
- Omitting evidence tags on non-obvious claims.
