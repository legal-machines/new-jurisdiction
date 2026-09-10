# New Jurisdiction

> **Build a legal system from first principles.**

New Jurisdiction is an open experiment where humans and AI agents propose, challenge, test and amend the law in public.

The research question is:

> **Can humans and AI build a legal system from first principles?**

More precisely: given explicit assumptions, goals and constraints, how effectively can humans and AI agents collaboratively create, review and maintain a coherent legal framework?

New Jurisdiction is hypothetical. It has no territory or sovereign authority. Its contents do not create legal rights or obligations and are not legal advice.

## Current experimental state

This repository is at **v0.1**. It contains the Founding Charter, governance and contribution protocols, a legal taxonomy, initial research questions, proposal and review formats, and deterministic validation.

The experiment begins without a fabricated body of law:

- the [Founding Charter](CHARTER.md) establishes the method and limits of the experiment;
- the [legal taxonomy](law/README.md) defines where accepted provisions may develop;
- there are no accepted substantive provisions yet;
- there are no accepted proposals yet;
- the [initial open questions](OPEN_QUESTIONS.md) are invitations to inquiry, not policy positions.

## How the experiment works

```text
current legal state
        ↓
identified problem
        ↓
proposal with explicit reasoning
        ↓
review and strongest objections
        ↓
testing against concrete cases
        ↓
maintainer decision
        ↓
new version-controlled legal state, or an inspectable rejection
```

Git is part of the experimental method:

- `main` represents the current accepted state;
- an Issue identifies a legal problem or requests a proposal;
- a branch represents a proposed alternative state;
- a Pull Request proposes an amendment;
- review records argument, criticism and counterargument;
- a merge accepts a change;
- Git history records provenance;
- a tag or release may identify a reproducible version.

Deterministic checks can verify structure, references and disclosure fields. They do not prove that a proposal is lawful, fair, coherent or wise.

## How to participate

Contributions are welcome from lawyers, researchers, developers, AI-agent users and human-only contributors.

1. Choose a question in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) or open a legal-problem Issue.
2. Read the [Charter](CHARTER.md), [governance rules](GOVERNANCE.md), [contribution protocol](CONTRIBUTING.md) and relevant current law.
3. Prepare the smallest coherent change that addresses the problem.
4. Add a structured proposal record and any necessary provision or case files.
5. State assumptions, trade-offs, the strongest objection, failure modes and uncertainty.
6. Disclose AI and human involvement accurately.
7. Run the deterministic checks and open a Pull Request for adversarial review.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete contribution path. Direct changes to `main` are not the normal contribution model.

## Bring your agent

Human-only participation is equally valid. If you use an AI agent, give it this repository and the following instruction:

```text
Read CHARTER.md, GOVERNANCE.md, CONTRIBUTING.md and AGENTS.md.

Study the current legal framework and identify one material problem.
Do not begin by drafting. First state the current legal state, the problem,
the objective and the relevant assumptions.

Propose the smallest coherent change that addresses the problem. Explain the
affected provisions, dependencies, trade-offs, strongest objection, expected
failure modes, test cases and remaining uncertainty.

Distinguish facts, assumptions, inferences and normative choices. Disclose the
AI systems used and human involvement accurately. Follow the repository
contribution rules and prepare a Pull Request.
```

The operational, vendor-neutral protocol is in [AGENTS.md](AGENTS.md).

## Repository map

| Path | Purpose |
| --- | --- |
| [CHARTER.md](CHARTER.md) | Founding principles and experimental limits |
| [GOVERNANCE.md](GOVERNANCE.md) | Review, decision and amendment process |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Human and agent contribution workflow |
| [AGENTS.md](AGENTS.md) | Executable protocol for AI agents |
| [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) | Initial unanswered research questions |
| [law/](law/README.md) | Current legal framework and taxonomy |
| [proposals/](proposals/README.md) | Proposal records and JSON Schema |
| [cases/](cases/README.md) | Synthetic cases used to test proposals |
| [evaluations/](evaluations/README.md) | Retained structured review artifacts |
| [research/](research/README.md) | Cited comparative and empirical material |
| [scripts/validate.py](scripts/validate.py) | Dependency-free deterministic validator |

## Contribution and governance rules

Every material change should be narrow, traceable and contestable. A proposal must expose its objective, affected interests, trade-offs, strongest objection, test cases and unresolved uncertainty. Sources must be cited when used; unknown facts must remain unknown.

AI systems may propose, analyze, critique and test rules. They are participants, not authorities. For v0.1, contributors propose and review while Legal Machines maintainers make merge decisions in public repository history. See [GOVERNANCE.md](GOVERNANCE.md).

## License

Unless a file says otherwise, this repository is licensed under the [Apache License 2.0](LICENSE).

## Legal Machines

New Jurisdiction is designed and maintained as an open research experiment by Legal Machines. The protocol does not privilege any AI model, agent or Legal Machines product.
