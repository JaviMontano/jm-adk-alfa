---
name: ai-content-detection-primary
type: execution
version: 2.1.0
description: "Execute deterministic AI Content Detection with evidence-backed likelihood reporting."
triad:
  lead: "ai-content-detection-lead"
  support: "ai-content-detection-support"
  guardian: "ai-content-detection-guardian"
---

# AI Content Detection - Execute

## Dynamic Parameters
| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{content}}` | Content excerpt, metadata, or packet | Yes | User input |
| `{{review_purpose}}` | Editorial / compliance / education / moderation / policy | Yes | User input |
| `{{evidence}}` | Detector output, watermark output, provenance, metadata | No | User input |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | markdown / json / both | No | Auto |

## Execution
1. Load `knowledge/body-of-knowledge.md`.
2. Load assets: signal taxonomy, thresholds, evidence, watermark, decision policy, and report contract.
3. Lead establishes scope and registers evidence.
4. Lead scores available signals and computes likelihood.
5. Support checks false-positive, threshold, and decision-policy risks.
6. Guardian validates evidence, classification, watermark, authorship claim, and final action.
7. For JSON output, validate with `scripts/validate_ai_content_detection_report.py` when a packet is available.

## Output
- Content scope and evidence register.
- Signal table with score, weight, direction, and evidence.
- Likelihood assessment with limitations.
- Watermark/provenance status.
- Human-AI strategy and safe decision policy.
- Risks and validation status.
