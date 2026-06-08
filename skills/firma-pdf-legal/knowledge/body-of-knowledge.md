# Firma Pdf Legal Body of Knowledge

## Stable Rules

- A legal PDF signing workflow must preserve the original file and write a new output path by default.
- The signature image must be user-supplied; the skill must not synthesize or imitate a person's signature.
- Anchor text placement is safer than absolute coordinates because it ties the operation to document content.
- Render verification proves that the edited PDF can be opened and visually inspected after insertion.
- Hashes make source and render evidence reproducible without embedding private files in reports.

## Determinism Boundaries

- Offline validators check packets, hashes, anchor status, placement bounds, consent, and evidence shape.
- Operational PDF editing may depend on PyMuPDF, but DoD fixtures must not depend on network or external services.
- Wall-clock timestamps, random filenames, remote certificate checks, and live legal status lookups are outside the deterministic check.

## Risk Signals

| Signal | Required Response |
|---|---|
| Missing anchor | Block and report anchor not found |
| Multiple anchors | Ask for page or occurrence selector |
| Missing consent | Block execution |
| Overwrite requested | Default to new output and ask for explicit confirmation |
| Legal interpretation requested | Mark as legal-review risk |
