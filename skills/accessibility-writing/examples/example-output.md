# Example Output

## Scope and Assumptions

| Field | Value |
| --- | --- |
| Objective | Rewrite onboarding page for accessible Spanish copy |
| Audience | Non-technical customers in Colombia |
| Language / locale | Spanish, Colombia |
| Channel | Web app onboarding |
| Content types | Alt text, chart description, CTA, error copy, instruction, paragraph rewrite |
| Reading target | Plain language; exact grade level not measured |
| Missing context | Brand tone and UI labels not provided |

## Reader-Facing Rewrite

### Bienvenido

Configura tu cuenta paso a paso y revisa tu avance en el panel.

### Avance de conversión

La conversión subió de 12% en enero a 18% en marzo.

### Acción principal

Continuar con la configuración

### Mensaje de error

Ingresa un correo con formato válido, por ejemplo nombre@empresa.com.

### Instrucción

Selecciona el botón "Continuar con la configuración".

## Alt Text and Image Descriptions

| Asset | Treatment | Proposed text | Rationale | Limits |
| --- | --- | --- | --- | --- |
| Hero image | Informative | Cliente revisando un panel de avance en un computador portatil. | Describes useful visual context without overloading. | Device and person are provided; no further details inferred. |
| Background pattern | Decorative | `alt=""` | It does not add meaning beyond the page content. | Assumes pattern is decorative. |
| Conversion chart | Complex | Short alt: "La conversión aumentó entre enero y marzo." Long description: "La conversión pasó de 12% en enero a 18% en marzo." | Captures the trend and exact supplied values. | Only January and March values were provided. |

## Links, Instructions, and Error Copy

| Item | Original | Accessible rewrite | Why it works |
| --- | --- | --- | --- |
| CTA link | Click here | Continuar con la configuración | Names the action out of context. |
| Error | Invalid | Ingresa un correo con formato válido, por ejemplo nombre@empresa.com. | Explains the problem and recovery action. |
| Instruction | Press the green button on the right. | Selecciona el botón "Continuar con la configuración". | Does not depend on color or position. |

## Validation Notes

| Claim / change | Evidence or source | Assumption | Status |
| --- | --- | --- | --- |
| Exact reading grade | None | No measurement tool was run | `not verified` |
| Chart values | User supplied January 12% and March 18% | No intermediate values provided | `verified from source` |
| Locale | User requested Colombia | Tone may need brand review | `verified from source` |

## Risks and Limits

- This output improves clarity and accessibility of writing; it does not test runtime accessibility.
- Brand tone and product UI labels should be checked before publishing.
- Reading level is an estimate because no readability tool was run.
