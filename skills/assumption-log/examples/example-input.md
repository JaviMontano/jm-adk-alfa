# Example Input

Create an assumption log for the payment onboarding modernization.

Context:

- Product believes enterprise customers can finish onboarding without assisted
  data migration.
- `services/events/onboarding.py` contains `account_created` and
  `data_import_completed` events.
- ADR-003 approves Supabase for operational analytics.
- A planning note still says Firebase is the only allowed persistence layer.
- The launch plan says Marketing owns localized copy, but no freeze date is
  listed.

Existing decisions:

- `DL-014`: decide whether assisted migration remains in launch scope.
- `ADR-003`: authorize Supabase for operational analytics.
