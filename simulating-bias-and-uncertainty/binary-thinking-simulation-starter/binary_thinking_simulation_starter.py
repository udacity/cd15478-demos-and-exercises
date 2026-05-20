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
# # When "Probably" Isn't the Same as "Definitely"
#
# **Scenario.** WaveForm, a fictional music streaming platform, runs genre-focused
# promotion campaigns each season. Their editorial team uses a simple rule:
# if a genre's hit rate looks above 50%, run a campaign; otherwise skip it.
# You'll use real Spotify track data to measure what genre hit rates actually look
# like, simulate what that 50% rule costs compared to a strategy that uses the full
# probability, and quantify the certainty illusion — the gap between "above 50%
# so it'll work" and what actually happens.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the dataset citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/spotify_tracks_sample.csv"

HIT_THRESHOLD = 50      # Spotify popularity ≥ this = "hit"
NET_GAIN_K = 15         # net gain per campaign if track hits ($K)
COST_K = 8              # cost per campaign if track misses ($K)
BINARY_THRESHOLD = 0.50 # WaveForm's current rule: hit rate > 50% → run campaign
N_PER_GENRE = 100       # promotion slots allocated to each genre per season
N_SIMS = 2_000          # Monte Carlo seasons to simulate

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. Load real track data and compute genre hit rates
#
# Load the Spotify track sample, classify each track as a hit or miss based on
# `track_popularity`, and compute each genre's hit rate from the data.

# %%
# TODO: Read the CSV into a DataFrame called `tracks`.
tracks = ...

# TODO: Add a column `is_hit`: 1 if track_popularity >= HIT_THRESHOLD, else 0.

# TODO: Compute `genre_stats` — a DataFrame with one row per genre containing
#       at least `hit_rate` (the proportion of tracks that are hits) and `n` (count).
#       Sort by hit_rate ascending.
genre_stats = ...

genre_stats

# %% [markdown]
# ## 2. Compute the break-even hit rate
#
# For a campaign to be worth running, its expected value must be positive.
# Derive the break-even hit rate from the payoff structure at the top of this notebook.

# %%
# TODO: Compute BREAK_EVEN — the minimum hit rate at which a campaign has non-negative EV.
#       Derive it from NET_GAIN_K and COST_K; do not hardcode a number.
BREAK_EVEN = ...

print(f"Break-even hit rate: {BREAK_EVEN:.1%}")
print(f"WaveForm's current threshold: {BINARY_THRESHOLD:.0%}")
print()

# TODO: Add two boolean columns to genre_stats:
#   `binary_runs` — True if WaveForm's current rule would run this genre (hit_rate > BINARY_THRESHOLD)
#   `ev_runs`     — True if the EV-aware rule would run this genre (hit_rate > BREAK_EVEN)
genre_stats["binary_runs"] = ...
genre_stats["ev_runs"] = ...

# TODO: Print the disagreement zone — genres EV-aware strategy runs but binary strategy skips.
disagreement = ...
print("Disagreement zone (EV says run, binary says skip):")
print(disagreement[["playlist_genre", "hit_rate", "ev_runs", "binary_runs"]])

# %% [markdown]
# ## 3. Simulate one season — binary strategy
#
# A "season" is 100 promotion campaigns per genre that the strategy decides to run.
# Each campaign's outcome is a random draw: the track hits with probability equal to
# that genre's real hit rate.
#
# Simulate one season under the binary strategy (run only genres above 50%) and
# compute total season profit.

# %%
# TODO: Write a function `simulate_season(hit_rates, n_per_genre)` that takes an
#       array of hit rates and the number of campaigns per genre, and returns
#       total profit in $K across all genres and campaigns.
#       Use RNG.binomial for the random draws.
def simulate_season(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    """Return total season profit ($K) for a set of genres with given hit rates."""
    # TODO: implement
    ...


# TODO: Extract the hit rates for genres the binary strategy runs.
binary_hit_rates = ...

# TODO: Simulate one season and print the result.
binary_season_profit = simulate_season(binary_hit_rates)
print(f"Binary strategy — one season: ${binary_season_profit:,.0f}K profit")
print(f"  Genres run: {(genre_stats['binary_runs']).sum()}")

# %% [markdown]
# ## 4. Simulate one season — EV-aware strategy
#
# Same structure, but the EV-aware strategy runs all genres above the break-even hit rate.

# %%
# TODO: Extract hit rates for genres the EV-aware strategy runs.
ev_hit_rates = ...

# TODO: Simulate one season and print the result.
ev_season_profit = simulate_season(ev_hit_rates)
print(f"EV-aware strategy — one season: ${ev_season_profit:,.0f}K profit")
print(f"  Genres run: {(genre_stats['ev_runs']).sum()}")

# %% [markdown]
# ## 5. Run 2,000 Monte Carlo seasons and compare distributions
#
# One season is just one draw. Run 2,000 simulations of each strategy to see the
# full distribution of seasonal profits.

# %%
# TODO: Simulate N_SIMS seasons for each strategy.
#       Store results as 1-D NumPy arrays `binary_profits` and `ev_profits`.
binary_profits = ...
ev_profits = ...

print(f"Binary  — mean: ${binary_profits.mean():,.0f}K, std: ${binary_profits.std():,.0f}K")
print(f"EV-aware — mean: ${ev_profits.mean():,.0f}K, std: ${ev_profits.std():,.0f}K")
print(f"Average gap: ${ev_profits.mean() - binary_profits.mean():,.0f}K per season")

# %% [markdown]
# ### Visualize the two profit distributions

# %%
# TODO: Plot overlapping histograms of binary_profits and ev_profits.
#       Add vertical lines for the mean of each distribution.
#       Label axes, add a title and legend.

# %% [markdown]
# ## 6. The certainty illusion
#
# The binary strategy runs genres above 50% on the assumption that they "will work."
# What fraction of those campaigns actually miss?

# %%
# TODO: For genres the binary strategy runs, compute the average miss rate
#       (i.e., 1 - hit_rate) and compare it to what binary thinking implies (0%).
#
# Then print a short comparison: what did binary thinking assume, and what does
# the data show?

# %% [markdown]
# ## 7. Takeaway
#
# *TODO: Write 2–3 sentences summarizing what the simulation reveals about rounding
# probabilities to 0 or 1. Name at least one specific genre (e.g., R&B, Rock) and
# quantify the economic consequence of treating its hit rate as "won't happen."*

# %% [markdown]
# ---
# ## Connecting forward: what this means for the Nimbus project
#
# In the capstone project, you'll analyze a pricing decision for **Nimbus Streaming**,
# a fictional 4M-subscriber video service. At every step of that analysis — estimating
# churn probability from pilot data, computing expected revenue impact under different
# price scenarios, running sensitivity tests — you'll be working with probability
# estimates that sit in the same uncertain 30–60% range you just simulated.
#
# The biases you quantified here don't disappear just because the analysis is more
# sophisticated. An analyst who thinks "we have a 54% chance this price increase pays
# off, so it'll pay off" is making the same mistake as WaveForm's editorial team.
# The decision framework you'll build in the project exists precisely to avoid that:
# to make recommendations that are grounded in the full uncertainty — the hit rate
# *and* the miss rate — not a rounded-up certainty.
