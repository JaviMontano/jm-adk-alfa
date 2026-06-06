---
name: session-start-bootstrap-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic session startup behavior."
---

# Session Start Bootstrap - Self-Improvement

## Evaluate

1. Do startup packets catch dirty trees and open PRs before writes?
2. Are context sources minimal and listed?
3. Do fixtures reject missing environment and missing first action?
4. Are conflicting instructions resolved by source precedence?
5. Are stale handoffs verified against current git/PR evidence?

## Improve

1. Add fixtures for every repeated unsafe startup failure.
2. Tighten source precedence before adding prose exceptions.
3. Keep scripts offline and free of wall-clock, network, or random inputs.

## Trigger

Run this meta-prompt when a session starts with wrong repo, wrong branch,
missing guardrails, or unsafe writes.
