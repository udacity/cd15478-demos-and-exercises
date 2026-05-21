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
# ## 8. Influence diagram
#
# A decision tree shows every path through the problem. An influence diagram shows
# the *structure* — which variables depend on which — without enumerating all paths.
#
# For this problem there are three nodes:
# - **Decision node** (rectangle): the launch option you choose
# - **Chance node** (oval): the demand state nature reveals
# - **Value node** (rounded rectangle): the resulting profit
#
# The three node shapes are drawn below. Your job is to add the two arrows and then
# answer the reflection question.

# %%
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
ax.set_title("Influence diagram — StrideWear Apex Trainer launch decision", pad=10)

# Decision node — rectangle (top-left)
ax.add_patch(mpatches.FancyBboxPatch(
    (0.3, 2.8), 2.8, 1.6, boxstyle="square,pad=0.05",
    fc="#dde8ff", ec="#555", lw=1.5, zorder=2))
ax.text(1.7, 3.8, "Launch Option", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(1.7, 3.3, "Full / Regional / Hold", ha="center", va="center", fontsize=8, color="#333")
ax.text(1.7, 2.95, "Decision node", ha="center", va="center", fontsize=7.5, color="#666", style="italic")

# Chance node — oval (top-right)
ax.add_patch(mpatches.Ellipse(
    (8.2, 3.6), 2.8, 1.6, fc="#fff3cc", ec="#555", lw=1.5, zorder=2))
ax.text(8.2, 3.8, "Demand State", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(8.2, 3.3, "High / Base / Low", ha="center", va="center", fontsize=8, color="#333")
ax.text(8.2, 2.95, "Chance node", ha="center", va="center", fontsize=7.5, color="#666", style="italic")

# Value node — rounded rectangle (bottom-center)
ax.add_patch(mpatches.FancyBboxPatch(
    (3.6, 0.5), 2.8, 1.6, boxstyle="round,pad=0.1",
    fc="#d4edda", ec="#555", lw=1.5, zorder=2))
ax.text(5.0, 1.5, "12-Month Profit ($M)", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(5.0, 1.0, "option_profit(option, state)", ha="center", va="center",
        fontsize=7.5, color="#333", family="monospace")
ax.text(5.0, 0.65, "Value node", ha="center", va="center", fontsize=7.5, color="#666", style="italic")

# TODO: Add two arrows using ax.annotate:
#   1. Decision node → Value node  (from around (2.2, 2.8) to around (4.1, 2.1))
#   2. Chance node   → Value node  (from around (7.2, 2.8) to around (5.9, 2.1))
#   Pattern: ax.annotate("", xy=<tip>, xytext=<tail>,
#                         arrowprops=dict(arrowstyle="->", lw=1.5, color="#333"))

plt.tight_layout()
plt.show()

# %% [markdown]
# *TODO: In 1–2 sentences — there is no arrow between the Decision node and the Chance
# node. What does that absence assume about the relationship between StrideWear's launch
# choice and the demand environment?*
