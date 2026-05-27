# Using Model Outputs in Decision Calculations

## Scenario

You are a decision scientist at **Ledge & Lend Group**, an online personal lending
marketplace. The credit team has trained two models on three years of closed-loan outcomes:

- **Model 1 — Default Risk Classifier** (`GradientBoostingClassifier`): predicts the probability
  that a borrower will default (`predicted_pd`).
- **Model 2 — Loss Severity Regressor** (`GradientBoostingRegressor`): predicts the fraction of
  principal that will be lost if a borrower defaults (`predicted_lgd`). Lower-risk borrowers tend
  to partially repay or respond to collections; higher-risk borrowers tend to disappear, resulting
  in a larger loss.

The file `data/loan_applicants.csv` contains the two models' outputs for 500 pending applications,
alongside each applicant's credit features and the loan terms Ledge & Lend Group would offer.

The business question: **what probability-of-default threshold should Ledge & Lend Group use?**
Applications below the threshold get approved; above it get rejected.

Three candidate thresholds are on the table:

- **Strict** — approve if PD < 15%
- **Moderate** — approve if PD < 25%
- **Permissive** — approve if PD < 40%

The Head of Lending has asked you to quantify expected total profit **and portfolio risk** under
each threshold — using **both** model outputs — and state with numbers which threshold to adopt.

## What you'll deliver

A completed notebook (start from `using_model_outputs_starter.ipynb`) that:

1. Loads the applicant data (the provided model-training cells are already in the notebook for
   context; you do not need to re-run them).
2. Implements an `applicant_ev()` function that, given a single applicant's `predicted_pd`,
   `loan_amount_usd`, `annual_interest_rate`, and `predicted_lgd`, returns the **expected net
   profit** from approving that applicant.
3. Implements an `applicant_variance()` function that returns the **profit variance** for one
   applicant under a Bernoulli default model (two outcomes: repay or default).
4. Applies both functions to all 500 applicants.
5. For each of the three thresholds, filters to the approved set and computes total expected
   profit, portfolio standard deviation, and **expected utility**
   (EU = total EV − λ × portfolio SD, where λ = 0.10).
6. Produces a side-by-side threshold comparison table.
7. Identifies the threshold that maximises expected utility and explains in 1–2 sentences why it
   wins on **both** EV and EU — referencing the LGD model and the portfolio SD column.
