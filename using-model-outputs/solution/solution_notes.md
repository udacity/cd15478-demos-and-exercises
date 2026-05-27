# Solution Walkthrough — Using Model Outputs in Decision Calculations

This is the text companion to `using_model_outputs_solution.ipynb`.

## Headline result

| Threshold | PD cutoff | Approved | Approval rate | Total EV | Portfolio SD | Expected Utility (λ=0.10) |
| --- | --- | --- | --- | --- | --- | --- |
| Strict | < 15% | 137 | 27.4% | ~$298,000 | ~$37,000 | ~$294,000 |
| **Moderate** | **< 25%** | **272** | **54.4%** | **~$489,000** | **~$80,000** | **~$481,000** |
| Permissive | < 40% | 416 | 83.2% | ~$453,000 | ~$122,000 | ~$440,000 |

**Moderate wins on both EV and expected utility.** Approving the 25–40% PD band (Permissive)
lowers EV by ~$36K *and* raises portfolio SD by ~$42K: those 144 applicants are harmful on
both dimensions. Their mean predicted LGD (~0.81) exceeds the break-even loss severity for
their interest rates, so they are net loss-makers. The risk-adjusted penalty (0.10 × $42K)
adds to that loss.

**What the LGD model changes:** A fixed LGD of 0.75 would show Moderate and Permissive as
essentially tied on EV (~$417K each), making the decision ambiguous. The per-applicant LGD
predictions reveal double jeopardy for high-risk borrowers — elevated default probability
AND elevated loss severity — which is what makes the recommendation clear.

## Key steps

1. **Provided model section.** Two sklearn models trained on `historical_loans.csv`
   (2 000 closed loans). Learners are not expected to modify this section; they read
   it to understand where `predicted_pd` and `predicted_lgd` come from.

2. **Load data.** 500 rows, 9 columns. Both model output columns (`predicted_pd`,
   `predicted_lgd`) are already present.

3. **`applicant_ev()`.** Takes four positional inputs: `predicted_pd`, `loan_amount`,
   `annual_rate`, `predicted_lgd`. No fixed LGD constant anywhere — both uncertain
   quantities come from models. The function is vectorized over pandas Series without
   `.apply()`.

4. **`applicant_variance()`.** Two outcomes (repay / default) with probabilities
   (1−PD / PD). Computes the weighted squared deviations from EV. Calls `applicant_ev()`
   internally so EV is not recomputed from scratch. The portfolio SD is
   `np.sqrt(approved["var_usd"].sum())` — independence assumed across borrowers.

5. **Expected utility.** `EU = total_ev - RISK_AVERSION × portfolio_sd`. With λ=0.10,
   the penalty for Permissive vs Moderate is 0.10 × $42K = $4.2K on top of the $36K
   EV shortfall, widening the gap to ~$41K.

4. **Threshold loop.** Filter by `predicted_pd < threshold`, then `sum()` the `ev_usd`
   column.

5. **Comparison table.** One row per threshold; styled with currency and percentage
   formatting.

6. **Recommendation.** Identify `idxmax()` of `total_ev_usd` and explain in 1–2
   sentences, naming the LGD model as the key.

## Code snippet — core function

```python
# LOAN_TERM_YEARS = 3

def applicant_ev(predicted_pd, loan_amount, annual_rate, predicted_lgd,
                 loan_term_years=LOAN_TERM_YEARS):
    interest_income = loan_amount * annual_rate * loan_term_years * (1 - predicted_pd)
    expected_loss   = loan_amount * predicted_lgd * predicted_pd
    return interest_income - expected_loss
```

## Common mistakes to flag

- **Keeping a fixed LGD constant.** Using `lgd=0.75` (copied from a simpler exercise)
  instead of `predicted_lgd`. The symptom: Moderate and Permissive are tied (~$417K
  each) rather than Moderate clearly winning.
- **Using `.apply()` for `applicant_ev()`.** The function works element-wise on pandas
  Series without `.apply()` because NumPy arithmetic is already vectorized. Using
  `.apply()` is not wrong but is unnecessary and slow.
- **Filtering with `<=` instead of `<`.** Threshold semantics are strict: `predicted_pd
  < threshold`. Using `<=` admits exactly one extra boundary applicant.
- **Confusing per-applicant EV with portfolio EV.** The per-applicant `ev_usd` column
  is diagnostic; the decision variable is the total across all approved applicants.
- **Recomputing EV inside `applicant_variance()` from scratch** rather than calling
  `applicant_ev()`. Not incorrect, but duplicates logic and diverges if one formula
  is later edited.
- **Using portfolio variance instead of portfolio SD** in the EU formula. EU =
  EV − λ × SD; if λ × Var is used instead, the penalty is on a completely different
  scale and the numbers are nonsensical.
- **Not mentioning the LGD model or portfolio SD in the recommendation.** The whole
  point is that both model outputs together — and the risk dimension — make the
  recommendation actionable.

## How this exercise feeds the project

The project's cost-benefit model follows exactly the same structure. In the Nimbus
project, `option_profit(option, lift_3mo, margin, cac, ltv_months)` takes model lift
as a float and returns a dollar profit. Here, `applicant_ev(predicted_pd, loan_amount,
annual_rate, predicted_lgd)` takes two model outputs as floats and returns a dollar
profit.

Both functions:
- Accept uncertain model outputs (lift; PD and LGD) as positional float arguments
- Return a single dollar number
- Are vectorized over pandas Series without `.apply()`

The threshold-comparison loop is the per-option loop in the project.
