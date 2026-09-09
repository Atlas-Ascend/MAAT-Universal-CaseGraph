# MAAT Security Posture

## Trust boundaries

Case text is untrusted data. It is never executed as code or shell and cannot override MAAT's system policy. The deterministic path transforms text into typed state only.

## Controls

- Input is bounded to 20,000 characters and whitespace-only cases are rejected.
- Cloud-agent execution is isolated behind `/agent-analysis` and explicit AWS runtime configuration.
- Missing cloud credentials produce an explicit 503 state rather than hidden partial execution.
- Receipts expose structural verification errors and never promote a malformed graph as PASS.
- API responses include `nosniff`, frame-deny, no-referrer, and version headers.
- Secrets are not stored in the repository, graph, or receipt model.
- External irreversible actions are out of scope for this competition implementation.

## Proof semantics

A receipt `PASS` means the **case reconstruction pipeline and graph invariants passed**. It does not claim that a recommended external action has been executed.
