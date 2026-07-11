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
# # Updating Demand Beliefs with Bayesian Methods
#
# **Scenario.** Chapter & Craft, a fictional bookstore and hobby retail chain, is piloting a
# Curated Reader's Box subscription. They must place their box-assembly order with suppliers
# two weeks in advance. The key unknown is mean weekly demand per store. You'll build the
# Normal-Normal conjugate update to revise that belief twice as pilot scan data comes in, and
# translate each updated belief into a recommended pre-order quantity.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the dataset citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

BENCH_PATH  = "data/hobby_book_industry_benchmarks.csv"
PILOT_PATH  = "data/pilot_scan_data.csv"

N_US_HOBBY_BOOK_STORES = 25_000  # approximate count of US sporting goods/hobby/book stores (US Census)
BOX_SHARE              = 0.008   # curated boxes ≈ 0.8% of category spend (illustrative estimate)
AVG_BOX_PRICE          = 24.0    # average Chapter & Craft box price ($)
PRIOR_SD               = 7.0     # units — wider than historical variability; new-product uncertainty
Q_BUFFER               = 0.5     # pre-order buffer: Q = posterior_mean + Q_BUFFER × posterior_sd

# %% [markdown]
# ## 1. Derive the prior mean from real hobby/book sales data
#
# Load the FRED monthly sporting goods/hobby/book store sales data and compute the average
# weekly per-store sales for recent years. Use the box share and average price to derive prior
# mean demand in units per store per week.

# %%
# TODO: Load the benchmark CSV into a DataFrame called `bench`.
bench = ...

# TODO: Compute `avg_monthly_usd_m` — average monthly hobby/book store sales in $M for 2022-2024.
avg_monthly_usd_m = ...

# TODO: Derive `prior_mu` — mean weekly box units per store.
#   Step 1: weekly sales per store = (avg monthly $) / N_US_HOBBY_BOOK_STORES / 4.33 weeks
#   Step 2: weekly box $ per store = weekly_sales × BOX_SHARE
#   Step 3: units = box_$ / AVG_BOX_PRICE
#   Then apply an early-stage discount: multiply by 0.75 (new program, narrower reach)
prior_mu = ...

print(f"Avg monthly US hobby/book store sales (2022-24): ${avg_monthly_usd_m:,.0f}M")
print(f"Derived prior_mu: {prior_mu:.1f} units/store/week")
print(f"Prior: Demand ~ Normal({prior_mu:.1f}, {PRIOR_SD:.1f}²)")

# %% [markdown]
# ## 2. Load pilot scan data and split into two batches

# %%
# TODO: Load pilot_scan_data.csv into `pilot`. Display it.
pilot = ...

# TODO: Split into batch1 (weeks 1-4) and batch2 (weeks 5-8).
batch1 = ...
batch2 = ...

# %% [markdown]
# ## 3. Compute likelihood parameters for each batch
#
# The likelihood for each batch is summarized by the sample mean and standard error of
# the weekly unit counts.

# %%
# TODO: Compute lik1_mu, lik1_sd (mean and se of mean_units_sold in batch1).
lik1_mu = ...
lik1_sd = ...  # standard error = std(ddof=1) / sqrt(n_weeks)

# TODO: Compute lik2_mu, lik2_sd for batch2.
lik2_mu = ...
lik2_sd = ...

print(f"Batch 1 likelihood: mu={lik1_mu:.1f}, se={lik1_sd:.2f}")
print(f"Batch 2 likelihood: mu={lik2_mu:.1f}, se={lik2_sd:.2f}")

# %% [markdown]
# ## 4. Implement `normal_update`
#
# The precision of a Normal distribution is 1 / sd². The conjugate update combines
# the prior and likelihood by adding their precisions and taking a precision-weighted
# average of their means:
#
#   prior_prec = 1 / prior_sd²
#   lik_prec   = 1 / lik_sd²
#   post_prec  = prior_prec + lik_prec          (precisions add)
#   post_mu    = (prior_prec × prior_mu + lik_prec × lik_mu) / post_prec
#   post_sd    = sqrt(1 / post_prec)

# %%
# TODO: Implement normal_update using the formula above. Return (posterior_mean, posterior_sd).
def normal_update(prior_mu: float, prior_sd: float,
                  lik_mu: float, lik_sd: float) -> tuple[float, float]:
    """Conjugate Normal-Normal update. Returns (posterior_mean, posterior_sd)."""
    ...


# %% [markdown]
# ## 5. First update: prior + batch 1

# %%
# TODO: Compute post1_mu, post1_sd using normal_update.
post1_mu, post1_sd = ...

print(f"Posterior 1: mu={post1_mu:.1f}, sd={post1_sd:.2f}")
print(f"  Sd reduced from {PRIOR_SD:.1f} → {post1_sd:.2f}")

# %% [markdown]
# ## 6. Second update: Posterior 1 + batch 2

# %%
# TODO: Compute post2_mu, post2_sd using normal_update.
post2_mu, post2_sd = ...

print(f"Posterior 2: mu={post2_mu:.1f}, sd={post2_sd:.2f}")
print(f"  Sd reduced from {post1_sd:.2f} → {post2_sd:.2f}")

# %% [markdown]
# ## 7. Plot all three belief distributions

# %%
# TODO: Plot prior, Posterior 1, and Posterior 2 as Normal pdfs on one axes.
#       Add a legend and labeled axes.
#       Use scipy.stats.norm.pdf to compute the y-values.

# %% [markdown]
# ## 8. Recommended pre-order quantity Q under each belief state
#
# Q = posterior_mean + Q_BUFFER × posterior_sd
# Chapter & Craft wants a small buffer above the mean to limit stockouts, but not so large
# they risk heavy inventory waste.

# %%
# TODO: Compute Q_prior, Q_post1, Q_post2 and print them.
Q_prior = ...
Q_post1 = ...
Q_post2 = ...

# TODO: Print a summary comparing Q across all three belief states.
