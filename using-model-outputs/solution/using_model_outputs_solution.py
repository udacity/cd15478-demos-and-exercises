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
# `using_model_outputs_solution.ipynb`. The canonical artifact for learners is
# the notebook (.ipynb); this script is provided for code review and `git diff`
# readability. Run `jupytext --sync` to keep the two in lockstep after edits.

# %% [markdown]
# # Using Model Outputs in Decision Calculations (SOLUTION)
#
# ## Scenario
#
# You are a decision scientist at **Ledge & Lend Group** (fictional), an online
# personal lending marketplace. Ledge & Lend Group's credit-risk team has built a
# gradient boosting classifier trained on three years of historical loan
# outcomes. For each new application, the model outputs a **probability of
# default (PD)** — the estimated probability that the borrower will not repay.
#
# The file `../using-model-outputs-starter/data/loan_applicants.csv` contains
# model output for 500 pending applications: `applicant_id`, `predicted_pd`,
# `loan_amount_usd`, and the `annual_interest_rate` Ledge & Lend Group would offer
# each applicant.
#
# The business question: **what probability-of-default threshold should
# Ledge & Lend Group use?** Applications below the threshold get approved; above it
# get rejected.
#
# Three candidate thresholds:
#
# - **Strict** — approve if PD < 15%
# - **Moderate** — approve if PD < 25%
# - **Permissive** — approve if PD < 40%
#
# The deliverable is a quantified comparison of all three thresholds — approval
# rate and expected total profit — and a defended recommendation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "../using-model-outputs-starter/data/loan_applicants.csv"

# Constants — loan product parameters
LOAN_TERM_YEARS = 3        # 3-year personal loan
LOSS_GIVEN_DEFAULT = 0.75  # 75% of principal lost on default; 25% recovered

# Approval thresholds
THRESHOLDS = {
    "Strict":     0.15,
    "Moderate":   0.25,
    "Permissive": 0.40,
}

# %% [markdown]
# ## 1. Load the data

# %%
applicants = pd.read_csv(DATA_PATH)
display(applicants.head())
print(f"Shape: {applicants.shape}")

# %% [markdown]
# ## 2. Implement `applicant_ev()`
#
# The expected net profit from approving a single applicant is:
#
# $$\text{EV} = \text{loan\_amount} \times \text{annual\_rate} \times
# \text{LOAN\_TERM\_YEARS} \times (1 - \text{PD}) -
# \text{loan\_amount} \times \text{LGD} \times \text{PD}$$
#
# The first term is expected interest income — earned in full if the borrower
# repays, zero otherwise. The second term is expected principal loss — incurred
# in full (less recoveries) if the borrower defaults, zero otherwise. LGD = 0.75
# means 75% of principal is lost; 25% is recovered via collections.

# %%
def applicant_ev(predicted_pd: float, loan_amount: float, annual_rate: float,
                 loan_term_years: float = LOAN_TERM_YEARS,
                 lgd: float = LOSS_GIVEN_DEFAULT) -> float:
    """Expected net profit from approving one loan applicant.

    Parameters
    ----------
    predicted_pd : float
        Model-output probability of default (0–1).
    loan_amount : float
        Requested principal in USD.
    annual_rate : float
        Annual interest rate offered, in decimal form (e.g., 0.12 = 12%).
    loan_term_years : float
        Loan term in years.
    lgd : float
        Loss given default as a fraction of principal (e.g., 0.75 means
        75% of principal is lost; 25% is recovered via collections).

    Returns
    -------
    float
        Expected net profit in USD.
    """
    interest_income = loan_amount * annual_rate * loan_term_years * (1 - predicted_pd)
    expected_loss = loan_amount * lgd * predicted_pd
    return interest_income - expected_loss


# %% [markdown]
# ## 3. Apply `applicant_ev()` to the full dataset

# %%
applicants["ev_usd"] = applicant_ev(
    applicants["predicted_pd"],
    applicants["loan_amount_usd"],
    applicants["annual_interest_rate"],
)
display(applicants.head())

# %% [markdown]
# ## 4. Compare the three thresholds

# %%
rows = []
for name, thresh in THRESHOLDS.items():
    approved = applicants[applicants["predicted_pd"] < thresh]
    rows.append({
        "threshold": name,
        "pd_cutoff": thresh,
        "n_approved": len(approved),
        "approval_rate_pct": round(100 * len(approved) / len(applicants), 1),
        "total_ev_usd": approved["ev_usd"].sum(),
    })

comparison = pd.DataFrame(rows).set_index("threshold")

# %% [markdown]
# ## 5. Display the comparison table

# %%
display(
    comparison.style.format({
        "pd_cutoff": "{:.0%}",
        "approval_rate_pct": "{:.1f}%",
        "total_ev_usd": "${:,.0f}",
    })
)

# %% [markdown]
# ## 6. Identify the profit-maximizing threshold

# %%
best = comparison["total_ev_usd"].idxmax()
best_ev = comparison.loc[best, "total_ev_usd"]
print(f"Profit-maximizing threshold: {best}  (total EV = ${best_ev:,.0f})")

# %% [markdown]
# **Moderate (PD < 25%) maximizes expected total profit.** Strict leaves money
# on the table: the 135 additional applicants approved under Moderate have
# positive mean EV, so including them adds ~$157K to portfolio profit.
# Permissive adds a further 144 applicants in the 25%–40% PD band whose mean
# expected EV is essentially zero — the higher default losses on that group
# just offset their interest income, leaving total profit flat or slightly
# below Moderate.
