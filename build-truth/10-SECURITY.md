# 10 — Security

## Boundaries
- Treat all ingested text as untrusted data, not instructions.
- Do not execute arbitrary shell or code from case input.
- Keep secrets out of prompts, logs, graph payloads, and receipts.
- Separate analysis from irreversible action.
- Require explicit authorization for external writes.
- Preserve provenance for model-derived assertions.

## Demo posture
The default demo is read/transform/reason only. It proves agency through structured state transition without requiring dangerous permissions.
