---
name: cv-cover-optimizer
version: 0.2.0
description: "Optimiza CV y carta de presentacion para ATS, rol objetivo y voz de marca con lint offline de keywords, secciones, longitud, contacto y tono."
owner: "JM Labs"
triggers:
  - cv-cover-optimizer
  - optimizar-cv
  - ats-cv
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Cv Cover Optimizer

## Purpose

Use this skill to improve a CV, resume, cover letter, or application packet against a target role. The skill produces ATS-aware edits, coverage gaps, brand-voice guardrails, and a deterministic validation result without inventing credentials.

## Inputs Expected

- Candidate CV or cover text.
- Target role, company, job description, or required keywords.
- Language preference and brand voice constraints.
- Permission boundary for editing files or returning proposed copy only.

## Outputs Expected

- Optimized CV or cover letter sections.
- ATS keyword coverage summary.
- Missing section/contact/length issues.
- Brand voice risks, including stacked trademarks or hustle framing.
- Validation command evidence from `scripts/ats_lint.py` when a machine-readable packet is provided.

## Procedure

### Discover

Identify the target role, source document type (`cv` or `cover`), required keywords, language, and whether the user wants direct edits or proposed text.

### Analyze

Compare source text against `assets/ats-keyword-policy.json`, `assets/document-section-policy.json`, `assets/brand-voice-policy.json`, and `assets/privacy-policy.json`.

### Execute

Rewrite only the requested sections. Preserve facts, seniority, dates, employers, credentials, and contact details. Do not invent metrics; mark suggested metrics as placeholders.

### Validate

Run `bash skills/cv-cover-optimizer/scripts/check.sh` for fixture coverage. For a specific JSON packet, run:

```bash
python3 skills/cv-cover-optimizer/scripts/ats_lint.py --input <packet.json>
```

## Assets

- `assets/ats-keyword-policy.json`
- `assets/document-section-policy.json`
- `assets/brand-voice-policy.json`
- `assets/privacy-policy.json`
- `assets/output-contract.json`

## Quality Criteria

- Recommendations are grounded in source text and target role evidence.
- ATS gaps identify missing keywords without keyword stuffing.
- CV output includes recognizable experience, education, skills, or achievement sections.
- Cover output stays concise and avoids generic flattery.
- Contact/PII handling is explicit and privacy-safe.
- Claims about candidate experience are not invented.

## Edge Cases

- No job description: produce a blocked or partial optimization and ask for role evidence.
- Minimal CV: focus on structure and missing data rather than fabricating content.
- Conflicting brand tone: preserve user preference and mark unresolved conflicts.
- Sensitive personal data: avoid exposing direct contact details in examples or fixtures.
- Cover letter over length: prioritize evidence-backed value and remove repetition.

## Scripts

`scripts/ats_lint.py --input <json>` lints CV/cover packets for ATS keyword coverage, section presence, length, contact, stacked trademarks, and hustle language. `scripts/check.sh` runs deterministic valid and invalid fixtures offline.

## Related Skills

- `cv-transformer`
- `brand-voice`
- `gratitud-post-proceso`

## Evidence Requirements

- Cite source document, job description, or user-provided constraints for every substantive recommendation.
- Mark inferred gaps as assumptions when the target role evidence is incomplete.

## Update-Safety Notes

- Default to proposed copy unless file-edit authority is explicit.
- Never overwrite the source CV or cover letter without explicit confirmation.
- Keep placeholders visibly marked when a metric or detail needs user confirmation.
