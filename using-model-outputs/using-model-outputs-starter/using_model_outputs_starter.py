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
# # Using Model Outputs in Decision Calculations
#
# ## Scenario
#
# You are a decision scientist at **Ledge & Lend Group** (fictional), an online
# personal lending marketplace. Ledge & Lend Group's credit-risk team has built a
# gradient boosting classifier trained on three years of historical loan
# outcomes. For each new application, the model outputs a **probability of
# default (PD)** — the estimated probability that the borrower will not repay.
#
# Your file `data/loan_applicants.csv` contains model output for 500 pending
# applications: `applicant_id`, `predicted_pd`, `loan_amount_usd`, and the
# `annual_interest_rate` Ledge & Lend Group would offer each applicant.
#
# The business question: **what probability-of-default threshold should
# Ledge & Lend Group use?**
#
# - **Strict** — approve if PD < 15%
# - **Moderate** — approve if PD < 25%
# - **Permissive** — approve if PD < 40%
#
# Your deliverable is a quantified comparison of all three thresholds — approval
# rate and expected total profit — and a defended recommendation.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the dataset
# documentation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "data/loan_applicants.csv"

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
#
# Load `data/loan_applicants.csv`. Display the first few rows and confirm the
# shape (500 rows, 4 columns).

# %%
# TODO: Read the CSV into a DataFrame called `applicants`.
applicants = ...

# %% [markdown]
# ## 2. Implement `applicant_ev()`
#
# Write a function that computes the **expected net profit** from approving a
# single loan applicant. The formula is:
#
# $$\text{EV} = \text{loan\_amount} \times \text{annual\_rate} \times
# \text{LOAN\_TERM\_YEARS} \times (1 - \text{PD}) -
# \text{loan\_amount} \times \text{LGD} \times \text{PD}$$
#
# The first term is expected interest income (earned only if the borrower
# repays). The second term is expected principal loss (incurred if the
# borrower defaults).

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
    # TODO: implement the formula above.
    ...


# %% [markdown]
# ## 3. Apply `applicant_ev()` to the full dataset
#
# Compute expected profit for every applicant and store it as a new column
# `ev_usd` in the `applicants` DataFrame. Display a few rows to spot-check.

# %%
# TODO: Add an `ev_usd` column to `applicants`.

# %% [markdown]
# ## 4. Compare the three thresholds
#
# For each threshold in `THRESHOLDS`, filter `applicants` to those with
# `predicted_pd` below the threshold. Compute:
#
# - **n_approved**: number of applicants approved
# - **approval_rate**: share approved out of 500 (as a percentage)
# - **total_ev_usd**: sum of `ev_usd` for approved applicants
#
# Collect the results into a DataFrame called `comparison` with one row per
# threshold.

# %%
# TODO: Build the `comparison` DataFrame.
comparison = ...

# %% [markdown]
# ## 5. Display the comparison table
#
# Display `comparison` with dollar amounts formatted so they are easy to read.

# %%
# TODO: Display `comparison`.

# %% [markdown]
# ## 6. Identify the profit-maximizing threshold
#
# Print the name of the threshold that produces the highest `total_ev_usd`.
# In 1–2 sentences, explain why the middle threshold outperforms both the
# strictest and most permissive option — use the numbers from your table.

# %%
# TODO: Print the profit-maximizing threshold name and its total expected profit.

# %% [markdown]
# *TODO: write your 1–2 sentence explanation here.*
