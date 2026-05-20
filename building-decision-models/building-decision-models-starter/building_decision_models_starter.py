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
# `building_decision_models_starter.ipynb`. The canonical artifact for learners
# is the notebook (.ipynb); this script is provided for code review and
# `git diff` readability. Run `jupytext --sync` to keep the two in lockstep
# after edits.

# %% [markdown]
# # Building and Solving Decision Models Programmatically
#
# **Scenario.** You are the lead decision scientist at **StrideWear**, a
# fictional athletic apparel brand. The company must commit now to a go-to-market
# strategy for a new performance running shoe launching in 12 months. Three
# options are on the table: **Full Launch** (broad multi-channel, $600K
# marketing), **Regional Launch** (selective rollout, $200K marketing), and
# **Hold** (delay one season). How well any option performs depends on the
# strength of the athletic footwear retail market — uncertain at this horizon.
#
# You will load real US sporting goods sales data, classify historical months
# into demand states, build a payoff matrix, compute expected value and minimax
# regret, visualize the decision tree, and finish with a sensitivity flex —
# *not* a stakeholder-facing recommendation.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the
# dataset citation.

# %% [markdown]
# ## Setup

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_PATH = "data/sporting_goods_sales.csv"

# Module-level constants for the payoff matrix ($ millions, incremental vs Hold)
PAYOFF_FULL_LOW    = -7.0
PAYOFF_FULL_BASE   =  4.0
PAYOFF_FULL_HIGH   = 12.0
PAYOFF_REGIONAL_LOW    = -0.5
PAYOFF_REGIONAL_BASE   =  2.0
PAYOFF_REGIONAL_HIGH   =  5.5

# %% [markdown]
# ## 1. Load and inspect the data
#
# Read `sporting_goods_sales.csv` into a DataFrame. Inspect the first and last
# few rows so you know what columns are present.

# %%
# TODO: Read the CSV into a DataFrame called `sales`. Parse the DATE column as
#       datetime and set it as the index.
sales = ...

# %% [markdown]
# ## 2. Compute year-over-year growth rates
#
# The demand state depends on how much sales grew (or fell) relative to the
# same month one year earlier. Use a 12-period lag to compute the year-over-year
# percentage change, then drop any rows where the growth rate is NaN.

# %%
# TODO: Add a column `yoy` to `sales` with the 12-month percentage change in
#       MRTSSM45111USS. Then drop NaN rows and store the result in `sales`.
sales["yoy"] = ...
sales = ...

print(f"Months with YoY data: {len(sales)}")
display(sales[["MRTSSM45111USS", "yoy"]].head())

# %% [markdown]
# ## 3. Classify each month into a demand state
#
# Tertile-bin the YoY growth rate column into three equal groups:
# **Low** (bottom third), **Base** (middle third), and **High** (top third).
# The 33rd and 67th percentiles of `yoy` are the cut-points. Record those
# cut-points — they describe what "Low" vs "Base" vs "High" means in numbers.

# %%
# TODO: Compute the 33rd and 67th percentiles of sales["yoy"].
Q33 = ...
Q67 = ...

print(f"33rd-percentile cut (Low | Base): {Q33:.2f}%")
print(f"67th-percentile cut (Base | High): {Q67:.2f}%")

# TODO: Add a column `state` to `sales` using pd.cut with bins
#       [-inf, Q33, Q67, inf] and labels ["Low", "Base", "High"].
sales["state"] = ...

display(sales[["MRTSSM45111USS", "yoy", "state"]].tail(12))

# %% [markdown]
# ## 4. Derive demand-state probabilities
#
# Because you used tertile binning, each bin contains roughly one-third of the
# observations. Use `pd.Series` indexed by state name so the probability vector
# aligns with the payoff matrix you'll build next.
#
# By construction, the exact values will be 1/3 each (or very close to it —
# rounding depends on whether the dataset length is divisible by 3). Use the
# exact fraction 1/3 in the probability vector so downstream EV calculations
# are clean.

# %%
# TODO: Build a pd.Series called `p` with equal 1/3 probability for each state.
#       Index: ["Low", "Base", "High"]
p = ...

print("Demand-state probability vector:")
print(p)
print(f"Sum: {p.sum():.3f}")

# Confirm the empirical counts are close to 1/3 each.
counts = sales["state"].value_counts().sort_index()
print("\nEmpirical counts per state:")
print(counts)

# %% [markdown]
# ## 5. Define the payoff matrix
#
# Use the values from the INSTRUCTIONS payoff table. Build a `pd.DataFrame`
# with options as rows (index) and demand states as columns.

# %%
# TODO: Build `payoffs` as a pd.DataFrame.
#       Rows: Full Launch, Regional Launch, Hold
#       Columns: Low, Base, High
#       Values: from the module-level constants defined in Setup.
payoffs = ...

print("Payoff matrix ($M incremental profit vs Hold):")
display(payoffs)

# %% [markdown]
# ## 6. Expected value per option
#
# Expected value is the probability-weighted average payoff.
# `(payoffs * p).sum(axis=1)` multiplies each column of `payoffs` by the
# corresponding probability and sums across states for each option.

# %%
# TODO: Compute `ev` as a pd.Series with one EV per option.
ev = ...

print("Expected value per option ($M):")
display(ev.round(3).to_frame("EV ($M)"))
print(f"\nEV-maximizing option: {ev.idxmax()}  (EV = ${ev.max():.2f}M)")

# %% [markdown]
# ## 7. Minimax regret per option
#
# Regret for a given (option, state) pair is the difference between the best
# possible payoff in that state and the payoff this option actually delivers.
# Minimax regret selects the option whose *worst-case regret* is smallest.

# %%
# TODO: Compute `best_per_state` — the maximum payoff across options in each
#       state (axis=0 maximum of payoffs).
best_per_state = ...

# TODO: Compute `regret` — the regret matrix (best_per_state - payoffs).
regret = ...

# TODO: Compute `max_regret` — the worst-case (row-wise max) regret per option.
max_regret = ...

print("Regret matrix ($M):")
display(regret)
print("\nMax regret per option ($M):")
display(max_regret.round(3).to_frame("Max regret ($M)"))
print(f"\nMinimax-regret option: {max_regret.idxmin()}  "
      f"(max regret = ${max_regret.min():.2f}M)")

# %% [markdown]
# ## 8. Decision tree visualization
#
# Draw a simple decision tree: a root node for the decision, one branch per
# option, and one leaf per demand state showing the payoff. Use matplotlib
# annotations with `boxstyle="round"` bounding boxes.

# %%
fig, ax = plt.subplots(figsize=(12, 7))
ax.axis("off")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# TODO: Build the decision tree visualization.
#
# Suggested layout:
#   - Root node at (1, 5) labeled "Decision\n(StrideWear)"
#   - Three option branches at x=4 at y positions 8, 5, 2 for
#     Full Launch, Regional Launch, Hold
#   - Three state leaves at x=8 per option branch, spread 1 unit apart
#     in y, labeled with state name and payoff ($M)
#
# Use ax.annotate() with arrowprops=dict(arrowstyle="->") for arrows
# and bbox=dict(boxstyle="round", fc="...") for node boxes.
# Color suggestion: root=lightyellow, options=lightblue, states=lightgreen.

# Root node
ROOT_X, ROOT_Y = 1.0, 5.0
OPTION_X = 4.0
LEAF_X = 8.0

# TODO: Draw root node annotation.

# TODO: Loop over options and states to draw branches and leaves.
#       Use payoffs and p defined above.

ax.set_title("StrideWear Launch Decision Tree", fontsize=14, pad=12)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 9. Compare the decision rules
#
# Build a side-by-side summary of what each rule selects, then write your
# 1–2 sentence defended choice.
#
# **Do not convert this into a recommendation to a stakeholder.** The deliverable
# stops at the defended-rule level.

# %%
# TODO: Build a comparison DataFrame with rows for EV-max and Minimax regret,
#       and columns for "Selected option" and "Score".
comparison = ...

display(comparison)

# %% [markdown]
# *TODO: Write your 1–2 sentence defended-choice paragraph here. Name the
# decision rule, explain the tradeoff in plain language, and do not attempt a
# stakeholder-facing recommendation.*

# %% [markdown]
# ## 10. Sensitivity flex — pessimistic demand weights
#
# Recompute EV under the assumption that the next 12 months are more likely
# to be weak than the historical baseline suggests:
# P(Low) = 0.5, P(Base) = 0.3, P(High) = 0.2.
# Report whether the EV-max option changes.

# %%
# TODO: Build `p_pess` as a pd.Series with the pessimistic weights.
p_pess = ...

# TODO: Recompute EV under the pessimistic weights using the same payoffs.
ev_pess = ...

print("EV per option under pessimistic demand weights ($M):")
display(ev_pess.round(3).to_frame("EV pess ($M)"))
print(f"\nEV-max under pessimistic weights: {ev_pess.idxmax()}  "
      f"(${ev_pess.max():.2f}M)")
print(f"EV-max under baseline weights:    {ev.idxmax()}  "
      f"(${ev.max():.2f}M)")

# %% [markdown]
# *TODO: Write one sentence summarizing what changed and what the sensitivity
# result implies for confidence in the baseline EV-max choice.*

# %% [markdown]
# ---
# ## Nimbus Streaming — How this exercise prepares Step 6
#
# The Nimbus Streaming capstone project asks you to complete **Step 6: Decision
# tree (options × posterior states, backward induction)**. That step mirrors
# everything you built here:
#
# - The probability vector over demand states (Low / Base / High) comes from
#   tertile-binning a posterior distribution — the same `pd.Series` pattern
#   you used in Step 4.
# - The payoff matrix uses the same `pd.DataFrame` layout (options as rows,
#   states as columns) and the same EV formula `(payoffs * p).sum(axis=1)`.
# - The decision tree visualization uses the same matplotlib annotation
#   approach with `boxstyle="round"` nodes.
# - The minimax regret calculation is identical in structure.
#
# The main differences in the project: four options instead of three, and the
# payoff values are derived from Nimbus's own cost-benefit model rather than
# stipulated. The code patterns transfer directly.
