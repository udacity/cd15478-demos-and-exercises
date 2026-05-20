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
# A new analyst joining WaveForm's Growth team has a question: why don't we just run
# promotion campaigns for every genre with a hit rate above 50%? Those are the likely
# winners. You've been asked to show her why the 50% threshold is the wrong one — using
# real Spotify track data and a bit of arithmetic.
#
# Each genre targets a distinct listener audience, so promotional slots aren't
# interchangeable. The decision per genre is simply: take the 100 slots it offers, or
# leave them empty.
#
# ## What this notebook delivers
#
# 1. Real genre hit rates derived from Spotify track data.
# 2. The break-even hit rate from the payoff structure.
# 3. A concrete simulation of the certainty illusion: how often does a "likely" genre miss?
# 4. A concrete simulation of the missed opportunity: how often does a "unlikely" genre hit?
# 5. One simulated season per strategy, showing the dollar difference.
# 6. The analytical expected profit per strategy — plain multiplication, no loops.
# 7. A takeaway on what rounding probabilities actually costs.
#
# The deliverable stops at the analytical layer. It does not produce a stakeholder recommendation.

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
BINARY_THRESHOLD = 0.50  # WaveForm's current rule: hit rate > 50% → run campaign
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
# binary threshold — so WaveForm's current rule would skip R&B (37.2%), Rap (41.5%),
# Rock (46.2%), and Latin (48.0%) entirely.

# %% [markdown]
# ## 2. Compute the break-even hit rate
#
# A campaign has non-negative expected value when the hit rate exceeds the break-even:
# `p × NET_GAIN_K − (1 − p) × COST_K ≥ 0`, which solves to
# `p ≥ COST_K / (COST_K + NET_GAIN_K)`.

# %%
BREAK_EVEN = COST_K / (COST_K + NET_GAIN_K)

print(f"Break-even hit rate:          {BREAK_EVEN:.1%}")
print(f"WaveForm's binary threshold:  {BINARY_THRESHOLD:.0%}")
print()

genre_stats["binary_runs"] = genre_stats["hit_rate"] > BINARY_THRESHOLD
genre_stats["ev_runs"]     = genre_stats["hit_rate"] > BREAK_EVEN

disagreement = genre_stats[genre_stats["ev_runs"] & ~genre_stats["binary_runs"]]
print("Disagreement zone — EV says run, binary says skip:")
disagreement[["playlist_genre", "hit_rate"]]

# %% [markdown]
# The break-even is 34.8%, well below 50%. R&B (37.2%), Rap (41.5%), Rock (46.2%),
# and Latin (48.0%) all clear the break-even but fall below the binary threshold —
# every one is an EV-positive campaign that the binary rule rejects.

# %% [markdown]
# ## 3. The certainty illusion — simulate 100 Pop campaigns
#
# WaveForm's rule approves Pop (54% hit rate) because it's above 50%. In practice the
# team thinks of this as "it'll work." Let's see what actually happens when we simulate
# 100 Pop promotion campaigns.

# %%
pop_rate = genre_stats.loc[genre_stats["playlist_genre"] == "pop", "hit_rate"].values[0]
pop_outcomes = RNG.binomial(1, pop_rate, N_PER_GENRE)

pop_hits   = int(pop_outcomes.sum())
pop_misses = N_PER_GENRE - pop_hits

print(f"Pop hit rate: {pop_rate:.1%}  (binary thinking: 'above 50% — it'll work')")
print()
print(f"Simulated result across {N_PER_GENRE} campaigns:")
print(f"  Hits:   {pop_hits}  (revenue: +${pop_hits * NET_GAIN_K:,}K)")
print(f"  Misses: {pop_misses}  (cost:    −${pop_misses * COST_K:,}K)")
print()
print(f"Binary thinking treats Pop as a near-certainty.")
print(f"Reality: {pop_misses} out of {N_PER_GENRE} campaigns missed — even though it was the 'safe' choice.")

# %% [markdown]
# A 54% hit rate means 46 misses in every 100 campaigns on average. The binary rule
# doesn't eliminate that uncertainty — it just stops the team from thinking about it.

# %% [markdown]
# ## 4. The missed opportunity — simulate 100 R&B campaigns
#
# WaveForm skips R&B entirely because 37.2% < 50%. The implicit assumption: "below
# 50% means it won't happen." Let's simulate what happens if they ran it anyway.

# %%
rb_rate = genre_stats.loc[genre_stats["playlist_genre"] == "r&b", "hit_rate"].values[0]
rb_outcomes = RNG.binomial(1, rb_rate, N_PER_GENRE)

rb_hits   = int(rb_outcomes.sum())
rb_misses = N_PER_GENRE - rb_hits

rb_ev_per_campaign = rb_rate * NET_GAIN_K - (1 - rb_rate) * COST_K

print(f"R&B hit rate: {rb_rate:.1%}  (binary thinking: 'below 50% — won't happen')")
print()
print(f"Simulated result across {N_PER_GENRE} campaigns:")
print(f"  Hits:   {rb_hits}  (revenue: +${rb_hits * NET_GAIN_K:,}K)")
print(f"  Misses: {rb_misses}  (cost:    −${rb_misses * COST_K:,}K)")
print(f"  Net:    ${rb_hits * NET_GAIN_K - rb_misses * COST_K:+,}K")
print()
print(f"Expected value per R&B campaign: ${rb_ev_per_campaign:.1f}K")
print(f"Binary thinking left an estimated ${rb_ev_per_campaign * N_PER_GENRE:,.0f}K on the table")
print(f"by treating {rb_rate:.1%} as 'won't happen.'")

# %% [markdown]
# A 37% hit rate is not zero — it means 37 hits in every 100 campaigns. Because the
# payoff is asymmetric ($15K gain vs. $8K loss), even a 35% hit rate is worth taking.
# Binary thinking conflates "less than 50%" with "won't happen" and misses the entire
# 35–50% range of EV-positive opportunities.

# %% [markdown]
# ## 5. One simulated season per strategy
#
# A "season" is 100 promotion campaigns per genre. Binary strategy runs only Pop.
# EV-aware strategy runs every genre above the break-even (all except EDM).
# Each outcome is one random draw — a single season will vary from the expected value.

# %%
def simulate_season(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    """Return total season profit ($K) for a set of genres with given hit rates."""
    hits   = RNG.binomial(n_per_genre, hit_rates)
    misses = n_per_genre - hits
    return float((hits * NET_GAIN_K - misses * COST_K).sum())


binary_hit_rates = genre_stats.loc[genre_stats["binary_runs"], "hit_rate"].values
ev_hit_rates     = genre_stats.loc[genre_stats["ev_runs"],     "hit_rate"].values

binary_season = simulate_season(binary_hit_rates)
ev_season     = simulate_season(ev_hit_rates)

print(f"One simulated season:")
print(f"  Binary strategy   (Pop only):                ${binary_season:,.0f}K")
print(f"  EV-aware strategy (R&B, Rap, Rock, Latin, Pop): ${ev_season:,.0f}K")
print(f"  Difference this season:                      ${ev_season - binary_season:+,.0f}K")
print()
print(f"This is one random draw. Step 6 shows the systematic expected gap.")

# %% [markdown]
# ## 6. Analytical expected profit — why the gap is systematic
#
# The single-season result varies with each run. But the expected profit is deterministic:
# for any genre with hit rate `p`, running `N` campaigns yields an expected profit of
# `N × (p × NET_GAIN_K − (1 − p) × COST_K)`. No simulation needed.

# %%
def expected_season_profit(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    """Return expected season profit ($K) — analytical, no randomness."""
    ev_per_genre = hit_rates * NET_GAIN_K - (1 - hit_rates) * COST_K
    return float((ev_per_genre * n_per_genre).sum())


binary_ev = expected_season_profit(binary_hit_rates)
ev_ev     = expected_season_profit(ev_hit_rates)

# Show the per-genre breakdown for the EV-aware strategy
print("Expected profit per genre (EV-aware strategy):")
for _, row in genre_stats[genre_stats["ev_runs"]].iterrows():
    ev_per = N_PER_GENRE * (row["hit_rate"] * NET_GAIN_K - (1 - row["hit_rate"]) * COST_K)
    print(f"  {row['playlist_genre']:<6}  hit rate {row['hit_rate']:.1%}  →  ${ev_per:+,.0f}K expected")

print()
print(f"Binary strategy expected season profit:    ${binary_ev:,.0f}K  (Pop only)")
print(f"EV-aware strategy expected season profit:  ${ev_ev:,.0f}K")
print(f"Systematic gap:                            ${ev_ev - binary_ev:,.0f}K per season")

# %% [markdown]
# The gap (~$775K per season) is not luck — it's the predictable cost of skipping four
# genres whose hit rates are above the break-even. Each of those genres has positive
# expected value; binary thinking discards that value by rounding their probabilities to zero.
#
# Note that R&B (37.2% hit rate) has only ~$56K expected profit per 100 campaigns — small
# individually, but the EV-aware strategy captures it consistently, every season. That is
# the difference between probability as information and probability as a binary verdict.

# %% [markdown]
# ## 7. Takeaway

# %% [markdown]
# **What the simulations reveal:** Steps 3 and 4 showed that "54% means it'll work" and
# "37% means it won't happen" are both wrong. Pop misses roughly 46 times in every 100
# campaigns. R&B hits roughly 37 times. The binary threshold doesn't describe reality —
# it describes a mental shortcut that discards the probability estimate as soon as it's
# been checked against 50%.
#
# **Why the analytical calculation matters more than the single season:** Step 5 gave one
# random outcome. Step 6 showed the systematic expected gap: ~$775K per season, every
# season, regardless of luck. That gap is the cost of the mental shortcut — not a fluke.
#
# **The deeper lesson:** The 50% threshold wasn't chosen because it's the economic
# break-even. It was chosen because "above 50% sounds like it'll work." The break-even
# for this payoff structure is 34.8%, not 50%. Any threshold that ignores the payoff
# math is not a decision rule — it's a guess dressed up as a rule.

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
