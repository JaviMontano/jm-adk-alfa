<!--
generated-by: scripts/scaffold-skill.py
generated-for: input-analysis
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Input Analysis

Parse project inputs (RFPs, briefs, emails). Detect contradictions, gaps, ambiguities. Score completeness 0-100. [EXPLICIT]

## Triggers

- input-analysis

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Use this skill when a project input (RFP, brief, email, notes, or mixed source packet) must be parsed before planning or implementation. Extract requirements, constraints, contradictions, gaps, and ambiguities; tag every finding with evidence; score completeness from 0 to 100; and add a warning when assumptions exceed 30%.

Consult `assets/manifest.json` for deterministic contracts and validate JSON reports with `bash skills/input-analysis/scripts/check.sh`.

## Output Format

Markdown or JSON with summary, evidence-tagged findings, contradiction/gap/ambiguity tables, completeness score, validation, and risks.
