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
# # When "Probably" Becomes "Definitely"
# ## Simulating the Cost of Probability Rounding
#
# When a weather app says **60% chance of rain**, most people round up mentally: *"It's going to rain."*
# When it says **35%**, they round down: *"It won't rain."*
#
# This feels like common sense — it turns a messy number into a clear action. But rounding comes with a hidden, predictable cost.
#
# This exercise simulates what happens when you treat probabilities as binary facts, and shows how the error rate follows directly from the math.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import matplotlib.pyplot as plt

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. Rounding up: "60% means it will rain"
#
# The app shows **60% chance of rain**. Binary thinking rounds up: *"It's going to rain — I'll cancel the picnic."*
#
# Simulate 1,000 days where the true rain probability is 60%.
# How many of those days stay dry — making binary thinking wrong?

# %%
n_days = 1_000
p_rain = 0.60

# TODO: Simulate n_days outcomes where each day has probability p_rain of rain.
#       Count rainy and dry days.
#       Print what binary thinking predicts vs. what the simulation shows.
outcomes = ...

# %%
# TODO: Build a bar chart with two bars: "Rainy (binary right)" and "Dry (binary wrong)".
#       Color the "wrong" bar orange (#e07b54) and the "right" bar gray (#cccccc).
#       Annotate each bar with its count and percentage.

# %% [markdown]
# ## 2. Rounding down: "35% means it won't rain"
#
# Now the app shows **35% chance of rain**. Binary thinking rounds down: *"It probably won't rain — no need for an umbrella."*
#
# Simulate 1,000 days at 35% true rain probability.
# How many of those days actually rain — leaving you without an umbrella?

# %%
p_rain_low = 0.35

# TODO: Simulate n_days outcomes at p_rain_low. Count rainy and dry days.
#       Print what binary thinking predicts vs. reality.
outcomes_low = ...

# %%
# TODO: Build the same bar chart as section 1, but for the 40% case.
#       This time "Dry" is binary-right and "Rainy" is binary-wrong (orange).

# %% [markdown]
# ## 3. The cost of getting it wrong — errors aren't equal
#
# The error rate treats every wrong prediction as equally bad. But the two types of mistake have very different costs:
#
# - **Caught without an umbrella** (predicted dry, it rained): ruined commute, soaked bag — call it **$15**
# - **Carried an umbrella for nothing** (predicted rain, it stayed dry): minor inconvenience — call it **$5**
#
# Given those costs, what's the expected cost per day of binary thinking? And what threshold would a cost-aware decision-maker actually use?

# %%
cost_wet     = 15   # cost when caught without umbrella in rain
cost_useless =  5   # cost of carrying umbrella on a dry day

probabilities = [p / 100 for p in range(5, 96, 5)]
binary_costs  = []
optimal_costs = []

# TODO: Derive the cost-aware optimal threshold.
#       Hint: bring umbrella when  p × cost_wet > (1-p) × cost_useless
#       Solve for p and assign to optimal_threshold.
optimal_threshold = ...

# TODO: Loop over probabilities. For each p:
#         - Simulate 1,000 days.
#         - Compute binary_cost:
#             if p > 0.5: predicted rain → wrong when dry → cost = dry_count × (-cost_useless)
#             else:       predicted dry  → wrong when rain → cost = rainy_count × (-cost_wet)
#           Append cost / 1_000 to binary_costs.
#         - Compute opt_cost using optimal_threshold the same way.
#           Append to optimal_costs.
# Then print the optimal threshold and plot both cost curves vs. probability.
# Shade the gap between 25% and 50% where the strategies differ.

# %% [markdown]
# ## 4. The forecaster's wet bias — and whether it accidentally helps
#
# Forecasters face the same asymmetric cost structure as users, but from the opposite side: underpredicting rain (leaving users soaked and angry) costs them more reputationally than overpredicting (users carry an unnecessary umbrella and shrug). So some forecast providers apply a **wet bias** — deliberately inflating rain probabilities, especially at the low end. A model estimate of 5% might be published as ~20%.
#
# Simulate three strategies across all probability levels and compare their expected daily cost:
# 1. **Binary thinking on true probabilities** — threshold at 50%
# 2. **Binary thinking on wet-biased forecast** — threshold at 50%, applied to inflated numbers
# 3. **Cost-optimal strategy** — threshold at 25%, applied to true probabilities

# %%
inflation = 0.15   # wet bias factor: true 5% → reported ~19%

probabilities       = [p / 100 for p in range(5, 96, 5)]
binary_true_costs   = []
binary_biased_costs = []
optimal_costs_s4    = []

# TODO: For each p in probabilities:
#   1. Simulate 1,000 days at true probability p.
#   2. Compute biased_p = min(1.0, p + inflation * (1 - p))
#   3. Compute expected cost for each of three strategies (same pattern as section 3):
#        Strategy 1: binary on p         — bring umbrella if p > 0.5
#        Strategy 2: binary on biased_p  — bring umbrella if biased_p > 0.5
#        Strategy 3: cost-optimal on p   — bring umbrella if p > optimal_threshold
#      For each: cost = dry_count × (-cost_useless) if bringing umbrella,
#                       rainy_count × (-cost_wet) if not.
#   4. Append cost / 1_000 to the respective list.
#
# Then derive biased_effective_threshold algebraically:
#   biased_p > 0.5  →  p + inflation*(1-p) > 0.5  →  solve for p
# Print all three effective thresholds.
biased_effective_threshold = ...

# %%
# TODO: Plot all three cost curves on a single chart.
#       Colors: orange (#e07b54) for binary-true,
#               purple (#c084fc) for binary-biased,
#               steelblue for cost-optimal.
#       Add vertical dashed lines at each strategy's effective threshold.
#       Label x-axis "True rain probability (%)" and y-axis "Expected cost ($)".
#       Add a legend and a light horizontal line at y=0.

# %% [markdown]
# ## 5. Takeaway
#
# *TODO: Write 3–4 sentences covering the three layers of distortion. Use specific numbers:
# what is the wet bias inflation factor, what does it do to a 5% estimate, what is the
# cost-optimal threshold and why, and what is the wet-biased effective threshold?
# End with one sentence connecting this pattern to a non-weather domain (finance, health,
# project planning).*
