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

# %% [markdown]
# # Comparing Marketing Campaigns with Expected Utility
#
# **Scenario.** You are the lead decision scientist at **Key & Quarter Hosts**
# a small short-term-rental management firm. Growth wants to launch
# a campaign next quarter to acquire new property owners. Three options are on
# the table — *Premium Listing Push*, *Local Concierge Add-on*, and *Hold*.
# Each pays off differently depending on how strong the broader short-term-rental
# market is over the next three months, which is uncertain.
#
# You will use **city-level Inside Airbnb summary statistics** to estimate the
# probability of Strong / Average / Weak market environments, then compare the
# three options on three decision rules:
#
# 1. Expected value (EV).
# 2. Expected CRRA utility under risk aversion.
# 3. Minimax regret.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the dataset
# citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "data/airbnb_city_stats.csv"

# %% [markdown]
# ## 1. Load the data
#
# Load `airbnb_city_stats.csv`. Print the first few rows to make sure it loaded
# cleanly.

# %%
# TODO: Read the CSV into a DataFrame called `cities`.
cities = ...

# %% [markdown]
# ## 2. Compute a per-listing monthly revenue proxy
#
# For each city, compute `revenue_proxy = median_price_usd ×
# median_reviews_per_month`. This is a coarse but defensible per-listing
# monthly revenue indicator: it combines what hosts charge per night with how
# often guests are booking and reviewing.

# %%
# TODO: Add a column `revenue_proxy` to `cities`.

# %% [markdown]
# ## 3. Classify each city into Strong / Average / Weak by tertile
#
# Using the **tertiles** (33rd and 67th percentiles) of `revenue_proxy`, label
# each city as one of:
#
# - `"Strong"` if `revenue_proxy` ≥ 67th percentile,
# - `"Average"` if 33rd percentile ≤ `revenue_proxy` < 67th percentile,
# - `"Weak"` if `revenue_proxy` < 33rd percentile.

# %%
# TODO: Compute the 33rd and 67th percentile cutoffs for revenue_proxy.
t33 = ...
t67 = ...

# TODO: Add a column `environment` to `cities` with values
# "Strong" / "Average" / "Weak".

# %% [markdown]
# ## 4. Estimate the empirical probability of each environment
#
# The probability of each environment is the share of cities that fell into it.
# Save the three probabilities into a Series `p` indexed by
# `["Strong", "Average", "Weak"]`. Confirm that the three values sum to 1.

# %%
# TODO: Build the probability Series `p`.
p = ...

# %% [markdown]
# ## 5. Define the payoff matrix
#
# Use the values from the *Payoff matrix* table in `INSTRUCTIONS.md`. Build a
# DataFrame `payoffs` with one row per option and one column per environment.
# Profits are in $M of incremental 12-month contribution profit relative to Hold.

# %%
# TODO: Build a DataFrame `payoffs` with rows = options, columns = environments.
payoffs = ...

# %% [markdown]
# ## 6. Expected value per option
#
# For each option, compute the expected profit using the empirical probabilities
# from step 4. Identify the EV-maximizing option.

# %%
# TODO: Compute `ev`, a Series of expected profits indexed by option.
ev = ...

# TODO: Print the EV table and the EV-maximizing option.

# %% [markdown]
# ## 7. Expected CRRA utility per option
#
# Use a CRRA utility function with risk-aversion parameter γ = 2 and a wealth
# baseline of $50M:
#
# $$u(x) = \frac{(W + x)^{1 - \gamma} - 1}{1 - \gamma}$$
#
# Compute the **expected utility** of each option, then back out the
# **certainty-equivalent profit** — the constant profit the decision-maker would
# accept in lieu of the gamble. For γ = 2, the certainty-equivalent of a gamble
# with expected utility $\bar{u}$ is $\frac{1}{1 - \bar{u}} - W$.
#
# Identify the option that maximizes expected utility.

# %%
GAMMA = 2.0
WEALTH_M = 50.0


# TODO: Implement the CRRA utility function.
def crra_utility(profit_m, gamma: float = GAMMA, wealth_m: float = WEALTH_M):
    """Return CRRA utility evaluated at (wealth_m + profit_m).

    Parameters
    ----------
    profit_m : float or array-like
        Incremental profit in $M.
    gamma : float
        Coefficient of relative risk aversion.
    wealth_m : float
        Wealth baseline in $M.
    """
    ...

# TODO: Build a utility table the same shape as `payoffs`, take the
# probability-weighted mean across columns to get expected utility per option,
# and convert to a certainty-equivalent profit.
expected_utility = ...
certainty_equivalent = ...

# TODO: Print the CE-equivalent profits and the utility-maximizing option.

# %% [markdown]
# ## 8. Minimax regret per option
#
# For each environment, compute the regret of each option — the gap between the
# best option's profit in that environment and this option's profit. Then take
# the *maximum* regret across environments for each option. The minimax-regret
# rule recommends the option with the smallest maximum regret.

# %%
# TODO: Compute a `regret` DataFrame the same shape as `payoffs` and
# `max_regret`, a Series of the row-wise maxima.
regret = ...
max_regret = ...

# TODO: Print the max-regret table and the minimax-regret option.

# %% [markdown]
# ## 9. Compare the three decision rules
#
# Produce a side-by-side comparison of the three rules — EV-max,
# expected-utility-max (with the certainty-equivalent in dollars), and
# minimax-regret — showing which option each one selects. If the three rules
# disagree, identify in 1–2 sentences which rule you would lean on and why.
#
# **Do not yet convert this comparison into a recommendation to a
# stakeholder.** The skill of translating analytical output into a
# stakeholder-facing recommendation is a separate skill covered in other modules. Today's
# deliverable is the comparison itself plus your defended choice of decision
# rule.

# %%
# TODO: Build a small DataFrame that shows, for each rule, the option it
# selects and the score that produced the choice (EV in $M, CE-profit in $M,
# max regret in $M).
comparison = ...

# %% [markdown]
# *TODO: write your 1–2 sentence defended-choice paragraph here.*

# %% [markdown]
# ## 10. Segmentation-aware option: Selective Push
#
# So far, every option commits Key & Quarter Hosts to a *single uniform campaign* across its
# whole portfolio. But Key & Quarter Hosts can observe which markets are *currently* in Strong,
# Average, or Weak condition from the Inside Airbnb data — and could target its
# campaign spend accordingly.
#
# **Selective Push**: run Premium Listing Push only in the currently-Strong markets,
# Local Concierge Add-on in Average markets, and Hold in Weak markets. Use the
# stipulated payoffs from the [Selective Push payoffs] table in `INSTRUCTIONS.md`.
#
# Add Selective Push to the payoff matrix and recompute all three decision metrics.
# Then produce an updated four-option comparison table. In 1–2 sentences, explain
# what the result implies about uniform versus segmented campaign strategies.

# %%
# TODO: Extend `payoffs` with a "Selective Push" row using the stipulated values.
#       (Strong = +6.0, Average = +1.5, Weak = -1.0)

# TODO: Recompute ev, expected_utility, certainty_equivalent, max_regret for
#       all four options. Build an updated comparison DataFrame.
comparison4 = ...

# %% [markdown]
# *TODO: write your 1–2 sentence interpretation of the Selective Push result here.*
