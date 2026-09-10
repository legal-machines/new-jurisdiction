# Proposals

A proposal is the core unit of change in New Jurisdiction. It is normally represented by a Pull Request containing a structured JSON record and the smallest coherent change to the legal framework.

There are no accepted proposal records in v0.1.

## Files

- [schema.json](schema.json) is the machine-readable proposal contract.
- [TEMPLATE.json](TEMPLATE.json) is a copyable drafting aid, not a proposal or experiment record.
- Actual proposal records are named `NJ-P-####.json`.

The numeric identifier is stable. The JSON `id` must match the filename, and identifiers must be unique.

## Lifecycle

Proposal branches may use these statuses:

- `draft` — not ready for a decision;
- `proposed` — submitted for review;
- `under_review` — active substantive review;
- `accepted` — approved for merge into the accepted state;
- `rejected` — not accepted after review;
- `withdrawn` — withdrawn by the proposer;
- `superseded` — replaced by an identified later proposal.

Only merged files on `main` are part of the canonical repository record. Before merging a proposal that changes law, a maintainer should set its status to `accepted`. Rejected and withdrawn proposals normally remain visible through their closed Pull Requests rather than being merged merely to create activity.

## Required reasoning

The schema requires a problem, objective, proposed change, affected interests, trade-offs, strongest objection, failure modes, test cases, sources, uncertainty and authorship disclosure.

Arrays may be empty when genuinely inapplicable. The narrative should state uncertainty rather than manufacture detail. A proposal without external sources may use an empty `sources` array; it must not imply that evidence was reviewed.

`affectedProvisions` and `testCases` contain repository-relative file paths. Referenced files must exist in the proposed branch. Dependencies use an explicit kind:

- `provision` for a repository path;
- `proposal` for another proposal identifier;
- `external` for a dependency outside the repository.

The validator checks local provision and proposal dependencies. An external dependency is disclosed but not treated as verified.

## Authorship

Choose the mode that describes what materially happened. Human-only work uses an empty `aiSystems` array. Every other mode lists at least one materially used system. `humanIntervention` must state the human role accurately, including when it was limited.

Do not infer a model version or review event that was not captured.

## Validate

```bash
python3 scripts/validate.py
```

Validation proves structural invariants only. It does not determine legal merit, consistency, fairness or compliance with the Charter.
