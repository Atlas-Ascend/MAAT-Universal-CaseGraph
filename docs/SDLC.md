# MAAT SDLC Control Plane

MAAT uses one promotion path from intent to production proof.

## Gates

1. **Discover / Define** — mission, users, use cases, constraints, acceptance criteria in `build-truth/01-05`.
2. **Design** — architecture, data model, agent contracts, tool boundaries in `build-truth/06-10` and `docs/ARCHITECTURE.md`.
3. **Implement** — deterministic CaseGraph pipeline, proof receipt engine, Strands integration boundary, API, and browser UI.
4. **Verify** — compile, lint, unit/API tests, 3+ acceptance fixtures, structural graph verification, and preflight.
5. **Secure** — untrusted-input boundary, no arbitrary execution, bounded cloud-agent route, security headers, input size limits.
6. **Package** — Python package metadata, pinned runtime baseline, Render blueprint, operational docs.
7. **Promote** — pull request only after CI PASS; merge SHA becomes deployment candidate.
8. **Deploy** — Render auto-deploys canonical `main`; `/health` and `/ready` are the runtime gates.
9. **Implement in production** — judge UI is served from the same FastAPI origin as `/build-case`; no disconnected prototype surface.
10. **Prove** — record CI run, merge SHA, Render deploy ID, live status, and endpoint verification in the promotion record.

## Release law

No stage inherits a PASS from an earlier stage. CI, merge, deployment, and live verification each require their own evidence.
