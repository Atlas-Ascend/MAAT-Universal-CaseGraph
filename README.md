# MAAT — Universal CaseGraph

**Turn chaos into an executable case.**

MAAT is a hackathon-grade agentic system that transforms unstructured human situations—notes, requirements, messages, evidence, deadlines, actors, conflicts, and dependencies—into a living **Universal CaseGraph** with explicit next actions and proof receipts.

## Mission

MAAT converts ambiguity into computable state:

`messy input → entities → events → evidence → contradictions → risks → tasks → dependencies → next-best action → receipt`

## Competition Build

This repository is the standalone competition implementation of the Ghost Atlas Universal CaseGraph doctrine. It is intentionally scoped as a new, independently auditable build rather than a replacement for the larger Ghost Atlas estate.

## Core Runtime

- Strands-based agent orchestration
- Universal CaseGraph domain model
- Evidence and contradiction analysis
- Dependency-aware planning
- Action routing
- Proof receipts
- Living graph UI
- SECA-style verification gate

## Command-to-Proof Loop

1. **INGEST** — accept messy human context.
2. **NORMALIZE** — identify actors, claims, requirements, evidence, events, and constraints.
3. **GRAPH** — construct typed nodes and relationships.
4. **REASON** — detect contradictions, missing evidence, blockers, and risk.
5. **PLAN** — generate dependency-aware tasks and next-best action.
6. **ACT** — invoke bounded tools or produce an executable handoff.
7. **VERIFY** — test whether the claimed action/result is supported.
8. **RECEIPT** — emit machine-readable proof.

## Repository Map

- `build-truth/` — 16 canonical Build Truth files
- `docs/` — architecture, judging, disclosure, and demo documentation
- `src/` — agent, graph, ingest, evidence, planning, tools, and API packages
- `web/` — living CaseGraph interface
- `tests/` — contract and acceptance tests
- `proof/` — run receipts, graph snapshots, and verification evidence

## Hackathon Definition of Done

A judge can press **BUILD CASE**, provide deliberately messy source material, and watch MAAT:

- construct the graph,
- identify contradictions,
- expose missing evidence,
- derive dependencies,
- choose a next-best action,
- execute or route that action,
- and produce a proof receipt.

## Status

**ACTIVE — Hackathon 10 / competition build seed**

See `build-truth/16-DEFINITION-OF-DONE.md` for the acceptance gate.
