# Updating Demand Beliefs with Bayesian Methods

## Scenario

You are the demand planning analyst at **Chapter & Craft**, a fictional bookstore and hobby
retail chain piloting a new "Curated Reader's Box" — a themed book-and-craft-kit subscription.
Customers reserve a box each week at checkout during an 8-week pilot. Chapter & Craft must place
its box-assembly order (book copies plus kit components) with suppliers two weeks in advance of
ship date, before seeing that week's final reservation count — which means over-ordering wastes
inventory and under-ordering leaves subscribers without a box.

The key unknown is **mean weekly demand per store** (in units). You don't know this before the
pilot, but you do have an industry benchmark from real US retail sales data to set a starting
point. As pilot stores report weekly reservation counts, you'll update your belief twice — first
after the pilot's first four weeks, then again after weeks five through eight — using the
Normal-Normal conjugate update. Each update sharpens your belief and shifts your recommended
pre-order quantity.

To anchor the starting point, the file `data/hobby_book_industry_benchmarks.csv` contains real
monthly US sporting goods, hobby, musical instrument, and book store sales from
[FRED](https://fred.stlouisfed.org/series/MRTSSM451USS) (US Census Bureau Monthly Retail Trade
Survey, NAICS 451, public domain). From those sales figures you'll derive the prior mean. The
prior standard deviation is set wider than historical sales variability to reflect new-product
uncertainty.

## What you'll deliver

A completed Jupyter notebook (start from `bayesian_updating_starter.ipynb`) that:

1. Loads the FRED hobby/book sales data and derives the prior mean demand from it. Uses the
   provided constants for prior standard deviation and average box price.
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
