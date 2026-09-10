# Current Law

This directory contains the accepted substantive legal framework of New Jurisdiction.

## Current state

There are **no accepted substantive provisions** in v0.1. The repository begins with a [Founding Charter](../CHARTER.md), governance, a contribution protocol, a taxonomy and open questions. The Charter defines the experiment; it is not a fabricated general constitution or code.

The absence of provisions is intentional. A category becomes populated only when a proposal has been reviewed and accepted.

## Taxonomy

| Category | Scope | Current state |
| --- | --- | --- |
| [Foundations](foundations/README.md) | Interpretive and system-level foundations | No accepted provisions |
| [Rights](rights/README.md) | Protected interests, duties and remedies | No accepted provisions |
| [Institutions](institutions/README.md) | Authority, competence and accountability | No accepted provisions |
| [Private law](private-law/README.md) | Persons, obligations, property and civil remedies | No accepted provisions |
| [Commercial law](commercial-law/README.md) | Enterprise, exchange and market relationships | No accepted provisions |
| [Criminal law](criminal-law/README.md) | Prohibited conduct and public sanctions | No accepted provisions |
| [Procedure](procedure/README.md) | Fair processes for claims, review and enforcement | No accepted provisions |
| [Evidence](evidence/README.md) | Proof, admissibility, provenance and reliability | No accepted provisions |

The taxonomy is organizational, not a decision that every category must eventually contain law. Proposals may challenge or amend the taxonomy through the ordinary process.

## Provision format

Accepted substantive provision files use a stable identifier and live in the relevant category:

```text
law/<category>/NJ-L-####.md
```

Each provision should contain:

```text
# NJ-L-#### — Title

Status: Accepted
Introduced by: NJ-P-####
Last amended by: NJ-P-#### or Not amended

## Scope
## Rule
## Definitions
## Exceptions
## Interpretation notes
```

Use only the sections the rule needs. Interpretation notes explain boundaries; they must not silently create a second rule. Git history and the referenced proposal retain the reasoning and amendment record.

An open branch or Pull Request may contain proposed provision text. It becomes accepted law only when merged under [GOVERNANCE.md](../GOVERNANCE.md).
