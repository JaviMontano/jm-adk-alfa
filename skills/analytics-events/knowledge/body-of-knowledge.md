# Analytics Events Body of Knowledge

## Canon

Analytics event design converts product behavior into a stable instrumentation contract. A good event has a clear trigger, owner, destination, property schema, identity behavior, privacy posture, QA method, and downstream use case.

## Naming

- Use lower snake_case.
- Prefer object_action, such as `checkout_started`, `purchase_completed`, or `workspace_invited`.
- Avoid vague names like `click`, `submit`, `success`, `error`, and `page_view` unless the object is explicit.
- Keep tense consistent: event names describe facts that happened.

## Properties

- Every property needs name, type, description, requirement status, and PII classification.
- Prefer stable ids over raw personal data.
- Use enum properties only when allowed values are known.
- Avoid embedding JSON blobs unless the downstream tool supports object properties intentionally.

## Identity

- Anonymous activity requires `anonymous_id`.
- Authenticated activity requires `user_id` when available.
- Profile merge behavior must be explicit.
- Event deduplication should use `event_id` or an equivalent deterministic key.

## QA

- Validate schema in development.
- Verify destination receipt for every destination.
- Test identity merge flows.
- Run negative checks for blocked PII.
- Preserve event aliases during migration with deprecation dates.
