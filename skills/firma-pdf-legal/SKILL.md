---
name: firma-pdf-legal
version: 0.2.0
description: "Coloca firma manuscrita sobre una linea legal de PDF usando ancla verificable, salida nueva, render de evidencia y contrato offline deterministico."
owner: "JM Labs"
triggers:
  - firma-pdf-legal
  - firmar-pdf
  - sign-pdf
  - firmar contrato pdf
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Firma Pdf Legal

## Purpose

Use this skill when a user needs to place a supplied handwritten signature image on a legal PDF at a specific anchor line, add an optional acknowledgement mention, preserve the source file, and produce renderable verification evidence. The skill supports operational signing through `scripts/sign_pdf.py` when PyMuPDF is available and validates deterministic signing packets offline through `scripts/signature_packet_lint.py`.

## Inputs Expected

- Source PDF path, output PDF path, and transparent PNG signature path.
- Anchor text that identifies the intended signature line, such as `Firma del trabajador`.
- Optional mention text, for example `Leida y aprobada`.
- User confirmation that the signature image may be applied to a new output file.
- Any legal-review boundary or instruction to stop instead of executing.

## Outputs Expected

- New signed PDF path; never overwrite the source PDF by default.
- Verification PNG path and render hash when available.
- Placement packet with anchor, page, rectangle, mention, source hashes, and evidence.
- Validation status from `scripts/signature_packet_lint.py` for machine-readable packets.
- Risks and limits, including when legal review or missing consent blocks execution.

## Procedure

### Discover

Confirm the source PDF, signature image, target anchor, desired output file, and whether the user authorizes signing. If a legal interpretation is requested, scope the answer to document handling and recommend expert review.

### Analyze

Check `assets/signature-placement-policy.json`, `assets/evidence-policy.json`, `assets/legal-boundary-policy.json`, and `assets/render-verification-policy.json` before choosing a placement strategy.

### Execute

Create a new output PDF only. Prefer anchor text placement. Add the mention only if the user asked for it or the task requires it. Do not create, imitate, or alter a person's signature image.

### Validate

For a signing packet, run:

```bash
python3 skills/firma-pdf-legal/scripts/signature_packet_lint.py --input <packet.json>
```

For the deterministic fixture suite, run:

```bash
bash skills/firma-pdf-legal/scripts/check.sh
```

If PyMuPDF is installed and the user supplied real files, the operational command is:

```bash
python3 skills/firma-pdf-legal/scripts/sign_pdf.py --pdf <input.pdf> --signature <signature.png> --out <signed.pdf> --anchor "Firma" --mention "Leida y aprobada"
```

## Assets

- `assets/signature-placement-policy.json`
- `assets/evidence-policy.json`
- `assets/render-verification-policy.json`
- `assets/legal-boundary-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- The source PDF is preserved and output goes to a new path.
- The signature image is user-supplied and consent is explicit.
- Anchor search is verified; missing anchors produce a blocked result.
- Placement evidence includes page, rectangle, anchor, source hashes, rendered PNG, and render hash.
- No network, current time, random IDs, external certificate lookup, or mutable legal claim is required for validation.
- Legal advice is not provided; legal uncertainty is reported as a risk.

## Edge Cases

- Missing anchor: stop with a deterministic error and do not write a signed PDF.
- Multiple anchors: require a page or occurrence selector before execution.
- No consent or unclear authority: block execution and request confirmation.
- Request to overwrite the original file: refuse by default and propose a new output path.
- Signature image is not supplied by the user: do not synthesize one.
- Mention text is too long or changes legal meaning: block or return for legal review.

## Scripts

`scripts/signature_packet_lint.py --input <json>` validates signing evidence packets for hashes, source preservation, consent, anchor placement, rendered verification, and deterministic evidence. `scripts/check.sh` runs valid and invalid fixtures offline. `scripts/sign_pdf.py` is the optional operational signer when PyMuPDF is available.

## Related Skills

- `firma-pdf-legal`
- `validar-liquidacion-co`
- `proceso-seleccion-orchestrator`

## Evidence Requirements

- Cite the user-supplied source paths, hashes, anchor text, and verification render when claiming a PDF was signed.
- Mark missing legal authority, missing files, or unavailable render verification as blockers.
- Keep claims evidence-tagged in host environments that require evidence tags.

## Update-Safety Notes

- Never overwrite the original PDF without explicit, separate confirmation.
- Keep examples and fixtures synthetic.
- Do not add network checks, live certificate validation, or wall-clock timestamps to deterministic validation.
