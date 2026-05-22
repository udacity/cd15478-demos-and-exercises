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
# `binary_thinking_simulation_solution.ipynb`. The canonical artifact for learners is
# the notebook (.ipynb); this script is provided for code review and `git diff`
# readability. Run `jupytext --sync` to keep the two in lockstep after edits.

# %% [markdown]
# # When "Probably" Isn't the Same as "Definitely" (SOLUTION)
#
# ## Scenario
#
# A new analyst joining Pitch & Slate Music's Growth team has a question: why don't we just run
# promotion campaigns for every genre with a hit rate above 50%? Those are the likely
# winners. You've been asked to show her why the 50% threshold is the wrong one —
# using real Spotify track data and a bit of arithmetic.
#
# Each genre targets a distinct listener audience, so promotional slots aren't
# interchangeable. The decision per genre is simply: take the 100 slots it offers, or
# leave them empty.
#
# ## What this notebook delivers
#
# 1. Real genre hit rates derived from Spotify track data.
# 2. The break-even hit rate — the minimum hit rate for a campaign to cover its costs.
# 3. A concrete simulation: how often does the "likely winner" (Pop, 54%) actually miss?
# 4. A concrete simulation: how often does the "unlikely" genre (R&B, 37%) actually hit —
#    and does it make money when it does?
# 5. One simulated season per strategy, showing the dollar difference for that draw.
# 6. The average profit per strategy — plain multiplication, no randomness needed.
# 7. A takeaway on what rounding probabilities actually costs.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "../binary-thinking-simulation-starter/data/spotify_tracks_sample.csv"

HIT_THRESHOLD    = 50    # Spotify popularity ≥ this = "hit"
NET_GAIN_K       = 15    # net gain per campaign if track hits ($K)
COST_K           = 8     # cost per campaign if track misses ($K)
BINARY_THRESHOLD = 0.50  # the new analyst's proposed rule: hit rate > 50% → run campaign
N_PER_GENRE      = 100   # promotion slots per genre per season

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. Load real track data and compute genre hit rates

# %%
tracks = pd.read_csv(DATA_PATH)
tracks["is_hit"] = (tracks["track_popularity"] >= HIT_THRESHOLD).astype(int)

genre_stats = (
    tracks.groupby("playlist_genre")["is_hit"]
    .agg(n="count", hit_rate="mean")
    .reset_index()
    .sort_values("hit_rate")
    .reset_index(drop=True)
)
genre_stats["hit_rate"] = genre_stats["hit_rate"].round(3)
genre_stats

# %% [markdown]
# Genre hit rates span from 18.8% (EDM) to 54.0% (Pop). Only Pop clears the 50%
# threshold — so the proposed rule would skip R&B (37.2%), Rap (41.5%),
# Rock (46.2%), and Latin (48.0%) entirely.

# %% [markdown]
# ## 2. Compute the break-even hit rate
#
# The proposed 50% threshold has nothing to do with whether a campaign is profitable.
# The right question is: at what hit rate do the revenues from hits exactly cover the
# cost of misses?
#
# `p × NET_GAIN_K = (1 − p) × COST_K`  →  `p = COST_K / (COST_K + NET_GAIN_K)`
#
# Any genre above this rate turns a profit; any genre below it loses money.

# %%
BREAK_EVEN = COST_K / (COST_K + NET_GAIN_K)

print(f"Break-even hit rate:         {BREAK_EVEN:.1%}")
print(f"New analyst's threshold:     {BINARY_THRESHOLD:.0%}")
print()

genre_stats["binary_runs"]    = genre_stats["hit_rate"] > BINARY_THRESHOLD
genre_stats["profitable_runs"] = genre_stats["hit_rate"] > BREAK_EVEN

disagreement = genre_stats[genre_stats["profitable_runs"] & ~genre_stats["binary_runs"]]
print("Disagreement zone — profitable by the payoff math, skipped by the 50% rule:")
disagreement[["playlist_genre", "hit_rate"]]

# %% [markdown]
# The break-even is 34.8%, not 50%. R&B (37.2%), Rap (41.5%), Rock (46.2%),
# and Latin (48.0%) all cover their costs but fall below the 50% threshold —
# every one is a profitable campaign that the proposed rule rejects.

# %% [markdown]
# ## 3. The certainty illusion — simulate 100 Pop campaigns
#
# Pop has a 54% hit rate, so the proposed rule runs it — treating this as "it'll work."
# Let's see what the simulation actually produces across 100 campaigns.

# %%
pop_rate = genre_stats.loc[genre_stats["playlist_genre"] == "pop", "hit_rate"].values[0]
pop_outcomes = RNG.binomial(1, pop_rate, N_PER_GENRE)

pop_hits   = int(pop_outcomes.sum())
pop_misses = N_PER_GENRE - pop_hits

print(f"Pop hit rate: {pop_rate:.1%}  (proposed rule: 'above 50% — it'll work')")
print()
print(f"Simulated result across {N_PER_GENRE} campaigns:")
print(f"  Hits:   {pop_hits}  (revenue: +${pop_hits * NET_GAIN_K:,}K)")
print(f"  Misses: {pop_misses}  (cost:    −${pop_misses * COST_K:,}K)")
print()
print(f"The proposed rule treats Pop as a near-certainty.")
print(f"Reality: {pop_misses} out of {N_PER_GENRE} campaigns missed.")

# %% [markdown]
# A 54% hit rate means roughly 46 misses in every 100 campaigns on average. The 50%
# rule doesn't eliminate that uncertainty — it just stops the team from thinking about it.

# %% [markdown]
# ## 4. The missed opportunity — simulate 100 R&B campaigns
#
# R&B has a 37% hit rate, so the proposed rule skips it — treating this as "it won't
# happen." But the relevant question isn't whether 37% sounds likely. It's whether
# a 37% hit rate is enough to turn a profit given the payoff structure.

# %%
rb_rate = genre_stats.loc[genre_stats["playlist_genre"] == "r&b", "hit_rate"].values[0]
rb_outcomes = RNG.binomial(1, rb_rate, N_PER_GENRE)

rb_hits   = int(rb_outcomes.sum())
rb_misses = N_PER_GENRE - rb_hits

# Does 37% cover costs? Revenue from hits minus cost of misses:
rb_avg_per_campaign = rb_rate * NET_GAIN_K - (1 - rb_rate) * COST_K

print(f"R&B hit rate: {rb_rate:.1%}  (proposed rule: 'below 50% — won't happen')")
print()
print(f"Simulated result across {N_PER_GENRE} campaigns:")
print(f"  Hits:   {rb_hits}  (+${rb_hits * NET_GAIN_K:,}K)")
print(f"  Misses: {rb_misses}  (−${rb_misses * COST_K:,}K)")
print(f"  Net:    ${rb_hits * NET_GAIN_K - rb_misses * COST_K:+,}K")
print()
print(f"Profit per R&B campaign on average: ${rb_avg_per_campaign:.1f}K")
print(f"By skipping R&B, the team left roughly ${rb_avg_per_campaign * N_PER_GENRE:,.0f}K on the table.")

# %% [markdown]
# A 37% hit rate is not zero — it means roughly 37 profitable hits per 100 campaigns.
# Because the payoff is asymmetric ($15K gain vs. $8K cost), 37% is enough to turn a
# profit. The 50% rule threw away $56K by treating "less than 50%" as "won't happen."

# %% [markdown]
# ## 5. One simulated season per strategy
#
# A "season" is N_PER_GENRE campaigns per genre that the strategy decides to run.
# Binary strategy: Pop only (above 50%).
# Payoff-aware strategy: every genre above the break-even (all except EDM).
# This is one random draw — results vary each run.

# %%
def simulate_season(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    """Return total season profit ($K) for a set of genres with given hit rates."""
    hits   = RNG.binomial(n_per_genre, hit_rates)
    misses = n_per_genre - hits
    return float((hits * NET_GAIN_K - misses * COST_K).sum())


binary_hit_rates  = genre_stats.loc[genre_stats["binary_runs"],    "hit_rate"].values
payoff_hit_rates  = genre_stats.loc[genre_stats["profitable_runs"], "hit_rate"].values

binary_season = simulate_season(binary_hit_rates)
payoff_season = simulate_season(payoff_hit_rates)

print(f"One simulated season:")
print(f"  Binary strategy      (Pop only):                   ${binary_season:,.0f}K")
print(f"  Payoff-aware strategy (R&B, Rap, Rock, Latin, Pop): ${payoff_season:,.0f}K")
print(f"  Difference this season:                            ${payoff_season - binary_season:+,.0f}K")
print()
print("This is one random draw. Step 6 shows why the gap is consistent, not just lucky.")

# %% [markdown]
# ## 6. Average profit per strategy — why the gap is consistent
#
# The single-season result varies. But the average profit over many seasons is just
# multiplication — no randomness needed. For any genre with hit rate `p` and `n`
# campaigns:
#
# `average profit = n × (p × NET_GAIN_K − (1 − p) × COST_K)`
#
# This is: fraction of campaigns that hit × gain, minus fraction that miss × cost.

# %%
def average_season_profit(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    """Return average season profit ($K) — multiplication only, no randomness."""
    profit_per_genre = hit_rates * NET_GAIN_K - (1 - hit_rates) * COST_K
    return float((profit_per_genre * n_per_genre).sum())


binary_avg = average_season_profit(binary_hit_rates)
payoff_avg = average_season_profit(payoff_hit_rates)

print("Average profit per genre (payoff-aware strategy):")
for _, row in genre_stats[genre_stats["profitable_runs"]].iterrows():
    avg = N_PER_GENRE * (row["hit_rate"] * NET_GAIN_K - (1 - row["hit_rate"]) * COST_K)
    print(f"  {row['playlist_genre']:<6}  hit rate {row['hit_rate']:.1%}  →  ${avg:+,.0f}K")

print()
print(f"Binary strategy average season profit:        ${binary_avg:,.0f}K  (Pop only)")
print(f"Payoff-aware strategy average season profit:  ${payoff_avg:,.0f}K")
print(f"Consistent gap:                               ${payoff_avg - binary_avg:,.0f}K per season")

# %% [markdown]
# The ~$775K gap is not luck — it's the sum of four genres the 50% rule rejected, each
# of which covers its costs on its own. The payoff-aware strategy captures them every
# season. R&B adds only ~$56K individually, but the 50% rule discards it every time
# simply because 37% sounds unlikely.

# %% [markdown]
# ## 7. Takeaway

# %% [markdown]
# **What the simulations revealed:** Pop (54%) missed roughly 46 times in 100. R&B
# (37%) hit roughly 37 times in 100 — and those 37 hits more than paid for the 63
# misses. The 50% rule gets both of these wrong: it treats 54% as a near-certainty
# and 37% as impossible. Neither is true.
#
# **Why the average profit matters:** The simulated season (step 5) was one random
# draw that varied. The arithmetic in step 6 is the same every time — ~$775K per
# season in foregone profit from four genres the 50% rule silently skipped. That gap
# is the cost of using the wrong threshold.
#
# **The key lesson:** The question is not "is this genre above 50%?" The question is
# "does this genre cover its costs?" Those are different questions with different
# answers. The break-even hit rate for this payoff structure is 34.8%. Any threshold
# that ignores the payoff math will leave money on the table.
