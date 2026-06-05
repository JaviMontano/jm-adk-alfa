---
name: user-prompt-filter-meta
type: meta
version: 2.1.0
description: "Meta-prompt for routing and critiquing prompt filter outputs."
---

# User Prompt Filter - Meta Prompt

Activate this skill only for pre-execution prompt filtering, sanitization,
classification, or routing. Reject normal content moderation and post-output
safety review unless the user explicitly asks to gate an incoming prompt.

## Critique Checklist

- Decision maps to a taxonomy rule.
- Secret-like evidence is redacted.
- Sanitized prompt preserves benign intent when possible.
- Downstream constraints are explicit.
- Filter output does not grant runtime permissions.
