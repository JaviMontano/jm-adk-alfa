# Example Input

Generate source-backed documentation for a small FastAPI service.

Available sources:

- `src/api.py` defines `GET /health` and `POST /tickets`.
- `README.md` exists but does not mention authentication.
- `openapi.json` defines request and response schemas for `/tickets`.
- `tests/test_api.py` covers health checks and ticket creation.

Requested output:

- refresh `README.md` for developers
- create `docs/api.md` for API consumers
- call out missing authentication details instead of inventing them
