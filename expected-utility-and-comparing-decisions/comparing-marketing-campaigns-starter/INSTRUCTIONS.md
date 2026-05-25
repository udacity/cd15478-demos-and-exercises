# Comparing Marketing Campaigns with Expected Utility

## Scenario

You are the lead decision scientist at **Key & Quarter Hosts**, a small short-term-rental management firm that lists properties on Airbnb-style platforms. The Head of Growth wants to launch a campaign next quarter to attract new property owners onto the Key & Quarter Hosts platform, and has put three options on the table:

- **Premium Listing Push** — invest in professional photography, premium listing positioning, and paid placement on aggregator sites. Expensive, with high upside if the broader short-term-rental market is strong but a sizeable loss if the market softens.
- **Local Concierge Add-on** — bundle Key & Quarter Hosts listings with a local concierge service (airport pickup, restaurant booking, late-night support). Modest budget, modest upside, modest downside.
- **Hold** — defer the campaign one quarter and reinvest the budget into existing-host retention.

Key & Quarter Hosts operates across a set of mid-tier short-term-rental markets. The campaign is a *single firm-wide choice* — whichever option the team picks runs across Key & Quarter Hosts's whole portfolio next quarter; you are not choosing different campaigns for different cities. How well that single choice performs depends on **the demand cycle the short-term-rental industry is in over the next three months** — a Strong-demand, Average, or Weak-demand environment that affects all of Key & Quarter Hosts's markets at once. The cycle is uncertain (you decide the campaign now; the cycle reveals itself later), but it is not a coin flip — there is a real distribution you can estimate from data.

To estimate that distribution, the team uses cross-city variation in current Inside Airbnb data as a *stand-in* for the range of conditions any given market can be in at any given time. The reasoning: eighteen real cities span a wide range of revenue-proxy values today, and that cross-sectional spread is a defensible empirical picture of what a Strong, Average, or Weak rental environment looks like.

The file `data/airbnb_city_stats.csv` contains city-level summary statistics for 18 well-known short-term-rental markets in the format published by [Inside Airbnb](http://insideairbnb.com/) (see `data/README.md` for the full citation). For each city, you have the median nightly price, the median monthly reviews per listing (Inside Airbnb's standard occupancy proxy), and a few other fields. You will compute `median_price × median_reviews_per_month` — a per-listing monthly revenue proxy — for each city, tertile-bin the eighteen cities into Strong / Average / Weak environments, and use the empirical share of cities in each bin as your prior on what kind of environment Key & Quarter Hosts will face next quarter. The cities themselves are not Key & Quarter Hosts's markets; they are a benchmark for what "a Strong market" or "a Weak market" looks like in numbers.

The Head of Growth has asked the team to run the numbers — expected value, expected utility under risk aversion, and minimax regret — and to identify which decision rule the team would lean on if forced to commit today. Today's deliverable is the side-by-side comparison plus your defended choice of decision rule. Translating this analytical comparison into a stakeholder-facing recommendation — with caveats, robustness checks, and supporting narrative — is a separate skill covered in other modules.

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
9. Produces a side-by-side comparison of which option each of the three decision rules selects (EV-max, expected-utility-max with the certainty-equivalent in dollars, and minimax-regret). If the three rules disagree, identify in one to two sentences which decision rule you would lean on and why. **Do not yet convert this comparison into a recommendation to a stakeholder** — the skill of translating analytical output into a stakeholder-facing recommendation is a separate skill covered in other modules. Today's deliverable is the comparison itself plus your defended choice of decision rule.
10. Adds a **segmentation-aware option** — Selective Push — to the payoff matrix and reruns all three decision rules. Selective Push targets the Premium Listing Push campaign only to markets currently showing Strong revenue signals, running Local Concierge Add-on in Average markets and Hold in Weak markets. Use the stipulated payoffs in the [Selective Push payoffs](#selective-push-payoffs) table below. Produce an updated four-option comparison table and explain in one to two sentences what the Selective Push result implies about uniform versus segmented campaign strategies.

## Payoff matrix

12-month incremental contribution profit ($M) relative to Hold.

| Option | Strong | Average | Weak |
| --- | ---: | ---: | ---: |
| Premium Listing Push | +10.0 | +2.0 | −6.0 |
| Local Concierge Add-on | +3.0 | +1.5 | 0.0 |
| Hold | 0.0 | 0.0 | 0.0 |

## Selective Push payoffs

| Option | Strong | Average | Weak |
| --- | ---: | ---: | ---: |
| Selective Push | +6.0 | +1.5 | −1.0 |
