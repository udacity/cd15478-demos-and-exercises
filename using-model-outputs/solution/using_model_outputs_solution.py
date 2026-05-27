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
# Ledge & Lend Group has two credit-risk models: a gradient boosting
# classifier that predicts the probability of default (`predicted_pd`) and a gradient
# boosting regressor that predicts loss given default (`predicted_lgd`). Both outputs
# are combined in an expected-value function to choose the profit-maximizing approval
# threshold from three candidates: Strict (PD < 15%), Moderate (PD < 25%), Permissive
# (PD < 40%).

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "../using-model-outputs-starter/data/loan_applicants.csv"
HIST_PATH = "../using-model-outputs-starter/data/historical_loans.csv"

LOAN_TERM_YEARS = 3     # 3-year personal loan
RISK_AVERSION   = 0.10  # λ: expected-utility penalty per $1 of portfolio SD
THRESHOLDS = {
    "Strict":     0.15,
    "Moderate":   0.25,
    "Permissive": 0.40,
}

# %% [markdown]
# ## Provided: How the credit-risk models were built

# %%
# ── PROVIDED — predictions are already in loan_applicants.csv ─────────────────
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

FEATURES = ['credit_score', 'annual_income_usd', 'debt_to_income_ratio',
            'employment_tenure_years']

hist = pd.read_csv(HIST_PATH)

clf = GradientBoostingClassifier(n_estimators=200, max_depth=3,
                                  learning_rate=0.05, random_state=42)
clf.fit(hist[FEATURES], hist['defaulted'])

defaults = hist[hist['defaulted'] == 1]
reg = GradientBoostingRegressor(n_estimators=200, max_depth=3,
                                 learning_rate=0.05, random_state=42)
reg.fit(defaults[FEATURES], defaults['loss_given_default'])

#   applicants['predicted_pd']  = clf.predict_proba(applicants[FEATURES])[:, 1]
#   applicants['predicted_lgd'] = reg.predict(applicants[FEATURES]).clip(0.22, 0.90)
# ─────────────────────────────────────────────────────────────────────────────

# %% [markdown]
# ## 1. Load the applicant data

# %%
applicants = pd.read_csv(DATA_PATH)
print(f"Shape: {applicants.shape}")
applicants.head()

# %% [markdown]
# ## 2. Implement `applicant_ev()`
#
# Both model outputs enter the formula directly:
#
# $$
# \text{EV} = \text{amount} \times \text{rate} \times \text{term}
#   \times (1 - \text{PD})
# \;-\;
# \text{amount} \times \text{LGD} \times \text{PD}
# $$
#
# `predicted_lgd` replaces the fixed constant used in simpler approaches.
# Higher-risk applicants have both elevated PD and elevated LGD, so they are
# penalised on both sides of the equation.

# %%
def applicant_ev(predicted_pd: float, loan_amount: float, annual_rate: float,
                 predicted_lgd: float,
                 loan_term_years: float = LOAN_TERM_YEARS) -> float:
    """Expected net profit from approving one loan applicant."""
    interest_income = loan_amount * annual_rate * loan_term_years * (1 - predicted_pd)
    expected_loss   = loan_amount * predicted_lgd * predicted_pd
    return interest_income - expected_loss

# %% [markdown]
# ## 2b. Implement `applicant_variance()`
#
# Under a Bernoulli default model, each applicant has two outcomes: repay (earn
# interest) or default (lose LGD × principal). The variance of that distribution
# measures how much the actual outcome could differ from the expected profit.
# Portfolio variance is the sum of individual variances (independent defaults).

# %%
def applicant_variance(predicted_pd: float, loan_amount: float, annual_rate: float,
                       predicted_lgd: float,
                       loan_term_years: float = LOAN_TERM_YEARS) -> float:
    """Variance of profit for one loan applicant (Bernoulli default model)."""
    profit_if_repay =  loan_amount * annual_rate * loan_term_years
    loss_if_default = -loan_amount * predicted_lgd
    ev = applicant_ev(predicted_pd, loan_amount, annual_rate, predicted_lgd, loan_term_years)
    return (profit_if_repay - ev)**2 * (1 - predicted_pd) + (loss_if_default - ev)**2 * predicted_pd

# %% [markdown]
# ## 3. Apply both functions to the full dataset

# %%
applicants["ev_usd"]  = applicant_ev(
    applicants["predicted_pd"],
    applicants["loan_amount_usd"],
    applicants["annual_interest_rate"],
    applicants["predicted_lgd"],
)
applicants["var_usd"] = applicant_variance(
    applicants["predicted_pd"],
    applicants["loan_amount_usd"],
    applicants["annual_interest_rate"],
    applicants["predicted_lgd"],
)
applicants.head()

# %% [markdown]
# ## 4. Compare the three thresholds

# %%
rows = []
for name, thresh in THRESHOLDS.items():
    approved = applicants[applicants["predicted_pd"] < thresh]
    total_ev  = approved["ev_usd"].sum()
    port_sd   = np.sqrt(approved["var_usd"].sum())
    rows.append({
        "threshold":         name,
        "pd_cutoff":         thresh,
        "n_approved":        len(approved),
        "approval_rate_pct": round(100 * len(approved) / len(applicants), 1),
        "total_ev_usd":      total_ev,
        "portfolio_sd":      port_sd,
        "expected_utility":  total_ev - RISK_AVERSION * port_sd,
    })

comparison = pd.DataFrame(rows).set_index("threshold")

# %% [markdown]
# ## 5. Display the comparison table

# %%
comparison.style.format({
    "pd_cutoff":         "{:.0%}",
    "approval_rate_pct": "{:.1f}%",
    "total_ev_usd":      "${:,.0f}",
    "portfolio_sd":      "${:,.0f}",
    "expected_utility":  "${:,.0f}",
})

# %% [markdown]
# ## 6. Identify the profit-maximizing threshold

# %%
best_eu = comparison["expected_utility"].idxmax()
best_ev = comparison["total_ev_usd"].idxmax()
print(f"Expected-utility winner: {best_eu}  (EU = ${comparison.loc[best_eu, 'expected_utility']:,.0f})")
print(f"Expected-value winner:   {best_ev}  (EV = ${comparison.loc[best_ev, 'total_ev_usd']:,.0f})")

# %% [markdown]
# **Moderate (PD < 25%) wins on both expected value and expected utility.**
# Approving the 25–40% PD band (Permissive) lowers EV by ~$36K *and* raises
# portfolio SD by ~$42K: those 144 applicants are harmful on both dimensions.
# Their mean predicted LGD (~0.81) exceeds the break-even loss severity for their
# interest rates, so they are net loss-makers. The risk-adjusted penalty
# (λ × ΔSD = 0.10 × $42K = $4.2K) adds to that loss rather than offsetting it.
# A fixed LGD assumption would mask this by showing Moderate and Permissive as tied.
