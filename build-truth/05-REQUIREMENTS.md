# 05 — Requirements

## Functional
- Accept plain text input.
- Normalize sentences into typed case nodes.
- Represent typed edges between nodes.
- Detect missing evidence and obvious conflicts/blockers.
- Generate dependency-aware tasks.
- Rank a next-best action.
- Emit a machine-readable proof receipt.
- Expose the process through an API and visual UI.
- Include a Strands agent integration path.

## Quality
- Deterministic core tests must run without cloud credentials.
- Model-backed behavior must be bounded behind explicit agent invocation.
- Every recommendation must reference graph state.
