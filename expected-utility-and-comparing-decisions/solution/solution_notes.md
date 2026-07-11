# Solution Walkthrough — Comparing Growth Campaigns with Expected Utility

This is the text companion to `comparing_campaigns_solution.ipynb`. It summarizes the key steps, the numbers a learner should arrive at, and the most common mistakes to flag.

## Headline result

| Decision rule | Selected option | Score |
| --- | --- | --- |
| Expected value | Featured Placement Push | $1.90M |
| Expected CRRA utility (γ = 2, W = $50M) | Neighborhood Concierge Bundle | CE = $1.41M |
| Minimax regret | Featured Placement Push | Max regret = $5.70M |

The three rules disagree. The point of the exercise is for the learner to recognize that the disagreement is not a bug — it reflects a real tradeoff between expected profit and exposure to a -$5.5M downside in a Weak market environment. A risk-averse decision-maker would lean on Neighborhood Concierge Bundle; a risk-neutral one would lean on Featured Placement Push. The deliverable stops at *defending a decision rule*; the exercise does **not** ask learners to translate the comparison into a stakeholder-facing recommendation.

## Key steps

1. **Load the data.** Eighteen cities, in Inside Airbnb summary format.
2. **Compute the revenue proxy.** `median_price_usd × median_reviews_per_month` — coarse but defensible per-listing monthly revenue indicator.
3. **Tertile cutoffs** of `revenue_proxy` land near 64 and 102. The 18 cities split exactly six per bin.
4. **Empirical probabilities** are 1/3 each by construction.
5. **Payoff matrix** is given in `INSTRUCTIONS.md`; the learner just needs to type it into a DataFrame.
6. **Expected value** is the row-wise dot product of the payoff matrix with the probability vector. Featured Placement Push wins on EV ($1.90M) but has a -$5.5M tail.
7. **Expected CRRA utility** uses $u(x) = ((W+x)^{1-\gamma} - 1) / (1-\gamma)$. With γ = 2 and W = $50M, Neighborhood Concierge Bundle wins on certainty-equivalent profit ($1.41M vs. $1.21M for Featured Placement Push). The CE-equivalent is computed by inverting the CRRA function.
8. **Minimax regret** picks Featured Placement Push ($5.70M max regret vs. $6.30M for Neighborhood Concierge Bundle and $9.00M for Hold).
9. **Comparison and defended rule** — the learner produces a small table that names the option each of the three rules selects, then defends one rule in 1–2 sentences. Either Featured Placement Push or Neighborhood Concierge Bundle is a defensible choice; what is *not* defensible is hand-waving past the disagreement. The exercise deliberately stops short of a stakeholder-facing recommendation.
10. **Sensitivity flex** to `(0.20, 0.30, 0.50)` flips Featured Placement Push's EV from +$1.90M to **-$0.29M**, and Neighborhood Concierge Bundle becomes the EV-max option (+$1.06M). The teaching takeaway: every analytical output is conditional on the probability vector, and any downstream recommendation built on top of this exercise inherits that conditionality.

## Code snippets

```python
# Revenue proxy
cities["revenue_proxy"] = (
    cities["median_price_usd"] * cities["median_reviews_per_month"]
)
```

```python
# Tertile classification
t33, t67 = cities["revenue_proxy"].quantile([1/3, 2/3])
def classify(value):
    if value >= t67: return "Strong"
    if value >= t33: return "Average"
    return "Weak"
cities["environment"] = cities["revenue_proxy"].apply(classify)
```

```python
# CRRA utility (gamma = 2, wealth baseline = 50M)
def crra_utility(profit_m, gamma=2.0, wealth_m=50.0):
    x = wealth_m + np.asarray(profit_m, dtype=float)
    if abs(gamma - 1.0) < 1e-9:
        return np.log(x)
    return (np.power(x, 1.0 - gamma) - 1.0) / (1.0 - gamma)

utility_table = payoffs.map(crra_utility)
expected_utility = (utility_table * p).sum(axis=1)
ce_wealth = np.power(expected_utility * (1.0 - 2.0) + 1.0, 1.0 / (1.0 - 2.0))
ce_profit = ce_wealth - 50.0
```

```python
# Minimax regret
regret = payoffs.max(axis=0) - payoffs
max_regret = regret.max(axis=1)
```

## Common mistakes to flag

- **Hardcoding the probabilities.** Setting `p = [1/3, 1/3, 1/3]` rather than computing it from the data. The empirical probabilities happen to be exactly 1/3 because of tertile binning, but the learner should derive them — the requirement is to use the dataset, not eyeball it.
- **Skipping the wealth baseline in CRRA.** Plugging incremental profits directly into a CRRA function gives `0^(1-γ)` for the Hold option, which is undefined for γ > 1. The wealth baseline keeps utility well-defined and is what makes the magnitudes interpretable.
- **Reporting expected utility as a dollar amount.** Utility numbers near 0.98 are not dollars — they are utils. The dollar-equivalent comparison is the certainty-equivalent profit, which requires inverting the CRRA function.
- **Confusing "regret" with "loss".** Regret is measured against the best option in each scenario, not against zero. Hold has no losses, but it has $9.00M of max regret because it forgoes $9.00M of profit when Strong materializes.
- **Picking the option that "feels right" before looking at the rules.** The exercise is about applying the framework. If the three rules disagree, the defended-choice paragraph should name the rule, not pick a winner by intuition.
- **Trying to write a stakeholder-facing recommendation in step 9.** The exercise deliberately stops at the defended-rule level. Translating analytical output into a recommendation memo is built explicitly later in the course.
- **Sensitivity flex changes the wrong thing.** Some learners flex the payoffs instead of the probabilities. The point of *this* flex is to demonstrate that the EV calculation is sensitive to the probability assumption — not the payoff structure.
