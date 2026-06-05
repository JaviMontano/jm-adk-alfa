---
name: assumption-log-meta
type: meta
version: 2.0.1
description: "Meta-prompt for Assumption Log routing."
---

# Assumption Log Meta Prompt

Use `assets/activation-policy.json` and `SKILL.md ## When To Activate` before
activating this skill.

Activate for assumption registers, assumption validation, hypothesis tracking,
evidence-gap tracking, contradiction review, and decision-linked assumption
management.

Do not activate for statistical assumptions, weather, generic logging,
certificate documents, or unrelated summaries. If the request is ambiguous,
return `needs_clarification` with the minimum missing input.
