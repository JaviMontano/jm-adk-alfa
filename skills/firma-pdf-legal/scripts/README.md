# Firma Pdf Legal Scripts

## `signature_packet_lint.py`

Validates deterministic JSON evidence packets for PDF signing work. It does not inspect private PDF bytes and does not call network services.

```bash
python3 skills/firma-pdf-legal/scripts/signature_packet_lint.py --input skills/firma-pdf-legal/scripts/fixtures/valid-anchored-signature.json
```

## `sign_pdf.py`

Optional operational signer that requires PyMuPDF. It writes a new PDF and a verification PNG when real files are available.

## `check.sh`

Runs valid and invalid JSON fixtures through the offline validator.
