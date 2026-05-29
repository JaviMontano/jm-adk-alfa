<!--
generated-by: scripts/scaffold-skill.py
generated-for: official-source-verifier
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Official Source Verifier

Consult official sources (ADK, Agent Skills spec, GitHub/Git docs, framework docs) when a decision depends on them. Prioritizes official over secondary, cites source and date, records the change a finding justifies. Never elevates a secondary source to authority.

## Triggers

- official source
- verify docs
- adk spec
- authoritative reference
- source priority

## Allowed Tools

- Read
- Grep
- Glob
- WebFetch
- WebSearch

## Quick Use

Use this skill when the request clearly matches the triggers and requires the `official-source-verifier` capability.

## Output Format

Markdown with summary, evidence, result, validation, and risks.
