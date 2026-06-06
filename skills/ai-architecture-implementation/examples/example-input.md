# Example Input — AI Architecture Implementation

Create a production implementation plan for `claims-risk-ai`.

Known context:

- Approved architecture exists for a batch + online scoring ML system.
- Audit finding F-001 requires drift monitoring; F-002 requires Blue & Gold CI/CD.
- Team uses Python, containers, GitHub Actions, and Kubernetes.
- Data source is claims events from PostgreSQL.
- Required controls: model registry, reproducible training, serving API, rollback, drift alerts, and runbooks.

Mode: remediation. Scope: full. Format: hybrid. Do not write production code; produce the phased implementation plan and validation packet.
