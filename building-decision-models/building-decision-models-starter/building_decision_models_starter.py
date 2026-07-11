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
# **Scenario.** Trailmark Outdoor Co.'s VP of Product Strategy has described three
# options for the Ridge Runner launch in plain English — not as a table. Your job is
# to turn that description into a Python decision model: define the structure, write
# the payoff function, build the tree, and solve it under two decision rules.
#
# See `INSTRUCTIONS.md` for the scenario narrative and `data/README.md` for the
# dataset citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DATA_PATH = "data/sporting_goods_sales.csv"

# %% [markdown]
# ## 1. Derive state probabilities from real market data
#
# Use the historical sales data to estimate how likely each demand environment is.
#
# 1. Load the data
# 2. Derive a growth metric from the sales column
# 3. Define two thresholds that divide months into three demand states (High / Base / Low)
# 4. Estimate the probability of each state from the historical data

# %%
# TODO: Load the CSV into `sales`. The columns are `date` and `sales_m`.
sales = ...

# TODO: Compute `yoy` — the year-over-year % change in `sales_m`. Drop NaN rows.

# TODO: Compute two thresholds that divide `yoy` into three equal-frequency bins.
t33, t67 = ...

# TODO: Classify each month as "High", "Base", or "Low" using those thresholds.

# TODO: Build `STATES` — a dict mapping state name → empirical probability.
#       (Each should be close to 1/3 by construction.)
STATES = ...

print("State probabilities:")
for state, prob in STATES.items():
    print(f"  {state}: {prob:.3f}")

# %% [markdown]
# ## 2. Influence diagram — map the structure before writing any code
#
# Before defining options or writing a payoff function, draw the dependency structure
# of the decision. An influence diagram uses three node types:
#
# - **Rectangle** — Decision node: a variable *you* control
# - **Oval** — Uncertainty node: an uncertain variable nature controls
# - **Rounded rectangle** — Value node: the payoff that depends on both
#
# The three nodes are drawn below. Add the two arrows, then answer the reflection.

# %%
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
ax.set_title("Influence diagram — Trailmark Outdoor Co. Ridge Runner launch decision", pad=10)

# Decision node — rectangle (top-left)
ax.add_patch(mpatches.FancyBboxPatch(
    (0.3, 2.8), 2.8, 1.6, boxstyle="square,pad=0.05",
    fc="#dde8ff", ec="#555", lw=1.5, zorder=2))
ax.text(1.7, 3.8, "Launch Option", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(1.7, 3.3, "National / Regional Test / Hold", ha="center", va="center", fontsize=8, color="#333")
ax.text(1.7, 2.95, "Decision node", ha="center", va="center", fontsize=7.5, color="#666", style="italic")

# Uncertainty node — oval (top-right)
ax.add_patch(mpatches.Ellipse(
    (8.2, 3.6), 2.8, 1.6, fc="#fff3cc", ec="#555", lw=1.5, zorder=2))
ax.text(8.2, 3.8, "Demand State", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(8.2, 3.3, "High / Base / Low", ha="center", va="center", fontsize=8, color="#333")
ax.text(8.2, 2.95, "Uncertainty node", ha="center", va="center", fontsize=7.5, color="#666", style="italic")

# Value node — octagon (bottom-center)
import numpy as np
ax.add_patch(mpatches.RegularPolygon(
    (5.0, 1.3), numVertices=8, radius=1.1, orientation=np.pi/8,
    fc="#d4edda", ec="#555", lw=1.5, zorder=2))
ax.text(5.0, 1.55, "12-Month Profit ($M)", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(5.0, 1.1, "option_profit(option, state)", ha="center", va="center",
        fontsize=7.5, color="#333", family="monospace")
ax.text(5.0, 0.65, "Value node", ha="center", va="center", fontsize=7.5, color="#666", style="italic")

# TODO: Add two arrows — one from the Decision node to the Value node,
#       and one from the Uncertainty node to the Value node.

plt.tight_layout()
plt.show()

# %% [markdown]
# *TODO: There is no arrow between the Decision node and the Chance node. In 1–2
# sentences, what does that absence assume about the relationship between Trailmark
# Outdoor Co.'s launch choice and the demand environment? When might that assumption
# be wrong?*

# %% [markdown]
# ## 3. Define the structure
#
# Read the VP of Product Strategy's description in `INSTRUCTIONS.md` and define:
# - `OPTIONS` — a list of the three option names, exactly as strings
# - Module-level constants for each option's cost and revenue by state

# %%
OPTIONS = ...  # TODO: fill in from the narrative

# TODO: Define business parameters as module-level constants.
#       Name them clearly so option_profit can reference them by name.
NATIONAL_LAUNCH_COST_M = ...
NATIONAL_LAUNCH_REV_M  = ...

REGIONAL_TEST_COST_M   = ...
REGIONAL_TEST_REV_M    = ...

# %% [markdown]
# ## 4. Implement `option_profit`
#
# Write the function that the rest of the model depends on. It takes an option name
# and a demand state name and returns the net 12-month profit in $M.
# Reference module-level constants only — no hardcoded numbers in the function body.

# %%
def option_profit(option: str, demand_state: str) -> float:
    """Net 12-month profit ($M) for a given option and demand state."""
    # TODO: implement for "National Launch", "Regional Test Launch", and "Hold"
    ...


# Quick sanity check — uncomment once the function is implemented:
# print(option_profit("National Launch", "High"))       # should be ~12.3
# print(option_profit("Regional Test Launch", "Low"))   # should be ~0.45
# print(option_profit("Hold", "Base"))                  # should be 0.0

# %% [markdown]
# ## 5. Build the payoff matrix
#
# Call `option_profit` across every option × state combination to produce
# a DataFrame with options as rows and demand states as columns.

# %%
# TODO: Build `payoffs` — a pd.DataFrame — by calling option_profit for each
#       (option, state) pair. Do not type the values in by hand.
payoffs = ...

payoffs

# %% [markdown]
# ## 6. Expected value per option

# %%
# TODO: Compute `ev` — a pd.Series of expected profits, one per option.
ev = ...

print("Expected value per option ($M):")
print(ev.round(2))
print(f"\nEV-maximizing option: {ev.idxmax()}  (${ev.max():.2f}M)")

# %% [markdown]
# ## 7. Expected CRRA utility
#
# A risk-neutral decision maker maximises expected value. A risk-averse one maximises
# **expected utility** — a concave transformation of payoff that penalises losses more
# heavily than equally-sized gains.
#
# Use **CRRA (Constant Relative Risk Aversion)** utility with risk aversion
# coefficient γ = 2, evaluated at total wealth rather than incremental profit:
#
# `u(profit) = ((W + profit)^(1 − γ) − 1) / (1 − γ)`
#
# The wealth baseline W = $20M represents Trailmark Outdoor Co.'s assumed existing
# scale. Applying utility to (W + profit) rather than to raw profit keeps the function
# well-defined even when incremental profit is negative, and means risk aversion is
# measured relative to the firm's total position — not just the project in isolation.

# %%
GAMMA    = 2.0
WEALTH_M = 20.0   # Trailmark Outdoor Co.'s assumed baseline wealth ($M)

# TODO: Implement the CRRA utility function.
def utility(profit_m: float) -> float:
    """CRRA utility evaluated at (WEALTH_M + profit_m)."""
    ...

# TODO: Compute `eu` — a pd.Series of expected utility per option — by
#       probability-weighting `utility(option_profit(opt, s))` over states.
eu = ...

# TODO: Convert `eu` to a certainty-equivalent profit `ce` by inverting the
#       CRRA function: ce_wealth = (eu * (1 - GAMMA) + 1) ** (1 / (1 - GAMMA));
#       ce = ce_wealth - WEALTH_M
ce = ...

print(f"EV-maximizing option: {ev.idxmax()}  (EV = ${ev.max():.2f}M)")
print(f"CE-maximizing option: {ce.idxmax()}  (CE = ${ce.max():.2f}M)")

# %% [markdown]
# ## 8. Decision tree — backward induction (rollback)
#
# Draw the tree: one root decision node, one branch per option, one sub-branch per
# demand state. Roll back both EV and the certainty-equivalent profit to the decision
# node for each option, and highlight which option each criterion recommends.
#
# When you're done, compare this tree to the influence diagram in step 2 — the diagram
# showed the structure; the tree performs the rollback. In 1–2 sentences, explain what
# it means that EV and certainty-equivalent profit disagree here.

# %%
# TODO: Build the matplotlib decision tree with EV and CE rolled back to the
#       decision node, highlighting the EV-optimal and CE-optimal branches.
