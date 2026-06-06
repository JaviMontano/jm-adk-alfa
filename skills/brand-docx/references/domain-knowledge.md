# Domain Knowledge - Brand DOCX

## Overview

`brand-docx` creates deterministic Microsoft Word artifacts from explicit brand
tokens. The output should behave like a brand system applied to a Word
document, not a generic Markdown or HTML template saved with a `.docx`
extension.

## Best Practices

1. Resolve brand tokens before creating Word styles.
2. Declare all date/year values from caller input.
3. Write core properties for title, creator, and artifact date.
4. Use Word package parts and styles rather than HTML as a substitute.
5. Apply primary color to section dividers and table headers.
6. Use explicit fallback tokens when no brand config exists.
7. Validate package structure and XML before delivery.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|---|---|---|
| HTML renamed as DOCX | Word package contract is false | Generate a real DOCX ZIP package |
| Remote font URL | Breaks offline deterministic delivery | Use declared font names and fallbacks |
| Inferred date | Makes output time-dependent | Require caller-supplied `artifact_date` |
| Legacy hardcoded colors | Breaks brand determinism | Use active config or fallback tokens |
| Placeholder leakage | Shows incomplete template resolution | Validate for unresolved `{{...}}` |
