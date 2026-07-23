# Updating Demand Beliefs with Bayesian Methods

## Scenario

You are the demand planning analyst at **Chapter & Craft**, a fictional bookstore and hobby
retail chain piloting a new "Curated Reader's Box" — a themed book-and-craft-kit subscription.
Customers reserve a box each week at checkout during an 8-week pilot. Chapter & Craft must place
its box-assembly order (book copies plus kit components) with suppliers two weeks in advance of
ship date, before seeing that week's final reservation count — which means over-ordering wastes
inventory and under-ordering leaves subscribers without a box.

The key unknown is **mean weekly demand per store** (in units). You don't know this before the
pilot, but you do have an industry benchmark from US retail sales data to set a starting
point. As pilot stores report weekly reservation counts, you'll update your belief twice — first
after the pilot's first four weeks, then again after weeks five through eight — using the
Normal-Normal conjugate update. Each update sharpens your belief and shifts your recommended
pre-order quantity.

Work through the batches in the order they actually arrive. Pilot data is split across two
files — `pilot_scan_data_weeks1_4.csv` and `pilot_scan_data_weeks5_8.csv` — so that you load
and use only weeks 1–4 to compute Posterior 1, and don't touch the weeks 5–8 file until after
that update is done. Loading both upfront would make the first update look like it already
knew what batch 2 would show.

To anchor the starting point, the file `data/hobby_book_industry_benchmarks.csv` contains
monthly US sporting goods, hobby, musical instrument, and book store sales (US Census Bureau
Monthly Retail Trade Survey, public domain — see `data/README.md` for the full citation).
From those sales figures you'll derive the prior mean. The prior standard deviation is set
wider than historical sales variability to reflect new-product uncertainty.

## What you'll deliver

A completed Jupyter notebook (start from `bayesian_updating_starter.ipynb`) that:

1. Loads the hobby/book sales data and derives the prior mean demand from it. Uses the
   provided constants for prior standard deviation and average box price.
2. Loads `pilot_scan_data_weeks1_4.csv`, the first batch of pilot data.
3. Computes batch 1's likelihood parameters: the sample mean and standard error of the
   weekly unit counts.
4. Implements `normal_update(prior_mu, prior_sd, lik_mu, lik_sd)` — the closed-form
   Normal-Normal conjugate update — and returns the posterior mean and standard deviation.
5. Applies the first update: prior + batch 1 likelihood → Posterior 1.
6. Loads `pilot_scan_data_weeks5_8.csv`, the second batch of pilot data, now that Posterior 1
   is in hand.
7. Computes batch 2's likelihood parameters.
8. Applies the second update: Posterior 1 + batch 2 likelihood → Posterior 2.
9. Plots all three distributions (prior, Posterior 1, Posterior 2) overlaid on one axes,
   showing how the belief sharpens with each update.
10. Computes the recommended pre-order quantity `Q` under each belief state, using the formula
    `Q = posterior_mean + Q_BUFFER × posterior_sd`. Report how Q changes across the three states.
