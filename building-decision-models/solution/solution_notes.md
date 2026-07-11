# Solution Walkthrough — Structuring and Solving a Product Launch Decision

This is the text companion to `building_decision_models_solution.ipynb`. It
summarizes the key steps, the numbers a learner should arrive at, and the most
common mistakes to flag.

## Headline result

| Decision rule | Selected option | Score |
| --- | --- | --- |
| EV-max | National Launch | EV = $3.72M |
| Expected CRRA utility (γ = 2, W = $20M) | Regional Test Launch | CE = $2.57M |

**EV-max and expected-utility-max pick different options** — that disagreement is
the engineered teaching moment. National Launch has the highest expected profit
($3.72M) because the $13.0M High-demand upside outweighs the −$3.5M Low-demand
loss on average. Regional Test Launch wins on certainty-equivalent profit because
CRRA utility (γ = 2) penalizes National Launch's −$4.2M downside heavily enough to
drag its certainty equivalent down to $1.78M — well below its own expected value,
and below Regional Test Launch's $2.57M.

The exercise stops at a defended choice of decision rule. It does not ask
learners to translate the comparison into a stakeholder-facing recommendation.

## Key steps

1. **Load data** — `pd.read_csv`, then rename columns to `date` and `sales_m`.
   Result is a 120-row DataFrame.

2. **YoY growth rate** — `sales["sales_m"].pct_change(12) * 100`.
   Drop NaN with `dropna(subset=["yoy"])`.

3. **Tertile binning** — `t33, t67 = sales["yoy"].quantile([1/3, 2/3])` gives
   thresholds at roughly 1.1% and 3.1%. Classify each month as `"Low"`, `"Base"`,
   or `"High"`.

4. **State probability dict** — `STATES = (counts / counts.sum()).reindex(["High", "Base", "Low"]).to_dict()`.
   Uses the empirical tertile proportions directly (High ≈ 0.343, Base ≈ 0.324,
   Low ≈ 0.333 — close to but not exactly 1/3 each, since real month counts don't
   split perfectly evenly across the three bins).

5. **Payoff matrix** — `pd.DataFrame` with options as rows (`National Launch`,
   `Regional Test Launch`, `Hold`), states as columns (`High`, `Base`, `Low`).
   Pull values from module-level constants:

   |  | High | Base | Low |
   | --- | ---: | ---: | ---: |
   | National Launch | 12.30 | 2.80 | −4.20 |
   | Regional Test Launch | 5.75 | 2.05 | 0.45 |
   | Hold | 0.00 | 0.00 | 0.00 |

6. **Expected value** — `ev = (payoffs * pd.Series(STATES)).sum(axis=1)`.
   National Launch: **$3.72M**. Regional Test Launch: **$2.78M**. Hold: **$0.00M**.
   EV-maximizing option: **National Launch**.

7. **Expected CRRA utility** — `u(x) = ((W+x)^(1-γ) - 1) / (1-γ)`, evaluated at
   `WEALTH_M + option_profit(...)` with γ = 2, W = $20M. Invert to a
   certainty-equivalent profit: `ce = (eu*(1-γ)+1)**(1/(1-γ)) - W`.
   National Launch: CE = **$1.78M**. Regional Test Launch: CE = **$2.57M**.
   CE-maximizing option: **Regional Test Launch**.

8. **Decision tree — backward induction** — root decision node on the left,
   one chance node per option, one leaf per demand state. Both EV and CE are
   rolled back to the decision node per option; the EV-optimal branch (National
   Launch) and CE-optimal branch (Regional Test Launch) are highlighted in
   different colors so the disagreement is visible directly on the tree.

## Code snippets

```python
# The EV calculation
ev = (payoffs * pd.Series(STATES)).sum(axis=1)
```

```python
# CRRA utility and certainty equivalent (gamma = 2, wealth baseline = $20M)
def utility(profit_m, gamma=2.0, wealth_m=20.0):
    x = wealth_m + profit_m
    return (x ** (1 - gamma) - 1) / (1 - gamma)

eu = pd.Series({opt: sum(STATES[s] * utility(option_profit(opt, s)) for s in STATES)
                for opt in OPTIONS})
ce_wealth = np.power(eu * (1.0 - 2.0) + 1.0, 1.0 / (1.0 - 2.0))
ce = ce_wealth - 20.0
```

## Common mistakes to flag

- **Hardcoding probabilities as exactly 1/3.** The requirement is to use the
  empirical tertile proportions from the data (`STATES` built from
  `value_counts()`), which land close to but not exactly at 1/3 each.

- **Skipping the wealth baseline in CRRA.** Plugging incremental profits
  directly into the utility function gives an undefined result for γ > 1 when
  profit is 0 or negative relative to a zero baseline. The wealth baseline
  keeps utility well-defined and is what makes the magnitudes interpretable.

- **Reporting expected utility as a dollar amount.** The `eu` values are utils,
  not dollars. The dollar-equivalent comparison is the certainty-equivalent
  profit, which requires inverting the CRRA function.

- **Confusing EV-max and CE-max are "supposed to agree."** They don't here,
  and that's the point — the disagreement is what motivates using expected
  utility instead of raw expected value when downside risk matters.

- **Jumping past the defended rule to a stakeholder recommendation.** The
  exercise deliberately stops at naming a decision rule and explaining the
  tradeoff. Translating the output into a recommendation memo — with caveats,
  risk appetite discussion, and strategic context — is taught in separate
  modules.

- **Confusing this decision tree with a machine-learning decision tree.**
  This tree maps choices and consequences that haven't happened yet
  (backward induction over a payoff structure); an ML decision tree
  classifies data it has already seen. Same name, different purpose.
