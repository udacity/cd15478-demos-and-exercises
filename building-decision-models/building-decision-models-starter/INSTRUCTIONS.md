# Structuring and Solving a Product Launch Decision

## Scenario

Trailmark Outdoor Co.'s VP of Product Strategy walked your analytics team through the launch options for the new **Ridge Runner** trail shoe on a call. The recap notes below summarize what was said — a spoken walkthrough, not a structured model. Your job is to turn it into one.

---

> "We're choosing between three paths. The first is a **National Launch**: we commit $700K to national marketing and broad retail distribution. If demand is strong, our models show this generates around $13M in gross revenue. In a typical year it's closer to $3.5M. But if demand is weak — which we've seen plenty of — unsold inventory markdowns can flip revenue negative, roughly −$3.5M.
>
> The second option is a **Regional Test Launch**: $250K to run the launch in a handful of priority markets. It's a more conservative play. Strong demand environment gets us about $6M; average conditions, around $2.3M; even in a weak environment we'd expect to clear maybe $0.7M since the limited footprint limits our inventory exposure.
>
> Third option: **Hold**. Delay to next season. No spend, no upside, no downside."

---

To estimate how likely each demand environment is, your team benchmarks against real US sporting goods retail sales data. `data/sporting_goods_sales.csv` contains monthly retail sales figures from FRED (MRTSSM45111USS, public domain). You'll compute year-over-year growth rates and use tertile binning to assign an empirical probability to each of three states — the same technique used across the decision science toolkit.

## What you'll deliver

A completed Jupyter notebook (start from `building_decision_models_starter.ipynb`) that:

1. Loads the sporting goods sales data, computes year-over-year growth rates, drops NaN
   rows, and derives state probabilities by tertile-binning the growth rates into
   **High**, **Base**, and **Low** demand environments.
2. Draws an **influence diagram** using the three node shapes provided in the starter
   (Decision rectangle, Uncertainty oval, Value octagon). Adds the two arrows
   connecting the nodes. Then writes 1–2 sentences explaining what the *absence* of an
   arrow between the Decision node and Uncertainty node assumes — and when that assumption
   might be wrong.
3. Defines `OPTIONS` and business constants directly from the VP of Product Strategy's
   description above. Defines all business parameters as module-level constants
   (`NATIONAL_LAUNCH_COST_M`, `REGIONAL_TEST_COST_M`, etc.).
4. Implements `option_profit(option, demand_state)` — a function that takes an option
   name and a demand state name and returns the net 12-month profit in $M. The function
   body must reference the module-level constants, not hardcode numbers.
5. Builds the payoff matrix as a `pd.DataFrame` by calling `option_profit` across every
   combination of option and demand state.
6. Computes **EV per option** as `(payoffs * pd.Series(STATES)).sum(axis=1)` and
   identifies the EV-maximizing option.
7. Computes **expected CRRA utility** per option using risk aversion γ = 2 and a wealth
   baseline of $20M, and reports the **certainty-equivalent profit** for each option.
   Identifies the utility-maximizing option.
8. Visualizes the decision tree using matplotlib as a **backward-induction rollback**:
   one root decision node, one branch per option, one sub-branch per demand state, and
   the EV and certainty-equivalent profit rolled back to the decision node for each
   option. Highlight the EV-optimal and CE-optimal branches. In 1 sentence, explain how
   this tree relates to the influence diagram you drew in step 2, and in 1–2 sentences,
   explain what it means that EV and certainty-equivalent profit recommend different
   options here.
