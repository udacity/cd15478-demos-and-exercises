# Comparing Marketing Campaigns with Expected Utility

## Scenario

You are the lead decision scientist at **BlueDoor Hosts**, a small short-term-rental management firm that lists properties on Airbnb-style platforms. The Head of Growth wants to launch a campaign next quarter to attract new property owners onto the BlueDoor platform, and has put three options on the table:

- **Premium Listing Push** — invest in professional photography, premium listing positioning, and paid placement on aggregator sites. Expensive, with high upside if the broader short-term-rental market is strong but a sizeable loss if the market softens.
- **Local Concierge Add-on** — bundle BlueDoor listings with a local concierge service (airport pickup, restaurant booking, late-night support). Modest budget, modest upside, modest downside.
- **Hold** — defer the campaign one quarter and reinvest the budget into existing-host retention.

BlueDoor operates across a set of mid-tier short-term-rental markets. The campaign is a *single firm-wide choice* — whichever option the team picks runs across BlueDoor's whole portfolio next quarter; you are not choosing different campaigns for different cities. How well that single choice performs depends on **the demand cycle the short-term-rental industry is in over the next three months** — a Strong-demand, Average, or Weak-demand environment that affects all of BlueDoor's markets at once. The cycle is uncertain (you decide the campaign now; the cycle reveals itself later), but it is not a coin flip — there is a real distribution you can estimate from data.

To estimate that distribution, the team uses cross-city variation in current Inside Airbnb data as a *stand-in* for the range of conditions any given market can be in at any given time. The reasoning: eighteen real cities span a wide range of revenue-proxy values today, and that cross-sectional spread is a defensible empirical picture of what a Strong, Average, or Weak rental environment looks like.

The file `data/airbnb_city_stats.csv` contains city-level summary statistics for 18 well-known short-term-rental markets in the format published by [Inside Airbnb](http://insideairbnb.com/) (see `data/README.md` for the full citation). For each city, you have the median nightly price, the median monthly reviews per listing (Inside Airbnb's standard occupancy proxy), and a few other fields. You will compute `median_price × median_reviews_per_month` — a per-listing monthly revenue proxy — for each city, tertile-bin the eighteen cities into Strong / Average / Weak environments, and use the empirical share of cities in each bin as your prior on what kind of environment BlueDoor will face next quarter. The cities themselves are not BlueDoor's markets; they are a benchmark for what "a Strong market" or "a Weak market" looks like in numbers.

The Head of Growth has asked the team to run the numbers — expected value, expected utility under risk aversion, and minimax regret — and to identify which decision rule the team would lean on if forced to commit today. A full stakeholder-facing recommendation will be assembled later in the course, after additional analysis steps; today's deliverable is the side-by-side comparison plus your defended choice of decision rule, and an answer to the question *"How sensitive is the EV-max choice to our assumption that the next quarter looks like the cross-city baseline?"*

## What you'll deliver

A completed Jupyter notebook (start from `comparing_campaigns_starter.ipynb`) that:

1. Loads the city-level Airbnb snapshot.
2. Computes `revenue_proxy = median_price_usd × median_reviews_per_month` for each city.
3. Classifies each city into one of three market environments — **Strong**, **Average**, or **Weak** — using the tertiles (33rd and 67th percentiles) of `revenue_proxy`.
4. Estimates the empirical probability of each environment from the share of cities that fell into it.
5. Defines a payoff matrix giving the 12-month incremental contribution profit (in $M) for each of the three campaign options under each of the three environments. Use the values in the [Payoff matrix](#payoff-matrix) table below.
6. Computes the **expected value (EV)** of each option using the empirical probabilities.
7. Computes the **expected CRRA utility** of each option using risk aversion γ = 2 and a wealth baseline of $50M, and reports the **certainty-equivalent profit** for each option. Identify the option that maximizes expected utility.
8. Computes the **maximum regret** of each option across the three environments and identifies the **minimax-regret** option.
9. Produces a side-by-side comparison of which option each of the three decision rules selects (EV-max, expected-utility-max with the certainty-equivalent in dollars, and minimax-regret). If the three rules disagree, identify in one to two sentences which decision rule you would lean on and why. **Do not yet convert this comparison into a recommendation to a stakeholder** — the skill of translating analytical output into a stakeholder-facing recommendation is built later in the course. Today's deliverable is the comparison itself plus your defended choice of decision rule.
10. Performs one **sensitivity flex**: recompute EV under the alternative assumption that the next quarter has elevated downside risk — set P(Strong) = 0.20, P(Average) = 0.30, P(Weak) = 0.50 — and report whether the EV-max option changes.

## Payoff matrix

Twelve-month incremental contribution profit, in $M, relative to baseline (Hold = 0 in every environment).

| Option | Strong | Average | Weak |
| --- | --- | --- | --- |
| Premium Listing Push | +10.0 | +2.0 | -6.0 |
| Local Concierge Add-on | +3.0 | +1.5 | 0.0 |
| Hold | 0.0 | 0.0 | 0.0 |

These numbers are pre-set so you can focus on the decision-theory mechanics. In a real engagement you would build them from a cost-benefit model.

## Requirements

- Your notebook must run top to bottom without errors.
- Probabilities of the three environments must be derived from the data, not hardcoded.
- All three decision rules (EV, expected CRRA utility, minimax regret) must be computed from the payoff matrix and the empirical probabilities — no hand-picked answers.
- The defended-choice paragraph must be 1–2 sentences, must name the decision rule you would lean on, and must not yet attempt a stakeholder-facing recommendation.
- The sensitivity flex must use the same payoff matrix and the same code path as the main analysis — only the probability vector changes.

## Resources you may find useful

- [NumPy Documentation: numpy.average](https://numpy.org/doc/stable/reference/generated/numpy.average.html)
- [pandas DataFrame Documentation: DataFrame.qcut](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html)
- [Wikipedia: Isoelastic utility (CRRA)](https://en.wikipedia.org/wiki/Isoelastic_utility) — short reference for the constant-relative-risk-aversion utility function.
- [Inside Airbnb: About the Project](http://insideairbnb.com/about/) — background on the data source.

## Note on the data

`data/airbnb_city_stats.csv` contains rounded city-level summary statistics consistent with Inside Airbnb snapshots from 2023–2024. The Inside Airbnb dataset is in the public domain ([CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)). See `data/README.md` for the full citation. The scenario company **BlueDoor Hosts** is fictional; only the underlying market data is real.
