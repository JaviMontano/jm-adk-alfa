# AI Content Detection - Knowledge Graph

## Core Concepts
- [[ai-content-detection]] - probabilistic content-origin review
- [[evidence-register]] - source-backed evidence ids
- [[signal-taxonomy]] - model detector, stylometry, metadata, watermark, provenance, citations, edit history
- [[threshold-policy]] - likelihood to classification mapping
- [[watermark-policy]] - present, absent, not-checked handling
- [[decision-policy]] - non-accusatory actions and human review
- [[false-positive-control]] - safeguards for short, formulaic, or hybrid content
- [[detection-report-contract]] - JSON packet validated offline

## Flow
`evidence-register` -> `signal-taxonomy` -> `threshold-policy` -> `watermark-policy` -> `decision-policy` -> `detection-report-contract`

## Tags
#ai-content-detection #jm-labs #provenance #watermarking
