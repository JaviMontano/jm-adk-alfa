# Example Output

## Summary

`Atlas Commerce` should standardize analytics events around lower snake_case object_action names, shared identity rules, and destination-specific QA checks.

## Events

| Event | Domain | Trigger | Owner | Platforms |
|---|---|---|---|---|
| `account_created` | activation | Account creation succeeds | Growth Analytics | web, iOS, backend |
| `workspace_invited` | activation | Invite is sent to a workspace member | Growth Analytics | web, backend |
| `cart_viewed` | checkout | Cart page or cart drawer is displayed | Commerce Analytics | web, iOS |
| `checkout_started` | checkout | User starts checkout from cart | Commerce Analytics | web, iOS |
| `payment_submitted` | checkout | Payment submission request is accepted by backend | Commerce Analytics | backend |
| `purchase_completed` | checkout | Order is confirmed by backend | Commerce Analytics | backend |

## Required Properties

| Property | Type | Required | PII | Description |
|---|---|---|---|---|
| `event_id` | string | yes | none | Deterministic event id for deduplication |
| `anonymous_id` | string | yes | none | Anonymous visitor identifier |
| `user_id` | string | no | low | Authenticated user identifier after login |
| `workspace_id` | string | no | low | Workspace identifier |
| `order_id` | string | no | low | Order identifier |
| `value` | number | no | none | Order value in reporting currency |

## Identity Policy

- Preserve `anonymous_id` before signup.
- Attach `user_id` after authentication.
- Merge anonymous and authenticated profiles only after `account_created`.
- Never send raw email, phone, address, or card fields to analytics destinations.

## Validation

- Naming policy: lower snake_case object_action.
- Property policy: every event references known properties.
- Identity policy: anonymous and authenticated identifiers are defined.
- Tracking plan: each event has destination, owner, and QA method.
- Privacy policy: sensitive fields are excluded or require review.
