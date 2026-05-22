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
# **The scenario.** A friend of yours wants to break into sports journalism. After some
# research, you find that candidates who apply to open roles at sports outlets have roughly
# a 3% chance of receiving an offer. Your friend is discouraged: *"3% is basically zero —
# why bother applying?"* This exercise will show, through simulation, exactly why that
# reasoning is wrong.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import matplotlib.pyplot as plt
import math

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. The bias in action — one application at 3%
#
# Binary thinking predicts: *"3% is basically zero — it won't happen."*
# Imagine 100 candidates each sending one application at a 3% offer rate.
# How often is binary thinking wrong?

# %%
# TODO: Simulate 100 single-application outcomes at a 3% offer rate.
#       Compute the empirical offer rate.
#       Print what binary thinking predicts and what the simulation shows.
single_outcomes = ...

# %%
# TODO: Build a bar chart showing the number of offers vs no-offers.
#       Label each bar with its count and percentage.
#       Annotate the offer bar to note what binary thinking predicted.

# %% [markdown]
# ## 2. The overconfidence mirror — spamming applications at 55%
#
# Your friend is also spamming applications to a less exciting but highly in-demand role
# with a 55% per-application offer rate. *"That one's above 50% — it will definitely work out."*
# Imagine 1,000 candidates each sending one application. How often does that certainty fail?

# %%
# TODO: Simulate 1,000 single-application outcomes at a 55% offer rate.
#       Compute the empirical failure rate.
#       Print what binary thinking predicts and how often it is wrong.
high_outcomes = ...

# %%
# TODO: Build a bar chart showing the number of offers vs no-offers.
#       Same style as step 1. Annotate the no-offer bar.

# %% [markdown]
# ## 3. Stack the applications
#
# Binary thinking about 30 applications at 3%: *"None of these will pan out."*
# Simulate 100 full job searches — each sending 30 applications at 3% — and
# look at the distribution of offers received.

# %%
# TODO: Simulate 100 job searches of 30 applications each at a 3% offer rate.
search_outcomes = ...

# %%
# TODO: Plot a histogram of offer counts across all searches.
#       Highlight the zero-offer bar and annotate it.

# %% [markdown]
# ## 4. P(at least one offer)
#
# The histogram shows the distribution — but the number your friend cares about
# is simpler: what fraction of those 100 searches ended with at least one offer?
# Compare sending 1 application to sending 30.

# %%
# TODO: Compute P(at least one offer) from search_outcomes and analytically.
#       Print both values.

# TODO: Build a bar chart comparing P(offer) for 1 application vs 30 applications.
#       Add a reference line at 0.5. Label axes and title clearly.

# %% [markdown]
# ## 5. Find your number
#
# How many applications does it take to reach 90% confidence of at least one offer?
# Solve analytically, then verify with simulation.

# %%
# TODO: Solve analytically for the minimum number of applications
#       needed to reach 90% confidence of at least one offer.
#       Verify by simulating searches of that length.
n_needed = ...

# %% [markdown]
# ## 6. Takeaway
#
# *TODO: Write 2–3 sentences. What does binary thinking get wrong here?
# Use specific numbers from steps 1–5 to support your answer.*
