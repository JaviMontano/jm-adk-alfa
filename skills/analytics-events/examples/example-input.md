# Example Input

Design an analytics event taxonomy and tracking plan for `Atlas Commerce` onboarding and checkout.

Context:
- Platforms: web app, iOS app, backend order service.
- Destinations: Segment, Amplitude, Snowflake.
- Journeys: account created, workspace invited, cart viewed, checkout started, payment submitted, purchase completed.
- Identity: anonymous visitors become users after account creation.
- Constraint: do not send raw email, phone, address, or card data to analytics destinations.

Required output:
- canonical event names
- triggers
- owners
- required properties
- identity policy
- tracking plan by destination
- privacy review notes
- QA and validation plan
