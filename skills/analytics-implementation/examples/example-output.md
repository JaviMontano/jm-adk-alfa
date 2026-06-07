# Example Output

## Summary

`Atlas Commerce` should implement GA4/Firebase Analytics across web, mobile, and backend with privacy-safe event contracts, a BigQuery export, and Looker Studio reporting readiness.

## GA4 And Firebase Setup

| Surface | Tool | Owner | Validation |
|---|---|---|---|
| web app | GA4 web stream | Web Analytics | DebugView plus Realtime event receipt |
| iOS app | Firebase Analytics | Mobile Analytics | Firebase DebugView |
| Android app | Firebase Analytics | Mobile Analytics | Firebase DebugView |
| backend order service | Measurement Protocol | Backend Analytics | BigQuery row check |

## Event Contracts

| Event | Trigger | Owner | Parameters | Validation |
|---|---|---|---|---|
| `account_created` | Account creation succeeds | Growth Analytics | `event_id`, `user_id`, `anonymous_id`, `plan_type` | DebugView |
| `checkout_started` | User starts checkout | Commerce Analytics | `event_id`, `user_id`, `cart_id` | DebugView |
| `purchase_completed` | Order is persisted | Commerce Analytics | `event_id`, `user_id`, `order_id`, `value` | BigQuery row check |

## Conversion And Export

- Mark `purchase_completed` as a conversion after event receipt is validated.
- Enable daily BigQuery export to an owned dataset.
- Partition export-derived marts by event date.
- Exclude raw email, phone, address, and card data.
