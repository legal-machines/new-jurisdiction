# Contributing

New Jurisdiction welcomes lawyers, researchers, developers, human-only contributors and people working with AI agents. You do not need to agree with an existing proposal to improve the experiment.

Before contributing, read [CHARTER.md](CHARTER.md), [GOVERNANCE.md](GOVERNANCE.md) and the relevant part of [law/](law/README.md). If an AI system will act on the repository, also give it [AGENTS.md](AGENTS.md).

## 1. Choose a legal problem

Start with one bounded problem. You may choose an item from [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) or open a legal-problem Issue.

Before proposing text, state:

- the current legal state;
- the problem in that state;
- the objective of a change;
- the facts, assumptions, inferences and normative choices on which the proposal depends.

Do not begin with a desired rule and reverse-engineer a problem statement around it.

## 2. Inspect relevant material

Read the relevant accepted law, open or retained proposals, synthetic cases, evaluations and research. Search for affected terms and identifiers. If no relevant accepted provision exists, say so explicitly.

Do not treat an Issue, branch, open Pull Request, evaluation or research note as accepted law.

## 3. Prepare the smallest coherent change

Create a branch. Modify only material needed to address the stated problem. A normal proposal contains:

- one structured record copied from [proposals/TEMPLATE.json](proposals/TEMPLATE.json) and named `proposals/NJ-P-####.json`;
- changes to the affected law, if any;
- synthetic case files under [cases/](cases/README.md), when needed to test the rule;
- research or evaluation artifacts only when they are actually used and accurately sourced.

Choose the next unused proposal number visible in the repository. Parallel work may collide; if it does, one proposer should renumber before merge. The validator checks identifier uniqueness and filename agreement.

For a new provision, add its file in the appropriate legal category. For an amendment, keep the scope narrow and list the changed file in `affectedProvisions`.

## 4. Complete the reasoning record

The proposal record must describe:

- problem;
- objective;
- proposed change;
- affected provisions and dependencies;
- trade-offs;
- strongest argument against;
- expected failure modes;
- concrete test cases;
- sources or comparative material, if used;
- unresolved uncertainty;
- authorship mode, AI systems used and human intervention.

Empty arrays are allowed where a field is genuinely inapplicable. Do not use them to avoid material analysis. Do not invent detail to satisfy a field; explain unknowns as uncertainty.

## 5. Test the proposal

Use concrete cases that could reveal ambiguity, overbreadth, underbreadth, conflicting duties, enforcement problems or unwanted incentives. Follow [cases/README.md](cases/README.md).

Synthetic cases are analytical tools. A proposal surviving them does not prove real-world outcomes.

Run:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

To check a proposal file before it has a final repository filename:

```bash
python3 scripts/validate.py --proposal path/to/proposal.json
```

## 6. Disclose authorship accurately

Use the authorship mode that best describes what materially happened:

- `human_authored`;
- `human_authored_ai_assisted`;
- `agent_drafted_human_reviewed`;
- `agent_authored`;
- `multi_agent`.

List each materially used AI system by a useful name and version when known. Describe human intervention concretely. Do not claim exact prompts, model versions, review or provenance that was not retained.

AI assistance is permitted. It is not evidence that a proposal is correct, and human submission does not make AI output authoritative.

## 7. Open and review the Pull Request

Use the Pull Request template. Link the problem Issue when one exists. Explain the proposal in plain language and identify the decision requested from maintainers.

During review:

- answer the strongest objections directly;
- separate drafting changes from changes to the objective;
- add cases when discussion reveals an untested edge;
- correct unsupported claims and citations;
- preserve unresolved disagreement in the record.

Maintainers may request changes, accept or reject the proposal under [GOVERNANCE.md](GOVERNANCE.md). Rejection is a legitimate experimental result.

## Contribution boundaries

Do not:

- rewrite unrelated law;
- fabricate sources, consensus, contributors, reviews or test results;
- present AI as a legal authority;
- add custom voting, tokens, blockchain or DAO mechanics;
- add platform infrastructure when GitHub already supports the needed workflow;
- include secrets, personal data or confidential client material;
- represent this hypothetical framework as real law or legal advice.
