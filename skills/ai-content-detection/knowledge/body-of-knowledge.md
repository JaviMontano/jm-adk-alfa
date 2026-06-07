# AI Content Detection - Body of Knowledge

## Canon
AI content detection is probabilistic. A responsible report weighs multiple
signals, records evidence, applies thresholds consistently, documents limits,
and avoids unsupported authorship or intent claims.

## Signal Types
| Signal | Meaning | Risk |
|--------|---------|------|
| model-detector | output from a detector tool or classifier | calibration and domain drift |
| stylometry | linguistic regularity, burstiness, perplexity-like indicators | false positives for formulaic or non-native writing |
| metadata | creation/edit metadata, timestamps, tool markers | missing or tampered metadata |
| watermark | explicit watermark/provenance marker | tool compatibility and removal |
| provenance | source chain, disclosures, signed records | incomplete chain of custody |
| citation-integrity | source citation consistency | source absence is not AI proof |
| edit-history | drafts, revisions, comments, authorship workflow | unavailable or private records |

## Classification Policy
- `likely-ai`: likelihood >= 0.80.
- `mixed`: 0.55 <= likelihood < 0.80.
- `likely-human`: likelihood <= 0.25.
- `inconclusive`: all other ranges or insufficient/conflicting evidence.

## Safety Rules
- Never identify a person as the AI user or author.
- Never recommend automatic punishment from detector output alone.
- Require human review for education, employment, moderation, compliance, or legal contexts.
- Treat watermark `present` as evidence-backed only.
- Treat short samples as low confidence unless provenance is strong.

## Offline Validation
`scripts/validate_ai_content_detection_report.py` validates the JSON packet,
signal evidence, thresholds, authorship claim, watermark evidence, decision
policy, and validation checks without network access.
