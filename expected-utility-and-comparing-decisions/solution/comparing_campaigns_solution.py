# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# This file is a jupytext-paired Python script export of
# `comparing_campaigns_solution.ipynb`. The canonical artifact for learners is
# the notebook (.ipynb); this script is provided for code review and `git diff`
# readability. Run `jupytext --sync` to keep the two in lockstep after edits.

# %% [markdown]
# # Comparing Marketing Campaigns with Expected Utility (SOLUTION)
#
# ## Scenario
#
# You are the lead decision scientist at **Key & Quarter Hosts**, a small
# short-term-rental management firm that lists properties on Airbnb-style
# platforms. The Head of Growth wants to launch a campaign next quarter to
# attract new property owners onto the Key & Quarter Hosts platform, and has put three
# options on the table:
#
# - **Premium Listing Push** — invest in professional photography, premium
#   listing positioning, and paid placement on aggregator sites. Expensive,
#   with high upside if the broader short-term-rental market is strong but a
#   sizeable loss if the market softens.
# - **Local Concierge Add-on** — bundle Key & Quarter Hosts listings with a local
#   concierge service (airport pickup, restaurant booking, late-night
#   support). Modest budget, modest upside, modest downside.
# - **Hold** — defer the campaign one quarter and reinvest the budget into
#   existing-host retention.
#
# Key & Quarter Hosts operates across a set of mid-tier short-term-rental markets. The
# campaign is a *single firm-wide choice* — whichever option the team picks
# runs across Key & Quarter Hosts's whole portfolio next quarter; we are not choosing
# different campaigns for different cities. How well that single choice
# performs depends on **the demand cycle the short-term-rental industry is
# in over the next three months** — a Strong-demand, Average, or Weak-demand
# environment that affects all of Key & Quarter Hosts's markets at once. The cycle is
# uncertain (we decide the campaign now; the cycle reveals itself later),
# but it is not a coin flip — there is a real distribution we can estimate
# from data.
#
# To estimate that distribution, we use cross-city variation in current
# Inside Airbnb data as a *stand-in* for the range of conditions any given
# market can be in at any given time. The reasoning: eighteen real cities
# span a wide range of revenue-proxy values today, and that cross-sectional
# spread is a defensible empirical picture of what a Strong, Average, or
# Weak rental environment looks like.
#
# The file `data/airbnb_city_stats.csv` contains city-level summary
# statistics for 18 well-known short-term-rental markets in the format
# published by Inside Airbnb (see `data/README.md` for the full citation).
# For each city, we have the median nightly price, the median monthly
# reviews per listing (Inside Airbnb's standard occupancy proxy), and a few
# other fields. We compute `median_price × median_reviews_per_month` — a
# per-listing monthly revenue proxy — for each city, tertile-bin the
# eighteen cities into Strong / Average / Weak environments, and use the
# empirical share of cities in each bin as the prior on what kind of
# environment Key & Quarter Hosts will face next quarter. The cities themselves are
# not Key & Quarter Hosts's markets; they are a benchmark for what "a Strong market"
# or "a Weak market" looks like in numbers.
#
# ## What this notebook delivers
#
# The Head of Growth has asked the team to run the numbers — expected value,
# expected utility under risk aversion, and minimax regret — and to identify
# which decision rule the team would lean on if forced to commit today. A
# full stakeholder-facing recommendation is a separate skill covered in other
# course, after additional analysis steps. Today's deliverable is:
#
# 1. The side-by-side comparison of what each decision rule selects.
# 2. A 1–2 sentence defended choice of decision rule.
#    the next quarter looks like the cross-city baseline?"*

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "../comparing-marketing-campaigns-starter/data/airbnb_city_stats.csv"

# %% [markdown]
# ## 1. Load the data

# %%
cities = pd.read_csv(DATA_PATH)
print(cities.head())
print("...")
print(cities.tail())

# %% [markdown]
# ## 2. Per-listing monthly revenue proxy
#
# A coarse but defensible per-listing monthly revenue indicator: median nightly
# price times Inside Airbnb's standard occupancy proxy (median monthly reviews
# per active listing).

# %%
cities["revenue_proxy"] = (
    cities["median_price_usd"] * cities["median_reviews_per_month"]
)
print(cities[["city", "median_price_usd", "median_reviews_per_month",
              "revenue_proxy"]].sort_values("revenue_proxy").round(2))

# %% [markdown]
# ## 3. Classify each city into Strong / Average / Weak by tertile

# %%
t33, t67 = cities["revenue_proxy"].quantile([1 / 3, 2 / 3])
print(f"33rd percentile cutoff: {t33:.2f}")
print(f"67th percentile cutoff: {t67:.2f}")


def classify(value: float) -> str:
    if value >= t67:
        return "Strong"
    if value >= t33:
        return "Average"
    return "Weak"


cities["environment"] = cities["revenue_proxy"].apply(classify)
print(cities[["city", "revenue_proxy", "environment"]])

# %% [markdown]
# ## 4. Empirical probability of each environment

# %%
counts = cities["environment"].value_counts()
p = (counts / counts.sum()).reindex(["Strong", "Average", "Weak"])
print("Empirical probabilities:")
print(p.round(3))
print(f"Sum: {p.sum():.3f}")

# %% [markdown]
# By construction, the tertile bins each contain ~1/3 of the cities. This
# gives a simple, defensible baseline distribution to work from.

# %% [markdown]
# ## 5. Payoff matrix

# %%
payoffs = pd.DataFrame(
    {
        "Strong":  {"Premium Listing Push": 10.0, "Local Concierge Add-on": 3.0, "Hold": 0.0},
        "Average": {"Premium Listing Push":  2.0, "Local Concierge Add-on": 1.5, "Hold": 0.0},
        "Weak":    {"Premium Listing Push": -6.0, "Local Concierge Add-on": 0.0, "Hold": 0.0},
    }
)
print("Payoff matrix ($M incremental profit):")
print(payoffs)

# %% [markdown]
# ## 6. Expected value per option

# %%
ev = (payoffs * p).sum(axis=1)
print("EV per option ($M):")
print(ev.round(3))
print(f"\nEV-maximizing option: {ev.idxmax()}  (${ev.max():.2f}M)")

# %% [markdown]
# ## 7. Expected CRRA utility per option
#
# CRRA utility on (wealth_baseline + incremental profit), with γ = 2 and
# W = $50M. The wealth baseline keeps utility well-defined and represents
# the existing scale of the business; with γ > 1 the function is more sensitive
# to losses than to equally sized gains, which is what "risk aversion" means
# operationally here.

# %%
GAMMA = 2.0
WEALTH_M = 50.0


def crra_utility(profit_m, gamma: float = GAMMA, wealth_m: float = WEALTH_M):
    """CRRA utility evaluated at (wealth_m + profit_m). Vectorized."""
    x = wealth_m + np.asarray(profit_m, dtype=float)
    if abs(gamma - 1.0) < 1e-9:
        return np.log(x)
    return (np.power(x, 1.0 - gamma) - 1.0) / (1.0 - gamma)


utility_table = payoffs.map(crra_utility)
expected_utility = (utility_table * p).sum(axis=1)
ce_total_wealth = np.power(
    expected_utility * (1.0 - GAMMA) + 1.0, 1.0 / (1.0 - GAMMA)
)
certainty_equivalent = ce_total_wealth - WEALTH_M

print("Expected utility per option:")
print(expected_utility.round(6))
print("\nCertainty-equivalent profit ($M) per option:")
print(certainty_equivalent.round(3))
print(f"\nUtility-maximizing option: {expected_utility.idxmax()}  "
      f"(CE = ${certainty_equivalent[expected_utility.idxmax()]:.2f}M)")

# %% [markdown]
# Notice that *Premium Listing Push* has the highest **expected profit** but
# *Local Concierge Add-on* has the highest **certainty-equivalent profit**.
# A risk-averse decision-maker would trade away ~$0.5M of expected profit to
# avoid the -$6M downside in a Weak environment.

# %% [markdown]
# ## 8. Minimax regret per option

# %%
best_per_state = payoffs.max(axis=0)
regret = best_per_state - payoffs
max_regret = regret.max(axis=1)

print("Regret matrix ($M):")
print(regret)
print("\nMax regret per option ($M):")
print(max_regret)
print(f"\nMinimax-regret option: {max_regret.idxmin()}  "
      f"(max regret = ${max_regret.min():.2f}M)")

# %% [markdown]
# ## 9. Compare the three decision rules

# %%
comparison = pd.DataFrame(
    {
        "Selected option": [ev.idxmax(),
                            expected_utility.idxmax(),
                            max_regret.idxmin()],
        "Score": [f"EV = ${ev.max():.2f}M",
                  f"CE = ${certainty_equivalent[expected_utility.idxmax()]:.2f}M",
                  f"Max regret = ${max_regret.min():.2f}M"],
    },
    index=["EV-max", "Expected-utility-max (γ=2)", "Minimax regret"],
)
print(comparison)

# %% [markdown]
# **The three rules do not agree.** EV-max picks Premium Listing Push,
# minimax-regret picks Premium Listing Push, but expected CRRA utility (γ = 2)
# picks Local Concierge Add-on. The disagreement is real: Premium has the
# higher expected profit but a heavier tail in a Weak market — its
# certainty-equivalent profit ($1.17M) is lower than Local Concierge's
# ($1.47M) once the −$6M downside is priced in.
#
# **The decision rule I would lean on is expected CRRA utility.** With γ = 2,
# the gap between Premium's EV ($2.0M) and Local Concierge's EV ($1.5M) does
# not justify the −$6M downside in a Weak quarter for a firm of Key & Quarter Hosts's
# scale. A risk-neutral decision-maker should lean on EV-max instead.
#
# This deliverable stops at *defending a decision rule*. Translating the
# comparison into a stakeholder-facing recommendation — with caveats,
# robustness checks, and downstream pipeline output — is built explicitly in
# the communication-focused modules.

# %% [markdown]
# ## 10. Segmentation-aware option: Selective Push
#
# Every option so far commits Key & Quarter Hosts to the *same campaign across its entire
# portfolio*. But Key & Quarter Hosts can observe which markets are currently Strong, Average,
# or Weak using the Inside Airbnb data — and could target its spend accordingly.
#
# **Selective Push**: run Premium Listing Push only in currently-Strong markets,
# Local Concierge Add-on in Average markets, and Hold in Weak markets.

# %%
payoffs.loc["Selective Push"] = {"Strong": 6.0, "Average": 1.5, "Weak": -1.0}
print("Updated payoff matrix ($M):")
print(payoffs)

# %%
ev4           = (payoffs * p).sum(axis=1)
utility4      = payoffs.map(crra_utility)
exp_u4        = (utility4 * p).sum(axis=1)
ce4_wealth    = np.power(exp_u4 * (1.0 - GAMMA) + 1.0, 1.0 / (1.0 - GAMMA))
ce4           = ce4_wealth - WEALTH_M
best4         = payoffs.max(axis=0)
max_regret4   = (best4 - payoffs).max(axis=1)

comparison4 = pd.DataFrame(
    {
        "Selected option": [ev4.idxmax(),
                            exp_u4.idxmax(),
                            max_regret4.idxmin()],
        "Score": [f"EV = ${ev4.max():.2f}M",
                  f"CE = ${ce4[exp_u4.idxmax()]:.2f}M",
                  f"Max regret = ${max_regret4.min():.2f}M"],
    },
    index=["EV-max", "Expected-utility-max (γ=2)", "Minimax regret"],
)
print(comparison4)

# %% [markdown]
# **All three rules now agree on Selective Push** (EV = $2.17M, CE = $2.01M,
# max regret = $4.0M — better than every other option on every criterion).
# The uniform options force Key & Quarter Hosts to either accept the full -$6M downside
# (Premium) or cap the upside at $3M (Concierge). Selective Push sidesteps
# that tradeoff: by concentrating the expensive campaign where it is most
# likely to pay off and limiting exposure elsewhere, it captures most of
# Premium's upside while cutting its worst-case loss by two-thirds.
#
# This mirrors the "WTP hybrid" concept in the Nimbus project: raising price
# only for high-willingness-to-pay segments can dominate a uniform price change
# on all three decision metrics.
