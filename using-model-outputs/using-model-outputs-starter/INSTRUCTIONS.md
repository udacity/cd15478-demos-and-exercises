# Using Model Outputs in Decision Calculations

## Scenario

You are a decision scientist at **ClearBridge Lending**, a fictional online personal lending marketplace. ClearBridge's credit-risk team has built a gradient boosting classifier trained on three years of historical loan outcomes. For each new application, the model outputs a **probability of default (PD)** — the estimated probability that the borrower will not repay the loan.

The file `data/loan_applicants.csv` contains the model's output for 500 pending applications: `applicant_id`, `predicted_pd`, `loan_amount_usd`, and the `annual_interest_rate` ClearBridge would offer each applicant. The business question: **what probability-of-default threshold should ClearBridge use?** Applications below the threshold get approved; above it get rejected.

Three candidate thresholds are on the table:

- **Strict** — approve if PD < 15%
- **Moderate** — approve if PD < 25%
- **Permissive** — approve if PD < 40%

A stricter threshold leaves money on the table: many marginal applicants who would have repaid are turned away. A looser threshold approves too many high-risk borrowers whose expected losses exceed the interest income they generate. The model's PD output is what lets the team find the right middle.

The Head of Lending has asked the team to quantify expected total profit under each threshold and to state — with numbers — which threshold ClearBridge should adopt.

## What you'll deliver

A completed notebook (start from `using_model_outputs_starter.ipynb`) that:

1. Loads the applicant data.
2. Implements an `applicant_ev()` function that, given a single applicant's `predicted_pd`, `loan_amount_usd`, and `annual_interest_rate`, returns the **expected net profit** from approving that applicant.
3. Applies `applicant_ev()` to all 500 applicants.
4. For each of the three thresholds, filters to the approved set and computes total expected profit and approval rate.
5. Produces a side-by-side threshold comparison table.
6. Identifies the profit-maximizing threshold and explains in 1–2 sentences why the middle threshold performs best.
