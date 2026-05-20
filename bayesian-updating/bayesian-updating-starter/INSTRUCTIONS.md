# Updating Demand Beliefs with Bayesian Methods

## Scenario

You are the demand planning analyst at **FreshCart**, a fictional grocery chain piloting a new
"Premium Meal Kit" subscription add-on. Customers pre-order weekly meal kits at checkout for
pickup the following week. FreshCart must commit their order to the supplier two weeks in advance,
before seeing actual pickup demand — which means pre-ordering too many leads to food waste and
pre-ordering too few leaves customers without their kits.

The key unknown is **mean weekly demand per store** (in units). You don't know this before the
pilot, but you do have an industry benchmark from real US grocery sales data to set a starting
point. As pilot stores report weekly scan data, you'll update your belief twice — first after
the pilot's first four weeks, then again after weeks five through eight — using the
Normal-Normal conjugate update. Each update sharpens your belief and shifts your recommended
pre-order quantity.

To anchor the starting point, the file `data/grocery_industry_benchmarks.csv` contains real
monthly US grocery store sales from [FRED](https://fred.stlouisfed.org/series/MRTSSM4451USS)
(US Census Bureau Monthly Retail Trade Survey, NAICS 4451, public domain). From those sales
figures you'll derive the prior mean. The prior standard deviation is set wider than historical
sales variability to reflect new-product uncertainty.

## What you'll deliver

A completed Jupyter notebook (start from `bayesian_updating_starter.ipynb`) that:

1. Loads the FRED grocery sales data and derives the prior mean demand from it. Uses the
   provided constants for prior standard deviation and average meal-kit price.
2. Loads the pilot scan data and separates it into two batches (weeks 1–4 and weeks 5–8).
3. Computes batch-level likelihood parameters for each batch: the sample mean and standard
   error of the weekly unit counts.
4. Implements `normal_update(prior_mu, prior_sd, lik_mu, lik_sd)` — the closed-form
   Normal-Normal conjugate update — and returns the posterior mean and standard deviation.
5. Applies the first update: prior + batch 1 likelihood → Posterior 1.
6. Applies the second update: Posterior 1 + batch 2 likelihood → Posterior 2.
7. Plots all three distributions (prior, Posterior 1, Posterior 2) overlaid on one axes,
   showing how the belief sharpens with each update.
8. Computes the recommended pre-order quantity `Q` under each belief state, using the formula
   `Q = posterior_mean + Q_BUFFER × posterior_sd`. Report how Q changes across the three states.
9. Sensitivity check: repeat Update 1 with `prior_sd × 2`. Show how a more uncertain prior
   gives the batch-1 data more influence over the posterior.

## Requirements

- Your notebook must run top to bottom without errors.
- The prior mean must be derived from the FRED grocery data — don't hardcode it.
- `normal_update` must use precision-weighted arithmetic (the same formula used in the project).
- The three-distribution plot must have a legend and labeled axes.
- The sensitivity result for step 9 must show a quantitative comparison (e.g., print the
  Posterior 1 mean under original vs. doubled prior sd).

## Resources you may find useful

- [FRED: MRTSSM4451USS — Grocery Stores](https://fred.stlouisfed.org/series/MRTSSM4451USS) — the source for the benchmark data
- [Wikipedia: Conjugate prior — Normal with known variance](https://en.wikipedia.org/wiki/Conjugate_prior#When_likelihood_function_is_a_continuous_distribution) — concise derivation of the precision-weighted update
- [scipy.stats.norm](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html) — for evaluating and plotting Normal pdfs

## Note on the data

`data/grocery_industry_benchmarks.csv` contains real monthly US grocery store sales from the
Federal Reserve Economic Data (FRED) series MRTSSM4451USS (US Census Bureau Monthly Retail
Trade Survey, NAICS 4451, public domain). `data/pilot_scan_data.csv` is synthetic — generated
to illustrate a realistic demand trajectory for a new meal-kit program. The scenario company
**FreshCart** is fictional; the grocery market data is real.
