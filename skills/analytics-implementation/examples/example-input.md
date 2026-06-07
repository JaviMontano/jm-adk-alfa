# Example Input

Plan analytics implementation for `Atlas Commerce`.

Context:
- Platforms: web app, iOS app, Android app, backend order service.
- Tools: GA4, Firebase Analytics, BigQuery export, Looker Studio.
- Events needed: `account_created`, `checkout_started`, `purchase_completed`.
- Conversion: `purchase_completed`.
- User properties: `plan_type`, `account_tier`.
- Constraint: do not send raw email, phone, address, or card data.

Required output:
- GA4/Firebase setup
- custom event contracts
- conversion setup
- user properties
- BigQuery export plan
- Looker Studio dashboard source
- implementation steps and QA
