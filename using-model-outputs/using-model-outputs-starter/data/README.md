# Data: `loan_applicants.csv` and `historical_loans.csv`

Simulated loan data for the Ledge & Lend Group exercise.

---

## `loan_applicants.csv`

500 pending loan applications, including credit features and the outputs of two
pre-trained credit-risk models.

| Column | Description |
| --- | --- |
| `applicant_id` | Unique applicant identifier (CB-001 through CB-500) |
| `credit_score` | Applicant credit score (540–850) |
| `annual_income_usd` | Applicant annual income, in USD |
| `debt_to_income_ratio` | Total monthly debt payments ÷ gross monthly income (0–1) |
| `employment_tenure_years` | Years at current employer |
| `loan_amount_usd` | Requested loan principal, in USD |
| `annual_interest_rate` | Interest rate offered to the applicant, in decimal form (e.g., 0.12 = 12%) |
| `predicted_pd` | **Model 1 output** — probability of default from the gradient boosting classifier (0–1) |
| `predicted_lgd` | **Model 2 output** — predicted loss given default from the gradient boosting regressor (0–1); the fraction of principal expected to be lost if the borrower defaults |

### Source and calibration

Records are simulated. `predicted_pd` is drawn from a Beta(2, 6) distribution — a shape commonly
cited in consumer-lending risk literature — and `annual_interest_rate` is a linear function of
`predicted_pd` plus noise, reflecting risk-based pricing. `predicted_lgd` is calibrated so that
higher-risk borrowers have both elevated default probability and elevated loss severity, consistent
with empirical findings in consumer credit (FDIC SDI charge-off data, Federal Reserve G.19
release). The prediction columns represent the outputs of the gradient boosting models described
in the scenario.

---

## `historical_loans.csv`

2 000 closed loans used to train both credit-risk models. Provided so that the model
training code in the notebook can be run end-to-end.

| Column | Description |
| --- | --- |
| `credit_score` | Borrower credit score at origination |
| `annual_income_usd` | Borrower annual income at origination, in USD |
| `debt_to_income_ratio` | Debt-to-income ratio at origination |
| `employment_tenure_years` | Years at employer at origination |
| `defaulted` | 1 if the borrower defaulted; 0 if the loan was repaid in full |
| `loss_given_default` | Fraction of principal lost (only observed for `defaulted == 1`; NaN otherwise) |

---

## License

Both files were generated programmatically for this exercise and are released into the
public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
