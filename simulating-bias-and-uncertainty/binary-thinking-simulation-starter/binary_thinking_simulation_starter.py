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
# # The Application Numbers Game
#
# **The bias.** When people encounter a probability below 50%, they tend to treat it as
# *"it won't happen."* Above 50%, they treat it as *"it will happen."* This is called
# **binary thinking** — collapsing a probability into a yes/no prediction before the
# outcome has occurred. It feels natural, but it leads to systematically wrong decisions.
#
# **The scenario.** You have just finished a data analytics program and you are job searching.
# Each application has roughly a 20% chance of converting to an offer. Binary thinking says:
# *"20% is below 50% — it probably won't work."* This exercise will show you, through
# simulation, exactly how wrong that reasoning is.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import matplotlib.pyplot as plt
import math

P_SINGLE = 0.03    # per-application offer probability
P_HIGH   = 0.10    # per-application probability in a strong-candidate scenario
N_APPS   = 30      # applications in a typical search
N_SIMS   = 100  # simulation runs
TARGET   = 0.90    # target confidence of getting at least one offer

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. The bias in action — one application at 20%
#
# Binary thinking predicts: *"20% is below 50% — it won't happen."*
# Simulate 10,000 single applications at `P_SINGLE` and measure how often that prediction is wrong.

# %%
# TODO: Simulate N_SIMS single-application outcomes at P_SINGLE.
#       Compute the empirical offer rate.
#       Print what binary thinking predicts and what the simulation shows.
single_outcomes = ...

# %% [markdown]
# ## 2. The overconfidence mirror — one application at 75%
#
# Binary thinking predicts: *"75% is above 50% — it will happen."*
# Simulate 10,000 single applications at `P_HIGH` and count how often that prediction fails.

# %%
# TODO: Simulate N_SIMS single-application outcomes at P_HIGH.
#       Compute the empirical failure rate.
#       Print what binary thinking predicts and how often it is wrong.
high_outcomes = ...

# %% [markdown]
# ## 3. Stack the applications
#
# Binary thinking about 10 applications at 20%: *"None of these will pan out."*
# Simulate `N_SIMS` full job searches — each with `N_APPS` applications — and
# compute P(at least one offer).

# %%
# TODO: Simulate N_SIMS job searches, each with N_APPS applications at P_SINGLE.
#       Compute P(at least one offer) across all simulations.
#       Print the result alongside the binary prediction.
search_outcomes = ...

# %% [markdown]
# ## 4. The full picture
#
# Plot P(at least one offer) as a function of applications sent, for both
# `P_SINGLE` and `P_HIGH`. Add a horizontal reference line at `TARGET`.

# %%
# TODO: For n = 1 to 20, compute P(at least one offer) for P_SINGLE and P_HIGH.
#       Plot both curves. Add a reference line at TARGET. Label axes and add a legend.

# %% [markdown]
# ## 5. Find your number
#
# How many applications does it take to reach `TARGET` confidence of at least one offer?
# Solve analytically, then verify with simulation.

# %%
# TODO: Solve analytically for the minimum n where P(at least one offer) >= TARGET.
#       Verify by simulating searches of that length.
n_needed = ...

# %% [markdown]
# ## 6. Takeaway
#
# *TODO: Write 2–3 sentences. What does binary thinking get wrong here?
# Use specific numbers from steps 1–5 to support your answer.*
