# Data: `loan_applicants.csv`

Simulated loan applicant data for the Ledge & Lend Group exercise.

## Variables

| Column | Description |
| --- | --- |
| `applicant_id` | Unique applicant identifier (CB-001 through CB-500) |
| `predicted_pd` | Probability of default output by the credit-risk model (0 = no default, 1 = certain default) |
| `loan_amount_usd` | Requested loan principal, in USD |
| `annual_interest_rate` | Interest rate offered to the applicant, in decimal form (e.g., 0.12 = 12%) |

## Source and calibration

The 500 applicant records are simulated. The probability-of-default distribution is a Beta(2, 6) draw — a shape commonly cited in consumer-lending risk literature, with a mode near 20% and a right tail reflecting the minority of applicants who are high-risk. Loan principal values are drawn from a uniform distribution over $3,000–$25,000, consistent with the personal-loan product tier. Interest rates are a linear function of `predicted_pd` plus noise, reflecting the industry practice of risk-based pricing.

Distribution parameters are calibrated to FDIC Statistics on Depository Institutions charge-off data for consumer installment loans (Federal Reserve Statistical Release G.19, and FDIC SDI — both public domain). Actual applicant records are not real; no personal data is included.

The "gradient boosting classifier" described in the scenario is fictional. The `predicted_pd` column in this file represents its output.

## License

This file was generated programmatically for this exercise and is released into the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
