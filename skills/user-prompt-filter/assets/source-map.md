# User Prompt Filter Source Map

| Source | Consumed By | Purpose |
|---|---|---|
| `assets/filter-input-schema.json` | `scripts/filter-prompt.py`, `SKILL.md` | Required input contract |
| `assets/threat-taxonomy.json` | `scripts/filter-prompt.py`, `knowledge/body-of-knowledge.md` | Threat classes and evidence patterns |
| `assets/risk-scoring-policy.json` | `scripts/filter-prompt.py`, `SKILL.md` | Decision and severity thresholds |
| `assets/sanitization-policy.json` | `scripts/filter-prompt.py`, `references/domain-knowledge.md` | Redaction and prompt transformation |
| `assets/output-schema.json` | `scripts/filter-prompt.py`, `templates/output.md` | Output structure |
| `scripts/fixtures/*.json` | `scripts/check.sh` | Positive and adversarial validation |
