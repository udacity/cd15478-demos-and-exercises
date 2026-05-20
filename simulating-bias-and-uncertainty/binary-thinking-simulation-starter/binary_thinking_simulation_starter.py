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
# promotion campaigns each season. Their editorial team uses a simple rule: if a
# genre's hit rate looks above 50%, run a campaign; otherwise skip it.
#
# You'll use real Spotify track data to measure what genre hit rates actually look
# like, then simulate two kinds of mistakes that rule causes: the certainty illusion
# (treating 54% as a guarantee) and the missed opportunity (treating 37% as
# impossible). Then you'll use plain arithmetic to show why the gap between the
# two strategies is systematic — not just bad luck.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the dataset citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH        = "data/spotify_tracks_sample.csv"

HIT_THRESHOLD    = 50    # Spotify popularity ≥ this = "hit"
NET_GAIN_K       = 15    # net gain per campaign if track hits ($K)
COST_K           = 8     # cost per campaign if track misses ($K)
BINARY_THRESHOLD = 0.50  # WaveForm's current rule: hit rate > 50% → run campaign
N_PER_GENRE      = 100   # promotion slots per genre per season

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
# A campaign has non-negative expected value when:
# `p × NET_GAIN_K − (1 − p) × COST_K ≥ 0`
# Solve for the minimum `p` (the break-even hit rate).

# %%
# TODO: Compute BREAK_EVEN from NET_GAIN_K and COST_K. Do not hardcode it.
BREAK_EVEN = ...

print(f"Break-even hit rate:         {BREAK_EVEN:.1%}")
print(f"WaveForm's binary threshold: {BINARY_THRESHOLD:.0%}")
print()

# TODO: Add two boolean columns to genre_stats:
#   `binary_runs` — True if hit_rate > BINARY_THRESHOLD
#   `ev_runs`     — True if hit_rate > BREAK_EVEN
genre_stats["binary_runs"] = ...
genre_stats["ev_runs"]     = ...

# TODO: Print the disagreement zone — genres EV says run but binary says skip.
disagreement = ...
print("Disagreement zone (EV says run, binary says skip):")
disagreement[["playlist_genre", "hit_rate"]]

# %% [markdown]
# ## 3. The certainty illusion — simulate 100 Pop campaigns
#
# Pop has a 54% hit rate — the only genre above the 50% binary threshold.
# WaveForm's rule treats this as "it'll work." Simulate 100 Pop promotion campaigns
# using `RNG.binomial(1, rate, N_PER_GENRE)` and count how many miss.

# %%
# TODO: Extract Pop's hit rate from genre_stats.
pop_rate = ...

# TODO: Simulate N_PER_GENRE Pop campaigns. Count hits and misses.
pop_outcomes = ...
pop_hits   = ...
pop_misses = ...

print(f"Pop hit rate: {pop_rate:.1%}  (binary thinking: 'above 50% — it'll work')")
print(f"\nSimulated result across {N_PER_GENRE} campaigns:")
print(f"  Hits:   {pop_hits}")
print(f"  Misses: {pop_misses}")

# TODO: In 1 sentence, explain what the miss count reveals about treating 54% as certainty.

# %% [markdown]
# ## 4. The missed opportunity — simulate 100 R&B campaigns
#
# R&B has a 37% hit rate — below 50%, so WaveForm skips it. But 37% is not zero.
# Simulate 100 R&B campaigns and count how many hit. Then compute the expected
# value of one R&B campaign to show whether skipping it was the right call.

# %%
# TODO: Extract R&B's hit rate from genre_stats.
rb_rate = ...

# TODO: Simulate N_PER_GENRE R&B campaigns. Count hits and misses.
rb_outcomes = ...
rb_hits   = ...
rb_misses = ...

# TODO: Compute the expected value per R&B campaign and the total expected profit
#       WaveForm left on the table by skipping 100 R&B campaigns.
rb_ev_per_campaign = ...

print(f"R&B hit rate: {rb_rate:.1%}  (binary thinking: 'below 50% — won't happen')")
print(f"\nSimulated result across {N_PER_GENRE} campaigns:")
print(f"  Hits:   {rb_hits}")
print(f"  Misses: {rb_misses}")
print(f"\nExpected value per R&B campaign: ${rb_ev_per_campaign:.1f}K")

# TODO: In 1 sentence, explain what the result reveals about treating 37% as impossible.

# %% [markdown]
# ## 5. One simulated season per strategy
#
# A "season" is N_PER_GENRE campaigns per genre that the strategy runs.
# Implement `simulate_season`, then compare one simulated season for each strategy.

# %%
# TODO: Implement simulate_season(hit_rates, n_per_genre).
#       Use RNG.binomial to draw campaign outcomes, then compute total profit.
def simulate_season(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    """Return total season profit ($K) for a set of genres with given hit rates."""
    ...


# TODO: Run simulate_season for each strategy and print the dollar difference.
binary_hit_rates = genre_stats.loc[genre_stats["binary_runs"], "hit_rate"].values
ev_hit_rates     = genre_stats.loc[genre_stats["ev_runs"],     "hit_rate"].values

binary_season = simulate_season(binary_hit_rates)
ev_season     = simulate_season(ev_hit_rates)

print(f"One simulated season:")
print(f"  Binary strategy:   ${binary_season:,.0f}K")
print(f"  EV-aware strategy: ${ev_season:,.0f}K")
print(f"  Difference:        ${ev_season - binary_season:+,.0f}K")

# %% [markdown]
# ## 6. Analytical expected profit — why the gap is systematic
#
# One season is one random draw. The expected profit is deterministic:
# for a genre with hit rate `p` and `n` campaigns,
# expected profit = `n × (p × NET_GAIN_K − (1 − p) × COST_K)`.
#
# Implement `expected_season_profit` and compute it for each strategy.
# This is plain arithmetic — no simulation needed.

# %%
# TODO: Implement expected_season_profit(hit_rates, n_per_genre).
#       No randomness — just multiply hit rates through the payoff formula.
def expected_season_profit(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    """Return expected season profit ($K) — analytical, no randomness."""
    ...


binary_ev = expected_season_profit(binary_hit_rates)
ev_ev     = expected_season_profit(ev_hit_rates)

print(f"Binary strategy expected season profit:    ${binary_ev:,.0f}K")
print(f"EV-aware strategy expected season profit:  ${ev_ev:,.0f}K")
print(f"Systematic gap:                            ${ev_ev - binary_ev:,.0f}K per season")

# %% [markdown]
# ## 7. Takeaway
#
# *TODO: Write 2–3 sentences. Use specific numbers from steps 3–6. Explain:*
# - *What the coin-flip simulations (steps 3–4) revealed about binary thinking.*
# - *Why the analytical gap (step 6) matters more than the single-season result (step 5).*

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
