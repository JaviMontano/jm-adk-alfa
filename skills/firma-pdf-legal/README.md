# Firma Pdf Legal

`firma-pdf-legal` signs a legal PDF with a user-supplied transparent PNG signature, places it at an anchor line, writes a new output PDF, and records render evidence.

## Deterministic Contract

- Preserve the source PDF.
- Use a stable anchor, page, rectangle, and mention policy.
- Record source PDF hash, signature PNG hash, verification PNG path, and render hash.
- Block if consent, anchor, render proof, or hashes are missing.
- Keep legal interpretation outside the automation result.

## Local Validation

```bash
bash skills/firma-pdf-legal/scripts/check.sh
python3 skills/firma-pdf-legal/scripts/signature_packet_lint.py --input skills/firma-pdf-legal/scripts/fixtures/valid-anchored-signature.json
```

## Assets

- `assets/signature-placement-policy.json`
- `assets/evidence-policy.json`
- `assets/render-verification-policy.json`
- `assets/legal-boundary-policy.json`
- `assets/output-contract.json`
