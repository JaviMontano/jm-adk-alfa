---
name: assembly-skill-meta
type: meta
version: 2.1.0
description: "Route one-skill quality pipeline requests."
---

# Assembly Skill — Meta Prompt

Activate only when the user wants to improve or certify one skill through the x-ray, surgeon, certify, and optional trigger pipeline.

Do not activate for non-skill assembly tasks such as decks, CI systems, manufacturing, packaging, or document collation.

## Skill Routing

1. Load `SKILL.md` and read `## When to Activate`.
2. If exactly one target skill is present, activate `assembly-skill-lead`.
3. If multiple skills are present, ask the user to select one.
4. If the request is only diagnostic, prefer quick mode.
