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
# # From Causal Estimates to ROI: Evaluating a Career Skills Program
#
# **Scenario.** CareerBridge, a fictional nonprofit, offered a career skills program
# primarily to disadvantaged workers — people with lower pre-program earnings. That
# targeting creates confounding: participants had lower baseline earnings, so a simple
# comparison makes the program look harmful when it isn't. You'll use IPW to correct
# for the bias and translate the causal estimate into a cost-benefit ROI.
#
# Data: LaLonde (1986) job training study via the MatchIt R package (public domain).
# See `INSTRUCTIONS.md` and `data/README.md` for details.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

DATA_PATH            = "data/lalonde_participants.csv"
COST_PER_PARTICIPANT = 250    # $ to deliver the program to one participant
LTV_MULT             = 2      # earnings effect assumed to persist for 2 years
EXPERIMENTAL_BENCH   = 1_794  # known causal effect from the randomized NSW experiment ($)

COVARIATES = ["age", "educ", "married", "nodegree", "re74", "re75"]
RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. Load data and compute the naive estimate

# %%
# TODO: Load the CSV into `df`. Display the first few rows.
df = ...

# TODO: Compute the naive difference-in-means on `re78`.
naive_lift = ...
print(f"Naive earnings lift: ${naive_lift:+,.0f}")

# %% [markdown]
# ## 2. Covariate imbalance check

# %%
# TODO: Implement standardized_mean_diff(df, var, treat="treat") following the
#       project's formula: (treated_mean - control_mean) / pooled_SD.
def standardized_mean_diff(df: pd.DataFrame, var: str, treat: str = "treat") -> float:
    """Standardized mean difference between treated and control groups."""
    ...


# TODO: Compute SMD for each variable in COVARIATES. Display as a DataFrame.
balance = ...
balance

# %% [markdown]
# ## 3. Fit propensity score model

# %%
# TODO: Create race dummies from the `race` column (drop_first=True, dtype float).
#       Concatenate with COVARIATES and add a constant via sm.add_constant.
race_d = ...
X = ...

# TODO: Fit a logistic regression (`sm.Logit`) of `treat` on X.
#       Extract predicted propensity scores and clip to [0.02, 0.98].
ps_model = ...
ps = ...

print(f"Propensity scores: min={ps.min():.3f}, max={ps.max():.3f}, mean={ps.mean():.3f}")

# %% [markdown]
# ## 4. Overlap check

# %%
# TODO: Plot overlapping KDE curves of propensity scores for treated and control groups.
#       Label axes and add a legend.

# %% [markdown]
# ## 5. IPW estimate

# %%
# TODO: Implement ipw_estimate(df, ps, outcome="re78", treat="treat").
#       Weights: 1/ps for treated, 1/(1-ps) for control.
#       Return the weighted treated mean minus weighted control mean.
def ipw_estimate(df: pd.DataFrame, ps: np.ndarray,
                 outcome: str = "re78", treat: str = "treat") -> float:
    """IPW-corrected average treatment effect."""
    ...


ipw_point = ipw_estimate(df, ps.values)
print(f"IPW earnings lift: ${ipw_point:+,.0f}")

# %% [markdown]
# ## 5b. Doubly-robust check: AIPW estimator
#
# Plain IPW is unbiased only if the propensity model is correctly specified.
# The **Augmented IPW (AIPW)** estimator adds an outcome model as a second
# layer of protection: the estimate is consistent if *either* the propensity
# model or the outcome model is correctly specified — not necessarily both.
#
# Steps:
# 1. Fit an OLS outcome model of `re78` on the same covariates plus a
#    treatment indicator.
# 2. Generate counterfactual predictions: what would each person earn
#    under T=1 (`mu1`) and under T=0 (`mu0`)?
# 3. Compute the AIPW estimate:
#    `AIPW = mean[(T/ps*(Y - mu1) + mu1) - ((1-T)/(1-ps)*(Y - mu0) + mu0)]`
#
# Compare the AIPW estimate to the plain IPW estimate and the experimental
# benchmark ($1,794). Note in 1–2 sentences whether AIPW changes the ROI
# conclusion relative to IPW.
#
# *In the Nimbus project, the outcome is binary (churned_3mo), so you would
# use logistic regression instead of OLS for the outcome model.*

# %%
# TODO: Fit an OLS outcome model of `re78` on COVARIATES + race dummies +
#       `treat` indicator. Use sm.OLS.
#       Build X_out: same constant + COVARIATES + race_d + df[["treat"]].

# TODO: Generate mu1 and mu0 (predicted re78 with treat=1 and treat=0).

# TODO: Compute aipw_point using the formula above.
aipw_point = ...

print(f"IPW estimate:  ${ipw_point:+,.0f}")
print(f"AIPW estimate: ${aipw_point:+,.0f}")
print(f"Experimental:  $+1,794")

# %% [markdown]
# ## 6. Bootstrap confidence interval

# %%
# TODO: Run 500 bootstrap replicates using RNG.integers(0, len(df), len(df)).
#       On each resample, fit a new propensity model and call ipw_estimate.
#       Store results in `boots`. Skip replicates that raise exceptions.
boots = []
# TODO: implement bootstrap loop

boots = np.array(boots)
ci = np.quantile(boots, [0.025, 0.975])
print(f"Bootstrap 95% CI: [${ci[0]:+,.0f}, ${ci[1]:+,.0f}]")
print(f"Bootstrap SE: ${boots.std(ddof=1):,.0f}")

# %% [markdown]
# ## 7. Naive vs. IPW comparison

# %%
# TODO: Print a clear side-by-side comparison:
#       Naive lift, IPW lift, and the known experimental benchmark.
#       Explain in 1–2 sentences why they differ.

# %% [markdown]
# ## 8. Cost-benefit model

# %%
# TODO: Compute corrected_roi and naive_roi using COST_PER_PARTICIPANT and LTV_MULT.
#   ROI = (lift × LTV_MULT - COST_PER_PARTICIPANT) / COST_PER_PARTICIPANT
corrected_roi = ...
naive_roi     = ...

print(f"Corrected ROI: {corrected_roi:.1%}")
print(f"Naive ROI:     {naive_roi:.1%}")

# %% [markdown]
# ## 9. Sensitivity check: experimental benchmark

# %%
# TODO: Compute the ROI if the true effect equals EXPERIMENTAL_BENCH.
#       Compare to corrected_roi and naive_roi.
bench_roi = ...
print(f"Experimental-benchmark ROI: {bench_roi:.1%}")
# TODO: Add 1–2 sentences interpreting the three ROI estimates.

# %% [markdown]
# ---
# ## Connecting forward: what this means for the Nimbus project
#
# The Nimbus project's Step 2 solves the same problem on a different domain: the pilot
# markets were non-randomly assigned (urban/higher-income areas), so the junior analyst's
# naive churn-lift estimate is biased. The project uses IPW — with the same
# `ipw_estimate` function signature you implemented here — to correct for that
# confounding before feeding the lift into the cost-benefit model.
#
# Step 4 of the project then builds the cost-benefit function (`option_profit`) that
# translates the corrected churn lift directly into 12-month incremental profit — the
# same ROI logic you applied in steps 8 and 9 above, scaled to Nimbus's 4M-subscriber base.
