# Example Input

Design an AI pipeline architecture for a regulated fraud scoring system.

Context:

- batch training uses transaction history and label files
- online inference must score authorization requests in near real time
- features are reused by three models
- a model registry does not exist yet
- promotion must support shadow/canary validation before production
- requirements include availability, drift detection, audit trail, and rollback
