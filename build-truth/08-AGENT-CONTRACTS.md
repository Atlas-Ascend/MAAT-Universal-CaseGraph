# 08 — Agent Contracts

## Intake Agent
Extract candidate actors, facts, requirements, evidence, deadlines, and tasks. May not invent missing facts.

## Graph Agent
Converts normalized candidates into typed nodes/edges. Must preserve source traceability.

## Evidence Agent
Marks support, contradiction, uncertainty, and missing evidence. Must distinguish absence of evidence from contradiction.

## Planning Agent
Creates tasks and dependencies from graph state. Must state why a task is necessary.

## Action Router
Chooses bounded tool/action routes. Irreversible external actions require an explicit authorization policy.

## Verification Agent
Tests claimed outcomes and emits PASS/FAIL/UNVERIFIED rather than optimistic prose.
