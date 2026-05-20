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
# # Structuring and Solving a Product Launch Decision
#
# **Scenario.** StrideWear's Head of Strategy has described three options for the
# Apex Trainer launch in plain English — not as a table. Your job is to turn her
# verbal description into a Python decision model: define the structure, write the
# payoff function, build the tree, and solve it.
#
# See `INSTRUCTIONS.md` for the scenario narrative and `data/README.md` for the
# dataset citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/sporting_goods_sales.csv"

# %% [markdown]
# ## 1. Derive state probabilities from real market data
#
# Load the sporting goods sales data, compute year-over-year (YoY) growth rates,
# and tertile-bin the growth rates into High / Base / Low demand states.
# The share of months in each bin gives the probability of each state.

# %%
# TODO: Load the CSV into `sales`. The columns are `date` and `sales_m`.
sales = ...

# TODO: Compute `yoy` — the year-over-year % change in `sales_m` (12-month lag).
#       Drop NaN rows produced by the shift.

# TODO: Compute the 33rd and 67th percentile thresholds of `yoy`.
t33, t67 = ...

# TODO: Classify each month as "High" (≥ t67), "Base" (t33 ≤ x < t67), or "Low" (< t33).

# TODO: Build `STATES` — a dict mapping state name → empirical probability.
#       (Each should be close to 1/3 by construction.)
STATES = ...

print("State probabilities:")
for state, prob in STATES.items():
    print(f"  {state}: {prob:.3f}")

# %% [markdown]
# ## 2. Define the structure
#
# Read the Head of Strategy's description in `INSTRUCTIONS.md` and define:
# - `OPTIONS` — a list of the three option names, exactly as strings
# - Module-level constants for each option's cost and revenue by state

# %%
OPTIONS = ...  # TODO: fill in from the narrative

# TODO: Define business parameters as module-level constants.
#       Name them clearly so option_profit can reference them by name.
FULL_LAUNCH_COST_M  = ...
FULL_LAUNCH_REV_M   = ...  # dict: {"High": ..., "Base": ..., "Low": ...}

REGIONAL_COST_M     = ...
REGIONAL_REV_M      = ...  # dict: {"High": ..., "Base": ..., "Low": ...}

# %% [markdown]
# ## 3. Implement `option_profit`
#
# Write the function that the rest of the model depends on. It takes an option name
# and a demand state name and returns the net 12-month profit in $M.
# Reference module-level constants only — no hardcoded numbers in the function body.

# %%
def option_profit(option: str, demand_state: str) -> float:
    """Net 12-month profit ($M) for a given option and demand state."""
    # TODO: implement for "Full Launch", "Regional Rollout", and "Hold"
    ...


# Quick sanity check — uncomment once the function is implemented:
# print(option_profit("Full Launch", "High"))    # should be ~11.4
# print(option_profit("Regional Rollout", "Low")) # should be ~0.3
# print(option_profit("Hold", "Base"))            # should be 0.0

# %% [markdown]
# ## 4. Build the payoff matrix
#
# Call `option_profit` across every option × state combination to produce
# a DataFrame with options as rows and demand states as columns.

# %%
# TODO: Build `payoffs` — a pd.DataFrame — by calling option_profit for each
#       (option, state) pair. Do not type the values in by hand.
payoffs = ...

payoffs

# %% [markdown]
# ## 5. Expected value per option

# %%
# TODO: Compute `ev` — a Series of expected profits indexed by option name.
#       Use (payoffs * pd.Series(STATES)).sum(axis=1).
ev = ...

print("Expected value per option ($M):")
print(ev.round(2))
print(f"\nEV-maximizing option: {ev.idxmax()}  (${ev.max():.2f}M)")

# %% [markdown]
# ## 6. Minimax regret

# %%
# TODO: Compute the regret matrix (best payoff per state minus each option's payoff)
#       and max_regret (the row-wise maximum of the regret matrix).
regret     = ...
max_regret = ...

print("Max regret per option ($M):")
print(max_regret.round(2))
print(f"\nMinimax-regret option: {max_regret.idxmin()}  "
      f"(max regret ${max_regret.min():.2f}M)")

# %% [markdown]
# ## 7. Decision tree visualization
#
# Draw the tree: one root decision node, one branch per option, one sub-branch per
# demand state, and a payoff label at each leaf.
# Use `boxstyle="round"` for the node boxes.

# %%
# TODO: Build the matplotlib tree diagram.
#       Hint: look at how the project solution draws its decision tree —
#       the structure here is the same: options × states × payoffs.

# %% [markdown]
# ## 8. Sensitivity flex
#
# Recompute EV under pessimistic demand weights:
# P(High) = 0.20, P(Base) = 0.30, P(Low) = 0.50.

# %%
STATES_PESS = {"High": 0.20, "Base": 0.30, "Low": 0.50}

# TODO: Compute ev_pess using STATES_PESS instead of STATES.
ev_pess = ...

print("EV under pessimistic weights ($M):")
print(ev_pess.round(2))
print(f"\nBase-case EV winner:       {ev.idxmax()}")
print(f"Pessimistic-case EV winner: {ev_pess.idxmax()}")

# %% [markdown]
# *TODO: Write 1–2 sentences. Does the EV-maximizing option change? Under what
# specific condition would you switch from the base-case recommendation?*

# %% [markdown]
# ---
# ## Connecting forward: what this means for the Nimbus project
#
# Step 6 of the Nimbus project follows the same pattern you just built:
# define `OPTIONS` and `STATES` (derived from the posterior distribution),
# call `option_profit(option, lift, margin, cac)` for every option × state
# combination to populate a payoff DataFrame, and draw the decision tree with
# `boxstyle="round"` node labels. The key transfer: writing `option_profit`
# as a reusable function that takes the option name and uncertain inputs as
# arguments — instead of hardcoding a table — is exactly what makes the
# project's tree extensible to new options or new state assumptions.
