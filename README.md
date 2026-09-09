# MAAT — Universal CaseGraph

**Turn chaos into an executable case.**

MAAT transforms fragmented professional context into a typed, inspectable Universal CaseGraph and routes that state through evidence analysis, dependency planning, structural verification, and a proof receipt.

## Production shape

`messy context → graph → findings → plan → verify → receipt`

The deterministic `/build-case` path is fully runnable without cloud credentials. The model-backed `/agent-analysis` route is an explicit Strands/Amazon Bedrock boundary and reports `503 not configured` until deployment authentication is supplied.

## Live surfaces

- `/` — judge-facing living CaseGraph interface
- `/health` — health + deployed version
- `/ready` — core readiness + agent-runtime state
- `/build-case` — deterministic command-to-proof API
- `/agent-analysis` — Strands/Bedrock analysis API
- `/docs` — OpenAPI interface

## Repository control plane

- `build-truth/` — 16 canonical Build Truth artifacts
- `docs/SDLC.md` — stage gates from definition to production proof
- `docs/ARCHITECTURE.md` — system topology and typed handoffs
- `docs/SECURITY.md` — trust boundaries and proof semantics
- `docs/OPERATIONS.md` — deployment and failure runbook
- `src/maat/` — implemented runtime
- `tests/` — unit, API, and acceptance matrix
- `examples/` — representative case fixtures
- `scripts/preflight.py` — release invariant check
- `render.yaml` — reproducible Render service definition
- `proof/` — execution evidence only; no aspirational completion claims

## Development

```bash
python -m pip install -e '.[dev]'
ruff check src tests scripts
pytest -q
python scripts/preflight.py
uvicorn maat.api:app --reload
```

## Release law

A feature is not deployed because code exists. Promotion requires: **CI PASS → reviewed merge SHA → Render LIVE → endpoint verification → recorded receipt**.

## Current lifecycle

**ACTIVE / IMPLEMENTED / PRODUCTION-HARDENING**
