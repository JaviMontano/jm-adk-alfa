# Example Output

## Summary

La solicitud queda lista para firmar un PDF legal con salida nueva, ancla verificable y evidencia de render. [CONFIG]

## Files

- source_pdf: `contrato-laboral.pdf` [CONFIG]
- signature_png: `firma-jm.png` [CONFIG]
- output_pdf: `contrato-laboral-firmado.pdf` [CONFIG]
- verification_png: `contrato-laboral-firmado.verify.png` [INFERENCIA]

## Placement

- anchor: `Firma del trabajador` [CONFIG]
- mention: `Leida y aprobada` [CONFIG]
- strategy: anchor text; block if the anchor is not found [CONFIG]

## Validation

```bash
python3 skills/firma-pdf-legal/scripts/signature_packet_lint.py --input signing-packet.json
```

## Risks

- La skill valida manipulacion de archivo y evidencia; no confirma validez legal del documento ni sustituye revision experta. [CONFIG]
