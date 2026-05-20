# Structuring and Solving a Product Launch Decision

## Scenario

StrideWear's Head of Strategy has described the options for the upcoming **Apex Trainer** launch to your analytics team. Her summary is below — but it's a verbal description, not a structured model. Your job is to turn it into one.

---

> "We're choosing between three paths. The first is a **Full Launch**: we commit $600K to national marketing and broad retail distribution. If demand is strong, our models show this generates around $12M in gross revenue. In a typical year it's closer to $4M. But if demand is weak — which we've seen plenty of — unsold inventory markdowns can flip revenue negative, roughly −$4M.
>
> The second option is a **Regional Rollout**: $200K to run the launch in eight priority markets. It's a more conservative play. Strong demand environment gets us about $5.5M; average conditions, around $2M; even in a weak environment we'd expect to clear maybe $0.5M since the limited footprint limits our inventory exposure.
>
> Third option: **Hold**. Delay to next season. No spend, no upside, no downside."

---

To estimate how likely each demand environment is, your team benchmarks against real US sporting goods retail sales data. `data/sporting_goods_sales.csv` contains monthly retail sales figures from FRED (MRTSSM45111USS, public domain). You'll compute year-over-year growth rates and use tertile binning to assign equal 1/3 probability to each of three states — the same technique used across the decision science toolkit.

## What you'll deliver

A completed Jupyter notebook (start from `building_decision_models_starter.ipynb`) that:

1. Loads the sporting goods sales data, computes year-over-year growth rates, drops NaN
   rows, and derives state probabilities by tertile-binning the growth rates into
   **High**, **Base**, and **Low** demand environments.
2. Defines `OPTIONS` and `STATES` — a list and a dictionary — directly from the
   Head of Strategy's description above. Defines all business parameters as
   module-level constants (`FULL_LAUNCH_COST_M`, `REGIONAL_COST_M`, etc.).
3. Implements `option_profit(option, demand_state)` — a function that takes an option
   name and a demand state name and returns the net 12-month profit in $M. The function
   body must reference the module-level constants, not hardcode numbers.
4. Builds the payoff matrix as a `pd.DataFrame` by calling `option_profit` across every
   combination of option and demand state.
5. Computes **EV per option** as `(payoffs * pd.Series(STATES)).sum(axis=1)` and
   identifies the EV-maximizing option.
6. Computes **minimax regret** per option (regret matrix, row-wise max, identify the
   option with the smallest maximum regret).
7. Visualizes the decision tree using matplotlib: one root decision node, one branch per
   option, one sub-branch per demand state, payoff at each leaf. Use `boxstyle="round"`
   for the node labels and label each leaf with the state name and profit.
8. Performs one **sensitivity flex**: recompute EV using pessimistic weights
   (P(High) = 0.20, P(Base) = 0.30, P(Low) = 0.50). Report whether the EV-maximizing
   option changes and what that implies about the robustness of the base-case choice.

## Requirements

- Your notebook must run top to bottom without errors.
- `option_profit` must derive all payoffs from module-level constants — no numbers
  hardcoded inside the function body.
- The payoff matrix must be built by calling `option_profit`, not by manually typing
  the values into a DataFrame.
- State probabilities must come from the data via tertile binning — don't hardcode 1/3.
- The tree diagram must show all three options and all three states (nine leaf nodes).
- The sensitivity interpretation must be 1–2 sentences and must name the specific
  condition under which the recommendation changes.

## Resources you may find useful

- [pandas: DataFrame.pct_change](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html) — for year-over-year growth rates
- [pandas: Series.quantile](https://pandas.pydata.org/docs/reference/api/pandas.Series.quantile.html) — for tertile thresholds
- [matplotlib: ax.text with bbox](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html) — for decision tree node labels

## Note on the data

`data/sporting_goods_sales.csv` contains monthly US sporting goods store retail sales
from FRED series [MRTSSM45111USS](https://fred.stlouisfed.org/series/MRTSSM45111USS)
(US Census Bureau Monthly Retail Trade Survey, NAICS 45111, public domain). See
`data/README.md` for the full citation. The scenario company **StrideWear** is fictional;
the underlying market data is real.
