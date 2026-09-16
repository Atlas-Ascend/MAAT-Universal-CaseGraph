# MAAT — Universal CaseGraph

**Turn chaos into an executable case.**

MAAT transforms fragmented professional context into a typed, inspectable Universal CaseGraph and routes that state through evidence analysis, dependency planning, structural verification, and a proof receipt.

MAAT is also the implementation provider for **GARI CaseGraph Universal**, a research-graph projection that lets Ghost Atlas Research Institute visualize and inspect its canonical research objects without replacing GARI, LABCORE, THOTH, GARI-Provenance, VERITAS, or ProofGrid.

## Production shape

`messy context → graph → findings → plan → verify → receipt`

GARI research projection:

`research objects → typed graph → evidence state → contradictions → proof/memory lineage → next question`

The deterministic `/build-case` path is fully runnable without cloud credentials. The model-backed `/agent-analysis` route is an explicit Strands/Amazon Bedrock boundary and reports `503 not configured` until deployment authentication is supplied.

## Live surfaces

- `/` — judge-facing living CaseGraph interface
- `/gari` — **GARI CaseGraph Universal** visual research cockpit
- `/gari/research-graph` — typed GARI research-object → visual graph projection API
- `/gari/research-graph/demo` — bounded GARI Brain Cycle 001→002 demonstration graph
- `/health` — health + deployed version
- `/ready` — core readiness + agent-runtime + GARI CaseGraph state
- `/build-case` — deterministic command-to-proof API
- `/agent-analysis` — Strands/Bedrock analysis API
- `/docs` — OpenAPI interface

## GARI CaseGraph Universal law

The GARI projection uses the 24 canonical GARI research object types and preserves branch, program, status, E0→E7 evidence state, evidence grade, owner, version, source references, provenance, proof references, dependencies, related objects and typed research edges.

**Projection is not promotion.** CaseGraph renders and tracks research state; it does not become the canonical memory owner and it cannot raise a scientific evidence state merely because a node is visible.

Canonical research ownership remains with GARI / LABCORE / THOTH / GARI-Provenance and the applicable research branch. Proof identity remains with ProofGrid. Research evidence status remains with GARI-VERITAS.

## Repository control plane

- `build-truth/` — canonical Build Truth artifacts
- `docs/SDLC.md` — stage gates from definition to production proof
- `docs/ARCHITECTURE.md` — system topology and typed handoffs
- `docs/SECURITY.md` — trust boundaries and proof semantics
- `docs/OPERATIONS.md` — deployment and failure runbook
- `src/maat/` — implemented runtime
- `tests/` — unit, API, GARI research-graph, and acceptance matrix
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
