# Solution Walkthrough — Using Model Outputs in Decision Calculations

This is the text companion to `using_model_outputs_solution.ipynb`. It summarizes the key steps, the numbers a learner should arrive at, and the most common mistakes to flag.

## Headline result

| Threshold | PD cutoff | Approved | Approval rate | Total expected profit |
| --- | --- | --- | --- | --- |
| Strict | < 15% | 137 | 27.4% | ~$260,000 |
| **Moderate** | **< 25%** | **272** | **54.4%** | **~$417,000** |
| Permissive | < 40% | 416 | 83.2% | ~$417,000 |

**Moderate maximizes total expected profit** (ties Permissive within rounding, but the 25%–40% PD band adds essentially zero mean EV — making Moderate the right recommendation on a risk-adjusted basis). The 135 marginal applicants added under Moderate (PD 15%–25%) have positive mean EV and lift total profit by ~$157K. The additional 144 applicants in the 25%–40% PD band are marginal at baseline LGD: their mean EV is near zero, so they do not improve portfolio profit.

**Sensitivity flex (LGD = 0.85):** Moderate clearly wins (~$361K vs. ~$302K for Permissive). Higher loss severity turns the 25%–40% PD band clearly negative, widening the advantage of Moderate and making the recommendation more robust.

## Key steps

1. **Load the data.** 500 rows, 4 columns. `predicted_pd` is already the model output — no modeling is needed.
2. **Implement `applicant_ev()`.** Takes `predicted_pd`, `loan_amount`, and `annual_rate` as positional arguments; `loan_term_years` and `lgd` as keyword arguments with module-level defaults. Returns a single dollar number. This mirrors the project's `option_profit()` idiom exactly.
3. **Apply row-wise.** The function is vectorized over pandas Series — `applicant_ev(df["predicted_pd"], df["loan_amount_usd"], df["annual_interest_rate"])` works without `.apply()`.
4. **Threshold loop.** Filter by `predicted_pd < threshold`, then `sum()` the `ev_usd` column.
5. **Comparison table.** One row per threshold, columns for approval count, approval rate, and total EV.
6. **Defend the recommendation.** Moderate wins because the marginal 15%–25% PD band adds value on net; the marginal 25%–40% PD band destroys it.
7. **Sensitivity flex.** Pass `lgd=0.85` as a keyword argument to the same `applicant_ev()` call. The profit-maximizing threshold does not change.

## Code snippet — core function

```python
# LOAN_TERM_YEARS = 3
# LOSS_GIVEN_DEFAULT = 0.75

def applicant_ev(predicted_pd: float, loan_amount: float, annual_rate: float,
                 loan_term_years: float = LOAN_TERM_YEARS,
                 lgd: float = LOSS_GIVEN_DEFAULT) -> float:
    """Expected net profit from approving one loan applicant."""
    interest_income = loan_amount * annual_rate * loan_term_years * (1 - predicted_pd)
    expected_loss   = loan_amount * lgd * predicted_pd
    return interest_income - expected_loss
```

## Common mistakes to flag

- **Using `.apply()` for `applicant_ev()`.** The function works element-wise on pandas Series without `.apply()` because NumPy arithmetic is already vectorized. Using `.apply()` is not wrong, but it is unnecessary and slow.
- **Filtering with `<=` instead of `<`.** The threshold semantics are strict: `predicted_pd < threshold`. Using `<=` admits exactly one extra applicant at the boundary and should not materially change results, but it contradicts the stated policy.
- **Confusing EV per applicant with total portfolio EV.** The per-applicant EV column is a diagnostic; the decision variable is the total across all approved applicants.
- **Hardcoding the LGD in the function body.** The function signature must accept `lgd` as a keyword argument so the sensitivity flex can pass `lgd=0.85` without copying the function.
- **Rounding `predicted_pd` before the threshold comparison.** Rounding to two decimal places changes which applicants are approved at the 15% and 25% boundaries.
- **Treating the Permissive result as proof that "approving more is always bad."** The point is subtler: the 25%–40% PD band is marginal at baseline LGD — it neither adds nor subtracts meaningfully from total portfolio profit. What destroys value is approving well above 40%, or operating in a high-LGD environment without tightening. The threshold choice is always conditional on the LGD and rate assumptions.

## How this exercise feeds the project

The project's Step 4 (cost-benefit model) follows exactly the same structure. In the Nimbus project, `option_profit(option, lift_3mo, margin, cac, ltv_months)` takes the model's lift estimate as a float and returns a dollar profit for one option. Here, `applicant_ev(predicted_pd, loan_amount, annual_rate)` takes the classifier's PD output as a float and returns a dollar profit for one applicant.

Both functions:
- Accept uncertain model output (lift, probability of default) as a positional float argument
- Accept business parameters (CAC, LTV months; LGD, loan term) as keyword arguments with module-level defaults
- Return a single dollar number

The threshold-comparison loop in this exercise is the per-option loop in the project. "Which threshold maximizes total expected profit?" is structurally identical to "Which campaign option maximizes expected contribution?" The project adds another layer — aggregating across a probabilistic uncertainty distribution rather than a fixed applicant table — but the function interface is the same.

A learner who can implement and use `applicant_ev()` correctly has the core idiom needed to read, extend, and debug `option_profit()` in the project.
