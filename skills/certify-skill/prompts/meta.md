---
name: certify-skill-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Certify Skill skill routing."
---

# Certify Skill Meta Prompt

Activate this skill when the user request matches:

- certifying, validating, grading, or quality-gating a skill directory
- asking whether a skill is ready to ship
- re-certifying a skill after repair

Do not activate for employment certificates, legal certification, or generic
non-skill quality review. [EXPLICIT]

## Skill Routing

1. Load `assets/activation-policy.json`.
2. If match, activate `certify-skill-lead`.
3. If not match, route away and do not produce certification tables.
