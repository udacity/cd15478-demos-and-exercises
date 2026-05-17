# Solution Walkthrough — [Exercise title]

This is the text companion to `[exercise_name]_solution.ipynb`. It summarizes the key steps, the numbers a learner should arrive at, and the most common mistakes to flag.

## Headline result

| [Decision rule / Metric / Result column] | [Selected option / Value] | [Score / Detail] |
| --- | --- | --- |
| [Rule 1] | [Result] | [Score] |
| [Rule 2] | [Result] | [Score] |
| [Rule 3] | [Result] | [Score] |

[1–2 sentence summary of the headline result. If multiple rules disagree, note that the disagreement is the engineered teaching moment, and describe in plain language what the tradeoff is.]

[Note: the exercise stops at a defended choice of decision rule. It does not ask learners to translate the comparison into a stakeholder-facing recommendation.]

## Key steps

1. **[Step 1 name]** — [What the learner does, what the output should look like.]
2. **[Step 2 name]** — [Same.]
3. **[Step 3 name]** — [Same.]
4. **[Step 4 name]** — [Same.]
5. **[Step 5 name]** — [Same.]
6. **[Step 6 name]** — [Same. Call out specific numerical values if helpful.]
7. **[Step 7 name]** — [Same. If the step uses a conceptually subtle technique, explain it briefly in plain language.]
8. **[Step 8 name]** — [Same.]
9. **[Comparison and defended rule]** — [Either A or B is defensible; what is not defensible is hand-waving past the disagreement.]
10. **[Sensitivity flex]** — [What changes when the assumption is flexed. Headline teaching takeaway is that every analytical output is conditional on its inputs.]

## Code snippets

```python
# [Most important snippet — the derivation step that's easy to get wrong]
```

```python
# [Second snippet — the helper function with constants pulled out at top]
```

```python
# [Third snippet — the comparison or sensitivity step]
```

## Common mistakes to flag

- **[Mistake 1]** — [Why learners fall into it; what the right move is.]
- **[Mistake 2]** — [Same.]
- **[Mistake 3]** — [Same.]
- **[Mistake 4 — likely about misreading utility / probability / regret semantics]** — [Same.]
- **[Mistake 5 — likely about jumping past the analytical layer to a stakeholder recommendation]** — The exercise deliberately stops at the defended-rule level. Translating analytical output into a recommendation memo is taught in separate modules.

## How this exercise feeds the project

**Project step this preps:** [Step number + name from the project README — e.g., "Step 7 — Apply decision theory (EV, CRRA utility, Minimax regret)."]

**Code patterns the learner takes with them:**
- [Pattern 1 — e.g., "The `crra_utility(profit, gamma=GAMMA, wealth_baseline=WEALTH)` helper. The project uses the same signature with γ=2 and W=$500M for Nimbus."]
- [Pattern 2 — e.g., "Tertile-binning a continuous metric via `pd.qcut`. The project uses the same pattern to discretize posterior draws into Low/Base/High states for the decision tree."]
- [Pattern 3 — e.g., "Probability-weighted dot product `(payoffs * p).sum(axis=1)` over a `pd.DataFrame` × `pd.Series`. The project computes EV per option the same way."]

**Conventions adopted from the project:**
- [Convention 1 — e.g., "Probability vector as `pd.Series` indexed by state name."]
- [Convention 2 — e.g., "Payoff matrix as `pd.DataFrame` with options as rows."]
- [Convention 3 — e.g., "Module-level constants for tunable parameters."]

**What's deliberately scoped out (because other modules / the project handles it):**
- [Scoped-out skill 1 — e.g., "Building the payoff matrix from a cost-benefit model is a separate module's job; here the matrix is stipulated."]
- [Scoped-out skill 2 — e.g., "Translating the comparison into a stakeholder memo is taught by the communication-focused modules."]

This section is for the SME reviewing the exercise — not for the learner. It documents the intentional connection between this exercise and the capstone project so the connection survives across exercise revisions and course re-orderings.
