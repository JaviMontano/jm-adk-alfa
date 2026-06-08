# Cv Cover Optimizer

Optimizes CVs, resumes, and cover letters for ATS keyword coverage, target-role relevance, and JM Labs brand voice constraints.

## Triggers

- `cv-cover-optimizer`
- `optimizar-cv`
- `ats-cv`
- requests to tailor a CV, resume, hoja de vida, or cover letter to a job description

## Local Contract

The skill is deterministic when given a JSON packet:

```json
{
  "kind": "cv",
  "text": "candidate document text",
  "job_keywords": ["python", "stakeholder management"]
}
```

Run:

```bash
bash skills/cv-cover-optimizer/scripts/check.sh
python3 skills/cv-cover-optimizer/scripts/ats_lint.py --input packet.json
```

## Assets

- `assets/ats-keyword-policy.json`
- `assets/document-section-policy.json`
- `assets/brand-voice-policy.json`
- `assets/privacy-policy.json`
- `assets/output-contract.json`

## Safety

Do not invent achievements, employers, dates, education, certifications, or metrics. Proposed metrics must remain placeholders until the user confirms them.
