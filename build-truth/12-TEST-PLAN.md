# 12 — Test Plan

## Unit
- Stable node IDs.
- Edge validity.
- Evidence-gap detection.
- Dependency ranking.
- Receipt linkage.

## Acceptance
Input: a changed requirement that may invalidate a database schema while deployment depends on the API.

Expected: MAAT identifies the changed requirement, schema validation need, deployment dependency, and selects schema-impact resolution ahead of deployment.

## CI gate
`pytest -q` must pass on Python 3.11 without AWS credentials.
