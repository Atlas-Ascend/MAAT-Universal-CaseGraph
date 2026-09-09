# MAAT Architecture

```text
Human Context
    |
    v
+------------------+
| Intake/Normalize |
+------------------+
    |
    v
+------------------+      +-------------------+
| Universal        |----->| Evidence/Conflict |
| CaseGraph        |      | Reasoner          |
+------------------+      +-------------------+
    |                         |
    +------------+------------+
                 v
         +----------------+
         | Planner / NBA  |
         +----------------+
                 |
                 v
         +----------------+
         | Strands Agent  |
         | + Tool Router  |
         +----------------+
                 |
                 v
         +----------------+
         | Verification   |
         +----------------+
                 |
                 v
         +----------------+
         | Proof Receipt  |
         +----------------+
```

## Runtime split
The deterministic core can build and test graph state without cloud access. The Strands layer supplies model-driven extraction/reasoning/tool choice for the competition runtime. This keeps CI reproducible while preserving genuine agentic execution in the deployed path.

## Handoff contract
Every stage returns typed state. Free-form model output is never treated as proof until normalized and linked to source or execution evidence.
