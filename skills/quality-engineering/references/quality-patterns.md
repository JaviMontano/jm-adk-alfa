# Quality Engineering Patterns

## Maturity Dimensions

Use the six canonical dimensions from `assets/maturity-model.json`:

1. test_strategy
2. test_automation
3. quality_gates_cicd
4. test_data_management
5. quality_metrics_dashboards
6. shift_left_practices

## Test Shapes

| Architecture | Shape | Distribution |
|---|---|---|
| monolith | test_pyramid | unit 55, integration 25, api 15, e2e 5 |
| microservices | test_diamond | unit 20, integration 40, contract 30, e2e 10 |
| event-driven | async_contract_shape | unit 20, integration 30, contract 25, event_schema 15, e2e 10 |
| frontend | test_trophy | unit 30, component 35, integration 20, e2e 15 |

## Gate Pattern

Commit, PR, release, and production gates are blocking. Nightly is async and must alert with an owner. Timeouts are part of the gate contract: an exceeded timeout fails blocking gates.

## Dashboard Pattern

Combine leading metrics that predict future quality with lagging metrics that show escaped risk. Coverage is useful only when paired with stability, flaky rate, review catch rate, incidents, MTTR, and regression rate.
