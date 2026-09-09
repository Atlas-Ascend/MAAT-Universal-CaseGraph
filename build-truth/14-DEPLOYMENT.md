# 14 — Deployment

## Target
Containerized FastAPI service with a static or separate web client. Amazon Bedrock is the default hosted model path for the Strands agent; Bedrock AgentCore is an optional production runtime target.

## Environment
- Python 3.10+
- AWS credentials only for model-backed routes
- Deterministic `/build-case` path remains locally runnable

## Operational proof
Health check + sample case execution + receipt generation + CI PASS.
