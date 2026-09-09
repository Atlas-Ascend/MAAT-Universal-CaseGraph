# 07 — Data Model

## Node types
`person`, `organization`, `requirement`, `event`, `claim`, `evidence`, `risk`, `task`, `decision`, `constraint`, `artifact`.

## Edge types
`owns`, `requires`, `blocks`, `depends_on`, `supports`, `contradicts`, `changes`, `produces`, `verifies`, `precedes`, `relates_to`.

## Case invariants
- Every node has stable `id`, `type`, `label`, and `source_text`.
- Every edge references existing nodes.
- Every selected next action references one or more graph nodes.
- Every receipt records inputs, derived output, evidence references, and verification status.
