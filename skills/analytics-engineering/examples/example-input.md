# Example Input

Design an analytics engineering plan for the `Atlas Commerce` warehouse.

Context:
- Sources are `stripe.payments`, `stripe.subscriptions`, `salesforce.accounts`, and `app.events`.
- Finance needs a certified `fct_revenue` mart refreshed hourly.
- Product needs session metrics from 900M monthly events with late arrivals up to 72 hours.
- Existing transformations are scattered SQL files with no enforced contracts.
- The team uses dbt Core on Snowflake and wants slim CI on pull requests.

Required output:
- Source-to-target mapping.
- Model layers with names, grain, owners, and materializations.
- Required tests and data contracts.
- Lineage from sources to marts.
- Documentation and validation plan.
- Risks, assumptions, and open questions.
