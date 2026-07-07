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
# When it says **40%**, they round down: *"It won't rain."*
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
# ## 2. Rounding down: "40% means it won't rain"
#
# Now the app shows **40% chance of rain**. Binary thinking rounds down: *"It probably won't rain — no need for an umbrella."*
#
# Simulate 1,000 days at 40% true rain probability.
# How many of those days actually rain — leaving you without an umbrella?

# %%
p_rain_low = 0.40

# TODO: Simulate n_days outcomes at p_rain_low. Count rainy and dry days.
#       Print what binary thinking predicts vs. reality.
outcomes_low = ...

# %%
# TODO: Build the same bar chart as section 1, but for the 40% case.
#       This time "Dry" is binary-right and "Rainy" is binary-wrong (orange).

# %% [markdown]
# ## 3. The rounding curve — error rate at every probability
#
# Sections 1 and 2 showed two specific points. Now let's see the full picture.
#
# For any forecast probability `p`:
# - If `p > 0.50` → binary thinking predicts rain → wrong when it stays dry, probability `1 - p`
# - If `p ≤ 0.50` → binary thinking predicts dry → wrong when it rains, probability `p`
#
# Simulate 1,000 days at each probability level from 5% to 95%.
# Plot the binary-thinking error rate across the full range.

# %%
probabilities = [p / 100 for p in range(5, 96, 5)]
error_rates   = []

# TODO: Loop over probabilities. For each p:
#         - Simulate 1,000 days at that probability.
#         - Compute the binary-thinking error rate:
#             if p > 0.5: binary predicts rain → error rate = fraction of dry days
#             if p ≤ 0.5: binary predicts dry  → error rate = fraction of rainy days
#         - Append to error_rates.
# Then plot error_rates vs. probabilities (as percentages).
# Add a vertical dashed line at 50% and label the axes.

# %% [markdown]
# ## 4. A month of forecasts — where does rounding go wrong?
#
# Real forecasts change day to day. Simulate a 30-day month where each day's true rain probability is drawn uniformly between 20% and 80%.
#
# For each day:
# 1. Simulate whether it actually rains.
# 2. Record what a binary thinker would predict (rain if forecast > 50%, dry otherwise).
# 3. Count and visualize the binary thinker's errors.

# %%
n_forecast_days = 30

# TODO: Draw n_forecast_days true probabilities from Uniform(0.20, 0.80).
#       Simulate whether it actually rained each day.
#       Compute binary_predictions: 1 if forecast > 0.50, else 0.
#       Count and print binary_errors.
true_probs      = ...
actually_rained = ...

# %%
days   = range(1, n_forecast_days + 1)
colors = ['#e07b54' if err else '#cccccc'
          for err in (binary_predictions != actually_rained)]

# TODO: Build a two-panel chart (sharex=True):
#   Top panel: bar chart of forecast probabilities per day, colored orange where
#              binary thinking was wrong and gray where it was right.
#              Add a horizontal dashed line at 50%.
#   Bottom panel: bar chart of actual rain outcomes, with a step line overlaid
#                 showing binary_predictions. Add a legend.

# %% [markdown]
# ## 5. Takeaway
#
# *TODO: Write 2–3 sentences. What are the two things that went wrong with binary thinking?
# Use specific numbers from steps 1–4 — what is the error rate for a 60% forecast?
# A 40% forecast? Where do errors cluster in a month of forecasts?*
