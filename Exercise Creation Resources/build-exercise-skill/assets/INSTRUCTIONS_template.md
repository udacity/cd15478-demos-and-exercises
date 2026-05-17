# [Exercise title — descriptive, never numbered]

## Scenario

[2–4 sentences setting up a fictional company and the decision they face. Name the fictional company clearly, describe the role the learner is stepping into, and state the decision in concrete terms.]

[1–2 sentences naming the options on the table. If there are 3 options, list them as bullets with a short description each:]

- **[Option A]** — [one-line description; high upside / high downside angle if applicable]
- **[Option B]** — [moderate]
- **[Option C / Hold]** — [baseline / status quo]

[1–2 sentences on what makes the decision hard — the source of uncertainty. Be explicit about *what kind of uncertainty* (temporal cycle, geographic spread, demand response, etc.) and why it can't be reduced to a coin flip.]

[1 paragraph on the data the learner has and what it's a stand-in for. If you're using real-company data with a fictional scenario, make the modeling assumption explicit here — the data is a benchmark for [X], the cities/quarters/products in the data are *not* the fictional company's actual [markets/quarters/etc.].]

[Final paragraph: what the team has been asked to produce. Frame as an analytical deliverable (a comparison, a strategy, a posterior, a tornado), NOT a stakeholder-facing recommendation.]

## What you'll deliver

A completed Jupyter notebook (start from `[exercise_name]_starter.ipynb`) that:

1. [First mechanical step — e.g., load the data]
2. [Second mechanical step — e.g., compute a derived metric]
3. [Third step — e.g., classify into discrete states]
4. [Fourth step — e.g., estimate empirical probabilities]
5. [Fifth step — e.g., define a stipulated payoff matrix; reference the table below]
6. [Sixth step — e.g., compute the primary decision metric]
7. [Seventh step — e.g., compute a secondary decision metric]
8. [Eighth step — e.g., compute a third decision metric]
9. [Ninth step — comparison or defended choice, NOT a stakeholder recommendation]
10. [Tenth step — sensitivity flex on one assumption]

## [Optional: Payoff matrix or any other stipulated inputs]

[If your exercise stipulates inputs that a different module covers how to derive, put them in a clearly-labeled table here. State why they're stipulated.]

| Option | State A | State B | State C |
| --- | --- | --- | --- |
| [Option A] | +X | +Y | -Z |
| [Option B] | ... | ... | ... |
| [Option C / Hold] | 0 | 0 | 0 |

These numbers are pre-set so you can focus on [the target skill]. In a real engagement you would build them from [the thing a different module teaches].

## Requirements

- Your notebook must run top to bottom without errors.
- [Any specific computational requirements — e.g., "probabilities must come from the data, not be hardcoded"]
- [Frame the deliverable carefully — e.g., "the defended-choice paragraph must name the decision rule, not pick a winner by intuition"]
- [Anything else the rubric will check]

## Resources you may find useful

- [Documentation link 1 — use descriptive titles, not "click here"]
- [Documentation link 2]
- [Conceptual reference if applicable, e.g., a Wikipedia entry for an unfamiliar term]

## Note on the data

`data/[dataset].csv` contains [brief description]. See `data/README.md` for the full source, license, and refresh instructions. The scenario company **[Fictional Co.]** is fictional; only the underlying [data type] is real.
