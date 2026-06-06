# Brand DOCX

Deterministic branded Microsoft Word generation for `.docx` artifacts with
real package validation, brand tokens, core properties, styled sections, tables,
and footer metadata. [CONFIG]

## Triggers

- "generate a Word document"
- "create a branded DOCX"
- "build a proposal in Word format"
- "make a brand-compliant report"
- "produce a cover page"
- "use python-docx"

## Assets

- `assets/activation-policy.json`: activation and routing rules.
- `assets/brand-docx-contract.json`: DOCX package contract and validator checks.
- `assets/fallback-brand-config.json`: deterministic fallback brand tokens.
- `assets/style-token-map.json`: token-to-Word-style mapping.
- `assets/evidence-policy.json`: evidence tag and validation report policy.

## Scripts

Run deterministic fixtures:

```bash
bash skills/brand-docx/scripts/check.sh
```

The check validates accepted DOCX packages and rejects HTML renamed as DOCX,
remote assets, unresolved placeholders, and legacy hardcoded colors. [CÓDIGO]

## Output

Return a saved `.docx` path plus validation evidence, or instructions only when
the user asks for a plan. Do not return HTML as DOCX.
