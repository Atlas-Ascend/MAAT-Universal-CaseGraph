# 06 — Architecture

## Components
1. Intake/normalization
2. CaseGraph builder
3. Evidence and contradiction reasoner
4. Dependency planner
5. Strands agent orchestrator
6. Action router
7. Verification gate
8. Receipt emitter
9. FastAPI surface
10. Living CaseGraph UI

## Control law
No action is promoted as complete without evidence. Agent output is advisory until converted into structured graph mutations or a receipt-backed action result.

See `docs/ARCHITECTURE.md` for the full flow.
