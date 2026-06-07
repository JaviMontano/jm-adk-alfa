# Analytics Events Knowledge Graph

## Core Nodes

- `analytics-events`: event taxonomy and tracking plan capability.
- `taxonomy`: product domains and event groups.
- `event`: named behavior with trigger, action, owner, and platforms.
- `property`: typed event attribute with PII classification.
- `identity-policy`: anonymous id, user id, merge behavior, and deduplication key.
- `tracking-plan`: destination, implementation owner, QA method, and rollout phase.
- `privacy-policy`: sensitive data handling and review.
- `deterministic-oracle`: local validator and fixtures.

## Required Edges

- `taxonomy` groups `event`.
- `event` references `property`.
- `event` is governed by `identity-policy`.
- `tracking-plan` implements `event`.
- `privacy-policy` validates `property`.
- `deterministic-oracle` verifies the full contract.
