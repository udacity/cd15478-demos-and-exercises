# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# This file is a jupytext-paired Python script export of
# `comparing_campaigns_solution.ipynb`. The canonical artifact for learners is
# the notebook (.ipynb); this script is provided for code review and `git diff`
# readability. Run `jupytext --sync` to keep the two in lockstep after edits.

# %% [markdown]
# # Comparing Growth Campaigns with Expected Utility (SOLUTION)
#
# ## Scenario
#
# You are the lead decision scientist at **Fernbrook Stays**, a small
# short-term-rental management firm that lists properties on Airbnb-style
# platforms. The VP of Growth wants to launch a campaign next quarter to
# attract new property owners onto the Fernbrook Stays platform, and has put three
# options on the table:
#
# - **Featured Placement Push** — invest in professional photography, top-of-search
#   placement, and paid listing on aggregator sites. Expensive,
#   with high upside if the broader short-term-rental market is strong but a
#   sizeable loss if the market softens.
# - **Neighborhood Concierge Bundle** — bundle Fernbrook Stays listings with a local
#   concierge service (airport pickup, restaurant booking, late-night
#   support). Modest budget, modest upside, modest downside.
# - **Hold** — defer the campaign one quarter and reinvest the budget into
#   existing-host retention.
#
# Fernbrook Stays operates across a set of mid-tier short-term-rental markets. The
# campaign is a *single firm-wide choice* — whichever option the team picks
# runs across Fernbrook Stays's whole portfolio next quarter; we are not choosing
# different campaigns for different cities. How well that single choice
# performs depends on **the demand cycle the short-term-rental industry is
# in over the next three months** — a Strong-demand, Average, or Weak-demand
# environment that affects all of Fernbrook Stays's markets at once. The cycle is
# uncertain (we decide the campaign now; the cycle reveals itself later),
# but it is not a coin flip — there is a distribution we can estimate
# from data.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "../comparing-marketing-campaigns-starter/data/airbnb_city_stats.csv"

# %% [markdown]
# ## 1. Load the data
#
# The file `data/airbnb_city_stats.csv` contains city-level summary
# statistics for 18 well-known short-term-rental markets in the format
# published by Inside Airbnb (see `data/README.md` for the full citation).
# For each city, we have the median nightly price, the median monthly
# reviews per listing (Inside Airbnb's standard occupancy proxy), and a few
# other fields. The cities themselves are not Fernbrook Stays's markets; they
# are a benchmark for what "a Strong market" or "a Weak market" looks like
# in numbers.

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
#
# To estimate the distribution of demand environments Fernbrook Stays might
# face, we use cross-city variation in the Inside Airbnb data as a
# *stand-in* for the range of conditions any given market can be in at any
# given time — eighteen cities span a wide range of revenue-proxy values
# today, and that cross-sectional spread is a defensible empirical picture
# of what a Strong, Average, or Weak rental environment looks like. We
# tertile-bin the eighteen cities into Strong / Average / Weak using the
# revenue proxy computed above.

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
# gives a simple, defensible baseline distribution to work from — the
# empirical share of cities in each bin becomes our prior on what kind of
# environment Fernbrook Stays will face next quarter.

# %% [markdown]
# ## 5. Payoff matrix

# %%
payoffs = pd.DataFrame(
    {
        "Strong":  {"Featured Placement Push": 9.0, "Neighborhood Concierge Bundle": 2.7, "Hold": 0.0},
        "Average": {"Featured Placement Push": 2.2, "Neighborhood Concierge Bundle": 1.4, "Hold": 0.0},
        "Weak":    {"Featured Placement Push": -5.5, "Neighborhood Concierge Bundle": 0.2, "Hold": 0.0},
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
# Notice that *Featured Placement Push* has the highest **expected profit** but
# *Neighborhood Concierge Bundle* has the highest **certainty-equivalent profit**.
# A risk-averse decision-maker would trade away expected profit to
# avoid the -$5.5M downside in a Weak environment.

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
#
# The VP of Growth asked the team to run the numbers — expected value,
# expected utility under risk aversion, and minimax regret — and to
# identify which decision rule the team would lean on if forced to commit
# today. Today's deliverable: a side-by-side comparison of what each
# decision rule selects, plus a defended choice of decision rule.

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
# **The three rules do not fully agree.** EV-max picks Featured Placement Push,
# minimax-regret also picks Featured Placement Push, but expected CRRA utility (γ = 2)
# picks Neighborhood Concierge Bundle. The disagreement is real: Featured Placement Push has
# the higher expected profit but a heavier tail in a Weak market — its
# certainty-equivalent profit is lower than Neighborhood Concierge Bundle's
# once the -$5.5M downside is priced in.
#
# **The decision rule I would lean on is expected CRRA utility.** With γ = 2,
# the gap between Featured Placement Push's EV and Neighborhood Concierge Bundle's EV does
# not justify the -$5.5M downside in a Weak quarter for a firm of Fernbrook Stays's
# scale. A risk-neutral decision-maker should lean on EV-max instead.
#
# This deliverable stops at *defending a decision rule*. Translating the
# comparison into a stakeholder-facing recommendation — with caveats,
# robustness checks, and downstream pipeline output — is built explicitly in
# the communication-focused modules.

# %% [markdown]
# ## 10. Segmentation-aware option: Targeted Placement Push
#
# Every option so far commits Fernbrook Stays to the *same campaign across its entire
# portfolio*. But Fernbrook Stays can observe which markets are currently Strong, Average,
# or Weak using the Inside Airbnb data — and could target its spend accordingly.
#
# **Targeted Placement Push**: run Featured Placement Push only in currently-Strong markets,
# Neighborhood Concierge Bundle in Average markets, and Hold in Weak markets.

# %%
payoffs.loc["Targeted Placement Push"] = {"Strong": 5.5, "Average": 1.4, "Weak": -0.9}
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
# **All three rules now agree on Targeted Placement Push.** The uniform options
# force Fernbrook Stays to either accept the full -$5.5M downside
# (Featured Placement Push) or cap the upside (Neighborhood Concierge Bundle). Targeted Placement Push
# sidesteps that tradeoff: by concentrating the expensive campaign where it is most
# likely to pay off and limiting exposure elsewhere, it captures most of
# Featured Placement Push's upside while cutting its worst-case loss substantially.
#
# This mirrors a broader "segmentation beats uniform strategy" idea: targeting
# spend using an observable signal can dominate a one-size-fits-all choice on
# all three decision metrics at once.
