# MAAT — Devpost Draft

## Tagline
Turn chaos into an executable case.

## What it does
MAAT takes fragmented project or professional context and reconstructs it as a living Universal CaseGraph: actors, requirements, events, evidence, risks, tasks, dependencies, contradictions, and decisions. It then selects a next-best action and produces a proof receipt explaining why.

## Why it matters
Most AI assistants generate prose. MAAT changes the state representation of the problem so humans and agents can operate on the same explicit model.

## How it is built
Python, Strands Agents SDK, FastAPI, Pydantic, and an AWS/Bedrock model path. The core graph and receipt engine is deterministic and testable; the Strands layer performs model-driven extraction, reasoning, and bounded tool selection.

## Demo
Paste a deliberately messy project update. Press **BUILD CASE**. Watch the graph expose a changed requirement, schema risk, API dependency, evidence gap, and the next action required before deployment.

## What is next
AgentCore deployment, richer file ingestion, graph persistence, multi-case comparison, and permissioned action tools.
