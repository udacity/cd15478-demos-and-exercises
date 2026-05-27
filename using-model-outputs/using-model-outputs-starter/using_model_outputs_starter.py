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
# **Scenario.** Ledge & Lend Group, an online lending marketplace, has two
# credit-risk models: a classifier that estimates probability of default (PD) and a
# regressor that estimates loss given default (LGD). You'll combine both model outputs
# in an expected-value function and use it to choose the profit-maximizing approval
# threshold.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for dataset details.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "data/loan_applicants.csv"
HIST_PATH = "data/historical_loans.csv"

LOAN_TERM_YEARS = 3     # 3-year personal loan
RISK_AVERSION   = 0.10  # λ: expected-utility penalty per $1 of portfolio SD
THRESHOLDS = {
    "Strict":     0.15,
    "Moderate":   0.25,
    "Permissive": 0.40,
}

# %% [markdown]
# ## Provided: How the credit-risk models were built
#
# The credit team trained both models on `historical_loans.csv` — 2 000 closed loans
# with known outcomes. **`predicted_pd` and `predicted_lgd` are already in
# `loan_applicants.csv`; you do not need to re-run this cell.** It is here so you can
# see the full pipeline from raw features to the model outputs you will use below.

# %%
# ── PROVIDED — run as-is or skip; predictions are already in the CSV ──────────
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

FEATURES = ['credit_score', 'annual_income_usd', 'debt_to_income_ratio',
            'employment_tenure_years']

hist = pd.read_csv(HIST_PATH)

# Model 1: binary classifier — will the borrower default?
clf = GradientBoostingClassifier(n_estimators=200, max_depth=3,
                                  learning_rate=0.05, random_state=42)
clf.fit(hist[FEATURES], hist['defaulted'])

# Model 2: regression — what fraction of principal is lost if the borrower defaults?
defaults = hist[hist['defaulted'] == 1]
reg = GradientBoostingRegressor(n_estimators=200, max_depth=3,
                                 learning_rate=0.05, random_state=42)
reg.fit(defaults[FEATURES], defaults['loss_given_default'])

# Both predictions are already written to loan_applicants.csv. The lines below
# show how they were generated from the two trained models:
#   applicants['predicted_pd']  = clf.predict_proba(applicants[FEATURES])[:, 1]
#   applicants['predicted_lgd'] = reg.predict(applicants[FEATURES]).clip(0.22, 0.90)
# ─────────────────────────────────────────────────────────────────────────────

# %% [markdown]
# ## 1. Load the applicant data

# %%
# TODO: Load loan_applicants.csv into a DataFrame called `applicants`. Display the first few rows.
applicants = ...

# %% [markdown]
# ## 2. Implement `applicant_ev()`
#
# The expected net profit from approving one applicant combines both model outputs:
#
# $$
# \text{EV} = \underbrace{\text{amount} \times \text{rate} \times \text{term}
#   \times (1 - \text{PD})}_{\text{expected interest income}}
# \;-\;
# \underbrace{\text{amount} \times \text{LGD} \times \text{PD}}_{\text{expected principal loss}}
# $$
#
# - The first term is interest income earned in full if the borrower repays, zero if they default.
# - The second term is the principal lost on default. **`LGD` is now model-predicted per
#   applicant** — not a single fixed constant — so higher-risk borrowers are penalised for
#   both their elevated default probability and their elevated loss severity.

# %%
# TODO: Implement applicant_ev(). Return expected net profit in USD.
def applicant_ev(predicted_pd: float, loan_amount: float, annual_rate: float,
                 predicted_lgd: float,
                 loan_term_years: float = LOAN_TERM_YEARS) -> float:
    """Expected net profit from approving one loan applicant."""
    ...


# %% [markdown]
# ## 2b. Implement `applicant_variance()`
#
# Expected value alone does not capture risk. Two portfolios can have the same EV
# but very different uncertainty profiles.
#
# Under a Bernoulli default model, each applicant has exactly two outcomes:
#
# | Event | Probability | Profit |
# |---|---|---|
# | Repays in full | $1 - \text{PD}$ | $\text{amount} \times \text{rate} \times \text{term}$ |
# | Defaults | $\text{PD}$ | $-\text{amount} \times \text{LGD}$ |
#
# The variance of a single applicant's profit is:
#
# $$
# \text{Var} = (\text{profit\_if\_repay} - \text{EV})^2 \times (1-\text{PD})
#            + (\text{loss\_if\_default} - \text{EV})^2 \times \text{PD}
# $$
#
# Assuming defaults are independent across borrowers, portfolio variance is the
# **sum** of individual variances, so portfolio SD = $\sqrt{\sum_i \text{Var}_i}$.

# %%
# TODO: Implement applicant_variance(). Return per-applicant profit variance in USD².
def applicant_variance(predicted_pd: float, loan_amount: float, annual_rate: float,
                       predicted_lgd: float,
                       loan_term_years: float = LOAN_TERM_YEARS) -> float:
    """Variance of profit for one loan applicant (Bernoulli default model)."""
    ...

# %% [markdown]
# ## 3. Apply `applicant_ev()` to the full dataset

# %%
# TODO: Add an 'ev_usd' column using applicant_ev() and a 'var_usd' column
#       using applicant_variance(). Both functions are vectorized — no .apply().

# %% [markdown]
# ## 4. Compare the three thresholds

# %%
# TODO: For each threshold in THRESHOLDS, compute:
#   - n_approved, approval_rate_pct
#   - total_ev_usd
#   - portfolio_sd  (sqrt of summed per-applicant variances)
#   - expected_utility  (total_ev_usd - RISK_AVERSION × portfolio_sd)
# Collect into a DataFrame called `comparison`.

# %% [markdown]
# ## 5. Display the comparison table

# %%
# TODO: Display `comparison` with formatted columns (currency, percentages).

# %% [markdown]
# ## 6. Identify the profit-maximizing threshold

# %%
# TODO: Print the threshold that wins on expected utility.
#       In 1-2 sentences, explain why it wins on both EV and EU — reference
#       the LGD model and the portfolio SD column.
