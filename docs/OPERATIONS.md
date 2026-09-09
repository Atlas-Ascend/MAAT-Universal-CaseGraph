# MAAT Operations Runbook

## Public runtime

- `GET /` — judge-facing Universal CaseGraph UI.
- `GET /health` — process health and version.
- `GET /ready` — deterministic core readiness plus model-runtime configuration state.
- `POST /build-case` — deterministic command-to-proof path; requires no AWS credentials.
- `POST /agent-analysis` — Strands/Amazon Bedrock path; returns HTTP 503 when cloud auth is not configured rather than failing ambiguously.
- `GET /docs` — generated FastAPI API documentation.

## Deployment

Canonical production source is `main`. Render builds with `pip install -e .` and starts `uvicorn maat.api:app --host 0.0.0.0 --port $PORT`.

## Promotion checks

1. GitHub CI passes on Python 3.11 and 3.12.
2. Merge candidate is the exact CI-proven head SHA.
3. Render reports the merged commit as `live`.
4. `/health` returns `status=ok` and the expected version.
5. `/build-case` produces a PASS receipt with zero verification errors.

## Failure route

A failed CI run returns to implementation. A failed Render build or update does not change the proof state to deployed. A missing AWS credential keeps only `/agent-analysis` unavailable; the deterministic core remains operational.
