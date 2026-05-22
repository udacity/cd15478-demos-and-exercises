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
# # Is Your Friend Actually Good at This?
#
# **The scenario.** Your friend claims they correctly predicted 55% of football games
# last season and made good money doing it. They have a pick for this weekend and want
# you to follow it.
#
# Binary thinking says: *"55% is above 50% — they know what they're doing, and I'll
# probably win."* This exercise runs the numbers on both claims.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import matplotlib.pyplot as plt
import math

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. One game — taking his word for it
#
# Assume your friend's 55% is completely real. Simulate 1,000 people each following
# one pick at 55%. How many lose? Build a bar chart showing the result.

# %%
# TODO: Simulate 1,000 single-game outcomes at a 55% win rate.
#       Print what binary thinking predicts and what the simulation shows.
outcomes = ...

# %%
# TODO: Build a bar chart showing losses vs wins.
#       Annotate the loss bar to show what binary thinking missed.

# %% [markdown]
# ## 2. The coin flipper problem — 20-game season
#
# Is your friend actually skilled, or just lucky? Simulate 1,000 people who pick
# games randomly (50/50) over a 20-game season. How many hit 55% or better by
# pure chance? (55% of 20 games = 11 correct.)

# %%
# TODO: Simulate 1,000 random guessers predicting 20 games each at 50%.
#       Count how many hit 11+ correct (55%+). Print the result.
random_correct = ...

# %%
# TODO: Plot a histogram of correct predictions across all 1,000 guessers.
#       Highlight bars at 11+ correct in orange. Add a vertical line at 10.5.
#       Annotate the orange zone.

# %% [markdown]
# ## 3. Does the season length matter? — 100 games
#
# Repeat the simulation with 100 games per season instead of 20.
# How often does a random guesser still hit 55%+ (55 correct out of 100)?

# %%
# TODO: Simulate 1,000 random guessers predicting 100 games each at 50%.
#       Count how many hit 55+ correct. Print the result.
random_correct_100 = ...

# %%
# TODO: Plot a histogram of correct predictions. Highlight 55+ in orange.
#       Add a vertical line at 54.5.

# %% [markdown]
# ## 4. How many games make 55% convincing?
#
# Simulate coin flippers for season lengths from 10 to 300 games (in steps of 5).
# For each length, compute the fraction of random guessers who hit 55%+.
# Plot the curve and mark the point where that fraction drops below 10%.

# %%
# TODO: For each season length in range(10, 301, 5):
#       simulate 5,000 coin flippers and compute the fraction hitting 55%+.
#       Find the first season length where that fraction drops below 10%.
#       Plot the curve with a 10% reference line and mark the threshold.
season_lengths = range(10, 301, 5)

# %% [markdown]
# ## 5. Takeaway
#
# *TODO: Write 2–3 sentences. What are the two things that went wrong with the
# original reasoning? Use specific numbers from steps 1–4.*
