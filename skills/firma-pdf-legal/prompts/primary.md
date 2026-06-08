# Firma Pdf Legal Primary Prompt

## Objective

Sign or prepare a signing packet for a legal PDF while preserving the source file, using a user-supplied signature image, and producing deterministic verification evidence.

## Required Inputs

- Source PDF path.
- Signature PNG path.
- Output PDF path.
- Anchor text and optional mention.
- Explicit consent and source-preservation preference.

## Process

1. Confirm inputs and consent.
2. Apply assets policies for placement, evidence, legal limits, and output shape.
3. Run the operational signer only when files and dependencies are available.
4. Validate packet evidence with `scripts/signature_packet_lint.py`.
5. Report result, validation, and risks.

## Output

Return a concise packet with summary, files, placement, evidence, validation commands, and risks.
