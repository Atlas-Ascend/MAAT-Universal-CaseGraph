# 17 — GARI CaseGraph Universal

## Identity

**Capability name:** `GARI CaseGraph Universal`  
**Implementation provider:** `MAAT — Universal CaseGraph`  
**Consumer / research institution:** `Ghost Atlas Research Institute (GARI)`  
**Status:** IMPLEMENTED RESEARCH VISUALIZATION MODE

This is a capability binding, not a new GARI organ and not a replacement CaseGraph repository.

## Mission

Give GARI one visual research graph that can show and track the full state of each research program from source and question through claims, hypotheses, branches, models, datasets, experiments, evidence, contradictions, synthesis, decisions, publications, proof receipts, corrections and next questions.

The graph exists to make the research organism inspectable.

## Canonical ownership law

MAAT/CaseGraph is the visualization and projection provider.

It does **not** replace:

- GARI — institute/research cognition;
- LABCORE — research infrastructure and ontology;
- THOTH — durable estate memory;
- GARI-Provenance — source/derivation lineage;
- GARI-VERITAS — scientific evidence-status authority;
- ProofGrid — durable proof receipts;
- the individual GARI branch that owns the underlying research object.

`PROJECTION != PROMOTION`

`VISIBLE != VALIDATED`

`GRAPH NODE != NEW CANON OBJECT`

## Source ontology

The research projection mirrors the 24 canonical object types defined by GARI BT-08:

`ResearchQuestion, Hypothesis, Claim, Evidence, Source, Dataset, Experiment, Benchmark, Simulation, Model, Framework, ResearchProgram, ResearchPacket, BranchFinding, Synthesis, Decision, SoftwareSpecification, Publication, CaseStudy, CanonNode, Correction, Supersession, TelemetryObservation, ProofReceipt`.

Each projected node can retain:

- stable object identity;
- canonical name;
- branch;
- program identity;
- description;
- status;
- E0→E7 evidence state;
- evidence grade;
- deployment status;
- owner;
- version;
- access class;
- source references;
- provenance;
- ProofGrid references;
- dependencies;
- related object identities;
- created/updated timestamps;
- typed payload.

## Graph relations

Canonical GARI edge classes remain source-controlled:

`DERIVED_FROM, SUPPORTS, CONTRADICTS, TESTS, REPLICATES, SUPERSEDES, IMPLEMENTS, SIMULATES, DEPENDS_ON, PRODUCED_BY, REVIEWED_BY, ROUTED_TO, DEPLOYED_AS, OBSERVED_IN_FIELD, CORRECTS, RELATED_TO`.

The CaseGraph projection may display additional explicitly sourced relations but may not invent relationship truth merely to make a graph look connected.

## Visual cockpit

Route: `/gari`

Required visual behaviors:

1. research-object graph with typed nodes and relation edges;
2. filtering by object type, GARI branch, evidence state and status;
3. E0→E7 evidence ladder;
4. branch/status/owner state summaries;
5. selected-object inspector showing full source/provenance/proof envelope;
6. relation ledger;
7. graph receipt showing projection contract and truth boundary;
8. JSON intake for already-typed GARI research objects;
9. demo route proving Brain Cycle 001 → retained evidence → next question continuity.

## API

`POST /gari/research-graph`

Accepts a typed `ResearchGraphRequest` and returns `GA-GARI-CASEGRAPH-UNIVERSAL-1.0`.

`GET /gari/research-graph/demo`

Returns a bounded synthetic/executable demonstration graph based on the already-sealed Sprint 33 Brain Cycle lineage. It does not promote a cognitive theory.

## Truth boundary

The graph can show scientific evidence status, but it cannot assign a higher evidence state merely through visualization.

A visible E3 node means the supplied canonical object is currently recorded as E3; the interface itself does not produce E3.

Likewise, ProofGrid receipt display proves only what the underlying receipt proves.

## Definition of done

GARI CaseGraph Universal is complete when:

- all 24 GARI object types are representable;
- graph edges fail closed when they reference missing nodes;
- source/provenance/proof metadata survive projection;
- evidence state remains distinct from deployment and object status;
- the visual surface renders research nodes and typed relationships;
- node inspection exposes full research metadata;
- filters and evidence ladder operate without mutating source data;
- API and UI tests pass;
- merged runtime deploy is live;
- `/gari` and `/gari/research-graph/demo` are verified after deployment.
