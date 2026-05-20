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
# `bayesian_updating_solution.ipynb`. The canonical artifact for learners is
# the notebook (.ipynb); this script is provided for code review and `git diff`
# readability. Run `jupytext --sync` to keep the two in lockstep after edits.

# %% [markdown]
# # Updating Demand Beliefs with Bayesian Methods (SOLUTION)
#
# ## Scenario
#
# FreshCart, a fictional grocery chain, pilots a Premium Meal Kit add-on and must
# pre-order from their supplier two weeks in advance. The key unknown is mean weekly
# demand per store. Using real US grocery sales data (FRED MRTSSM4451USS) to set a
# prior, and synthetic pilot scan data for two sequential updates, you'll implement
# the closed-form Normal-Normal conjugate update and translate each posterior into a
# recommended pre-order quantity.
#
# ## What this notebook delivers
#
# 1. A prior mean derived from real FRED grocery sales data.
# 2. Two sequential Normal-Normal updates (prior → Posterior 1 → Posterior 2).
# 3. A three-distribution plot showing belief sharpening.
# 4. Pre-order quantities Q under each belief state.
# 5. A sensitivity check showing how prior width affects the first update.
#
# Stops at the analytical layer — does not produce a stakeholder recommendation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

BENCH_PATH  = "../bayesian-updating-starter/data/grocery_industry_benchmarks.csv"
PILOT_PATH  = "../bayesian-updating-starter/data/pilot_scan_data.csv"

N_US_GROCERY_STORES = 38_000
MEAL_KIT_SHARE      = 0.003
AVG_MEAL_PRICE      = 12.0
PRIOR_SD            = 25.0
Q_BUFFER            = 0.5

# %% [markdown]
# ## 1. Derive the prior mean from real grocery sales data

# %%
bench = pd.read_csv(BENCH_PATH)
bench.columns = ["date", "sales_m"]
bench["date"] = pd.to_datetime(bench["date"])
bench

# %%
avg_monthly_usd_m = bench[bench["date"].dt.year >= 2022]["sales_m"].mean()
weekly_per_store  = (avg_monthly_usd_m * 1e6 / N_US_GROCERY_STORES) / 4.33
meal_kit_per_store = weekly_per_store * MEAL_KIT_SHARE
prior_mu = round((meal_kit_per_store / AVG_MEAL_PRICE) * 0.75, 1)  # 0.75 = early-stage discount

print(f"Avg monthly US grocery sales (2022-24): ${avg_monthly_usd_m:,.0f}M")
print(f"Weekly per-store sales: ${weekly_per_store:,.0f}")
print(f"Derived prior_mu (with early-stage discount): {prior_mu} units/store/week")
print(f"Prior: Demand ~ Normal({prior_mu}, {PRIOR_SD}²)")

# %% [markdown]
# ## 2. Load pilot scan data and split into two batches

# %%
pilot = pd.read_csv(PILOT_PATH)
pilot

# %%
batch1 = pilot[pilot["week"] <= 4]
batch2 = pilot[pilot["week"] > 4]

# %% [markdown]
# ## 3. Compute likelihood parameters for each batch

# %%
lik1_mu = batch1["mean_units_sold"].mean()
lik1_sd = batch1["mean_units_sold"].std(ddof=1) / np.sqrt(len(batch1))

lik2_mu = batch2["mean_units_sold"].mean()
lik2_sd = batch2["mean_units_sold"].std(ddof=1) / np.sqrt(len(batch2))

print(f"Batch 1 likelihood: mu={lik1_mu:.1f}, se={lik1_sd:.2f}")
print(f"Batch 2 likelihood: mu={lik2_mu:.1f}, se={lik2_sd:.2f}")

# %% [markdown]
# ## 4. Implement `normal_update`

# %%
def normal_update(prior_mu: float, prior_sd: float,
                  lik_mu: float, lik_sd: float) -> tuple[float, float]:
    """Conjugate Normal-Normal update. Returns (posterior_mean, posterior_sd)."""
    prior_prec = 1 / prior_sd ** 2
    lik_prec   = 1 / lik_sd ** 2
    post_var   = 1 / (prior_prec + lik_prec)
    post_mu    = post_var * (prior_prec * prior_mu + lik_prec * lik_mu)
    return post_mu, np.sqrt(post_var)

# %% [markdown]
# ## 5. First update: prior + batch 1

# %%
post1_mu, post1_sd = normal_update(prior_mu, PRIOR_SD, lik1_mu, lik1_sd)

print(f"Posterior 1: mu={post1_mu:.1f}, sd={post1_sd:.2f}")
print(f"  Sd reduced: {PRIOR_SD:.1f} → {post1_sd:.2f}")

# %% [markdown]
# ## 6. Second update: Posterior 1 + batch 2

# %%
post2_mu, post2_sd = normal_update(post1_mu, post1_sd, lik2_mu, lik2_sd)

print(f"Posterior 2: mu={post2_mu:.1f}, sd={post2_sd:.2f}")
print(f"  Sd reduced: {post1_sd:.2f} → {post2_sd:.2f}")

# %% [markdown]
# ## 7. Plot all three belief distributions

# %%
xs = np.linspace(0, 160, 600)

fig, ax = plt.subplots(figsize=(9, 4))
for label, mu, sd, ls in [
    (f"Prior  (μ={prior_mu:.0f}, σ={PRIOR_SD:.0f})",   prior_mu,  PRIOR_SD,  "--"),
    (f"Post 1 (μ={post1_mu:.1f}, σ={post1_sd:.1f})",  post1_mu,  post1_sd,  "-."),
    (f"Post 2 (μ={post2_mu:.1f}, σ={post2_sd:.1f})",  post2_mu,  post2_sd,  "-"),
]:
    ax.plot(xs, stats.norm.pdf(xs, mu, sd), ls, linewidth=2, label=label)

ax.set(title="FreshCart meal-kit demand belief — two sequential updates",
       xlabel="Weekly units per store", ylabel="Density")
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# Each update narrows the distribution and shifts the mean toward the pilot's observed
# demand (~105 units/week). The prior was wide and anchored conservatively at 80; by
# Posterior 2, almost all probability mass is between 100 and 110 units.

# %% [markdown]
# ## 8. Recommended pre-order quantity Q

# %%
Q_prior = prior_mu  + Q_BUFFER * PRIOR_SD
Q_post1 = post1_mu  + Q_BUFFER * post1_sd
Q_post2 = post2_mu  + Q_BUFFER * post2_sd

summary = pd.DataFrame({
    "belief_state":  ["Prior", "Posterior 1", "Posterior 2"],
    "mean":          [round(prior_mu, 1), round(post1_mu, 1), round(post2_mu, 1)],
    "sd":            [round(PRIOR_SD, 1), round(post1_sd, 1), round(post2_sd, 1)],
    "Q_recommended": [round(Q_prior),     round(Q_post1),     round(Q_post2)],
})
summary

# %% [markdown]
# Q rises from 92 → 97 → 107 units as evidence pushes the mean estimate up. The buffer
# itself also shrinks (0.5 × 25 = 12.5 → 0.5 × 3.0 = 1.5) because the posterior is
# tighter — FreshCart is more confident and needs less of a safety cushion.

# %% [markdown]
# ## 9. Sensitivity check: doubled prior sd

# %%
PRIOR_SD_WIDE = PRIOR_SD * 2

post1_wide_mu, post1_wide_sd = normal_update(prior_mu, PRIOR_SD_WIDE, lik1_mu, lik1_sd)

print(f"Update 1 with original prior sd ({PRIOR_SD:.0f}):  posterior mu = {post1_mu:.1f}, sd = {post1_sd:.2f}")
print(f"Update 1 with doubled prior sd  ({PRIOR_SD_WIDE:.0f}): posterior mu = {post1_wide_mu:.1f}, sd = {post1_wide_sd:.2f}")
print()
print("A wider prior assigns less precision to the prior belief, so the likelihood")
print("(batch-1 data) gets proportionally more weight. The posterior shifts closer to")
print("the batch-1 mean and arrives with a slightly different uncertainty level.")
